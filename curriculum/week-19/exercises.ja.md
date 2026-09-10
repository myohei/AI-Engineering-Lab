# Week 19: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 19 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-gemini-multimodal-ocr.ipynb`を最後まで実行する。bill-of-lading
   imageをlocalでrenderし、Gemini visionでfieldをstructured JSONに抽出し、per-field
   accuracyとcost-per-documentの推定値をprintします。両方の数字をWeek 19のtracker
   sheetに記録する。

2. **Standard**: 抽出loopを*別の* Gemini model rungで再実行する（例: `gemini-2.5-flash-lite`
   vs `gemini-2.5-flash`）。accuracy vs cost per documentの二行tableをmarkdown cellに追加し、
   安いほうのmodelがあなたのaccuracy barをクリアするかどうかを一行で書く。

3. **Stretch**: 抽出したJSONを**BigQuery**にloadし、各行をclassifyする単一の
   `ML.GENERATE_TEXT` callを実行する（例: `freight_terms`整合性やcommodity risk label）。
   table schemaと正確なSQLをdocument化し、このdataに対するfree-tierの境界がどこかを
   記録する。

4. **Portfolio**: `vertex-deployment-guide.md`をcommitする（AI Studio vs Vertex、OCR
   accuracy table、ADK agent、eval score、cost per document）。これはWeek 20で完成させる
   三cloud比較matrixの**Google列**です。

## Hints

1. **Easy**: `OVERALL_FIELD_ACCURACY`と`COST_PER_DOCUMENT_USD`を記録する。image renderと
   accuracyはkeyなしでlocalに動きますが、*本当の*数字には`GOOGLE_API_KEY`が必要です。
2. **Standard**: `gemini_extract` cellの`MODEL`定数を変えて、同じ4枚のimageで再実行する。
   二行tableでaccuracy vs cost-per-documentを比較する。
3. **Stretch**: `ML.GENERATE_TEXT`には先にremote modelの登録が必要です（`CREATE MODEL …
   REMOTE WITH CONNECTION`）。抽出したJSONをloadし、classify queryを一回実行してschemaを
   記録する。
4. **Portfolio**: AI Studio対Vertexのdecisionを先頭に置き、次にaccuracy table、ADKのeval
   score、cost per document。この四つの見出しがそのままGoogle列になります。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: Google CloudとAI Studioをsetup。API keyを取得。quotaを確認。
- [ ] Tue: Gemini multimodal lab: BoL image → structured JSON。accuracyを測定。
- [ ] Wed: support agentをADK/Agent Engineで再作成。Foundry版と比較。
- [ ] Thu: golden setでVertex evaluationを実行。結果をBigQueryにlog。
- [ ] Fri: Use case: end-to-end pipeline（images → clean table）。cost per documentを公開。
- [ ] Sat: Week 19のquiz（quiz.md）を受ける。8/10で合格。scoreをNotesに記録。
- [ ] Milestone: Excel trackerを更新。Vertex guideをcommit。
