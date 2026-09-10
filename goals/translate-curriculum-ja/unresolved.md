# Unresolved plan-review findings

判定: STOP（Plan adversarial review round 2終了時点でblocking findingが残ったため）。round 3以降の修正loopは開始しない。

## Round 1 → Round 2

- round 1: `plan-normal-review` と `plan-adversarial-review-r1` を別contextで実施。
- round 1の採用findingを `goals/translate-curriculum-ja/goal.md` の指摘節だけへ反映した。
- round 2: 新しいclean contextの `plan-adversarial-review-r2` が変更節だけを再レビュー。
- round 2は、未解決の採用findingを同じIDで再報告した。これは収束条件に該当する。

## 未解決finding

### F-A-001 — high / verification / blocking

- 対象: `Outcome`、`Key Decisions`、V1/V2、P0/P8。
- 事実: Planはstructural signature、protected token、link policy、quiz、self-testを要求するが、各Outcome項目と各validator/mutationの1対1対応が書かれていない。
- 反例: 実装者がMermaid、inline code、canonical link、3方向navigation、ledger 69件のいずれかをcheckerから漏らしても、V1/V2が成功し得る。
- round 2判定: 同じfinding IDで未解決。

### F-A-002 — high / execution / blocking

- 対象: `Outcome`、`Key Decisions`、P6/P7。
- 事実: 69ペアのbilingual reviewを要求するが、review batch/checkpoint、source/JA hashとのledger結合、P7で修正したときのsign-off失効条件がない。
- 反例: reviewerが50件目で停止した場合の安全なresume単位がなく、承認済みJAを後から変更しても`approved`が残り得る。
- round 2判定: 同じfinding IDで未解決。

### F-A-005 — high / failure / blocking

- 対象: `Constraints`、`Key Decisions`、P0/P1〜P5、Next Steps。
- 事実: P0はcanonical link追加前のraw source hashを保存する一方、P1〜P5はcanonical linkを追加し、Constraintsはsource hash変化でSTOPすると記載する。target JAのsnapshotもない。
- 反例: 正規のlink追加後のresumeだけでhash conflictになり、逆に例外化すると外部差分を見逃し得る。
- round 2判定: 同じfinding IDで未解決。

### F-A-006 — high / failure / blocking

- 対象: `Constraints`、`Key Decisions`、Next Steps、P1〜P5。
- 事実: scoped validatorの実行形式がVerification surface/stepに定義されず、retry対象がmissing fileに限られている。
- 反例: empty/truncatedまたは構造不一致の既存fileがmissingではないためretryされず、parallel batch中のsource hash conflict時の停止境界も不明。
- round 2判定: 同じfinding IDで未解決（round 1のnon-blocking findingがround 2でblockingと再評価された）。

### F-A-007 — high / integration / blocking

- 対象: Next Steps、P0/P8、Review packet evidence。
- 事実: `goal_complete`がcontroller-measured evidenceを要求し、`goal_verify`の実行も必要だが、Planは`goal_record_result`までしか工程化しておらず、runId/generation/workflowRunIdと各必須引数の対応が固定されていない。
- 反例: V1〜V6が成功しても、stale generationやworkflowRunId未対応のためGoal完了が拒否され得る。
- round 2判定: 同じfinding IDで未解決。

## 解消済みfinding

- F-A-003: 日本語navigationと英語notebook参照の方針が明記された。
- F-A-004: Exact allowlistとsource/notebook不変性の方針が明記された（baseline運用矛盾はF-A-005として残る）。
- F-A-008: P6→P7→P8の依存とGoal/TASK更新の直列性が明記された。

## Handoff

人間が次のPlan revisionを行うまで、`goal_start`、`tktk_goal_bind`、`goal_begin_run`、workflow起動、翻訳実装、`goal_complete`は実行しない。次回は未解決findingの前提（validatorの完全なtraceability、pair hash state machine、scoped retry、controller evidenceのtool sequence）を再設計してから、別の新規Plan reviewを開始する。

## Human resolution after STOP

ユーザーは、validator強化・bilingual review・batch retry・Goal tool sequenceを推奨案で承認し、link方針については「英語原文は変更せず、`curriculum/README.ja.md`の日本語indexのみ更新する」と決定した。この記録は旧Planの監査履歴であり、更新後Planの承認を意味しない。更新後Planは新しいbounded review cycleで再レビューする。

