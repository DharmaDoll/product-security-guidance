# A runtime socket turns a Pod into a node administrator

## シナリオ

運用担当者は障害調査を簡単にするため、診断用DaemonSetへ`/run/containerd/containerd.sock`をmountしました。診断imageは通常のapplication namespaceへも配置され、application teamがPodへの`exec`権限を持っています。

Applicationが侵害され、攻撃者は診断Podへ移動します。Runtime socketを使って別containerを操作し、host filesystemをmountした新しいcontainerを作ります。この操作は通常のKubernetes APIで新しいPodを作らないため、admission policyやAPI auditだけを見ても止められません。攻撃者はnode上のkubelet credentialとstatic Pod manifestへ到達し、nodeを継続的な足場にします。

## 何が境界だったか

Container runtime socketは、単なるlocal IPC fileではありません。Socketのwrite権限を持つ主体は、runtimeが許すcontainer作成・exec・mount等を依頼できます。Rootful runtimeでは、その権限がhost管理に近い場合があります。

Kubelet APIもnodeとcontainerへ強い操作を提供します。`nodes/proxy`のような一見readに見える権限から、kubelet endpointを通じてcontainer操作へ届く場合があります。Static Pod manifestはAPI serverを経由せずkubeletが直接読み込むため、書込権限を得ると通常のadmissionを迂回できます。

このシナリオで守る資産は、nodeのruntime authority、node credential、host filesystem、同じnode上のworkload、clusterがnodeを信頼する条件です。脅威主体は侵害されたapplication processから始まり、診断用workload、runtime socket、host、node identityという信頼境界を越えます。

## 用語

- **Node trusted computing base**：Workloadの隔離を成立させるOS image、kernel、runtime、shim、kubelet等のnode agent、plugin、設定、credential。
- **Runtime socket**：Kubeletや管理clientがcontainer runtimeを操作するlocal endpoint。File permissionだけでなく、誰がmount・接続できるかを確認する。
- **Kubelet API**：Node上のPod、log、exec、metrics等へ接続するHTTPS API。API serverとは別の認証・認可・network境界を持つ。
- **Static Pod**：Kubeletがlocal manifest等から直接管理するPod。通常のAPI admissionを通るPodと同じ強制経路ではない。
- **Node identity**：Node agentがclusterへ自nodeとして接続するcredentialと名前・pool・lifecycleの対応。
- **Rootless／user namespace**：Daemonまたはcontainerのhost上の権限を減らす方式。対応機能やresource controllerが異なり、採用だけで全境界を満たすわけではない。

## 悪用経路を分解する

1. Applicationまたはoperator identityが侵害される。
2. Runtime socket、kubelet API、debug endpoint、hostPath、static manifest等のnode管理経路を発見する。
3. 認証なし、広いgroup、workload mount、過大なRBAC、書込可能pathのいずれかで境界を越える。
4. Runtime操作、host file書込、credential取得によってnodeを管理する。
5. Node credentialやplugin、serviceを使って永続化する。
6. Node固有でないcredentialや広いAPI権限があれば、他node・Secret・workloadへ広がる。
7. Inventory・audit・collectorが不完全だと、侵害nodeを正常なpool memberとして扱い続ける。

## よくある誤解

### 「Pod Securityをrestrictedにしたのでhostも安全」

Pod Securityはworkload specの一部を制限します。既存の診断Pod、runtime socket自体のowner、kubelet API、host service、node credential、static Pod pathの保護は別に確認します。

### 「SocketはUnix fileなので外部公開APIより安全」

Network非公開でも、mountされたworkloadや広いlocal groupから利用できれば管理権限が移ります。Path、owner、modeに加え、mount inventoryと実際の接続主体を見ます。

### 「最新imageを配ったのでpatch済み」

Node上で実行中のkernel、runtime、shim、kubelet、pluginが期待版であること、更新失敗したnodeがpoolに残らないことが必要です。Image定義だけでは実効版を証明しません。

### 「Rootlessならcontainer escapeは問題にならない」

Rootlessはdaemonとcontainerのhost権限を減らしますが、kernel共有、対応しないstorage・network・cgroup機能、rootful daemonの併存、設定fallbackは残ります。Threatとplatformに対する具体的な効果を確認します。

### 「NodeがReadyなら信頼できる」

Readyはnodeの完全性、patch、credential漏えい、設定、boot chainを証明しません。侵害nodeを隔離し、credentialを失効し、新しいnodeを別の信頼判断で登録できる必要があります。

## 判断基準

次の質問へ具体的に答えられる状態を目指します。

- Node poolの用途と、信頼するOS・kernel・runtime・agent・pluginは何か。
- Runtime socket、kubelet、debug／metrics、SSH等へ、どのidentityがどのnetworkから何をできるか。
- Workloadと一般userが書き込めないbinary、config、service、plugin、credential、static manifestはどれか。
- Node identityはどう発行・更新・失効し、侵害nodeの権限をどこまでに閉じ込めるか。
- 更新失敗、isolation機能のunsupported、collector停止をどの状態として扱うか。
- Nodeを隔離・削除・再作成した後、credential、local data、再登録経路が残っていないと何で確認するか。

次に[control](README.md)で必要な特性を確認し、[pattern](../../../../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)でplatformへ落とす設計を選びます。
