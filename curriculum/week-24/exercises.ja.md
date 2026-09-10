# Week 24: 演習とチェックリスト

> **日本語版** · [英語版](exercises.md) · [Week 24 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-governance-and-finopps.ipynb` を最後まで実行する。最後にtotal DBUs、estimated cost、audit-event countをprintします。三つともWeek 24のtracker sheetに記録してください。

2. **Standard**: governance notebookに二つ目のcolumn mask（例: `delay_hours` 上）と二つ目のrow filterを追加する。それぞれが *誰を* 守るか、controlを外すと *何が壊れるか*（間違った数字、leak）を一文ずつ書く。

3. **Stretch**: `gold_on_time_kpis` をbronze source tableまで遡るlineage queryを書き、続いて `system.access.column_lineage` で `on_time_rate` の **column-level** lineageを確認する。

4. **Portfolio**: **ZoroLogistics Lakehouse Intelligence capstone** を完成させる: [`reference/platforms/databricks/capstone/`](../../reference/platforms/databricks/capstone/) に従い、Weeks 21〜23のassetsをtarget、governance、FinOps dashboard付きの **Declarative Automation Bundle** にbundleし、deployment guideをportfolioにpublishする。

## Hints

1. **Easy**: notebookを最後のcellまで実行する。記録する三つの数字は `total DBUs (billing)`、`estimated cost USD`、`audit events` です。fresh trialでの `0.0` DBU合計は想定内です。billing tableは時間とともに埋まります。
2. **Standard**: `delay_hours` への二つ目のcolumn maskは、同じ `CREATE FUNCTION … RETURN IF(is_account_group_member(…), value, NULL)` + `ALTER COLUMN … SET MASK` の形に従います。return typeは `DOUBLE` に合わせる。二つ目のrow filterは、別のcolumnをkeyにしたもう一つの `SET ROW FILTER` です。
3. **Stretch**: `system.access.table_lineage` を `gold_on_time_kpis` からbronze sourceへ逆向きにたどる（一hop以上かかります）。続いて `system.access.column_lineage` を `target_column_name = 'on_time_rate'` でfilterする。
4. **Portfolio**: capstoneの `databricks.yml` には `pipelines.medallion` + `jobs.etl_job` が既に宣言されています。`dashboards`、`registered_models`、FinOps datasetをresourceとして追加し、[`reference/platforms/databricks/capstone/README-run.md`](../../reference/platforms/databricks/capstone/README-run.md) の実行順に従ってください。

## Checklist（manifest.json + Excel trackerに対応）

- [ ] Mon: Weeks 22〜23のassetsをDABにbundleする。CLIでvalidateしてdeployする。
- [ ] Tue: CI/CDを追加する: GitHub Actionsがbundleをvalidateしてdeployする。
- [ ] Wed: Governance: row filter + column mask + lineage review。audit queryを書く。
- [ ] Thu: FinOps: billing system-table dashboard。cost改善を一つ見つけてdocument化する。
- [ ] Fri: Use case: capstone demoをend-to-endで + graduation checklist。portfolioをpublishする。
- [ ] Sat: Week 24のquiz（quiz.md）を受ける。8/10で合格。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新: Week 24 done、program complete。🎓
