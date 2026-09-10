# START HERE: AI Engineering Lab 完全初心者ガイド

> Pythonを1行も書いたことがない？ LLM APIを触ったことがない？ このページはあなたのためのものです。
> 一度上から最後まで読めば、約15分で、何から始め、何を期待し、詰まったときにどうするかが分かります。
>
> **English:** [START-HERE.md](START-HERE.md) · **日本語版:** このページ

**AI Engineering Labの一部 · [Zorost Intelligence AI Lab](https://zorost.com)が開発 · zorost.com**

---

## 1. このリポジトリは何ですか？

AI Engineering Labは、やる気のある初心者が **24週間**（週約10時間）で、実際に動くAI engineerになるための、無料・オープン・自習型のtraining programです。

ここでいう「AI engineer」とは、研究所で新しいmodel architectureを発明する人ではなく、**AIを使うsoftwareを設計し、構築し、評価し、shipする人**を指します。large language model（LLM）の仕組み、promptと評価の方法、自分のマシンでのmodel実行、fine-tuning、AI agent、AI coding toolの仕事での使い方、real cloud platformへのdeployを学び、最後はDatabricksのproduction capstoneで終わります。

すべてを1つの架空のケーススタディで学びます。あなたは運送会社 **ZoroLogistics** のAI engineering teamです。Week 1で生成したdatasetをWeek 24でも使うため、24個の無関係なtoy demoではなく、つながったportfolioが残ります。

![24週間の7つのphaseと、各phaseで作るもの](assets/diagrams/lab-journey.png)

## 2. 誰向けですか？ 先に何を知っておく必要がありますか？

**必要なもの:**

- softwareをインストールできるコンピューター（Windows、macOS、Linuxのいずれでも可）
- 24週間、週約 **10時間**（自習型なので、もっとゆっくりでも可）
- 基本的なコンピューター操作：アプリのインストール、ファイルの解凍、web browserの利用

**必要ないもの:**

- プログラミング経験。Week 1でPythonをゼロから教えます。
- 高校数学を超える数学。すべての式を平易な言葉で説明し、実行できるcodeで動きを確認します。
- 高性能なcomputerやGPU。Week 1〜8は普通のlaptopで動きます。GPUが重要になるWeek 8以降は、無料・安価な選択肢を紹介します。
- お金。Week 1〜13のtoolは無料で使えます。cloud週（18〜24）はfree tierを使い、範囲内に収める方法を説明します。

**向いている人:** AIをtoolkitに加えたいsoftware developer、engineeringへ進みたいdata analyst、学生・career changer、手探りで済ませずAI featureを作りたいtechnical founderです。

**あまり向いていない人:** model architectureの研究職を目指している人（deep-learning theory courseを探してください）、または2時間のprompt engineering crash courseを探している人。このprogramはその正反対です。

## 3. 最初の1時間：具体的な手順

今すぐ、次の順番で進めてください。必要になったところで詳しい説明に移動できます。

1. **リポジトリをコンピューターに置きます。**
   - 最も簡単な方法：GitHubページの緑色の **Code** ボタン → **Download ZIP** → `Documents/ai-engineering-lab` のような分かりやすい場所に解凍します。
   - より実践的な方法（Week 1で学びます）：[Git](https://git-scm.com/downloads)をインストールし、terminalで `git clone https://github.com/zorost/AI-Engineering-Lab.git` を実行します。
2. **全体像を眺めます。** [`curriculum/learning-path.md`](curriculum/learning-path.md) を開き、図を見ます。暗記ではなく、旅の形をつかむことが目的です。
3. **Week 1を開きます。** [日本語版Week 1](curriculum/week-01/README.ja.md) で、Python、VS Code、Jupyterを導入します。この3つが以降のlabを動かします。
4. **進捗trackerを用意します。** [`curriculum/tracking/ai-engineering-lab-24-week-tracker.xlsx`](curriculum/tracking/) をExcel、Google Sheets、またはLibreOfficeで開きます。名前と開始日を入力し、各taskを完了するたびにチェックします。
5. **毎週同じリズムで進めます。**

![Study、Build、Ship、Reflectの4つのbeat](assets/diagrams/lab-week.png)

   | Beat | いつ | やること |
   |---|---|---|
   | **Study** | 月〜火 | その週のREADMEとリンク先のknowledge-baseを読む |
   | **Build** | 水〜木 | 週のJupyter notebookを実行し、変更を加える |
   | **Ship** | 金 | ユースケース演習を終え、具体的な成果物を作る |
   | **Reflect** | 金〜日 | 10問quiz（8/10で合格）を受け、trackerを更新する |

6. **用語で迷ったら** [`reference/GLOSSARY.ja.md`](reference/GLOSSARY.ja.md) を調べます。プログラム中のtechnical termが平易な日本語で定義されています（[英語版](reference/GLOSSARY.md)もあります）。

これで準備は完了です。あとはWeek 1が、一つずつ小さなstepに分けて案内します。

## 4. 各パーツの関係（60秒のmental model）

- **`curriculum/`**: 24週間の本編。ここがmain pathで、ほかはこれを支えます。
- **`reference/knowledge-base/`**: 概念を整理した資料。各週から14ファイルのうち1つにリンクします。単独のreference libraryとしても読めます。
- **`reference/skills/`**: tool別の短いhow-to card（Claude Code、Cursor、Ollama、OpenRouterなど）。具体的なcommandが必要になったときに開きます。
- **`reference/agents/` と `reference/platforms/`**: Week 14〜24で使うdeep diveです。
- **`zoro/` + `data/`**: ZoroLogisticsのsynthetic-data toolkit。Week 1で使い方を学び、内部実装に触れる必要はありません。
- **`reference/skills/agent-skills/`**: AI *agent*（harnessが読み込むskill）に渡す、install可能な手順です。coding agentと開発し始めるWeek 12まで不要です。
- **`reference/resources/`**: Anthropic、Google、NVIDIA、Hugging Faceなどの無料courseを、補助になる週と対応付けたcatalogです。
- **`reference/GLOSSARY.ja.md`**: technical termの用語集（日本語版）です。英語版は `reference/GLOSSARY.md`。
- **`ROADMAP.md` / `CHANGELOG.md`**: programの今後と変更履歴です。

![リポジトリの構成と、最初に開く2つの場所](assets/diagrams/lab-map.png)

## 5. 学習を成立させる5つのルール

1. **すべてのnotebookを自分で実行する。** codeを読むだけではcodeを書く練習になりません。このprogramは「実行すること」自体がlessonになるように設計されています。読んだだけなら約10%、実行して意図的に壊したときに本来の学びが得られます。
2. **金曜日のuse caseは、見た目が悪くてもshipする。** score付きの未完成な成果物は、完璧なplanに勝ります。scoreが完了の根拠です。
3. **一度に1つだけ変える。** 動いた、または壊れた理由を、どの変更が生んだのか分かるようにします。toolよりも、この習慣こそがprogramの本当の学びです。
4. **30分以上止まったら、脱出ルートを使う。** 苦労は学習の一部ですが、何日もblockedのままにしないでください。
5. **trackerを正直に保つ。** future-youはこのdashboardをもとに判断します。「Done」はページを読んだことではなく、成果物をshipしたことです。

## 6. 詰まったときの脱出ルート（この順番）

1. **エラーメッセージを全文読み直します。** 最後の行が問題を、上の行が場所を示します。初心者は早く読み止めすぎます。
2. **その週の `exercises.md` を確認します。** 過去のlearnerが遭遇した失敗向けのヒントがあります。
3. **用語が分からない場合は [`reference/GLOSSARY.ja.md`](reference/GLOSSARY.ja.md) を検索します。**
4. **AI assistantにエラーの説明を頼みます。** 完全なtracebackを貼り、「Python初心者にも分かるように説明して」と聞いてください。Week 12以降はcoding agentを専門的に使いますが、最初から気軽に使って構いません。
5. **GitHub Issueを開きます。** 週番号、実行した内容、完全なerrorを記載してください。maintainerとほかのlearnerが確認します。

## 7. よくある質問

**実際にどれくらいかかりますか？**

設計上は週約10時間で24週間です。PythonとSQLを知っていればWeek 1〜2は早く進みます。週5時間しか取れなければ48週間かけても構いません。大切なのはcalendarよりcadenceです。

**GPUは必要ですか？**

Week 8までは不要です。その後も、core exerciseなら小さなmodelをCPUで動かせます。Week 8ではApple Silicon（Metal）、NVIDIA（CUDA）、時間単位のcloud GPU、free tierを扱い、download前に自分のhardwareで動くか予測するVRAM sizing methodを学びます。

**API keyにお金を払う必要はありますか？**

ありません。すべての必須exerciseに、local model（Ollama）、free-tier API（OpenRouterの `:free` model）、またはAPI不要の経路があります。有料optionが明らかに良い場合は、その週におおよそのcostをUSDで示します。

**先の週へ飛ばせますか？**

可能ですが、case studyは累積します。Week 9のquantization labはWeek 8のlocal modelを使い、Week 8のmodelはWeek 7のRAG botを、RAG botはWeek 1のdataを使います。飛ばした場合は後で埋め戻してください。経験のあるengineerはPhase 1の4つの金曜日use caseを実行してtestできます。すべて簡単ならWeek 5から始めても構いません。

**Andrew NgやDeepLearning.AIと関係がありますか？**

ありません。公開されたAI Engineering Skills Map frameworkを、公開資料とofficial vendor documentationから調査して独立に実装したprogramです（[`README.md`](README.md#the-framework-behind-the-program)参照）。すべての文章はZorost Intelligenceのoriginal workで、MIT licenseです。

**最後に何が得られますか？**

見せられるportfolioです。43個の実行済みnotebook、fine-tuned model、RAG agent、独自MCP serverを持つmulti-agent system、3つのcloud deployment、自分で作ったeval harness、governed Databricks lakehouse capstone、そして旅の進捗を示すtracker dashboardが残ります。

**リポジトリ内の何かが間違っている、または古くなっています。**

その可能性はあります。AI toolは速く変わるので、contributionの機会です。[`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) にissueやpull requestの方法があります。古いcommandを直すこと自体が学習の一部です。

---

© 2026 Zorost Intelligence LLC · [zorost.com](https://zorost.com)
