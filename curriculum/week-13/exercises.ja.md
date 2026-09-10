# Week 13: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 13 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-loop-log-and-eval-gates.ipynb` をend-to-endに実行します。最後に
   verifier pass rate（0〜1の数字）がprintされます。その数字をExcel trackerの
   Week 13 sheetに記録してください。unit checkが一つでもfailしたらclassifierを直して
   再実行します。目標はpassするverifierであり、赤いcellのscreenshotではありません。

2. **Standard**: unit checkをもう一つ（`billing` category用）と、edge-case eval rowを
   もう一つ（例: 二つのshipment idを含むticket）追加します。verifierを再実行し、
   before/afterのpass rateをloop logに記録します。binaryなunit checkと統計的なevalの
   どちらの層がより多くのdefectを捕まえたか、そしてなぜかを一文で説明します。

3. **Stretch**: *本物の* headless agent loopを回します。`claude` がinstallされて
   いれば、agentic-loop cellのとおりnotebookに対して `claude -p '…'` を使います。
   なければ、あなたのharnessの等価なheadless modeを使います。出力をcaptureし、
   実際のtokenと、出たdefectをlogします。seeded example rowと実際のdataの違いを
   noteしてください。

4. **Portfolio**: Support Bot MVP、loop log（三つのloopすべて）、spec-v1-vs-v2 diffを
   forkにcommitします。短いretrospectiveを加えます。最初に何を信じていて、developerと
   externalのloopが何を修正し、どうやって知ったか。これは、一つのharnessをsteerする
   だけでなく、測定されたloopを回せることを証明するartifactです。

## Hints

1. **Easy**: pass rateは最終cellがprintする数字です。unit checkが一つでも赤ければ、
   まずkeyword listを直します。目標はpassするverifierであり、赤いcellのscreenshot
   ではありません。
2. **Standard**: billing categoryのkeywordは `CATEGORY_KEYWORDS` にあります。billing
   keywordを含むticketの期待categoryと一致するassertionを書き、新しいedge caseを
   実際に捕まえるのはどの層（unit vs eval）かをnoteしてください。
3. **Stretch**: `claude -p`（またはあなたのharnessのheadless mode）は、同じagentを
   script化したものです。stdoutをcaptureし、実際のtoken数とdefectを§4のseeded
   example rowと比較してください。
4. **Portfolio**: retrospectiveには三つの部分が要ります。最初に持っていたbelief、
   各loopが修正したこと、そして変わったと教えてくれたevidence（before/afterの
   pass rate）です。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: 三つのloopとverifier patternを学ぶ（knowledge-base 01）。
- [ ] Tue: support bot MVPのspecを書く。verifier（eval suite + unit test）を定義する。
- [ ] Wed: agentic loop session: verifierがpassするまでbuild → test → fix。loopをlogする。
- [ ] Thu: developer loop: freshな目でreviewし、specを更新し、missしたedge caseを追加する。
- [ ] Fri: Use case: external loop。実際の人にbotを使ってもらう。issueをfileする。spec + evalを更新する。
- [ ] Sat: Week 13 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。MVPとloop logをcommitする。
