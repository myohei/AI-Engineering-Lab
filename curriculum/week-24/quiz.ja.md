# Week 24: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 24 README](README.ja.md) · [演習](exercises.ja.md)

各問に答えてから、Answer keyで確認してください。各問の末尾には、出題元のConcepts section（§）またはnotebook cellへのpointerが付いています。

1. **(MCQ)** Unity Catalogのprivilege modelは「additive-only」です。実務的にそれが意味するのはどれですか？ *(Concepts §governanceを参照)*

   - A) 特定のprincipalを `DENY` できる
   - B) `DENY` は存在しない。principalはprivilegeを得るだけで、defaultは「何もなし」
   - C) grantはworkspace横断で自動複製される
   - D) privilegeはtableにのみ適用され、viewには適用されない

2. **(Short answer)** `01-governance-and-finopps.ipynb` で、`mask_value` functionはなぜ `STRING` ではなく `DOUBLE` をreturnしなければならないのですか？ *(Concepts §governance、notebook 01 cell 7を参照)*

3. **(MCQ)** *どのsource tableが* `gold_on_time_kpis` を支えているかを証明するqueryはどれですか？ *(Concepts §system tables、notebook 01 cell 17を参照)*

   - A) `SELECT * FROM system.access.audit`
   - B) `SELECT * FROM system.access.table_lineage WHERE target_table_full_name LIKE '%gold_on_time_kpis'`
   - C) `SELECT * FROM system.billing.usage`
   - D) `SHOW GRANTS ON TABLE gold_on_time_kpis`

4. **(MCQ)** bundleにおいて `prod` targetを `dev` と区別するのは何ですか？ *(Concepts §DABsを参照)*

   - A) `prod` は別のbundle名を使う
   - B) `mode: production` がworkspaceをうっかりした上書きから守る
   - C) `prod` はvariableを使えない
   - D) `prod` は `bundle validate` をskipする

5. **(Short answer)** CI/CDのreference flowが、personal access tokenではなくOIDC token federation（またはOAuth M2M）を使うのはなぜですか？ *(Concepts §DABs、How it breaksを参照)*

6. **(MCQ)** **row filter** の最も良い説明はどれですか？ *(Concepts §governanceを参照)*

   - A) entitlement tableをjoinするview
   - B) groupごとにrowを隠す、tableにattachされたboolean UDF
   - C) 自由textを書き換えるLLM call
   - D) column-levelのNULL mask

7. **(MCQ)** serverless computeは *premium* DBU rateを請求するのに、総costではしばしば勝ちます。なぜですか？ *(Concepts §FinOpsを参照)*

   - A) cold-startすることがないから
   - B) 古典的なbillを支配するidle時間と過剰provisioningを消すから
   - C) rate limitがないから
   - D) DBU rateがSKUs横断でフラットだから

8. **(Short answer)** notebookは `total_dbu * 0.55` でcostを見積もり、rateは「illustrative」とcommentしています。本当のdollar値を得る正しい方法は何ですか？また、どのtableをjoinしますか？ *(Concepts §FinOps、notebook 01 final cellを参照)*

9. **(MCQ)** `databricks bundle validate --strict -t dev` が保証するのは何ですか？ *(Concepts §DABsを参照)*

   - A) resourceがprodにdeployされる
   - B) configが健全であること。warningはerrorとして扱われる
   - C) pipelineが正常に実行されたこと
   - D) workspaceがlockされること

10. **(MCQ)** **column mask**（`ai_mask` ではなく）はどれですか？ *(Concepts §governance、How it breaksを参照)*

   - A) `ai_mask(text, ARRAY('person_name', 'email'))`
   - B) `ALTER TABLE t ALTER COLUMN value_usd SET MASK f`
   - C) `ai_classify(text, ARRAY('a','b'))`
   - D) `CREATE VIEW v AS SELECT '*** REDACTED ***'`

## Answer key

1. **B.** `DENY` は存在しません。accessはadditiveにgrantされ、defaultは「何もなし」なので、広すぎるgrantは能動的にrevokeしなければなりません。

2. **mask functionのreturn typeは、maskされるcolumnの型と一致しなければならないから**です。`value_usd` は `DOUBLE` なので、`mask_value` は `DOUBLE` をreturnしなければなりません。`STRING` returnなら `SET MASK` が失敗します。

3. **B.** `system.access.table_lineage` はsource→target tableの対応を示します。targetを `gold_on_time_kpis` でfilterすれば、そのupstream sourceが列挙されます。

4. **B.** `mode: production` はworkspaceをうっかりした上書きから守ります。`dev` は速いiterationのために `mode: development` を使います。

5. **repoにsecretを保存しないため**です。OIDC/M2MはCI platformのidentityをDatabricks OAuthと交換します（またはrepoの外で管理されるservice-principal client secretを使います）。PATは長寿命のsecretで、source管理下に置いてはいけません。

6. **B.** row filterは `SET ROW FILTER` で適用されるboolean UDFで、callerが見てよいrowに対してのみTRUEを返します。

7. **B.** classic computeはidle VMsと過剰provisioningに課金します（22 h/day idleするall-purpose clusterは2 hの仕事に約24 hを請求）。serverlessは実行分だけ課金するので、premium rateでも月次総spendではしばしば安くなります。

8. **`system.billing.usage` を `system.billing.list_prices` にjoinする**ことです。`sku_name`（とcloud）で結合し、`usage_quantity` にSKUのprice（`p.pricing.default`）を掛けます。固定の `0.55` 定数の代わりに。

9. **B.** `validate --strict` はbundle設定をcheckし、warningをerrorとして扱います。deployも実行もしません。

10. **B.** `ALTER TABLE … ALTER COLUMN … SET MASK` は決定論的なquery時governance policyをattachします。`ai_mask`（A）はLLMによるcontent書き換え、view（D）はdynamic viewであってcolumn maskではありません。
