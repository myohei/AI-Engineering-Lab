# Week 12: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 12 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-harness-setup-and-comparison.ipynb` を最後のcellまで実行し、
   harness-readiness score（0〜3）をExcel trackerのWeek 12 sheetに記録します。2未満なら、
   そのharnessの `reference/skills/` guideに従ってもう一つinstallして再実行します。

2. **Standard**: notebookの `SPEC.md` templateを `specs/eta-cli-SPEC.md` にcopyし、
   すべてのbracket（一つのrefused tradeoffを含む）を埋めてから、最初のharnessに
   このspecからCLIをbuildさせます。六項目のtest planを実行し、pass/failの行を
   trackerに貼り付けます。

3. **Stretch**: *同じ* `SPEC.md` を二つ目のharnessで実行し、notebookのcomparison
   worksheetのすべてのcell（plan、tokens、cost、quality）を埋めます。一ページの比較を
   書きます。どのharnessがより良いplanを、どのcostで作ったか、teamならどちらを
   選ぶか、そしてなぜか。

4. **Portfolio**: 動く `eta-cli`（test green）、埋まった `SPEC.md`、1ページのharness
   比較をforkにcommitします。どのharnessがbuildしたか、何token/何dollarかかったか、
   拒否した一つのtradeoffは何かを書いた `README` noteを加えます。これはprogram最初の
   「specからtoolのshipまでagentをsteerした」artifactです。

## Hints

1. **Easy**: scoreは `claude`/`opencode`/`dsh` に対する `shutil.which` です。ないtoolは
   gracefulにskipされるので、数字を上げるために無理にinstallせず、今週実際に使う
   ものをinstallしてください。
2. **Standard**: refused-tradeoffの行から書き始めます。CLIが決して *してはならない*
   こと（ETAを捏造する）を述べ、それを捕まえるtest planのpoint（unknown id →
   exit `2`）を書きます。
3. **Stretch**: harness Bには *同一の* `SPEC.md` を使います。変えるのはharnessだけ
   です。worksheetの六つのcolumnをすべて埋めてください。空欄のある比較はvibeです。
4. **Portfolio**: `README` noteには三つのfactが要ります。どのharnessか、
   何token/何dollarか、そして拒否した一つのtradeoff。この三つが「agentをsteerした」
   storyのすべてです。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: 2つのharness（Claude Code + OpenCodeまたはDSH）をinstall・authenticateする。skill guideを読む。
- [ ] Tue: ETA CLIのSPEC.mdを書く。user、constraints、一つのrefused tradeoff、test plan。
- [ ] Wed: agentにCLIをbuildさせる。testを実行する。greenになるまでiterateする。
- [ ] Thu: 同じtaskを二つ目のharnessで繰り返す。plan、cost、code qualityを比較する。
- [ ] Fri: Use case: CLIをshipする。team向けの1ページのharness比較を書く。
- [ ] Sat: Week 12 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。CLIと比較をcommitする。
