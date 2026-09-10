# Week 11: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 11 README](README.ja.md) · [演習](exercises.ja.md)

まず自分で答えてから、answer keyで確認してください。各問に答えのある場所が記載されているので、間違えたsectionやcellを読み返せます。

## 設問

1. **(MCQ)** Ngのevals + error analysisについての主張は、正確には *何* についての主張ですか？(Concepts intro + KBの「Why this file matters」を参照)
   - A) よりethicalであること
   - B) Velocity。failureを測れるteamは速くshipできる
   - C) GPU costの削減
   - D) Code reviewの置き換え

2. **(MCQ)** knowledge baseが、golden setを発明ではなく *実物の* inputから引くべきだと主張するのはなぜですか？(Concepts §「Golden set」を参照)
   - A) 実物のinputの方が生成が楽だから
   - B) 発明したcaseはあなたの信念をencodeする。実物のcaseは問題をencodeする
   - C) 実物のinputにはlabelが不要だから
   - D) 発明したcaseは常に短すぎるから

3. **(MCQ)** 「正しいが可変の答えを持つgeneration」に合うmetric familyはどれですか？(Concepts §task-metric表を参照)
   - A) Accuracy
   - B) Recall@k
   - C) Rubric付きLLM-as-judge
   - D) Schema conformanceのみ

4. **(Short answer)** `notebooks/01-zoroeval-harness.ipynb` で、groundedness rubricのlevel「3」は何をcatchし、rubricはなぜこのようにanchoredされていますか？(notebook cell 12 + Concepts §「LLM-as-judge」を参照)

5. **(MCQ)** あるjudgeは、倍加した10 sampleのうち9で同じscoreを返しますが、groundedな答え（human label 5）には1を返します。この二つの事実は何を告げていますか？(Concepts 実例1を参照)
   - A) Judgeは完璧
   - B) Self-agreementは高いが、judgeはそのdimensionを依然としてmissする。再calibrateするかhuman reviewにfallbackする
   - C) Rubricは使えないほど曖昧
   - D) Calibrationは無関係

6. **(MCQ)** Workshop notebookで、HLPは何を「fixable」ではなく「upstream」に分類しますか？(notebook cell 10を参照)
   - A) 同じ情報を与えられれば人間も犯すようなfailure
   - B) Ticket triageでの任意のfailure
   - C) 5回より多く起こるfailure
   - D) `trace_id` を持つfailure

7. **(Short answer)** seed-42 run logでは、34のwrong traceをclusterすると `field_date_format`（8）と `hallucinated_rate`（8）が同率topになります。Topのfixable classのcoverageはいくつで、なぜ *最大の* classから直すのですか？(Concepts 実例2を参照)

8. **(MCQ)** `notebooks/02-error-analysis-workshop.ipynb` で、extraction scoreが0.88、thresholdが0.90のとき、`ci_gate(score, threshold)` は `False` を返します。「no」と言えるgateのpointは何ですか？(notebook cell 15 + Concepts §「CIでのeval」を参照)
   - A) Pipelineが速くなる
   - B) 誰もblockしようとしない数値は、誰も信じない数値である
   - C) Modelが決してdeployされないことを保証する
   - D) Eval setを置き換える

9. **(MCQ)** **code metric**（model metricではなく）はどれですか？(Concepts §code vs model表を参照)
   - A) 「答えはpassageにgroundedしているか？」
   - B) 「ticketは正しいqueueにrouteされたか？」
   - C) 「endpointは2秒以内にvalidなJSONを返したか？」
   - D) 「要約はすべてのclaimを捉えているか？」

10. **(Short answer)** Error-analysis loopの五つのstepを挙げ、第五step（failure classをeval setに加え戻す）がloopをratchetにする理由を述べてください。(Concepts §「Error-analysis loop」を参照)

## Answer key

1. **B)** Ngの主張は *velocity* についてです。failureを測ることでteamは速くshipできます。すべての変更が、数値を動かすか動かさないかのどちらかだからです。「data-driven」であることについての軟らかい主張ではありません。

2. **B)** 発明したcaseは問題についてのあなたの *信念* をencodeし、実物のcaseは問題そのものをencodeします。実の顧客ticket一枚が、でっち上げ十枚に値しえます。

3. **C)** 答えが多くの言い方で表せるとき、string matchingはfailします。だからLLM-as-judgeとrubricで採点します（しばしばsimilarity scoreと併用）。

4. **Level 3は「coreの答えはsupportされているが、passageに存在しないclaim（数値、日付、policy詳細）を少なくとも一つ含む」をcatchします。** Rubricはanchoredされており、各levelが具体的なfailureを名指すので、「3 vs 1」は肩をすくめるのではなく、擁護可能で調査する価値があります。

5. **B)** Self-agreement 0.90はrubricが安定していることを意味しますが、安定は正しさではありません。Systematicなmiss（human 5 → judge 1）は、そのdimensionでjudgeが信頼できないことを意味するので、再calibrateするかhuman reviewにfallbackします。Calibrateしていないjudgeは二つ目の未検証modelです。

6. **A)** Upstream = 同じ情報を与えられた有能な人間でもfailする。だからfixはmodelではなくdata/intakeです（例: modelにも人間にも必要なschema contract）。

7. **Coverageはwrong traceの ≈ 8 / 34 ≈ 24%**。最大のclassから直すのは、**頻度が賢さより重要** だからです。最大のclassこそが今週まず値打ちのある一つの変更であり、eval setに加え戻すべきclassです。

8. **B)** Gateの権威はblockする意志から来ます。誰もblockしようとしない数値は、誰も信じない数値です。ここではextraction scoreがbarにfailしてreleaseをblockします。

9. **C)** Code metricはdeterministicなplumbing（schema/parse/latency）を測り、すべてのcommitで速く安く実行されます。他の三つはmodelの確率的outputを測ります。

10. **Traceを読む → failureをclusterする → 頻度で優先順位 → fix → failureをeval setに加え戻す。** 第五stepがratchetです。failしたcase（とfixのbehavior）をeval setに入れることで、そのclassは二度と静かにregressできず、error analysisが一回限りから恒久的な改善loopに変わります。
