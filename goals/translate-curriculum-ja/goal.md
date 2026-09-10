## Goal

AI Engineering LabのWeek 02〜24について、英語の週次教材を日本語で学習できる状態にする。各週の`README.md`、`exercises.md`、`quiz.md`に対応する`README.ja.md`、`exercises.ja.md`、`quiz.ja.md`を作成し、既存のWeek 01訳と同じ命名・文体で提供する。

### Outcome

- 対象23週×3ファイル、合計69個の`.ja.md`が存在する。
- 見出しlevel列、表の行・列形状、code fence（language/body）、Mermaid block、inline code、本文URL/path、protected token、数値token、quizのquestion/option/answer対応を保持し、説明文を自然な日本語にする。
- 英語原文から日本語版へのlinkは追加しない。`curriculum/README.ja.md`から23個の週READMEへ辿れ、各JA教材から英語原文と同週の2つのJA siblingへ辿れる。各週のJA READMEから、その週の英語notebook全件（Week 02〜24で41件）へ辿れる。
- 英語source 69件、全45 notebook、baselineはP0のraw SHA-256とbyte一致する。変更はExact allowlist内のindex、validator、baseline、state/report、69 JA file、Goal管理fileだけである。
- P0で`translation-review-state.json`を69行の`pending` stateとして初期化し、翻訳・reviewの確定ごとにmainがatomic更新する。stateはresumeの唯一の作業正、`translation-review.md`はP9でstateから決定論的に生成する表示用reportとする。
- 翻訳者とは別context/runのbilingual reviewerが69ペアを全段落について確認し、coverage、semantic equivalence、omission/addition、naturalness、term consistency、否定・条件・因果、numbers/identifiers、quiz answerをsign-offする。reviewerはJA/stateを書かず、mainがstructured resultと実assignmentを記録する。
- `check_translations.py`はtraceability matrixに従い、inventory、allowlist、baseline/state digest、構造、protected token、quiz、navigation、notebook link graph、review state/reportを個別に検査する。`--self-test`は実worktreeを変更せず、parserとstate writerのfault/mutationを隔離fixtureで拒否する。
- 完了はV1〜V6のexit 0とcontroller-measured evidenceで証明する。

## Constraints & Preferences

