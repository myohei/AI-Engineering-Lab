# 24週カリキュラムの日本語翻訳を完了する

> feature: `translate-curriculum-ja` — Goal contract pointer。Goal binding後の完了条件の正は `goals/translate-curriculum-ja/goal.md` とGoal recordです。

## Goal

`goals/translate-curriculum-ja/goal.md` のExact allowlistとVerification surfaceに従い、Week 02〜24の週次Markdown教材69件を日本語化する。英語sourceとnotebookは変更しない。

## Scope

- In: Goal contractのExact allowlist。
- Out: Goal contractのOut。

## Constraints & Preferences

- Goal contractのstate schema、failure enum、review protocol、Goal tool sequenceを正とする。
- agentはgit操作を行わず、scope外pathを変更しない。

## Progress

### Done

- inventory、Week 01実例、checker、Goal controller、workflow templateを調査。
- Plan revision 1〜3のSTOP記録を`goals/translate-curriculum-ja/unresolved.md`へ保存。
- Codex Astra recommendationをPlan revision 4へ反映中。

### Done

- 実装完了: 69 JA教材・validator・baseline・review state/report・README.ja.md index。V1〜V6全件exit 0。
- 翻訳: zai/glm-5.3（batch 1〜5）、review: 同model別context（block単位、reject 6件は全てfix後approved）。

## Next Steps

- Plan review承認後にtask #70をdoingへ戻し、Goal recordへbindingする。
- Goal complete後に、このTASK.mdをGoal pointer/statusだけの内容へ保つ。

## Critical Context

- 契約の詳細、V1〜V6、Exact allowlist、P0〜P9は`goals/translate-curriculum-ja/goal.md`を参照。
- 監査履歴と未解決findingは`goals/translate-curriculum-ja/unresolved.md`を参照。
