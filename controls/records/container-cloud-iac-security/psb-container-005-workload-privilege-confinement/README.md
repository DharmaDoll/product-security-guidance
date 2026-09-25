# PSB-CONTAINER-005: Workload privilege confinement

学ぶ：[A trusted image can still become a privileged process](learning.md) ·
設計する：[Workload privilege and host boundary](../../../../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/README.md) ·
試す：[Kubernetes Pod Security Admission + CEL](../../../../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/implementations/kubernetes-psa-cel/README.md)

## 問い

Workload内のprocessが侵害されても、不要なroot権限、kernel機能、hostのnamespace・file・runtime API、用途を限定していない書込領域、control-plane credentialへ到達できないように制限し、その制限を実行前に強制できるか。

## できてはいけないこと

署名済みimageや承認済みdeploymentという理由だけで、privileged container、root実行、権限昇格、過大なLinux capability、unconfined syscall、host namespace・hostPath・runtime socket、書込み可能なroot filesystemを許可してはいけません。
Init、sidecar、ephemeral container、debug経路、policy評価エラー、広い例外を使って同じ制限を迂回できてはいけません。

## 適用範囲と非適用

ContainerとPodに相当するworkloadの実効process identity、privilege escalation、capability、syscall・MAC profile、host接続、filesystem、workloadへ渡すcontrol-plane credential、作成・更新時の強制と例外が対象です。

CPU・memory・PID・storage枯渇への[resource availability](../psb-container-007-workload-resource-consumption-bounds/README.md)、[workload間・外部宛てのnetwork segmentation](../psb-container-006-workload-network-segmentation/README.md)、[node／daemon自体のhardening](../psb-container-003-container-host-daemon-boundary/README.md)、applicationの脆弱性、imageの真正性は別の主題です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `WORKLOAD-CONFINE-1` | Main、init、sidecar、ephemeral、debug等、最終的に実行できる全containerと対象OS・runtime classを列挙し、同じconfinement profileで評価する |
| `WORKLOAD-CONFINE-2` | Privileged modeとroot実行を既定で拒否し、processの権限昇格を無効にする。必要な実行identityはworkloadごとに明示する |
| `WORKLOAD-CONFINE-3` | Kernel capabilityを既定で全てdropし、必要な追加だけを狭く許可する。対象OSでruntime既定以上のseccompと利用可能なMAC profileを適用する |
| `WORKLOAD-CONFINE-4` | Host namespace、host process、hostPath、device、host port、container runtime・node管理socket等のhost接続を既定で拒否する |
| `WORKLOAD-CONFINE-5` | Image由来のroot filesystemをread-onlyにし、必要な書込みを用途・所有者・lifecycleが明確なvolumeへ限定する |
| `WORKLOAD-CONFINE-6` | Control-plane credentialを不要なworkloadへ自動付与しない。必要な場合は専用identity、最小権限、対象audience、期限へ限定する |
| `WORKLOAD-CONFINE-7` | Final workloadの作成・更新・ephemeral／debug追加を実行前に強制し、policyの欠落・評価エラー・未対応形式を通常の許可へ変えない。例外は対象・理由・owner・期限を限定する |

## 実装判断の羅針盤

Imageの真正性とprocessへ渡す権限は別に判断します。最初に「侵害後も必要な権限」をworkloadごとに決め、platformの組込みprofileで広い既定値を強制し、不足するread-only filesystemやcredential付与等だけを追加policyで補います。

[IaCやCIのplan検査](../psb-iac-001-infrastructure-change-authorization-and-drift/README.md)は早いfeedbackとして有用ですが、controllerによるPod生成、mutation、直接作成、ephemeral container追加を含む最終状態の強制点にはなりません。Cluster admissionとruntimeが同じprofileを実際に適用し、policy版と対象scopeを記録できる構成にします。

一部のsystem workloadがhost接続を必要とする場合、一般namespaceを丸ごと除外しません。必要なhost機能、workload identity、配置先、owner、期限を別のprofileまたは[Security exception lifecycle](../../governance-operations/psb-gov-002-security-exception-lifecycle/README.md)へ結び付けます。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は「できてはいけないこと」が実際に起きないかを確認する項目です。実施済みの診断結果ではありません。

- Main containerが基準を満たしていても、privilegedなinit・sidecar・ephemeral containerを追加できないか。
- `runAsNonRoot`を省略したimage、UID 0、`privileged: true`、`allowPrivilegeEscalation: true`が拒否されるか。
- `drop: [ALL]`を外したり、`SYS_ADMIN`等の未承認capabilityを追加したりできないか。
- Seccompを`Unconfined`または未指定にし、AppArmor／SELinux等の必要なMAC profileを外しても実行できないか。
- `hostNetwork`、`hostPID`、`hostIPC`、HostProcess、`hostPath`、host port、device、runtime socketを一般workloadから利用できないか。
- Root filesystemを書込み可能に戻したり、書込みvolumeをhostの機密pathへ差し替えたりできないか。
- 不要なservice account tokenを自動mountできないか。必要なtokenを別audience・別namespace・過大なRBACへ流用できないか。
- Enforcement対象外のnamespace、runtime class、user、subresource、API経路から同じworkloadを作成できないか。
- Policy版の不一致、CEL／webhook error、profile取得不能、未対応OSを通常のallowへ変えていないか。
- 期限切れまたはowner不明の例外でhost接続やprivilegeを継続できないか。

## 境界と受け渡し

- Exact artifactとconsumer判断は[PSB-CONTAINER-001](../psb-container-001-deployment-artifact-admission/README.md)から受け取ります。
- Node、kernel、container runtime、daemon自体のhardeningは[PSB-CONTAINER-003](../psb-container-003-container-host-daemon-boundary/README.md)の別主題です。
- 実行後のprocess、syscall、file変更とsensor healthは[PSB-CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)へ渡します。
- Resource consumptionは[PSB-CONTAINER-007 Workload resource consumption bounds](../psb-container-007-workload-resource-consumption-bounds/README.md)、旧`CNT-008`は[PSB-CONTAINER-006 Workload network segmentation](../psb-container-006-workload-network-segmentation/README.md)へ移行しました。
- [IaC change boundary](../psb-iac-001-infrastructure-change-authorization-and-drift/README.md)はsource・plan・applyを結び、manifest検査はfeedbackを提供しますが、live workload enforcementの代替ではありません。

## 参照資料とマッピング

- [REF-WORKLOAD-CONFINEMENT-001](../../../../sources/README.md#ref-workload-confinement-001)
- [NIST SP 800-190](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)
- [成果物間の関係](../../../../mappings/pilot.yaml)
- [Framework mapping](../../../../mappings/frameworks.yaml)
- [横断分析](../../../../docs/ANALYSIS_LENSES.md)
