# Week 22: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 22 README](README.ja.md) · [演習](exercises.ja.md)

各問に答えてから、Answer keyで確認してください。各問の末尾には、出題元のConcepts section（§）またはnotebook cellへのpointerが付いています。

1. **(MCQ)** PySparkにおいて、*action*（実行をtriggerする）はどれですか？ *(Concepts §lazinessを参照)*

   - A) `df.select("id")`
   - B) `df.filter(col("x") > 0)`
   - C) `df.count()`
   - D) `df.withColumn("y", col("x") * 2)`

2. **(Short answer)** notebookのcross-check cellが、完全一致 `py_avg ==
   sql_avg` のtestではなく `match:
   abs(py_avg - sql_avg) < 1e-6` をprintするのはなぜですか？ *(Concepts §PySpark worked example、notebook 01 final cellsを参照)*

3. **(MCQ)** Lakeflow Pipelinesで、*現在のstateを反映するよう再計算され*、dimensionが遅く変わっても正しいのはどのdataset typeですか？ *(Concepts §Lakeflow Pipelinesを参照)*

   - A) streaming table
   - B) materialized view
   - C) temporary view
   - D) external table

4. **(MCQ)** notebook `02-streaming-and-dlt-pipeline.ipynb` で、`@dp.expect_or_drop("weight_positive", "weight_kg > 0")` は `weight_kg = -5` のrowに何をしますか？ *(Concepts §expectations、notebook 02 cell 5を参照)*

   - A) rowを保持し、warning metricを記録する
   - B) pipeline update全体を止める
   - C) rowを除去してupdateを続行する
   - D) weightを0に変換する

5. **(Short answer)** Lakeflowのdataset functionは `collect()`、`count()`、`toPandas()`、`save()` を呼んではいけません。理由を一文で説明してください。 *(Concepts §Lakeflow Pipelinesを参照)*

6. **(MCQ)** 同じsourceに対して二つのStructured Streaming queryを実行しますが、両方を一つのcheckpoint locationに向けています。どうなりますか？ *(Concepts §Structured Streaming、How it breaksを参照)*

   - A) stateを安全に共有し、両方が正しくresumeする
   - B) exactly-onceのresume stateが壊れる。各queryには独自のcheckpointが必要
   - C) 何も起きない。checkpointはread-only
   - D) 二つ目のqueryが黙ってbatchになる

7. **(MCQ)** streaming writeで対応して **いない** Delta sink output modeはどれですか？ *(Concepts §Structured Streamingを参照)*

   - A) Append
   - B) Complete
   - C) Update
   - D) AppendとCompleteはどちらも動く

8. **(Short answer)** PySpark KPI aggregationで、`F.when(F.col("is_on_time"), 1.0).otherwise(0.0)` を `F.avg(...)` でwrapし、boolean columnを直接平均しないのはなぜですか？ *(Concepts §PySpark worked example、notebook 01 cell 7を参照)*

9. **(MCQ)** **Lakeflow Job** のtaskが、依存関係すべてが成功したときだけ実行されるようにしたい。これを表すdefaultのRun-if gateはどれですか？ *(Concepts §Lakeflow Jobsを参照)*

   - A) `AT_LEAST_ONE_SUCCESS`
   - B) `NONE_FAILED`
   - C) `ALL_SUCCESS`
   - D) `ALL_DONE`

10. **(MCQ)** Auto Loader（`cloudFiles`）と `COPY INTO` の比較で、Auto Loaderを選ぶのはどんなときですか？ *(Concepts §Structured Streamingを参照)*

   - A) schemaが変わらない数千のfileを扱うとき
   - B) 数百万のfileや進化するschemaを扱うとき
   - C) Kafka topic専用のとき
   - D) checkpointを避けたいとき

## Answer key

1. **C: `df.count()`.** `count`、`show`、`collect`、`saveAsTable` はactionです。`select`、`filter`、`withColumn` はlazyなtransformationです。

2. **浮動小数点演算**では、等価な二つのaggregationが下桁の数桁で食い違うことがあります。tolerance check（`< 1e-6`）は、丸め差によるfalse negativeなしに「同じ数字」をtestします。

3. **B: materialized view。** 現在のstateを反映するよう再計算されます（"always correct"）。streaming tableは各recordを一度だけ処理し、dimensionの遅い変更では再計算されません。

4. **C: rowを除去して続行します。** `expect_or_drop` は違反rowを捨てます。`@dp.expect` ならwarnして保持し、`expect_or_fail` ならupdateを中断するところです。

5. **それらはeager実行を強制するactionだから**です。これは、pipelineが順序/retryの解決に必要とするdeclarative planを壊します。dataset functionは、触られていないlazyなDataFrameをreturnしなければなりません。

6. **B.** checkpointはqueryごとのoffset、commit、stateを保存します。一つのpathを共有する二つのqueryは、互いのresumeを壊します。各queryに独自のUC volume pathが必要です。

7. **C: Update。** Delta sinkはAppendとCompleteに対応しますが、Update modeには対応しません。

8. **booleanはそのままでは有意に平均できない**ためです。さらに `is_on_time` は推論次第でbooleanにも文字列にもなり得ます。1.0/0.0にcastすれば数値になり、`avg` がそれを正しいon-time rateにします。

9. **C: `ALL_SUCCESS`。** これがdefaultのRun-if gateで、すべての依存taskが成功した後にtaskが実行されます。

10. **B.** Auto Loaderはscaleとschema evolutionのために作られています（数百万のfile、incremental、進化するschema）。`COPY INTO` は安定した数千のfileに対してより単純です。
