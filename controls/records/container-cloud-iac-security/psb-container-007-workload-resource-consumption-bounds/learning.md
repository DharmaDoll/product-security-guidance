# One log loop can exhaust a shared node

[コントロール記録](README.md) ·
[設計パターン](../../../../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/README.md) ·
[Kubernetes実装](../../../../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)

## シナリオ：正常なPodがlogを書き続ける

API workloadにCPUとmemoryのrequest／limitを設定しました。入力処理の不具合で同じerrorを高速に出力し続けると、container logとwritable layerがnodeのlocal storageを消費します。CPUとmemoryが制限されていてもdiskやinodeが枯渇し、同じnodeの別workloadがevictされることがあります。

別の欠陥が子processを作り続ける場合は、CPU limitで遅くなってもPIDを使い切れます。Node全体のprocess作成が失敗すれば、他のPodやsystem daemonにも影響します。守る対象は「問題のPodを必ず動かし続けること」ではなく、一つのworkloadの失敗を共有基盤全体へ広げないことです。

## Requestとlimitは別の役割

Requestは主にschedulerが配置先を選ぶ時の予約量です。CPU競合時のweightや、memory pressure時のeviction判断にも影響します。Requestを書いただけでは、workloadがその量を越えて使えないという意味になりません。

CPU limitはkernelによるthrottle、memory limitはOOM killにつながります。Local ephemeral storageは継続的なhard capではなく、kubeletが使用量を計測して超過を検知した後のevictionになる場合があります。PID limitへ達すると新しいprocess作成が失敗します。上限値だけでなく、到達時のapplicationの挙動も設計対象です。

## Pod、namespace、nodeの三段階

ContainerやPodの値は一つのworkloadを扱います。ResourceQuotaはnamespaceのrequest・limit合計やobject数を扱います。しかしquotaはcluster capacityから独立した絶対値で、複数namespaceのquota合計が実capacityへ収まることを保証しません。

Nodeではsystem daemon用の予約、Podへ渡すallocatable、memory・disk・PID pressureのthresholdが必要です。ResourceQuotaが正しくても、node reservationが不足したり、全tenantが同時にbudgetを使ったりすれば、配置不能やevictionは起こります。

## 「上限あり」を実効性と取り違えない

Manifestにlimitがあること、API serverがquotaを数えること、runtimeがcgroup等へlimitを反映すること、nodeがpressureを観測していることは別の証拠です。さらにKubernetes 1.37ではCPU／memoryを実行中のPodでresizeできるため、作成時だけの検査では足りません。

値の存在を確認した後、quotaの`status.used`、実効QoS・resource state、runtime limit、throttle、OOM、eviction、unschedulable、node pressureを観測します。Metricsやeventを取れない状態は、枯渇がない状態ではありません。

## 振り返りで問うこと

- Requestをruntimeの使用上限だと思っていないか。
- CPUとmemory以外に、PID、log、writable layer、`emptyDir`、inode、object数を列挙したか。
- Rolling updateやJobの並列実行を含むpeak時の合計がnamespace budgetへ収まるか。
- Namespace quotaの合計とnode allocatable、system reservation、failure domainの余力が整合するか。
- CPU throttle、OOM kill、node pressure eviction、unschedulableを同じ「resource error」にしていないか。
- Admission設定や自己申告のplatform evidenceを、runtimeでの強制結果にしていないか。

この教材は[NIST SP 800-190とKubernetes資料の採否](../../../../sources/README.md#ref-workload-resource-bounds-001)を使ったリポジトリでの解釈です。個別clusterへの導入済み状態は示しません。
