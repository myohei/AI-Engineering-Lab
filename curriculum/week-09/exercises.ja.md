# Week 09: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 09 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-quantization-lab.ipynb` をend-to-endで実行します。perplexity ladderとtriage-accuracy表（と最後のquality-vs-VRAM summary数値）がprintされます。FP16 / 8-bit / 4-bitのperplexityとtriage accuracyを、Excel trackerのWeek 9 sheetに記録します。CPU-only hardwareではfallback pathを実行し、*estimateである* ことを明示して、推定ladderを記録します。

2. **Standard**: quantization notebookのmarkdown cellで、7B、8B、13B modelのVRAM表を手計算で再現します。bytes-per-param rule（FP16 ≈ 2、INT8 ≈ 1、INT4 ≈ 0.5）を適用し、[`reference/knowledge-base/06-model-engineering.md`](../../reference/knowledge-base/06-model-engineering.md) の表をsource of truthとして、各sizeに収まるGPUを挙げます。数字はcopyではなくruleに従っていなければなりません。

3. **Stretch**: `notebooks/02-vllm-serving-and-benchmarks.ipynb` を第三のengineに拡張します。SGLang（またはTGI）をinstallし、*同じ* model（`Qwen/Qwen2.5-1.5B-Instruct`）をserveし、同じbatch sizeでlatency/throughput benchmarkを再実行します。新しいengineを比較表のcolumnに追加し、(a) 高QPS serving と (b) すべてのrequestが長いsystem promptを共有するworkload のどちらのengineを選ぶかを一文で書きます。

4. **Portfolio**: `week-09-quality-vs-cost-report.md` を書き、**quantized triage service** milestone（[`curriculum/projects/README.md`](../projects/README.md) で追跡）の最初のartifactとしてcommitします。含めるもの: 測定したperplexity ladder、30-ticket golden setでのprecisionごとのtriage accuracy、vLLM-vs-Ollama benchmark表、そして数値が裏付ける一文のproduction推奨。

## Hints

1. **Easy**: notebookをそのまま実行します。最後のcellが `QUALITY_RETENTION_PCT` をprintします。deviceがFP16のみをliveでreportする場合は、cell 25の *estimate* 行を記録し、cellの言うとおりにestimateと明示します。

2. **Standard**: 手計算表は、7B / 8B / 13B に対する `params × (bits/8)`、FP16（×2）、INT8（×1）、INT4（×0.5）です。copyした値からではなくruleから始めてください。pointは、数字がbytes-per-param定数から *導かれる* ということです。

3. **Stretch**: model（`Qwen/Qwen2.5-1.5B-Instruct`）とbatch sizeを固定し、serverだけを入れ替えます。SGLangの同等物は `python -m sglang.launch_server` です。shared-system-prompt workloadで天秤にかけるのがそのprefix cacheです。

4. **Portfolio**: gateが求めるのは、*quality* 側の数値（perplexity ladder + triage accuracy）と *cost* 側の数値（serving表）を、一つの文に一緒に読み込むことです。片側だけの推奨は半分のdeliverableです。

## Checklist（manifest.json + Excel trackerに対応）

- [ ] Mon: 数値formatとquantization methodを学ぶ（knowledge-base 06）。
- [ ] Tue: 7〜8B modelをbitsandbytesでquantizeする。triage evalでqualityを測る。
- [ ] Wed: llama.cppでGGUF sweep。Q4/Q5/Q8。perplexityとspeedを記録する。
- [ ] Thu: vLLM（OpenAI互換API）でserveする。latencyとthroughputをbenchmarkする。
- [ ] Fri: Use case。quality-vs-cost reportをpublishし、production quantizationを選ぶ。
- [ ] Sat: Week 9 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。reportをcommitする。
