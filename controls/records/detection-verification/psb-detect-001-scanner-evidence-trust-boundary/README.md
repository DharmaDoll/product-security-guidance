# PSB-DETECT-001 Scanner evidence trust boundary

## このcontrolを一枚で理解する

| 項目 | 内容 |
|---|---|
| セキュリティ上の問題 | Scanner自体、database、policy、実行状態、対象範囲が不明な結果をsecurity gateが信頼すると、侵害されたtoolや失敗した検査をclean resultとして受け入れる。 |
| 誰から、または何から守るか | Scanner配布経路の侵害、database・policyの差替え、timeoutやparser障害、過大なignore、証拠へのsecret複製、AI補助への権限移譲から守る。 |
| 何が対象か | Scanner executableと依存tool、検出data・policy、検査対象とカテゴリ、実行状態、正規化したfinding、例外、保存証拠。 |
| 何をするか | Toolとdataを変更不能なidentityへ結び、宣言した対象を決定的に検査し、finding・clean・errorを分け、redacted evidenceをgateへ渡す。 |
| 成功状態 | Clean resultについて、対象・tool・data・policy・時刻・完了状態を説明でき、findingと評価不能はrelease permissionを生成しない。 |
| 対象外・残余リスク | Findingなしは未知脆弱性、検出対象外、application behavior、runtime侵害を否定しない。Live coverageと実gate導入は別途確認する。 |

## 問いと適用範囲

「この結果は、どのbytesを、どのscanner・data・policyで、どこまで正常に調べた結果か」に答えられるか。
Dependency、container image、IaC、secret、SBOMなどの決定的な検査へ適用します。一つのscannerが全カテゴリを扱う必要はありません。

## 必要なセキュリティ特性

| ID | 満たすべき状態 |
|---|---|
| SCAN-1 | Scanner release、配布artifact、publisher identityを実行前に検証し、実際に実行するbinary digestを記録する |
| SCAN-2 | Vulnerability DB、schema、policy・check bundleのexact identityと鮮度を結果へ結ぶ |
| SCAN-3 | `CLEAN`、`FINDING`、`ERROR`を分け、timeout・取得不能・形式不正・identity不一致をcleanにしない |
| SCAN-4 | 検査対象のartifact identity、対象範囲、検出カテゴリを宣言し、対応するdeterministic detectionを実行する |
| SCAN-5 | 保存証拠からmatched secret、snippet、不要な絶対pathやpayloadを除き、rule・target・decisionは残す |
| SCAN-6 | Ignoreはexact rule・targetへ限定し、GOV-002の独立承認・期限・失効・error semanticsを使用する |
| SCAN-7 | 二つ目のscannerやorchestratorは、固有の検出・保証・developer feedbackと追加riskを比較してから採用する |
| SCAN-8 | AI remediationや説明をauthoritative gateから分け、元のstructured findingと人のレビューで再確認する |

## 実装判断の羅針盤

Scannerの正常終了はcoverage十分を意味せず、finding 0件は検査対象が安全という証明でもありません。結果には対象artifact、カテゴリ、除外範囲を含めます。
Tool取得・DB更新をnetwork-enabled jobへ分け、通常scanではreview済み入力をread-onlyで利用する方式を検討します。ただし`offline` optionだけで悪意あるbinaryの通信をOS levelで遮断したとは扱いません。

Scannerを追加する場合、tool数ではなく固有の検出結果と独立保証を比較します。AIによる修正説明は開発者支援には使えますが、scan結果、exception承認、release可否を決めません。

## 例外との接続

`SCAN-6`は[Security exception lifecycle](../../governance-operations/psb-gov-002-security-exception-lifecycle/README.md)へ接続します。
Scanner側にはrule、target、finding identityと、そのfindingを一時的に受け入れてよい理由の判断を残します。Scanner停止やDB取得失敗はfinding例外ではなく`ERROR`であり、例外に自動変換しません。

## 関連資料

- [教材: Zero findings is a scoped observation](../../../../docs/learning/zero-findings-is-a-scoped-observation.md)
- [設計pattern: Scanner acquisition and evidence boundary](../../../../engineering/detection-verification/scanner-acquisition-and-evidence-boundary/README.md)
- [参照仕様と採否](../../../../sources/README.md#ref-scanner-evidence-001)
- [Framework mapping](../../../../mappings/frameworks.yaml)
- [Exception consumer mapping](../../../../mappings/exception-consumers.yaml)

旧Trivy・DockSec adapterとfixtureは実装候補として保留しました。この移行は現在の配布物、live DB、実際のcoverage、CI gateを検証していません。
