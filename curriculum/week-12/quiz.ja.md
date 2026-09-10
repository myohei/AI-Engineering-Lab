# Week 12: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 12 README](README.ja.md) · [演習](exercises.ja.md)

まず記憶だけで答えてから、Answer keyで確認してください。各問には、それがtestするsectionまたはcellが明記されているので、間違えたら何を読み直すべきかが正確に分かります。

## Questions（問題）

1. **(MCQ)** modelとharnessは同じものではありません。division of laborを正しく捉えている
   statementはどれですか？ *(Concepts「What a harness is」を参照)*
   - A) harnessはparameterを追加してmodelを賢くする。
   - B) modelはreasoningを供給し、harnessはagency（loop、tools、context、verifiers）を供給する。
   - C) harnessは単なるeditorであり、modelがすべての仕事をする。
   - D) modelはagencyを供給し、harnessはreasoningを供給する。

2. **(MCQ)** OpenCodeで作業しています。永続的なproject指示として自動的に読み込まれる
   fileはどれですか？ *(Concepts「Rules files」を参照)*
   - A) `CLAUDE.md`
   - B) `opencode.json`
   - C) `AGENTS.md`
   - D) `.cursor/rules/*.mdc`

3. **(Short answer)** Week-12の `SPEC.md` で、最も重要な一行は *refused tradeoff* です。
   specの他の部分がしていないことを、それは何をしますか？ *(Concepts「実例1」を参照)*

4. **(MCQ)** managed-context tableの「stays out」columnに属するのはどれですか？
   *(Concepts「Managed context」を参照)*
   - A) 失敗したtestの出力
   - B) `SPEC.md`
   - C) API key入りの `.env` file
   - D) 編集中の特定のsource file

5. **(Short answer)** notebookの最終cell（cell §5）は一つの数字をprintします。それは何と
   呼ばれ、正確に何を数えていますか？ *(notebook cell §1と§5を参照)*

6. **(MCQ)** specは *loopが照らし合わせて閉じる完了の定義* です。ということは、主に…
   *(Concepts「Planning vs execution」を参照)*
   - A) 未来の人間の読者向けのdocumentation
   - B) modelをより礼儀正しくするprompt
   - C) 「正しい」の意味の実行可能なstatementであり、verifierがcheckする
   - D) testを書くことの代替

7. **(Short answer、数字付き)** あるharness runは40,000 input tokenと10,000 output tokenを、
   $3.00/1M inputと$15.00/1M outputで使いました。計算を示し、合計costをdollarで
   答えてください。 *(Concepts「実例2」を参照)*

8. **(MCQ)** blast-radius ruleはautonomyを調整します… *(Concepts「Verifiers、SPEC.md、
   and blast radius」を参照)*
   - A) login時に、sessionごとに一度
   - B) actionごとに、間違えたときのdamageの大きさに基づいて
   - C) modelの好みの程度に基づいて
   - D) database書き込みにのみ適用し、file読み取りには決してしない

9. **(Short answer)** comparison worksheetのnumeric columnを二つ挙げ、それぞれが何を
   記録するかを述べてください。 *(notebook cell §3を参照)*

10. **(MCQ)** OpenRouterで、`:free` model variantの最も良い使い方は… *(Concepts
    「OpenRouterとcost管理」を参照)*
    - A) service-level保証付きのproduction throughput
    - B) 本番のthroughputに金を払う前に、plumbing（auth、config、prompt）をtestする
    - C) 自分のmodelのfine-tuning
    - D) harnessのpermission systemの代替

## Answer key

1. **B.** harnessはloop、tools、context管理、verifiersを追加します。modelはreasoning
   だけです。同じmodelで二つのharnessの結果が違うのは、この四つで違うからです。

2. **C.** OpenCodeは `AGENTS.md`（project + global）をauto-loadします。`CLAUDE.md` は
   Claude Code、`.cursor/rules/*.mdc` はCursor、`opencode.json` はconfigであり
   instructionsではありません。

3. **agentが曖昧さを当て推量で解決することを禁じます。** specの残りは *何を* build
   するかを言います。refused tradeoffは、agentが当て推量を *許されない* 場所を前もって
   宣言するただ一つの場所です。ここでは、missing/NaN shipmentのETAを決して捏造して
   はならない、ということです。

4. **C.** Secrets（`.env`、key）はwindowの外に出します。貼り付けられたものはlogされ、
   要約され、繰り返され得るからです。spec、失敗したtestの出力、特定のsource fileは
   *入ります*。

5. **harness-readiness score、0〜3のinteger。** `sum(1 for n in ('claude','opencode','dsh') if shutil.which(n))` で、installされてPATH上にある三つのcoding harnessの数です。

6. **C.** specはverifierが照らし合わせてcheckする、完了の実行可能な定義です。人間向けの
   documentationではなく、testを書くことの代用でもありません（specはtestを *明記* します）。

7. **$0.27。** Input: 40,000 × $3.00 / 1,000,000 = $0.12。Output: 10,000 × $15.00 / 1,000,000 =
   $0.15。Total = $0.12 + $0.15 = $0.27。

8. **B.** leashはactionごとです。scratch fileのreadはほぼタダで間違えられますが、
   production dataの書き込みは違う。同じagentでも、この二つには別のleashが与えられます。

9. **次のうち二つ:** `plan_quality_1to5`（planがあなたのspecにどれだけ近いか）、
   `tokens_used`、`cost_usd`、`tests_green_first_try`（testが初回で通ったか）、
   `diff_files_changed`、`code_quality_1to5`。

10. **B.** `:free` modelはzero-costですがrate制限がありavailabilityも低い。auth/config/
    promptが動くことを証明してから、本番の仕事にはpaid slugに切り替えます。