- 英語原文をsource of truthとして意味・構成・数値を保つ。Week 01の既存日本語Markdown/notebookと、Week 02〜24の英語source/notebookは変更しない。Notebook本文の翻訳は別Goalとする。
- P0はGoalのbaseline epochごとに一度だけ実行する。`translation_baseline.json`は`baseCommit`、source 69件、notebook 45件、source-derived protected-token/block manifest、canonical payloadの`manifestDigest`を含む。baselineもstateと同じcanonical serialization（`lastStateDigest`相当の自己fieldを除外、再帰key sort、array schema順、`ensure_ascii=true`、`separators=(',', ':')`、`allow_nan=false`、末尾LFなし）を使い、known-digest fixtureで検証する。baseline temp→flush/fsync→no-clobber atomic publication→readbackを行い、各publication境界を記録する。baseline/state作成後にGoal記録が欠落した場合は`BASELINE_RECORD_MISSING`でSTOPし、再生成しない。P0完了時のepoch、base commit、digestを`goal.md`と`tktk_log`へ記録する。resume時は既存baselineと記録済みdigestを再利用する。
- `translation-review-state.json`は次のcanonical serializationでdigestを計算する：`lastStateDigest`を対象payloadから除外、JSON objectは再帰的にkey sort、arrayはschema順、UTF-8文字列はUnicode normalizationなし、`ensure_ascii=true`、`separators=(',', ':')`、`allow_nan=false`、末尾LFなし。保存fileはcanonical JSON＋末尾LF 1個とする。更新はcandidate構築→digest計算→`lastStateDigest`設定→同directoryのexclusive tempへwrite/flush/fsync→更新前digestを再照合→`os.replace`→directory fsync→readback検証の順で行う。replace前の失敗は旧stateを保持し、replace後のreadback失敗はrollbackせずSTOPする。state actionごとにprecondition/post-state/許可failure code/idempotencyをtransition ledgerで固定し、`activeOperation`はdispatch前に設定、成功/失敗handoff時に解除する。
- state rootには`schemaVersion=1`、`baselineId`、`manifestDigest`、`revision`、`lastCompletedPhase`、`executionStatus`、`stopCode`、`activeOperation`、`rows`、`lastStateDigest`を持たせる。`executionStatus`は`initializing / active / stopped / ready_for_verification`、phaseは`null / P0 / P1..P6 / P7a/P8a..P7e/P8e / P9_READY`とする。rowsはbaselineのsource 69件と完全一致し、ASCII昇順・重複なしとする。各rowには`sourcePath`、`jaPath`、`batchId`、`sourceHash`、`jaHash`、`translationStatus`、`reviewStatus`、`translationAttempt`、`reviewAttempt`、`lastFailureCode`、`translatorAssignments`、`reviewerAssignment`、`reviewResult`を持たせる。未知field、未知enum、不正型、重複JSON key、NaN/Infinity、不正Unicodeは拒否する。
- P0はbaseline/stateの両方が不存在の新規epochでだけ初期化を許可する。baseline作成後にstateがmissing、state digestが不一致、baseline digestが不一致の場合は`STATE_MISSING`/`STATE_DIGEST_MISMATCH`でSTOPし、filesystemやreportから再構築しない。
- `translationStatus`は`pending / in_progress / translated / failed`、`reviewStatus`は`pending / in_progress / provisional / approved / rejected`、`translationAttempt`と`reviewAttempt`は各0〜2とする。translation attemptはdispatch予約時に増加し、review attemptはreview finding後のfix予約時に増加する。review再実行だけでは増加させない。retry可能codeは`MISSING`、`INVALID_UTF8`、`EMPTY_OR_TRUNCATED`、`STRUCTURE_MISMATCH`、`PROTECTED_TOKEN_MISMATCH`、`QUIZ_MISMATCH`、`NAVIGATION_MISMATCH`、`REVIEW_FINDING`。即STOP codeは`BASELINE_RECORD_MISSING`、`STATE_MISSING`、`STATE_INVALID`、`STATE_DIGEST_MISMATCH`、`BASELINE_CONFLICT`、`SOURCE_CONFLICT`、`NOTEBOOK_CONFLICT`、`JA_HASH_CONFLICT`、`SCOPE_VIOLATION`、`REVIEW_BUDGET`、`REVIEWER_UNAVAILABLE`、`REVIEW_PROTOCOL_ERROR`、`WORKER_INTERRUPTED`、`PERMANENT_ERROR`、`RETRY_EXHAUSTED`、`VERIFICATION_FAILED`、`TOOL_ERROR`。未知codeは`PERMANENT_ERROR`として扱う。retryはattempt=0→1、1→2だけ許可し、2回目失敗は`RETRY_EXHAUSTED`でSTOP、3回目予約は拒否する。
- 翻訳・review batchは直列実行する。各workerは絶対worktree pathと明示されたread/write allowlistを受け取り、write前にresolved cwdとscopeを確認する。各batch後にscoped validatorを通し、validな既存fileは再利用し、missing/invalid/truncatedだけをretryする。source/notebook conflict検出後は次のwriteを開始しない。成果物を自動削除・rollbackしない。
- P0でsourceの各Markdown block（heading、paragraph、table、list、code/mermaid fence、quiz question/answer）にstable block IDとsource hashを付けたcoverage manifestをbaselineへ保存する。reviewer resultは`requestId`、source/JA hash、reviewerAssignment、verdict、全source blockからJA blockへのcoverage（欠落・重複なし）、quality fields、findings（id/sourceLocator/jaLocator/description）を必須とする。mainは結果のrequestId・assignment・hashを照合してからprovisional stateを保存する。reviewerとtranslator/mainのassignmentは別run/contextでなければならず、実際のsubagent/session handleをmainが受け取り、任意文字列の自己申告を受け付けない。mainは`approved`を自己設定しない。JA修正後はhash mismatchで未承認となり、同じreviewerが再確認する。
- agentはgit add/commit/push/reset/checkoutを行わない。`manifest.json`、tracker、site、root/reference、dependency、英語source、notebook、allowlist外pathは変更しない。

## Progress

### Done