## Plan revision 2: round 1 → round 2 unresolved findings

round 1の通常review（`normal-plan-review-v2`）と、別clean contextの敵対的review（`adversarial-plan-review-v2-r1`）を実施し、採用findingを指す節だけ修正した。round 2の新しいclean context（`adversarial-plan-review-v2-r2`）で次のfindingが同じIDで再発、または新規blockingとして検出されたため、プロトコルに従いここでSTOPする。round 3以降の修正loopは開始しない。

### F-A-005 — high / failure / blocking（再発）

- baseline JSON/digestをcontroller runへ固定すると書いたが、P0にatomicなbaseline checkpointの作成順序、schema、resume時の照合操作がない。
- JSON作成後・digest作成前に停止した場合、generationの固定baselineを判定できない。
- 次回は`generation`、base commit、source/notebook raw hash、baseline manifest digestを含むcheckpointをatomicに作り、controller runへ同値を記録する手順を定義する。

### F-A-008 — high / failure / blocking（再発）

- ledgerと5 checkpointを個別にatomic replaceすると書いたが、両者のcommit順序・digest照合・片方だけ更新された場合のauthoritative stateがない。
- checkpoint replace直後にledger replace前で停止すると、approved row集合が不一致になる。
- 次回はcheckpointにledger digestとrow hash/statusを含め、書込み順序、resume照合、片側更新時のSTOP/rebuildを定義する。

### F-A-010 — high / failure / blocking（再評価）

- mainのwrite barrierとworker cancelは定義したが、各fileのatomic replace直前にworkerがbarrier/permitを確認し、cancel完了をackする手順がない。
- hash conflict検出時にrename直前のworkerが新規writeを完了し得る。
- 次回はmain管理のwrite permit、replace直前の確認、barrier後のack待ちを定義する。

### F-A-014 — high / integration / blocking（新規）

- `full` modeは69件・23週index・全ledgerを必須とする一方、P7aが`full/current pair V1`に依存している。
- Week 02〜06の15 rowしかない時点でfull modeを実行するとP7aが開始できない。
- 次回はP7a〜P7eを`--mode review --weeks <range>`へ明示的に変更し、full modeを全review完了後だけ実行する。

### Round 2判定

- blocking findings: 4件
- 判定: STOP。goal_start、workflow、翻訳実装、goal_completeは実行しない。

## Plan revision 3: final round 1 → round 2 unresolved findings

revision 3では、baseline/stateのatomicity、直列batch、scoped mode、run A/B、fixed workflow runner、protected token、Goal/TASK SoTを反映した。round 1の通常reviewとclean-context敵対的review後に局所修正し、round 2の新しいclean contextで次を同じID（または新規ID）としてblocking判定した。プロトコルに従い追加修正は行わない。

### F-A-001 — high / failure / blocking（再発）

- `translation-review-state.json`の`lastStateDigest`をdigest対象から除外すること、canonical serialization、更新順、fault時の扱いが未定義。
- 次回はstate digestのpayload/schema、`payload→digest→field→fsync→atomic replace`順を固定する。

### F-A-008 — high / verification / blocking（再発）

- quizのoption grammarを「全形式」と記すだけで、`a.`、`- A)`、answer keyの`**b.**`/`**B.**`などの具体形式が未列挙。
- 次回は形式別schemaとlabel mutationを明記する。

### F-A-009 — high / verification / blocking（再発）

- self-testがpure parser/fixture中心で、atomic state writerのreplace failure、旧state保持、invalid stateでSTOPするfault caseを含まない。
- 次回はisolated state writer fault-injectionをV2へ追加する。

### F-A-010 — high / failure / blocking（再発）

- `attemptCount=2`と`lastFailureCode`はあるが、retry可能code、即STOP code、attempt増加時点、2回目失敗時のstate/handoff遷移が未定義。
- 次回はfailure-code enumと遷移表を固定する。

### F-A-014 — high / evidence / blocking（再発）

- P9生成の`translation-review.md`へstate digestを出力し、V1でcanonical stateとの一致を確認する要件がない。
- 次回はreport headerのbaseline/state digestとdeterministic render一致を必須にする。

### F-A-016 — high / bug / blocking（新規）

- P7a〜P7eが`--mode review`をdependencyにするが、reviewer結果をmainがprovisional stateへ記録してからvalidatorを実行する順序が明記されていない。
- 次回は`reviewer result → main provisional record → review mode → rejectならfix/re-review → approved`の順を固定する。

