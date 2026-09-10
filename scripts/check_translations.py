#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic validator for the Japanese curriculum translation (weeks 02-24).

Single-file tool, Python 3.12+, standard library only.
Run with:  uv run scripts/check_translations.py <command>

Commands
--------
  --init                                     Build scripts/translation_baseline.json and
                                             curriculum/translation-review-state.json (both must
                                             not exist yet; exit 2 otherwise). Unparseable quiz
                                             -> exit 3 with source:line on stderr.
  --mode translation --weeks A-B             Check JA structural fidelity for weeks A..B.
  --mode review --weeks A-B                  Check recorded review results for weeks A..B.
  --mode full (default)                      translation (all 69) + review (all 69) + index +
                                             report checks.
  --accept-translation --source P            Mark row translated; record measured jaHash.
  --begin-translation --source P --assignment S   attempt++ (max 2), status in_progress.
  --begin-review --source P --reviewer S     Set reviewerAssignment (row must be translated).
  --record-review --source P --payload F     Record reviewResult; approved -> reviewStatus
                                             approved (quality complete), else rejected.
  --finalize                                 All rows approved -> P9_READY / ready_for_verification.
  --render-report                            Write curriculum/translation-review.md
                                             (requires ready_for_verification).
  --self-test                                Run the offline fixture test suite.

Exit codes: 0 pass/done, 1 check failures ("FILE: reason" lines on stdout), 2 usage or
state/precondition error (state file is never modified on error), 3 quiz parse failure at --init.

Canonical JSON: json.dumps(sort_keys=True, ensure_ascii=True, separators=(',',':'),
allow_nan=False); saved files are canonical JSON + trailing "\\n". Digests are sha256 over the
canonical UTF-8 bytes of the payload with the digest field itself removed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 1
REPORT_FORMAT_VERSION = 1
WEEKS = list(range(2, 25))  # 02..24
SOURCE_FILES = ("README.md", "exercises.md", "quiz.md")
MAX_TRANSLATION_ATTEMPTS = 2

QUALITY_KEYS = (
    "paragraphCoverage",
    "semanticEquivalence",
    "omissionAddition",
    "naturalness",
    "termConsistency",
    "negationConditionsCausality",
    "numbersIdentifiers",
    "quizAnswer",
)
QUALITY_VALUES = {"pass", "na", "fail"}

TRANSLATION_STATUSES = {"pending", "in_progress", "translated"}
REVIEW_STATUSES = {"pending", "approved", "rejected"}
EXECUTION_STATUSES = {"active", "ready_for_verification"}

BASELINE_REL = "scripts/translation_baseline.json"
STATE_REL = "curriculum/translation-review-state.json"
REPORT_REL = "curriculum/translation-review.md"
INDEX_JA_REL = "curriculum/README.ja.md"

