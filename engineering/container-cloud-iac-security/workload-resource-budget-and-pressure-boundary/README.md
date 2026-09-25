# ENG-CONTAINER-005: Workload resource budget and pressure boundary

## 利用場面と推奨構造

故障または侵害された一つのworkloadが、共有nodeや別tenantのCPU、memory、PID、local storage、control-plane object capacityを枯渇させる範囲を制限する設計です。

```text
reviewed workload budget
  requests + ceilings + object count + overload behavior
             |
             v
  final admission / resize enforcement
             |
      +------+----------------+
      |                       |
      v                       v
workload runtime bound   tenant aggregate quota
      |                       |
      +----------+------------+
                 v
 node allocatable + system reservation + pressure thresholds
                 |
                 v
 quota / cgroup / throttle / OOM / eviction / pressure evidence
```

Workload、tenant／namespace、nodeの三段階を一つのbudget contractでつなぎます。一つの設定だけで全段階を達成した扱いにはしません。

## Resource budget contract

| 要素 | 決めること | 主な証拠 |
|---|---|---|
| Subject | Workload、tenant、namespace、failure domain | Inventory、owner、selector、namespace lifecycle |
| Normal demand | CPU／memory／storageの通常時とpeakのrequest | Load observation、sizing review、scheduler state |
| Ceiling | CPU、memory、PID、local storage、object数の最大値 | Admission policy、quota、runtime／kubelet config |
| Amplification | Replica、surge、Job並列数、debug、resize | Controller spec、subresource coverage、quota usage |
| Failure behavior | Throttle、OOM、process失敗、eviction、unschedulable | Application test、event、status、runbook |
| Shared capacity | Node allocatable、system reservation、tenant合計、headroom | Node config・status、capacity model、pressure threshold |
| Observation | Current usage、limit hit、pressure、取得障害 | Metrics、event、quota status、runtime state、collector health |

数値はworkloadの挙動とplatform capacityから決めます。旧実装の`1000m`、`512Mi`、PID `256`を全workloadの標準値にはしません。

## Kubernetesでの配置

ContainerのCPU／memory／ephemeral-storage requestはschedulerの配置入力です。CPU／memory limitはcontainer runtimeがkernelのcgroupへ渡します。CPUは主にthrottleし、memoryはOOM killにつながります。Ephemeral storageはwritable layer、log、disk-backed `emptyDir`等をkubeletが計測し、超過時にPodをevictします。Memory-backed `emptyDir`はmemory使用量として扱います。

ResourceQuotaはnamespace内のrequest・limit合計とobject数を制限します。CPU／memory quotaを設定すると各containerへ明示値を要求できますが、ephemeral-storageは未指定のPodを同じ方法で必ず拒否しません。代表実装ではCELで明示値を要求します。

LimitRangeは個別objectのmin／maxやdefaultを設定できます。Default注入は利用者が省略した値を補うため、提出されたbudgetと最終budgetの違いが見えにくくなります。明示値をreviewしたいprofileでは、default mutationを使わずvalidationで不足を拒否します。

Kubernetes 1.37ではPodのCPU／memoryを`pods/resize` subresourceから変更できます。作成・通常updateだけでなくresize、controllerが生成するfinal Pod、ephemeral container追加を強制範囲へ含めます。Ephemeral containerは個別resource limitを指定できないため、Pod-level budgetを確認できない構成では追加を拒否する選択肢があります。

## PID・local storage・node pressure

Pod PID limitはworkload manifestではなく、nodeごとのkubelet `podPidsLimit`で設定します。Nodeごとに値が違うと配置先で境界が変わります。`systemReserved`と`kubeReserved`のPID予約、`pid.available` eviction thresholdも併せて確認します。Evictionは周期的な検知であり、急増するPIDをhard limitの代わりにはできません。

Local ephemeral storageの計測可否はnodeのfilesystem layoutとkubelet設定に依存します。Periodic scanは削除後もprocessが開いたfileを見落とし得ます。Project quotaも使用量の観測を改善しますが、storageを常時hard capするとは限りません。Disk容量だけでなくinode、container log、image／container filesystem、collector healthを確認します。

Node allocatableはcapacityそのものより小さく、OSとKubernetes daemonの予約を差し引く必要があります。Memory、disk、PID pressureではkubeletがPodをevictします。Quotaはnamespace単位でnodeを分離しないため、tenant quotaの合計、placement、failure domain、priorityをcapacity側で照合します。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| ResourceQuota | Namespaceの合計request／limitとobject数を制限する。Cluster capacityや一containerの実使用量、node分離は保証しない |
| Validating Admission Policy／webhook | 必須field、範囲、resize、debug経路を明示的に拒否する。全resource種別、subresource、failure policy、既存objectを管理する必要がある |
| LimitRange | 個別container／Pod／PVCのmin・maxとdefaultが必要な場合。Default mutationと複数LimitRangeの挙動をreviewする |
| Kubelet／runtime config | PID、cgroup、node reservation、evictionを強制する。Managed platformでは設定・観測APIがprovider固有になる |
| Dedicated node／sandbox | 強いtenant・failure-domain分離が必要な場合。Capacity効率、運用、配置、costが増える |

## 導入順序

1. Workloadごとの通常・peak・故障時の消費経路とownerを列挙する。
2. CPU、memory、PID、local storage、object数のrequest、ceiling、過負荷時の挙動をreviewする。
3. Tenant aggregate quotaとrolling update／Job並列実行時のpeakを照合する。
4. Admissionを先に用意し、controller生成後のPod、resize、debug経路を拒否確認する。
5. Node allocatable、system／kube reservation、PID limit、pressure threshold、tenant合計を整合させる。
6. 隔離環境でquota超過、CPU throttle、OOM、PID失敗、storage eviction、unschedulableを別の結果として観測する。
7. 実環境でusage、headroom、throttle、OOM、eviction、pressure、収集障害を継続確認し、budgetを更新する。

## 失敗経路

- Requestを設定したためruntime使用量も制限されたと考える。
- Limitだけを設定し、schedulerが過小なrequestでnodeへ詰め込むことを許す。
- Namespace quotaの合計がcluster capacityを越えていても、各namespaceがquota内なので安全と判断する。
- CPU／memoryだけを検査し、PID、log、writable layer、`emptyDir`、inode、Pod／Job数を無制限にする。
- LimitRangeのdefaultで不足fieldを補い、提出したmanifestがreview済みbudgetを持つと扱う。
- Createだけを検査し、resize、ephemeral container、surge、Job並列化でbudgetを広げる。
- OOM、eviction、unschedulable、metrics欠落を同じ健康状態に集約する。

## このpatternの範囲

このpatternは、一workloadの消費を共有基盤へ広げないresource isolationを扱います。Application rate limit、autoscalingの妥当性、冗長性、PDB、persistent storageの可用性・performance、network bandwidth、事業SLOは別の責任です。

- [Control](../../../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)
- [教材](../../../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/learning.md)
- [Kubernetes代表実装](implementations/kubernetes-resourcequota-cel/README.md)
- [Workload privilege and host boundary](../workload-privilege-and-host-boundary/README.md)
- [Runtime detection to triage](../runtime-detection-to-triage/README.md)
- [参照資料と採否](../../../sources/README.md#ref-workload-resource-bounds-001)
