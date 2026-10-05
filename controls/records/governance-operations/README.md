# Governance / Operations

担当者、例外、製品影響、初動、復旧を、文書の存在ではなく判断可能な状態として扱います。

| Control | 判断すること |
|---|---|
| [PSB-GOV-001 Supply-chain impact assessment](psb-gov-001-supply-chain-impact-assessment/README.md) | 既知の問題を含む依存から稼働製品を調べ、独立承認付きの対応計画へ渡す |
| [PSB-GOV-002 Security exception lifecycle](psb-gov-002-security-exception-lifecycle/README.md) | Security failureを消さず、限定したrisk acceptanceのscope・承認・期限を管理する |
| [PSB-GOV-003 Product vulnerability priority decision](psb-gov-003-vulnerability-priority-decision/README.md) | 適用性・severity・known exploitation・露出を分け、ownerと組織期限を持つpriorityへ変換する |
| [PSB-GOV-004 Credential exposure containment](psb-gov-004-credential-exposure-containment/README.md) | 漏えいした旧authorityと派生sessionを封じ込め、consumer移行・拒否確認・影響調査を経てclosureを判断する |
| [PSB-GOV-005 Deployed artifact recovery](psb-gov-005-deployed-artifact-recovery/README.md) | 影響artifactを別digestへ再構築・全対象へ置換し、旧digestが非稼働になるまでclosureを保留する |
| [PSB-GOV-006 Vulnerability report intake](psb-gov-006-vulnerability-report-intake/README.md) | 外部・社内からの脆弱性報告を安全に受け取り、取りこぼさず調査担当へ渡す |
| [PSB-GOV-007 Vulnerability advisory and notification](psb-gov-007-vulnerability-advisory-and-notification/README.md) | 影響する利用者が対象と取るべき行動を分かるように告知し、通知失敗と訂正を扱う |
| [PSB-GOV-008 Vulnerability remedy validation](psb-gov-008-vulnerability-remedy-validation/README.md) | 修正を主張する製品・版で問題が解消したか確かめ、検証した版の提供状態を分ける |

## 一つの脆弱性報告を追う

報告がサポート窓口へ届いた場合、まず[GOV-006](psb-gov-006-vulnerability-report-intake/README.md)で内容を守り、受領連絡と調査担当者への引き渡しを分けます。次に[GOV-003](psb-gov-003-vulnerability-priority-decision/README.md)で影響する製品・版、調査できない範囲、担当者と期限を決めます。依存が原因なら、製品・成果物・稼働先の調査に[GOV-001](psb-gov-001-supply-chain-impact-assessment/README.md)を使います。

修正する対象は[GOV-008](psb-gov-008-vulnerability-remedy-validation/README.md)で問題の解消と提供する版を確かめます。稼働中の成果物を置き換える必要があれば、[GOV-005](psb-gov-005-deployed-artifact-recovery/README.md)で旧成果物が残っていないかを別に確認します。[GOV-007](psb-gov-007-vulnerability-advisory-and-notification/README.md)では、利用者へ伝える対象・現時点で取れる行動・未確認の範囲を決め、告知と通知を確認します。通知は修正が出た後に限りません。調査中や回避策だけの段階でも、必要な連絡を判断します。

この流れは読むための例です。非該当なら根拠と調査範囲を残し、修正しない対象や期限を超える一時使用は[GOV-003](psb-gov-003-vulnerability-priority-decision/README.md)の判断と、必要時の[GOV-002](psb-gov-002-security-exception-lifecycle/README.md)の限定した例外へ戻します。どの段階でも、次の担当者に未確認の範囲を渡します。

[検索0件をどう判断するか](psb-gov-001-supply-chain-impact-assessment/learning.md)で影響調査を学び、[調査できない製品の優先度をどう決めるか](psb-gov-003-vulnerability-priority-decision/learning.md)で次の判断へ進めます。
[例外は検査の合格ではない](psb-gov-002-security-exception-lifecycle/learning.md)と[更新後も旧成果物が残るとき](psb-gov-005-deployed-artifact-recovery/learning.md)は、その判断を一時的な許可と復旧完了へ渡す教材です。
復旧完了では、[使用許可](../container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)と[実際の稼働digest](psb-gov-005-deployed-artifact-recovery/README.md)を分け、[runtime検知](../container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md)のアラート不在を旧digest非稼働の証拠にはしません。

[届いた報告が調査へ進まないとき](psb-gov-006-vulnerability-report-intake/learning.md)は、受領連絡と担当者への引き渡しを分けて考える教材です。
[修正を出したのに利用者へ届かないとき](psb-gov-007-vulnerability-advisory-and-notification/learning.md)は、修正・告知・通知を分けて考える教材です。
[修正した版でも問題が残るとき](psb-gov-008-vulnerability-remedy-validation/learning.md)は、変更・修正の検証・提供を分けて考える教材です。

PSIRT全体の組織能力、実際のprovider操作、incident全体の復旧完了は、この記録だけでは評価しません。
