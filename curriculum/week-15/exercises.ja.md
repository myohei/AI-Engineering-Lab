# Week 15: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 15 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-langgraph-support-agent.ipynb` をmock brainでend-to-endに
   実行します。graph diagram（ASCII/Mermaid）とnodeごとのlatency/token tableを
   Excel trackerのWeek 15 sheetにcopyします。

2. **Standard**: refund-approvalの閾値を `$500` から自分の値に変更し、escalate pathで
   JSONL fileにescalation recordを書き込む新しいnode（`log_escalation`）を一つ追加し、
   新しいnodeが現れるようにgraph可視化を再printします。

3. **Stretch**: 実際のAPI keyで実行し、run途中で意図的にgraphをcrashさせ（例: `tool`
   nodeでraise）、それから `Command(resume=...)` でcheckpointからresumeし、最終answerが
   clean（未crash）runと一致することを確認します。resumeしたcheckpoint IDを記録して
   ください。

4. **Portfolio**: graph agentを (a) 可視化、(b) checkpoint
   config、(c) refund-approval trace とともにcommitします。graphの形、閾値、interruptがどのnodeを守るかを
   述べる `README` blockを加えます（[`curriculum/projects/README.md`](../projects/README.md) で追跡）。

## Hints

1. **Easy**: mock brainで上から下へ実行します。Mermaid diagramとnodeごとの
   latency/token tableを、printされたとおりに正確にcopyしてください。tableの `calls`
   columnが、実際に発火したnodeを教えます。
2. **Standard**: `500.0` の比較はdiagram文字列の中ではなく `compute_refund`/`classify_intent`
   の中にあります。閾値を一箇所で変え、それから `log_escalation` を、JSONL fileに
   一行appendするnodeとして追加し、`escalate` path 上の `escalate` nodeの *手前* に
   配線します。
3. **Stretch**: crashを強制するには `tool_node` の中でraiseし、*同じ* `thread_id` で
   resumeします。resumeされた `final_answer` をclean runのものと比較してください。
   checkpoint idは `graph.get_state(cfg)` から記録します。
4. **Portfolio**: reviewerは `README` blockを冷ややかな目で読みます。graphの形
   （node + edge）、checkpoint config（`MemorySaver`）、閾値、そして *interruptがどの
   nodeを守るか* を述べてください。「HITLを追加した」では足りません。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: graph-based agent設計を学ぶ（reference/knowledge-base/10-agents-multiagent.md + LangGraph docs）。
- [ ] Tue: Week 14 agentをLangGraphにportする。graphを可視化する。
- [ ] Wed: checkpointとresumeを追加する。run途中でcrashさせて復旧する。
- [ ] Thu: $500超のrefundのためのhuman-in-the-loop interruptを追加する。
- [ ] Fri: Use case: approval付きのend-to-end run。nodeごとのlatencyとtokenを記録する。
- [ ] Sat: Week 15 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。graph agentをcommitする。
