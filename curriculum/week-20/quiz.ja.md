# Week 20: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 20 README](README.ja.md) · [演習](exercises.ja.md)

1. **MCQ**: Bedrock vs SageMakerの区別を一行で表すのはどれですか？ *(Concepts §Bedrock vs SageMakerを参照)*
   - A) Bedrock = modelを消費。SageMaker = modelを所有
   - B) Bedrock = train。SageMaker = APIsをcall
   - C) 同じserviceである
   - D) BedrockにはGPU clusterが必要

2. **MCQ**: Converse APIが三cloudの中で最もcleanとされる理由は… *(Concepts §Converse APIを参照)*
   - A) 画像をsupportする唯一のAPIだから
   - B) 一つのprovider-neutralなmessage/tool-calling formatにより、`modelId`をswapして他は何も変えないで済むから
   - C) 無料だから
   - D) modelを自動fine-tuneするから

3. **MCQ**: Bedrockでの`AccessDeniedException`は、通常何を意味しますか？ *(Concepts §How it breaksを参照)*
   - A) Pythonが古い
   - B) Model accessでmodelを有効化していないか、IAM policyにactionがない
   - C) regionが間違っている
   - D) model IDが長すぎる

4. **Short answer**: notebook 01のRAG sectionが計算する**二つの**metricは何で、それぞれ何を意味しますか？ *(notebook 01 cell 9〜11を参照)*

5. **MCQ**: `anthropic.claude-3-5-sonnet-20241022-v2:0`のようなBedrock model IDsが日付付きsuffixを持つ理由は… *(Concepts §Model catalogを参照)*
   - A) ランダムだから
   - B) modelは頻繁に置き換えられるので、暗記せずconsoleから現在のIDをcopyするため
   - C) 価格をencodeしているから
   - D) regionをencodeしているから

6. **MCQ**: 名前、住所、tracking識別子をmaskするGuardrail filterはどれですか？ *(Concepts §Guardrails表を参照)*
   - A) Denied topics
   - B) Content filters
   - C) PII redaction
   - D) Custom word filters

7. **Short answer**: notebook 02のdry-run `local_guardrail`で、promptが`GUARDRAIL_INTERVENED`を返す二つの条件は何ですか？ *(notebook 02 cell 6を参照)*

8. **MCQ**: Provisioned Throughputがlab週に悪い考えな理由は… *(Concepts §Pricingを参照)*
   - A) pay-per-tokenのみだから
   - B) model unitを時間あたり予約し、使っても使わなくても課金されるから
   - C) credit cardが必要だから
   - D) Novaでしか動かないから

9. **Short answer**: Week 20のportfolio deliverable（三cloud matrix）はすべてのcellに何を要求し、それがなぜblog postではなくprocurement decisionにするのですか？ *(Concepts §The problem / How it breaksを参照)*

10. **MCQ**: notebook 02のdry-runで、最後のcellがprintするのは… *(notebook 02 cell 11を参照)*
    - A) `RECALL: 1.000 GROUNDEDNESS: 1.000`
    - B) `BLOCKED: 3 ALLOWED: 2`
    - C) `EVAL_SCORE: 1.000`
    - D) `BLOCKED: 2 ALLOWED: 3`

## Answer key

1. **A**: Bedrockはmanaged foundation-model層（消費）。SageMaker AIはbuild/train/deploy-your-own層（所有）です。
2. **B**: Converse APIの、Claude/Nova/Llama/Mistralにわたる単一formatにより、`modelId`をswapするだけで他は変わりません。
3. **B**: `AccessDeniedException`は、modelがModel accessで有効になっていないか、IAM policyにactionがないことを意味します。codeに触る前に両方を確認。
4. **Recall**: retrievalが正しいsource documentをsurfaceした質問の割合。**groundedness**: ground-truthのfactを含むanswerの割合（citation付きで、hallucinationでない）。どちらも質問set上の割合です。
5. **B**: 日付付きsuffixは頻繁に置き換えられます。consoleから現在のIDをcopyし、決して暗記しない。
6. **C**: PII redactionが名前、住所、tracking識別子をmaskします。
7. promptがinsult語（`idiot`、`garbage`、`stupid`、`useless`）を含む場合、**または**freight keyword（`shipment`、`refund`、`track`、`freight`、`delivery`、`policy`、`pallet`、`bill`）を一つも含まない場合。
8. **B**: Provisioned Throughputはmodel unitを時間あたり予約し、idleの間もmeterします。labにはon-demandが正しい選択です。
9. **すべてのcellが、Week 18〜20の測定値（同じgolden set、seed、metric）までtraceできなければならない**こと。per-cell evidenceがあればmatrixはrecommendationを支えます。なければただの意見であり、だからblog postではなくprocurement decisionなのです。
10. **B**: `BLOCKED: 3 ALLOWED: 2`（三つのblockされたprompt、insult、cake recipe、pirate joke、と二つの許可されたfreight prompt）。
