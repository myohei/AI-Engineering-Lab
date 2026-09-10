# Week 20: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 20 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-bedrock-converse-and-knowledge-bases.ipynb`を最後まで実行する。
   Converse APIでWeek 6のprompt suiteをBedrock modelにわたって実行し、RAGのために
   Knowledge Baseにqueryして、最後にrecallとgroundednessをprintします。両方の数字を
   Week 20のtracker sheetに記録する。

2. **Standard**: prompt suite比較に*三つ目*のBedrock modelを追加する（例: Nova Lite vs
   Claude vs Llama）。accuracy、latency、推定token costの三行tableをmarkdown cellに追加し、
   各modelが他の二つに対してどれだけ得または失するかのdeltaを述べる。

3. **Stretch**: Guardrailを（agentだけでなく）**Knowledge Baseのresponse path**に適用する。
   guardrailをattachした`retrieve_and_generate`に対してoff-topic query setを実行し、
   guardrailなしのrunと比べてblocked/allowed countがどう動くかを示す。

4. **Portfolio**: **三cloud比較matrix**（Foundry vs Vertex vs Bedrock）を
   [`curriculum/projects/`](../projects/README.md)に公開する。すべてのcellがWeek 18〜20の
   測定値までtraceできなければならない。cost行を追加し、「どのjobにどのcloudか」の
   recommendationを一段落で締める。これがPhase 6のcapstoneであり、matrixこそが
   deliverableです。

## Hints

1. **Easy**: `RECALL`と`GROUNDEDNESS`を記録する。dry-runのlocal retrieverは*target*値
   （`1.000 / 1.000`）をprintします。liveのKnowledge Baseはそれに合わせるか超える必要が
   あります。
2. **Standard**: `MODELS`に三つ目のmodel IDを追加し、`accuracy_for`を呼び、他の二つに対する
   accuracy、latency、推定token costのdeltaを述べる。
3. **Stretch**: guardrailを`retrieve_and_generate`にattachし（KB callにguardrail configを
   渡す）、off-topic query setを実行してblocked/allowed countを比較する。
4. **Portfolio**: matrixはWeek 18〜20のguideから行ごとにbuildする。printされた数字のない
   cellはgapです。当て推量ではなく、空欄の正直なまま残す。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: AWS accountとIAM least-privilege roleをsetup。Bedrock modelを有効化。
- [ ] Tue: Converse API lab: Week 6のprompt suiteをBedrock modelで実行。
- [ ] Wed: shipping policy用のKnowledge Base（RAG）をbuild。citation付きでquery。
- [ ] Thu: Bedrock Agent + Guardrailsを作成。blockされたpromptをtest。
- [ ] Fri: Use case: cost付きの3-cloud比較matrix（Foundry vs Vertex vs Bedrock）を公開。
- [ ] Sat: Week 20のquiz（quiz.md）を受ける。8/10で合格。scoreをNotesに記録。
- [ ] Milestone: Excel trackerを更新。AWS guideとmatrixをcommit。