- Week 02〜24の対象source Markdownが69件、対応する`.ja.md`が0件であることを確認した。
- Week 01の既存日本語訳、week-template、checker、Goal controller、workflow templateを調査した。
- ユーザー決定（validator強化、別bilingual reviewer、retry、英語sourceからのlinkなし、日本語indexのみ）を反映した。
- 旧Plan revision 1〜3をround 2でSTOPし、監査履歴を`unresolved.md`へ保存した。
- Codex AstraのPlan recommendationを取得し、single state、固定schema、直列main駆動、scoped mode、fault-injection、Goal toolの実装制約を採用した。

### In Progress

- 実装完了。最終確認（V1〜V6実測）とcommit、task完了報告のみ残す。

### Blocked

- なし（旧STOP系は`unresolved.md`のHuman resolutionにより解消。Goal recordはセッションcwd制約のため未作成、tktk task #70が唯一のtask record）。

## Key Decisions

- `scripts/check_translations.py`は読み取り専用check modeとmain専用state actionを持つ。actionは`init`、`begin-translation`、`accept-translation`、`record-failure`、`begin-review`、`record-review`、`approve-review`、`advance`、`finalize`、`render-report`、`recover-load`に限定し、schema・digest・許可遷移を検証する。`recover-load`はvalid canonical stateだけを読み、壊れたstateを再構築しない。
- validator modeを明示する。`--mode translation --weeks 02-06`は対象15 pair、全baseline、全source/notebook hash、allowlist、既存state、構造/protected/linkを必須にし、将来週のJAと未完index/review rowを保留する。`--mode review --weeks 02-06`は対象15 pairがtranslatedで、provisional review result・current hash・distinct assignment・quality fieldがあることを必須にする。`--mode full`はP9でのみ使い、69 pair、23 index link、41週local notebook link、全state/report、全global invariantを必須にする。
- source-derived protected-token/block manifestはP0で固定し、candidate extractor（backtick外のCamelCase、hyphen/underscoreを含むidentifier、uppercase/digit acronym、vendor/model/protocol/API/CLI名、environment variable、filename、license identifier、Markdown block/paragraph locator）で全sourceを走査する。各candidateを`protected`、`allowed-translatable`、`ignored-with-reason`へ分類し、未分類candidateが0件になるまでP0を完了しない。manifestにはcategory、exact token、occurrence count、locator、分類理由を保存し、JA側はcategoryごとにexact count/locator対応を検査する。
- Quizのoption grammarはquestionごとにsourceから固定する。`a.`〜`d.`、inline `(a)`〜`(d)`、`- A)`〜`- D)`、`- (a)`〜`- (d)`を解析し、answer keyの`**b.**`、`**(b)**`、`**B)**`、`**B.**`、`**B**:`、`**B: free text.**`等の形式を保持する。question/answerは番号1〜10の一意な順序、option label集合、answer labelの1対1対応を検査し、形式ごとの削除・重複・case/記号変更・answer swapをself-testする。未認識形式はshort answerへ黙ってfallbackせずP0でSTOPする。
- `--self-test`は`TemporaryDirectory`内で本番state writerを使う。initの既存target、baseline/state publication境界、no-clobber、partial write、flush/fsync/replace/readback failure、old state保持、invalid tempからの復元禁止、stale digest、unknown enum、attempt上限、review role違反、各quiz grammar、report stale digestをfault/mutationとして検証する。実worktreeのpath inventory・source/notebook/baseline hash・statusは前後一致させる。
- reportは`translation-review-state.json`のstateだけから、sourcePath順・固定template・UTF-8/LF・末尾LF 1個で生成する。headerに`formatVersion`、`baselineId`、`manifestDigest`、`stateDigest`を含め、V1はcanonical stateからのdigestと`render(state)`の全bytes一致を検査する。reportはresumeのsourceではない。
- Goal recordと`goal.md`がGoal昇格後の完了条件のSoTである。`TASK.md`はgoal binding後にGoalへのpointer、taskId、statusだけへ縮小し、P9でmainが直列更新する。reviewer/state/reportの作業stateは`translation-review-state.json`だけが正である。
- generic `goal-workflow.js`はplannerがstepを再生成し、最大4並列・failure時replanするため、このGoalの実装駆動には使わない。Goal runはlifecycle/evidenceの単位とし、mainがP0→P1→P2→P3→P4→P5→P6→P7a→P8a→…→P7e→P8e→P9を固定順で直接駆動し、各stepのprecondition・state action・attempt・STOPを検査する。workflowRunIdは使わず、Goal runの必須軸はrunId/generationとする。workflow templateを要求する実行環境では、source/JA/stateを変更しない決定論的preflight scriptだけを起動し、generic implement/replan経路を許可しない。
- Goal toolは実装契約に従う。成功経路では`goal_begin_run`→main direct execution→`goal_verify`→`goal_complete`とし、同じrunへ`goal_record_result`を先行させない。`goal_verify`失敗やblocked handoffでrunがsettledした後は、同じGoalの新runを`goal_begin_run`で登録し、同じgeneration・baselineId・stateDigestを照合して再検証する。run failureはGoal全体を自動完了扱いにせず、`tktk_block` evidenceを残す。bind失敗時はgoalIdを保持して同じbindをretryし、`goal_start`を重複実行しない。

