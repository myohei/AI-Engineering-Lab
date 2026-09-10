# Week 22: 演習とチェックリスト

> **日本語版** · [英語版](exercises.md) · [Week 22 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-pyspark-data-engineering.ipynb` を最後まで実行する。最後にfinal on-time rateと、PySpark aggregationをSQL版と比較する `match: True/False` をprintします。両方をWeek 22のtracker sheetに記録してください。

2. **Standard**: `01-pyspark-data-engineering.ipynb` で、*各月の中で* on-time rateによってcarrierをrankするwindow functionを追加する。連続する月をまたいで最も改善したcarrierと最も低下したcarrierを特定し、その理由を一文で仮説として書く（`carrier_name` と `region` をjoinして）。

3. **Stretch**: `02-streaming-and-dlt-pipeline.ipynb` で、silver materialized viewに三つ目のexpectationを追加する（例: `@dp.expect_or_fail("non_negative_delay", "delay_hours >= 0")`）。pipelineを再実行し、制約に違反したときにupdateに何が起きるかを `@dp.expect_or_drop` と対比して（markdown cellで）記述する。

4. **Portfolio**: **ZoroLogistics streaming pipeline** milestoneを進める: pipelineをscheduled **Lakeflow Job**（task type Pipeline、run-if `ALL_SUCCESS`）でwrapし、pipeline DAGのscreenshotと監視queryをportfolioにcaptureする。

## Hints

1. **Easy**: notebook 01を最初から最後まで実行する。記録する数字は *最後の* cell（`final on-time rate` と `enriched rows`）にあり、`match: True/False` はその直前のcross-check cellです。`match` が `False` なら、PySparkの `agg` をSQLの `CASE` とdiffしてください。
2. **Standard**: windowは既に存在します（`rank_in_month`）。最も改善/低下したcarrierを見つけるには、各月の `rank_in_month = 1` を前月のものと `carrier_id` でjoinし、`on_time_rate` をdiffする。
3. **Stretch**: `@dp.expect_or_fail` decoratorを `silver` の他のdecoratorの *上に* 追加し、`delay_hours < 0` のrowを `events/` にdropして再実行する。対比: `expect_or_fail` はupdateを中断し、`expect_or_drop` ならrowを除去して続行したはずです。
4. **Portfolio**: Lakeflow Jobの **Pipeline** task typeがpipelineをwrapします。下流taskのrun-ifは `ALL_SUCCESS` に設定し、DAG screenshotと `system.lakeflow.jobs` の監視queryの両方をcaptureする。

## Checklist（manifest.json + Excel trackerに対応）

- [ ] Mon: PySpark lab: DataFramesでshipment dataをtransformする。SQLと比較する。
- [ ] Tue: Python（またはSQL）でDLT pipelineを書く。data qualityにexpectationを付ける。
- [ ] Wed: live shipment event用のstreaming tableを追加する（Auto Loader/streaming source）。
- [ ] Thu: Lakeflow Jobを作る: pipelineのscheduleとorchestrate。runとlineageを確認する。
- [ ] Fri: Use case: streaming KPI pipelineがquality gateをpassする。監視queryをpublishする。
- [ ] Sat: Week 22のquiz（quiz.md）を受ける。8/10で合格。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新し、pipeline codeをcommitする。
