# PSB-CONTAINER-002 Container registry publication boundary

**承認した成果物だけを正しい場所へ公開し、公開後の変更と使用停止を追えるか。**

## なぜ必要か

例えば、公開済みのrelease tagを別のdigestへ付け替えられると、利用者は同じ名前から別の内容を取得します。Registryへ保存したこと、保持していること、使用を許すことは別々の判断です。

## 満たすべきこと

1. **接続先と公開権限を絞る。** 認証したregistryへ保護された通信で接続し、意図しないmirrorへ認証情報やファイルを渡さない（REGISTRY-1）。人とautomationの権限を対象repositoryとpull・push・delete・管理操作へ限定する（REGISTRY-2）。Automationは用途と期限を絞った短命のidentityを使う（REGISTRY-3）。
2. **公開物を識別して変更を追う。** Release参照を正確なOCI digestへ結び付け、保護後のtag付替えや証拠のない削除を防ぐ（REGISTRY-4）。重要な取得、変更、権限・policy変更を、主体、対象、結果、時刻へ結び付けて監査する（REGISTRY-5）。
3. **使用停止と不明状態を扱う。** Active、deprecated、quarantined、removedなどの状態と使用可否・期限を分け、使用停止の判断を利用先へ渡す（REGISTRY-6）。API、監査、inventory、lifecycle情報が欠ける、古い、部分的、取得不能な場合は「変更なし」と扱わない（REGISTRY-7）。

## 公開・削除・使用停止の権限を分ける

公開担当、registry管理者、使用停止を決める担当、利用者の役割を分けます。新しい成果物を公開する権限だけで、既存releaseの置換・削除やルール変更までできるようにしません。

## 公開前に決めること

| 境界 | 決めること |
|---|---|
| 接続先 | 正確なホスト名と認証する相手、信頼する証明書、mirror、client、TLS検証に失敗した場合の動作 |
| 権限 | 人と自動処理ごとに、対象repositoryと取得・公開・削除・管理の操作を限定する。通常は拒否し、緊急時の例外を別に決める |
| 公開記録 | Manifest／indexの種類、digest、tag、公開した主体、承認した判断、成功時刻 |
| 上書き・削除の防止 | いつtag／digestを保護し、置換・削除をどう拒否し、例外を誰が承認するか |
| 監査 | 重要な取得・変更・拒否を要求単位で記録し、収集停止や欠落をどう見つけるか |
| 公開後の状態 | 使用可否と期限、検査・インシデント・サポート終了による判断、起動前検査への伝達 |

OCI descriptorのdigestはcontent addressです。取得したbytesのdigestとsizeをconsumerが照合できるようにし、tagは同一性の根拠にしません。
Image indexを公開する場合、そのdigestと各platform用manifestのdigestを区別します。Indexを承認したという記録から、実行先で選択されたmanifestの確認を省きません。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| Registry標準の上書き・削除防止 | 標準機能と監査で必要範囲を守れる場合。契約プラン、API、例外権限、保持期間の挙動に依存する |
| 新規追加だけを許すrelease repository | 新しいdigestと参照名で公開できる場合。保存容量、不要物の整理、復旧用の在庫管理の負担が増える |
| Release専用repositoryへ昇格 | Build／stagingから確認済みのdigestを移す場合。コピーで内容が変わらないこと、権限、証拠との対応を確認する |
| 外部のルール評価と監査照合 | 標準機能が不足する場合。検査前の変更、イベント欠落、一覧の取得漏れ、修復と収集の権限も管理する |

Lifecycleのnon-deployable状態はregistry削除だけで実現しません。Admission側の拒否、repository policy、consumer trust decisionを同じdigestへ結び、replicaやcacheも含めて状態を観測します。`deprecated`は用途・期限を限った利用を認める場合があり、状態名だけから使用可否を推論しません。使用停止を決めた`quarantined`等は取得可能なままでもconsumerが拒否できるようにします。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- HTTP、予期しないmirror、認証できないendpointへfallbackしないか。
- 匿名や別repositoryから書ける、公開担当が不要なdelete・管理操作をできる状態ではないか。
- 期限切れ、別job、対象外のidentityで公開できないか。
- 保護したtagを別digestへ向ける、manifestを置換・削除する操作を拒否するか。
- 重要な取得・変更やpolicy変更の監査が欠けたとき、欠落を識別できるか。
- 使用停止と決めた成果物を、別tag・digest・cacheから利用できないか。APIの部分取得を「対象なし」にしていないか。

これらは診断・設計レビューの確認項目であり、実際のregistryで試した結果ではありません。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| NIST SP 800-190 §4.2.1 | 承認したregistry接続先を認証し、通信を保護する部分に関係する。 | 実際のTLS接続、mirror、認証情報の配送は未確認。 |
| NIST SP 800-190 §4.2.2 | 古いimageを見つけ、使用停止・撤回の状態へ進める部分に関係する。 | 実際の在庫、削除、利用者側cacheは未確認。 |
| NIST SP 800-190 §4.2.3 | 公開・上書き・削除を許可された主体に限り、操作を追跡する部分に関係する。 | 提供元の権限設定や操作拒否は未確認。 |

この3件の詳しい範囲は[マッピング](../../../../mappings/frameworks.yaml)にあります。Registryへの保存を、利用者側の使用許可や規格への準拠と同一視しません。

## このコントロールの範囲

対象はregistryの接続先、公開・取得・削除の権限、公開済みのdigest、監査、使用停止の状態です。複数platformのimage indexと個別manifestは別のdigestを持ちます。公開記録ではどちらを指すか示し、利用先では選ばれたmanifestまで追います。保持中でも使用停止は可能で、最終的な起動の拒否は[CONTAINER-001](../psb-container-001-deployment-artifact-admission/README.md)へ渡します。公開しただけでは成果物の安全性を示せません。

権限、immutability、retention、lifecycleの選び方は上の方式説明を参照してください。Provider未選定のためlive設定やcollectorは作らず、旧JSON verifierも移植していません。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-container-registry-publication-001)、[移行記録](../../../../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#container-registry-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。

対策同士のつながりは[公開したコンテナを動かし、侵害の広がりを抑える](../../../../engineering/container-deployment-to-response.md)で確認できます。