### State action transition ledger

| action | precondition | state change | failure / idempotency |
|---|---|---|---|
| `init` | baseline/state both absent; clean allowlist | publish baseline, publish 69 `pending` rows, then `active/P0` | existing target or publication failure → STOP; same requestId replay is no-op only after digest match |
| `begin-translation` | row `pending`/`failed`, `translationAttempt < 2`, `activeOperation=null` | increment translationAttempt, set `in_progress`, set activeOperation with requestId/hash/assignment | duplicate requestId is no-op; stale hash/scope → conflict, no write |
| `accept-translation` | row `in_progress`, scoped pass, current JA hash | set `translated`, clear activeOperation, preserve attempt | same hash replay is no-op; mismatch → `JA_HASH_CONFLICT` |
| `begin-review` | row `translated`, review pending/rejected, `reviewAttempt < 2` | set `in_progress`, set activeOperation and reviewerAssignment | same requestId/hash is no-op; missing reviewer assignment → `REVIEW_PROTOCOL_ERROR` |
| `record-review` | matching requestId, current source/JA hash, provisional not yet committed | set `provisional` or `rejected`, store complete reviewResult, clear activeOperation | stale/partial result rejected; exact replay is no-op |
| `approve-review` | provisional result has complete coverage/quality, current hashes, distinct assignments | set `approved`, advance phase only when batch is complete | incomplete result → `REVIEW_PROTOCOL_ERROR` |
| `record-failure` | activeOperation matches request | clear activeOperation; retryable code returns row to pending, terminal code sets stopped | unknown code → `PERMANENT_ERROR`; duplicate event is no-op |
| `finalize` / `render-report` | all rows approved, current hashes, no activeOperation | set `ready_for_verification`, render deterministic report | any missing row/digest/report mismatch → `VERIFICATION_FAILED` |

翻訳のattempt budgetとreview/fixのattempt budgetは別々に数える。worker中断は`WORKER_INTERRUPTED`としてactiveOperationを解消し、retry可能ならrowをpendingへ戻す。terminal STOPでは`executionStatus=stopped`、`stopCode`、handoff payloadを保存し、同じrunで続行しない。Goal runがsettledした後の再検証は新しいrunId/generationで行う。

### V1/V2 traceability matrix

| Outcome条件 | V1のfull/partial検査 | V2のisolated mutation/fault |
|---|---|---|
| 69 JA pair・allowlist・index | inventory、exact allowlist、index 23 links、untracked whitespace/conflict marker/EOF | JA削除、index link削除、余計なpath、trailing whitespaceを拒否 |
| source/notebook/baseline不変性 | baseCommit、69 source hash、45 notebook hash、baseline manifestDigest | source本文、notebook、baseline payload/digest改変を拒否 |
| Markdown構造 | heading level列、table shape、fence info/body、Mermaid | 各構造要素の削除・改変を拒否 |
| protected token | inline code、bare token manifest、本文URL/path、数値 | 各token categoryの削除・改変を拒否 |
| quiz | question番号、option grammar、answer label/番号の1対1対応 | 各option形式の削除・重複・case/記号変更・answer swapを拒否 |
| navigation | index、JA→source/sibling、README→週local全notebook graph | 別週link、英語filename誤り、notebook link欠落を拒否 |
| review品質 | 69 unique row、current hash、distinct assignment、全quality field、approved | row削除、stale hash、role違反、field欠落、approved偽装を拒否 |
| state/report安全性 | state schema/digest、lastCompletedPhase、report header/deterministic bytes | atomic writer fault、invalid recovery、stale report digestを拒否 |

