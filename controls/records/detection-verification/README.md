# Detection / Verification

「指摘なし」と言える検査だったか、外から見えるサービスに見落としがないかを確認します。

| Control | 判断すること |
|---|---|
| [PSB-DETECT-001 Scanner evidence trust boundary](psb-detect-001-scanner-evidence-trust-boundary/README.md) | 「指摘なし」は信頼できるツールで必要な対象を最後まで調べた結果か確かめる |
| [PSB-DETECT-003 External attack surface reconciliation](psb-detect-003-external-attack-surface-reconciliation/README.md) | 外から見える候補を所有台帳と照合し、未登録・期待外・再出現を担当者へ渡す |

検査結果の「指摘なし」は、実際に調べた対象・項目・時点に限ります。外部サービスの候補が0件でも、収集に成功した範囲でしか言えません。詳しい確認条件は各controlから教材と設計パターンへ進んでください。
