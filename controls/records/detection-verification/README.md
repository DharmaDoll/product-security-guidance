# Detection / Verification

Security findingだけでなく、観測対象、検出器とデータのidentity、実行状態、証拠の安全性を確認します。

| Control | 判断すること |
|---|---|
| [PSB-DETECT-001 Scanner evidence trust boundary](psb-detect-001-scanner-evidence-trust-boundary/README.md) | Scannerが何を、どのtool・data・policyで、正常に調べた結果かを説明する |
| [PSB-DETECT-003 External attack surface reconciliation](psb-detect-003-external-attack-surface-reconciliation/README.md) | 外から見える候補を所有台帳と照合し、未登録・期待外・再出現を担当者へ渡す |

Findingなしは、宣言した対象・検出カテゴリ・時点に限定された結果です。未知脆弱性、未検査対象、本番runtimeの安全を意味しません。
外部候補が0件でも、選んだ収集元の正常な観測範囲に限った結果です。
