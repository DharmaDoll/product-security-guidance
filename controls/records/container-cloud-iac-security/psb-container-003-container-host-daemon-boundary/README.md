# PSB-CONTAINER-003: Container host and daemon boundary

学ぶ：[A runtime socket turns a Pod into a node administrator](learning.md) ·
設計する：[Node runtime and management boundary](../../../../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)

## 問い

Workload、node上のprocess、operator identityのいずれかが侵害されても、container runtime、kubelet、host OSの管理権限へ無制限に進めず、侵害nodeをclusterから切り離せるか。

## できてはいけないこと

Runtime socketやkubelet APIへ到達したworkloadが、別containerの作成・操作、host filesystemへの書込み、credential取得を行えてはいけません。Nodeごとのcredential、daemon設定、plugin、static Pod manifest、service unitを改変し、通常のAPI admissionやauditを迂回できてはいけません。

一つのnodeが侵害された時に、共有credentialや過大なnode権限を使って他nodeやcluster全体へ進めてはいけません。Inventory・patch・設定・auditの取得失敗を「問題なし」にしてはいけません。

## 適用範囲と非適用

Productionまたは共有container nodeのOS image、kernel、container runtimeとshim、kubelet等のnode agent、plugin、管理endpoint・socket、node identity、host上の管理操作、boot trust、更新・隔離・廃棄が対象です。

Workload manifestのprivilege、host mount、service accountは[PSB-CONTAINER-005](../psb-container-005-workload-privilege-confinement/README.md)、network通信は[PSB-CONTAINER-006](../psb-container-006-workload-network-segmentation/README.md)、resource budgetは[PSB-CONTAINER-007](../psb-container-007-workload-resource-consumption-bounds/README.md)が扱います。Control plane全体、developer端末、CI runner、registry、application vulnerabilityは別の主題です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `HOST-1` | Node poolごとに用途、workload sensitivity、owner、OS／kernel／runtime／node agent／pluginの構成を決め、不要なservice・package・対話利用を持ち込まない |
| `HOST-2` | Kernel、runtime、shim、node agent、pluginをsupport中のreview済み版へ保ち、影響範囲を把握してdrain・更新または再作成・rollback・期限超過時の隔離を実行できる |
| `HOST-3` | Runtime・kubelet・debug・metrics等のendpointとsocketを列挙し、必要な主体・network・操作だけへ認証・認可し、workloadから管理socketを利用できないようにする |
| `HOST-4` | Binary、config、service unit、plugin、static workload、credential、runtime state等の保護pathを、承認済みimageまたは変更経路だけが更新でき、symlink・mount・上書き・永続化を検知または拒否する |
| `HOST-5` | Nodeごとに固有のidentityを安全に登録・更新・失効し、node agentのAPI権限を自nodeと割当workloadへ限定する。侵害nodeを隔離・削除し、再登録を新しい信頼判断へ結ぶ |
| `HOST-6` | Rootless／user namespace、LSM、seccomp、kernel module制約、sandboxed runtime等からthreatに合うhost側の隔離を選び、unsupportedまたはfallback時に通常の隔離済み状態として扱わない |
| `HOST-7` | 人とautomationのhost管理権限、接続元、期限、承認、break-glass、操作記録を限定し、runtime socket等による監査迂回を残さない |
| `HOST-8` | Node image、boot・attestation、component、設定、endpoint、identity、auditの実効状態と収集healthを継続確認し、未対応・未取得・古い証拠を合格へ変換しない |

## 実装判断の羅針盤

最初に「安全なnode」の抽象的なチェックリストではなく、node poolの役割、実行するworkload、管理経路、更新方式、侵害時の切離し方を決めます。Managed serviceではproviderが持つ境界と利用者が設定・観測できる境界を分けます。Self-managed nodeではOS imageからruntime、kubelet、pluginまでを一つのtrusted computing baseとして管理します。

