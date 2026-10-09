# PSB-CONTAINER-003 Container host and daemon boundary

**Workloadや管理者の権限から、container runtime・kubelet・host全体を操作できないか。**

## なぜ必要か

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

## フレームワークとの関係

NIST SP 800-190の次の8節と、host・runtime・nodeの管理境界を照合しています。

| 節 | このControlとの関係 | 限界 |
| --- | --- | --- |
| §4.3.1 | Nodeやruntimeの管理操作を必要な主体へ限る。 | 全clusterの管理権限までは扱えない。 |
| §4.3.5 | Nodeの登録・認証・隔離・除去を一つの信頼の流れとして扱う。 | 実際の登録・再登録とcluster通信は未確認。 |
| §4.5.1 | Host OSの不要な機能や部品を減らす。 | 実hostの部品・processは棚卸ししていない。 |
| §4.5.2 | 機密度に応じた配置とkernel共有の隔離を選ぶ。 | 実際の配置・sandbox強制は未確認。 |
| §4.5.3 | Host OS、runtime、node agentの版と更新を管理する。 | Advisoryから更新完了までの実運用は未確認。 |
| §4.5.4 | Hostの管理操作を限定し、監査へ残す。 | 実login・権限操作・ログ配送は未確認。 |
| §4.5.5 | Hostの実行物・設定・認証情報の改変を防ぐか検知する。 | 実fileの完全性やhostPathの強制は未確認。 |
| §4.6 | 採用した基盤で測定・証明が使える場合、nodeの信頼判断へ結び付ける。 | Hardware attestationを一律の必須条件にしない。 |

関係の強さは節ごとに異なり、§4.6は条件付きです。[マッピング](../../../../mappings/frameworks.yaml)で対象特性と残る範囲を確認できます。実nodeでの拒否・監査やNIST資料全体への対応を示しません。

## このコントロールの範囲

対象は共有・本番nodeのOS、runtime、kubelet、管理経路、node identity、更新と隔離です。Workload自身の権限制限は[CONTAINER-005](../psb-container-005-workload-privilege-confinement/README.md)、通信の制限は[CONTAINER-006](../psb-container-006-workload-network-segmentation/README.md)、実行後の異常検知は[CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)へ渡します。Nodeの侵害が疑われる場合、そのnode上のsensorによる「異常なし」だけでは安全と判断しません。

管理対象と設定・更新方式は[engineering](../../../../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)で選びます。対象platformを決めるまで具体実装は追加しません。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-container-host-daemon-001)、[NIST資料](../../../../sources/README.md#spec-nist-sp-800-190--container-security-guidance)、[移行記録](../../../../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#container-host-daemon-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
