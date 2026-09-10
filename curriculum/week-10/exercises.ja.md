# Week 10: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 10 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-sft-dataset-and-lora-training.ipynb` をend-to-endで実行します。dataset size（~300例）と、最後にprintされる最終training lossを、Excel trackerのWeek 10 sheetに記録します。GPUがない場合は、dataset構築cell（CPUのみ）を最後まで実行し、dataset statsを記録します。training cellはskipしたことを注記します。

2. **Standard**: SFT datasetを *別の* seedと ~50の自分で手書きした追加example（生成されたもののcopyではなく、ZoroLogistics向けの本物のinstruction/response pairを書く）で再buildします。LoRA adapterを再trainし、before/after evalで、adapterがextraction evalでbase modelに依然として勝つことを、正確なdeltaとともに示します。

3. **Stretch**: plain LoRAを **DoRA** にswapします（PEFTの `LoraConfig` で `use_dora=True` を設定。あるいはbitsandbytesで4-bit QLoRA baseに切り替え）。他をすべて固定します。before/after eval表をplain-LoRA runと比較し、その追加mechanismが *あなたのtaskに* 見合ったかを一文で書きます。

4. **Portfolio**: **LoRA fine-tuned triage + extraction model** milestone（[`curriculum/projects/README.md`](../projects/README.md) で追跡）をcommitします。adapter config（`r`、`alpha`、target module）、loss curve画像、before/after eval表、catastrophic-forgetting checkの数値、そして正当化付きのdeploy/no-deploy decision。

## Hints

1. **Easy**: Dataset cell（2〜10）はCPUのみです。training cellにはGPUが必要です。GPUなしのhardwareでは、dataset statsを記録し、trainerがskipされたことを注記します。最終の `SFT_EXAMPLES` はprintされます。
2. **Standard**: 生成されたもののcopyではなく、ZoroLogistics向けの *本物の* instruction/response pairを書きます（新しいlane、customsのedge case、damage claim）。deltaが比較可能になるよう、 *同じ* held-out setでevalを再実行します。
3. **Stretch**: `use_dora=True` は `LoraConfig` の一行変更です。唯一の変数がmechanismになるよう、`r`、alpha、target、epoch、dataを同一に保ちます。loss curveではなくbefore/after表を比較します。
4. **Portfolio**: gateが求めるのは、表の両方のcolumn（新task *と* generic）と、明示的なdeploy/no-deployの一文です。数値付きの「don't deploy」は合格する結果です。forgetting checkのないdecisionは違います。

## Checklist（manifest.json + Excel trackerに対応）

- [ ] Mon: fine-tuning理論とselection orderを学ぶ（knowledge-base 06）。
- [ ] Tue: Week 6のcorpusからSFT dataset（instruction + response）をbuildする。
- [ ] Wed: TRL/UnslothでLoRAをtrainする（Colab free tierまたはlocal GPU）。loss curveをlogする。
- [ ] Thu: preference pairを作る。小さなDPO stepを実行する。evalでbefore/afterを比較する。
- [ ] Fri: Use case。before/after eval表をpublishし、deploy vs iterateを決める。
- [ ] Sat: Week 10 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。adapterとeval結果をcommitする。
