# Week 14: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 14 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `notebooks/01-react-agent-from-scratch.ipynb` をmock brainでend-to-endに
   実行します（API key不要）。最後にscenario score（0〜10の数字）がprintされます。
   その数字をExcel trackerのWeek 14 sheetに記録してください。

2. **Standard**: 五つ目のtool `list_carriers`（`zoro.data` からcarrier名、region、
   on-time rate、fleet sizeを返す）を、適切なJSON schema付きで追加します。tool
   registryに登録し、それを必要とする新しいscenarioを一つ追加して、traceに正しい
   （引数なしでの）呼び出しが示されることを確認します。

3. **Stretch**: `OPENAI_API_KEY`（または `OPENROUTER_API_KEY`）をsetし、実際のmodelで
   10 scenarioを再実行して、scoreをmockと比較します。保存されたtraceを開き、実際の
   modelとmockが一致しないscenarioを **一つ** 見つけます。*なぜか*（tool選択、引数
   format、refusal振る舞い）を説明するmarkdown cellを書きます。

4. **Portfolio**: agent、trace log、そして次を述べる短い `README` blockをcommitします:
   10 scenario、最終score、guardrailの正確な閾値（max step、cost cap、refusal policy）。
   これはprogram最初のinspectable agent artifactです（[`curriculum/projects/README.md`](../projects/README.md) で追跡）。

## Hints

1. **Easy**: すべてのcellを上から下へ実行します。mock brainにkeyは不要で、最終cellは
   `FINAL_SCORE` を0〜1のfractionとしてprintします。その数字をそのまま記録してください。
2. **Standard**: `TOOLS` registryで、既存toolの三部分の形（function、`name`/`description`、
   `parameters` schema）をまねます。`list_carriers` は引数を **取らない** ので、
   `required` は `[]` です。`expect` が `list_carriers` を名指しするscenarioを追加します。
3. **Stretch**: *同じ* scenario IDについて、実際のrunのtraceをmockのものとdiffします。
   違う `tool`、違う `args` 値、あるいはmockがactしたところの `refuse` を探してください。
4. **Portfolio**: reviewerは `README` blockを初見で（前提知識なしで）読みます。10 scenario、score、
   三つの閾値（`max_steps`、`cost_cap`、refusal policy）を、形容詞ではなく具体的な
   数字で述べてください。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: agent loopとReActを学ぶ（reference/knowledge-base/10-agents-multiagent.md）。
- [ ] Tue: tool-calling loopを手で実装する。2つのtool（track shipment、convert units）を配線する。
- [ ] Wed: planningとreflectionを追加する。すべてのstepをlogする。traceがdebuggerです。
- [ ] Thu: guardrailを追加する: refusal、max step、cost cap。adversarial inputをtestする。
- [ ] Fri: Use case: agentが未見の10 scenarioを解く。trace logを公開する。
- [ ] Sat: Week 14 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新する。agentとtraceをcommitする。
