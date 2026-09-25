# PSB-IAC-001: Infrastructure change authorization and drift boundary

学ぶ：[The reviewed plan is not always the change that runs](learning.md) ·
設計する：[Infrastructure plan, apply, and drift boundary](../../../../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)

## 問い

Infrastructureの変更を、reviewしたsource・依存、解決済みの実行計画、許可されたapply、provider上の現在状態まで同じ変更として追跡し、禁止した状態と未確認の状態を止められるか。

## できてはいけないこと

Reviewしたsourceとは異なるmodule、provider、variable、policy、targetからplanを作り、許可済みの変更としてapplyできてはいけません。人やpolicyが確認したplanとは別の再planを、同じ承認で実行できてはいけません。

Planで値を確認できなかった、policy engineが失敗した、対象resourceを解釈できなかった、現在状態を取得できなかった場合に「問題なし」としてはいけません。Console、API、別toolによる変更や未管理resourceが、CIを通らなかったという理由だけで見えなくなってはいけません。自動修正が、影響範囲を確認せずresource削除、network遮断、credential変更等を実行してはいけません。

## 適用範囲と非適用

Terraform、OpenTofu、CloudFormation等で管理するinfrastructure source、module・provider等の依存、variable、state・workspace、resolved plan、Policy as Codeの判断、apply identity、cloud control plane、実resourceの観測、drift・例外・修正判断が対象です。

個々のresourceに必要な暗号化、network、identity、logging等の安全値は、資産、脅威、provider仕様を持つ別のcontrolまたはplatform標準で定義します。CI identityの発行・交換そのものは[PSB-CICD-006](../../cicd-security/psb-cicd-006-workload-federation-boundary/README.md)、workloadの最終admissionは[PSB-CONTAINER-005](../psb-container-005-workload-privilege-confinement/README.md)等が扱います。IaCのplan合格だけで、live resourceが安全、変更経路が完全、組織へ導入済みとは扱いません。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `IAC-CHANGE-1` | Infrastructure sourceのrevision、root・child module、provider、variable、policy、tool、state／workspace、targetを一つの変更identityとして記録する。Provider lockとmodule version等、toolごとに異なる固定範囲を明示する |
| `IAC-CHANGE-2` | 対象資産と脅威から導いたruleを、source textだけでなく解決済みplanのcreate・update・delete・replaceとsecurity-relevant valueへ適用する。標準moduleの使用だけを適合の証拠にしない |
| `IAC-CHANGE-3` | Allow、deny、明示的な人の判断、評価error、未対応resource、unknown／apply時決定値、対象漏れを別の状態にし、security判断に必要な値が未確定ならapply前に止めるか独立した強制点へ渡す |
| `IAC-CHANGE-4` | Review・policy判断を、sourceと依存、target、入力、保存した実行可能planへ結び付け、applyはそのplanだけを消費する。Planを機微artifactとしてアクセス、保持、廃棄、置換防止の対象にする |
| `IAC-CHANGE-5` | Apply authorityをreview・plan生成から分離し、承認されたtargetと操作に限定する。保護された実行主体だけが取得でき、期限、再利用、取消し、auditを管理できるidentityを使う |
| `IAC-CHANGE-6` | Console、API、SDK、別IaC tool、別pipeline等の変更経路を列挙し、provider側の拒否または独立した観測へ接続する。一部のhookを全変更経路の強制と扱わない |
| `IAC-CHANGE-7` | Provider APIから得た実resourceと管理対象inventoryを、承認済みdesired stateへ継続的に照合する。Out-of-band変更、未管理resource、収集欠落、stale state、権限不足を区別する |
| `IAC-CHANGE-8` | 例外とdriftにはresource、rule、owner、理由、期限、影響を結び付ける。修正は新しいplanとしてreviewし、自動修正は可逆性、blast radius、rollback、証拠保全を確認した操作へ限定する |

## 実装判断の羅針盤

最初にmodule catalogやscanner製品を選ぶのではなく、守るresource、禁止する状態、変更できる全経路、最終的に確認するprovider状態を一つ決めます。その上で、安全な既定値を持つmoduleは作業を簡単にする入口、plan policyはapply前の判断、provider guardrailは迂回経路の強制、drift観測はapply後の確認として配置します。

