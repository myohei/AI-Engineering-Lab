# Week 07: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 07 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `01-rag-policy-bot.ipynb` を `k=3` と `k=10` で再実行します。recallがどう変わるかを報告し、recall@kが何を評価するかについて一文書きます。

2. **Standard**: golden eval setに二つのquestionを追加します（一つは二つのpolicy documentにまたがるもの）。recallを再測定し、直せるmissは直します。

3. **Stretch**: `02-knowledge-graph-lab.ipynb` で `via` constraintを追加します。選んだportを *通る* 最安routeで、合計cost付きの完全なpathを返します。

4. **Portfolio**: RAG botを `projects/policy_bot.py` としてpackage化します（CLI: question in → cited answer out）。golden eval setと保存したrecall数値を付けます。

## Hints

1. **Easy**: `recall_at_k(vector_search, k=3)` と `k=10` を再実行します。recall@kはkについてmonotone non-decreasingなので、precisionが下がっても大きなkが評価される *理由* を説明します。
2. **Standard**: `QUERIES` に二つの `(question, [doc_ids])` tupleを追加します。一つのquestionは `POL-001` と `POL-002` を組み合わせないと答えられないものにします。二つのrecall関数を再実行し、どのarm（vector vs. keyword）が各missを回復したかを調べます。
3. **Stretch**: pathが選んだport nodeを通るようにcandidate `SERVES` edgeをfilterします。`carrier → lane → port → lane → port` をtraverseし、一つのedgeだけでなく二つのleg costを合計する必要があります。
4. **Portfolio**: chunk→embed→index→hybrid→generateのchainを、question文字列を受け取って `(answer, [citations])` を返す関数にwrapします。`recall_hybrid` をJSON fileに保存し、`--eval` でprintします。

## Checklist（manifest.json + Excel trackerに対応）

- [ ] Mon: retrievalの基礎を学ぶ（knowledge-base 05）。
- [ ] Tue: policy corpusをchunkしてembedする。vector indexを構築する。baseline retrieval accuracyを測定する。
- [ ] Wed: hybrid searchとrerankingを追加する。answerでsourceをcitationする。groundednessを測定する。
- [ ] Thu: carrier-lane-port graphをNeo4jで構築する。shortestとcheapest routeをqueryする。
- [ ] Fri: Use case。RAG botがcitation付きで10の未見の質問に答える。retrieval missをlogする。
- [ ] Sat: Week 7 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。RAGとgraph labをcommitする。