### Revision 3最終判定

- blocking findings: 6件
- 判定: STOP。`goal_start`、workflow、翻訳実装、`goal_complete`は実行しない。

## Plan revision 4: Astra recommendation + round 1/2 unresolved findings

Codex Astra（`openai-codex/gpt-6-astra`）でPlan correction recommendationを取得し、single state、canonical digest、failure enum、quiz grammar、state-writer fault test、report digest、scoped review orderを反映した。Astraの敵対的reviewはusage limitで失敗したため、独立clean-contextのCodex Solをfallbackとして使用した。round 1通常review→fallback敵対review→局所修正→round 2変更箇所のみ敵対reviewを完了した。

### F-A-001 / F-N-001 — high / failure / blocking（再発）

- P0のbaseline/state/Goal記録境界で、`goal.md`記録成功後`tktk_log`前のcrash、`advance(P0)`前後のphase、baselineId導出、commit marker、resume codeが一意に定義されていない。
- 次回は各durable boundary、record欠落code、init/advanceのどちらがP0を確定するかを固定する。

### F-A-002 / F-N-002 — high / bug / blocking（再発）

- reject後のJA fixを予約・hash受理・同reviewer再reviewするactionがstate transition ledgerにない。`activeOperation`、attempt、batch root stateの整合も未定義。
- 次回はreject→fix reservation→write→scoped validation→hash accept→re-review→approveを明示する。

### F-A-003 — high / evidence / blocking（再発）

- translator/reviewer assignmentがstate上の文字列だけで、実dispatch receipt/session handleとの照合schemaがない。
- 次回はcontroller発行receipt、run/context/role/request/hashとの照合を固定する。

### F-A-006 / F-N-005 — high / integration / blocking（再発）

- generic workflowを禁止したが、必須runtimeで代替するread-only preflightのexact entrypoint、cwd、argv、write-set、exit条件が未定義。新script追加はallowlist問題にもなる。
- 次回は実行可能entrypointをcontractのscope/allowlistへ追加するか、workflow必須環境を明示的STOP条件にする。

### F-N-003 — high / integration / blocking（再発）

- settled run後のretryで、same generationを使う記述とnew generationを要求する記述が矛盾する。
- 次回はGoal controllerのrun/generation遷移に合わせ、旧run・新run・baselineId・stateDigestのhandoffを一つに固定する。

### F-N-007 — high / failure / blocking（再発）

- `WORKER_INTERRUPTED`やV1〜V6失敗時のretryable/terminal区分、handoff payloadのschema、run settlement→block→new-run手順が未定義。unknown-field rejectとも衝突する。
- 次回はfailureごとのrun/state/tktk遷移を固定する。

### F-N-008 — medium / bug / blocking（再発）

- protected-token candidate extractorにlowercase固有名・一般ASCII tokenのcatch-allまたは固定lexiconがなく、unclassified=0でも抽出漏れを検出できない。
- 次回はtoken extraction grammar/lexicon/catch-allとextractor omission fixtureを追加する。

### Revision 4最終判定

- blocking findings: 7件
- round 2後の修正loopは再開しない。`goal_start`、workflow、翻訳実装、`goal_complete`は実行しない。

## Human resolution / execution authorization (2026-09-05)

ユーザーが残りblocking findingを容認のうえ実装継続を明示指示（「実装完了な状態までもっていって。それぞれSubagentをたてて」/「continue」）。これにより:

- F-A-001/002/003, F-N-001/002/007/008: state machine・provenance・token抽出は**実用的サブセット**として実装する（canonical digest・atomic state・translation/review別attempt・ coverage manifest・token regex manifest は実装。controller発行receipt照合や完全な遷移表は割愛し、main直管理で代用）。
- F-A-006/F-N-003/F-N-005: generic workflow / Goal recordは本セッションcwd制約（root）により最初から不適用。tktk task #70を唯一のtask recordとする。
- F-N-101〜106（sa-2追加報告）: `STATE_PUBLISH_UNCERTAIN`・Outcome registry等は現契約に存在しない概念であり、reviewer sessionのdriftとして記録のみ。token抽出漏れ(F-N-101)とpause/resume不能(F-N-106)はそれぞれ上記対応・不適用に含める。
- 実装後も本fileは修正せず、監査履歴として保持する。
