# Week 11: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 11 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-zoroeval-harness.ipynb` をend-to-endで実行します。（倍加sample上の）judge-agreement rateと（judge vs あなたのhuman labelの）calibration agreementを、Excel trackerのWeek 11 sheetに記録します。API keyがなければ、code-metric cell（extraction + triage accuracy）を実行してそれらを記録し、judge cellはskipしたことを注記します。

2. **Standard**: `ZoroEval` classに *第四の* golden setを追加します。新しいtaskを選び（shipment-note要約またはticketの *priority* classification）、taskに合うmetric（judge-with-rubricまたはexact-match）で10項目のgolden setを書き、同じjudge/agreement pipelineに通します。選んだmetricとその理由をdocument化します。

3. **Stretch**: CI gateを実際のscript `zoroeval/gate.py`（または `scripts/zoroeval_gate.py`）にします。Eval scoreのJSON fileを読み、thresholdを適用し、pass/fail表をprintし、どれかのmetricがthreshold未満なら非零codeでexitします。(a) 良いartifactをpassさせることと (b) わざと壊したartifactをblockすることをdemoします。

4. **Portfolio**: **ZoroEval v1** を **eval harness + CI gate** milestone（[`curriculum/projects/README.md`](../projects/README.md) で追跡）としてcommitします。harness class、三つのgolden set、calibrated judgeとそのagreement数値、error-analysis note（top failure cluster + fix）、そしてgate script。これは後のすべての週がfailure classを追加していくartifactなので、inspectableにします。

## Hints

1. **Easy**: Code-metric cell（extraction + triage）はkeyなしで動きます。`OPENAI_API_KEY` が未設定ならjudge cellはskipされます。実際に動いた数値を記録し、skipされたcellを注記します。
2. **Standard**: Taskに *合う* metricを選びます。Priority labelにはexact-match、要約にはjudge-with-rubric。既存の三つのsetからcopyしたものではなく、domainから拾った本物の10項目を書きます。
3. **Stretch**: `ci_gate(score, threshold)` は既にbooleanを返します。scriptは、scoreのJSONを読み、各metricのthresholdを適用し、PASS/FAILをprintし、どれかのmetricがfailしたら `sys.exit(1)` するだけです。Passするcaseとblockするcaseの両方をdemoします。
4. **Portfolio**: *あなたの* harnessへのgateは自己言及的です。Thresholdのないharnessや、誰もcalibrateしていないjudgeは、自分自身のgateにfailします。Class、三つのset、agreement数値、top-fix noteを一緒にshipします。

## Checklist（manifest.json + Excel trackerに対応）

- [ ] Mon: evalsとerror analysisを学ぶ（knowledge-base 07 + Ngのletters）。
- [ ] Tue: extraction、RAG、triageのgolden eval setを定義する。rubric付きLLM-as-judgeを実装する。
- [ ] Wed: judgeを走らせる。judge agreementを測る。rubricをcalibrateする。
- [ ] Thu: Error analysis。Week 6〜10 artifactのfailureをclusterし、top fixを選ぶ。
- [ ] Fri: Use case。ZoroEval v1がCI風scriptで一つのartifactをgateする。loopをdocument化する。
- [ ] Sat: Week 11 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。ZoroEvalをcommitする。
