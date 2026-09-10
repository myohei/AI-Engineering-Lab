# Week 05: 演習とChecklist

> **日本語版** · [英語版](exercises.md) · [Week 05 README](README.ja.md) · [クイズ](quiz.ja.md)

## Graded exercises

1. **Easy**: `01-tokenization-lab.ipynb` を別の価格pair（例：Mtokあたり `$0.50/$1.50`）で
   再実行し、新しい一日あたりcostを報告します。続いてsystem promptを8語に切り詰め、
   ドルのdeltaを示します。
2. **Standard**: token count比較に新しいtext型（JSON schema、法律条文、carrier契約書の
   一節）を追加します。そのchars/token比がproseと異なる理由を一文で書きます。
3. **Stretch**: `02-embeddings-and-attention-lab.ipynb` を拡張します。toy embeddingの
   次元を半分に割り、*二つの* attention headを並行に走らせます。両方の重み行列をprintし、
   headがどう違うかを記述します。torchは使いません。
4. **Portfolio**: `projects/token_budget.py` を書きます。text fileを読み、価格pairと
   target window sizeを受け取り、token count、cost、window使用率をprintするCLIです。
   小さなREADMEとともにcommitします。

## Hints

1. **Easy**: `estimate_cost` はそのまま使い、変わるのは二つの価格引数とsystem promptの
   文字列だけです。新しい数字だけでなく *delta* を報告します。
2. **Standard**: 句読点やcode調の記号が多いtext型（JSON schemaや法律条文）を選び、
   それをtokenizeしてchars/tokenをproseの行と比較してから、一文を書きます。
3. **Stretch**: embedding次元 `d` を `axis=-1` に沿って半分に割り、`Q1/K1/V1` と
   `Q2/K2/V2` にし、同じ `scaled_dot_product_attention` を二回呼んで出力をstackします。
   各headの重み行列が *どの* token関係を好むかを記述します。
4. **Portfolio**: file path、二つの価格、window sizeを `argparse` で受け取り、tokenは
   `len(enc.encode(text))`、使用率は `tokens / window` を使います。ドル金額は小数点以下
   4桁に丸めます。

## Checklist（manifest.jsonとExcel trackerに対応）

- [ ] Mon: tokenizationとembeddingsを学ぶ（knowledge-base 03）。
- [ ] Tue: Tokenizer lab。BPE encode/decodeと、LLM APIのtoken-cost estimator。
- [ ] Wed: Embeddings lab。shipment commodity descriptionに対するsimilarity search。
- [ ] Thu: Attention lab。NumPyでscaled dot-product attentionを実装。重みを可視化。
- [ ] Fri: Use case：context-window budget calculatorを構築（callあたりtoken数 vs window size）。
- [ ] Sat: Week 5 quiz（quiz.md）を受け、8/10で合格する。scoreをNotesに記録する。
- [ ] Milestone: Excel trackerを更新。両方のlabをcommitする。
