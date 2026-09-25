# ENG-CONTAINER-003: Workload privilege and host boundary

## 利用場面と推奨構造

Application processが侵害されても、workloadへ不要なkernel・host・control-plane authorityを渡さない設計です。

```text
workload requirements
  ├─ required process identity
  ├─ required kernel / filesystem access
  └─ required platform credential
              |
              v
IaC / CI feedback ──> final workload admission ──> runtime profile
                         |       |                    |
                         |       +-- supplemental     +-- effective state
                         |           fail-closed policy     observation
                         +-- built-in baseline
                                 |
                                 v
                    allow / deny / evaluation error
```

推奨する順序は、workloadが実際に必要とする権限を決め、platformの組込みprofileで共通baselineを強制し、足りない特性だけを小さな追加policyで補うことです。製品名やmanifest fieldからcontrolの意味を逆算しません。

## 一つにまとめる境界

次は、application code executionからhostやkernel authorityへ進む同じ失敗経路を制限するため、一つのconfinement profileで扱います。

- Process identity、root、privileged mode、privilege escalation
- Linux capability、seccomp、AppArmor／SELinux等のMAC
- Host namespace、host process、host path、device、host port、runtime／node管理socket
- Image root filesystemと明示したwritable volume
- Workloadへ自動的に渡るcontrol-plane credential
- Main、init、sidecar、ephemeral、debugを含む実行経路

CPU・memory・PID・storageの枯渇は、request／limitだけでなくquota、node capacity、eviction、scheduling、runtime enforcementを扱うavailability設計です。NetworkはCNI、identity、ingress／egress、DNS、service mesh、external boundaryを扱います。どちらもこのpatternへ詰め込みません。

## Profile contract

| 要素 | 決めること | 証拠 |
|---|---|---|
| Scope | Cluster、namespace、workload class、OS、runtime class | 対象inventory、namespace／selector、除外一覧 |
| Process | UID／user、privileged、escalation | Final workload、admission decision |
| Kernel | Capability allowlist、seccomp、MAC | Profile名・版、runtimeの実効状態 |
| Host attachment | Namespace、path、device、port、管理socket | 拒否policy、例外decision、runtime mount |
| Filesystem | Read-only root、明示したwritable volume | Final mount、volume identity・lifecycle |
| Credential | 自動mountの禁止、必要なidentity・audience・期限 | Service identity、binding、token設定 |
| Enforcement | Create、update、ephemeral／debug、error semantics | Policy版、decision、audit、coverage |

Policy名だけでは不十分です。どのversionのprofileを、どのscopeへ、どのmodeで適用し、何を追加policyへ渡したかを記録します。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| Platform組込みprofile | 共通baselineを低い運用負荷で強制したい場合。製品が定義する固定profileの範囲外は補えず、version差を管理する必要がある |
| Declarative admission policy | Final objectのfieldで判断できる追加条件を強制する場合。外部照会を避けやすいが、CEL／schema／subresource coverageを対象versionで確認する |
| External policy engine／webhook | 複雑な組織policy、外部data、共有ruleが必要な場合。Availability、TLS identity、timeout、failure policy、upgrade compatibilityを所有する |
| Sandbox runtime／dedicated node | Shared kernelでは隔離が不足する高risk workload。起動時間、互換性、運用負荷、配置capacityが増える |
| [IaC・CI検査](../../../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md) | 開発者へ早くfeedbackする場合。Admissionやruntimeの代替にせず、同じprofile版とのdriftを管理する |

## Kubernetesでの配置

Kubernetesでは、Pod Security Admissionの`restricted`を対象namespaceへ`enforce` modeで適用し、policy versionをcluster minorへ固定する構成を起点にできます。`audit`と`warn`は移行時の観測には使えますが、それだけでは違反Podを拒否しません。

Restricted profileはnon-root、privilege escalation、seccomp、capability、host namespace・hostPath等の広いbaselineを扱います。Read-only root filesystemや不要なservice account tokenの禁止等は別のadmission policyで補います。追加policyは`failurePolicy: Fail`と`Deny` actionを使い、対象namespace selectorとPod subresourceを確認します。

Pod Security Admissionの`enforce`はDeploymentやJob等のtemplate自体ではなく、controllerが生成するPodを拒否します。CIでtemplateを検査して早く失敗させつつ、最終的な強制はPod作成境界に残します。

代表実装は[Kubernetes Pod Security Admission + CEL](implementations/kubernetes-psa-cel/README.md)にあります。

## 例外とsystem workload

Node agent、CNI、storage driver、runtime sensor等はhost機能を必要とする場合があります。一般workloadのbaselineを弱める代わりに、専用namespace、service identity、node placement、許可するhost path・capability、owner、期限を分けます。

Namespace、user、runtime classの広い除外は、その主体が作成できる全workloadを除外します。例外は[Security exception lifecycle](../../governance-operations/security-exception-decision-boundary/README.md)へ接続し、元の不合格を合格へ書き換えません。

## 失敗経路

- `warn`または`audit`だけを設定し、拒否されると誤認する。
- Profile versionを`latest`にして、cluster upgradeで意味が変わる。
- Main containerだけを検査し、init・ephemeral containerを見ない。
- IaC scannerがpassしたmanifestと、mutation後に実行されるPodが異なる。
- Admission policyが構文errorや未対応fieldで失敗したときに`Ignore`する。
- System namespaceやcontroller identityを広く除外し、一般利用者がその経路を使える。
- Read-only rootを設定しても、hostPathや過大なwritable volumeを許す。
- Admission時の設定を、runtimeが実際に適用した証拠とみなす。

## 導入時の確認

[Controlの診断で確認する項目](../../../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md#failure-checks)を、対象versionと同じ使い捨てclusterで確認します。正常Pod、profile違反、追加policy違反、policy評価errorを区別し、本番credentialや攻撃用imageは使いません。

Runtimeで実効UID、capability、seccomp、mount、credentialを観測する場合は、admissionのdecision identityと対象Podを結び、[Runtime detection to triage](../runtime-detection-to-triage/README.md)へ渡します。

## このpatternの範囲

このpatternは、[resource availability](../workload-resource-budget-and-pressure-boundary/README.md)、[network segmentation](../workload-network-allow-boundary/README.md)、[node／daemon hardening](../node-runtime-management-boundary/README.md)、applicationの脆弱性、artifact authenticityを保証しません。Kubernetes実装はLinux Pod向けの代表経路であり、Windows HostProcess、全policy engine、全runtime classを対象にしません。

- [Control](../../../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)
- [教材](../../../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/learning.md)
- [Deployment artifact admission](../deployment-artifact-admission-boundary/README.md)
- [Runtime detection to triage](../runtime-detection-to-triage/README.md)
- [参照資料と採否](../../../sources/README.md#ref-workload-confinement-001)
