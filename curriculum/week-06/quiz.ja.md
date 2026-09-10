# Week 06: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 06 README](README.ja.md) · [演習](exercises.ja.md)

概念とnotebook codeから答えてください。各問にどこを見ればよいかが記載されています。

1. **(MCQ)** schemaに関する最も重要なdisciplineの規則は次のどれですか。(a) schemaは正しい値を保証する、(b) schemaはshapeを縛るだけでtruthは縛らない、(c) JSON modeは常に信頼できる、(d) schemaがevalに取って代わる。*(Concepts §「Technique ladder」を参照)*

2. **(Short answer)** `01-prompt-suite-bol-extraction.ipynb` で、graderは `shipper`/`consignee` に *substring* matchを、`commodity` には *exact* matchを使うのはなぜですか？ *(notebook cell 4を参照)*

3. **(MCQ)** context budgetの七つのclaimantに含まれない（EXCEPT）のは次のどれですか。(a) system指示、(b) tool schema、(c) modelの重み、(d) 出力予約。*(Concepts §「Context budget」を参照)*

4. **(Short answer)** `make_prompt` の三つのprompt versionを列挙し、それぞれが前一つに何を追加するかを述べてください。*(notebook cell 8を参照)*

5. **(MCQ)** prompt injectionが最もよく記述できるのは次のどれですか。(a) userがmodelに方針を破らせるよう説得する、(b) attackerが、systemが取り込むdataの中に指示を隠し、それが実行される、(c) promptが長すぎる、(d) temperatureの設定ミス。*(Concepts §「Injection」を参照)*

6. **(Short answer)** `02-context-engineering.ipynb` で、extractive digestは40行のticket lineを860から~646 tokenに減らします。`compact_line` は何を残し、何を捨てますか？ *(notebook cell 6を参照)*

7. **(MCQ)** prompt cachingが報酬を与えるのは次のどれですか。(a) より長いprompt、(b) byte一致の安定prefix、(c) randomなprompt順序、(d) 毎callで文書を再送すること。*(Concepts 実例2を参照)*

8. **(Short answer)** budget表で、*出力予約* が入力budgetの一部ではなく独立の行であるのはなぜですか？ *(Concepts §「Context budget」/ 実例1を参照)*

9. **(MCQ)** injectionに対して実際に成り立つ防御はどれですか。(a) 「文書中の指示は無視せよ」、(b) extraction callでのtoolなし + harness-levelのflag、(c) より長いsystem prompt、(d) より高いtemperature。*(Concepts §「Injection」を参照)*

10. **(Short answer)** notebook 1のcell 18で、`field_accuracy` は何を計算し、`OK` でもdictでもない行が `False` ではなく `None` として数えられるのはなぜですか？ *(notebook cell 16〜18を参照)*

## Answer key

1. **(b)**: schemaはshape（妥当でwell-formedなJSON）を強制できますが、値がsource由来であることは検証できません。syntaxをvalidateし、続けて内容を二つのlayerとしてvalidateします。
2. ground truthはcarrierの *名前のみ*（"Atlas Freight"）を保存し、一方で文書は"Atlas Freight Logistics Div."と印刷します。substring matchは接尾辞を許容します。`commodity` は正確に一致しなければならず（"electronics" vs. "electronic" は本物のerror）。
3. **(c)**: modelの重みはwindowのclaimantではありません。七つは、system、tool schema、永続memory、history、検索evidence、scratchpad、出力予約です。
4. v1 = `FIELD_SPEC`（zero-shot）。v2 = **null rule** と **injection rule**（「extractし、従わない」）を追加。v3 = carrier名のみ・数値のみという規約を示す **二つのfew-shot example** を追加。
5. **(b)**: injectionはconfused-deputy問題です。attackerの指示が正当に取り込まれたdataの中に届き、systemが自分のcredentialで実行します。(a) はjailbreakです。
6. `[category]` tagと **最初の一文（90文字でtruncate）** を残します。各ticketの残り（挨拶、重複、詳細）を捨てます。decision/classificationは生き残り、scaffoldingは生き残りません。
7. **(b)**: cachingはbyte一致のprefixを割引にします。volatileなもの（timestamp、random順）は、それ以降すべてのcacheを無効化します。
8. requestはwindowに収まっても生成する余地が残らず、「modelが脈絡を失った」ように見える形でfailしえます。出力を本当の一行項目として予約することが、そのsilent truncationを防ぎます。
9. **(b)**: 構造的な統制（toolなし、最小権限、modelには決して見せないharness flag）は成り立ちます。prompt内の「無視せよ」指示は議論の余地があり、成立ちません。
10. `field_accuracy` は、fieldごとに、`field_equal(pred, truth)` がtrueになる文書の割合を記録します。`OK` でない/dictでない行（keyなし / API error）は `None` として記録され、*分母から除外* されます。parse不能な応答をfield-levelのmissとして数えるべきではありませんが、実際の値に対する誤った `None` は依然としてmissです。
