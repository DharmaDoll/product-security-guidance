# Kubernetes Pod Security Admission + CEL implementation

Kubernetes 1.37で、対象namespaceのPodを組込み`restricted` profileへ通し、そこに含まれないread-only root filesystemとservice account tokenの自動mount禁止をValidating Admission Policyで補う最小構成です。

通常のPod作成では、API server上の次の二層が対象外の設定を拒否します。どちらが先に拒否するかには依存しません。

1. Pod Security Admissionがroot、privileged、権限昇格、過大なcapability、host namespace・hostPath、unconfined seccomp等を拒否する。
2. CEL policyが全containerの`readOnlyRootFilesystem: true`とPodの`automountServiceAccountToken: false`を要求し、評価errorは`failurePolicy: Fail`、違反は`Deny`として拒否する。

これは[PSB-CONTAINER-005](../../../../../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)の代表実装です。Resource limitとNetworkPolicyは扱いません。

## 対象と前提

- Kubernetes `1.37.x`
- `kubectl` `1.37.x`またはversion skew policy内のclient
- Pod Security Admissionが利用できるcluster
- `admissionregistration.k8s.io/v1`のValidating Admission Policy
- Linux Pod。WindowsとHostProcessはこの例の確認対象外
- Cluster-scoped policyを作成できる権限

Pod Security AdmissionはKubernetes 1.25から、Validating Admission Policyは1.30からstableです。この実装は2026-09-25時点のKubernetes 1.37仕様にprofileを固定しています。別minorへ導入する場合は`namespace.yaml`の三つのversion labelを対象minorへ変更し、拒否ケースを再実行します。

## ファイル

| ファイル | 役割 |
|---|---|
| `namespace.yaml` | `restricted`を`enforce`し、profileを`v1.37`へ固定する使い捨てnamespace |
| `admission-policy.yaml` | Read-only root filesystemとtoken自動mount禁止を補うfail-closed CEL policyとbinding |
| `fixtures/secure-pod.yaml` | 両方のpolicyを通るPod |
| `fixtures/privileged-pod.yaml` | Pod Security Admissionが拒否するPod |
| `fixtures/writable-root-pod.yaml` | CEL policyが書込み可能なroot filesystemを拒否するPod |
| `fixtures/ambient-token-pod.yaml` | CEL policyがtoken自動mountを拒否するPod |
| `verify.sh` | 使い捨てclusterへpolicyを入れ、server-side dry runで四経路を確認して解除する |

## 使い捨てclusterで試す

現在のcontextが破棄可能なtest clusterであることを確認し、そのcontext名を明示して実行します。

```bash
kubectl config current-context
PSB_TEST_CONTEXT=kind-psb-workload-confinement ./verify.sh
```

Scriptは`PSB_TEST_CONTEXT`と現在のcontextが一致しない限り何も変更しません。成功時は次を表示します。

```text
PASS secure pod accepted
PASS privileged pod rejected
PASS writable root filesystem rejected
PASS ambient service account token rejected
```

確認にはserver-side dry runを使うため、fixtureのcontainer imageはpull・実行されません。Policy、binding、test namespaceは終了時に削除します。

## 手元のclusterへ段階的に導入する

1. 対象cluster minorとPod Security Standardsの差分を確認し、`enforce-version`をそのminorへ固定する。
2. Host機能を必要とするsystem workloadと一般workloadをinventory化し、同じnamespaceへ混在させない。
3. `admission-policy.yaml`の名前、selector、追加条件をreviewし、まずtest clusterへ適用する。
4. 対象namespaceへ`product-security-guidance.example/workload-confinement: enforce`を付ける。
5. Pod Security Admissionは最初に`warn`・`audit`で既存違反を調べ、修正後に`enforce: restricted`へ切り替える。
6. `secure-pod.yaml`と三つの拒否fixtureを対象cluster versionでserver-side dry runする。
7. Deployment、Job、直接Pod、ephemeral container等、組織が使う全経路の実Pod生成を確認する。
8. Admission audit、policy version、対象namespace、例外を運用証拠へ残す。

この例のnamespaceをそのまま本番名へ変えるだけでは、既存workloadやsystem componentとの互換性を確認できません。

## 解除

使い捨て確認は`verify.sh`が自動で解除します。手動で入れた場合は、最初に対象namespaceの追加selector labelを外し、影響を確認してからpolicyを削除します。

```bash
kubectl label namespace YOUR_NAMESPACE \
  product-security-guidance.example/workload-confinement-
kubectl delete -f admission-policy.yaml
```

Pod Security Admissionのlabelを外すと`restricted` enforcementも消えます。単なるrollbackとして無条件に外さず、元のpolicyまたは承認済み代替策へ戻します。

## 制限

- このrepositoryではlive Kubernetes clusterへ接続しておらず、拒否結果は未実行です。
- Namespace selectorが付かないnamespaceは追加CEL policyの対象外です。全namespaceのinventoryは別途必要です。
- Pod Security Admissionの広いexemption、API server設定、static Pod、kubeletやruntimeの直接操作は確認しません。
- Read-only root filesystemでも、明示したvolumeへの書込み、memory上の改変、network通信は可能です。
- Service account tokenを明示的にprojectする経路とRBAC・audience・期限は、このmanifestだけでは評価しません。
- AppArmor／SELinux profile、sandbox runtime、Windows、device pluginは別の実装判断です。Networkは[NetworkPolicy代表実装](../../../workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)、resourceは[ResourceQuota + CEL代表実装](../../../workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)で独立して扱います。
- Admission成功はruntimeでprofileが実際に適用された証拠や、applicationが安全である証拠ではありません。
