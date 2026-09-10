# AI Engineering Lab: 24週間AI Engineering Program

> **日本語版** · [英語版](README.md) · [ルートの日本語ガイド](../README.ja.md)
>
> **Find the Signal. Act with Intelligence.** · [Zorost Intelligence AI Lab](https://zorost.com)が開発

AI Engineering Labの本編です。Pythonの基礎からproduction lakehouse AIまでを、週単位で進む24週間のpathとして学びます。各週には **section**（phase）、**category**（skill area）、継続するZoroLogistics case studyの **use case**、実行可能な **notebook**、Excel trackerに記録する **checklist** があります。

![FoundationsからDatabricks capstoneまでの7つのphaseと、各phaseで作るもの](../assets/diagrams/lab-journey.png)

> **初めての方へ:** まず [`START-HERE.ja.md`](../START-HERE.ja.md) を読み、[`reference/GLOSSARY.md`](../reference/GLOSSARY.md) を1つのtabで開いておいてください。technical termは現在、英語の用語集で定義されています。Week 1の日本語ガイドでは重要語を日本語でも説明します。

## プログラムの進め方

![Study、Build、Ship、Reflectの4つのbeatで構成する1週間](../assets/diagrams/lab-week.png)

1. **1つのcase studyを24週間使います。** 架空の運送会社 **ZoroLogistics** のAI engineering teamとして進めます。Week 1のdata、model、agentをWeek 24まで再利用・改善・production化します。卒業時には24個の無関係なdemoではなく、つながったportfolioができます。
2. **Weekly cadence（週約10時間）:**
   - **月〜火 · Study:** その週のREADMEと、リンクされているknowledge-baseを読む。
   - **水〜木 · Build:** notebookを実行し、変更・拡張する。
   - **金 · Use case:** use-case exerciseを完成させ、具体的な成果物をshipする。
   - **金〜日 · Reflect & check off:** Excel trackerを更新し、自分のforkへpushする。
3. **どこでもevalを行います。** Week 3以降、すべてのAI成果物にはscore（metricまたはeval）とerror-analysis noteを付けます。これがAI engineeringの中心的な習慣です。
4. **local-first、cloud-laterです。** Week 1〜13はlaptopで進めます（GPUはWeek 8まで不要で、その後も小さなmodelならCPUで動きます）。Week 18〜24は主要cloudのfree/limited tierを使います。

## 前提条件

- いずれかのprogramming languageに慣れていること（Pythonはゼロから説明します）
- Gitの基本（Week 1で復習します）
- laptop（RAM 16 GB推奨。Week 8以降はApple SiliconまたはNVIDIA GPUがあると便利です）
- 任意のaccount（各週で作成）：GitHub、Hugging Face、任意のmodel API key、Azure / Google Cloud / AWS / Databricksのfree tier

## 24週間の一覧

| Week | Week title | Section | Category |
|---|---|---|---|
| 1 | Python Foundations & the AI Engineering Landscape | Foundations | Python & Environment |
| 2 | Data Engineering & SQL for AI | Foundations | Data & SQL |
| 3 | Machine Learning Fundamentals | Foundations | Classical ML |
| 4 | Deep Learning with PyTorch | Foundations | Deep Learning |
| 5 | How LLMs Work: Tokens to Transformers | LLM Core | LLM Internals |
| 6 | Prompt Engineering & the Context Window | LLM Core | Prompt & Context |
| 7 | RAG, Vector Search & Knowledge Graphs | LLM Core | Retrieval & Graphs |
| 8 | Open Models & Local Inference: GPUs, Ollama, llama.cpp | LLM Core | Local Models & GPUs |
| 9 | Quantization & Efficient Inference | Model Engineering | Quantization & Serving |
| 10 | Fine-Tuning: LoRA, SFT & DPO | Model Engineering | Fine-tuning |
| 11 | Evals & Error Analysis for AI Systems | Model Engineering | Evaluation |
| 12 | Coding-Agent Harnesses: Claude Code, Cursor, OpenCode, DSH | Harnesses & Loops | Harnesses |
| 13 | Agentic Coding Loops & Spec-Driven Development | Harnesses & Loops | Loops & Specs |
| 14 | Agent Fundamentals: The Loop, Tools & Memory | Agents | Agent Core |
| 15 | Agent Frameworks: LangGraph & the State-Graph Model | Agents | Frameworks |
| 16 | Multi-Agent Systems & MCP | Agents | Multi-Agent & Protocols |
| 17 | OpenClaw, Hermes & Agent Operations | Agents | Personal Agents & Ops |
| 18 | Azure AI Foundry | Cloud AI Platforms | Microsoft |
| 19 | Google Vertex AI & Gemini | Cloud AI Platforms | Google |
| 20 | AWS Bedrock & SageMaker AI | Cloud AI Platforms | AWS |
| 21 | Databricks Day Zero: Unity Catalog & the Lakehouse | Databricks Zero to Hero | Platform & Data |
| 22 | Databricks Data Engineering: PySpark, Streaming & Lakeflow | Databricks Zero to Hero | Pipelines |
| 23 | Databricks ML & GenAI: Training, Serving, Genie | Databricks Zero to Hero | ML & GenAI |
| 24 | Databricks Production: DABs, Governance & the Capstone | Databricks Zero to Hero | Production & Capstone |

Week 1〜24の日本語版を用意しています。Week 1: [`README.ja.md`](week-01/README.ja.md)・[`exercises.ja.md`](week-01/exercises.ja.md)・[`quiz.ja.md`](week-01/quiz.ja.md)（Notebookも日本語のMarkdownセル版）。

Week 2〜24の日本語版（Notebook本体は英語版を使用します）:

| Week | README | 演習 | クイズ |
|---|---|---|---|
| 2 | [AIのためのData EngineeringとSQL](week-02/README.ja.md) | [演習](week-02/exercises.ja.md) | [クイズ](week-02/quiz.ja.md) |
| 3 | [Machine Learningの基礎](week-03/README.ja.md) | [演習](week-03/exercises.ja.md) | [クイズ](week-03/quiz.ja.md) |
| 4 | [PyTorchで学ぶDeep Learning](week-04/README.ja.md) | [演習](week-04/exercises.ja.md) | [クイズ](week-04/quiz.ja.md) |
| 5 | [LLMsの仕組み——TokenからTransformerまで](week-05/README.ja.md) | [演習](week-05/exercises.ja.md) | [クイズ](week-05/quiz.ja.md) |
| 6 | [Prompt EngineeringとContext Window](week-06/README.ja.md) | [演習](week-06/exercises.ja.md) | [クイズ](week-06/quiz.ja.md) |
| 7 | [RAG、Vector SearchとKnowledge Graph](week-07/README.ja.md) | [演習](week-07/exercises.ja.md) | [クイズ](week-07/quiz.ja.md) |
| 8 | [Open ModelsとLocal Inference — GPUs、Ollama、llama.cpp](week-08/README.ja.md) | [演習](week-08/exercises.ja.md) | [クイズ](week-08/quiz.ja.md) |
| 9 | [QuantizationとEfficient Inference](week-09/README.ja.md) | [演習](week-09/exercises.ja.md) | [クイズ](week-09/quiz.ja.md) |
| 10 | [Fine-Tuning — LoRA、SFTとDPO](week-10/README.ja.md) | [演習](week-10/exercises.ja.md) | [クイズ](week-10/quiz.ja.md) |
| 11 | [AI SystemのためのEvalとError Analysis](week-11/README.ja.md) | [演習](week-11/exercises.ja.md) | [クイズ](week-11/quiz.ja.md) |
| 12 | [Coding-Agent Harnesses — Claude Code、Cursor、OpenCode、DSH](week-12/README.ja.md) | [演習](week-12/exercises.ja.md) | [クイズ](week-12/quiz.ja.md) |
| 13 | [Agentic Coding LoopとSpec-Driven Development](week-13/README.ja.md) | [演習](week-13/exercises.ja.md) | [クイズ](week-13/quiz.ja.md) |
| 14 | [Agentの基礎 — Loop、Tools & Memory](week-14/README.ja.md) | [演習](week-14/exercises.ja.md) | [クイズ](week-14/quiz.ja.md) |
| 15 | [Agent Frameworks — LangGraphとState-Graph Model](week-15/README.ja.md) | [演習](week-15/exercises.ja.md) | [クイズ](week-15/quiz.ja.md) |
| 16 | [Multi-Agent SystemとMCP](week-16/README.ja.md) | [演習](week-16/exercises.ja.md) | [クイズ](week-16/quiz.ja.md) |
| 17 | [OpenClaw、HermesとAgent Operations](week-17/README.ja.md) | [演習](week-17/exercises.ja.md) | [クイズ](week-17/quiz.ja.md) |
| 18 | [Azure AI Foundry](week-18/README.ja.md) | [演習](week-18/exercises.ja.md) | [クイズ](week-18/quiz.ja.md) |
| 19 | [Google Vertex AIとGemini](week-19/README.ja.md) | [演習](week-19/exercises.ja.md) | [クイズ](week-19/quiz.ja.md) |
| 20 | [AWS BedrockとSageMaker AI](week-20/README.ja.md) | [演習](week-20/exercises.ja.md) | [クイズ](week-20/quiz.ja.md) |
| 21 | [Databricks Day Zero: Unity Catalogとlakehouse](week-21/README.ja.md) | [演習](week-21/exercises.ja.md) | [クイズ](week-21/quiz.ja.md) |
| 22 | [Databricks Data Engineering: PySpark、StreamingとLakeflow](week-22/README.ja.md) | [演習](week-22/exercises.ja.md) | [クイズ](week-22/quiz.ja.md) |
| 23 | [Databricks ML & GenAI: Training、Serving、Genie](week-23/README.ja.md) | [演習](week-23/exercises.ja.md) | [クイズ](week-23/quiz.ja.md) |
| 24 | [Databricks Production: DABs、GovernanceとCapstone](week-24/README.ja.md) | [演習](week-24/exercises.ja.md) | [クイズ](week-24/quiz.ja.md) |

各週のフォルダー（`curriculum/week-NN/`）は、1つのcomplete lessonです。

```
week-NN/
├── README.md        # lesson：problem → deep concepts（table、diagram、例、pitfall、glossary）
│                    # → notebook walkthrough → use case → sources
├── notebooks/       # 1〜3個の実行可能なJupyter notebook（Python / SQL / PySpark）
├── exercises.md     # graded exercise、hint、その週のchecklist
└── quiz.md          # 10問のself-check（8問正解で合格）
```

## Phase

### Phase 1 · Foundations（Week 1〜4）

Python、data engineering、classical ML、deep learningを、AI engineeringの方法で学びます。すべてのmodelにmetric、split、error analysisを付けます。Week 1では、以降ずっと再利用するZoroLogistics synthetic-data generatorを作ります。

### Phase 2 · LLM Core（Week 5〜8）

LLMの仕組みを、tokenとembeddingからattention、KV cacheまで学びます。その上にある2つのengineering superpower、**prompt/context-window engineering** と **retrieval（RAG + knowledge graph）** を扱います。Week 8ではlocalへ進み、open model、Ollama / llama.cpp / MLX、CUDAからApple MetalまでのGPU setupを行います。

### Phase 3 · Model Engineering（Week 9〜11）

modelを安く、自分の用途に合わせます。quantization formatとserving engine、LoRA/SFT/DPOによるfine-tuning、そしてすべてを判断するevalとerror analysis（Ngがagentをどれだけ速くshipできるかを左右する最大の要素）を学びます。

### Phase 4 · Harnesses & Loops（Week 12〜13）

coding agentを使いこなします。Claude Code、Cursor、OpenCode、DeepSeek Harnessを設定・操作し、managed context、rules file、subagent、3つのloop（agentic coding → developer feedback → external feedback）を、spec、verifier、blast-radius ruleとともに学びます。

### Phase 5 · Agents（Week 14〜17）

手書きのReAct loopからLangGraph state graph、multi-agent orchestration、MCPへ進みます。Week 17ではOpenClawをpersonal lab assistantとして動かし、Hermes系のopen modelをagent brainに使い、tracing、eval、costのops layerを加えます。

### Phase 6 · Cloud AI Platforms（Week 18〜20）

同じZoroLogistics support agentを3通りでdeployします。Azure AI Foundry（Microsoft）、Vertex AI + AI Studio（Google）、Bedrock + SageMaker（AWS）を比較し、capability、governance、costを見て選び方を学びます。

### Phase 7 · Databricks Zero to Hero（Week 21〜24）

Zorost Databricks modernization playbookを一通り実行します。Unity Catalog、Delta Lake medallion、DBSQL、PySpark、streaming、Lakeflow Pipelines & Jobs、MLflow、feature engineering、Databricks Model Training、Model Serving + Unity AI Gateway、AI Search（Vector Search）、AI functions、Genie、Agent Bricksを扱い、その後DABs、CI/CD、governance、FinOpsへ進みます。最後は **ZoroLogistics Lakehouse Intelligence** capstoneです。

## 進捗管理

`tracking/ai-engineering-lab-24-week-tracker.xlsx` をdownloadし、Excel、Google Sheets、またはLibreOfficeで開きます。次の内容が入っています。

- **Dashboard** sheet：名前、開始日、週ごとのcompletion bar、24週間のprogress chart
- **週ごとのsheet**：status dropdown（☐ Not started · ▶ In progress · ✅ Done · ⏭ Skipped）、週ごとのcompletion percentage、Notes column付きchecklist

このworkbookは `manifest.json` から生成されます。詳しくは [`tracking/README.md`](tracking/README.md) を参照してください。

## 修了時にできること

24週（Week 24 capstoneを含む）を終えると、次の成果物が残ります。

- 43個の実行済みnotebook（Python、SQL、PySpark）
- portfolio：fine-tuned model、RAG agent、multi-agent system、MCP server、3つのcloud deployment、governed Databricks lakehouse
- 自分で構築したeval harness。これがAI engineerとdemo builderを分ける成果物です。

forkとtracker dashboardをmentor、team、または[Zorost Intelligence](https://zorost.com)と共有できます。

---
© 2026 Zorost Intelligence LLC · https://zorost.com
