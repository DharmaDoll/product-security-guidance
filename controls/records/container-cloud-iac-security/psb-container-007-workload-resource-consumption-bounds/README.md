# PSB-CONTAINER-007 Workload resource consumption bounds

**一つのworkloadが故障・侵害されても、共有資源を使い尽くさないか。**

## なぜ必要か

例えば、ログを書き続ける処理は、CPU・memoryの上限があってもnodeのdiskやinodeを枯渇させます。一つのcontainerの制限だけでなく、namespace全体とnodeに残す余力まで確認します。

## 満たすべきこと

1. **資源の予算を決める。** CPU、memory、PID、local storage、object数の用途、owner、上限到達時の動きを決める（RESOURCE-1）。Main、init、sidecar、debugと、logや書込領域など消費経路を漏らさない（RESOURCE-2）。
2. **異なる上限を混同しない。** 配置判断に使うrequest、実行時のlimit、throttle、OOM、evictionを別に扱う（RESOURCE-3）。Namespace単位の合計・object数を制限し（RESOURCE-4）、PIDとlocal storageの上限・計測範囲も確認する（RESOURCE-5）。
3. **nodeの余力と実際の動きを確かめる。** Namespaceの予算をnodeのcapacityやsystem用の予約と照合する（RESOURCE-6）。作成、更新、scale、resize、debugでも最終的な予算を強制し、実効limit、資源枯渇、観測失敗を区別する（RESOURCE-7）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- Main以外のcontainerやdebug経路でrequest・limitを省略し、未レビューの既定値を使えないか。
- Replica増加、Jobの同時実行、Pod・PVC等の作成でnamespace予算を越えられないか。
- 更新やresizeで作成時の上限を越えられないか。
- Fork、log、writable layer、`emptyDir`、inode消費でPID・diskの上限を迂回できないか。
- CPUのthrottle、memoryのOOM、node pressureによるevictionを別の結果として観測できるか。
- Quotaの合計がnodeの余力を超える、runtimeが設定を適用しない、metricsが欠ける場合に合格扱いしないか。

これらは診断・設計レビューの確認項目であり、実際のclusterで試した結果ではありません。

## フレームワークとの関係

- NIST SP 800-190 §4.4.3: 一つのcontainerが周囲のworkloadへ割り当てた資源を使い尽くさないよう、消費経路と実行時の上限を考える部分を支えます。Kubernetesのrequests・limits・ResourceQuotaやnode容量の具体値を、この節が指定するわけではありません。

対象特性と限界は[マッピング](../../../../mappings/frameworks.yaml)にあります。実環境のquota・cgroup・storage圧迫と拒否は未確認です。

## このコントロールの範囲

対象はworkload、namespace、nodeの資源消費と共有capacityです。Process・hostの権限は[CONTAINER-005](../psb-container-005-workload-privilege-confinement/README.md)、通信範囲は[CONTAINER-006](../psb-container-006-workload-network-segmentation/README.md)、異常な消費の検知は[CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)へ渡します。Autoscalingや事業上のavailability目標は別に判断します。

予算とnodeの余力の合わせ方は[engineering](../../../../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/README.md)で選びます。[Kubernetes実装例](../../../../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)は限定した構成です。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-workload-resource-bounds-001)、[NIST資料](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
