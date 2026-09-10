# Week 04: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 04 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-pytorch-tensors-and-autograd.ipynb` を最後まで実行します。
   autogradのgradientが手計算の値と一致することを確認し、toy MLPの最終訓練lossを
   Week 4のtracker sheetに記録してください。

2. **Standard**: `notebooks/02-mlp-eta-train-and-eval.ipynb` で、ちょうど一つを意図的に
   壊します（例：learning rateを100倍高くする、featureの正規化をskipする）そして実行
   します。markdown cellで、learning curveからその失敗を診断し（例：lossの爆発、あるいは
   訓練lossがvalidation lossよりはるかに低い）、fixを名指しします。

3. **Stretch**: 三つのhyperparameter、hidden width、dropout rate、weight decayを
   **validation** splitのみを使ってtuneし、最良の組み合わせのvalidation MAEを記録します。
   その後でのみ、test setをちょうど一度だけ評価し、その数字をbaselineと並べて報告します。

4. **Portfolio**: **ETA prediction (ML → DL) with model cards** のmilestone
   （[`curriculum/projects/README.md`](../projects/README.md) を参照）を完成させます。
   (a) neural test MAE、(b) 比較対象のWeek 3 baseline MAE、(c) carrier/lane別の最大error
   clusterと仮説を名指ししたerror-analysis note、この三点を載せたmodel card v2をcommit
   します。

## Hints

1. **Easy**: `y.backward()` の直後に、手計算した `2x` の値を `x.grad.item()` と比較して
   ください。toy-MLPの最終lossはnotebookの最後のcellがprintする数字で、「ほぼゼロ」は
   netがlinearなsignalをlearnしたことを意味します。
2. **Standard**: ちょうど一つのつまみだけを変え（例：`lr=0.1`、またはscalerをskip）、
   再実行します。それからtrain/val curveの *形* を読み、fixの前に失敗を名指しします。
   爆発する値や、発散していくgapなど。
3. **Stretch**: `(width, dropout, weight_decay)` の小さなgridをloopし、それぞれ
   **training** splitで訓練し、**validation** のみでscoreします。最良の組み合わせは
   validation MAEが最も低いもので、test setを実行するのはその後、一度だけです。
4. **Portfolio**: error-analysis noteでは、*数字*（worst carrier/laneの平均絶対error）と
   *仮説*（例：極端なdelayや季節性がそのsliceを支配している）をpairにします。gateは
   数字と「なぜ」であって、数字だけではありません。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: tensor、autograd、computation-graphのmental modelを学ぶ。
- [ ] Tue: MLP notebookを実行。loss curveを確認。一つを意図的に壊して診断する。
- [ ] Wed: dropout/weight decayを追加。validation splitで3 hyperparameterをtuneする。
- [ ] Thu: test setでneural vs baselineを比較。errorをcarrierとlaneで切り分ける。
- [ ] Fri: Use case：error-analysis note（最大error cluster + 仮説）を書く。
- [ ] Sat: Week 4 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新。model card v2をcommitする。
