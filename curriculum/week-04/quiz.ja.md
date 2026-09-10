# Week 04: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 04 README](README.ja.md) · [演習](exercises.ja.md)

十問すべてに答えてから、Answer keyで確認してください。*(Concepts §Xを参照)* はREADMEのsubsection、*(notebook cell Yを参照)* は `01-pytorch-tensors-and-autograd.ipynb` または `02-mlp-eta-train-and-eval.ipynb` のcellを示します。

1. **Multiple choice。** autograd cellで、`y = x ** 2` 、`x = torch.tensor(3.0, requires_grad=True)`、`y.backward()` とします。`x.grad` は何で、なぜですか？ *(Concepts §2、autograd cellを参照)*
   a. 3.0。`x` をcopyするから
   b. 6.0。`df/dx = 2x` で `2 × 3 = 6` だから
   c. 9.0。`3² = 9` だから
   d. 0.0。`x` はleafだから

2. **Short answer。** training loopの五行を順に書き、各行が何のためかを述べてください。 *(Concepts §4を参照)*

3. **Multiple choice。** validation/testで評価する前に `model.eval()`（と `torch.no_grad()`）を呼ばなければならないのはなぜですか？ *(Concepts §7、「うまくいかない理由」を参照)*
   a. modelをGPUに移動するため
   b. **dropoutをoff** にしgradient trackingをskipして、test予測をdeterministicで安くするため
   c. optimizerのstateをresetするため
   d. DataLoaderに再seedするため

4. **Short answer。** 今週のETA taskで、modelが最適化する **loss** とmodel cardが報告する **metric** の違いは何ですか？ *(Concepts §4を参照)*

5. **Multiple choice。** ETA MLPは23個の入力featureを持ちます。その23はどこから来ていますか？ *(notebook「feature table」cell、Concepts §5を参照)*
   a. 23個のraw shipment column
   b. 7 numeric + 4 one-hot weather + 12 one-hot commodity = 23
   c. 20 carrier + 3つの日付
   d. 23個のrandom embedding

6. **Short answer。** このdatasetでは、neural MLPのtest MAEは≈ 4.99 h、gradient-boosting baselineは≈ 4.87 hです。deltaはいくつで、それを（隠さずに）報告することが今週の要点であるのはなぜですか？ *(Concepts §7、worked example 3を参照)*

7. **Multiple choice。** learning curveで **overfitting** を示す症状はどれですか？ *(Concepts §5を参照)*
   a. trainもvalも高くて平坦
   b. trainが低く、valが高く、gapがepochとともに拡大
   c. 両curveが一緒に減少して同じ値に収束
   d. valがtrainより低い

8. **Short answer。** `DataLoader(train_ds, batch_size=256, shuffle=True)` で、訓練には `shuffle=True` が正しく、validation/testでは誤りなのはなぜですか？ *(notebook「DataLoader」cell、Concepts §5を参照)*

9. **Multiple choice。** `AdamW` の `weight_decay` 引数は何をしますか？ *(Concepts §6を参照)*
   a. 訓練中にactivationの一部をrandomにゼロにする
   b. lossに二乗重みpenaltyを追加し、重みをゼロへ向かわせる
   c. 毎epoch learning rateを減衰させる
   d. batch sizeを時間とともに縮める

10. **Short answer。** `EtaMLP` で使われている二つのregularizerの名を挙げ、それぞれが減らすべき症状を述べてください。 *(Concepts §6、model cellを参照)*

## Answer key

1. **b。** `f(x) = x²` の導関数は `2x` です。`x = 3` ではそれは `6.0` です。autogradはcomputation graphを逆向きにたどり、chain ruleのgradientで `x.grad` を埋めます。notebookはそれが6.0に等しいことをassertします。

2. **`opt.zero_grad()`（前stepのgradientをclear）→ `loss = loss_fn(model(xb), yb)`（forward + error測定）→ `loss.backward()`（autogradが `.grad` を埋める）→ `opt.step()`（optimizerが重みを更新）**、これを `for xb, yb in loader` でloopします。forward、loss、backward、stepがengineのすべてです。

3. **b。** `model.eval()` は訓練中のみの挙動（dropout）を無効にし、`torch.no_grad()` はgradientの記帳を無効にします。その結果、予測は完全なnetworkをdeterministicに使い、memoryを無駄にしません。忘れるとdropoutが有効のままになり、test metricが汚染されます。

4. **lossはMSEです**。滑らかで微分可能で、optimizerが最小化します。**報告されるmetricは時間単位のMAE** で、微分対象ではないけれど、運用者に解釈できます（「平均でX時間外れる」）。設計上、異なるものです。滑らかなものを最適化し、重要なものを報告します。

5. **b。** `ColumnTransformer` は7つのnumeric columnを標準化し、`weather_severity`（4 category）と `commodity`（12 category）をone-hot encodeし、7 + 4 + 12 = 23のfeatureを生み出します。

6. **delta ≈ +0.116 h**：MLPは平均で約7分 *悪く*、事実上の互角です。負けを正直に報告するのがdisciplineです。modelは、自分の訓練lossではなく、baselineに対してdeltaを明示して評価されます。Week 4の要点は、都合よく選んだ勝利ではなく、evalとerror analysisの習慣です。

7. **b。** overfittingは、train lossが低いままvalidation lossが高く、gapが拡大する形で現れます。modelは訓練標本を暗記しています。両方高く平坦はunderfitting、一緒に収束はhealthyです。

8. **訓練batchのshuffle** は連続するgradient stepの相関をなくし、generalizationを助けます。しかしvalidation/testの順序は保たれなければならず、そうすればper-epoch lossが比較可能になり、（時系列dataでは）時系列順が壊されません。`shuffle=True` を渡されるのは訓練loaderだけです。

9. **b。** `weight_decay` は、重みの二乗に比例するpenaltyをlossに追加し、重みをゼロへ引き寄せて、より滑らかでnoiseにfitしにくい関数にします。`AdamW` ではAdamのadaptive stepからdecoupleされています。

10. **Dropout**（訓練中のみactivationをrandomにゼロにする）と **weight decay**（二乗重みpenalty）です。どちらも **overfitting**、すなわち訓練lossがvalidation lossを大きく下回りgapが拡大する症状を減らします。
