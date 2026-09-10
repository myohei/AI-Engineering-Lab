# Week 21: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 21 README](README.ja.md) · [演習](exercises.ja.md)

各問に答えてから、Answer keyで確認してください。各問の末尾には、出題元のConcepts section（§）またはnotebook cellへのpointerが付いています。

1. **(MCQ)** Unity Catalogの三段階namespace `catalog.schema.object` において、次のうち有効な *object* typeはどれですか？ *(Concepts §UC is governanceを参照)*

   - A) metastore
   - B) volume
   - C) workspace
   - D) compute plane

2. **(MCQ)** Delta tableにdefault設定で `VACUUM` を実行した後、`SELECT * FROM tbl TIMESTAMP AS OF '30 days ago'` を試します。どうなりますか？ *(Concepts §Delta gives time travelを参照)*

   - A) 常に動く。VACUUMはfileをcompact化するだけ
   - B) 失敗する。7日より古いdata fileが恒久削除されているため
   - C) errorなしで空のtableを返す
   - D) tableがpartition済みの場合のみerrorを返す

3. **(Short answer)** Unity Catalogのprivilege modelが「additive-only」と記述されるのはなぜですか？また、`zrl_.silver.shipments` を読むためにprincipalが必要な *二つの* privilege種類は何ですか？ *(Concepts §privilege modelを参照)*

4. **(MCQ)** notebook `02-medallion-sql.ipynb` のsilver queryは、`ROW_NUMBER() OVER (PARTITION BY shipment_id ORDER BY planned_departure)` でdedupeし、`WHERE rn = 1` を残します。`carrier_id` でpartitionすると何が壊れますか？ *(Concepts §medallion、notebook 02 cell 4を参照)*

   - A) 何も壊れない。carrier_idも行ごとに一意である
   - B) 同じcarrierの別々のshipmentが一つにつぶされる
   - C) imputationが動かなくなる
   - D) time travelが失敗する

5. **(MCQ)** managed tableとexternal tableについて正しい記述はどれですか？ *(Concepts §Unity Catalogを参照)*

   - A) `DROP TABLE` はどちらもdataを削除する
   - B) `DROP TABLE` がdataを削除するのはmanaged tableだけである
   - C) external tableはDeltaになれない
   - D) managed tableには `LOCATION` 句が必要である

6. **(Short answer)** notebook `01-unity-catalog-and-delta-lab.ipynb` は最後に `bronze rows` と `time-travel versions` をprintします。labを実行した後、`time_travel_demo` tableのversionがちょうど **2** になる理由を説明してください。 *(Notebook walkthrough、notebook 01 cells 9〜12を参照)*

7. **(MCQ)** filter column（`carrier_id`）でdata skippingを有効にしたいが、後でlayoutのkeyを打ち直す可能性もあります。新しいtableで使うべき機能はどれですか？ *(Concepts §Delta gives time travelを参照)*

   - A) Hive partitioning
   - B) `ZORDER BY` のみ
   - C) liquid clustering（`CLUSTER BY`）
   - D) `OPTIMIZE` のみ

8. **(Short answer)** 実例のGRANTで、`zrl_analysts` がtableへの `SELECT` だけではなく、`USE CATALOG ON CATALOG zrl_` *と* `USE SCHEMA` *と* `SELECT` を受け取る必要があるのはなぜですか？ *(Concepts §privilege modelを参照)*

9. **(MCQ)** notebookの `%sql` cell `CREATE OR REPLACE TABLE shipments_bronze AS SELECT * FROM read_files('/Volumes/zrl_/zorologistics/raw/shipments.csv', format => 'csv', header => true, inferSchema => true)` がDelta tableを生成するのはなぜですか？ *(Notebook walkthroughを参照)*

   - A) `read_files` はDeltaしか出力しない
   - B) 明示しない限り、Databricksのdefault table formatがDeltaであるため
   - C) CSVがgeneratorで既に変換されていたため
   - D) それがstreaming tableであるため

10. **(MCQ)** 次のうち、Hive partitioningではなくliquid clusteringの *帰結* はどれですか？ *(Concepts §Delta gives time travelを参照)*

   - A) tableをrewriteせずにclustering keyを変更できる
   - B) time travelが不可能になる
   - C) deletion vectorの有効化が必要になる
   - D) `VACUUM` と互換性がない

## Answer key

1. **B: volume.** volumeは `catalog.schema.object` レベルのgoverned objectです。metastoreはcatalogの*上*のregistryであり、workspace/compute planeはplatformの概念であってUC objectではありません。

2. **B: 失敗します。** VACUUMはretention窓（default 7日）より古いdata fileを恒久削除するため、その窓を超えたtime travelは不可能です。

3. **additive-onlyとは `DENY` が存在しないこと**です。principalはprivilegeを*得る*ことしかできず、defaultは「何もなし」です。tableを読むには、principalに **traversal**（`USE CATALOG zrl_` + `USE SCHEMA silver`）**とaction**（tableへの `SELECT`）が必要です。二種類とも必須です。

4. **B.** `carrier_id` でpartitionして各partition一行だけ残すと、一つのcarrierの別々のshipmentがすべて一行につぶれます。`shipment_id` が、一意のままでなければならない自然keyです。

5. **B.** `DROP TABLE` がdataを削除するのはmanaged tableだけです。external tableはmetadataのみdropします（dataはあなたのstorageに残ります）。

6. **二つのversion = `CREATE OR REPLACE`（version 1、1,000行）と `INSERT`（version 2、さらに1,000行）です。** 各writeが新しいtransaction log entryをappendするので、`DESCRIBE HISTORY` はちょうど二つのversionを示し、`VERSION AS OF
   1` は1,000行のstateを読み、currentは2,000を読みます。

7. **C: liquid clustering。** `CLUSTER BY` はskippingのためのdataのcolocationと、rewriteなしのkey変更を両立させます。`ZORDER BY` 単独では、rewriteなしにkeyを打ち直すことはできません。

8. **privilegeは下に継承されますが、traversalとactionは別物です。** tableへの `SELECT` だけではそれ自体では不十分で、principalはまず `USE CATALOG` と `USE SCHEMA` でcontainerに*到達*しなければなりません。UCはtraversal連鎖にactionを加えたものを要求します。親への `USE` grantのない素の `SELECT` grantでは、読みは許可されません。

9. **B.** Deltaはdefaultのstorage layerであり、設定で変えない限りDatabricksで作られるすべてのtableがDelta tableなので、`CREATE … AS SELECT FROM read_files` はgoverned Delta tableとしてlandingします。

10. **A.** Hive partitioning/Z-orderに対するliquid clusteringの最大の利点は、tableをrewriteせずにclustering keyを変更できることです。
