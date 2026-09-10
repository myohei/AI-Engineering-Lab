# Week 07: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 07 README](README.ja.md) · [演習](exercises.ja.md)

概念とnotebook codeから答えてください。各問にどこを見ればよいかが記載されています。

1. **(MCQ)** RAGが主に提供するもの、production順に並べると次のどれですか。(a) speed、cost、scale、(b) grounding、freshness、permissions、(c) より少ないtoken、より長いcontext、より低いtemperature、(d) fine-tuning、quantization、caching。*(Concepts §「七段階のpipeline」を参照)*

2. **(Short answer)** RAG pipelineの七つのstageを順に挙げてください。*(Conceptsのdiagram / KB §2を参照)*

3. **(MCQ)** `01-rag-policy-bot.ipynb` で、`section_aware_chunks` は何を基準にsplitしますか。(a) 256 tokenごと、(b) `## ` 見出し、(c) 文境界、(d) embedding-similarityの低下。*(notebook cell 4を参照)*

4. **(Short answer)** 10問のgolden setで、vector-only retrievalは7問hitし、hybrid+rerankは9問hitします。両方のrecall@5の値を書き、deltaが何を意味するか説明してください。*(Concepts 実例1を参照)*

5. **(MCQ)** RRFはranked listをどうfuseしますか。(a) 生のscoreの平均、(b) list横断で1/(k+rank)を合計、(c) 最大のscoreを取る、(d) rankを掛ける。*(Concepts 実例2を参照)*

6. **(Short answer)** `02-knowledge-graph-lab.ipynb` で、`SERVES` edgeの `cost` attributeは何と等しくなっていますか？また、仕込まれたNaN distanceにもかかわらず、graphはどうやってconnectedに保たれていますか？*(notebook cell 4を参照)*

7. **(MCQ)** answer qualityに対する、単一で最もleverageの高いretrieval upgradeは次のどれですか。(a) より大きなembedder、(b) cross-encoderによるreranking、(c) より長いchunk、(d) eval setにより多くのquestion。*(Concepts §「Hybrid searchとreranking」を参照)*

8. **(Short answer)** retrieval（recall@k）とgeneration（groundedness）はなぜ別々に測らなければならないのですか？それぞれの失敗は何を指し示しますか？*(Concepts §「Retrieval eval」を参照)*

9. **(MCQ)** vector RAGよりもknowledge graphで答えるのが最も適切なquestionは次のどれですか。(a) 「late-deliveryのrefundはいくらか？」、(b) 「Long Beachに届くcarrierはどれで、そのcostはいくらか？」、(c) 「dangerous goodsを定義せよ」、(d) 「customs policyを要約せよ」。*(Concepts §「Knowledge graph」を参照)*

10. **(Short answer)** notebook 1のcell 8で、`recall_at_k` はなぜ、正確なchunkそのものを要求するのではなく、top-k chunkの `doc_id` の *いずれか* がrelevantな `doc_id` と一致するかをcheckするのですか？*(notebook cell 7〜8を参照)*

## Answer key

1. **(b)**: grounding（citation可能なtext）、freshness（retrainではなくre-index）、permissions（retrievalの前にindexをfilterする）。
2. **ingest → chunk → embed → index → retrieve → rerank → generate**（citation付き）。
3. **(b)**: `## ` のsection見出しで分割するため、各chunkは、citation metadataとして `doc_id` とsection名を持つ一貫した一つのpolicy sectionになります。
4. **vector-only recall@5 = 0.70、hybrid+rerank recall@5 = 0.90。** delta（回復した2問）は、vector-onlyがmissしたqueryに対してkeyword arm + rerankerが正しいdocumentをfetchしたことを示します。recallはanswer qualityについては何も言いません。
5. **(b)**: `1/(60+rank_vec) + 1/(60+rank_kw)`。signal間の合意が一つの強いsignalをrankで上回り、score normalizationは不要です。
6. `cost = carrier base_rate_usd_per_km_ton × lane distance_km`。NaN distance（とtransit days）はdefault値（900 km / 3 days）で埋められ、すべてのlaneがconnectedのままになります。
7. **(b)**: cross-encoder rerankerはqueryとpassageを一緒に再採点します。generationに比べて安価で、最良のchunkをtopに動かします。
8. recall@kが低いのはindexing/chunkingの問題です（data pathを直す）。recallが高いのにgroundednessが低いのはprompt/generationの問題です（instruction/citationを直す）。単一のend-to-end scoreは、どのlayerが壊れているかを隠します。
9. **(b)**: これは明示的な `SERVES`/`ARRIVES_AT` relationship上のconstrained traversal（shortest/cheapest path）であり、chunk retrievalでは近似しかできません。他はvector RAGが扱うlookup/definition型のquestionです。
10. recall@kは *正しいdocumentをsurfaceしたか* に関するものであって、正確なchunkそのものではありません。relevantなdocumentは複数のchunkに分割されることがあり、正確なpassageを保証するには `k` を巨大にしなければなりません。doc_id checkが標準的なrecallの定義です。
