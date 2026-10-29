# PSB-CONTAINER-005 Workload privilege confinement

**Workloadが侵害されても、不要なroot・kernel・hostの権限を使えないか。**

## なぜ必要か

例えば、署名済みのimageでも、privileged containerとして動かせばhostの機能へ届きます。Imageを受け入れる判断と、実行中のprocessに渡す権限は別に確認します。

## 満たすべきこと

1. **実行経路を漏らさない。** Main、init、sidecar、ephemeral、debugなど最終的に動く全containerを、対象OSとruntimeに合う同じ制限で評価する（WORKLOAD-CONFINE-1）。
2. **processとhostの権限を絞る。** Privileged・root実行と権限昇格を既定で拒否し（WORKLOAD-CONFINE-2）、不要なcapabilityを落としてsyscall・MAC profileを適用する（WORKLOAD-CONFINE-3）。Host namespace、path、device、port、runtime socketも既定で拒否する（WORKLOAD-CONFINE-4）。
3. **書込先と認証情報を限定する。** Imageのroot filesystemを読み取り専用にし、必要な書込みだけを用途が決まったvolumeへ許す（WORKLOAD-CONFINE-5）。Control-plane credentialは不要なworkloadへ渡さず、必要なら専用identity、権限、audience、期限を絞る（WORKLOAD-CONFINE-6）。
4. **実行前に強制する。** 作成・更新・debug追加後の最終状態を確認し、policy欠落・評価失敗・未対応形式を通常の許可へ変えない。例外は対象・owner・期限を限定する（WORKLOAD-CONFINE-7）。

## 制限を組み合わせる

推奨する順序は、workloadが実際に必要とする権限を決め、platformの組込みprofileで共通baselineを強制し、足りない特性だけを小さな追加policyで補うことです。製品名やmanifest fieldからcontrolの意味を逆算しません。

## 一つにまとめる境界

次は、application code executionからhostやkernel authorityへ進む同じ失敗経路を制限するため、一つのconfinement profileで扱います。

- Process identity、root、privileged mode、privilege escalation
- Linux capability、seccomp、AppArmor／SELinux等のMAC
- Host namespace、host process、host path、device、host port、runtime／node管理socket
- Image root filesystemと明示したwritable volume
- Workloadへ自動的に渡るcontrol-plane credential
- Main、init、sidecar、ephemeral、debugを含む実行経路

CPU・memory・PID・storageの枯渇は、request／limitだけでなくquota、node capacity、eviction、scheduling、runtime enforcementを扱うavailability設計です。NetworkはCNI、identity、ingress／egress、DNS、service mesh、external boundaryを扱います。どちらもこのpatternへ詰め込みません。

## 権限制限の対象と例外を決める

| 要素 | 決めること | 証拠 |
|---|---|---|
| Scope | Cluster、namespace、workload class、OS、runtime class | 対象inventory、namespace／selector、除外一覧 |
| Process | UID／user、privileged、escalation | Final workload、admission decision |
| Kernel | Capability allowlist、seccomp、MAC | Profile名・版、runtimeの実効状態 |
| Host attachment | Namespace、path、device、port、管理socket | 拒否policy、例外decision、runtime mount |
| Filesystem | Read-only root、明示したwritable volume | Final mount、volume identity・lifecycle |
| Credential | 自動mountの禁止、必要なidentity・audience・期限 | Service identity、binding、token設定 |
| Enforcement | Create、update、ephemeral／debug、error semantics | Policy版、decision、audit、coverage |

Policy名だけでは不十分です。どのversionのprofileを、どのscopeへ、どのmodeで適用し、何を追加policyへ渡したかを記録します。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| Platform組込みprofile | 共通baselineを低い運用負荷で強制したい場合。製品が定義する固定profileの範囲外は補えず、version差を管理する必要がある |
| Declarative admission policy | Final objectのfieldで判断できる追加条件を強制する場合。外部照会を避けやすいが、CEL／schema／subresource coverageを対象versionで確認する |
| External policy engine／webhook | 複雑な組織policy、外部data、共有ruleが必要な場合。Availability、TLS identity、timeout、failure policy、upgrade compatibilityを所有する |
| Sandbox runtime／dedicated node | Shared kernelでは隔離が不足する高risk workload。起動時間、互換性、運用負荷、配置capacityが増える |
| [IaC・CI検査](../psb-iac-001-infrastructure-change-authorization-and-drift/README.md) | 開発者へ早くfeedbackする場合。Admissionやruntimeの代替にせず、同じprofile版とのdriftを管理する |

## 例外とsystem workload

Node agent、CNI、storage driver、runtime sensor等はhost機能を必要とする場合があります。一般workloadのbaselineを弱める代わりに、専用namespace、service identity、node placement、許可するhost path・capability、owner、期限を分けます。

Namespace、user、runtime classの広い除外は、その主体が作成できる全workloadを除外します。例外は[Security exception lifecycle](../../governance-operations/psb-gov-002-security-exception-lifecycle/README.md)へ接続し、元の不合格を合格へ書き換えません。

組込みprofileの版と適用範囲を明示し、警告だけの設定を拒否と取り違えないようにします。作成・更新・debug追加と、変更処理を通った最終状態を確認します。実行時の設定確認は対象workloadと起動時の判断を結び、検知・調査へ渡します。

製品固有の配置・制約は[既存のKubernetes実装例](../../../../engineering/implementations/kubernetes-psa-cel/README.md)へまとめています。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- Main containerだけが基準を満たす場合、privilegedなinit・sidecar・ephemeral containerを追加できないか。
- Root実行、権限昇格、未承認capability、制限のないseccomp・MAC profileで実行できないか。
- Host namespace、hostPath、device、runtime socketを一般workloadから使えないか。
- Root filesystemを書込み可能に戻す、volumeをhostの機密pathへ向ける操作を拒否するか。
- 不要なservice account tokenが自動で渡されないか。別audienceや過大な権限へ流用できないか。
- Policy評価失敗、未対応OS、期限切れ例外、別API経路を使っても実行できないか。

これらは診断・設計レビューの確認項目であり、実際のclusterで試した結果ではありません。

## フレームワークとの関係

- NIST SP 800-190 §4.4.3: Workloadの実行前に権限・file system・kernel呼出しを制限する設計が部分的に関係します。Kubernetes固有のservice accountや全host接続までこの節から導けるわけではありません。

対象特性は[マッピング](../../../../mappings/frameworks.yaml)にあります。実clusterでの受入拒否やruntimeの強制は未確認です。

## このコントロールの範囲

対象はworkloadの実行時権限と、実行前の強制です。成果物の受入は[CONTAINER-001](../psb-container-001-deployment-artifact-admission/README.md)、node・daemonの管理は[CONTAINER-003](../psb-container-003-container-host-daemon-boundary/README.md)、通信は[CONTAINER-006](../psb-container-006-workload-network-segmentation/README.md)、資源消費は[CONTAINER-007](../psb-container-007-workload-resource-consumption-bounds/README.md)へ渡します。CIやIaCでのmanifest検査は早い発見に役立ちますが、実行直前の強制の代わりにはなりません。

制限の組み合わせと例外の置き方は上の方式説明で選びます。[Kubernetes実装例](../../../../engineering/implementations/kubernetes-psa-cel/README.md)は限定した構成です。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-workload-confinement-001)、[NIST資料](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。

対策同士のつながりは[公開したコンテナを動かし、侵害の広がりを抑える](../../../../engineering/container-deployment-to-response.md)で確認できます。
