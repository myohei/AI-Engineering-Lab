# Week 02: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 02 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-pandas-cleaning.ipynb` を最後まで実行します。最後に、
   clean後のrow countと、取り除かれたduplicate rowの数がprintされます。両方の数字を
   Week 2のtracker sheetに記録してください。

2. **Standard**: raw datasetをprofileし、**五つ**のplanted issueをdocument化します。（1）
   duplicate row、（2）`NaN` weight、（3）`NaN` lane distance、そして自分で見つける
   もう二つ（不可能な値は `delay_hours`、非正の値は `weight_kg`、あるいはlabelと
   `actual_arrival` が矛盾するrowの `status` を確認する）。それぞれについて、finding、
   evidence（countまたはsample row）、fixをprofile reportに書きます。

3. **Stretch**: `notebooks/02-sql-with-duckdb.ipynb` で、「carrier/lane/month別on-time
   rate」のqueryを、plainな `GROUP BY` の代わりに **window function**（例：`AVG(...) OVER
   (PARTITION BY carrier_id, lane_id, month ORDER BY month)`）で書き直し、
   二つのapproachがfloating-point tolerance以内で一致することをassertするcellを追加します。

4. **Portfolio**: **ZoroLogistics data generator + silver dataset** のmilestone
   （[`curriculum/projects/README.md`](../projects/README.md) を参照）を進めます。cleaning
   workflowを実行可能なscript `data/make_silver.py` に変えます。raw dataを再生成（または
   load）し、cleanし、validation suiteを実行し、`data/silver/` に書き出すものです。
   一つのコマンドで、一つのreproducibleなsilver tableです。

## Hints

1. **Easy**: 最後のcellは二つの数字、`CHECKS_PASSED` と
   `SILVER_ROW_COUNT` をprintします。両方記録してください。`CHECKS_PASSED` が
   12でなければ、最初の `FAIL` 行までスクロールして、再実行の前にそのdecisionを直します。
2. **Standard**: *仕込まれていない* 二つのissueには、`delay_hours` をprofileする
   （極端な値はその `describe()` のtailを見る）ことと、`planned_arrival` と
   `planned_departure` の関係をcheckすることが効きます。arrivalがdepartureに
   先行するrowはstructural defectです。
3. **Stretch**: window functionはすべてのrowを保持するので、carrierごとの月次rateをCTEで
   wrapして `AVG(...) OVER (PARTITION BY carrier_id)` を追加します。それから
   二つのapproachが `np.allclose` で一致することをassertします。
4. **Portfolio**: `make_silver.py` は三つの関数、`load_or_generate()`、
   `clean(df)`、`validate(df) -> bool` として構成します。こうするとscriptは、
   notebookと同じ `raw → clean → validate → save` の流れを、一つのコマンドとして
   読めるようになります。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: data qualityの概念を学ぶ。pandas refresher exerciseを実行する。
- [ ] Tue: pandas cleaning notebookを実行する。generator outputの中の5つのdata issueを見つけてdocument化する。
- [ ] Wed: DuckDBでSQL queryを書く。carrier/lane/month別on-time rate、window、top-lane analysis。
- [ ] Thu: 10以上のcheckを持つdata validation suite（pandera）を追加する。
- [ ] Fri: Use case：clean済みsilver datasetとprofile reportを提出する。すべてのcleaning decisionをdocument化する。
- [ ] Sat: Week 2 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。silver pipeline scriptをcommitする。
