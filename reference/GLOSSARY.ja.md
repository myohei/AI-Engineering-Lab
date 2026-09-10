# AI Engineering Lab: Glossary（用語集）

> **日本語版** · [英語版](GLOSSARY.md)
> プログラムで登場するすべての技術用語を、平易な言葉で説明する。用語はテーマ別のグループに分け、
> 通読できる順に並べてある。各グループ内では、後の用語の前提となる知識を前の用語が築いていく。
> 各エントリの末尾には、その用語を深く学べるプログラム内の位置を記す。
>
> **このファイルの使い方:** 最初から最後まで通読しないこと。ある週の教材に知らない単語が出てきたら、
> そこへジャンプして（エディタの検索が頼りになる）、1段落の定義を読んだら、作業に戻る。

**Part of AI Engineering Lab · Developed by [Zorost Intelligence AI Lab](https://zorost.com) · zorost.com**

---

## Foundations: softwareとdata

**API (Application Programming Interface)**: あるプログラムが、決められた契約に従って別のプログラムに
処理を依頼し、答えを受け取るための仕組み。「modelをcallする」とは、自分のコードがAPI requestを
送信しているということ。*Week 1; KB-01.*

**CLI (Command-Line Interface)**: ボタンをクリックする代わりに、terminalへコマンドを打ち込んで操作する
プログラム。AI engineeringのツール（git、Ollama、Claude Code）の多くはCLI。*Week 1.*

**Git / GitHub**: Gitはversion control（版管理）: ファイルへのすべての変更を記録し、undo・比較・共同作業を
可能にする。GitHubはgit repositoryをhostするwebsiteで、他の人が閲覧・コピーできる。このプログラム自体も
GitHub上にある。*Week 1.*

**IDE (Integrated Development Environment)**: 追加機能を備えたcode editor: file browser、terminal、
debugger、拡張機能が1つのウィンドウに揃う。このプログラムではVS Codeを使う。CursorはAI-native IDE。
*Week 1; skills/cursor.*

**Jupyter / notebook**: code cell、その出力、文章での解説を混ぜたinteractiveなdocument。このプログラムの
ハンズオンはすべてnotebook（`.ipynb`ファイル）で行われるため、cellを1つずつ実行して何が起きたか確認
できる。*Week 1.*

**Library / package**: 事前に書かれたコードで、ゼロから書かずにimportして使えるもの。`pandas`は
data library、`torch`はdeep-learning library。*Week 1.*

**Python**: AI engineeringのprogramming language。読みやすいsyntaxと、他に並ぶもののないAI/data
libraryのecosystemを持つことから選ばれた。Week 1でゼロから教える。

**Repository ("repo")**: gitが変更を追跡するcodeのフォルダ。このプログラム自体が1つのrepository。
*Week 1.*

**SQL (Structured Query Language)**: 表形式のdatabaseへ問い合わせるための言語:
`SELECT column FROM table WHERE condition`。AI engineeringはdataの上で動き、そのdataは今も
SQLでやり取りされる。*Week 2; KB-02.*

**Terminal / shell**: OSへ直接コマンドを打ち込むテキストのウィンドウ（macOSのTerminal、Windowsの
PowerShell/Windows Terminal）。*Week 1.*

**Virtual environment**: 1つのprojectのためだけに分離されたPython packageのフォルダ。あるprojectの
libraryバージョンが別のprojectを壊さないようにするためのもの。Week 1で1つ作ったら、あとは二度と
気にせず済む。*Week 1.*

## Machine learningとdeep learning

**Model**: 学習済みの数値（parameter）のファイルと、それを使うcodeの構造のセット。inputを与えると
output（ETA、category、次のtoken）を産出する。*Week 3.*

**Training**: modelのparameterが、例data上でのerrorを減らすように自動調整されるプロセス。trainingは
高くつき、学習済みmodelを使う方（inference）は安い。*Week 3 to 4; KB-02.*

**Inference**: 学習済みmodelを使って、新しいinputに対する予測を作ること。AI engineeringの大部分は
このinference側: prompting、serving、evaluating。*Week 3; KB-02.*

**Feature**: modelへ渡すinput変数: 距離、配送業者、曜日。**Feature engineering**は、modelが実際に
学習できるinputを作り込むこと。*Week 3;
Week 23.*

**Label / target**: training dataの中の正解列: 実際のETA、本当のon-time flag。modelは予測をlabelと
比べることで学習する。*Week 3.*

**Regression vs. classification**: regressionは数を予測し（時間単位のETA）、classificationはcategoryを
予測する（on-timeかdelayedか）。Week 3では両方を1つずつ作る。

**Train/test split**: training中にmodelが一切見ていないdataを脇に置いておき、*新しい* caseでの性能を
測ること。意味があるのはその性能だけ。*Week 3.*

**Overfitting**: modelがtraining dataのnoiseまで暗記してしまい、新しいdataでは性能が落ちること。
MLの中心的な失敗モードで、検出手段がtest split。*Week 3 to 4;
KB-02.*

**Neural network**: inputに学習済みのweightを掛け、非線形性へ通して渡す、単純なunitのlayerから成る
model。深さ（layerを多数重ねること）が複雑なpatternの学習を可能にする。*Week 4.*

**PyTorch**: 最も普及しているopen-sourceのdeep-learning framework。Week 4ではその上で小さな
neural networkを作り、あらゆるLLMの中の「deep learning」を魔法ではなくしていく。*Week 4.*

**Autograd / gradient descent**: trainingを成立させる数学: 各parameterがerrorにどう寄与したかを計算し
（gradient）、全parameterを少し下り坂へ動かす。PyTorchのautogradが微積分を代行してくれる。
*Week 4; KB-02.*

**Embedding**: 意味を表す密な数値vector。類似したもの同士がvector空間で近くに位置するようになる。
LLMの内部でも使われ、別の用途としてはsemantic searchを支える。*Week 5; KB-03.*

## LLM core

**LLM (Large Language Model)**: テキストの次のtokenを予測するようtrainingされた、非常に大きな
neural network。この単一の能力がscaleされると、要約、抽出、推論、対話が生まれる。*Week 5; KB-03.*

**Token**: modelが実際に読むテキストのかたまり。およそ英語1語の¾。cost、context上限、速度はすべて
tokenで測られる。*Week 5; KB-03.*

**Tokenizer**: テキストをtokenへ切り分け、それぞれを整数IDへ対応付けるcomponent。modelによって
tokenizeの仕方が異なるため、必ず実際のmodelのtokenizerで測ること。*Week 5.*

**Transformer**: 現代のすべてのLLMの基盤となるneural architecture: blockを積み重ねた構造で、各blockは
self-attention（token同士が互いから情報を集める）と小さなfeed-forward networkを組み合わせる。
*Week 5; KB-03.*

**Attention / self-attention**: 各tokenが、自分にとってどのtokenが重要かを重み付けする仕組み（文中の
「it」が自分の名詞へ遡って注目する、のように）。Q·K·V projectionの動きはWeek 5で視覚的に解説される。
*Week 5; KB-03.*

**Context window**: modelが一度に考慮できるtoken数の上限: あなたの指示、会話、retrieveされたdocument、
model自身の出力が、すべてこの枠を取り合う。これを管理するのが*context engineering*。*Week 6; KB-04.*

**KV cache**: 各tokenのkey/value vectorを保存しておくserving最適化。生成のたびにprompt全体の
attentionを再計算しなくて済む。最初のtokenが遅く、残りが速くstreamされる理由。*Week 5; KB-03.*

**Temperature**: samplingのダイヤル: 低いtemperatureほどoutputが予測しやすくなり（最も確率の高い
tokenを選ぶ）、高いtemperatureほど多様になる。extraction taskはゼロ近くで動かす。*Week 5 to 6.*

**Hallucination**: modelが、完全な自信とともに偽りのことを述べること。modelの仕事はもっともらしい
テキストを生成することであって、検証済みの事実ではないため。engineering上の答えはretrieval（事実を
与える）、structured output、evals。*Week 6 to 7; KB-03.*

**Prompt**: modelの前に置くすべてのもの: system指示、例、userの依頼、retrieveした根拠。*Week 6.*

**System prompt**: 毎回のrequestに付けて送る恒常的な指示: role、policy、output形式、guardrail。
policy layerであって、security layerではない。*Week 6; KB-04.*

**Few-shot prompting**: promptに1〜3個の完成したinput→output例を含め、modelにその*pattern*を
なぞらせること。並の例3つより、良い例1つが勝る。*Week 6.*

**Chain-of-thought**: 答える前にstep by stepで考えるようmodelに求めること。多段階の問題に効く一方、
毎回のcallでtokenを消費する。*Week 6; KB-04.*

**Structured output**: modelの答えをschema（通常はJSON）へ制約し、人間ではなくcodeが消費できるように
すること。忘れずに: schemaは形を制約するだけで、真実は決して保証しない。*Week 6; KB-04.*

**Prompt injection**: *systemが読むcontent*（web page、documentのfield）に隠された指示がmodelを
乗っ取る攻撃。OWASPのLLM risk第1位。防御はpromptの外側に置く。*Week 6; KB-04.*

**Prompt caching**: 繰り返されるrequestの処理済みprefixを再利用するprovider機能。system promptと
contextが安定していれば、costとlatencyを削減できる。*Week 6; KB-04.*

**RAG (Retrieval-Augmented Generation)**: 関連documentをretrieveし、context windowへ入れ、
*そこから* citation付きで答えるようmodelへ求めること。hallucinationと古い知識に対する定番の
治療法。*Week 7; KB-05.*

**Vector database**: embedding vectorを保存し、query vectorへの近傍を高速に探すdatabase。RAGの
retrieval側の半分。*Week 7; KB-05.*

**Chunking**: documentを、embedして有用にretrieveできる大きさへ切り分けること。chunk sizeとoverlapは、
RAGの諸判断の中でも最も効き目の大きい部類に入る。*Week 7.*

**Reranking**: vector searchの上位候補を、真の関連性で並べ替える第二段階のmodel。RAG pipelineにとっての
安上がりな精度。*Week 7; KB-05.*

**Knowledge graph**: entityとrelationshipの形で蓄えたdata（shipment、*carried_by*→carrier）。
vector searchでは答えられないmulti-hopの質問を可能にする。Week 7で1つ作る。

## Model engineering

**Open-weight model**: parameterファイルをdownloadして自分で実行できるmodel（Llama、Qwen、Mistral、
DeepSeek…）。通例「open source」と呼ばれるが、licenseはさまざまだ。*Week 8; KB-06.*

**Foundation model**: 広範なdataでtrainingされた大きなmodel。ゼロからtrainingする代わりに、prompting、
RAG、fine-tuningでtaskへ適応して使う。*Week 8; KB-06.*

**Ollama / llama.cpp / MLX**: このプログラムが使う3つのlocal-inference stack: 手軽さのOllama、制御と
GGUFのllama.cpp、Apple Silicon向けのMLX。*Week 8;
skills/ollama-llamacpp; KB-08.*

**GGUF**: llama.cppがquantize済みmodelに使うfile形式。1つのファイルをdownloadして、どこでも実行
できる。*Week 8 to 9.*

**Quantization**: modelのweightを低精度（16-bit → 8/6/5/4-bit）で保存し、memoryを減らしてinferenceを
速くすること。代償のquality低下は小さい。Q4_K_Mが定番のsweet spot。*Week 9; KB-06.*

**VRAM**: GPU memory。local modelにとっての硬い壁: modelのweight、KV cache、runtimeのすべてが
収まらなければならない。Week 8〜9では、downloadする前に必要量を見積もることを学ぶ。

**vLLM**: LLM向けの高スループットなopen-source serving engine（paged attention、continuous
batching）。userが1人から50人になったときの行き先。*Week 9; KB-08.*

**Fine-tuning**: 自分のdataでmodelのtrainingを続け、振る舞いを変えること: tone、format、domain語彙。
*Week 10; KB-06.*

**SFT (Supervised Fine-Tuning)**: input→理想的なoutput例によるfine-tuning。振る舞い変更の最初の段。
*Week 10.*

**LoRA (Low-Rank Adaptation)**: 全parameterの代わりに、追加した小さな行列の集まりだけをfine-tuning
する方法: 安く、速く、出来上がる「adapter」ファイルはごく小さい。*Week 10; KB-06.*

**DPO (Direct Preference Optimization)**: 「良い答え vs 悪い答え」のpairでtrainingし、独立した
reward modelなしに振る舞いをpreferenceへ揃えること。*Week 10.*

**Distillation**: 小さいmodelが大きいmodelの出力を模倣するようtrainingすること。capabilityと引き換えに
速度とcostを得る。*KB-06.*

**Eval (evaluation)**: 固定されたcase群に対するmodelやsystemのqualityの、再現可能な測定。*score*を
産出する。AI engineerとdemo builderを分かつ規律。*Week 11; KB-07.*

**Golden set**: evalが採点の基準にする、正解つきinputのcuratedな集合。promptに手を付ける前に、まず
golden setを直すこと。*Week 6, 11.*

**LLM-as-judge**: 正しさが曖昧なとき（要約、回答）、強いmodelに別systemの出力をrubricに照らして採点
させること。安くscalableだが、人間の採点に対するcalibrationが必須。*Week 11; KB-07.*

**Error analysis**: 実際の失敗を手で読み、categoryへclusterし、最大のcategoryから直すこと。この
プログラムで最もROIの高い習慣。*Week 11;
KB-07.*

## Harnesses・loops・agents

**Harness (coding-agent harness)**: LLMがあなたのコンピュータで行動できるようにするsoftware wrapper:
fileの読み取り、command実行、code編集。その周りにpermission、rules file、context管理が備わる。
このプログラムが比較する4つは、Claude Code、Cursor、OpenCode、DeepSeek Harness。
*Week 12; KB-09; reference/skills*

**Rules file**: harnessが毎セッション読む、永続する指示ファイル（`CLAUDE.md`、`AGENTS.md`、
`.cursor/rules`）: projectの規約、command、境界。*Week 12; reference/skills*

**Subagent**: 独自のcontext windowを持つ、spawnされたhelper agent。狭い仕事（research、review）を
任せることで、main agentのwindowを綺麗に保つ。*Week 12; KB-09.*

**Verifier**: agentの仕事を自動で検査するものすべて: test、linter、type check、eval。loopを閉じるとは、
agentが自分でverifierを実行することを指す。*Week 13.*

**Spec-driven development**: 先にspecificationを書き、agentをそこへ向けて誘導すること。qualityを、
その場の感覚ではなく明示的なcontractに対して判定できるようになる。*Week 13;
KB-01.*

**Agent**: toolを備えたmodelがloopに入ったもの: 観察 → 思考 → 行動 → 観察…を、完了するか止まるまで
続ける。stepが事前に分からないtaskをagentが扱う。*Week 14; KB-10.*

**ReAct**: agent patternの原型: 1つのloopの中で*reasoning*（「次に何をすべきか？」）と*action*
（tool call）を交互に織り交ぜる。Week 14でゼロから1つ作る。

**Tool (function calling)**: modelがharnessへ実行を頼めるfunction: `track_shipment(id)`。modelは
構造化されたintentを出し、あなたのcodeがそれを実行して結果を返す。*Week 14; KB-10.*

**Guardrails**: agentの周りの硬い制限: 最大step数、cost上限、refusal rule、取り返しのつかない行動に
対する人間の承認。*Week 14; KB-10.*

**Trace / observability**: agentがたどった全step — prompt、tool call、output、cost — の記録log。
それにより失敗をdebugでき、evalできるようになる。*Week 17; KB-07, KB-10.*

**LangGraph**: agentを明示的なstate graphとしてmodel化するframework: node（step）、edge（遷移）、
checkpoint（resumability）。*Week 15; KB-10.*

**Multi-agent system**: 仕事を、orchestratorが調整する専門化されたagent群（router、tracker、refunds）へ
分割すること。測って選ぶtradeであって、defaultではない。*Week 16;
KB-10.*

**MCP (Model Context Protocol)**: toolとdataをAI agentへ公開するためのopen standard: 1つのserverで、
多数の互換clientに対応する。Week 16ではZoroLogistics向けのMCP serverを1つ作る。*Week 16; KB-11.*

**A2A (Agent-to-Agent)**: 境界を越えて他のagentへtaskを委譲するためのGoogleのprotocol。agent対toolに
焦点を当てるMCPを補完する。*KB-11.*

**OpenClaw**: このプログラムがWeek 17で使うopen-sourceのpersonal-agent framework。Week-16のMCP
serverへ接続した24時間365日のassistantを動かす。*Week 17; agents/openclaw.*

**Router / OpenRouter**: 何百ものmodelを1つのAPI keyの後ろに並べるservice。modelの入れ替え、
cost/qualityの比較、`:free` variantの利用が可能になる。*Week 12;
skills/openrouter.*

## Cloud platforms・Databricks

**Azure AI Foundry**: AI appとagentの構築、評価、deployのためのMicrosoftのplatform。model catalogと
enterprise governanceを備える。*Week 18; KB-12.*

**Google Vertex AI**: Google CloudのML/GenAI platform: Gemini model、Agent Builder、evaluation
service、MLOps。*Week 19; KB-12.*

**AWS Bedrock**: foundation model（Claude、Llama、Nova…）を1つのAPIで提供するAmazonのmanaged
service。加えて、Knowledge Bases、Agents、Guardrailsも備える。*Week 20; KB-12.*

**Serverless endpoint**: requestごとに支払い、serverの管理を一切しないmodel hosting。自分でGPU
instanceをprovisionすることの対極。*Week 18 to 20.*

**Lakehouse**: data lakeの安価なopen storageと、data warehouseの信頼性・SQL性能を組み合わせたdata
platform。Databricksの中心的なidea。*Week 21; KB-13.*

**Delta Lake**: lakehouseの土台となるopen storage layer（object storage上のtableに、ACID transaction、
time travel、schema enforcementを与える）。*Week 21.*

**Unity Catalog**: Databricksのgovernance layer: data、model、permissionの管理をlineage付きで
1か所にまとめる。*Week 21; platforms/databricks/01.*

**Medallion architecture**: dataをbronze（raw）→ silver（cleaned）→ gold（business-ready）のtableへ
整理すること。*Week 21 to 22.*

**PySpark**: Apache Spark — cluster全体でdataを処理する分散compute engine — のPython API。
*Week 22.*

**Lakeflow (DLT & Jobs)**: Databricksのdeclarative pipelineとorchestration tool: tableを宣言すれば、
依存関係、retry、monitoringは任せっぱなしでよい。*Week 22.*

**MLflow**: open-sourceの実験tracking・model registry system: 毎回のtraining runをparameter、
metric、artifact付きでlogする。*Week 23.*

**Feature store**: 計算済みfeatureのgovernedな置き場。trainingとservingが同一の定義を使えるように
する。*Week 23.*

**Model serving**: modelを、applicationがcallするendpointの後ろへ置くこと。Databricks Model Serving、
Foundry endpoint、Vertex endpointがそのmanaged版。*Week 23; KB-12.*

**Vector Search / AI Search**: RAGのためのDatabricksのmanaged vector databaseで、Unity Catalogの
governance下にある。*Week 23.*

**Genie**: governed dataの上に立つ、Databricksのnatural-language interface: 英語で尋ねると、governedな
SQLの答えが返る。*Week 23.*

**Agent Bricks**: platform上のdataでagentを構築・評価するためのDatabricksのtool。*Week 23 to 24.*

**DABs (Databricks Asset Bundles)**: Databricks向けのinfrastructure-as-code: project全体 — job、
pipeline、endpoint — をYAMLで宣言し、1コマンドでdeployする。*Week 24.*

**CI/CD (Continuous Integration / Continuous Deployment)**: 変更のたびにcodeを自動でtestしてdeploy
すること。本番が手作業の賭けにならないために。*Week 24.*

**FinOps**: cloud/AI支出を測定して制御する規律: budget、alert、cost-per-query dashboard。
*Week 24; platforms/databricks/17.*

**Governance**: dataとAIを大規模に*安全に*使えるようにする管理: permission、lineage、audit、
quality rule。Week 21〜24を貫く1本の糸。

---

*用語が足りない？ それはbugです。issueをopenするか、追加してください
（[`.github/CONTRIBUTING.md`](../.github/CONTRIBUTING.md) を参照）。*

© 2026 Zorost Intelligence LLC · [zorost.com](https://zorost.com)