Terraformでは`.terraform.lock.hcl`が現在追跡するのはprovider dependencyであり、remote moduleのversion選択を同じ仕組みで固定するわけではありません。保存planを`terraform apply`へ渡せば、そのplanに記録された変更を実行できます。Apply時に設定から再planする構成は、review対象と実行対象を別にします。

PlanとJSON表現には機微な入力や値が平文で含まれ得ます。Policyへ渡す、artifact storeへ保存する、review画面へ表示する各経路で、アクセスと保持を設計します。Redactionした表示だけを、保存artifactも秘匿されているという意味にしません。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は「できてはいけないこと」が実際に起きないかを確認する項目です。実施済みの診断結果ではありません。

- Review後にsource revision、module version、provider lock、variable、policy bundle、workspaceまたはtargetを変え、既存の承認でapplyできないか。
- Speculative planや表示用JSONだけをreviewし、apply jobが別のplanを作り直していないか。保存planを差し替え、別targetへ適用できないか。
- Remote moduleが広いversion constraintやbranchを使い、reviewなしで別内容へ解決されないか。Provider lockの存在をmodule contentの固定と誤認していないか。
- Createだけを検査し、update、delete、replace、data source、import、moved resource、targeted plan等がruleを迂回できないか。
- Security-relevant値がunknown、null、sensitive、provider default、apply時決定、unsupported schemaの時にallowへ落ちないか。
- Policy input生成失敗、policy engine timeout、rule取得失敗、plan JSON format変更、対象resource 0件を「違反なし」にしないか。
- Plan artifactまたはJSONを一般のPR参加者、log、cache、長期artifact、別jobから読めないか。削除後も複製やbackupへ残らないか。
- Untrustedなplan生成jobがapply credential、state write、policy変更、approval status、artifact置換権限を持たないか。
- Apply identityを別repository、branch、environment、workspace、account、subscription、project、region、actionへ再利用できないか。失効後のsessionが残らないか。
- Console、cloud API、SDK、別pipeline、別IaC tool、emergency pathから同じ禁止状態を作成・更新できないか。Provider hookの対象外操作を列挙できるか。
- Stateにあるresourceだけを調べ、同じaccount内の未管理resource、import漏れ、削除済みと誤認したresourceを見落とさないか。
- Provider APIのpagination、権限不足、rate limit、region漏れ、stale cache、state lock、refresh失敗をdriftなしに変換しないか。
- 期限切れ・wildcard・owner不明の例外が残らないか。例外がmodule、plan、provider、driftの全段階を意図せず無効にしないか。
- 自動修正がresource削除、network遮断、key変更、database再作成等を、影響確認、承認、rollback、証拠保全なしに実行しないか。

## 境界と受け渡し

- Source change reviewから、承認済みrevisionとreviewer decisionを受け取ります。IaC controlはそのidentityをresolved planとapplyへ渡します。
- [PSB-CICD-006](../../cicd-security/psb-cicd-006-workload-federation-boundary/README.md)からjob identityの発行条件を受け取り、このcontrolでtargetと許可操作へ限定します。
- Container workloadではplan検査を早いfeedbackとして使い、最終objectの拒否を[Deployment artifact admission](../psb-container-001-deployment-artifact-admission/README.md)と[Workload privilege confinement](../psb-container-005-workload-privilege-confinement/README.md)へ渡します。
- Provider上の逸脱、観測障害、修正結果をDetection／Operationsへ渡し、重大なout-of-band変更やcredential悪用はincident responseへ接続します。

## 参照資料とマッピング

- [REF-IAC-CHANGE-BOUNDARY-001](../../../../sources/README.md#ref-iac-change-boundary-001)
- [成果物間の関係](../../../../mappings/pilot.yaml)
- [横断分析](../../../../docs/ANALYSIS_LENSES.md)
- [移行記録](../../../../docs/IAC_CHANGE_BOUNDARY_MIGRATION.md)

旧成果物のframework mappingは、IaCのplan・apply・provider状態への直接要件ではなかったため継承していません。判断理由は移行記録に残しています。
