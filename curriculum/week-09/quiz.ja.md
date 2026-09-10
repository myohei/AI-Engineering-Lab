# Week 09: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 09 README](README.ja.md) · [演習](exercises.ja.md)

まず自分で答えてから、answer keyで確認してください。各問に答えのある場所が記載されているので、間違えたsectionやcellを読み返せます。

## 設問

1. **(MCQ)** あるmodelは13B paramsを持ちます。INT4で *weightのみ* のVRAMはどれだけ必要で、どのruleが答えを与えますか？(Concepts §「Formatごとに一つの数値」を参照)
   - A) ~26 GB、13B × 2 bytes
   - B) ~13 GB、13B × 1 byte
   - C) ~6.5 GB、13B × 0.5 bytes
   - D) ~3.25 GB、13B × 0.25 bytes

2. **(MCQ)** `scale ≈ 0.0039`、`zero_point = 0` のinteger quantizationで、float `0.5` はどのintegerにmapされますか？(Concepts 実例2を参照)
   - A) 128
   - B) 255
   - C) 0
   - D) 64

3. **(Short answer)** knowledge baseは、なぜperplexityを「screenであってverdictではない」と言っていますか？ほぼ平坦なperplexity ladderが隠せる、ZoroLogisticsの具体的なfailureを挙げてください。(Concepts §「Perplexityはscreenであってverdictではない」を参照)

4. **(MCQ)** 7B triage modelで、Q2_KはFP16比で~8 F1 pointを失うのに、perplexityはわずかに悪いだけに見えます。正しいproduction判断はどれで、その理由は？(Concepts 実例3を参照)
   - A) Q2_Kをship。最小で最安だから
   - B) Q4_K_Mをship。VRAMの一部でほとんどのF1を保つ。Q2_Kは避ける
   - C) FP16をship。quantizationはリスクが高すぎる
   - D) Q8_0をship。唯一のほぼlosslessな選択肢だから

5. **(MCQ)** `notebooks/01-quantization-lab.ipynb` で、`perplexity()` helper（cell 12）は実際に何を計算しますか？(notebook cell 12を参照)
   - A) noteのtokenにわたる `exp(mean cross-entropy loss)`
   - B) 30 ticketのtriage accuracy
   - C) 各formatのbytes-per-parameter
   - D) 正しくdecodeされるtokenの割合

6. **(Short answer)** lab notebookで、`LIVE_FP16` と `LIVE_QUANT` の違いは何ですか？また、どんなhardware条件がそれぞれを `True` にしますか？(notebook cell 4を参照)

7. **(MCQ)** vLLMがnaiveなbatcherよりも高いthroughputを維持できる理由を説明するmechanismはどれですか？(Concepts §「Serving」を参照)
   - A) すべてのmodelを自動的にINT4にquantizeする
   - B) PagedAttention + continuous batchingが、idleなGPU時間を新しいtokenで埋め戻す
   - C) 常にbatch size 1を使う
   - D) 精度のためにmodelをFP32で実行する

8. **(MCQ)** `notebooks/02-vllm-serving-and-benchmarks.ipynb` で、同じOpenAI SDK clientがvLLMにもOllamaにも動くのはなぜですか？(notebook cell 14を参照)
   - A) どちらのengineも同じdataでtrainingされている
   - B) どちらもOpenAI互換の `/v1` surfaceを出す。変わるのは `base_url` だけ
   - C) notebookがengineごとにSDKにpatchを当てている
   - D) Ollamaが内部でvLLMをimportしている

9. **(Short answer)** 測定結果がFP16 triage accuracy 0.92、INT8 0.92、INT4 0.89、INT4のVRAMはFP16の25%だったとします。Friday reportが求める、数値を付けた一文のproduction推奨を書いてください。(Concepts 実例3 + Fridayのgateを参照)

10. **(MCQ)** 「うまくいかない理由」節が、GPU上のweight-only quantizationに帰しているfailure modeはどれですか？(Concepts §「うまくいかない理由」を参照)
    - A) 常にmodelを大きくする
    - B) memoryは確実に縮めるが、fused kernelなしでは自動的には速くならない
    - C) KV cacheを消し去る
    - D) 実行にApple MPSを必要とする

## Answer key

1. **C)** INT4は4 bits = 0.5 bytes/paramなので、13B × 0.5 = 6.5 GBです。ruleは「4-bitなら十億paramsあたり約1 GB」、そして `bytes = params × (bits / 8)`。

2. **A)** `q = round(0.5 / 0.0039) = round(128.2) = 128`。scaleは `(max − min) / 255 = 1.0 / 255 ≈ 0.0039` です。

3. **Perplexityは流暢さの速いproxyであって、特定のjobのproxyではない。** quantizeされたmodelは、perplexityがほぼ同一のまま、named entityを見逃したり、壊れたJSONを出したり、billing ticketをclaimsにrouteしたりできます。ship判断にはtask eval（例: 30-ticket triage accuracy）を実行しなければなりません。

4. **B)** Q4_K_Mはtriage F1を~0.897に保ち（~1.5-pointの損失）、~3.5×少ないVRAMと~3.4×低いcost。Q2_Kの8-pointのF1低下（0.912 → 0.831）は相当な数のticketを静かにmisrouteするので、避けるべきzoneです。

5. **A)** `math.exp(total_loss / total_tokens)` を計算します。各noteのtokenにわたるexponentiateした平均cross-entropyで、note間でlossを平均するので、短いnoteも長いnoteも等しく寄与します。

6. **`LIVE_FP16 = (DEVICE in ("cuda", "mps"))`**: FP16はNVIDIAとApple Siliconで動きます。**`LIVE_QUANT = (DEVICE == "cuda")`**、bitsandbytesの8/4-bitにはCUDAのみが必要です。MPSではFP16だけがliveで動き、CPUでは両方が `False` になりfallback pathが走ります。

7. **B)** continuous batchingは新しいrequestをtoken-by-tokenで受け入れ、終わったものを即座にevictし、PagedAttentionの固定size KV pageがfragmentationを消すので、GPUはstragglerのidle時間を新しい仕事で埋め戻します。

8. **B)** どちらもOpenAI互換の `/v1/chat/completions` endpointを出します。notebookが変えるのは `base_url`（vLLMは :8000、Ollamaは :11434）とmodel名だけで、これが相互運用性のsuperpowerです。

9. **合格する答えはtradeとship/no-ship lineを述べます。** 例:「INT4をshipする。VRAMの25%でFP16 triage accuracyの96.7%（0.89 vs 0.92）を保ち、misfileするticketはこれです。」（数字はestimateではなく自分のrunから来なければなりません。）

10. **B)** weight-only quantはmemoryを確実に縮めますが、speedの勝利はfused kernel次第です。なければ、小さくはなるが速くはなりません。
