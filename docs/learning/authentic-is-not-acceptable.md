# Authentic is not acceptable

## 正規の署名でも拒否する場面

利用者は製品のreleaseを取得しました。署名は承認した鍵で検証でき、digestも来歴のsubjectと一致しています。
しかし来歴のソースは正規repositoryではなくforkで、build parameterにはレビューしていない機能の有効化が含まれています。
署名が保証するのは、その署名対象が認証できたことです。利用者が欲しかったreleaseであるかは、別の判断です。

この架空シナリオでは、利用者が事前に定めた正規repository・build type・parameterを照合すれば拒否できます。
逆に期待値を今回届いた来歴から自動生成すれば、想定外の値でも一致し、受入判断が循環します。

## 三つの判断を分ける

| 判断 | 問うこと | それだけでは分からないこと |
|---|---|---|
| 同一性 | 使うbytesは認証したsubjectと同じか | 署名者・内容の安全性 |
| 認証 | 利用者が信頼する主体の署名か | 自分たちが承認した生成条件か |
| 受入 | Builder・ソース・条件が期待値と合うか | 正規ソースに欠陥や悪意がないか |

同一性と認証を確認し、さらに期待値と一致しても、脆弱性検査やレビューは必要です。
「不正な署名」と「crypto toolが起動できない」は理由が異なりますが、どちらも自動使用を止めます。
判定不能を再試行するときも、署名不要の経路へ落とすのではなく、収集・検証機能を復旧します。

## Trust on first useの限界

最初に取得した値を基準にし、更新差分を監視する方式は初回の正当性を独立に保証しません。
採用するなら、初回承認とpolicy変更の責任者、差分の通知、許容範囲を明示します。
公開鍵と来歴を同じ侵害された配布先から取得し、その鍵を無条件で信頼する方式とは区別します。

[SLSA v1.2のverification仕様](https://slsa.dev/spec/v1.2/verifying-artifacts)を設計入力とし、上の架空シナリオはリポジトリでの解釈です。
[REF-PORTFOLIO-001](../../sources/README.md#ref-portfolio-001)では外部依存・platformからgovernanceへ期待値管理をつなぎます。
攻撃段階9から10の使用許可、12の拒否理由の調査へ責任を渡します。検証しただけで、本番admissionや対応を実装したとは扱いません。

- [Control](../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)
- [方式と確認方法](../../engineering/release-integrity/consumer-artifact-acceptance/README.md)
