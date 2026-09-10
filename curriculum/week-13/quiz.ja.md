# Week 13: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 13 README](README.ja.md) · [演習](exercises.ja.md)

まず記憶だけで答えてから、Answer keyで確認してください。各問には対象のsectionまたはcellが明記されているので、間違えたら何を読み直すべきかが分かります。

## Questions（問題）

1. **(MCQ)** 分scaleのcadenceで回り、verifierに対して閉じるのはどのloopですか？
   *(Concepts「The three loops」を参照)*
   - A) External feedback
   - B) Developer feedback
   - C) Agentic coding
   - D) The configuration-management loop

2. **(MCQ)** unit checkとmini evalは二つの *異なる* verifier層です。なぜなら…
   *(Concepts「The verifier has layers」を参照)*
   - A) unit testは統計的でevalはbinaryだから
   - B) evalは多数のexampleにわたるaccuracyをrateとして測り、手書きcheckがmissしたclass全体を捕まえるから
   - C) evalのほうがunit testより実行が安いから
   - D) unit testがevalの必要性をなくすから

3. **(Short answer)** notebookの最終cellがverifier pass rateの計算に使う式を正確に書いて
   ください。 *(notebook cell §7を参照)*

4. **(MCQ)** spec-driven developmentでは、feedbackがgapを見つけたとき、fixはどこへ入りますか？
   *(Concepts「SPEC.md patterns」を参照)*
   - A) まずcodeへ。時間があればその後specへ
   - B) まずspecへ、次にcode、次にtest/eval caseへ
   - C) agentへのchat messageへ。そして失われる
   - D) eval setだけへ

5. **(Short answer)** Support Bot classifierが区別する六つのcategoryをすべて挙げてください。
   *(notebook cell §1を参照)*

6. **(MCQ)** blast-radius ruleはactionごとにautonomyを調整します。最も厳しいleashが必要な
   actionはどれですか？ *(Concepts「Blast-radius rules」を参照)*
   - A) scratch fileを読むこと
   - B) branch上でrepoを編集すること
   - C) production dataに書き込むこと
   - D) unit testを実行すること

7. **(Short answer)** `classify_ticket('hello')` は何を返しますか？そしてなぜ？
   *(notebook cell §1と `_check_unknown` unit checkを参照)*

8. **(MCQ)** `PreToolUse` hookの存在理由は… *(Concepts「Harness primitives」を参照)*
   - A) 編集後にdiffを要約すること
   - B) toolが走る *前に* policyを強制またはblockすること（例: `data/raw/` への書き込みを拒否）
   - C) skillをon-demandでloadすること
   - D) subagentをspawnすること

9. **(Short answer、数字付き)** 三つのagentic cycleで合計12,000 input tokenと3,000 output
   tokenを、$3.00/1M inputと$15.00/1M outputで使いました。計算を示し、合計costをdollarで
   答えてください。 *(Concepts「実例1」を参照)*

10. **(MCQ)** external loopのbug reportを永続的な変更に変える正しい方法は…
    *(Concepts「実例2」を参照)*
    - A) codeを直して先へ進む
    - B) fileし、それからspec行と新しいeval caseを追加して、静かにregressできないようにする
    - C) userにそのinputの使用をやめてもらう
    - D) loop logに記録して他には何もしない

## Answer key

1. **C.** agentic codingは数分で回ります。書く → testする → 失敗を読む → 直す、を
   verifierがpassするまで。developer feedbackは数十分〜数時間、external feedbackは
   数時間〜数週間です。

2. **B.** 6つのunit checkはbinaryで手書きです。60-ticket evalはaccuracyをrateとして
   報告し、手書きcheckが決して名指ししなかったclass全体（例: customs）をsurface化
   できます。

3. **`verifier_pass_rate = (unit_passed + eval_correct) / (unit_total + eval_total)`**。
   `round(verifier_pass_rate, 3)` としてprintされます。すなわち `(unit checks passed + eval correct) / (unit
   checks + eval cases)` です。

4. **B.** まずspec、次にcode、次にtest/eval case。この順序がloopのdriftを防ぎます。
   specがsource of truthであり、codeはその現在のimplementationです。

5. **tracking、damage、refund、documents、customs、billing**（keywordが一致しない場合の
   fallback `'unknown'` もあります）。

6. **C.** production dataへの書き込みはreal customerへの害をもたらし、元に戻すのが
   難しい。手動approvalが必要です。scratch fileのreadはほぼタダで間違えられます。

7. **`'unknown'`。** `'hello'` はどのkeywordにも一致しないので、すべてのcategoryの
   scoreが0になります。`classify_ticket` はscoreが `> 0` のときだけ最良のcategoryを
   返し、それ以外では `'unknown'` です。

8. **B.** `PreToolUse` hookはtool callの前に走り、それをblockできます。「Xに触れないと
   覚えておいて」を、harnessが強制するものに変えます。

9. **$0.081。** Input: 12,000 × $3.00 / 1,000,000 = $0.036。Output: 3,000 × $15.00 / 1,000,000 =
   $0.045。Total = $0.036 + $0.045 = $0.081。

10. **B.** fileし、spec-vs-evalを決め、失敗したinputをeval setに追加する。それが
    feedbackを一回限りのfixではなく永続的なものにするtriage ruleです。
