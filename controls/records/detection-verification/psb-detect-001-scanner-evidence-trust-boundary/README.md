# PSB-DETECT-001 Scanner evidence trust boundary

## このcontrolを一枚で理解する

| 項目 | 内容 |
|---|---|
| セキュリティ上の問題 | どのtool・設定で何を調べたか不明な結果を信じると、侵害されたscannerや失敗した検査を「問題なし」と受け入れる。 |
| 誰から、または何から守るか | 配布経路や検出データの侵害、設定の差替え、timeout・解析障害、過大な除外、結果へのsecret複製、AI支援への判定の委譲。 |
| 何が対象か | Scannerと依存tool、検出データ・方針、対象範囲、実行状態、指摘、例外、保存する証拠。 |
| 何をするか | Tool・データ・方針と検査対象を特定し、検査完了・指摘・評価不能を分け、必要な結果だけを受入判断へ渡す。 |
| 成功状態 | 問題なしとした対象・条件・完了状態を説明でき、指摘や評価不能をそのままmerge・releaseの許可にしない。 |
| 対象外・残余リスク | 指摘なしは未知脆弱性、未検査対象、アプリの挙動、実行中の侵害を否定しない。実際の検査範囲と受入条件は別途確認する。 |

## 問いと適用範囲

「この結果は、何を、どのscanner・データ・設定で、どこまで正常に調べた結果か」に答えられるか。
依存関係、container image、IaC、secret、SBOM、workflow・Action定義などの検査へ適用します。一つのscannerが全カテゴリを扱う必要はありません。

## 必要なセキュリティ特性

| ID | 満たすべき状態 |
|---|---|
| SCAN-1 | 配布物と発行者を実行前に検証し、実際に使うbinary・imageのdigestを記録する。検証方式は配布元の方式に合わせる |
| SCAN-2 | 該当する検出データ、形式、方針・ルールの版と内容を結果へ結び、必要な鮮度を確認する |
| SCAN-3 | `CLEAN`、`FINDING`、`ERROR`を分け、timeout・取得不能・形式不正・識別不一致を問題なしにしない。終了コードだけで正常完了・指摘なしを決めず、指摘と解析失敗が同時にある場合は両方を残す |
| SCAN-4 | 対象の内容・版、収集範囲、除外、検出カテゴリを定め、対応する検査を完了する。対象不足・部分的な解析を問題なしにしない |
| SCAN-5 | 保存する結果からsecret、ソースの抜粋、不要な絶対pathやpayloadを除き、ルール・対象・判断は残す |
| SCAN-6 | Ignoreは特定のルール・対象へ限定し、GOV-002の独立承認・期限・失効・評価不能の扱いを使う |
| SCAN-7 | 二つ目のtoolは固有の検出・保証・修正支援と、追加の保守・侵害リスクを比較して採用する |
| SCAN-8 | AIの修正案や説明を許可・拒否の判断から分け、元の指摘と人のレビューで再確認する |

## 実装判断の羅針盤

Scannerの正常終了だけでは検査範囲が十分か判断できません。結果には対象、カテゴリ、除外範囲を含め、採用版と出力modeの意味を確認します。
検査できた範囲と見つかった指摘は別に保持します。一部で指摘が見つかっても、別の対象を解析できなければ検査全体を完了済みとはしません。評価不能として受入を止め、得られた指摘は調査へ残します。
Tool取得・データ更新を別の処理へ分け、通常の検査ではレビュー済み入力を読取り専用で使う方式を検討します。`offline` optionだけでは悪意あるbinaryの通信をOSで遮断したとは扱えません。

Scannerを追加する場合、固有の検出結果と保証を比較します。AIの説明は修正支援には使えますが、検査結果、例外承認、merge・release可否を決めません。

## 診断で確認する項目（異常時テスト）

設計レビュー・脆弱性診断のチェックリストです。実環境で確認した結果とは区別します。

| 確認すること | できてはいけないこと・見る結果 |
|---|---|
| Tool・検出データ・方針の差替え、古いデータ | 識別や必要な鮮度を確認せず、正式な結果として受け入れる |
| Timeout、取得失敗、不正な出力、未知の終了状態 | 指摘なしや空配列に置き換わる。評価不能として後段の許可を止めるか確認する |
| 対象なし、収集漏れ、一部の解析失敗、別revision | 完了した対象を示さず、予定した範囲全体を検査済みにする |
| 一部で指摘があり、別の対象は解析失敗 | `FINDING`だけで検査全体を完了済みにする、または`ERROR`だけを残して見つかった指摘を失う |
| 指摘があるのに出力処理は成功するmode | 終了コード0だけで指摘なしにする。指摘と受入条件が接続されているか確認する |
| 検査対象が設定・ignore・しきい値を変更する | 独立した承認や失効確認を通らず、検査や指摘を消せる |
| 生の結果、AIの説明、欠落した必須検査 | Secretを保存・転送する、AIだけで許可する、検査不足でも受入可能になる |

Workflowのjob・イベント・結果公開・必須checkの具体的な確認は[Workflow analysis gate and reporting](../../../../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md#診断で確認する項目異常時テスト)へ分けます。

## 例外との接続

`SCAN-6`は[Security exception lifecycle](../../governance-operations/psb-gov-002-security-exception-lifecycle/README.md)へ接続します。
Scanner側にはルール、対象、指摘の識別情報と、一時的に受け入れてよい理由の判断を残します。Scanner停止やDB取得失敗は指摘の例外ではなく`ERROR`です。

## 関連資料

- [教材: Zero findings is a scoped observation](learning.md)
- [設計pattern: Scanner acquisition and evidence boundary](../../../../engineering/detection-verification/scanner-acquisition-and-evidence-boundary/README.md)
- [設計pattern: Workflow analysis gate and reporting](../../../../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)
- [参照仕様と採否](../../../../sources/README.md#ref-scanner-evidence-001)
- [Workflow検査の参照仕様と採否](../../../../sources/README.md#ref-workflow-analysis-001)
- [Framework mapping](../../../../mappings/frameworks.yaml)：NIST SP 800-190 §4.1.1のイメージ脆弱性検査に使う証拠の範囲・状態を支える部分的な設計関係。旧SSDF `RV.1.1`・`PW.4.1`、OSPS `VM-06.02`、NIST SP 800-190 §4.4.1は[移行台帳](../../../../docs/MIGRATION.md)に非継承理由を記録
- [Exception consumer mapping](../../../../mappings/exception-consumers.yaml)

旧adapterとfixtureは移植していません。製品固有の実装は実効性を判断して選びます。現在の配布物、live DB、実際の検査範囲、CIでの強制は未確認です。
