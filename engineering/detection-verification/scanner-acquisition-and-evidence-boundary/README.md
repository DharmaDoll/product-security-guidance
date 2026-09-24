# Scanner acquisition and evidence boundary

`ENG-DETECT-001` / `detection-verification`

## 解く設計問題

セキュリティスキャナー自体も外部から取得する実行コードです。配布物の完全性、検出データの更新、実行の成否を別々に確認し、後続の許可・拒否判断へ渡す情報を定めます。

```text
reviewed scanner identity → integrity-verified executable
reviewed DB / policy identity → isolated scan of exact target
execution health + normalized findings → CLEAN | FINDING | ERROR
                                      → gate / exception decision
```

## 境界を分ける

取得処理は配布元へ接続し、チェックサム・署名・発行者を検証します。検出データの更新処理は、内容のダイジェスト、形式、作成時刻、有効期限を記録します。検査処理には対象の成果物と読取り専用の入力だけを渡し、リリース用の認証情報を持たせません。
出力の正規化では、製品固有の状態を`CLEAN`・`FINDING`・`ERROR`へ変換します。未知の状態や欠けた項目を`CLEAN`で補いません。後続の判断では、検出件数だけでなく、検査の正常完了と対象の一致を確認します。

## Scanner portfolio

ツールを追加する前に、共通のテスト対象で重複する検出と固有の検出を比較します。配布経路、通信先、必要な認証情報、更新頻度、出力の意味も判断材料にします。
修正支援ツールは検査結果の正本を置き換えず、元の検出結果へ辿れる説明を提供します。この設計ではAIによる説明を別の処理へ分け、許可・拒否の条件にしません。外部サービスへ送信する情報の分類と保存期間も確認します。

## Evidenceと例外

通常保存するのはツール・検出データ・方針・検査対象の識別情報と、検出カテゴリ、重大度、ルール、状態、時刻です。検出した秘密情報やソースの抜粋を長期保存用の証拠へ複製しません。
検出結果の例外は特定のルール・対象・成果物へ限定し、[共通の例外管理](../../governance-operations/security-exception-decision-boundary/README.md)を利用します。ツール、データ取得、出力解析、検査範囲の異常は、リスクを受容する例外ではなく`ERROR`です。

## 確認方法と限界

改ざんされた実行ファイル、期限切れの検出データ、方針の不一致、タイムアウト、不正な出力、秘密情報を含む生の結果、未知の終了コードを負のシナリオにします。
既知のテスト対象で検出できても、実環境の網羅性、データの最新性、未知脆弱性の不在、本番の状態は証明しません。旧Trivy 0.72.0とDockSec 2026.7.5のadapterは移植せず、採用時に現行仕様と配布物を再レビューします。

[Control](../../../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)、[教材](../../../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/learning.md)、[Sources](../../../sources/README.md#ref-scanner-evidence-001)を参照してください。
