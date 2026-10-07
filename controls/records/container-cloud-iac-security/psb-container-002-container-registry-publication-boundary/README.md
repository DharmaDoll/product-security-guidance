# PSB-CONTAINER-002 Container registry publication boundary

**承認した成果物だけを正しい場所へ公開し、公開後の変更と使用停止を追えるか。**

例えば、公開済みのrelease tagを別のdigestへ付け替えられると、利用者は同じ名前から別の内容を取得します。Registryへ保存したこと、保持していること、使用を許すことは別々の判断です。

## 満たすべきこと

1. **接続先と公開権限を絞る。** 認証したregistryへ保護された通信で接続し、意図しないmirrorへ認証情報やファイルを渡さない（REGISTRY-1）。人とautomationの権限を対象repositoryとpull・push・delete・管理操作へ限定する（REGISTRY-2）。Automationは用途と期限を絞った短命のidentityを使う（REGISTRY-3）。
2. **公開物を識別して変更を追う。** Release参照を正確なOCI digestへ結び付け、保護後のtag付替えや証拠のない削除を防ぐ（REGISTRY-4）。重要な取得、変更、権限・policy変更を、主体、対象、結果、時刻へ結び付けて監査する（REGISTRY-5）。
3. **使用停止と不明状態を扱う。** Active、deprecated、quarantined、removedなどの状態と使用可否・期限を分け、使用停止の判断を利用先へ渡す（REGISTRY-6）。API、監査、inventory、lifecycle情報が欠ける、古い、部分的、取得不能な場合は「変更なし」と扱わない（REGISTRY-7）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- HTTP、予期しないmirror、認証できないendpointへfallbackしないか。
- 匿名や別repositoryから書ける、公開担当が不要なdelete・管理操作をできる状態ではないか。
- 期限切れ、別job、対象外のidentityで公開できないか。
- 保護したtagを別digestへ向ける、manifestを置換・削除する操作を拒否するか。
- 重要な取得・変更やpolicy変更の監査が欠けたとき、欠落を識別できるか。
- 使用停止と決めた成果物を、別tag・digest・cacheから利用できないか。APIの部分取得を「対象なし」にしていないか。

これらは診断・設計レビューの確認項目であり、実際のregistryで試した結果ではありません。

## このコントロールの範囲

対象はregistryの接続先、公開・取得・削除の権限、公開済みのdigest、監査、使用停止の状態です。複数platformのimage indexと個別manifestは別のdigestを持ちます。公開記録ではどちらを指すか示し、利用先では選ばれたmanifestまで追います。保持中でも使用停止は可能で、最終的な起動の拒否は[CONTAINER-001](../psb-container-001-deployment-artifact-admission/README.md)へ渡します。公開しただけでは成果物の安全性を示せません。

権限、immutability、retention、lifecycleの選び方は[engineering](../../../../engineering/container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md)を参照してください。Provider未選定のためlive設定やcollectorは作らず、旧JSON verifierも移植していません。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-container-registry-publication-001)、[移行記録](../../../../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#container-registry-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
