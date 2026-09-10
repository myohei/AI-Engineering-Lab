# Week 08: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 08 README](README.ja.md) · [演習](exercises.ja.md)

概念とnotebook codeから答えてください。各問にどこを見ればよいかが記載されています。

1. **(MCQ)** 「Open weights」が意味するのは次のどれですか。(a) modelがOSI open-sourceである、(b) training済みのweightが公開されており、実行/quantize/fine-tuneできる、(c) licenseが存在しない、(d) あらゆる法的制限から自由である。*(Concepts §「Open vs. closed」を参照)*

2. **(Short answer)** 商用のZoroLogistics shipping toolにとって、Apache-2.0/MITが安全なlicense defaultであるのはなぜですか？また、LlamaやGemmaのmodelをshipする前に何をしなければなりませんか？*(Conceptsの表 / KB §1を参照)*

3. **(MCQ)** 4-bit（Q4）の7B modelの、weightのみのmemoryはおよそ次のどれですか。(a) 14 GB、(b) 7 GB、(c) 3.5 GB、(d) 1 GB。*(notebook cell 2 / Conceptsの表を参照)*

4. **(Short answer)** `02-vram-sizing-and-model-selection.ipynb` で、`kv_cache_gb` が使うformulaを書き、32 layers、32 heads、head_dim 128、seq_len 4096、2 bytes/paramについて計算してください。*(notebook cell 6を参照)*

5. **(MCQ)** `-ngl`（GPUにoffloadするlayer数）が0のとき、modelはどうなっていますか。(a) 完全にGPU上にある、(b) 静かにCPUで動いている、(c) MLXを使っている、(d) 4-bitにquantizeされている。*(Concepts §「GPU setup」を参照)*

6. **(Short answer)** `01-local-model-playground.ipynb` で、Modelfileは何を設定し、`--format json` は「JSONで答えよ」というpromptと何が違いますか？*(notebook cell 7を参照)*

7. **(MCQ)** Apple Siliconで通常最速のruntimeはどれで、その理由は何ですか。(a) llama.cpp、CPUのみ、(b) MLX、unified memory、(c) Ollama、より小さい、(d) LM Studio、GUI。*(Concepts §「Local stack」を参照)*

8. **(Short answer)** notebook 2のcell 10で、pickerは8 GB Windows laptopには *3B* modelを、16 GB MacBookには *8B* modelを推奨します。なぜですか？`0.8` comfort factorは何をしていますか？*(notebook cell 8と10を参照)*

9. **(MCQ)** 16 GB boxでpickerの `task` を `"triage"` から `"reasoning"` に変えると `None` が返ります。その理由は次のどれですか。(a) reasoning modelは存在しない、(b) catalog内で最小のreasoning-class modelがQ4で~12.8 GB budgetより多く必要とする、(c) licenseがそれを禁じている、(d) OS reserveが小さすぎる。*(Concepts 実例2を参照)*

10. **(Short answer)** 「あなたのlocal modelはどれくらい速い？」と聞かれたとき、報告すべき二つの数値は何ですか？また、userが感じるのはどちらですか？*(Concepts §「GPU setup」 / KB §10を参照)*

## Answer key

1. **(b)**: openな *weight* は公開されます。しかし、合法的に何をしてよいかを決めるのはlicense（OSI open-sourceではないかもしれない）です。(a) はdistributionとlicensingを混同しています。
2. Apache-2.0/MITはpermissiveで、attribution/noticeのみで商用利用を認めます。LlamaとGemmaは商用利用可能ですが、記録すべき条項を伴います（例: ~700M-MAU scale cap、prohibited-use list）。だからshipの前にcompliance fileにlicenseと条項を記録しなければなりません。
3. **(c)**: weightは `7B × 0.5 bytes/param ≈ 3.5 GB`。
4. `2 × layers × heads × head_dim × seq_len × bytes_per_param` → `2 × 32 × 32 × 128 × 4096 × 2 = 2,147,483,648 bytes ≈ 2.15 GB`。
5. **(b)**: offloadされたlayerがないので、llama.cppはCPUで動きます。「CUDAをinstallした」ままGPUが一つも仕事をしていない、ということが起こえます。
6. Modelfileは `FROM <model>`、triage用の `SYSTEM` prompt、`PARAMETER temperature 0` を設定します。`--format json` はvalidなJSONを強制する *generation時の制約*（JSON mode）ですが、「JSONで答えよ」というpromptはmodelが無視できるただの要求です。
7. **(b)**: MLXはAppleのunified memoryの上で動き（host↔device間copyなし）、M-series chipではしばしば最速のlocal pathです。
8. Pickerは `total_footprint` が `available_gb × 0.8` に収まる最大のmodelを返します（comfort factorはOS reserveの他に20%をheadroomとして確保）。8 GB × 0.8 = 6.4 GBにはQ4の3B（~4.7 GB）しか収まらず、16 GB × 0.8 = 12.8 GBならQ4の8B（~8.6 GB）が収まります。
9. **(b)**: `MIN_PARAMS["reasoning"] = 13.0` は3B〜8Bのmodelを除外し、Q4の14Bは合計~14 GBで12.8 GB budgetを超えるため、どのoptionも収まりません。
10. **Prefill速度**（prompt tokens/sec）と **decode速度**（generation tokens/sec）。userが感じるのは **decode**、新しいtokenが流れ出るrateです。
