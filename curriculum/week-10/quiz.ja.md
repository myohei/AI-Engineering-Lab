# Week 10: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 10 README](README.ja.md) · [演習](exercises.ja.md)

まず自分で答えてから、answer keyで確認してください。各問に答えのある場所が記載されているので、間違えたsectionやcellを読み返せます。

## 設問

1. **(MCQ)** Ngのselection orderは何で、fine-tuningはどこに位置しますか？(Concepts §「最後のlever」を参照)
   - A) Fine-tune → RAG → prompt → agentic
   - B) Prompt（eval付き） → RAG → agentic → fine-tune last
   - C) RAG → fine-tune → prompt → agentic
   - D) weightは常にcontextに勝つので、fine-tune first

2. **(MCQ)** shapeが `(in=1536, out=1536)`、rank `r=16` のLoRA moduleに、LoRAはいくつのtrainable parameterを追加しますか？(Concepts 実例1を参照)
   - A) 1536
   - B) 49,152
   - C) 700,416
   - D) 1.54 billion

3. **(Short answer)** LoRAの実例で、trainable parameterの合計は~1.54B中の~0.70M、約0.05%でした。この小さな割合がbudgetにとって重要なのはなぜですか？(Concepts 実例1を参照)

4. **(MCQ)** `notebooks/01-sft-dataset-and-lora-training.ipynb` で、各extraction exampleのassistant turnは何ですか？(notebook cell 6を参照)
   - A) 一語のcategory
   - B) `bol["fields"]` のground-truth JSON
   - C) 空文字列
   - D) system prompt

5. **(Short answer)** knowledge baseはなぜ「数百のcleanで多様なon-taskなexampleが、数万のnoisyなexampleに勝る」と言っていますか？(Concepts §「SFT: imitation learning」を参照)

6. **(MCQ)** DPOを古典的RLHFから区別するものは何ですか？(Concepts §「SFT → DPO → RLVR」を参照)
   - A) DPOには別途trainingしたreward modelが必要
   - B) DPOは `(prompt, chosen, rejected)` pair上のsupervised objectiveにpreference signalを直接foldする
   - C) DPOにはunit testのようなverifiable rewardが必要
   - D) DPOはmodel全体をfreezeして何もtrainしない

7. **(MCQ)** `notebooks/02-dpo-and-before-after-evals.ipynb` で、「forgetting check」とは何ですか？(notebook cell 6を参照)
   - A) modelがすでに知っているはずの5つのgeneric questionのheld-out setを、前後で採点する
   - B) adapterがまだVRAMに収まるかのtest
   - C) loss curveが下がったかのcheck
   - D) 二つの異なるbase modelの比較

8. **(Short answer)** net gainを計算してください: before = {extraction 0.60、triage 0.72、generic 0.95}、after = {extraction 0.88、triage 0.91、generic 0.93}。`net = extraction_delta + triage_delta − forgetting_cost` はいくつで、deployしますか？(Concepts 実例2を参照)

9. **(MCQ)** あなたのfine-tuneは新task evalを上げましたが、generic checkが0.95から0.80に下がりました。「うまくいかない理由」節に従うと、正しいactionはどれですか？(Concepts §「うまくいかない理由」を参照)
   - A) Shipする。specialist gainこそが大事
   - B) Deployしない。rank/alphaを下げるか、general dataの一部を戻して加える
   - C) Epochを増やす
   - D) Generic checkを無視する

10. **(MCQ)** 変わるfact（例: 昨四半期の価格）をweightに保存してはいけないのはなぜですか？(Concepts §「Fine-tuningが報われるとき」を参照)
    - A) Weightは数値を保持できない
    - B) 揮発性のfactにはretrieveした知識が間違っている。memorizeではなくretrieveする
    - C) Fine-tuningは常に古いfactを削除する
    - D) Factは小さすぎて重要ではない

## Answer key

1. **B)** 順序はmanaged-API prototype → eval付きprompt/context → RAG → agentic → fine-tune last。fine-tuningは最後の、最も高価で、最も元に戻しにくいleverです。

2. **B)** LoRAはmoduleごとに `r × (in + out) = 16 × (1536 + 1536) = 49,152` を追加します。これは一つのattention projectionで、`q/k/v/o` 全体では `4 × 49,152 = 196,608` です。

3. **LoRAはほとんど何もtrainしないので、adapterは数MBで済み、fine-tuneはfull trainingのmemoryの一部で済みます。** QLoRAはbaseを4-bitにするので、1.5B（あるいは7〜8B）のrunが、datacenterではなくfree Colab T4や16 GB laptopに収まります。

4. **B)** assistant turnは `json.dumps(bol["fields"], sort_keys=True)`、つまりmodelがimitateすることを学ぶground-truthの構造化field（label）です。

5. **小さいmodelは、dataで支配的なpatternを何であれ内面化します。** exampleの大半が的外れか矛盾していれば、それこそを教えることになります。*behavior* のcoverage（多様性、edge case）が行数より重要です。

6. **B)** DPOは `(prompt, chosen, rejected)` pair上のsupervised風objectiveにpreference signalを直接foldします。RLHFのreward model + PPO loopより単純で安定です。（verifiable rewardを使うのはDPOではなくRLVRです。）

7. **A)** forgetting checkは、前後で採点される5つのgeneric question（`GENERIC_QA`）です。adapterがgeneral competenceをun-teachすることをcatchします。

8. **net = (0.88−0.60) + (0.91−0.72) − (0.95−0.93) = 0.28 + 0.19 − 0.02 = +0.45。** 正なので、specialist gainが小さなgeneric regressionを稼いだ → deployします。（forgetting costがgainを上回るなら、答えはdon't deployです。）

9. **B)** これほど大きなgeneric低下はcatastrophic forgettingを意味します。Shipしません。learning rateを下げる、general dataの小さな割合を戻して加える、またはrank/alphaを下げる。epochを増やすことは決してしません。

10. **B)** 変わるfactにとってweightは間違った場所です。来四半期にはmodelはすでに間違っているでしょう。新しいknowledgeはRAGの仕事です。retrieveし、fine-tuningは *behavior*（style、format、vocabulary）に使ってください。
