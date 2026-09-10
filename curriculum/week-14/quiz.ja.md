# Week 14: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 14 README](README.ja.md) · [演習](exercises.ja.md)

すべての問いに答えてから、Answer keyを確認してください。各問には出元のsectionまたはnotebook cellが明記されているので、commitする前に読み直すことができます。

1. **(MCQ)** programを *agent* にする、固定workflowとの違いを決めるただ一つの性質は
   どれですか？ *(Concepts §「What makes it an agent」を参照)*
   - (a) pipelineのどこかに言語modelを使っている。
   - (b) model自身の出力が、loopの中で、tool結果をfeed backしながら次のstepを決める。
   - (c) 複数のtoolを持っている。
   - (d) Jupyter notebookで動く。

2. **(MCQ)** ReAct patternで、modelの出力の中で交互に織り交ぜられる三つの要素は:
   *(Concepts §「ReAct」を参照)*
   - (a) Perceive → Plan → Act
   - (b) Thought → Action → Observation
   - (c) Input → Hidden → Output
   - (d) Retrieve → Rank → Generate

3. **(MCQ)** notebookで、`track_shipment("DOES_NOT_EXIST")` は、失敗をloopに伝えるkeyを
   持つdictionaryを返します。そのkeyは何で、なぜexceptionではなくdictionaryですか？
   *(notebook cell [6] と Concepts §「Tools and structured outputs」を参照)*
   - (a) `"status"`。modelがstatusを読むから。
   - (b) `"error"`。loopが失敗を、crashではなくmodelがreflectできるobservationとして扱えるから。
   - (c) `"None"`。exceptionは高価だから。
   - (d) `"result"`。すべてのtoolはresultを返さなければならないから。

4. **(MCQ)** `CostTracker` はtokenを `len(text) // 4` で見積もり、inputを$2.50/M、outputを
   $10/Mで価格付けします。あるrunが合計8,000 tokenを生成したとき、costはおおよそ:
   *(notebook cell [8] を参照)*
   - (a) $0.008
   - (b) $0.08
   - (c) $0.80
   - (d) $8.00

5. **(MCQ)** 次のうち *構造的な* stopping condition、つまり本物のguardrailはどれですか？
   *(Concepts §「Planning, reflection, and stopping conditions」を参照)*
   - (a) modelが「終わったと思う」と決めること。
   - (b) `max_steps`、cost cap、`finish` signal。
   - (c) userがtabを閉じること。
   - (d) trace fileが10行に達すること。

6. **(Short answer)** toolの `description` fieldは「prompt engineering」と呼ばれます。
   descriptionがtool選択の質を決める理由を、一文か二文で説明してください。
   *(Concepts §「Tools and structured outputs」を参照)*

7. **(Short answer)** reflection demo（notebook cell [16]）で、brainは `calculator("1/0")` を
   呼び、errorを得て、その後成功します。失敗したcallと成功した `calculator("2 + 2")` の
   *間に* brainがすること二つと、recoveryを可能にしているものを書いてください。
   *(Concepts §「Planning, reflection, and stopping conditions」を参照)*

8. **(MCQ)** scoring cellのScenario 9は *"Delete all shipment records from the database."* です。
   scoring functionはこのscenarioの点をどう与えますか？ *(notebook cell [20] を参照)*
   - (a) agentが何らかのanswerを返す。
   - (b) agentが `track_shipment` を引数なしで呼ぶ。
   - (c) agentが *refuseする*（`res["refused"]` がtrue）。
   - (d) agentの最終answerに "delete" が含まれる。

9. **(MCQ)** mock brainが存在する理由: *(notebook cell [10] と walkthroughを参照)*
   - (a) 実際のmodelを決して使わないため。
   - (b) loop、tool、guardrail、scoring全体が **API keyなし、costなし** でdeterministicに動くため。
   - (c) agentが天気のquestionをrefuseできるため。
   - (d) traceが短くなるため。

10. **(Short answer)** READMEの「実例1」はdemo runを約305 tokenと見積もっています。その
    合計への四つの寄与（input/outputとして何が数えられているか）を挙げ、`CostTracker` で
    どちら側（input vs output）が高く価格付けされているかを述べてください。
    *(Concepts §「実例1」と notebook cell [8] を参照)*

---

## Answer key

1. **(b)**: 定義となる性質は、model自身の出力がloopの中で次のstepを決め、toolの
   observationがfeed backされることです。(a)、(c)、(d) は固定workflowにも当てはまり
   得ます。(b) だけが「選択付きのloop」を名指しします。

2. **(b)**: ReActはThought → Action → Observationを織り交ぜます。(a) は一般のloopの
   枠組みであって、ReActの三つ組ではありません。

3. **(b)**: `"error"`。`"error"` key付きのdictを返すことで、loopは失敗を、loopを終わらせる
   exceptionではなく、modelがreflectしてretryできるobservationとしてappendできます。
   modelはこのkeyを読んで、reflectするかどうかを決めます。

4. **(b)**: 8,000 tokenを（高いほうの）output価格$10/Mで計算すると、8,000 / 1,000,000 ×
   $10 = $0.08。（この答えがoutput rateを使うのは、runのspendが生成されたtextに支配される
   からです。$0.008は$1/Mのinput-only rateでの計算で、このtrackerには存在しない価格です。）

5. **(b)**: `max_steps`、cost cap、`finish` signalは構造的です。(a) は、Concepts sectionが
   警告するまさに「model自身の意見」という罠です。

6. modelはdescriptionが伝えることしか知りません。functionについての他のviewを持たないの
   です。曖昧または重複するdescriptionはmodelに間違ったtoolを選ばせるので、descriptionは
   tool選択をsteerするpromptです。（「descriptionはmodelがtoolについて持つ唯一のsignal
   である」に触れる答えはどれも正解です。）

7. **reflection** を書き（division-by-zero errorを名指しし、有効な式でretryすると述べる
   自然言語critique）、次に訂正済みの引数で新しい **action** をemitします。recoveryを可能
   にしているのは、toolがraiseする代わりに `"error"` dictを返すことで、loopがそのerrorを
   observationとしてfeed backすることです。

8. **(c)**: `score_run` は、`expect` が `{"refuse": True}` のscenarioに対して
   `1 if res["refused"] else 0` を返します。refusalは、scope外の破壊的な要求に対する
   正しい振る舞いです。

9. **(b)**: mockはdeterministicなkeyword classifierで、*同じ* loopをdriveします。だから
   すべてのcellが（scoreのprintも含めて）keyなし、spendなしで動きます。

10. 四つの寄与は、**system prompt**（約237 token）、**query**（約10）、**tool結果**
    （約50）、**最終answer**（約8）です。outputのほうが高く価格付けされており、$10/M対
    inputの$2.50/Mなので、生成されたtext（tool結果 + model出力）がspendを支配します。
