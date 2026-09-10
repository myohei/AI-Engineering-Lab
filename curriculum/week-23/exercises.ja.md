# Week 23: 演習とチェックリスト

> **日本語版** · [英語版](exercises.md) · [Week 23 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-mlflow-feature-engineering-training.ipynb` を最後まで実行する。championとchallengerのtest MAE、そして最終的な `@prod`/`@challenger` version mappingをprintします。四つともWeek 23のtracker sheetに記録してください。

2. **Standard**: `notebooks/02-vector-search-rag.ipynb` で、inline corpusに五つ目のpolicy documentを追加し、再embedし、AI Search indexを再syncし、該当する質問が新しいdocumentをtop結果でretrieveするようになったことを確認する。古いscoreの隣に新しいgroundedness scoreを書き留める。

3. **Stretch**: `01-mlflow-feature-engineering-training.ipynb` で、time-series `FeatureLookup` を外した変種（static featureのみ）をtrainingする。test-MAEの劣化を定量化し、point-in-time featureの価値（leakage防止の測定値）について一文で書く。

4. **Portfolio**: **ZoroLogistics point-in-time ETA model** milestoneを進める: `@prod` modelをModel Serving endpointでserveし、sample feature vectorでcallし、predictionとlatencyをportfolioに記録する。

## Hints

1. **Easy**: notebook 01を最後のcellまで実行する。二つのMAEs、`@prod`/`@challenger` mapping、`point-in-time gain` を記録する。autologgingがwarningを出しても安全です。metricはちゃんとrunに載ります。
2. **Standard**: 五つ目のdocは、`createDataFrame` による書き込みの *前に* inlineの `docs` listに追加する。embed → index（`pipeline_type="TRIGGERED"` にはsyncが必要）→ query を再実行し、新しいgroundedness scoreを古いものと比較する。
3. **Stretch**: notebook 01のchallenger pathを再利用するが、`create_training_set` からpoint-in-time lookupを *丸ごと* 外す。championとのtest-MAE差が、leakage防止の測定値です。
4. **Portfolio**: `@prod` をscale-to-zero endpointでserveし、`dataframe_records`（model signatureが期待するのと同じfeature dict）でcallし、predictionとcold/warm latencyを記録する。

## Checklist（manifest.json + Excel trackerに対応）

- [ ] Mon: MLflow + feature tables: baselineをlogする。point-in-time featureをbuildする。
- [ ] Tue: ETA model（XGBoostまたはPyTorch）をtrainingする。MLflowにregisterする。challengerと比較する。
- [ ] Wed: serving endpoint + AI Gateway rate limitを作る。Pythonからcallする。
- [ ] Thu: Vector Search: policy docsをindexする。ai_queryでRAG chainをbuildする。
- [ ] Fri: Use case: gold tableでGenie space。SQLをverifyする。publishする。
- [ ] Sat: Week 23のquiz（quiz.md）を受ける。8/10で合格。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新し、ML assetsをcommitする。
