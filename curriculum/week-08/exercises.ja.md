# Week 08: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 08 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `02-vram-sizing-and-model-selection.ipynb` を `task="coding"` と `task="reasoning"` で再実行します。推奨がどう変わるか、なぜかを、それぞれ一文で説明します。

2. **Standard**: catalogに二つのmodelを追加します（例: Gemma 2 9B、Phi-3.5。model cardの実際のlayer/head数を使用）。そして両方のhardware caseでpickerを再実行します。

3. **Stretch**: `01-local-model-playground.ipynb` で `num_ctx` sweep（2048 vs 8192）を追加し、同じpromptについてtokens/secとVRAMのtradeoffを報告します。

4. **Portfolio**: `projects/model_picker.py` を書きます（CLI: hardware GB + task in → model + quant + license + footprint out）。backend benchmark表とともにcommitします。

## Hints

1. **Easy**: `pick_model(16.0, task="coding")` と `task="reasoning"` を呼びます。違いはcatalogではなく `MIN_PARAMS` です。各taskがどのfloorを上げるか、そして推奨がどう動くか（または `None` を返すか）を説明します。
2. **Standard**: 各model cardの実際の `layers`/`heads`/`head_dim` で二つのdictを `CATALOG` にappendします（例: Gemma 2 9B、Phi-3.5）。両方のhardware caseで `list_options` を再実行し、license欄の変化を記録します。
3. **Stretch**: `--verbose` 付きの `benchmark(model, prompt, n=3)` を `num_ctx=2048` と `num_ctx=8192` で（flagとして渡して）実行します。二つの長さについてtokens/sec *と* `kv_cache_gb` のKV-cache GB差を報告します。
4. **Portfolio**: `argparse` で二つの引数（`--gb`、`--task`）。`total_footprint`/`list_options` のlogicを再利用し、top pickとそのlicenseをprintします。benchmark表をその隣のmarkdown fileに書き出します。

## Checklist（manifest.json + Excel trackerに対応）

- [ ] Mon: modelのlandscapeを学ぶ。open vs closed、license、family（knowledge-base 08）。
- [ ] Tue: Ollamaをinstallする。小さいmodelをpullする。chatとstructured outputをlocalで実行する。
- [ ] Wed: llama.cppとMLXを試す。backend横断のtokens/secを表で比較する。
- [ ] Thu: GPU setup check。CUDA/MPS/ROCm。小さいscriptでbenchmarkする。
- [ ] Fri: Use case。local model + VRAM basedのmodel pickerによるticket triage。
- [ ] Sat: Week 8 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。benchmark表とpickerをcommitする。