ACTION_FLAGS = (
    "accept_translation",
    "begin_translation",
    "begin_review",
    "record_review",
    "finalize",
    "render_report",
)

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def die(msg: str, code: int = 2) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha1_hex(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def canonical_dumps(payload: object) -> str:
    return json.dumps(
        payload, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False
    )


def digest_payload(payload: dict, skip_field: str) -> str:
    body = {k: v for k, v in payload.items() if k != skip_field}
    return sha256_bytes(canonical_dumps(body).encode("utf-8"))


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / f".{path.name}.tmp{os.getpid()}"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def atomic_write_json(path: Path, payload: dict) -> None:
    atomic_write_bytes(path, (canonical_dumps(payload) + "\n").encode("utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------


def source_paths(weeks: list[int] | None = None) -> list[str]:
    weeks = weeks if weeks is not None else WEEKS
    out = []
    for w in weeks:
        for name in SOURCE_FILES:
            out.append(f"curriculum/week-{w:02d}/{name}")
    return out


def ja_path_for(source: str) -> str:
    stem, ext = source.rsplit(".", 1)
    return f"{stem}.ja.{ext}"


def week_of(source: str) -> int:
    m = re.match(r"^curriculum/week-(\d{2})/", source)
    if not m:
        die(f"unexpected source path: {source}")
    return int(m.group(1))


def batch_id(week: int) -> str:
    idx = (week - 2) // 5
    start = 2 + idx * 5
    end = min(start + 4, 24)
    return f"{start:02d}-{end:02d}"


def discover_notebooks(root: Path) -> list[str]:
    nbs = sorted(root.glob("curriculum/week-*/notebooks/*.ipynb"))
    return [p.relative_to(root).as_posix() for p in nbs]


def week_notebook_map(nb_paths: list[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for rel in nb_paths:
        week = rel.split("/")[1].replace("week-", "")
        if int(week) not in WEEKS:
            continue
        out.setdefault(week, []).append(Path(rel).name)
    for v in out.values():
        v.sort()
    return dict(sorted(out.items()))


def git_head(root: Path) -> str:
    """git rev-parse HEAD; 'unknown' if root is not inside a git repo (self-test fixture)."""
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True
        )
        return proc.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


# ---------------------------------------------------------------------------
# Markdown analysis
# ---------------------------------------------------------------------------


def fence_infos(text: str) -> list[str]:
    """Info strings of each opening fence, in order (fence count == len)."""
    infos: list[str] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```"):
            if not in_fence:
                infos.append(stripped[3:].strip())
            in_fence = not in_fence
    return infos


def non_fence_lines(text: str) -> list[str]:
    """Lines outside fenced code blocks (fence marker lines themselves excluded)."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return out


def heading_levels(text: str) -> list[int]:
    levels: list[int] = []
    for line in non_fence_lines(text):
        m = re.match(r"^(#{1,6})(\s|$)", line)
        if m:
            levels.append(len(m.group(1)))
    return levels


def table_shapes(text: str) -> list[list[int]]:
    shapes: list[list[int]] = []
    cur: list[str] = []
    for line in non_fence_lines(text):
        if line.lstrip().startswith("|"):
            cur.append(line)
        elif cur:
            shapes.append([row.count("|") - 1 for row in cur])
            cur = []
    if cur:
        shapes.append([row.count("|") - 1 for row in cur])
    return shapes


def code_span_ranges(text: str) -> list[tuple[int, int, str]]:
    """CommonMark-ish inline code spans: (start, end, content)."""
    ranges: list[tuple[int, int, str]] = []
    i, n = 0, len(text)
    while i < n:
        if text[i] != "`":
            i += 1
            continue
        j = i
        while j < n and text[j] == "`":
            j += 1
        run = j - i
        k = j
        while k < n:
            if text[k] == "`":
                k2 = k
                while k2 < n and text[k2] == "`":
                    k2 += 1
                if k2 - k == run:
                    ranges.append((i, k2, text[j:k]))
                    i = k2
                    break
                k = k2
            else:
                k += 1
        else:
            i = j
    return ranges


def inline_code_spans(text: str) -> list[str]:
    return [content for _, _, content in code_span_ranges("\n".join(non_fence_lines(text)))]


def strip_code_spans(text: str) -> str:
    ranges = code_span_ranges(text)
    if not ranges:
        return text
    out: list[str] = []
    pos = 0
    for start, end, _content in ranges:
        out.append(text[pos:start])
        out.append(" ")
        pos = end
    out.append(text[pos:])
    return "".join(out)


def prose_text(text: str) -> str:
    """Fenced blocks, inline code spans, and the leading nav/header blockquote removed.

    The leading blockquote block (starting within the first 12 lines) is the nav header on
    the JA side and the course header on the EN side; it is mandated but not a translation
    of the other side's header, so its tokens/numbers are excluded symmetrically.
    """
    lines = non_fence_lines(text)
    start = None
    for i, line in enumerate(lines[:12]):
        if line.lstrip().startswith(">"):
            start = i
            break
    if start is not None:
        end = start
        while end < len(lines) and lines[end].lstrip().startswith(">"):
            end += 1
        lines = lines[:start] + lines[end:]
    return strip_code_spans("\n".join(lines))


# --- protected tokens / numbers --------------------------------------------

_URL_CHARS = r"[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]"
URL_RE = re.compile(rf"https?://{_URL_CHARS}+")

_PATH_EXTS = (
    "md|markdown|ipynb|py|json|csv|tsv|yaml|yml|toml|txt|sql|html|css|js|jsx|ts|tsx|"
    "parquet|db|sqlite|sqlite3|env|sh|bash|zsh|cfg|ini|lock|png|jpg|jpeg|gif|svg|webp|mermaid"
)
PATH_RE = re.compile(
    rf"(?<![A-Za-z0-9_./~*\-])(?:[A-Za-z0-9_.\-*/]+/)*[A-Za-z0-9_.\-*]+\.(?:{_PATH_EXTS})(?![A-Za-z0-9_\-])"
)
IDENT_RE = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)+(?![A-Za-z0-9_])")
ACRONYM_RE = re.compile(r"(?<![A-Za-z0-9_])[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*(?![A-Za-z0-9_])")
NUM_RE = re.compile(r"(?<![A-Za-z0-9_])\d+(?:[.,]\d+)*(?![A-Za-z0-9_])")

TOKEN_CATEGORIES = ("url", "path", "identifier", "acronym")


def _normalize_url(token: str) -> str:
    prev = None
    while prev != token:
        prev = token
        token = token.rstrip(".,;:!?")
        if token.endswith(")") and "(" not in token:
            token = token[:-1]
        if token.endswith("]") and "[" not in token:
            token = token[:-1]
    return token


def _is_protected_identifier(token: str) -> bool:
    """Hyphen/underscore identifiers whose letters are all uppercase (Q4_K_M, JSON-RPC, ...)."""
    letters = [c for c in token if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)


def extract_prose_features(prose: str) -> tuple[dict[str, Counter], Counter]:
    """Extract protected tokens (per category) and number tokens from prose.

    Overlaps are resolved in category priority order: url, path, identifier, acronym;
    numbers never overlap any already-taken span.
    """
    taken = bytearray(len(prose))
    feats: dict[str, Counter] = {cat: Counter() for cat in TOKEN_CATEGORIES}

    def book(m: re.Match) -> None:
        for i in range(m.start(), m.end()):
            taken[i] = 1

    def _match(cat: str, rx: re.Pattern) -> None:
        for m in rx.finditer(prose):
            if any(taken[m.start() : m.end()]):
                continue
            token = m.group(0)
            if cat == "url":
                token = _normalize_url(token)
            elif cat == "identifier":
                if not _is_protected_identifier(token):
                    continue
            feats[cat][token] += 1
            book(m)

    _match("url", URL_RE)
    _match("path", PATH_RE)
    _match("identifier", IDENT_RE)
    _match("acronym", ACRONYM_RE)

    nums: Counter = Counter()
    for m in NUM_RE.finditer(prose):
        if any(taken[m.start() : m.end()]):
            continue
        nums[m.group(0)] += 1
        book(m)
    return feats, nums


def _describe_counter_diff(en: Counter, ja: Counter, limit: int = 4) -> str:
    diffs = []
    for token in sorted(set(en) | set(ja)):
        if en[token] != ja[token]:
            diffs.append(f"{token}: EN={en[token]} JA={ja[token]}")
    return "; ".join(diffs[:limit]) + ("; ..." if len(diffs) > limit else "")


# --- block manifest ---------------------------------------------------------


def _classify_block(lines: list[str]) -> str:
    first = lines[0].lstrip()
    if first.startswith("|"):
        return "table"
    if first.startswith(("-", "*", "+")):
        return "list"
    if re.match(r"^\d+[.)]\s", first):
        return "list"
    return "paragraph"


def split_blocks(text: str) -> list[tuple[str, str]]:
    """Split into blocks separated by headings, blank lines, fences.

    Returns (type, content) with type in heading|fence|table|list|paragraph.
    """
    blocks: list[tuple[str, str]] = []
    cur: list[str] = []
    in_fence = False

    def flush() -> None:
        nonlocal cur
        if cur:
            blocks.append((_classify_block(cur), "\n".join(cur)))
            cur = []

    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            if in_fence:
                cur.append(line)
                flush()
                in_fence = False
            else:
                flush()
                cur = [line]
                in_fence = True
            continue
        if in_fence:
            cur.append(line)
            continue
        if re.match(r"^#{1,6}\s", line):
            flush()
            blocks.append(("heading", line))
            continue
        if line.strip() == "":
            flush()
            continue
        cur.append(line)
    flush()
    return blocks


# ---------------------------------------------------------------------------
# Quiz parsing
# ---------------------------------------------------------------------------


class QuizParseError(Exception):
    def __init__(self, source: str, line: int, msg: str):
        super().__init__(f"{source}:{line}: {msg}")
        self.source = source
        self.line = line
        self.msg = msg


_OPTION_LINE_STYLES = (
    ("plain", re.compile(r"^[ \t]{1,10}([a-d])[.)][ \t]\S")),
    ("list-upper", re.compile(r"^[ \t]*-[ \t]+([A-D])\)[ \t]\S")),
    ("list-paren", re.compile(r"^[ \t]*-[ \t]+\(([a-d])\)[ \t]\S")),
)

# Answer-label styles, tried in order; full-width punctuation accepted for JA.
_ANSWER_LABEL_PATTERNS = (
    ("paren", re.compile(r"^\*\*[（(]([A-Da-d])[)）]\*\*")),
    ("dot", re.compile(r"^\*\*([A-Da-d])[.。]\*\*")),
    ("upper-paren", re.compile(r"^\*\*([A-D])[)）]\*\*")),
    ("upper-dot", re.compile(r"^\*\*([A-D])[.。]\*\*")),
    ("colon-after", re.compile(r"^\*\*([A-Da-d])\*\*[:：]")),
    ("colon-inside", re.compile(r"^\*\*([A-Da-d])[:：][ \t]+\S.*?\*\*")),
)

_NUMBERED_LINE = re.compile(r"^(\d{1,2})\.[ \t]+(\S.*)$")


def parse_quiz(source: str, text: str) -> dict:
    """Parse a 10-question quiz. Raises QuizParseError on unrecognized structure."""
    lines = text.splitlines()
    akey = None
    for i, line in enumerate(lines):
        if re.match(r"^#{1,6}\s+Answer\b", line, re.I):
            akey = i
            break
    if akey is None:
        raise QuizParseError(source, 1, "answer key heading not found")
    qsec = lines[:akey]
    asec = lines[akey + 1 :]

    qstarts = []
    for i, line in enumerate(qsec):
        m = _NUMBERED_LINE.match(line)
        if m:
            qstarts.append((i, int(m.group(1)), m.group(2)))
    nums = [n for _, n, _ in qstarts]
    if nums != list(range(1, 11)):
        first_line = qstarts[0][0] + 1 if qstarts else 1
        raise QuizParseError(source, first_line, f"question numbers {nums} != 1..10")

    types: list[str] = []
    styles: set[str] = set()
    for qi, (idx, n, first) in enumerate(qstarts):
        end = qstarts[qi + 1][0] if qi + 1 < len(qstarts) else len(qsec)
        block = qsec[idx + 1 : end]
        low = first.lower()
        if "mcq" in low or "multiple choice" in low or "multiple-choice" in low:
            qtype = "mcq"
        elif "short answer" in low:
            qtype = "short"
        else:
            raise QuizParseError(source, idx + 1, f"question {n}: unknown question type")
        found: tuple[str, set[str]] | None = None
        for style, rx in _OPTION_LINE_STYLES:
            labels = {m.group(1).lower() for l in block if (m := rx.match(l))}
            if labels:
                if found is not None:
                    raise QuizParseError(
                        source, idx + 1, f"question {n}: mixed option styles in one question"
                    )
                found = (style, labels)
        if qtype == "mcq":
            if found is None:
                inline_labels = {x.lower() for x in re.findall(r"[（(]([a-d])[)）]", first)}
                if inline_labels >= {"a", "b", "c", "d"}:
                    found = ("inline", inline_labels)
            if found is None:
                raise QuizParseError(source, idx + 1, f"question {n}: MCQ options not recognized")
            if found[1] != {"a", "b", "c", "d"}:
                raise QuizParseError(
                    source, idx + 1, f"question {n}: option labels {sorted(found[1])} != a..d"
                )
            styles.add(found[0])
        types.append(qtype)
    if "mcq" not in types:
        raise QuizParseError(source, 1, "no MCQ questions found")
    if len(styles) > 1:
        raise QuizParseError(source, 1, f"mixed option styles across questions: {sorted(styles)}")
    option_style = styles.pop()

    astarts = []
    for i, line in enumerate(asec):
        m = _NUMBERED_LINE.match(line)
        if m:
            astarts.append((i, int(m.group(1)), m.group(2)))
    anums = [n for _, n, _ in astarts]
    if anums != list(range(1, 11)):
        raise QuizParseError(source, akey + 2, f"answer key numbers {anums} != 1..10")

    tmap = dict(zip(nums, types))
    answers: list[dict] = []
    answer_styles: set[str] = set()
    for i, n, rest in astarts:
        if tmap[n] == "mcq":
            label = None
            for code, rx in _ANSWER_LABEL_PATTERNS:
                m = rx.match(rest)
                if m:
                    label = m.group(1).lower()
                    answer_styles.add(code)
                    break
            if label is None:
                raise QuizParseError(
                    source, akey + 2 + i, f"answer {n}: MCQ answer label not recognized"
                )
            answers.append({"q": n, "answer": label})
        else:
            answers.append({"q": n, "answer": None})
    answer_style = next(iter(answer_styles)) if len(answer_styles) == 1 else "mixed"
    return {
        "questions": len(qstarts),
        "optionStyle": option_style,
        "answerStyle": answer_style,
        "types": types,
        "answers": answers,
    }


# ---------------------------------------------------------------------------
# State / baseline loading and validation
# ---------------------------------------------------------------------------

_STATE_ROW_KEYS = {
    "sourcePath": str,
    "jaPath": str,
    "batchId": str,
    "sourceHash": str,
    "jaHash": (str, type(None)),
    "translationStatus": str,
    "reviewStatus": str,
    "translationAttempt": int,
    "reviewAttempt": int,
    "lastFailureCode": (str, type(None)),
    "translatorAssignments": list,
    "reviewerAssignment": (str, type(None)),
    "reviewResult": (dict, type(None)),
}


def validate_state(state: dict, baseline: dict | None) -> list[str]:
    errs: list[str] = []
    label = STATE_REL
    if state.get("schemaVersion") != SCHEMA_VERSION:
        errs.append(f"{label}: bad schemaVersion {state.get('schemaVersion')!r}")
    if baseline is not None:
        if state.get("baselineId") != baseline["manifestDigest"][:16]:
            errs.append(f"{label}: baselineId does not match baseline manifestDigest[:16]")
        if state.get("manifestDigest") != baseline["manifestDigest"]:
            errs.append(f"{label}: manifestDigest does not match baseline")
    if state.get("executionStatus") not in EXECUTION_STATUSES:
        errs.append(f"{label}: unknown executionStatus {state.get('executionStatus')!r}")
    if state.get("lastCompletedPhase") not in (None, "P9_READY"):
        errs.append(f"{label}: unknown lastCompletedPhase {state.get('lastCompletedPhase')!r}")
    if not isinstance(state.get("revision"), int):
        errs.append(f"{label}: revision is not an int")
    rows = state.get("rows")
    if not isinstance(rows, list):
        errs.append(f"{label}: rows is not a list")
        return errs
    if baseline is not None and {r.get("sourcePath") for r in rows} != set(baseline["sources"]):
        errs.append(f"{label}: rows do not cover exactly the baseline sources")
    for row in rows:
        sp = row.get("sourcePath", "<missing>")
        for key, typ in _STATE_ROW_KEYS.items():
            if key not in row:
                errs.append(f"{label}: row {sp}: missing key {key}")
            elif not isinstance(row[key], typ):
                errs.append(f"{label}: row {sp}: key {key} has wrong type")
        if row.get("translationStatus") not in TRANSLATION_STATUSES:
            errs.append(f"{label}: row {sp}: unknown translationStatus {row.get('translationStatus')!r}")
        if row.get("reviewStatus") not in REVIEW_STATUSES:
            errs.append(f"{label}: row {sp}: unknown reviewStatus {row.get('reviewStatus')!r}")
        rr = row.get("reviewResult")
        if isinstance(rr, dict):
            if rr.get("verdict") not in ("approved", "rejected"):
                errs.append(f"{label}: row {sp}: reviewResult.verdict invalid")
            q = rr.get("quality")
            if not isinstance(q, dict) or set(q) != set(QUALITY_KEYS):
                errs.append(f"{label}: row {sp}: reviewResult.quality keys invalid")
            elif any(v not in QUALITY_VALUES for v in q.values()):
                errs.append(f"{label}: row {sp}: reviewResult.quality has invalid values")
    return errs


def load_baseline(root: Path) -> tuple[dict | None, list[str]]:
    path = root / BASELINE_REL
    if not path.exists():
        return None, [f"{BASELINE_REL}: missing (run --init first)"]
    baseline = json.loads(read_text(path))
    errs = []
    if baseline.get("schemaVersion") != SCHEMA_VERSION:
        errs.append(f"{BASELINE_REL}: bad schemaVersion {baseline.get('schemaVersion')!r}")
    if digest_payload(baseline, "manifestDigest") != baseline.get("manifestDigest"):
        errs.append(f"{BASELINE_REL}: manifestDigest mismatch (file tampered)")
    return baseline, errs


def load_state(root: Path, baseline: dict | None) -> tuple[dict | None, list[str]]:
    path = root / STATE_REL
    if not path.exists():
        return None, [f"{STATE_REL}: missing (run --init first)"]
    state = json.loads(read_text(path))
    errs = []
    if digest_payload(state, "lastStateDigest") != state.get("lastStateDigest"):
        errs.append(f"{STATE_REL}: lastStateDigest mismatch (state tampered)")
    errs.extend(validate_state(state, baseline))
    return state, errs


# ---------------------------------------------------------------------------
# Checks (read-only modes)
# ---------------------------------------------------------------------------


def global_failures(root: Path, baseline: dict | None, state: dict | None) -> list[str]:
    fails: list[str] = []
    if baseline is not None:
        for rel, want in baseline.get("sources", {}).items():
            f = root / rel
            if not f.exists():
                fails.append(f"{rel}: missing (EN source present at --init)")
            elif sha256_file(f) != want:
                fails.append(f"{rel}: hash mismatch vs baseline (EN source changed after --init)")
        for rel, want in baseline.get("notebooks", {}).items():
            f = root / rel
            if not f.exists():
                fails.append(f"{rel}: missing (notebook present at --init)")
            elif sha256_file(f) != want:
                fails.append(f"{rel}: hash mismatch vs baseline (notebook changed after --init)")
    return fails


def check_translation_pair(
    en_text: str, ja_text: str, source: str, ja_rel: str, week_nbs: list[str]
) -> list[str]:
    """Structural fidelity checks for one EN->JA pair. Returns reason strings (unprefixed)."""
    reasons: list[str] = []

    # -- nav header ---------------------------------------------------------
    if source.endswith("README.md"):
        nav = ["[英語版](README.md)", "](exercises.ja.md)", "](quiz.ja.md)"]
    else:
        base = source.rsplit("/", 1)[1][: -len(".md")]
        nav = [f"[英語版]({base}.md)", "](README.ja.md)"]
    head = "\n".join(ja_text.splitlines()[:12])
    for pat in nav:
        if pat not in head:
            reasons.append(f"nav header missing link {pat!r}")

    # -- hygiene ------------------------------------------------------------
    ja_lines = ja_text.splitlines()
    tw = [i + 1 for i, l in enumerate(ja_lines) if l != l.rstrip()]
    if tw:
        reasons.append(f"trailing whitespace on line(s) {tw[:5]}")
    if not ja_text.endswith("\n") or ja_text.endswith("\n\n"):
        reasons.append("file must end with exactly one newline")
    for i, line in enumerate(ja_lines):
        if re.match(r"^(<<<<<<<|=======|>>>>>>>|\|\|\|\|\|\|\|)", line):
            reasons.append(f"conflict marker on line {i + 1}")

    # -- structure ----------------------------------------------------------
    if heading_levels(en_text) != heading_levels(ja_text):
        reasons.append(
            f"heading level sequence mismatch: EN={heading_levels(en_text)} JA={heading_levels(ja_text)}"
        )
    if table_shapes(en_text) != table_shapes(ja_text):
        reasons.append("table row/column shape mismatch")
    if fence_infos(en_text) != fence_infos(ja_text):
        reasons.append(
            f"fence count/info mismatch: EN={fence_infos(en_text)} JA={fence_infos(ja_text)}"
        )
    en_spans, ja_spans = sorted(inline_code_spans(en_text)), sorted(inline_code_spans(ja_text))
    if en_spans != ja_spans:
        diff = _describe_counter_diff(Counter(en_spans), Counter(ja_spans))
        reasons.append(f"inline code span multiset mismatch ({diff})")

    # -- tokens / numbers ----------------------------------------------------
    en_feats, en_nums = extract_prose_features(prose_text(en_text))
    ja_feats, ja_nums = extract_prose_features(prose_text(ja_text))
    for cat in TOKEN_CATEGORIES:
        if en_feats[cat] != ja_feats[cat]:
            diff = _describe_counter_diff(en_feats[cat], ja_feats[cat])
            reasons.append(f"protected token mismatch ({cat}): {diff}")
    if en_nums != ja_nums:
        diff = _describe_counter_diff(en_nums, ja_nums)
        reasons.append(f"number token multiset mismatch: {diff}")

    # -- quiz ----------------------------------------------------------------
    if source.endswith("quiz.md"):
        try:
            q_en = parse_quiz(source, en_text)
        except QuizParseError as exc:
            reasons.append(f"EN quiz parse failed (baseline drift?): {exc}")
            q_en = None
        try:
            q_ja = parse_quiz(ja_rel, ja_text)
        except QuizParseError as exc:
            reasons.append(f"quiz parse error: {exc}")
            q_ja = None
        if q_en is not None and q_ja is not None:
            if q_ja["optionStyle"] != q_en["optionStyle"]:
                reasons.append(
                    f"quiz option style mismatch: EN={q_en['optionStyle']} JA={q_ja['optionStyle']}"
                )
            if q_ja["types"] != q_en["types"]:
                reasons.append("quiz question type sequence mismatch (MCQ/short answer)")
            for a_en, a_ja in zip(q_en["answers"], q_ja["answers"]):
                if a_en != a_ja:
                    reasons.append(
                        f"quiz answer mismatch q{a_en['q']}: EN={a_en['answer']} JA={a_ja['answer']}"
                    )

    # -- README notebook references ------------------------------------------
    if source.endswith("README.md"):
        link_targets = {Path(t).name for t in re.findall(r"\]\(([^)\s]+)\)", ja_text)}
        for nb in week_nbs:
            stem = nb[: -len(".ipynb")]
            if nb not in link_targets and f"{stem}.ja.ipynb" not in link_targets:
                reasons.append(f"notebook {nb} not referenced by a markdown link")
    return reasons


def review_row_failures(root: Path, row: dict) -> list[str]:
    label = row.get("jaPath", "<no-jaPath>")
    fails: list[str] = []
    if row.get("translationStatus") != "translated":
        fails.append(f"{label}: translationStatus={row.get('translationStatus')!r}, expected translated")
    rr = row.get("reviewResult")
    if not isinstance(rr, dict):
        fails.append(f"{label}: reviewResult missing")
    else:
        if rr.get("coverageComplete") is not True:
            fails.append(f"{label}: coverageComplete is not true")
        q = rr.get("quality")
        if not isinstance(q, dict) or set(q) != set(QUALITY_KEYS):
            fails.append(f"{label}: quality keys invalid (need all of {list(QUALITY_KEYS)})")
        else:
            bad = {k: v for k, v in q.items() if v not in ("pass", "na")}
            if bad:
                fails.append(f"{label}: quality not pass/na: {bad}")
        if not isinstance(rr.get("findings"), list):
            fails.append(f"{label}: findings missing or not a list")
        verdict = rr.get("verdict")
        if verdict == "approved" and row.get("reviewStatus") != "approved":
            fails.append(f"{label}: verdict approved but reviewStatus={row.get('reviewStatus')!r}")
        if verdict == "rejected" and row.get("reviewStatus") != "rejected":
            fails.append(f"{label}: verdict rejected but reviewStatus={row.get('reviewStatus')!r}")
    reviewer = row.get("reviewerAssignment")
    if not reviewer:
        fails.append(f"{label}: reviewerAssignment is null")
    elif any(reviewer == a for a in row.get("translatorAssignments", [])):
        fails.append(f"{label}: reviewer {reviewer!r} equals a translator assignment")
    ja_file = root / label
    if not ja_file.exists():
        fails.append(f"{label}: file missing")
    elif row.get("jaHash") != sha256_file(ja_file):
        fails.append(f"{label}: jaHash does not match current file hash")
    return fails


def run_check(root: Path, sources: list[str], mode: str, weeks: list[int]) -> list[str]:
    """All checks for the given mode. Returns failure strings "FILE: reason"."""
    fails: list[str] = []
    baseline, berrs = load_baseline(root)
    fails.extend(berrs)
    state, serrs = load_state(root, baseline)
    fails.extend(serrs)
    fails.extend(global_failures(root, baseline, state))

    targets = weeks if mode in ("translation", "review") else WEEKS

    if mode in ("translation", "full"):
        week_nbs = (baseline or {}).get("weekNotebooks", {})
        for w in targets:
            nbs = week_nbs.get(f"{w:02d}", [])
            for name in SOURCE_FILES:
                src = f"curriculum/week-{w:02d}/{name}"
                if src not in sources:
                    continue
                ja_rel = ja_path_for(src)
                ja_file = root / ja_rel
                if not ja_file.exists():
                    fails.append(f"{ja_rel}: missing")
                    continue
                en_text = read_text(root / src)
                ja_text = read_text(ja_file)
                for reason in check_translation_pair(en_text, ja_text, src, ja_rel, nbs):
                    fails.append(f"{ja_rel}: {reason}")

    if mode in ("review", "full") and state is not None:
        for row in state["rows"]:
            if week_of(row["sourcePath"]) in targets:
                fails.extend(review_row_failures(root, row))

    if mode == "full":
        idx = root / INDEX_JA_REL
        if not idx.exists():
            fails.append(f"{INDEX_JA_REL}: missing")
        else:
            text = read_text(idx)
            for w in WEEKS:
                if not re.search(rf"\]\([^)]*week-{w:02d}/README\.ja\.md\)", text):
                    fails.append(f"{INDEX_JA_REL}: no markdown link to week-{w:02d}/README.ja.md")
        rep = root / REPORT_REL
        if state is None:
            pass  # state missing already reported
        elif not rep.exists():
            fails.append(f"{REPORT_REL}: missing (run --render-report)")
        elif read_text(rep) != render_report(state):
            fails.append(f"{REPORT_REL}: content does not match --render-report output for current state")
    return fails


# ---------------------------------------------------------------------------
# --init
# ---------------------------------------------------------------------------


def build_baseline(root: Path, sources: list[str], nb_paths: list[str]) -> tuple[dict, list[str]]:
    """Returns (baseline-without-manifestDigest, stderr-lines for quiz parse errors)."""
    parse_errors: list[str] = []
    quiz_inventory: list[dict] = []
    for src in sources:
        if not src.endswith("quiz.md"):
            continue
        try:
            q = parse_quiz(src, read_text(root / src))
        except QuizParseError as exc:
            parse_errors.append(f"{exc.source}:{exc.line}: {exc.msg}")
            continue
        quiz_inventory.append(
            {
                "source": src,
                "questions": q["questions"],
                "optionStyle": q["optionStyle"],
                "answerStyle": q["answerStyle"],
                "answers": q["answers"],
            }
        )

    token_acc: dict[tuple[str, str], dict] = {}
    block_manifest: list[dict] = []
    for src in sources:
        text = read_text(root / src)
        feats, _nums = extract_prose_features(prose_text(text))
        for cat in TOKEN_CATEGORIES:
            for token, count in feats[cat].items():
                entry = token_acc.setdefault(
                    (cat, token), {"category": cat, "token": token, "count": 0, "files": set()}
                )
                entry["count"] += count
                entry["files"].add(src)
        for i, (btype, _content) in enumerate(split_blocks(text)):
            block_manifest.append(
                {"source": src, "blockId": sha1_hex(f"{src}#{i}")[:12], "type": btype}
            )

    protected = []
    for (_cat, _tok), entry in sorted(token_acc.items()):
        protected.append(
            {"token": entry["token"], "category": entry["category"], "count": entry["count"],
             "files": sorted(entry["files"])}
        )

    baseline = {
        "schemaVersion": SCHEMA_VERSION,
        "baseCommit": git_head(root),
        "sources": {src: sha256_file(root / src) for src in sources},
        "notebooks": {rel: sha256_file(root / rel) for rel in nb_paths},
        "weekNotebooks": week_notebook_map(nb_paths),
        "protectedTokens": protected,
        "quizInventory": quiz_inventory,
        "blockManifest": block_manifest,
    }
    return baseline, parse_errors


def build_state(baseline: dict, sources: list[str]) -> dict:
    rows = []
    for src in sources:
        rows.append(
            {
                "sourcePath": src,
                "jaPath": ja_path_for(src),
                "batchId": batch_id(week_of(src)),
                "sourceHash": baseline["sources"][src],
                "jaHash": None,
                "translationStatus": "pending",
                "reviewStatus": "pending",
                "translationAttempt": 0,
                "reviewAttempt": 0,
                "lastFailureCode": None,
                "translatorAssignments": [],
                "reviewerAssignment": None,
                "reviewResult": None,
            }
        )
    state = {
        "schemaVersion": SCHEMA_VERSION,
        "baselineId": baseline["manifestDigest"][:16],
        "manifestDigest": baseline["manifestDigest"],
        "revision": 1,
        "lastCompletedPhase": None,
        "executionStatus": "active",
        "stopCode": None,
        "activeOperation": None,
        "rows": rows,
        "lastStateDigest": None,
    }
    return state


def cmd_init(root: Path, sources: list[str], nb_paths: list[str]) -> None:
    bp, sp = root / BASELINE_REL, root / STATE_REL
    if bp.exists() or sp.exists():
        die(
            "--init refused: baseline and/or state already exist "
            f"(baseline={bp.exists()} state={sp.exists()}); remove them to re-init",
            2,
        )
    nb_paths = nb_paths if nb_paths is not None else discover_notebooks(root)
    baseline, parse_errors = build_baseline(root, sources, nb_paths)
    if parse_errors:
        for line in parse_errors:
            print(f"quiz parse error {line}", file=sys.stderr)
        raise SystemExit(3)
    baseline["manifestDigest"] = digest_payload(baseline, "manifestDigest")
    atomic_write_json(bp, baseline)

    state = build_state(baseline, sources)
    state["lastStateDigest"] = digest_payload(state, "lastStateDigest")
    atomic_write_json(sp, state)

    print(f"wrote {bp} ({bp.stat().st_size} bytes)")
    print(f"wrote {sp} ({sp.stat().st_size} bytes)")
    print(f"manifestDigest: {baseline['manifestDigest']}")


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------


def render_report(state: dict) -> str:
    lines: list[str] = []
    lines.append("# Translation review")
    lines.append("")
    lines.append(f"- formatVersion: {REPORT_FORMAT_VERSION}")
    lines.append(f"- baselineId: {state['baselineId']}")
    lines.append(f"- manifestDigest: {state['manifestDigest']}")
    lines.append(f"- stateDigest: {state['lastStateDigest']}")
    lines.append(f"- rows: {len(state['rows'])}")
    lines.append("")
    header = ("sourcePath", "jaPath", "batch", "translationStatus", "reviewStatus", "verdict", "quality")
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "---|" * len(header))
    for row in sorted(state["rows"], key=lambda r: r["sourcePath"]):
        rr = row.get("reviewResult") or {}
        verdict = rr.get("verdict")
        q = rr.get("quality") or {}
        if q:
            p = sum(1 for v in q.values() if v == "pass")
            na = sum(1 for v in q.values() if v == "na")
            f = sum(1 for v in q.values() if v == "fail")
            quality = f"pass={p}/na={na}/fail={f}"
        else:
            quality = "-"
        cells = (
            row["sourcePath"], row["jaPath"], row["batchId"],
            row["translationStatus"], row["reviewStatus"],
            str(verdict), quality,
        )
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# State actions
# ---------------------------------------------------------------------------


def load_state_strict(root: Path) -> tuple[dict, dict]:
    baseline, berrs = load_baseline(root)
    if baseline is None or berrs:
        die("baseline missing or invalid: " + "; ".join(berrs), 2)
    state, serrs = load_state(root, baseline)
    if state is None or serrs:
        die("state missing or invalid: " + "; ".join(serrs), 2)
    return baseline, state


def save_state(root: Path, state: dict) -> None:
    state["lastStateDigest"] = digest_payload(state, "lastStateDigest")
    atomic_write_json(root / STATE_REL, state)
    # verify round-trip
    reread = json.loads(read_text(root / STATE_REL))
    if digest_payload(reread, "lastStateDigest") != reread.get("lastStateDigest"):
        die("state verification failed after write (digest mismatch)", 2)


def find_row(state: dict, source: str) -> dict:
    for row in state["rows"]:
        if row["sourcePath"] == source:
            return row
    die(f"--source {source!r} not found in state rows (use the EN path, e.g. curriculum/week-02/README.md)", 2)
    raise AssertionError  # unreachable


def action_accept_translation(root: Path, state: dict, row: dict) -> None:
    if row["translationAttempt"] < 1:
        die(f"{row['sourcePath']}: translationAttempt is 0; run --begin-translation first", 2)
    ja_file = root / row["jaPath"]
    if not ja_file.exists():
        die(f"{row['jaPath']}: file missing, cannot accept translation", 2)
    row["jaHash"] = sha256_file(ja_file)
    row["translationStatus"] = "translated"
    row["lastFailureCode"] = None


def action_begin_translation(root: Path, state: dict, row: dict, assignment: str) -> None:
    if row["translationAttempt"] >= MAX_TRANSLATION_ATTEMPTS:
        die(
            f"{row['sourcePath']}: translationAttempt already {row['translationAttempt']} "
            f"(max {MAX_TRANSLATION_ATTEMPTS})",
            2,
        )
    if not assignment:
        die("--assignment must be a non-empty string", 2)
    row["translationAttempt"] += 1
    row["translationStatus"] = "in_progress"
    row["translatorAssignments"] = row["translatorAssignments"] + [assignment]


def action_begin_review(root: Path, state: dict, row: dict, reviewer: str) -> None:
    if row["translationStatus"] != "translated":
        die(
            f"{row['sourcePath']}: translationStatus is {row['translationStatus']!r}, "
            "must be translated before review",
            2,
        )
    if not reviewer:
        die("--reviewer must be a non-empty string", 2)
    row["reviewerAssignment"] = reviewer
    row["reviewAttempt"] += 1


def _validate_review_payload(payload: dict) -> list[str]:
    errs: list[str] = []
    need = {"reviewer", "verdict", "coverageComplete", "quality", "findings"}
    missing = need - set(payload)
    if missing:
        errs.append(f"payload missing keys: {sorted(missing)}")
        return errs
    verdict = payload["verdict"]
    if verdict not in ("approved", "rejected"):
        errs.append(f"verdict {verdict!r} invalid (approved|rejected)")
    if not isinstance(payload["coverageComplete"], bool):
        errs.append("coverageComplete must be a bool")
    q = payload["quality"]
    if not isinstance(q, dict) or set(q) != set(QUALITY_KEYS):
        errs.append(f"quality must have exactly the keys {list(QUALITY_KEYS)}")
    else:
        bad = {k: v for k, v in q.items() if v not in QUALITY_VALUES}
        if bad:
            errs.append(f"quality values must be pass|na|fail, got {bad}")
    if not isinstance(payload["findings"], list):
        errs.append("findings must be a list")
    if not isinstance(payload["reviewer"], str) or not payload["reviewer"]:
        errs.append("reviewer must be a non-empty string")
    if verdict == "approved" and isinstance(q, dict) and set(q) == set(QUALITY_KEYS):
        if payload["coverageComplete"] is not True:
            errs.append("approved verdict requires coverageComplete=true")
        bad = {k: v for k, v in q.items() if v not in ("pass", "na")}
        if bad:
            errs.append(f"approved verdict requires all quality pass/na, got {bad}")
    return errs


def action_record_review(root: Path, state: dict, row: dict, payload: dict) -> None:
    errs = _validate_review_payload(payload)
    if errs:
        die("invalid review payload: " + "; ".join(errs), 2)
    if row["translationStatus"] != "translated":
        die(f"{row['sourcePath']}: row is not translated", 2)
    if not row["reviewerAssignment"]:
        die(f"{row['sourcePath']}: no reviewerAssignment; run --begin-review first", 2)
    if payload["reviewer"] != row["reviewerAssignment"]:
        die(
            f"{row['sourcePath']}: payload reviewer {payload['reviewer']!r} != "
            f"reviewerAssignment {row['reviewerAssignment']!r}",
            2,
        )
    row["reviewResult"] = {
        "reviewer": payload["reviewer"],
        "verdict": payload["verdict"],
        "coverageComplete": payload["coverageComplete"],
        "quality": {k: payload["quality"][k] for k in QUALITY_KEYS},
        "findings": payload["findings"],
    }
    if payload["verdict"] == "approved":
        row["reviewStatus"] = "approved"
    else:
        row["reviewStatus"] = "rejected"
        row["lastFailureCode"] = "review_rejected"


def action_finalize(root: Path, state: dict) -> None:
    not_approved = [r["sourcePath"] for r in state["rows"] if r["reviewStatus"] != "approved"]
    if not_approved:
        die(f"cannot finalize: {len(not_approved)} row(s) not approved, e.g. {not_approved[:3]}", 2)
    state["lastCompletedPhase"] = "P9_READY"
    state["executionStatus"] = "ready_for_verification"


def cmd_render_report(root: Path) -> None:
    baseline, state = load_state_strict(root)
    if state["executionStatus"] != "ready_for_verification":
        die(
            f"--render-report requires executionStatus=ready_for_verification, "
            f"got {state['executionStatus']!r}",
            2,
        )
    path = root / REPORT_REL
    atomic_write_bytes(path, render_report(state).encode("utf-8"))
    print(f"wrote {path} ({path.stat().st_size} bytes)")


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _fixture_readme_en() -> str:
    return (
        "# Week 02: Fake\n"
        "\n"
        "Prose mentions Q4_K_M, JSON-RPC and MIT with number 42 and\n"
        "https://example.com/docs plus files README.md and data.csv.\n"
        "Run `zoro.data` now. See the notebook via [link](notebooks/01-fake.ipynb).\n"
        "\n"
        "## Table\n"
        "\n"
        "| A | B |\n"
        "|---|---|\n"
        "| 1 | 2 |\n"
        "\n"
        "## Code\n"
        "\n"
        "```python\n"
        "x = drop_duplicates()\n"
        "```\n"
        "\n"
        "Done.\n"
    )


def _fixture_readme_ja() -> str:
    return (
        "# Week 02: Fake（日本語版）\n"
        "\n"
        "> **日本語版** · [英語版](README.md) · [演習](exercises.ja.md) · [クイズ](quiz.ja.md)\n"
        "\n"
        "Q4_K_M、JSON-RPC、MITについて。数値42とhttps://example.com/docs、\n"
        "ファイルREADME.mdとdata.csvに言及する。今すぐ `zoro.data` を実行する。\n"
        "ノートブックは[リンク](notebooks/01-fake.ipynb)から。\n"
        "\n"
        "## 表\n"
        "\n"
        "| A | B |\n"
        "|---|---|\n"
        "| 1 | 2 |\n"
        "\n"
        "## コード\n"
        "\n"
        "```python\n"
        "x = drop_duplicates()\n"
        "```\n"
        "\n"
        "完了。\n"
    )


def _fixture_quiz_en() -> str:
    mcq = (
        "1. **Multiple choice.** Question one about `drop_duplicates()` and 42. *(see §1)*\n"
        "   a. Option A with MIT\n"
        "   b. Option B\n"
        "   c. Option C\n"
        "   d. Option D\n"
        "\n"
        "2. **Short answer.** Why Q4_K_M and JSON-RPC matter for https://example.com/q4.\n"
        "\n"
        "3. **Multiple choice.** Question three.\n"
        "   a. x\n"
        "   b. y\n"
        "   c. z\n"
        "   d. w\n"
        "\n"
        "4. **Short answer.** Explain the seed 7.\n"
        "\n"
        "5. **Multiple choice.** Pick one of 4.\n"
        "   a. 1\n"
        "   b. 2\n"
        "   c. 3\n"
        "   d. 4\n"
        "\n"
        "6. **Short answer.** Six.\n"
        "\n"
        "7. **Multiple choice.** Pick.\n"
        "   a. a\n"
        "   b. b\n"
        "   c. c\n"
        "   d. d\n"
        "\n"
        "8. **Short answer.** Eight.\n"
        "\n"
        "9. **Short answer.** Nine.\n"
        "\n"
        "10. **Short answer.** Ten.\n"
        "\n"
        "## Answer key\n"
        "\n"
        "1. **b.** Because B.\n"
        "\n"
        "2. **Same seed**: deterministic output.\n"
        "\n"
        "3. **b.** Yes it is b.\n"
        "\n"
        "4. Answer four mentions 7.\n"
        "\n"
        "5. **b.** Pick b.\n"
        "\n"
        "6. Six answer.\n"
        "\n"
        "7. **b.** b.\n"
        "\n"
        "8. Eight answer.\n"
        "\n"
        "9. Nine answer.\n"
        "\n"
        "10. Ten answer.\n"
    )
    return "# Week 02: Quiz (10 questions, 8/10 to pass)\n\nIntro text.\n\n" + mcq


def _fixture_quiz_ja() -> str:
    mcq = (
        "1. **Multiple choice。** この問いは `drop_duplicates()` と42について。 *(§1を参照)*\n"
        "   a. MITを含む選択肢A\n"
        "   b. 選択肢B\n"
        "   c. 選択肢C\n"
        "   d. 選択肢D\n"
        "\n"
        "2. **Short answer。** Q4_K_MとJSON-RPCがhttps://example.com/q4で重要な理由。\n"
        "\n"
        "3. **Multiple choice。** 第三問。\n"
        "   a. x\n"
        "   b. y\n"
        "   c. z\n"
        "   d. w\n"
        "\n"
        "4. **Short answer。** seed 7を説明せよ。\n"
        "\n"
        "5. **Multiple choice。** 4つのうちひとつ選べ。\n"
        "   a. 1\n"
        "   b. 2\n"
        "   c. 3\n"
        "   d. 4\n"
        "\n"
        "6. **Short answer。** 六番。\n"
        "\n"
        "7. **Multiple choice。** 選べ。\n"
        "   a. a\n"
        "   b. b\n"
        "   c. c\n"
        "   d. d\n"
        "\n"
        "8. **Short answer。** 八番。\n"
        "\n"
        "9. **Short answer。** 九番。\n"
        "\n"
        "10. **Short answer。** 十番。\n"
        "\n"
        "## Answer key\n"
        "\n"
        "1. **b。** Bだから。\n"
        "\n"
        "2. **同じseed**: deterministicな出力。\n"
        "\n"
        "3. **b。** bである。\n"
        "\n"
        "4. 7に言及する回答。\n"
        "\n"
        "5. **b。** bを選ぶ。\n"
        "\n"
        "6. 六番の回答。\n"
        "\n"
        "7. **b。** b。\n"
        "\n"
        "8. 八番の回答。\n"
        "\n"
        "9. 九番の回答。\n"
        "\n"
        "10. 十番の回答。\n"
    )
    return "# Week 02: クイズ（10問、8/10で合格）\n\n> **日本語版** · [英語版](quiz.md) · [README](README.ja.md)\n\nイントロ。\n\n" + mcq


def _expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _expect_exit(code: int, fn, *args, **kw) -> None:
    try:
        fn(*args, **kw)
    except SystemExit as exc:
        _expect(exc.code == code, f"expected exit {code}, got {exc.code}")
        return
    raise AssertionError(f"expected SystemExit({code}), function returned normally")


def _write_state(root: Path, state: dict) -> None:
    state["lastStateDigest"] = digest_payload(state, "lastStateDigest")
    atomic_write_json(root / STATE_REL, state)


def self_test() -> None:
    real_root = repo_root()
    guarded = [real_root / BASELINE_REL, real_root / STATE_REL, real_root / REPORT_REL]
    snapshots = {p: (p.read_bytes() if p.exists() else None) for p in guarded}
    index_snapshot = (
        (real_root / INDEX_JA_REL).read_bytes() if (real_root / INDEX_JA_REL).exists() else None
    )

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        wk = root / "curriculum" / "week-02"
        (wk / "notebooks").mkdir(parents=True)
        (root / "scripts").mkdir(parents=True)
        (wk / "notebooks" / "01-fake.ipynb").write_text('{"cells": []}\n', encoding="utf-8")
        (wk / "README.md").write_text(_fixture_readme_en(), encoding="utf-8")
        (wk / "quiz.md").write_text(_fixture_quiz_en(), encoding="utf-8")
        readme_ja_rel = wk / "README.ja.md"
        quiz_ja_rel = wk / "quiz.ja.md"
        readme_ja_rel.write_text(_fixture_readme_ja(), encoding="utf-8")
        quiz_ja_rel.write_text(_fixture_quiz_ja(), encoding="utf-8")

        sources = ["curriculum/week-02/README.md", "curriculum/week-02/quiz.md"]  # mini inventory
        nb_paths = discover_notebooks(root)
        passed: list[str] = []

        def check(mode: str = "translation", weeks: list[int] | None = None) -> list[str]:
            return run_check(root, sources, mode, weeks or [2])

        # -- init and healthy baseline --------------------------------------
        cmd_init(root, sources, nb_paths)
        state_bytes = (root / STATE_REL).read_bytes()
        baseline = json.loads(read_text(root / BASELINE_REL))
        _expect(len(baseline["sources"]) == 2, "fixture baseline should cover 2 sources")
        _expect(len(baseline["notebooks"]) == 1, "fixture baseline should cover 1 notebook")
        _expect(baseline["weekNotebooks"] == {"02": ["01-fake.ipynb"]}, "weekNotebooks map")
        _expect(len(baseline["quizInventory"]) == 1, "quizInventory size")

        # 1) normal pair passes
        fails = check()
        _expect(fails == [], f"normal pair should pass, got {fails}")
        passed.append("normal pair pass")

        readme_ja = _fixture_readme_ja()
        quiz_ja = _fixture_quiz_ja()

        def restore() -> None:
            readme_ja_rel.write_text(readme_ja, encoding="utf-8")
            quiz_ja_rel.write_text(quiz_ja, encoding="utf-8")
            (root / STATE_REL).write_bytes(state_bytes)

        def scenario(name: str, mutate, needle: str) -> None:
            mutate()
            fails = check()
            _expect(any(needle in f for f in fails), f"{name}: expected failure containing {needle!r}, got {fails}")
            restore()
            passed.append(name)

        # 2) JA missing
        scenario("JA missing detected", lambda: readme_ja_rel.unlink(), "missing")

        # 3) broken table
        scenario(
            "broken table detected",
            lambda: readme_ja_rel.write_text(readme_ja.replace("| 1 | 2 |\n", "", 1), encoding="utf-8"),
            "table row/column shape mismatch",
        )

        # 4) deleted inline code
        scenario(
            "deleted inline code detected",
            lambda: readme_ja_rel.write_text(readme_ja.replace(" `zoro.data` ", " ", 1), encoding="utf-8"),
            "inline code span multiset mismatch",
        )

        # 5) changed number
        scenario(
            "changed number detected",
            lambda: readme_ja_rel.write_text(readme_ja.replace("42", "43", 1), encoding="utf-8"),
            "number token multiset mismatch",
        )

        # 6) deleted option label
        scenario(
            "deleted option label detected",
            lambda: quiz_ja_rel.write_text(quiz_ja.replace("   d. 選択肢D\n", "", 1), encoding="utf-8"),
            "quiz parse error",
        )

        # 7) swapped answer
        scenario(
            "swapped answer detected",
            lambda: quiz_ja_rel.write_text(quiz_ja.replace("1. **b。**", "1. **c。**", 1), encoding="utf-8"),
            "quiz answer mismatch q1: EN=b JA=c",
        )

        # 8) trailing whitespace
        scenario(
            "trailing whitespace detected",
            lambda: readme_ja_rel.write_text(readme_ja.replace("完了。\n", "完了。 \n", 1), encoding="utf-8"),
            "trailing whitespace",
        )

        # 9) tampered state digest
        def tamper_digest() -> None:
            state = json.loads(read_text(root / STATE_REL))
            state["revision"] = 999  # no digest recomputation
            atomic_write_json(root / STATE_REL, state)
        tamper_digest()
        fails = check()
        _expect(any("lastStateDigest mismatch" in f for f in fails), f"digest mismatch not detected: {fails}")
        _expect_exit(2, load_state_strict, root)
        restore()
        passed.append("tampered state digest detected")

        # 10) unknown enum value
        def unknown_enum() -> None:
            state = json.loads(read_text(root / STATE_REL))
            state["rows"][0]["translationStatus"] = "weird"
            _write_state(root, state)
        unknown_enum()
        fails = check()
        _expect(any("unknown translationStatus" in f for f in fails), f"unknown enum not detected: {fails}")
        _expect_exit(2, load_state_strict, root)
        restore()
        passed.append("unknown enum value detected")

        # 11) --init refused when files exist
        _expect_exit(2, cmd_init, root, sources, nb_paths)
        passed.append("--init refused when baseline/state exist")

        # 12) precondition-violating action leaves state untouched
        def max_attempts() -> None:
            state = json.loads(read_text(root / STATE_REL))
            state["rows"][0]["translationAttempt"] = MAX_TRANSLATION_ATTEMPTS
            _write_state(root, state)
        max_attempts()
        before = (root / STATE_REL).read_bytes()
        state = json.loads(read_text(root / STATE_REL))
        row = find_row(state, sources[0])
        _expect_exit(2, action_begin_translation, root, state, row, "agent-x")
        _expect((root / STATE_REL).read_bytes() == before, "state bytes changed on failed action")
        restore()
        passed.append("failed action leaves state bytes unchanged")

        # 13) unparseable quiz fails --init with exit 3
        (root / BASELINE_REL).rename(root / "baseline.bak")
        (root / STATE_REL).rename(root / "state.bak")
        good_quiz = read_text(wk / "quiz.md")
        (wk / "quiz.md").write_text(good_quiz.replace("**Multiple choice.**", "**Frobnicate.**", 1), encoding="utf-8")
        _expect_exit(3, cmd_init, root, sources, nb_paths)
        (wk / "quiz.md").write_text(good_quiz, encoding="utf-8")
        (root / "baseline.bak").rename(root / BASELINE_REL)
        (root / "state.bak").rename(root / STATE_REL)
        passed.append("unparseable quiz fails --init (exit 3)")

        # 14) full state-action workflow: begin -> accept -> review -> approve -> review-mode pass
        _baseline, state = load_state_strict(root)
        row = find_row(state, sources[0])
        action_begin_translation(root, state, row, "translator-agent")
        state["revision"] += 1
        save_state(root, state)
        _baseline, state = load_state_strict(root)
        row = find_row(state, sources[0])
        action_accept_translation(root, state, row)
        state["revision"] += 1
        save_state(root, state)
        _baseline, state = load_state_strict(root)
        row = find_row(state, sources[0])
        action_begin_review(root, state, row, "reviewer-agent")
        state["revision"] += 1
        save_state(root, state)
        payload = {
            "reviewer": "reviewer-agent",
            "verdict": "approved",
            "coverageComplete": True,
            "quality": {k: "pass" for k in QUALITY_KEYS},
            "findings": [],
        }
        payload_file = root / "payload.json"
        payload_file.write_text(json.dumps(payload), encoding="utf-8")
        args_like = argparse.Namespace(source=sources[0], payload=str(payload_file))
        _run_state_action(root, "record_review", args_like)
        fails = check("review", [2])
        readme_fails = [f for f in fails if f.startswith("curriculum/week-02/README.ja.md")]
        _expect(readme_fails == [], f"approved row should pass review mode, got {readme_fails}")
        _expect(any("quiz.ja.md" in f for f in fails), "pending quiz row should still fail review mode")
        _baseline, state = load_state_strict(root)
        row = find_row(state, sources[0])
        _expect(row["reviewStatus"] == "approved" and row["translationStatus"] == "translated", "row statuses after approval")
        restore()
        passed.append("state-action workflow (begin/accept/review/approve, review-mode pass)")

        # final sanity: still healthy
        _expect(check() == [], "fixture should be healthy again at end of self-test")

    for p in guarded:
        now = p.read_bytes() if p.exists() else None
        _expect(now == snapshots[p], f"self-test must not create/modify {p}")
    _expect(
        ((real_root / INDEX_JA_REL).read_bytes() if (real_root / INDEX_JA_REL).exists() else None)
        == index_snapshot,
        "self-test must not modify the real index file",
    )

    print(f"self-test scenarios passed: {len(passed)}")
    for name in passed:
        print(f"  [ok] {name}")
    print("SELF-TEST PASS")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_weeks(spec: str) -> list[int]:
    m = re.match(r"^(\d{2})-(\d{2})$", spec)
    if not m:
        die(f"--weeks must look like 02-06, got {spec!r}", 2)
    a, b = int(m.group(1)), int(m.group(2))
    if not (2 <= a <= b <= 24):
        die(f"--weeks range invalid: {spec} (weeks are 02..24)", 2)
    return list(range(a, b + 1))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check_translations.py",
        description="Deterministic validator for the Japanese curriculum translation.",
    )
    p.add_argument("--init", action="store_true", help="build baseline + state")
    p.add_argument("--self-test", action="store_true", help="run offline fixture self-test")
    p.add_argument("--mode", choices=("translation", "review", "full"), default="full")
    p.add_argument("--weeks", help="week range like 02-06 (required for translation/review)")
    p.add_argument("--accept-translation", action="store_true")
    p.add_argument("--begin-translation", action="store_true")
    p.add_argument("--begin-review", action="store_true")
    p.add_argument("--record-review", action="store_true")
    p.add_argument("--finalize", action="store_true")
    p.add_argument("--render-report", action="store_true")
    p.add_argument("--source", help="EN source path, e.g. curriculum/week-02/README.md")
    p.add_argument("--assignment")
    p.add_argument("--reviewer")
    p.add_argument("--payload", help="JSON file for --record-review")
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    root = repo_root()

    if args.self_test:
        if args.init or args.mode != "full" or args.weeks or any(getattr(args, f) for f in ACTION_FLAGS):
            die("--self-test cannot be combined with other commands", 2)
        self_test()
        return

    if args.init:
        if any(getattr(args, f) for f in ACTION_FLAGS) or args.weeks or args.mode != "full":
            die("--init cannot be combined with other commands", 2)
        sources = source_paths()
        nb_paths = discover_notebooks(root)
        if len(sources) != 69:
            die(f"expected 69 EN sources, found {len(sources)}", 2)
        if len(nb_paths) != 45:
            die(f"expected 45 notebooks, found {len(nb_paths)}", 2)
        cmd_init(root, sources, nb_paths)
        return

    selected_actions = [f for f in ACTION_FLAGS if getattr(args, f)]
    if len(selected_actions) > 1:
        die(f"only one state action at a time, got {selected_actions}", 2)
    if selected_actions:
        if args.weeks or args.mode != "full":
            die("state actions cannot be combined with --mode/--weeks", 2)
        _run_state_action(root, selected_actions[0], args)
        return

    if args.mode == "full":
        if args.weeks:
            die("--weeks is only valid with --mode translation|review", 2)
        weeks = WEEKS
    else:
        if not args.weeks:
            die(f"--mode {args.mode} requires --weeks A-B", 2)
        weeks = parse_weeks(args.weeks)

    fails = run_check(root, source_paths(), args.mode, weeks)
    for f in fails:
        print(f)
    print(f"{'PASS' if not fails else 'FAIL'}: {len(fails)} failure(s) [mode={args.mode}]")
    if fails:
        raise SystemExit(1)


def _run_state_action(root: Path, action: str, args: argparse.Namespace) -> None:
    if action == "render_report":
        cmd_render_report(root)
        return
    if action == "finalize":
        _baseline, state = load_state_strict(root)
        action_finalize(root, state)
        state["revision"] += 1
        save_state(root, state)
        print(f"finalized: lastCompletedPhase=P9_READY executionStatus=ready_for_verification")
        return
    if not args.source:
        die(f"--{action.replace('_', '-')} requires --source", 2)
    _baseline, state = load_state_strict(root)
    row = find_row(state, args.source)
    if action == "accept_translation":
        action_accept_translation(root, state, row)
    elif action == "begin_translation":
        action_begin_translation(root, state, row, args.assignment or "")
    elif action == "begin_review":
        action_begin_review(root, state, row, args.reviewer or "")
    elif action == "record_review":
        payload_path = Path(args.payload or "")
        if not payload_path.is_file():
            die(f"--payload file not found: {args.payload!r}", 2)
        try:
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            die(f"payload is not valid JSON: {exc}", 2)
        if not isinstance(payload, dict):
            die("payload must be a JSON object", 2)
        action_record_review(root, state, row, payload)
    state["revision"] += 1
    save_state(root, state)
    print(f"ok: {action} on {row['sourcePath']} (revision={state['revision']})")


if __name__ == "__main__":
    main()