## Next Steps

1. `goal_validate_contract`でこのPlan revisionを検証する。
2. 新しいbounded review cycleを実施する。round 1は通常review→別clean-context敵対的review、採用したblocking findingの指す節だけを修正する。round 2は変更節・参照節だけを新しいclean-context敵対的reviewerへ渡し、同じfinding IDの再発またはblocking残存時は追加修正せずSTOPする。
3. review承認後、worktree root `/Users/yohei/dev/github.com/zorost/AI-Engineering-Lab.feature-translate-curriculum-ja`で`tktk_touch(key="70")`を呼ぶ。`goal_start(slug="translate-curriculum-ja", title="カリキュラム日本語化", worktree=<絶対パス>, contract=<絶対パス>, taskId=70)`が成功したらgoalIdを保持し、`tktk_goal_bind(key="70", goalId=<goalId>)`を同じgoalIdで実行する。cwd不一致、tool error、binding不整合なら翻訳を開始せずSTOPする。
4. `goal_begin_run(goalId=<goalId>)`でrunId/generationを登録する。mainが固定順P0〜P9を直接駆動し、各stepのstate precondition/postconditionとallowlistを検査する。generic workflow templateは起動しない。実行環境がworkflow起動を必須にする場合だけ、source/JA/stateを変更しないdeterministic preflight scriptを起動し、implement/replan経路は拒否する。runId/generationが不一致ならSTOPする。
5. P0でbaselineと69 pending rowのstateを一度だけatomicに初期化する。baseline作成→state作成→baselineId/baseCommit/manifestDigestを`goal.md`と`tktk_log`へ記録→`advance(P0)`の順とする。baseline/stateが揃っていてGoal記録だけ欠落した場合は`BASELINE_RECORD_MISSING`、片側欠落は`STATE_MISSING`としてSTOPし、再生成しない。P0 publication境界のfault結果もstate/logへhandoffする。
6. mainがP1〜P5を直列に実行する。各workerに絶対worktreeを渡し、対象batchをatomicに生成した後、`uv run scripts/check_translations.py --mode translation --weeks <range>`を実行する。pass後だけmainがstate rowを`translated`へatomic更新する。途中停止時はstateのpending/in_progress rowとattempt/failure codeから再開し、validなJA fileを再生成しない。
7. P6で`curriculum/README.ja.md`に23週のJA README linkだけを追加し、index検査を通す。各batchのreviewは、`begin-review`でrequestId・対象hash・reviewer assignmentをprovisional stateへ先に記録→read-only bilingual reviewerがstructured resultを返す→mainがrequestId・assignment・hash・coverageを照合して`record-review`→`uv run scripts/check_translations.py --mode review --weeks <range>`→`approve-review`の順で行う。rejectがあれば同batchのP8相当でmainが指摘pairだけを修正し、同じreviewerが再確認してapprovedにする。translationAttemptとreviewAttemptを混同せず、attempt=2、未知code、hash conflict、budget failureでは次batchを開始せずhandoffする。
8. P9の入口は全69 row approved、current hash一致、state `lastCompletedPhase=P8e`、`activeOperation=null`。mainが`finalize`→`render-report`を実行し、report header/digest/全bytesを検証する。mainがTASK.mdをGoal pointer/statusだけへ縮小し、Goal/contract/state/reportの最終bytesを固定してからV1〜V6を診断実行する（結果を自己申告だけで完了判定に使わない）。verification後はTASK/contract/report/stateを変更しない。
9. 診断が成功した同じGoal runで`goal_verify(goalId=<goalId>, runId=<runId>, generation=<generation>)`を一度だけ実行する。controllerがVerification surface全行をmeasured evidenceとして記録し、`goal_show`でsettled/result pass、measuredAt、generationを確認する。V1〜V6の欠落、argv不一致、exit mismatch、tool errorがあれば`goal_complete`せず、新run/retryまたは`tktk_block`へhandoffする。成功時のみ`goal_complete(goalId=<goalId>, summary=<完了要約>)`を呼び、その後に`tktk_done(key="70", summary=<要件ごとの検証結果>)`を実行する。Goal recordがcompleteでない場合はtktk_doneを呼ばない。範囲外pathがあれば削除・rollbackせずSTOPする。

