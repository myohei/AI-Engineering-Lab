# Week 17: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 17 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-agent-ops-observability.ipynb`をend-to-endで実行する（API keyは
   不要）。最後にcoverage metric（0から1までの数字）をprintします。その値を
   Excel trackerのWeek 17 sheetに記録する。

2. **Standard**: ZoroLogistics向けの二つのOpenClaw skill、`track-shipment`と
   `refund-policy`を書く。YAML frontmatter（name、description、明確な*when to use*
   trigger）付きの`SKILL.md` fileとして作る。workspaceにloadし、`openclaw skills list`
   （またはdashboard）で両方が認識されていることを確認する。

3. **Stretch**: Hermes-class modelをpullし（`ollama run hermes4`）、OpenClawをそれに
   向ける（`baseUrl: "http://localhost:11434"`、**`/v1`なし**）。前のmodelで使った
   同じ三つのpromptを実行する。Hermes modelがどのpromptをうまく扱い、どれをしくじったか、
   そしてtool useにfunction-calling tuningがなぜ重要かを書き留める。

4. **Portfolio**: 二つのskill、生成されたops runbook、coverage metricをcommitする。
   runbook（threshold、dashboard、incident手順）は、reviewerがcoldで読むstanding ops
   artifactである（[`curriculum/projects/README.md`](../projects/README.md)で管理）。

## Hints

1. **Easy**: notebookを最初から最後まで実行する（keyは不要）。最後のcellが`COVERAGE`を
   0から1までの数字としてprintする。その値をそのまま記録する。
2. **Standard**: 各`SKILL.md`には`name` + `description`のfrontmatterと、正確な手順を
   書いたMarkdown bodyが必要。agentが照合するのは`description`なので、具体的にする
   （「shipmentのstatusやETAをユーザーが尋ねたとき」など）。`openclaw skills list`で
   確認する。
3. **Stretch**: OpenClawをOllamaに向けるときは`baseUrl: "http://localhost:11434"`で
   **`/v1`なし**。前と同じ三つのpromptを実行し、Hermes modelがどれをうまく扱い、どれを
   しくじったか、それがfunction-calling tuningとどう対応するかを記録する。
4. **Portfolio**: 二つの`SKILL.md` file、生成されたrunbook、coverageの数字を一緒に
   commitする。reviewerはrunbookをcoldで読むので、thresholdとincident手順は形容詞で
   なく具体的な数字で書く。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: OpenClawとHermesを学ぶ（reference/agents/openclaw.md + reference/agents/hermes.md + knowledge-base/10）。
- [ ] Tue: OpenClawをlocalにinstall・configure。channel（WebChatまたはTelegram）を接続。
- [ ] Wed: OpenClaw skillを2つ書く。Week 16のMCP serverを接続。context loopをtest。
- [ ] Thu: Ollama経由でHermes-class modelに差し替え。assistantの品質を比較。
- [ ] Fri: Use case: assistantにtracingとcost trackingを追加。ops runbookを公開。
- [ ] Sat: Week 17のquiz（quiz.md）を受ける。8/10で合格。scoreをNotesに記録。
- [ ] Milestone: Excel trackerを更新。skillsとrunbookをcommit。
