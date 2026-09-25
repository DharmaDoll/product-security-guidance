# ENG-CONTAINER-006: Node runtime and management boundary

## 利用場面と推奨構造

Container nodeのruntime、kubelet等のnode agent、host OSを、workloadと日常のoperator操作から分離し、一nodeの侵害をcluster全体へ広げないための設計です。

```text
reviewed node image + supported component set
                    |
                    v
        secure enrollment / unique node identity
                    |
          +---------+----------+
          |                    |
          v                    v
 runtime / kubelet API     host management path
 socket + authz + network  identity + approval + audit
          |                    |
          +---------+----------+
                    v
       node pool with one sensitivity contract
                    |
                    v
 effective version / endpoint / config / identity / audit evidence
                    |
                    v
       isolate -> revoke -> replace -> re-enroll
```

Node imageの定義、clusterへの参加条件、実行中の管理面、観測、侵害後の切離しを一つのlifecycleとして扱います。設定を一度確認したことを、稼働nodeの現在状態や再登録時の信頼へ一般化しません。

## Node trust contract

| 要素 | 決めること | 主な証拠 |
|---|---|---|
| Pool purpose | Workload sensitivity、tenant、環境、owner、failure domain | Node pool定義、placement、inventory |
| Trusted components | OS image、kernel、runtime、shim、node agent、CNI／NRI／CSI／snapshotter等のplugin | Exact version、image identity、support情報、実process |
| Management surfaces | Runtime／NRI socket、kubelet、debug、metrics、SSH、provider session | Listener、socket、mount、RBAC、firewall、session policy |
| Protected state | Binary、config、service unit、plugin、static workload、credential、runtime data | Image manifest、ownership、mount、drift、change record |
| Node identity | Bootstrap、node name・poolとのbinding、rotation、API権限、revocation | Certificate／workload identity metadata、authorizer、admission、denial probe |
| Isolation | User namespace／rootless、LSM、seccomp、module policy、sandboxed runtime | Effective runtime・kernel state、unsupported／fallback状態 |
| Replacement | Cordon、drain、isolate、credential失効、local state処理、再作成 | Incident・rollout record、old-node denial、new enrollment |
| Observation | Coverage、freshness、collector authority、欠測、audit delivery | Node denominator、last success、error、central audit receipt |

## 境界ごとの設計

### 1. Node imageとcomponent set

Production nodeは目的を絞り、不要なinteractive tool、package、service、host上のapplicationを減らします。Minimalはpackage数だけでは決まりません。Node更新、診断、sensor、network、storageに必要なcomponentを明示し、ownerとsupport期間を持たせます。

Kernelだけでなくcontainer runtime、low-level runtime、shim、kubelet等のagent、root権限で動くpluginをinventoryへ含めます。Nodeをin-place patchする方式でも、immutable imageを再作成する方式でも、期限超過したnodeをpoolから外す動作とrollbackを設計します。

### 2. Runtime・kubelet・補助endpoint

Runtime socketのwrite権限はhost管理権限として扱います。Containerdではruntime socketだけでなくNRI、plugin、debug、metrics endpointを確認します。Debugやheap profileは機微情報を含み、CPU／memoryを消費させる可能性があるため、通常のapplication networkへ公開しません。

KubeletはAPI serverとは別のHTTPS endpointを持ちます。Anonymous accessを無効にし、certificateまたはwebhookで認証し、Webhook authorization等の対象platformが提供する認可を使います。`nodes/proxy`等の権限、node portへのnetwork到達、API serverからnodeへの経路を一組でreviewします。

Socket modeやfirewall ruleの宣言だけではなく、実listener、socket metadata、group member、workload mount、接続拒否を確認します。Remote Docker API等を有効にする場合は、private reachability、相互認証、細粒度の認可、credential lifecycleを別々に確認します。

### 3. Host上の変更経路

Runtime binary、config、system service、plugin、static Pod manifest、node credentialへ書き込める主体を、node image buildまたは承認済み更新agentへ限定します。一般user、workload、診断toolが直接変更できる構成にしません。

Static Podやruntime socketによる操作は通常のAPI admissionを迂回できます。Host pathを書込不可にするだけでなく、symlink、別mount namespace、package post-install、unit override、environment file、plugin directoryから同じ結果へ到達できないかを確認します。

### 4. Node identityと侵害範囲

Nodeごとに固有のcredentialを使い、node name・pool・instance lifecycleへ結びます。Bootstrap credentialを継続利用せず、rotation・expiry・revocationを設計します。KubernetesではNode authorizerとNodeRestriction等を用い、kubeletが自nodeと割当workloadに必要な範囲を越えてAPIを操作しないようにします。

NodeのReady状態をidentityや完全性の証明にしません。侵害時にはnetwork隔離、scheduling停止、workload退避、node credential失効、node削除、local data処理を分けて実行し、同じidentityの再参加を拒否します。

### 5. Host側の隔離

Workloadのsecurity contextは[Workload privilege confinement](../workload-privilege-and-host-boundary/README.md)で決めます。このpatternは、それを実現するkernel、runtime、LSM、seccomp、user namespace、sandboxed runtimeの提供状態とfallbackを扱います。

Rootless runtime、user namespace、VM／microkernel sandboxには、network、storage、cgroup、device、性能、debug、observabilityの差があります。単一の方式を普遍的な必須値にせず、workload threatとplatform supportに合わせます。Featureがunsupportedまたは起動失敗した時に、弱いruntime classへ黙ってfallbackさせません。

