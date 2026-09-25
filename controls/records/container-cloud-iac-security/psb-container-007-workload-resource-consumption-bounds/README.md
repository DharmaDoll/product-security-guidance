# PSB-CONTAINER-007: Workload resource consumption bounds

学ぶ：[One log loop can exhaust a shared node](learning.md) ·
設計する：[Workload resource budget and pressure boundary](../../../../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/README.md) ·
試す：[Kubernetes ResourceQuota + CEL](../../../../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)

## 問い

故障または侵害されたworkloadが、reviewした予算を越えてCPU、memory、process、local storage、object数を消費し、同じ基盤の別workloadやnodeを気付かないまま枯渇させることを防げるか。

## できてはいけないこと

Requestだけを設定して使用量の上限と扱ったり、containerごとのlimitだけを設定してnamespace・node全体の枯渇を防いだと扱ったりしてはいけません。
CPU／memoryだけを見て、fork bomb、log・writable layer・`emptyDir`によるdisk／inode枯渇、大量のPod・Job・PVC作成、nodeのsystem processに必要な余力を無制限にしてはいけません。

## 適用範囲と非適用

WorkloadのCPU、memory、PID、local ephemeral storage、Pod等のobject数、tenant／namespaceのaggregate budget、node allocatable・system reservation・pressure／eviction、作成・更新・resize時の強制と実行後の観測が対象です。

Applicationのrequest rate limit、autoscalingの正しさ、replica冗長性、disruption budget、persistent storageの耐久性・IOPS、network bandwidth、cluster自体へのDDoS対策、事業上のavailability SLOは別の主題です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `RESOURCE-1` | Workloadまたは同じ保護境界の単位で、CPU、memory、PID、local ephemeral storage、object数のrequest、上限、用途、owner、過負荷時の挙動を決める。全環境へ同じ固定値を適用しない |
| `RESOURCE-2` | Main、init、sidecar、debug等の実行経路と、writable layer、log、`emptyDir`等のlocal storage経路を列挙し、予算外の経路を残さない |
| `RESOURCE-3` | Schedulingに使うrequest、runtime ceiling、overcommit、throttle、OOM・evictionを別の意味として扱い、requestまたはlimitの片方だけで他方を満たしたことにしない |
| `RESOURCE-4` | Tenant／namespace単位でrequest・limitの合計とPod・Job・PVC等のobject数を制限し、一workloadのreplica増加やobject作成が共有capacityを占有しないようにする |
| `RESOURCE-5` | Pod単位のPID上限とnodeのPID予約、local storageの計測対象・上限・inode／disk pressureを選択したruntimeとnode構成で強制する |
| `RESOURCE-6` | Node allocatable、system／platform reservation、eviction threshold、workload priority、failure domainごとの余力を整合させ、namespace quotaをcluster capacityの証明にしない |
| `RESOURCE-7` | Create、update、controller生成、scale、resource resize、debug経路でfinal budgetをfail closedに強制し、実効cgroup、quota使用量、throttle、OOM、eviction、unschedulable、pressureと観測障害を区別する |

## 実装判断の羅針盤

最初に固定値を配るのではなく、通常時・peak・故障時に必要な資源と、上限到達時にworkloadがどう失敗するかを決めます。CPU limitは主にthrottle、memory limitはOOM、local storage limitは計測後のeviction、PID limitは新規process作成失敗につながるため、同じ「上限」でもapplicationへの影響が違います。

Requestはschedulerの配置判断と競合時の配分・evictionに使われます。Limitはruntime側のceilingですが、node全体の余力や他namespaceの使用量は決めません。Workload単位、tenant aggregate、node capacityの三つを同じbudget contractへ結びます。

Admissionで値があることを確認しても、runtimeがその値をcgroup等へ反映した証拠にはなりません。Quota status、Podの実効QoS・resize状態、node allocatable・pressure、runtime limit、OOM／eviction eventを継続して観測し、取得不能を「枯渇なし」に変えません。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は「できてはいけないこと」が実際に起きないかを確認する項目です。実施済みの診断結果ではありません。

- CPU／memoryのrequestまたはlimitを省略したPod、init container、sidecarを作成できないか。Platformのdefault注入で未review値を通常の合格にしていないか。
- Requestがlimitより大きい、単位を誤った、zeroまたはpolicy範囲外のquantityを受け入れないか。
- Namespace quotaを越えるPod作成、replica増加、rolling updateのsurge、Job／CronJobの同時実行、PVC・Service等のobject増加を拒否または明示した失敗状態にできるか。
- `/resize`や別のupdate経路で、作成時にreviewしたCPU／memory budgetを越えられないか。
- Ephemeral／debug containerを追加してresource accountingを迂回できないか。採用platformで個別limitを指定できない場合、Pod budgetまたはdebug禁止へ接続しているか。
- CPU limit到達をPod停止と誤認せずthrottleを観測できるか。Memory limit到達時のOOM killとnode pressure evictionを区別できるか。
- Fork bombでPodのPID上限、nodeのPID reservation、`pid.available` thresholdを越えて他workloadやsystem processを停止できないか。
- Log、writable layer、`emptyDir`、削除後も開かれたfile、inode消費でlocal storage計測や上限を迂回できないか。
- ResourceQuotaの合計がnode・failure domainのallocatableを越え、全tenantが同時にrequestした時に配置不能やsystem starvationにならないか。
- Kubelet／runtime設定不一致、unsupported resource、quota controller遅延、metrics欠落、event収集停止を「上限が効いている」と扱っていないか。
- Priorityや例外を使って、一般workloadがsystem reservationや他tenantのcapacityを継続的に奪えないか。

## 境界と受け渡し

- Process・kernel・host・filesystem権限は[PSB-CONTAINER-005](../psb-container-005-workload-privilege-confinement/README.md)が扱います。
- Workloadの通信範囲は[PSB-CONTAINER-006](../psb-container-006-workload-network-segmentation/README.md)が扱います。
- OOM、fork、disk書込み等の予期しないruntime挙動とsensor healthは[PSB-CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)へ渡します。
- Autoscaling、冗長化、capacity planning、SLOは、このcontrolのresource isolationを入力にする別のavailability設計です。

## 参照資料とマッピング

- [REF-WORKLOAD-RESOURCE-BOUNDS-001](../../../../sources/README.md#ref-workload-resource-bounds-001)
- [NIST SP 800-190](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)
- [成果物間の関係](../../../../mappings/pilot.yaml)
- [Framework mapping](../../../../mappings/frameworks.yaml)
- [横断分析](../../../../docs/ANALYSIS_LENSES.md)
