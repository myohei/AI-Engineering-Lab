# Week 03: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 03 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-eta-regression-baseline.ipynb` を最後まで実行します。最後に、
   mean/median baselineと三つのregressorのMAE/RMSE比較がprintされます。最良のtest MAEを
   Week 3のtracker sheetに記録してください。

2. **Standard**: 四つ目のregressor（例えば `HistGradientBoostingRegressor`）を、
   *同じ* time-aware splitとfeatureで追加します。同じ比較表にそのMAE/RMSEを報告し、
   baselineに勝ったかどうかと、その差（delta）を一行で述べてください。

3. **Stretch**: 単一のvalidation splitを、scikit-learnの `TimeSeriesSplit` に置き換え、
   最良のmodelをcross-validationし、foldをまたぐMAEのmean ± standard deviationを報告
   します。時間順のcross-validation推定が一つのrandom splitより公平である理由を説明する
   markdown cellを追加します。

4. **Portfolio**: **ETA prediction (ML → DL) with model cards** のmilestone
   （[`curriculum/projects/README.md`](../projects/README.md) を参照）を進めます。Week 3
   model cardと、すべてのrunのmodel、split日付、seed、metricを記録する `experiments.json`
   logをcommitします。これはWeek 4のneural modelが超えるべきraw materialです。

## Hints

1. **Easy**: printされた比較表から、baseline *と* 各modelのMAE/RMSEを記録します。
   「最良」の行はtest MAEが最も低い行で、それはmodelですらないかもしれない（median baselineが最良行になることもある）。
2. **Standard**: 同じ `models` dictに `HistGradientBoostingRegressor` を追加し、同一の
   `Pipeline([("prep", prep), ("model", ...)])` wrapperを保ちます。変わるのはestimator
   だけにします。
3. **Stretch**: `TimeSeriesSplit` は *順序付き* のtrain/test index pairを生成します。
   それをpipelineでiterateしてfoldのMAEsを平均します。fold内でも決してshuffleしない
   ことに注意します。
4. **Portfolio**: `experiments.json` には、splitを割合ではなく二つのcut date（`CUT1`、
   `CUT2`）として保存します。こうするとlogはreproducibleです。「80/20」という文字列は、
   見知らぬ人があなたのsplitを再構築するには十分ではありません。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: 教師あり学習とevalの考え方を学ぶ。modelより先にmetricを選ぶ。
- [ ] Tue: ETA regression baselineを実行。3 modelのMAE/RMSEを比較表にlogする。
- [ ] Wed: time-aware splitとcross-validationを実装。modelを公平に比較する。
- [ ] Thu: on-time classification。precision/recall/F1、thresholdのtradeoff、confusion matrix。
- [ ] Fri: Use case：Week 3 model card（metric、split、top error source）を書いてcommitする。
- [ ] Sat: Week 3 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新。すべてのexperimentをJSON experiment logに記録する。