### 6. 管理と観測

Host管理は個人または一つのautomation identity、対象node／pool、操作、接続元、期限へ限定します。恒久的な共有SSH keyや広いlocal groupを既定にせず、provider sessionや短期credentialを使う場合も実際のhost権限とauditを確認します。

設定値のsnapshotと稼働状態を分けます。少なくともnode数の分母、実component version、listener／socket、credential lifecycle、isolation、変更記録、audit delivery、collector errorを同じ期間へ結びます。取得できない項目を空欄の合格にしません。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| Immutable／container-optimized node image | Nodeを再作成でき、host上の固有状態を持たない場合。Driftを減らせるがimage build、rollout、emergency diagnosisを設計する必要がある |
| Self-managed Linux + containerd | OS、systemd、runtime、plugin、kubeletを自組織が管理する場合。観測と設定自由度が高い一方、patch・credential・plugin・node replacementの責任も持つ |
| Docker rootless／userns-remap | Docker daemon authorityを減らす必要があり、storage・network・cgroup等の制約を受け入れられる場合。Rootful daemonの併存とresource enforcementを別途確認する |
| Managed Kubernetes node pool | ProviderがOS imageやagentの一部を管理する場合。責任分界、release channel、upgrade、node access、証拠API、managed control planeの非可視範囲を明示する |
| Sandboxed／VM-backed runtime | Untrustedまたは異なるsensitivityのworkloadをshared kernelから分ける場合。Startup、density、device、network、observability、costが変わる |
| Boot measurement／node attestation | Node image・firmwareの期待値をcluster参加条件へ使える場合。Hardware／cloud capability、reference measurement、freshness、replacementとの統合が必要 |

## 導入順序

1. Production node pool、workload sensitivity、管理者、runtime、node agent、全pluginをinventoryする。
2. Runtime／kubelet／debug／metrics／SSH等のsurfaceと、socket・listener・network・identity・操作を対応付ける。
3. Node image、component support、protected path、更新または再作成の契約を決める。
4. Unique node identity、bootstrap、API最小権限、rotation、revocation、再登録条件を決める。
5. Workload threatに応じてrootless／user namespace、LSM、seccomp、sandboxed runtime、boot trustを選び、fallbackを拒否する。
6. 隔離poolでsocket mount、kubelet access、static workload改変、stolen node credential、unsupported version、collector停止を試す。
7. 段階的にnodeを入れ替え、old nodeの権限拒否、workload再配置、local state、audit deliveryを確認する。
8. Version、endpoint、identity、drift、audit、collector healthを継続照合し、期限超過nodeを自動または承認付きで隔離する。

## 失敗経路

- Kubernetes APIのRBACだけを確認し、runtime socket、kubelet API、static Podという迂回経路を残す。
- `/run/containerd/containerd.sock`だけを確認し、NRI、debug、metrics、plugin directory、別runtime endpointを見落とす。
- Node image manifestが正しいため、稼働kernel・runtime・shim・agentも同じだと推定する。
- RootlessまたはLSMの設定項目があるだけで、実効状態やunsupported fallbackを確認しない。
- `Ready`、fresh boot、providerの一般的な認証をnode trustと同一視する。
- Cordon／drainで封じ込めが終わったと扱い、credential、network、local data、再登録を残す。
- Collectorが読めなかったnodeやfieldを、逸脱のないnodeとして集計する。
- Hardware attestationを全platformへ必須化するか、providerが公開しないため無条件に安全とする。

## 具体実装をまだ置かない理由

このpatternの変更箇所は、OS distribution、containerd／Docker／CRI-O、Kubernetes distribution、managed service、node image build、identity、network、attestation capabilityで変わります。Provider-neutralな`policy.json`と合成`host-evidence.json`を用意しても、live socket、listener、process、credential、patch、auditを強制・観測できません。

実装は、少なくとも次を一組にして選べる時に追加します。

- 対象OS image、kernel、runtime、node agent、pluginとsupport版
- Self-managedまたはmanaged providerの責任分界
- 変更するimage build、service、runtime／kubelet config、identity、network policy
- 使い捨てnode poolで行う拒否試験と、更新・隔離・rollback手順
- 稼働nodeから取得できるversion、endpoint、credential、audit、collector healthの証拠

Docker rootlessだけ、containerd file modeだけ、Kubernetes kubelet設定だけを置くと、別の管理経路を残したままcontrol全体の代表実装に見えます。対象が決まった時点で、限定したscopeを名前とREADMEの冒頭に示して実装します。

## このpatternの範囲

このpatternはproduction／shared container nodeのhost・runtime・node agentと管理面を扱います。Control plane datastore、cluster-wide administrator lifecycle、cloud account、developer endpoint、CI runner、workload spec、application availabilityは各隣接領域の責任です。

- [Control](../../../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)
- [教材](../../../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/learning.md)
- [Workload privilege confinement](../workload-privilege-and-host-boundary/README.md)
- [Runtime detection to triage](../runtime-detection-to-triage/README.md)
- [参照資料と採否](../../../sources/README.md#ref-container-host-daemon-001)
- [移行記録](../../../docs/CONTAINER_HOST_DAEMON_MIGRATION.md)
