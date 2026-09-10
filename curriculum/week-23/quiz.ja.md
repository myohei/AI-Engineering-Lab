# Week 23: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 23 README](README.ja.md) · [演習](exercises.ja.md)

各問に答えてから、Answer keyで確認してください。各問の末尾には、出題元のConcepts section（§）またはnotebook cellへのpointerが付いています。

1. **(MCQ)** 古いMLflow Registryの"Staging/Production" stageがdeprecatedになり、aliasが好まれるのはなぜですか？ *(Concepts §aliasesを参照)*

   - A) aliasの方がqueryが速い
   - B) aliasはmutableなので、複数の名前付き参照（Champion、Challenger、`@prod`）を保持し、pointerの付け替えでpromoteできる
   - C) stageはXGBoostで一度も動かなかった
   - D) aliasにはmodel signatureが必要

2. **(Short answer)** `01-mlflow-feature-engineering-training.ipynb` では、`carrier_daily_stats` tableが `timeseries_columns=["metric_date"]` を宣言し、lookupが `timestamp_lookup_key="planned_departure"` を設定しています。timestamp keyを *外して* daily tableを `carrier_id` だけで直接joinすると、trainingに何がleakしますか？ *(Concepts §feature engineering、notebook 01 cell 9を参照)*

3. **(MCQ)** AI Searchの検索modeのうち、vector similarityとkeyword（BM25）matchingをReciprocal Rank Fusionで融合するのはどれですか？ *(Concepts §AI Searchを参照)*

   - A) ANN
   - B) semantic
   - C) hybrid
   - D) direct upload

4. **(MCQ)** `ai_classify` や `ai_extract` のようなAI functionsには、どのruntime環境が必要ですか？ *(Concepts §AI functionsを参照)*

   - A) 任意のclassic all-purpose cluster
   - B) serverless computeとDBR 18.2+
   - C) 専用GPU clusterのみ
   - D) Photon付きPro SQL warehouse

5. **(Short answer)** notebookがgroundednessを「回答のtokenのうちretrieved contextに現れる割合」として計算するのはなぜですか？「回答はそれっぽく見える」とprintするだけではなく。 *(Concepts §worked RAG example、notebook 02 cell 13を参照)*

6. **(MCQ)** champion/challenger比較で、challengerは `daily_*` columnをdropした後にtrainingされます。`champion_MAE < challenger_MAE`（正の「point-in-time gain」）が成り立つことは何を意味しますか？ *(Concepts §worked example、notebook 01 final cellを参照)*

   - A) time-series featureがmodelを害している
   - B) time-series featureがstatic featureを超える予測価値を持つ
   - C) modelがoverfitしている
   - D) training setが小さすぎる

7. **(MCQ)** idle時に$0で済む低trafficのETA endpointが欲しい。正しいserving設定はどれですか？ *(Concepts §Servingを参照)*

   - A) `min_provisioned_throughput > 0`
   - B) `scale_to_zero_enabled: true`
   - C) provisioned throughput
   - D) external-model endpoint

8. **(Short answer)** `ai_mask`（AI function）とUnity Catalog column maskの違いは何ですか？ *(Concepts §AI functions、How it breaksを参照)*

9. **(MCQ)** Genie Agentsが *caller* のgrantを超えられないのはなぜですか？ *(Concepts §Genieを参照)*

   - A) Genieは事前書き込み済みのSQLしか実行しない
   - B) GenieのSQLは、viewerが既に読めるtableに対してviewerとして実行される
   - C) GenieはすべてのSQL functionを無効にする
   - D) Genieは外部model経由でroutingされる

10. **(MCQ)** `02-vector-search-rag.ipynb` のDelta Sync indexは `embedding_vector_column="embedding"`（self-managed）を使います。*managed* な代替は何ですか？ *(Concepts §AI Search、notebook 02 cell 5を参照)*

   - A) `embedding_source_column` + `embedding_model_endpoint_name` を渡して、index側にembedさせる
   - B) vectorを一つずつ `upsert` でuploadする
   - C) managedな代替は存在しない
   - D) embeddingをCSVに保存する

## Answer key

1. **B.** aliasはmutableな名前付き参照なので、Champion、Challenger、`@prod` を同時に保持し、一つのaliasを付け替えるだけでpromoteできます。stageは単一の線形stateを強制していました。

2. **未来のcarrier統計がleakします。** `carrier_daily_stats` を `carrier_id` だけでjoinすると、carrierの *最新の* 統計（shipment出発後の可能性がある）が引っ張られます。timestamp keyはjoinを `planned_departure` 時点のAS OFにするので、出発より前のhistoryだけが使われます。

3. **C: hybrid。** hybridはANN vector searchとBM25 keyword searchをReciprocal Rank Fusionで組み合わせます。

4. **B: serverless computeとDBR 18.2+。** AI functionsはPro/Classic warehouseでは動きません。

5. **groundednessは主張ではなく測定されなければならないから**です。token overlapは、回答がmodelの先入観ではなくretrieved textから作られているかをcheckする、安く再現可能なproxyです。*もっともらしく聞こえる* が条項をでっち上げる回答は低scoreになります。

6. **B.** （AS-OF time-series featureを持つ）championがstaticのみのchallengerに勝つので、point-in-time featureには予測signalがあります。gainはその測定された差です。

7. **B: `scale_to_zero_enabled: true`**（`min_provisioned_throughput: 0` 付き）なら、endpointはidle中にreplicaをゼロまで縮み、requestがcold-startするまで費用がかかりません。

8. **`ai_mask` はcontent変換**です。自由textを（名前付きPII entityをredactして）一度だけbatch操作として書き換えます。**column mask** はquery時に強制される決定論的なgovernance policyで、columnの値を *誰が見られるか* を制御するものであり、textの書き換えではありません。

9. **B.** Genieが生成するSQLは *viewer* として、viewerのUnity Catalog grantで実行されるので、callerが読めないtableを読んだり、unmaskされた値を見たりすることはできません。

10. **A.** managed embeddingでは、`embedding_model_endpoint_name` を使ってDatabricksがtext columnからvectorを計算します。self-managedは、`embedding` columnを自分で事前計算して保存していたことを意味します。
