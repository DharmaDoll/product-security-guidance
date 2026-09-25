# A trusted image can still become a privileged process

[コントロール記録](README.md) ·
[設計パターン](../../../../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/README.md) ·
[Kubernetes実装](../../../../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/implementations/kubernetes-psa-cel/README.md)

## シナリオ：署名済みimage内のapplicationが侵害される

署名とprovenanceを検証した正規のweb applicationをdeployしました。数週間後、そのapplicationの入力処理に欠陥が見つかり、攻撃者がcontainer内で任意のcommandを実行します。

Imageが正規だったことは、実行processへ渡した権限を小さくしません。Containerがrootかつprivilegedで、host filesystemやruntime socketをmountしていれば、攻撃者はapplicationの権限からnode管理へ進めます。逆に、non-root、権限昇格なし、capabilityなし、host接続なし、read-only root filesystem、runtime既定のseccompという状態なら、同じapplication欠陥が直ちにhost権限になる経路を減らせます。

## Containerという名前は境界の強さを決めない

Containerはhost kernelを共有します。`privileged`、host namespace、hostPath、runtime socket等を許すと、通常のcontainer隔離を意図的に弱めます。Non-rootだけでも十分ではありません。Linux capability、setuidによる昇格、system call、mountしたpathという別の権限経路が残るためです。

Main containerだけを確認しても、先に動くinit container、platformが追加するsidecar、障害調査で追加するephemeral containerが強い権限を持てば、同じPodの境界は越えられます。

## 設定値と強制点を分ける

Manifestに安全な値が書かれていることと、その値以外では実行できないことは別です。CIのlintは早く気付くために使い、cluster admissionはcontrollerが生成した最終Podと直接作成されたPodを拒否するために使います。Runtime側でprofileが実際に適用されたかは、実行後の観測へ引き継ぎます。

KubernetesのPod Security Standardsは広い共通profileを提供しますが、read-only root filesystemや不要なservice account tokenの禁止までは一括して保証しません。組込みprofileが担う範囲と、追加policyで補う範囲を分けます。

## 振り返りで問うこと

- 署名済みimageであることを、強いruntime権限を許す理由にしていないか。
- Main、init、sidecar、ephemeral、debugの全経路を同じ基準で見ているか。
- Non-root以外に、capability、seccomp、MAC、host接続、書込領域の経路が残っていないか。
- 一般workloadとhost機能を必要とするsystem workloadを、同じ広い例外namespaceへ入れていないか。
- IaCの検査成功を、live clusterでの拒否確認と取り違えていないか。
- Network到達範囲やresource枯渇まで、この一つのprofileで解決したことにしていないか。

この教材は[NIST SP 800-190とKubernetes資料の採否](../../../../sources/README.md#ref-workload-confinement-001)を使ったリポジトリでの解釈です。個別clusterへの導入済み状態は示しません。

\n