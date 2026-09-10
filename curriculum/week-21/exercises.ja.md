# Week 21: 演習とチェックリスト

> **日本語版** · [英語版](exercises.md) · [Week 21 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-unity-catalog-and-delta-lab.ipynb` を最後まで実行する。最後にbronze row countとtime-travel version数をprintします。両方の数字をWeek 21のtracker sheetに記録してください。

2. **Standard**: `notebooks/02-medallion-sql.ipynb` で、silver層が二つのinvariantをpassすることを検証する: (1) duplicateした `shipment_id` 値がないこと、(2) `NULL` の `weight_kg` や `distance_km` がないこと。使ったimputation値（weight mean、distance mean）と、それぞれへの一文の根拠をdocument化したmarkdown cellを追加する。

3. **Stretch**: window function（`ROW_NUMBER() OVER (PARTITION BY month ORDER BY on_time_rate)`）を使って **月別on-time rate worst 5 lane** をrankする二つ目のgold artifact（tableまたはview）を追加する。どのlane/carrierの組合せを最初に直すべきか、なぜかを一文で述べる。

4. **Portfolio**: **ZoroLogistics lakehouse** milestoneを進める（[`curriculum/projects/README.md`](../projects/README.md) を参照）: gold dashboard queryをAI/BI dashboardとしてpublishし（SQL editor → 実行 → "Create dashboard"）、portfolioに含めるためにCatalog Explorerの **lineage** graph（bronze → silver → gold）をcaptureする。

## Hints

1. **Easy**: notebookを最初から最後まで実行する。`spark.version` や `current_user()` がerrorを出すなら、まだcomputeにattachされていません。記録する二つの数字は `%sql` のcount cellではなく *最後の* cellにあります。
2. **Standard**: silverのquality-check queryを新しい `%sql` cellにcopyする。passするsilverは `null_weights = 0` かつ `distinct_shipments = rows` です。`null_weights > 0` なら `COALESCE` に抜けがあるcolumnがあります。cell 4を読み直してください。
3. **Stretch**: 「月別worst lane」のrankingにはgold aggregationの*後*にwindowが必要です。`ROW_NUMBER() OVER (PARTITION BY month ORDER BY
   on_time_rate)` はgold queryの `GROUP BY` の内側ではなく外側にnestしてください。
4. **Portfolio**: AI/BI dashboardに必要なのはraw gold tableではなく *dashboard-ready* query（notebook 02の3ヶ月rolling）です。lineageはSQL editorではなくCatalog Explorerのtableの **Lineage** tabにあります。

## Checklist（manifest.json + Excel trackerに対応）

- [ ] Mon: Databricks account/workspaceを作成（free trial）。UIを見て回る。
- [ ] Tue: Unity Catalog lab: catalog/schema/volumeを作る。CSV dataをloadする。権限をgrantする。
- [ ] Wed: Delta Lake lab: table作成、time travel、VACUUM、OPTIMIZE、liquid clustering。
- [ ] Thu: SQLでのmedallion: bronze raw → silver clean → shipmentsのgold aggregate。
- [ ] Fri: Use case: lineage付きのgoverned silver/gold table。最初のAI/BI dashboardを作る。
- [ ] Sat: Week 21のquiz（quiz.md）を受ける。8/10で合格。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新し、SQL notebookをcommitする。