Runtime socketへの書込権限は通常のworkload操作より強く、Kubernetes APIのadmissionやauditを通らない経路になり得ます。Kubelet API、static Pod manifest、containerd pluginも同様に別の強制点です。通常のAPI RBACだけでnode管理面を保護した扱いにしません。

固定したfile mode、patch日数、rootlessの採用を全platformへ配るのではなく、対象runtime・distribution・providerの仕様へ落とします。設定ファイルだけでなく、実際のlistener、socket owner、process引数、component version、node credential、割当権限、変更記録を確認します。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は「できてはいけないこと」が実際に起きないかを確認する項目です。実施済みの診断結果ではありません。

- WorkloadからDocker／containerd／CRI socket、NRI socket、kubelet API、debug endpointへ到達し、別containerの作成・exec・filesystem取得ができないか。
- Kubeletのanonymous access、`AlwaysAllow`相当のauthorization、広い`nodes/proxy`権限、publicまたは一般workload networkからの到達が残っていないか。
- Static Pod manifest、kubelet／runtime config、service unit、runtime binary、CNI／NRI／snapshotter plugin、credentialを一般userやworkloadが書き換えられないか。Symlinkや別mountで検査を迂回できないか。
- Node credentialを別nodeへ複製し、既存node名で再登録できないか。侵害nodeのcredential失効後もsession、certificate、bootstrap経路が使えないか。
- Compromised nodeが他node向けSecret、Pod、service account token、保護labelを取得・変更できないか。Node固有の認可と登録制限が有効か。
- Version inventoryからkernel、runtime、shim、kubelet、pluginが漏れず、unsupported版、patch取得失敗、更新期限超過を正常状態にしないか。
- Rootless／user namespace、LSM、seccomp、sandboxed runtimeがunsupportedまたは起動失敗した時に、rootful／unconfinedなruntimeへ黙ってfallbackしないか。
- Debug／metrics／pprof endpointが認証なしで機微情報を返したり、外部から資源を消費させられたりしないか。
- Hostへの直接login、sudo、runtime socket操作、break-glass、image／service変更が、個人またはautomation identityと時刻へ結び付いて残るか。Audit停止や転送不達を検知できるか。
- Node imageやboot measurementを信頼条件に使う場合、古い・別pool・失敗したattestationで参加できないか。提供されないplatformをattestedとして扱っていないか。
- 侵害nodeをcordon／drainしただけでcredential・runtime state・local data・再登録経路が残らないか。隔離、削除、再作成、証跡保全の順序を確認できるか。
- Collector権限不足、対象node欠落、pagination不足、stale cache、schema変更、command timeoutを「逸脱なし」に変換していないか。

## 境界と受け渡し

- Workload側でruntime socket mountやhostPathを拒否する意図は[PSB-CONTAINER-005](../psb-container-005-workload-privilege-confinement/README.md)から受け取り、このcontrolはhost側のsocket、endpoint、node TCBを守ります。
- Runtime sensorのinstall権限、kernel互換性、host上の保護はこのcontrolが入力を渡し、event・drop・通知は[PSB-CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)が扱います。
- Host componentの脆弱性検出結果はscannerのidentityとhealthを含めて[PSB-DETECT-001](../../detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)から受け取ります。
- 侵害nodeの封じ込め、影響範囲、復旧判断はGovernance／Operationsへ渡します。

## 参照資料とマッピング

- [REF-CONTAINER-HOST-DAEMON-001](../../../../sources/README.md#ref-container-host-daemon-001)
- [NIST SP 800-190](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)
- [成果物間の関係](../../../../mappings/pilot.yaml)
- [Framework mapping](../../../../mappings/frameworks.yaml)
- [横断分析](../../../../docs/ANALYSIS_LENSES.md)

この主題は対象platformを決めないと、設定path、service、API、更新・attestation方法が確定しません。今回は具体実装を作らず、対象を選ぶためのpatternまでを正本にします。理由と実装開始条件は[移行記録](../../../../docs/CONTAINER_HOST_DAEMON_MIGRATION.md)に残しています。
