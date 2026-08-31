# Week 01: Quiz（10問、8/10で合格）

> **日本語版** · [英語版](quiz.md) · [Week 1 README](README.ja.md) · [演習](exercises.ja.md)

10問すべてに答えてから、Answer keyで確認してください。*(Concepts §Xを参照)* はREADMEのsubsection、*(notebook cell Yを参照)* は `01-environment-and-tools.ipynb` または `02-zorologistics-data-generator.ipynb` のcellを示します。

1. **Multiple choice。** Andrew NgのAI Engineering Skills Mapの4つのskillを正しく並べているのはどれですか？ *(Concepts §1を参照)*
   a. Prompt engineering、fine-tuning、RAG、deployment
   b. AI applicationのbuilding/deployment、software engineering fundamentals、coding agentの利用、buildの方向付け
   c. Data engineering、ML、deep learning、MLOps
   d. Frontend、backend、data、DevOps

2. **Multiple choice。** `shipments(100_000, seed=42)` が100,000行ではなく100,200行を返すのはなぜですか？ *(Concepts §6、notebook「Verify persistence」cellを参照)*
   a. NumPyのrounding error
   b. Week 2で見つけるため、generatorが約0.2%のduplicate rowを意図的に追加する
   c. seedはcarriersにだけ適用され、shipmentsには適用されない
   d. `save_all()`が常に200行のheaderを追加する

3. **Short answer。** seed cellで、最初の `first_five(42)` は `[89250, 773956, 654571, 438878, 433015]` を返します。同じseedで2回目に呼ぶと何が返り、なぜですか？ *(notebook「seed habit」cellを参照)*

4. **Multiple choice。** seed付きrandomnessに推奨されるmodernなNumPyの書き方はどれですか？また、legacyのglobal formより好まれる理由は何ですか？ *(Concepts §6を参照)*
   a. `np.random.seed(42)`。simpleでthread-safeだから
   b. `numpy.random.default_rng(seed)`。localでthread-safe、hidden global stateがないから
   c. `random.random(42)`。built-inで速いから
   d. `np.random.RandomState`。deprecatedだが必須だから

5. **Short answer。** environment notebookの最後のcellは `READINESS = CHECK_PYTHON + CHECK_LIBS + CHECK_ZORO + CHECK_GIT + CHECK_NUMPY + CHECK_SEED` を計算します。score 6は何を意味し、5だったら何をすべきですか？ *(notebook final cellを参照)*

6. **Multiple choice。** `zoro/data.py`で、`lanes` tableへの *foreign key* はどのcolumnですか？ *(Concepts §2、data dictionaryを参照)*
   a. `shipments.shipment_id`
   b. `shipments.lane_id`
   c. `lanes.lane_id`
   d. `carriers.carrier_name`

7. **Multiple choice。** generator notebookは`save_all(...)`を呼ぶ前に、`zoro/`を含むfolderまで親をたどってoutput directoryを解決します。これによってどのfailureを防ぎますか？ *(notebook「Generate and persist」cellを参照)*
   a. `data/`がrepo rootではなく *notebook folder* に書かれること
   b. carriersとlanesの間でseed collisionが起きること
   c. duplicate `shipment_id`が生成されること
   d. `data-dictionary.md`でGit merge conflictが起きること

8. **Short answer。** Week 1のoutputに仕込まれた3つのdata-quality flawを挙げ、seed 42でのそれぞれのおおよその件数を書いてください。 *(Concepts §6、verification cellを参照)*

9. **Multiple choice。** `02-zorologistics-data-generator.ipynb`のdata dictionaryはtupleのlistから`data/data-dictionary.md`を書き出します。各tupleが持つ4つのfieldは何ですか？ *(notebook「data dictionary」cellを参照)*
   a. table、column、dtype、meaning
   b. table、seed、dtype、count
   c. column、value、sample、note
   d. name、type、nulls、source

10. **Short answer。** なぜ同じseedは単なる便利機能ではなく、program全体の *contract*（「same seed, same company」）なのですか？ *(Concepts §6とFridayのZorost gateを参照)*

## Answer key

1. **b。** Ngの4領域は、AI applicationのbuilding/deployment、software engineering fundamentals、coding agentの利用、buildの方向付けです。prompt engineeringとRAGは最初の領域に含まれるbuilding blockであり、4領域そのものではありません。

2. **b。** `data.py`は `pd.concat([df, df.sample(frac=0.002)])` を実行し、約0.2%（100,000行なら200行）のduplicate rowを仕込みます。Week 2で実際にcleanするためです。

3. **同じlist** `[89250, 773956, 654571, 438878, 433015]` です。固定seedにより`default_rng`が同じsequenceを再生します。異なるseed（例：`7`）なら異なる数字になります。

4. **b。** `numpy.random.default_rng(seed)`はlocal generator objectを返すため、別のlibrary callが順序を変えるhidden global stateがありません。`np.random.seed`はglobal stateを変更し、reproducibilityを静かに壊す可能性があります。

5. **6は6つすべてのcheck（Python version、import、`zoro.data`の完全性、Git、NumPy、determinism）がpassし、environmentが準備できたことを意味します。5なら各FAIL行を読み、壊れているcheckを直して6になるまで再実行します。** failing environmentのまま先へ進まないでください。

6. **b。** `shipments.lane_id`は`lanes.lane_id`を参照します。`shipment_id`はshipments table自身のprimary keyです。

7. **a。** rootを解決しないと、`save_all()`がkernelのcwdを基準に動き、CSVがnotebook folderに書かれることがあります。これでは後続週が期待するrepo rootの`data/` pathが壊れます。

8. **duplicate shipment row（0.2% sampleで約200行）、`NaN`の`weight_kg`（0.3% sampleで約301個）、`NaN`のlane `distance_km`（20 laneの5%で約1個）**です。Week 2で見つけるために、すべて意図的に仕込まれています。

9. **a。** 各tupleは `(table, column, dtype, meaning)` です。notebookはこれをDataFrameにしてからMarkdown tableに書き出します。

10. **seedがあれば、見知らぬ人でもあなたのforkを再実行してbyte-identicalなdataを得られます。そのため、Week 23で測ったmetricをWeek 1のbaselineと比較できます。determinismがあるから、anecdoteではなくreproducible artifactになります。**
