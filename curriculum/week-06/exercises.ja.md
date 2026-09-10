# Week 06: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 06 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `01-prompt-suite-bol-extraction.ipynb` を別のmodelで再実行し（`OPENAI_MODEL` または
   `OPENROUTER_MODEL` を設定）、version-3のscore deltaを報告します。
2. **Standard**: chain-of-thought付きの四番目のprompt versionを追加します（「cargo blockについて
   まずstep by stepで考えよ」）。そのaccuracyとtoken costをversion 3と比較します。
3. **Stretch**: `02-context-engineering.ipynb` に *tiered* なeviction policyを追加します。各budget
   claimantにpinned / compressible / disposableのlabelを付け、3倍長い文書でworksheetを再実行し、
   何が最初に切られるかを示します。
4. **Portfolio**: prompt suiteを `projects/bol_extractor.py` として保存します。JSON eval log
   （version → score → note）と、fieldあたりaccuracyが90%を下回るとfailするgateを付けます。

## Hints

1. **Easy**: 実行前に `OPENAI_MODEL`（または `OPENROUTER_MODEL`）を設定します。version 3だけを
   再実行し、その `OVERALL` 行をdefault modelのscoreとdiffします。
2. **Standard**: `make_prompt` に `version == 4` branchを追加し、「まずcargo blockについて
   推論せよ」という一行を先頭に置きます。accuracy *と* token cost（CoTのtextは追加のinput
   tokenです）を比較します。
3. **Stretch**: worksheetの各claimantにtier label（`pinned`/`compressible`/`disposable`）を
   付け、文書が三倍になったとき、その順序でevictしてから合計を上限に対して再測定します。
4. **Portfolio**: 三つの `make_prompt` versionとgraderを一つの関数でwrapし、`{version: score}`
   をJSONにdumpし、最良scoreが0.90未満なら `sys.exit(1)` します。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: prompt engineeringとcontext engineeringを学ぶ（knowledge-base 04）。
- [ ] Tue: BoL extraction prompt suiteを構築。20のsynthetic文書に対して実行する。
- [ ] Wed: structured outputとfew-shot exampleを追加。per-field accuracyを改善する。
- [ ] Thu: Context engineering。budget、compaction、caching。tokenとlatencyを測る。
- [ ] Fri: Use case：eval setで90%超のfield accuracyに到達。failure caseをdocument化する。
- [ ] Sat: Week 6 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新。prompt suiteとeval結果をcommitする。
