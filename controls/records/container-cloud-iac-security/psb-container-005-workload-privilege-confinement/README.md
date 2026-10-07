# PSB-CONTAINER-005 Workload privilege confinement

**Workloadが侵害されても、不要なroot・kernel・hostの権限を使えないか。**

例えば、署名済みのimageでも、privileged containerとして動かせばhostの機能へ届きます。Imageを受け入れる判断と、実行中のprocessに渡す権限は別に確認します。

## 満たすべきこと

1. **実行経路を漏らさない。** Main、init、sidecar、ephemeral、debugなど最終的に動く全containerを、対象OSとruntimeに合う同じ制限で評価する（WORKLOAD-CONFINE-1）。
2. **processとhostの権限を絞る。** Privileged・root実行と権限昇格を既定で拒否し（WORKLOAD-CONFINE-2）、不要なcapabilityを落としてsyscall・MAC profileを適用する（WORKLOAD-CONFINE-3）。Host namespace、path、device、port、runtime socketも既定で拒否する（WORKLOAD-CONFINE-4）。
3. **書込先と認証情報を限定する。** Imageのroot filesystemを読み取り専用にし、必要な書込みだけを用途が決まったvolumeへ許す（WORKLOAD-CONFINE-5）。Control-plane credentialは不要なworkloadへ渡さず、必要なら専用identity、権限、audience、期限を絞る（WORKLOAD-CONFINE-6）。
4. **実行前に強制する。** 作成・更新・debug追加後の最終状態を確認し、policy欠落・評価失敗・未対応形式を通常の許可へ変えない。例外は対象・owner・期限を限定する（WORKLOAD-CONFINE-7）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- Main containerだけが基準を満たす場合、privilegedなinit・sidecar・ephemeral containerを追加できないか。
- Root実行、権限昇格、未承認capability、制限のないseccomp・MAC profileで実行できないか。
- Host namespace、hostPath、device、runtime socketを一般workloadから使えないか。
- Root filesystemを書込み可能に戻す、volumeをhostの機密pathへ向ける操作を拒否するか。
- 不要なservice account tokenが自動で渡されないか。別audienceや過大な権限へ流用できないか。
- Policy評価失敗、未対応OS、期限切れ例外、別API経路を使っても実行できないか。

これらは診断・設計レビューの確認項目であり、実際のclusterで試した結果ではありません。

## このコントロールの範囲

対象はworkloadの実行時権限と、実行前の強制です。成果物の受入は[CONTAINER-001](../psb-container-001-deployment-artifact-admission/README.md)、node・daemonの管理は[CONTAINER-003](../psb-container-003-container-host-daemon-boundary/README.md)、通信は[CONTAINER-006](../psb-container-006-workload-network-segmentation/README.md)、資源消費は[CONTAINER-007](../psb-container-007-workload-resource-consumption-bounds/README.md)へ渡します。CIやIaCでのmanifest検査は早い発見に役立ちますが、実行直前の強制の代わりにはなりません。

制限の組み合わせと例外の置き方は[engineering](../../../../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/README.md)で選びます。[Kubernetes実装例](../../../../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/implementations/kubernetes-psa-cel/README.md)は限定した構成です。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-workload-confinement-001)、[NIST資料](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
