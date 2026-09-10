# Week 18: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 18 README](README.ja.md) · [演習](exercises.ja.md)

1. **MCQ**: Foundryのhierarchyで、**hub**が所有するresourceはどれですか？ *(Concepts §Model catalog / hub-projectを参照)*
   - A) Deployment、eval、trace
   - B) Azure OpenAI instance、AI Search index、storage、key vault、そしてnetwork boundary
   - C) agent定義のみ
   - D) 何も所有しない。projectがすべてを所有する

2. **MCQ**: Azureに対してOpenAI SDKを呼ぶとき、`model=`引数はあなたの… *(notebook 01 cell 3を参照)*
   - A) 生のmodel ID。例えば`gpt-4.1`
   - B) deploy時にあなたが選んだdeployment name
   - C) region名
   - D) API version文字列

3. **MCQ**: 使っても使わなくても課金されるdeployment optionはどれですか？ *(Concepts §Deployment tableを参照)*
   - A) Serverless endpoint (MaaS)
   - B) Provisioned throughput (PTU)
   - C) Pay-per-token on-demand
   - D) どれでもない

4. **Short answer**: notebook 01で、`field_matches`がintegerとして（文字列一致ではなく数値比較で）比較するBoL fieldは**どの二つ**ですか？ *(notebook 01 cell 12を参照)*

5. **MCQ**: 暴走agentがbudgetを使い切れないようにする、*月次spend*をcapするのに正しいAI Gateway controlはどれですか？ *(Concepts §AI Gatewayを参照)*
   - A) Token-rate limit
   - B) Semantic cache
   - C) Token-usage quota / cost cap
   - D) Model routing

6. **MCQ**: notebook 02のdry-runで、fixの*前*に失敗するgolden questionはどれで、なぜですか？ *(notebook 02 cell 10を参照)*
   - A) Q1（refund）。promptが間違っているから
   - B) Q4（customs）。`KEYWORD_DOCS`に`customs` → `POL-004`の対応がないから
   - C) Q2（address）。`$85`がmisspellだから
   - D) Q3（dangerous goods）。docに`UN number`がないから

7. **Short answer**: Week 6の`EXTRACT_PROMPT`がmodelにJSONとして返させる十fieldのうち、少なくとも**五つ**を挙げてください。 *(notebook 01 cell 4を参照)*

8. **MCQ**: Foundry codeに対する推奨されるproduction認証（keyの代わり）はどれですか？ *(Concepts §How it breaksを参照)*
   - A) HardcodeされたAPI key
   - B) `DefaultAzureCredential` / managed identity経由のEntra ID
   - C) 共有のteam password
   - D) 認証なし

9. **Short answer**: notebookのplaceholder price（$0.15/1M input、$0.60/1M output）で、150 input tokenと120 output tokenを使うBoL抽出一回のcostを計算してください。計算過程を示すこと。 *(notebook 01 cell 15を参照)*

10. **MCQ**: 「fixのないtraceはbug reportである」の意味は… *(Concepts §Evaluation & tracingを参照)*
    - A) 失敗したtraceは削除すべき
    - B) scoreが変わらなくても、traceを読めば十分
    - C) eval loopが完了するのは、traceを読み、最悪の失敗をfixし、before/after scoreを示したときだけ
    - D) traceはLLM-as-judge run専用

## Answer key

1. **B**: hubが共有enterprise resourceを所有し、projectがteamのdeployment、eval、traceを持ちます。この分離こそgovernanceの要点です。
2. **B**: Azureでは`model=`は生のmodel IDではなくあなたの*deployment name*です。Week 18のclassic gotchaです。
3. **B**: PTUはcapacityを予約し、使用に関係なく課金します。serverlessはpay-per-tokenです。
4. **`quantity`と`gross_weight_kg`**: どちらも`int(float(pred)) == int(float(truth))`で比較されます。
5. **C**: token-usage quota / cost capが累積spendを抑えます。rate limitはburst rateを絞るだけです。
6. **B**: `KEYWORD_DOCS`は意図的に`customs`/`storage`を省くので、Q4（customs hold fee）は対応するdocがなく、fixが`customs → POL-004`を追加するまで失敗します。
7. 次のうち五つ: `shipper`、`consignee`、`port_of_loading`、`port_of_discharge`、`commodity`、`quantity`、`gross_weight_kg`、`declared_value_usd`、`freight_terms`、`date_of_issue`。
8. **B**: productionのguidanceは`DefaultAzureCredential`経由のmanaged identity / service principalです。keyはlegacyなquick-startの道です。
9. Input 150 × $0.15/1M = $0.0000225。output 120 × $0.60/1M = $0.0000720。**合計 ≈ $0.0000945**（一セントの十分の一以下）。
10. **C**: loopが閉じるのは、traceがbefore/after付きの数字へつながるときだけです。診断のないscoreも、fixのない診断も不完全です。
