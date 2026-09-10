# Week 17: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 17 README](README.ja.md) · [演習](exercises.ja.md)

各問は出典のsectionまたはnotebook cellを明示しています。答えてから、Answer keyで確認してください。

1. **(MCQ)** OpenClawのmemory modelは「modelが覚えているのはdiskに保存されたものだけ」です。
   *stableなpreferences*を格納するのはどのfileで、*durableなfacts/decisions*を格納するのは
   どのfileですか？ *(Concepts §「OpenClaw: 個人assistant runtime」と `reference/agents/openclaw.md` §2.6を参照)*
   - (a) preferencesが`MEMORY.md`。factsが`USER.md`。
   - (b) preferencesが`USER.md`。factsが`MEMORY.md`。
   - (c) 両方とも`DREAMS.md`。
   - (d) file baseのmemoryは存在しない。

2. **(MCQ)** OpenClawのpermission tierを、最も制限的 → 最も許容的な順に並べたものはどれですか？ *(Concepts
   §「OpenClaw: 個人assistant runtime」を参照)*
   - (a) `full → auto → ask → allowlist → deny`
   - (b) `deny → allowlist → ask → auto → full`
   - (c) `ask → deny → auto → full → allowlist`
   - (d) `allowlist → deny → full → auto → ask`

3. **(MCQ)** 「Hermes」はNous Researchによる二つの別物を指します。正しい記述はどれですか？
   *(Concepts §「Hermes: 一つの名前、二つのartifact」を参照)*
   - (a) Hermesはmodelのみ。frameworkは無関係。
   - (b) Hermes *model*はあなたが動かす脳。Hermes Agentは、learning loop、gateway、subagents付きでmodelを動かす*framework*。
   - (c) Hermes Agentはmodel。Hermesはbenchmark。
   - (d) 同じartifactの二つの名前。

4. **(MCQ)** OpenClawをOllamaの`/v1` endpointに向けるとtool callingが壊れるのはなぜですか？ *(Concepts
   §「Hermes」と `reference/agents/openclaw.md` §6を参照)*
   - (a) `/v1` endpointのほうが遅い。
   - (b) OpenClawはOllamaの**native `/api/chat`**と通信する。`/v1`はOpenAI互換endpointで、tool callを壊す。
   - (c) `/v1`はcloud subscriptionが必要。
   - (d) 壊れない。`/v1`が必須。

5. **(MCQ)** observability notebookにおける**span**とは: *(notebook cell [4]とConcepts
   §「Agent operations」を参照)*
   - (a) inputs、outputs、latency、tokensを持つ、traceへlinkされたinstrument済みの一 step。
   - (b) run全体の最終的な答え。
   - (c) modelのparameter数。
   - (d) chat channel内の一つのmessage。

6. **(Short answer)** cost dashboardは`hermes-4-14b`をtokenあたり$0.00で計算します。local modelの
   場合、代わりに*何を*支払うのでしょうか。そしてrunbookはなぜそれをdashboardで引き続き追跡するのでしょうか？
   *(notebook cell [9]とConcepts §「実例1」を参照)*

7. **(MCQ)** production-eval samplingのcellは、threshold 0.85に対してSHIPかHOLDかを決めます。
   sampleされたpass rate `p`が0.85未満のとき、printされるdecisionは: *(notebook cell [11]を参照)*
   - (a) SHIP
   - (b) HOLD。ship前に調査する
   - (c) より大きいsampleでRETRY
   - (d) decisionはprintされない

8. **(Short answer)** 最後のcellは、100個のoperationのうち85%がtracedである状況で、`COVERAGE`を
   `instrumented / total_ops`としてprintします。*残り*の15%が何を表すか、そしてrunbookが0.85を
   受け入れるのではなく100%のcoverageを目指す理由を説明してください。 *(notebook cell [14]とConcepts
   §「実例2」を参照)*

9. **(MCQ)** `reference/agents/openclaw.md` §9.1によれば、最も多い初回実行時のOpenClawの失敗は
   どれですか？ *(Concepts §「うまくいかない理由」を参照)*
   - (a) Gateway portは常に空いている。
   - (b) Ollamaの`/v1` endpointに向けたときtool callingが壊れる。
   - (c) skillは常に発動する。
   - (d) modelはすべてを自動的に覚えている。

10. **(Short answer)** ops runbookが述べる四つのものを挙げ、runbookがdocumentationではなく
    「standing discipline」である理由を一文で説明してください。 *(notebook cell [13]とConcepts
    §「Agent operations」を参照)*

---

## Answer key

1. **(b)**: `USER.md`がstableなpreferences（あなたが誰で、どう答えてほしいか）を持ち、`MEMORY.md`が
   persistすべきdurableなfacts/decisionsを持ちます。

2. **(b)**: `deny → allowlist → ask → auto → full`。最も制限的から最も許容的です。

3. **(b)**: model（Hermes 2/3/4）が脳。Hermes Agentは別個のframeworkです。両者は独立した
   artifactで、自由に組み合わせられます。

4. **(b)**: OpenClawはOllamaのnative `/api/chat`を使います。`/v1` endpointはOpenAI互換の
   surfaceで、tool callingを壊します。

5. **(a)**: spanは、inputs、outputs、latency、tokensを持つinstrument済みの一 step（model callまたは
   tool call）。traceは一つのrunに対するspanの列です。

6. （token単位のAPI spendではなく）**hardwareとlatency**で支払います。modelはあなたのmachineで
   動くからです。それでもdashboardが追跡するのは、always-on assistantの*resource* costとlatencyが、
   token単位の限界costが$0でも、runbookのlatency/cost alertに必要だからです。

7. **(b)**: HOLD（0.85未満）。ship前に調査します。

8. 残りの15%は、tracerをbypassする操作（`untraced_step`）です。runbookが100%を目指すのは、
   instrumentされていないtrafficでの失敗は不可視だからです。traceしない15%こそ、silent regressionが
   隠れる場所であり、metricは「実際にどれだけ見えているか」という正直な答えだからです。

9. **(b)**: Ollamaの`/v1` endpointに向けたときにtool callingが壊れるのが、最も多い初回実行時の失敗です。

10. runbookが述べるもの: **threshold**（pass rate、cost/day、latency、coverage）、**watchすべき
    dashboard**、そして**what-to-do-when**の手順（pass rate低下、cost spike、latency spike、
    低coverageに対して）。standing disciplineなのは、書いて忘れる一度きりの記述ではなく、毎日
    実行する繰り返しのdecisionとthresholdをencodeしているからです。
