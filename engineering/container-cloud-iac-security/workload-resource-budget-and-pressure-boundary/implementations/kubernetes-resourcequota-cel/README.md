# Kubernetes ResourceQuota + CEL implementation

Kubernetes 1.37で、一つの使い捨てnamespaceへCPU、memory、local ephemeral storage、Pod・Job数のaggregate budgetを設定し、各regular・init containerに明示request／limitを要求する実装です。

`verify.sh`はYAMLの形だけを見ません。Live API serverで必須値不足とnamespace quota超過を拒否し、正常Podを起動してResourceQuotaの使用量とQoSを確認します。PID、node reservation、pressure／eviction、cgroupの実効値はこの構成だけでは証明できないため、対応済みにしません。

これは[PSB-CONTAINER-007](../../../../../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)の限定した代表実装です。数値は使い捨てtest profileであり、productionの推奨値ではありません。

## 対象と前提

- Kubernetes `1.37.x`
- `kubectl` `1.37.x`またはversion skew policy内のclient
- Stableな`admissionregistration.k8s.io/v1` Validating Admission Policyが有効
- `ResourceQuota` admissionが有効
- Linux Pod
- `registry.k8s.io/e2e-test-images/agnhost:2.66.1`を取得できるtest cluster、またはreview済みmirrorへの置換
- Namespace、ResourceQuota、ValidatingAdmissionPolicy／Bindingを作成・削除できる権限

`agnhost:2.66.1`はKubernetes `v1.37.0` source treeがE2E testに指定する版です。長期利用やair-gapped環境ではmulti-architecture manifest digestを確認して組織registryへmirrorし、各manifestのimageをexact digestへ置き換えます。

## Test profile

| 境界 | 値 | 意味 |
|---|---:|---|
| Namespace requests | CPU `1`、memory `512Mi`、ephemeral storage `1Gi` | Schedulerへ提出できるaggregate request |
| Namespace limits | CPU `2`、memory `1Gi`、ephemeral storage `2Gi` | Namespace内Podが宣言できるaggregate ceiling |
| Object count | Pod `4`、Job `2` | Replica／Job object増加の上限例 |
| Normal Pod | CPU `250m`、memory `64Mi`、ephemeral storage `128Mi` | Requestとlimitを同じ値にした一container test Pod |
| Admission | Regular・init containerの三resourceを必須、ephemeral containerを拒否 | 予算のない実行経路を拒否 |

CPUとmemoryを同値にしたnormal Podは`Guaranteed` QoSになります。これは全workloadへ同値を要求する推奨ではなく、QoS観測を明確にするtest choiceです。Ephemeral-storageはQoS classの判定には使われません。

## ファイル

| ファイル | 役割 |
|---|---|
| `namespace.yaml` | 固定名の使い捨てnamespace、resource profile label、Pod Security `restricted:v1.37` |
| `resource-quota.yaml` | Namespaceのaggregate request／limitとPod・Job数 |
| `admission-policy.yaml` | 必須resource field、init container、resize／ephemeral subresource、debug禁止、fail-closed binding |
| `workload.yaml` | 明示budgetを持つ正常Pod |
| `reject-missing-resource.yaml` | Ephemeral-storage値を省略した拒否fixture |
| `reject-over-quota.yaml` | Normal Podと合計するとCPU request quotaを越える拒否fixture |
| `verify.sh` | Live admission、Pod起動、QoS、quota usage、cleanup |

## 使い捨てclusterで試す

現在のcontextが破棄可能なtest clusterであることを確認します。固定namespace、policy、bindingのいずれかが既に存在する場合、scriptは削除せず停止します。

```bash
kubectl config current-context
PSB_TEST_CONTEXT=YOUR-DISPOSABLE-CONTEXT ./verify.sh
```

成功時の主な出力は次のとおりです。

```text
PASS missing ephemeral-storage budget denied
PASS bounded Pod has Guaranteed QoS
PASS quota usage records the admitted Pod budget
PASS aggregate CPU request above namespace quota denied
```

終了時にはnamespace、ValidatingAdmissionPolicy、Bindingを削除します。Live Podを作るためimage pullとnode capacityを使用します。

## 採用先へ持ち込む

1. Workloadごとに通常・peak・故障時のCPU、memory、local storage、PID、replica／Job数と上限到達時の挙動を測る。
2. Namespaceが一つのbudget owner／保護境界になるように分け、rolling updateのsurgeとJob並列実行を含むaggregate quotaを決める。
3. `resource-quota.yaml`のtest値をcapacity review済みの値へ置き換え、必要なobject countとPVC budgetを加える。
4. Pod-level resources、regular／init／sidecar、`pods/resize`、debugの採用方針に合わせてCELをreviewする。
5. Policyを`Warn`または隔離namespaceで評価し、既存Podとcontroller生成物をinventoryしてから`Deny`へ移す。
6. Nodeごとに`podPidsLimit`、`systemReserved`、`kubeReserved`、allocatable、memory／disk／PID eviction threshold、local storage計測可否を確認する。
7. Quota status、runtime limit、CPU throttle、OOM、eviction、unschedulable、node pressure、collector healthを別のsignalとして観測する。

`ResourceQuota`の値をcopyするだけでは、cluster capacity、workloadの必要量、PID、node pressure、runtime enforcementを確認できません。

## 解除

使い捨て確認は`verify.sh`が自動で削除します。採用先でpolicyやquotaを外すと新しいPod・resize・replicaが無制限に受理され得ます。Workload停止または承認済みの代替境界を用意し、binding、policy、quotaの順序と既存Podへの影響を確認して変更します。ResourceQuotaやpolicyを後から追加しても、既に実行中のPodを自動的に縮小しません。

## 制限

- このrepositoryにはlive Kubernetes clusterと`kubectl`がなく、API拒否、Pod起動、quota usageは未実行です。
- Test profileの数値はproduction推奨値ではありません。Workload測定、failure behavior、node／failure-domain capacityから決めます。
- ResourceQuotaはnamespace aggregateを制限してもnodeを分離せず、cluster capacityに合わせて自動調整しません。
- CELはregular・init containerを確認し、個別budgetを持てないephemeral containerを拒否します。Productionのdebug手順は別途必要です。
- PID limit、system／kube reservation、node allocatable、eviction threshold、priority、pressure、cgroupの実効値を確認しません。
- Local ephemeral storageの計測とevictionはnode filesystem layoutとkubeletに依存します。Hard disk quota、inode、削除後も開かれたfileを保証しません。
- CPU limitは主にthrottle、memory limitはOOM、ephemeral storage limitはevictionにつながります。Application availabilityやSLOを保証しません。
