# Week 18: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 18 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-foundry-serverless-endpoints.ipynb`を最後まで実行する。
   serverless endpointをdeploy/callし、Week 6のbill-of-lading抽出promptを実行し、
   per-field accuracyと推定costをprintします。printされたcostをWeek 18のtracker
   sheetに記録する。

2. **Standard**: 同じ抽出promptを*二つ目*のdeploymentに対して実行する（例: Azure OpenAI
   のGPT deployment vs Phi-4 serverless endpoint）。per-field accuracyと推定costを比較する
   二行tableをmarkdown cellに追加し、大量volumeのBoL抽出にどちらのmodelを選ぶか、その理由を
   一行で述べる。

3. **Stretch**: support-agent endpointを**AI Gateway**（Azure API Management）の後ろに置く。
   token-rate-limit policyとcontent-safety policyをconfigureし、callのburstを撃ち込んで、
   rate limitが実際にthrottleしたevidenceを掴む。gatewayの後ろでevaluation batchを再実行し、
   scoreがregressしていないことを確認する。

4. **Portfolio**: forkに`foundry-deployment-guide.md`をcommitする（setup手順、endpoint
   call、agent定義、eval trace、cost estimate、gateway config）。これはWeek 20で完成させる
   三cloud比較matrixの**Microsoft列**であり、「ここでXをどうやるか」のnoteを残しておけば
   matrixは勝手に書けます。

## Hints

1. **Easy**: printされるcostは最後の`TOTAL_ESTIMATED_COST_USD`。dry-runでもpipeline全体は
   歩きますが、*本当の*数字にはcredentialが必要です。dry-runの`0.000`を測定値として
   記録しないこと。
2. **Standard**: `call_openai_sdk`を別の`deployment=`引数で再利用する。同じ4文書とseedを
   維持すれば、二つの行は別々のtestではなく公平な比較になります。
3. **Stretch**: rate limitが姿を現すのは*burst*の下だけです。tight loopで多数のrequestを
   撃ち、429/429相当のresponseを数えてthrottleのevidenceにする。
4. **Portfolio**: guideは「ここでXをどうやるか」のlist（endpoint、agent、eval、gateway、
   cost）として構成する。Week 20のmatrixの列は、その見出しから勝手に書けます。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: Azure subscriptionとAI Foundryのhub/projectをsetup（free tier）。
- [ ] Tue: serverless model endpointをdeploy。Python SDKとOpenAI SDKから呼ぶ。
- [ ] Wed: tools付きのsupport agentをFoundryで作成。playgroundでtest。
- [ ] Thu: online evaluation batchを実行。traceを読む。最悪の失敗をfix。
- [ ] Fri: Use case: agentをAI Gatewayの後ろに置く（rate limit + content safety）。costを公開。
- [ ] Sat: Week 18のquiz（quiz.md）を受ける。8/10で合格。scoreをNotesに記録。
- [ ] Milestone: Excel trackerを更新。Foundry deployment guideをcommit。
