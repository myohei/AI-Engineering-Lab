# Week 15: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 15 README](README.ja.md) · [演習](exercises.ja.md)

各問は、出元のsectionまたはnotebook cellを明記しています。答えてからkeyを確認してください。

1. **(MCQ)** state-graph modelで、**node** は何を返しますか？ *(Concepts §「The
   state-graph mental model」と notebook cell [6] を参照)*
   - (a) ゼロから再serializeされたstate全体。
   - (b) そのnodeが変更したfieldだけのpartial state。frameworkがそれをmerge backする。
   - (c) printするための文字列のanswer。
   - (d) 何も返さない。nodeはglobal変数をmutateする。

2. **(MCQ)** notebook cell [4] の `compute_refund(shipment_id)` は、shipmentが48時間超で
   遅れているとき申告valueの10%を、7日超のとき50%を返します。**60時間** 遅れて申告valueが
   **$6,000** のshipmentは、どの結果になりますか？ *(Concepts §「実例1」を参照)*
   - (a) $0（遅れが足りない）
   - (b) $600。$500を超えるので `needs_approval = True`
   - (c) $3,000。そして `needs_approval = False`
   - (d) $600。そして `needs_approval = False`

3. **(MCQ)** `interrupt_before=["refund_approval"]` は、実際には何をしますか？
   *(Concepts §「Human-in-the-loop」と notebook cell [8] を参照)*
   - (a) `refund_approval` nodeを削除する。
   - (b) graphを `refund_approval` の *前で* pauseし、callerにcontrolをyieldする。続けるにはresumeが要る。
   - (c) すべてのticketを `refund_approval` にrouteする。
   - (d) 警告をlogするが、実行は続ける。

4. **(MCQ)** notebook cell [10] で、同じ `thread_id`（`t-1`）上で二つのinvocationが実行
   されます。観測できる帰結と、それがdemoすることは何ですか？ *(Concepts §「Checkpoints,
   resume, and time-travel」を参照)*
   - (a) threadがすでに存在するので、二つ目のrunがcrashする。
   - (b) `history` listがrunをまたいで積もる。durableなstateとしての会話memory。
   - (c) 二つ目のrunが `history` を空にresetする。
   - (d) 二つのrunはisolatedで、何も共有しない。

5. **(MCQ)** Week 14の手書きloopをkeepせずLangGraphを採用する *正しい* 理由はどれですか？
   *(Concepts §「Framework judgment」を参照)*
   - (a) すべてのagentを速くするから。
   - (b) durableでaudit可能、cyclicなcontrol flow、checkpoint、resume、HITLが必要だから。
   - (c) toolが不要になるから。
   - (d) 常により少ないcodeで済むから。

6. **(Short answer)** `AgentState` の異なるfieldを三つ挙げ、それぞれどのnodeが書くかを
   述べてください。 *(Concepts §「The state-graph mental model」の表と notebook cell [2] を参照)*

7. **(Short answer)** checkpointは、最終answerより多くを保存します。checkpointが記録する
   三つのものを挙げ、「crash後のresume」を「最初からやり直す」と違えるものはどれかを
   説明してください。 *(Concepts §「Checkpoints, resume, and time-travel」を参照)*

8. **(MCQ)** `route_after_intent` で、intentが `"escalate"` のときどのkeyが返り、そのkeyは
   `add_conditional_edges` でどのnodeにmapされますか？ *(notebook cell [6] と [8] を参照)*
   - (a) `"tool"` → `tool_node`
   - (b) `"refund_approval"` → `refund_approval_node`
   - (c) `"escalate"` → `escalate_node`
   - (d) `"generate"` → `generate_node`

9. **(Short answer)** nodeごとのtable（notebook cell [14]）は、nodeごとに `calls`、latency、
   tokenを報告します。最終answerのlatencyだけを測るのがmistakeなのはなぜですか？そして
   tracking中心のsampleでは、*output* tokenを支配すると予想されるのはどのnodeですか？
   *(Concepts §「実例2」を参照)*

10. **(MCQ)** LangGraphが **installされていない** とき、notebookは、nodeごとのtableと
    routing accuracyがそれでもprintされるように何をしますか？ *(notebook cell [0] と [8] を参照)*
    - (a) raiseして止まる。
    - (b) manual runnerが *同じnode function* を *同じgraph順* で歩く。
    - (c) すべてのcellをskipする。
    - (d) LangGraphを自動でinstallする。

---

## Answer key

1. **(b)**: nodeは自分が変更したfieldだけを返します。frameworkがそれらをshared stateに
   merge backします。state全体を返すことやglobalをmutateすることは、explicit-state契約を
   崩します。

2. **(b)**: 60時間 > 48h、ただし7日未満 → 10%分岐: $6,000 × 0.10 = $600。$500閾値を
   超えるので `needs_approval = True` です。

3. **(b)**: `interrupt_before` は名前付きnodeの前でpauseしてcontrolをyieldします。runは、
   resume（例: `Command(resume={"approved": True})`）の後だけ進みます。

4. **(b)**: 同じthread上の二つのrunはcheckpointされたstateを共有するので、`history` が
   積もります。隠れた変数ではなく、durableな会話memoryです。

5. **(b)**: LangGraphは、durableでaudit可能なcyclic control flowについてのみ、その複雑さに
   見合います。他の選択肢は誤りです（速くも短くもなく、machineryが増えるだけです）。

6. 三つなら例えば: `intent`（`intent_node` が書く）、`shipment_id`（`intent_node`）、
   `refund_amount` と `needs_approval`（`intent_node`）、`tool_result`（`tool_node`）、
   `final_answer`（`generate`/`escalate`/`refund_approval`）、`history`（すべてのnode）、
   `escalated`（`escalate_node`）。正しいfield→書き手の組三つで満点です。

7. checkpointは、(1) 現在の **state** 全体（すべてのfield）、(2) **thread id**、(3) graph内の
   **位置** を記録します。resumeを違えるのは *state + 位置* です。空のstateで最初のnodeから
   再実行するのではなく、止まったnodeと値から正確に続けられます。

8. **(c)**: `"escalate"` → `escalate_node`。conditional edgeの、人間への引き継ぎ分岐です。

9. 最終answerだけを測ると、時間とtokenが *どこへ* 行くかが隠れます。遅いtool nodeと遅い
   generate nodeは、別のfixが要る別の問題です。tracking中心のsampleでは、JSONの
   tracking/policy結果を出力するので、`tool` がoutput tokenを支配します。

10. **(b)**: notebookは `manual_run` fallbackを定義していて、同じnodeを同じ順で歩きます。
    だからLangGraphがinstallされているかどうかに関係なく、nodeごとのtableとrouting
    accuracyがprintされます。
