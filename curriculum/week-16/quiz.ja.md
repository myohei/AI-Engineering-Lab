# Week 16: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 16 README](README.ja.md) · [演習](exercises.ja.md)

各問は、出元のsectionまたはnotebook cellを明記しています。答えてからkeyを確認してください。

1. **(MCQ)** MCP architectureで、LLMを動かしてconnectionを開始する役割と、能力をexpose
   する役割はどれですか？ *(Concepts §「MCP: one protocol instead of N integrations」を参照)*
   - (a) hostがLLMを動かして開始し、serverが能力をexposeする。
   - (b) serverがLLMを動かし、hostが能力をexposeする。
   - (c) clientがLLMを動かし、serverがconnectionを開始する。
   - (d) hostとserverは同じもの。

2. **(MCQ)** MCPのmessageは、二つのtransport上のJSON-RPC 2.0です。正しい組はどれで、
   notebookが使うのはどちらですか？ *(Concepts と notebook 01 cell [8] を参照)*
   - (a) stdioとStreamable HTTP。notebookは **stdio** を使う。
   - (b) WebSocketとgRPC。notebookはWebSocketを使う。
   - (c) stdioとgRPC。notebookはgRPCを使う。
   - (d) HTTP/1.1とHTTP/2。notebookはHTTP/2を使う。

3. **(MCQ)** 次のうち、MCP serverがexposeできる **primitive** はどれで、READMEで挙げられて
   いるZoroLogisticsでの例はどれですか？ *(Concepts §「MCP: one protocol instead of N
   integrations」を参照)*
   - (a) 「tool」。`track_shipment(shipment_id)` のような、modelがinvokeするfunction。
   - (b) 「channel」。WebChatのようなmessaging surface。
   - (c) 「checkpoint」。保存されたgraph state。
   - (d) 「thread」。会話のkey。

4. **(MCQ)** 最初に **supervisor / manager-worker** patternを選ぶべき、最も重要な理由は:
   *(Concepts §「Multi-agent: the first lesson is restraint」を参照)*
   - (a) 常に最速だから。
   - (b) controlを中央化し（decompose、delegate、synthesize）、保守的でdebugしやすいままでいられるから。
   - (c) context isolationが不要だから。
   - (d) bad handoffを決して起こさないから。

5. **(MCQ)** MCPとA2Aは競合ではなく補完的です。正しいstatementはどれですか？
   *(Concepts §「MCP vs. A2A」を参照)*
   - (a) MCPはagent間delegation用で、A2Aはtool用。
   - (b) MCPは一つのagentをtool/dataにつなぎ、A2Aはagentがsystemをまたいでagentにdelegateできるようにする。
   - (c) A2Aはすべての場面でMCPを置き換える。
   - (d) 同じprotocolの別名。

6. **(Short answer)** notebookの `team_run` は、specialistの仕事に加えて、固定の `+200`
   tokenを課します。この200 tokenは何を表していて、それを *省いた* A/Bは、なぜsingle
   agentに対して不公平ですか？ *(notebook 02 cell [8] と Concepts §「うまくいかない理由」を参照)*

7. **(MCQ)** 10-ticket A/Bで、notebookの `justification` は、このsliceではteamは正当化
   されないと結論します。その結論を導く観察の組合わせはどれですか？
   *(notebook 02 cell [13] を参照)*
   - (a) accuracyは同等なのに、teamはaccuracy gainなしにhandoff + synthesisへより多くのtokenを使っている。
   - (b) teamのほうが正確だが、遅い。
   - (c) single agentのほうが精度が低く、安い。
   - (d) teamは何も正しくrouteしていない。

8. **(Short answer)** MCP clientの `list_tools()` は、`track_shipment` のtool schemaを
   返します。そのschemaの `required` arrayに何が入るかを書き、呼び出しを決めるとき、
   modelがそのschemaを何に使うかを説明してください。 *(notebook 01 cell [10] と
   Concepts §「MCP: one protocol instead of N integrations」を参照)*

9. **(MCQ)** notebook 02のground-truth mappingは、ticket category `"billing"` をどの
   specialist routeにmapしますか？ *(notebook 02 cell [2] を参照)*
   - (a) `tracking`
   - (b) `docs`
   - (c) `refunds`
   - (d) `escalate`

10. **(Short answer)** multi-agent systemの *benefit* を二つと *cost* を二つ挙げ、分割が
    見合うかを決めるAnthropicのruleを述べてください。 *(Concepts §「Multi-agent: the
    first lesson is restraint」を参照)*

---

## Answer key

1. **(a)**: hostがLLMを動かしてconnectionを開始します。（hostの中の）clientがconnectionを
   持ち、serverが能力をexposeします。

2. **(a)**: stdio（local subprocess）とStreamable HTTP（remote）。notebookは
   `StdioServerParameters` 経由で、serverをstdio subprocessとして起動します。

3. **(a)**: toolはmodelがinvokeするfunction、例: `track_shipment(shipment_id)`。
   resourcesとpromptsが他の二つのprimitiveで、channel/checkpoint/threadはMCP primitive
   ではありません。

4. **(b)**: supervisorはcontrolを中央化し（decompose → delegate → synthesize）、保守的で
   debug可能なdefaultです。それでもbottleneckになり、誤routeもするので、(a)/(d) は誤りです。

5. **(b)**: MCPはcapability layer（agent ↔ tool/data）で、A2Aはinterop layer
   （agent ↔ agent）です。二つは補完的です。

6. +200 tokenは、supervisorのhandoffとsynthesis stepをmodel化しています。これを省くと、
   teamの実際のcostを過小評価します。single agentにはhandoffがないので、比較はteamを
   不当に有利にします。（「supervisor handoff + synthesis overhead」と「teamを実際より
   安く見せる」に触れた答えで満点です。）

7. **(a)**: accuracyが同等なのに、handoff + synthesisによるtoken/costの増え分でaccuracy
   gainがないなら、このsliceではteamは正当化されません。

8. `"required": ["shipment_id"]`。modelはschema（name、properties、required）を、toolの
   *呼び方* の契約として読みます。どの引数を、どんな型で渡すべきか。protocolによって
   強制されるようになった、あの「descriptionはprompt engineering」という考えです。

9. **(c)**: `CAT_TO_ROUTE` は `billing`（と `refund`、`damage`）を `refunds` にmapします。

10. benefit（二つ）: context isolation、role specialization、並列性、failure isolation。
    cost（二つ）: coordination overhead、latency、token、bad handoff。rule: よくprompt
    された一つのagentと良いtoolから始め、agentの前にworkflowを追加し、測定されたbenefitが
    costを上回るときにだけ分割する。
