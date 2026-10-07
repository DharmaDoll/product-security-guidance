# PSB-CONTAINER-003 Container host and daemon boundary

**Workloadや管理者の権限から、container runtime・kubelet・host全体を操作できないか。**

例えば、workloadからruntime socketへ届くと、通常のAPIによる許可や監査を通らずに別containerを操作できます。一つのnodeが侵害されたとき、他nodeへ広がる権限を止め、そのnodeを信頼から外せることも必要です。

## 満たすべきこと

1. **管理するnodeを把握し、更新する。** Node poolごとに用途、owner、OS・kernel・runtime・agent・pluginの構成を決め（HOST-1）、対応中の版へ更新する。更新できないnodeの隔離と復旧手順も決める（HOST-2）。
2. **hostの管理経路を守る。** Runtime・kubelet・debug等のendpointやsocketを列挙し、使える主体と操作を限定する（HOST-3）。Binary、設定、plugin、static workload、認証情報を未承認の変更から守る（HOST-4）。人とautomationのhost管理権限も限定し、操作を追えるようにする（HOST-7）。
3. **nodeの権限と隔離を保つ。** Nodeごとに別のidentityを使い、そのnodeに必要なAPI権限だけを与える。侵害時は失効・削除し、再登録を新しい信頼判断へ結び付ける（HOST-5）。選んだhost側の隔離が未対応・失敗した場合は、隔離できたものとして動かさない（HOST-6）。
4. **現在の状態を確認する。** Node image、component、設定、endpoint、identity、監査の実効状態と収集の健全性を確認し、欠落・古い・部分的な証拠を合格にしない（HOST-8）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- Workloadからruntime socketやkubelet APIへ届き、別containerの作成・操作やhostの変更ができないか。
- Static workload、runtime設定、plugin、node認証情報を未承認の主体が変更できないか。
- 侵害nodeのidentityで他nodeの情報を取得できないか。失効後も再登録や残ったsessionで操作できないか。
- 隔離機能が未対応・起動失敗したとき、弱い設定へ黙って戻らないか。
- Nodeの更新期限超過、監査停止、収集対象の欠落を「問題なし」としていないか。
- Nodeを切り離した後、認証情報・実行状態・再登録経路を残していないか。

これらは診断・設計レビューの確認項目であり、実nodeでの拒否や隔離を確認した結果ではありません。

## このコントロールの範囲

対象は共有・本番nodeのOS、runtime、kubelet、管理経路、node identity、更新と隔離です。Workload自身の権限制限は[CONTAINER-005](../psb-container-005-workload-privilege-confinement/README.md)、通信の制限は[CONTAINER-006](../psb-container-006-workload-network-segmentation/README.md)、実行後の異常検知は[CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)へ渡します。Nodeの侵害が疑われる場合、そのnode上のsensorによる「異常なし」だけでは安全と判断しません。

管理対象と設定・更新方式は[engineering](../../../../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)で選びます。対象platformを決めるまで具体実装は追加しません。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-container-host-daemon-001)、[NIST資料](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)、[移行記録](../../../../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#container-host-daemon-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
