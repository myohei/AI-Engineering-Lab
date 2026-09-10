# Week 16: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 16 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-mcp-server-lab.ipynb` をend-to-endに実行します（API key不要）。
   `track_shipment` のtool-schema JSON（`list_tools()` が返したもの）をExcel trackerの
   Week 16 sheetにcopyしてください。

2. **Standard**: MCP serverに四つ目のtool `get_bol(bol_id)` を、`zoro.data.bol_samples()`
   をbackendとして追加します。client connectionを再実行し、新しいtoolをprotocol越しに
   呼びます。その結果が `data.bol_samples()` の直接呼び出しと一致することを確認します。

3. **Stretch**: `notebooks/02-multiagent-triage-team.ipynb` で、四つ目のspecialist
   （billing）とそのrouting ruleを追加し、同じ10 ticketでA/Bを再実行し、新しい
   accuracy/latency/costの数字でarchitecture正当化を書き直します。

4. **Portfolio**: MCP server、triage team、そしてA/B report（`notebooks/02` の出力）を
   commitします。reportは一つのtableと一段落の正当化からなり、hiring-managerが読める
   artifactです（[`curriculum/projects/README.md`](../projects/README.md) で追跡）。

## Hints

1. **Easy**: notebook 01を上から下へ実行します。`mcp` SDKがあれば `ROUND_TRIP_TOOLS`
   の数字は `3` になるはずです。`track_shipment` のschemaは、cell [10] がprintした
   とおりに正確にcopyしてください。
2. **Standard**: server *と* `MANUAL_SCHEMAS` の両方に `get_bol(bol_id)` を追加します。
   `bol_id` は `ZRL-10000` の形です。clientを再接続し（新しい `stdio_client` session）、
   `list_tools()` が四つ目のtoolを拾うようにし、その結果が `data.bol_samples()` の
   直接呼び出しと等しいことをassertします。
3. **Stretch**: `billing` specialistは、`supervisor_classify`、`CAT_TO_ROUTE`、
   `add_conditional_edges` のmapを *まとめて* 拡張して追加します。同じ10 ticketを
   再実行し、新しい `ACCURACY_DELTA` で正当化を書き直します。
4. **Portfolio**: A/B reportこそがartifactです。table *と* 正当化paragraphをshipして
   ください。reviewerが数字とあなたのdecisionを同じ息で見られるように。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: orchestration patternとMCPを学ぶ（knowledge-base/10 + knowledge-base/11）。
- [ ] Tue: ZoroLogistics toolをexposeするMCP serverをbuildする。MCP inspectorでtestする。
- [ ] Wed: multi-agent triage team（supervisor + 3 specialist）をbuildする。
- [ ] Thu: A/B test: 同じ10 taskでmulti-agent vs single agent。qualityとcostを測る。
- [ ] Fri: Use case: A/B reportを公開する。architecture decisionを正当化する。
- [ ] Sat: Week 16 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。teamとMCP serverをcommitする。
