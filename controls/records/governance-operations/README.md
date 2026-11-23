# Governance / Operations

**インシデント・重大な脆弱性の対応中は、[プロダクトインシデント対応プレイブック](product_incident_response_playbook.md)を開いてください。** 当番の招集、暫定重要度の判断、封じ込め、顧客・当局への連絡、復旧確認と初報テンプレートをまとめています。

## 一つの脆弱性報告を追う

| Control | 判断すること |
|---|---|
| [PSB-GOV-006 Vulnerability report intake](psb-gov-006-vulnerability-report-intake/README.md) | 外部・社内からの脆弱性報告を安全に受け取り、取りこぼさず調査担当へ渡す |
| [PSB-GOV-003 Product vulnerability priority decision](psb-gov-003-vulnerability-priority-decision/README.md) | 脆弱性が自社製品に影響するかを調べ、担当者と対応期限を決める |
| [PSB-GOV-001 Supply-chain impact assessment](psb-gov-001-supply-chain-impact-assessment/README.md) | 問題のある依存が、どの製品・成果物・稼働環境に使われているか調べる |
| [PSB-GOV-007 Vulnerability advisory and notification](psb-gov-007-vulnerability-advisory-and-notification/README.md) | 影響する利用者が対象と取るべき行動を分かるように告知し、通知失敗と訂正を扱う |
| [PSB-GOV-008 Vulnerability remedy validation](psb-gov-008-vulnerability-remedy-validation/README.md) | 修正を主張する製品・版で問題が解消したか確かめ、検証した版の提供状態を分ける |
| [PSB-GOV-005 Deployed artifact recovery](psb-gov-005-deployed-artifact-recovery/README.md) | 影響する稼働成果物を置き換え、古い成果物がもう動いていないか確かめる |

## SOC：記録・検知・初動

| Control | 判断すること |
|---|---|
| [GOV-011 Security event evidence](psb-gov-011-security-event-evidence/README.md) | 不正操作と影響を調べられる記録を残し、欠測を見逃さない。 |
| [GOV-012 Detection and response readiness](psb-gov-012-detection-and-response-readiness/README.md) | 重要な異常を検知し、対応できる担当者の判断へつなぐ。 |
| [PSB-GOV-004 Credential exposure containment](psb-gov-004-credential-exposure-containment/README.md) | 認証情報が漏れた疑いがあるとき、古い権限を止め、使われた範囲を調べる |

複数領域にまたがる事案は[SOC向けの読み順](../../README.md#soc-reading-path)、ルールの検証・配備は[Detection Engineering](../../../engineering/detection-engineering-lifecycle.md)を参照してください。

## ランタイム保護：稼働中のワークロードを守る

| 確認したいこと | Container / Cloud / IaC のコントロール |
|---|---|
| コンテナの異常な実行やセンサー停止に気づけるか | [CONTAINER-004 Runtime threat detection](../container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md) |
| 侵害されたワークロードの権限や通信先をどこまで制限できるか | [CONTAINER-005 ワークロードの権限制限](../container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)・[CONTAINER-006 ネットワーク分離](../container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md) |

## 平時の運用：検査・公開資産・例外

| Control | 判断すること |
|---|---|
| [PSB-GOV-009 Scanner evidence trust boundary](psb-gov-009-scanner-evidence-trust-boundary/README.md) | 必要な対象を最後まで調べた、信頼できる検査結果か確かめる |
| [PSB-GOV-010 External attack surface reconciliation](psb-gov-010-external-attack-surface-reconciliation/README.md) | 管理から漏れた公開サービスを台帳と照合し、担当者へ渡す |
| [PSB-GOV-002 Security exception lifecycle](psb-gov-002-security-exception-lifecycle/README.md) | 一時的な例外は承認した対象と期限だけに効き、期限後は元の拒否へ戻る |
