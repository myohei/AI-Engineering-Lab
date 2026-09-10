# Week 19: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 19 README](README.ja.md) · [演習](exercises.ja.md)

1. **MCQ**: Google AI StudioとVertex AIは、ほぼ同じGemini modelを公開しています。*機密data*にとって最も重要な違いは何ですか？ *(Concepts §AI Studio vs Vertexを参照)*
   - A) Vertexのmodelのほうが速い
   - B) AI Studioのfree tierは、defaultであなたのdataをGoogle製品の改善に使う可能性がある
   - C) Vertexにはquotaがない
   - D) AI Studioにはcloud projectが必要

2. **MCQ**: `google-genai` SDKで、同じclientをAI StudioからVertexに切り替えるのは何ですか？ *(notebook 02 cell 8を参照)*
   - A) model名を変えること
   - B) `vertexai=True`に加えて`project`/`location`を設定すること
   - C) 別のimportを使うこと
   - D) `response_mime_type`を設定すること

3. **MCQ**: 大volume・単純な抽出に最も*安い* Gemini rungはどれですか？ *(Concepts §Gemini ladderを参照)*
   - A) `gemini-2.5-pro`
   - B) `gemini-2.5-flash`
   - C) `gemini-2.5-flash-lite`
   - D) "Thinking" variant

4. **Short answer**: notebook 01で、pipelineはGeminiを呼ぶ前に、なぜ各BoLの**text**をそのままpromptに貼るのではなく、Pillowで**PNG**にrenderするのですか？ *(notebook 01 cell 3を参照)*

5. **MCQ**: Vertexでbatch途中に出る`429` errorは、ほぼ常に… *(Concepts §How it breaksを参照)*
   - A) 構文のbug
   - B) quota天井。regionごと/modelごとのquotaを引き上げるか、callを分散する
   - C) 間違ったAPI key
   - D) 存在しないmodel

6. **MCQ**: Googleの三つのagent層のうち、support agentをrebuildするのに使う**code-firstでopen-source**なframeworkはどれですか？ *(Concepts §Agent stackを参照)*
   - A) Agent Builder
   - B) Agent Engine
   - C) ADK
   - D) Colab Enterprise

7. **Short answer**: OCR promptがJSONとして返す十個のBoL fieldのうち、少なくとも**五つ**を挙げてください。 *(notebook 01 cell 6を参照)*

8. **MCQ**: BigQuery MLの`ML.GENERATE_TEXT`を使うと… *(Concepts §BigQuery MLを参照)*
   - A) SQLでtransformerを一からtrainできる
   - B) SQLから出ずに、BigQueryの*中から*Geminiを生成/分類に呼び出せる
   - C) Vertex IAMを置き換えられる
   - D) imageをrenderできる

9. **Short answer**: notebookのplaceholder price（$0.000315/image、$0.30/1M input、$2.50/1M output）で、image一枚、input 150 token、output 120 tokenのBoL文書**一枚**のcostを計算してください。計算過程を示すこと。 *(notebook 01 cell 11を参照)*

10. **MCQ**: 「per-fieldの数字のないpipelineは、JSON blobのscreenshotにすぎない」の意味は… *(Concepts §How it breaksを参照)*
    - A) JSON出力は決して正しくない
    - B) きれいなblobを眺めるだけでなく、ground truthに対してfieldごとにaccuracyを測らなければならない
    - C) screenshotがdeliverable
    - D) 合計accuracyだけが重要で、per-fieldは任意

## Answer key

1. **B**: AI Studioのfree tierは、defaultでdataをGoogle製品の改善に使う可能性があります。governedなdataが行く場所はVertexです。分離する習慣がdeliverableです。
2. **B**: `genai.Client(vertexai=True, project=..., location=...)`が、認証と課金をADC付きのVertexに切り替えます。
3. **C**: `flash-lite`が、大volume・単純なtaskに最も安いrungです。accuracy barをクリアする最も安いmodelを選びましょう。
4. **Geminiにpromptのtextを読ませるのではなく*vision*をexerciseさせるため**です。imageにrenderすることで、pipelineがend-to-end（image → JSON）のままになり、GoogleのedgeであるOCR能力をtestできます。
5. **B**: `429`はcode bugではなくquota問題です。batchの前にregionごと/modelごとのquotaを確認し、引き上げてください。
6. **C**: ADKがcode-firstのopen-source frameworkです。Agent Builderはlow-code、Agent Engineはmanaged runtimeです。
7. 次のうち五つ: `shipper`、`consignee`、`port_of_loading`、`port_of_discharge`、`commodity`、`quantity`、`gross_weight_kg`、`declared_value_usd`、`freight_terms`、`date_of_issue`。
8. **B**: `ML.GENERATE_TEXT`は、BigQuery SQLの中からremoteのGemini modelを呼び出します。「warehouseから出ないAI」です。
9. Image $0.000315 + input 150 × $0.30/1M = $0.000045 + output 120 × $2.50/1M = $0.00030 → **合計 ≈ $0.00066**。
10. **B**: 正しそうに見えるJSON blobでもconsigneeが間違っていることがあります。ground truthに対するper-field accuracyだけが正直なmetricです。
