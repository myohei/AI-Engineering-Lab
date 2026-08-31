# Week 01: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 1 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercise

1. **Easy:** `notebooks/01-environment-and-tools.ja.ipynb` を最初から最後まで実行します。最後に0〜6のreadiness scoreが表示されます。Week 1のExcel tracker sheetに数字を記録してください。checkが失敗したらenvironmentを直して再実行します。目標はerrorのスクリーンショットではなく、score 6です。

2. **Standard:** `notebooks/02-zorologistics-data-generator.ja.ipynb` を開き、2つ変更します。seedを `42` から自分で決めた値へ、shipment countを `100_000` から `5_000` へ変更します。再実行し、(a) row countが変わる、(b) column schemaは同じ、(c) planted data issue（duplicate row、`NaN` weight、`NaN` distance）がまだ存在することを確認します。schemaは同じなのにrowが変わる理由を、Markdown cellに1文で書きます。

3. **Stretch:** 自分のscratch space（curriculum folderにはcommitしない）にstandalone script `generate_small.py` を書きます。`zoro.data`をimportし、各table（`carriers`、`lanes`、`shipments`、`support_tickets`）をexplicit seed付き・縮小サイズで1つずつ生成し、table名とrow countを1行ずつprintします。fresh terminalから `python generate_small.py` を実行し、Jupyterの外でもenvironmentが使えることを証明します。

4. **Portfolio:** [`curriculum/projects/README.md`](../projects/README.md) で追跡する **ZoroLogistics data generator + silver dataset** milestoneを始めます。`save_all()`のoutputをforkの`data/` directoryに、`data/data-dictionary.md`と一緒にcommitします。さらにREADME blockを追加し、seed、tableごとの正確なrow count、schemaを記載します。これはprogramで最初に作る、見知らぬ人がinspectできるartifactです。

## Hints

1. **Easy:** scoreが6でなければ、上から各`FAIL`行を読みます。最初のfailure（通常は`zoro` import失敗、またはGit work tree外）がscoreを下げている原因です。
2. **Standard:** `data.shipments(...)`に渡す`seed`と`n`だけを変更します。`zoro/data.py`は変更しないでください。変更前後に`df.columns`をprintし、valuesではなくcolumn listが同じことを確認します。
3. **Stretch:** notebookのwalk-up path loop（`while not (p / "zoro").is_dir() ...`）を再利用します。どのfolderからscriptを起動しても`zoro`を見つけられるようにします。
4. **Portfolio:** README blockの1か所に4つのrow countとseedを記録します。見知らぬ人があなたに質問せず、同じ数字を再生成できることが目標です。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: VS Code、Python environment（uvまたはconda）、gitを設定し、repoをfork/cloneする。
- [ ] Tue: environment notebookのPython refresher exerciseを完了する。
- [ ] Wed: environment check notebookを最初から最後まで実行する（version、import、deterministic seed）。
- [ ] Thu: ZoroLogistics data generatorを作る（shipments、carriers、lanes、deterministic seed）。
- [ ] Fri: use case：100k-row datasetを生成し、CSV/Parquetへ保存し、data dictionaryと一緒にcommitする。
- [ ] Sat: Week 1 quiz（`quiz.ja.md`）を受け、8/10で合格し、scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新し、Week 1をcheck offしてforkへpushする。
