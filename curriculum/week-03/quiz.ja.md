# Week 03: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 03 README](README.ja.md) · [演習](exercises.ja.md)

十問すべてに答えてから、Answer keyで確認してください。*(Concepts §Xを参照)* はREADMEのsubsection、*(notebook cell Yを参照)* は `01-eta-regression-baseline.ipynb` または `02-on-time-classification.ipynb` のcellを示します。

1. **Multiple choice。** time-aware splitは何を防ぎ、どのように防ぎますか？ *(Concepts §2、split cellを参照)*
   a. featureを追加することによるoverfitting
   b. `planned_departure` でsplitすることでtrainが常にvalidation/testより前になるようにし、leakageを防ぐ
   c. late classのresamplingによるclass imbalance
   d. より小さいtest setを使うことによるunderfitting

2. **Short answer。** 目的がETAであるのに、modelは生の到着timestampではなく `delay_hours` で訓練されるのはなぜですか？ *(notebook「ETA regression baseline」introを参照)*

3. **Multiple choice。** このdatasetでは、どのbaselineが *最も低い* test MAEを持ち、なぜですか？ *(Concepts §6、worked example 2を参照)*
   a. mean baseline。meanが二乗誤差を最小化するから
   b. median baseline。`delay_hours` は右にskewしており、medianは長い裾にrobustだから
   c. LinearRegression。linearだから
   d. RandomForest。treeはoutlierを扱えるから

4. **Short answer。** regression notebookで、`OneHotEncoder` を通る二つのcategoryと、`StandardScaler` を通る七つのnumeric columnは何ですか？ *(notebook「feature table」cellを参照)*

5. **Multiple choice。** on-time classifierのheadline metricとして **accuracyが禁止される** のはなぜですか？ *(Concepts §4、classification introを参照)*
   a. 二値taskではaccuracyは決して計算されないから
   b. ~20%がlateだと「常にon time」は~80%正確でありながら、すべてのlate shipmentを見逃すから
   c. accuracyにはGPUが必要だから
   d. ここではaccuracyはF1と同一だから

6. **Short answer。** threshold 0.5のLogisticRegressionのrecallは≈ 0.06です。このrecallの値は運用上何を意味し、thresholdを下げるとどう変わりますか？ *(Concepts §6、worked example 3を参照)*

7. **Multiple choice。** classification notebookの `predict_proba(test_df)[:, 1]` は何を返しますか？ *(notebook「threshold」cellを参照)*
   a. 予測されたclass label（0または1）
   b. 行ごとの *late* classの確率（float）
   c. modelのaccuracy
   d. feature importance

8. **Short answer。** Week 3のfeatureの `StandardScaler` をfitするとき、どのsplitで `.fit()` を呼ぶべきで、なぜですか？ *(Concepts §5を参照)*

9. **Multiple choice。** confusion matrixの四つのcellの正しい読み方はどれですか？ *(notebook「confusion matrix」cellを参照)*
   a. 行が予測、列が実際
   b. 対角線＝正解（TNとTP）、非対角＝error（FPとFN）
   c. 行列はon-time rowだけを数える
   d. 行列は構成上対称

10. **Short answer。** 金曜日のZorost gateによると、Week 3 model cardは三つの何を述べなければなりませんか？ *（「The use case」を参照）*

## Answer key

1. **b。** random shuffleは未来のshipmentにmodelを訓練させ、その間に過去がtestに座ることを許します。cut date付きで `planned_departure` 上でsplitすると、trainは厳密にvalより前、valはtestより前になり、未来はleakできません。

2. **`delay_hours` はplanned arrivalへの修正量です**。`planned_arrival + predicted_delay` が調整済みETAです。delayを直接予測することは、scheduleに支配されるtimestampではなく、modelがlearnできる部分（遅れ）を狙い撃ちします。

3. **b。** `delay_hours` は右にskewしている（median 0.73 h vs. mean 3.56 h、max 227.88 h）ため、median baseline（MAE 3.795 h）は裾に耐え、mean baseline（5.088 h）と三つのmodelすべてに勝ちます。

4. **`weather_severity` と `commodity`** が `OneHotEncoder` を通ります。**`distance_km`、`weight_kg`、`value_usd`、`on_time_rate`、`fleet_size`、`month`、`day_of_week`** が `StandardScaler` を通ります。これらは `build_features` の `CAT_COLS` と `NUM_COLS` のlistです。

5. **b。** targetはimbalanced（~20% late）なので、定数「on time」classifierは~80%正確でありながら、late shipmentを一つも捕捉しません。重要なのはlate classなので、accuracyに代わってそのF1/precision/recallを使います。

6. **recall ≈ 0.06は、modelが実際にlateのshipmentのうち~6%しかflagしていないことを意味します**。ほぼすべての違反を見逃しています。thresholdを下げる（例：0.20）と、より多くの行をlateとflagし、recallが（~0.49へ）上がり、precisionが下がります。

7. **b。** `predict_proba` はclass確率の二列arrayを返します。`[:, 1]` は二列目、つまり各行のpositive（`is_late`）classの確率を取ります。

8. **training splitのみで `.fit()` を呼び**、その後validationとtestに `.transform()` します。全dataでfitすると、val/testのmeanと分散が訓練にleakし、modelの見かけの性能が膨らみます。

9. **b。** 行＝実際、列＝予測とすると、対角線に正解（左上TN、右下TP）が載り、非対角にerror（FPとFN）が載ります。thresholdを動かすと、その二つの非対角cellの間で重みが移動します。

10. **headline metric**（ETAにはMAE、on-timeにはlate classのF1）、それを生み出した **正確なsplit**（cut dateであって「80/20」ではない）、そしてerrorをsliceして見つかった **単一の最大error source**（例：厳しいweather、あるlane、あるcarrier）。
