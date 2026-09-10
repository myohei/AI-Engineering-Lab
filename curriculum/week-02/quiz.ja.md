# Week 02: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 02 README](README.ja.md) · [演習](exercises.ja.md)

十問すべてに答えてから、Answer keyで確認してください。*(Concepts §Xを参照)* はREADMEのsubsection、*(notebook cell Yを参照)* は `01-pandas-cleaning.ipynb` または `02-sql-with-duckdb.ipynb` のcellを示します。

1. **Multiple choice。** seed 42では、rawのshipments tableは100,200行で、cleaning notebookの最終silver row countは100,000行です。この200行の違いは何が原因ですか？ *(Concepts §6、Step 4を参照)*
   a. 200個の `NaN` weightがdropされた
   b. 200行のduplicate rowが `drop_duplicates()` で取り除かれた
   c. 200個の非正のweightがdropされた
   d. 200行の不良transit rowがdropされた

2. **Short answer。** notebookは `NaN` の `weight_kg` を、global medianではなく **commodityごとのmedian** でimputeするのはなぜですか？ *(Concepts §2、Step 4を参照)*

3. **Multiple choice。** company全体のon-time rateを計算する単一のSQL expressionはどれですか？ *(notebook「on-time rate」cellを参照)*
   a. `COUNT(is_on_time)`
   b. `SUM(is_on_time) / COUNT(*)`
   c. `AVG(CAST(is_on_time AS INT))`
   d. `MAX(is_on_time)`

4. **Short answer。** `GROUP BY` とwindow functionの違いを、それぞれ一文で説明してください。 *(Concepts §4を参照)*

5. **Multiple choice。** window functionのqueryで、`QUALIFY rnk <= 2` は何をしますか？ *(notebook「window functions」cellを参照)*
   a. 結果全体を2行に制限する
   b. windowで計算されたrankが2以下のrow、すなわち各月のtop 2 carrierだけにfilterする
   c. carrierをアルファベット順にsortする
   d. `monthly` CTEをdeduplicateする

6. **Short answer。** Step 5の12のvalidation checkのうち三つを挙げ、それぞれが守る性質を述べてください。 *(notebook Step 5を参照)*

7. **Multiple choice。** このdatasetにおける **referential integrity** とは何で、それを強制するcheckはどれですか？ *(Concepts §5を参照)*
   a. すべての `weight_kg` が正であること。`(ships["weight_kg"] > 0).all()` で強制される
   b. すべての `shipments.carrier_id`/`lane_id` が既存のmaster keyと一致すること。`isin(...)` で強制される
   c. すべての `shipment_id` が一意であること。`duplicated().sum() == 0` で強制される
   d. すべての `delay_hours` が範囲内であること。`between(-48, 240)` で強制される

8. **Multiple choice。** DuckDBはregisterされたpandas DataFramesの上で直接SQLを実行します。`con.register("shipments", ships)` は何を達成しますか？ *(notebook「register」cellを参照)*
   a. DataFrameを永続的な `.db` fileに書き込む
   b. in-memoryのDataFrameを、`shipments` という名前のquery可能なtableとして公開する
   c. DataFrameをParquetに変換する
   d. DuckDB server processを起動する

9. **Short answer。** rateはbooleanの平均です。100,000行のsilver rowのうち79,566行がon-timeの場合、on-time rate（小数点以下3桁）はいくつですか？また、その *complement*（≈20.4%）はWeek 3のclassification problemにとって何を意味しますか？ *(Concepts §6、Step 3を参照)*

10. **Short answer。** cleaning workflowは、一回限りのscriptではなく、**gate付きの再実行可能なrecipe** である必要があるのはなぜですか？ *(Concepts §5〜6を参照)*

## Answer key

1. **b。** generatorは約0.2%のduplicate row（100,200行中の200行）を仕込みます。`drop_duplicates()` がそれらを取り除き、100,000行が残ります。防御的なdrop（非正のweight、不良transit）は、それらの欠陥が存在しないため0行を取り除きます。

2. **Weightはcargo typeによって変わる** ので、commodityごとのmedianは、単一のglobal数値よりも誠実な推定です。notebookは `groupby("commodity")["weight_kg"].transform("median")` を使います。medianがたまたま近い場合でも、（group内でimputeする）この習慣が重要です。

3. **c。** booleanを `INT`（0/1）にcastして平均すると、on-timeの割合が得られます。`AVG(CAST(is_on_time AS INT))` → ≈0.7957。選択肢a、b、dはrateを計算しません。

4. **`GROUP BY` はrowをgroupごとに一行にcollapse** してreduceします（count/avg/sum）。**window functionは、すべての元のrowを保持したままgroup横断で値を計算します**。例：各carrierをその月の中でrankする。

5. **b。** `RANK() OVER (PARTITION BY month ORDER BY on_time_rate DESC)` が月ごとのrankを割り当て、`QUALIFY rnk <= 2` はrank 1〜2だけ、つまり *各月内の* top二つのcarrierだけを残します。

6. 次のうち三つ：duplicate rowなし。`NaN` の `weight_kg` なし。weightはすべて正。`NaN` の `delay_hours` なし。`NaN` の `is_on_time` なし。`value_usd` は非負。`carrier_id`/`lane_id` のreferential integrity。`is_on_time` はboolean。`delay_hours` は `[-48, 240]` 内。arrivalはdepartureより後。lanesに `NaN` のdistanceなし。それぞれが「silver」contractが必要とする一つのinvariantを守ります。

7. **b。** referential integrityとは、すべてのforeign keyの値（`carrier_id`、`lane_id`）が実在するmaster recordを指すことです。`isin(carriers["carrier_id"])` / `isin(lanes["lane_id"])` のcheckがそれを強制します。

8. **b。** `con.register` はin-memoryのDataFrameをtable名にbindするので、fileもserverもなしでSQLの `FROM shipments` が動きます。dataはmemoryに残ります。

9. **0.796**（79.6%）。complementは **late share ≈ 20.4%** で、これはWeek 3の「on-time vs late」のtargetがimbalancedであることを意味します。常に「on time」と言うclassifierは約79.6%正確でありながら、すべてのlate shipmentを見逃すので、accuracyはheadline metricとして禁止されます。

10. **dataは届き続ける** ので、一回限りのfixは次のbatchでdirtyなtableへと劣化します。recipe + gate（12-check suite）があれば、誰でも `raw → silver` を再実行して、結果がcleanであると *証明* できます。再実行できないcheckは、artifactではなく願望です。