## Critical Context

### Scope

**In**

- `curriculum/week-02`〜`curriculum/week-24`の`README.ja.md`、`exercises.ja.md`、`quiz.ja.md`（69ファイル）。
- `curriculum/README.ja.md`のWeek 02〜24 navigation index。
- `scripts/check_translations.py`と`--self-test`、`scripts/translation_baseline.json`。
- `curriculum/translation-review-state.json`（唯一のreview/resume state）。
- `curriculum/translation-review.md`（P9でstateから生成するreport）。
- Goal契約、TASK.md、作業進捗、`unresolved.md`の監査履歴。

**Exact allowlist**

- `TASK.md`、`goals/translate-curriculum-ja/goal.md`、`goals/translate-curriculum-ja/unresolved.md`
- `scripts/check_translations.py`、`scripts/translation_baseline.json`
- `curriculum/README.ja.md`
- 各`week-02`〜`week-24`の次の3 pathだけ：`README.ja.md`、`exercises.ja.md`、`quiz.ja.md`
- `curriculum/translation-review-state.json`、`curriculum/translation-review.md`

**Out**

- `curriculum/week-01/**`の既存成果物。
- Week 02〜24の英語原文（`README.md`、`exercises.md`、`quiz.md`）への全変更。
- Week 02〜24の`*.ipynb`およびそのMarkdown cell。
- `curriculum/manifest.json`、`curriculum/tracking/**`のtracker、`docs/index.html`、root/reference文書、site生成物、依存関係。
- 教材内容の追加、third-party教材の転載、secret、allowlist外の全path。

### Verification surface

| rowId | cwd | argv | expectedExit | artifact |
|---|---|---|---:|---|
| V1 | `.` | `["uv", "run", "scripts/check_translations.py", "--mode", "full"]` | 0 | `-` |
| V2 | `.` | `["uv", "run", "scripts/check_translations.py", "--self-test"]` | 0 | `scripts/check_translations.py` |
| V3 | `.` | `["uv", "run", "scripts/check_links.py"]` | 0 | `-` |
| V4 | `.` | `["uv", "run", "scripts/check_notebooks.py"]` | 0 | `-` |
| V5 | `.` | `["uv", "run", "--with", "openpyxl", "scripts/release_check.py"]` | 0 | `curriculum/tracking/ai-engineering-lab-24-week-tracker.xlsx` |
| V6 | `.` | `["git", "diff", "--check"]` | 0 | `-` |

### Implementation plan

