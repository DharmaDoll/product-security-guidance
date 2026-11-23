# Governance / Operations

**インシデント・重大な脆弱性の対応中は、[プロダクトインシデント対応プレイブック](product_incident_response_playbook.md)を開いてください。** 当番の招集、暫定重要度の判断、封じ込め、顧客・当局への連絡、復旧確認と初報テンプレートをまとめています。

## 一つの脆弱性報告を追う

| PSIRTが判断する場面 | 確認するコントロール |
|---|---|
| 報告が届いた | [GOV-006 受付](psb-gov-006-vulnerability-report-intake/README.md)で調査担当へ渡し、[GOV-003 優先度](psb-gov-003-vulnerability-priority-decision/README.md)で製品への影響・担当・期限を決める。依存が原因なら[GOV-001 依存の影響調査](psb-gov-001-supply-chain-impact-assessment/README.md)で対象製品と稼働先を絞る。 |
| 利用者に行動を求める | [GOV-007 告知・通知](psb-gov-007-vulnerability-advisory-and-notification/README.md)で対象者と伝達結果を確認する。回避策があれば修正前にも知らせる。 |
| 修正版ができた | [GOV-008 修正の検証](psb-gov-008-vulnerability-remedy-validation/README.md)で対象版の問題解消を確認し、[GOV-005 稼働成果物の復旧](psb-gov-005-deployed-artifact-recovery/README.md)で旧版が稼働先に残っていないか確認する。 |

## SOC：記録・検知・初動

- **何が起きたかを調べる**：[GOV-011 Security event evidence](psb-gov-011-security-event-evidence/README.md)で、操作と影響を追えるログ、欠けた期間や対象を確認する。
- **異常を当番の判断につなぐ**：[GOV-012 Detection and response readiness](psb-gov-012-detection-and-response-readiness/README.md)で、検知が機能し、対応できる担当者に届くことを確認する。
- **認証情報が漏れた疑いがある**：[GOV-004 Credential exposure containment](psb-gov-004-credential-exposure-containment/README.md)で、旧権限の失効と利用履歴を確認する。

複数領域にまたがる事案は[SOC向けの読み順](../../README.md#soc-reading-path)、ルールの検証・配備は[Detection Engineering](../../../engineering/detection-engineering-lifecycle.md)を参照してください。

## ランタイム保護：稼働中のワークロードを守る

| 確認したいこと | Container / Cloud / IaC のコントロール |
|---|---|
| コンテナの異常な実行やセンサー停止に気づけるか | [CONTAINER-004 Runtime threat detection](../container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md) |
| 侵害されたワークロードの権限や通信先をどこまで制限できるか | [CONTAINER-005 ワークロードの権限制限](../container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)・[CONTAINER-006 ネットワーク分離](../container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md) |

## 平時の運用：検査・公開資産・例外

- [GOV-009 Scanner evidence trust boundary](psb-gov-009-scanner-evidence-trust-boundary/README.md) — 「指摘なし」を採用する前に、検査対象・完了状態・結果の出所を確かめる。
- [GOV-010 External attack surface reconciliation](psb-gov-010-external-attack-surface-reconciliation/README.md) — 外から見えるサービスを台帳と照合し、未登録の公開面を担当者へ渡す。
- [GOV-002 Security exception lifecycle](psb-gov-002-security-exception-lifecycle/README.md) — 一時的な許可の対象と期限を絞り、期限後に元の制御へ戻す。
