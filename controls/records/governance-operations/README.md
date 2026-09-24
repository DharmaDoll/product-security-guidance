# Governance / Operations

担当者、例外、製品影響、初動、復旧を、文書の存在ではなく判断可能な状態として扱います。

| Control | 判断すること |
|---|---|
| [PSB-GOV-001 Supply-chain impact assessment](psb-gov-001-supply-chain-impact-assessment/README.md) | 既知の問題を含む依存から稼働製品を調べ、独立承認付きの対応計画へ渡す |
| [PSB-GOV-002 Security exception lifecycle](psb-gov-002-security-exception-lifecycle/README.md) | Security failureを消さず、限定したrisk acceptanceのscope・承認・期限を管理する |
| [PSB-GOV-003 Product vulnerability priority decision](psb-gov-003-vulnerability-priority-decision/README.md) | 適用性・severity・known exploitation・露出を分け、ownerと組織期限を持つpriorityへ変換する |
| [PSB-GOV-004 Credential exposure containment](psb-gov-004-credential-exposure-containment/README.md) | 漏えいした旧authorityと派生sessionを封じ込め、consumer移行・拒否確認・影響調査を経てclosureを判断する |
| [PSB-GOV-005 Deployed artifact recovery](psb-gov-005-deployed-artifact-recovery/README.md) | 影響artifactを別digestへ再構築・全対象へ置換し、旧digestが非稼働になるまでclosureを保留する |

PSIRT全体の組織能力、実際のprovider操作、incident全体の復旧完了は、この記録だけでは評価しません。
