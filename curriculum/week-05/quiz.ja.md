# Week 05: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 05 README](README.ja.md) · [演習](exercises.ja.md)

概念とnotebook codeから答えてください。各問にどこを見ればよいかが記載されています。

1. **(MCQ)** LLMがquestionに「答える」ことは、次のどれとして最もよく記述できますか。(a) knowledge baseから最も近い事実を検索する、(b) 学習済みdistributionから次のtokenを繰り返しsampleする、(c) call間で保存されたreasoning planを実行する、(d) promptをcacheからlookupする。*(Concepts §「Tokenizationは正面玄関」を参照)*

2. **(Short answer)** `01-tokenization-lab.ipynb` で、`enc.encode("ZoroLogistics")` は4 tokenを返すのに `enc.encode("shipment")` は1を返すのはなぜですか？ *(notebook cell 6を参照)*

3. **(MCQ)** causal maskが存在する理由は次のどれですか。(a) attentionが速く走るため、(b) tokenが未来の位置にattendできないため、(c) embeddingが正規化されたままのため、(d) softmaxがoverflowしないため。*(Concepts §「Self-attention」を参照)*

4. **(Short answer)** notebook 1の `estimate_cost` が使う式を書き、Mtokあたり$1.00/$3.00で57 input tokenと60 output tokenのcallあたりcostを計算してください（$0.000001の桁まで）。*(notebook cell 10を参照)*

5. **(MCQ)** notebookのchars/token表で、bill of ladingはおよそいくらでtokenizeされますか。(a) 5.3 chars/token、(b) 3.0 chars/token、(c) 4.0 chars/token、(d) 1.0 chars/token。*(notebook cell 8 / Conceptsの表を参照)*

6. **(Short answer)** `02-embeddings-and-attention-lab.ipynb` で、query *"temperature-sensitive medical cargo that must stay cold"* の正しいtop-1 commodityは何ですか？そしてcosine similarityはなぜそれを一位にしますか？ *(notebook cell 2と6を参照)*

7. **(MCQ)** KV cacheは生成をstepあたりO(n²)からO(n)にしますが、その代償は次のどれですか。(a) より多くのcompute、(b) 列長とともに線形に増えるmemory、(c) causal maskの喪失、(d) より低いtemperature。*(Concepts §「The KV cache」を参照)*

8. **(Short answer)** 7B-class model（32 layer、32 head、head_dim 128）をcontext 4096、FP16として、`2 × layers × heads × head_dim × seq_len × bytes_per_param` でKV-cache sizeをGBで計算してください。*(Concepts 実例2を参照)*

9. **(MCQ)** modelの重みを変えるknowledge獲得の仕組みはどれですか。(a) zero-shot ICL、(b) RAG retrieval、(c) fine-tuning、(d) prompt caching。*(Conceptsの表を参照)*

10. **(Short answer)** notebook 1のcell 12で、100,000 noteを超える一日あたりcostが、最初のnoteのcountではなく *平均* note token countから計算されるのはなぜですか？ *(notebook cell 11〜12を参照)*

## Answer key

1. **(b)**: modelは学習済みdistributionから次のtokenを繰り返しsampleします。「答える」とは、EOS/`max_tokens` まで走るそのloopのことです。
2. **BPE** は頻出の文字pairをmergeしてvocabを構築するので、よく使う語 "shipment" は単一tokenになった一方、珍しいbrand名 "ZoroLogistics" は一度もmergeされずsubword片に分割されます（`Z`/`oro`/`Log`/`istics`）。
3. **(b)**: causal（下三角）maskは未来の位置をゼロにし、tokenは自分自身とそれより前のtokenだけにattendします。これがincrementalな生成を可能にするものでもあります。
4. `(input_tokens/1e6)·price_in + (output_tokens/1e6)·price_out` → `57/1e6·1.00 + 60/1e6·3.00 = 0.000057 + 0.000180 = $0.000237`。
5. **(b)**: BoLは~3.0 chars/token（364文字、123 token）です。IDs、code、数値fieldがsubwordに分割されるためです。
6. **pharmaceuticals**: "pharmaceuticals and medical supplies needing cold-chain handling" が "temperature-sensitive medical cargo" と意味的に最も近く、そのembedding vectorがquery vectorと最も整合します（cosineが最高）。
7. **(b)**: 過去のK/Vをcacheすると各stepはO(n)になりますが、cacheは線形に伸びます（`2·L·H·hd·seq·bpp`）。これが長context servingの支配的なmemory costです。
8. `2 × 32 × 32 × 128 × 4096 × 2 bytes = 2,147,483,648 bytes ≈ 2.15 GB`。
9. **(c)**: fine-tuningが重みを変えます。ICLとRAGは重みに触れず、cachingはservingの最適化です。
10. 一日あたりの数字は *典型的な* noteを表さなければなりません。最初のnoteは平均より長い（41 token vs. ~30）ので、それだけを使うと一日あたりcostを過大に評価します。