| Step | Owner | Write-set | Depends on | Reversibility |
|---|---|---|---|---|
| P0 | main | `scripts/check_translations.py`, `scripts/translation_baseline.json`, `curriculum/translation-review-state.json`, `goals/translate-curriculum-ja/goal.md` | Goal record/binding/run登録 | baseline/state/validatorを削除して可逆。epoch再初期化は不可。Goal記録欠落はSTOP |
| P1 | translation-W02-06 + main-record | Week 02〜06の各3 `.ja.md`とstate対象row | P0 | 15 pair削除で可逆。scoped pass後だけtranslated確定 |
| P2 | translation-W07-11 + main-record | Week 07〜11の各3 `.ja.md`とstate対象row | P1 | P1 state digestを保持して直列 |
| P3 | translation-W12-16 + main-record | Week 12〜16の各3 `.ja.md`とstate対象row | P2 | hash conflictは次stepを開始しない |
| P4 | translation-W17-20 + main-record | Week 17〜20の各3 `.ja.md`とstate対象row | P3 | 12 pairとstateをhandoff可能 |
| P5 | translation-W21-24 + main-record | Week 21〜24の各3 `.ja.md`とstate対象row | P4 | 12 pairとstateをhandoff可能 |
| P6 | main | `curriculum/README.ja.md`の23週indexだけ | P5 + translation mode pass | index再生成で可逆 |
| P7a | bilingual-review-W02-06 → main-record | reviewer read-only、stateの15 row | P6 + translation pass | reviewer resultをprovisionalにatomic記録 |
| P8a | main-fix → same reviewer → main-record | P7aが指摘したJA pairとstate row | P7a | 指摘pairだけ修正。approvedはreviewer result後だけ |
| P7b | bilingual-review-W07-11 → main-record | reviewer read-only、stateの15 row | P8a | P7a stateを保持 |
| P8b | main-fix → same reviewer → main-record | P7bが指摘したJA pairとstate row | P7b | attempt上限でSTOP |
| P7c | bilingual-review-W12-16 → main-record | reviewer read-only、stateの15 row | P8b | 同上 |
| P8c | main-fix → same reviewer → main-record | P7cが指摘したJA pairとstate row | P7c | 同上 |
| P7d | bilingual-review-W17-20 → main-record | reviewer read-only、stateの12 row | P8c | 未レビューrowとfailure codeをhandoff |
| P8d | main-fix → same reviewer → main-record | P7dが指摘したJA pairとstate row | P7d | 同上 |
| P7e | bilingual-review-W21-24 → main-record | reviewer read-only、stateの12 row | P8d | 69 unique rowがapprovedになるまで未完了 |
| P8e | main-fix → same reviewer → main-record | P7eが指摘したJA pairとstate row | P7e | 再承認されなければSTOP |
| P9 | main | stateからのreport生成、exact allowlist監査、TASK/Goal pointer更新、V1〜V6 | P8e + full finalize | TASK/Goal bytesをverification前に確定。reportはstateから再生成。範囲外差分は削除せずSTOP |

### Review packet evidence

- `curriculum/week-01/README.ja.md`、`exercises.ja.md`、`quiz.ja.md`が既存の日本語文体・navigation・technical term方針の実例である。
- `curriculum/week-02`〜`week-24`には各`README.md`、`exercises.md`、`quiz.md`があり、対応する`.ja.md`はない（source 69 / JA 0）。Week 02〜24の英語notebookは41件、全notebookは45件である。
- `curriculum/_templates/week-template.md`はweekly READMEのrich lesson構造、quizの10問/Answer key、exercisesの4 graded exercise/Hints/Checklistを要求する。
- `scripts/check_links.py`はMarkdown相対linkの存在だけを検査し、`scripts/check_notebooks.py`は45 notebookの構造QA、`scripts/release_check.py`は24週とtrackerを検査する。release checkerは`openpyxl`が必要である。
- `goal-controller/README.md`、`src/run.ts`、`src/verify.ts`では、`goal_begin_run`のrun登録、`goal_record_result`のsettle、controller実測verify、exact argv/exitのcomplete判定が定義されている。`goal_begin_run`の後付けworkflowRunId更新は使わず、runId/generationを必須軸にする。
- generic `goal-workflow.js`はplanner、最大4並列、failure時replanを行うため、実装をmainの固定直列駆動に置く。generic templateは成功経路で起動しない。実行環境がworkflow起動を必須にする場合は、write-set空・agent呼出しなし・payload/cwd検査だけのdeterministic preflight scriptを使い、implement/replan経路を拒否する。
- `tktk_start`はtask #70、worktree `/Users/yohei/dev/github.com/zorost/AI-Engineering-Lab.feature-translate-curriculum-ja`、branch `feature/translate-curriculum-ja`を返した。`goal_validate_contract`は本契約を受理した。
- baseline前にworktree rootで`git status --porcelain=v1 --untracked-files=all`を取得し、TASK/goal/unresolved以外の差分がないことを確認する。P0以降のpathはExact allowlistとmainのstatus監査で固定する。
- Codex Astra（`openai-codex/gpt-6-astra`）が、独自workflow/run A/Bを避け、single state、canonical digest、failure enum、quiz grammar、isolated writer fault test、report digest、scoped review orderを推奨した。これを本revisionの設計根拠とする。
