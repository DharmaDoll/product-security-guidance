# PSB-CONTAINER-001 Deployment artifact admission

**実行する成果物をすべて確認し、現在の受入条件に合わなければ起動を止められるか。**

## なぜ必要か

例えば、main imageだけを確認しても、init containerやsidecarが未確認なら別のコードを起動できます。Tag、過去の「合格」表示、deployerが付けた`verified: true`だけで使用を許可してはいけません。

## 満たすべきこと

1. **実行するものを漏らさない。** Main、init、sidecar、ephemeralなど全artifactをrepositoryとdigestで特定する（ARTIFACT-ADMIT-1）。複数platformのimage indexを使う場合は、実行先が選ぶmanifestとの対応も追う。
2. **利用者の受入判断と結び付ける。** 署名、来歴、builder、source、入力などについて、利用者が現在採用する条件で判断した結果を、正確なdigestと対象環境へ結び付ける（ARTIFACT-ADMIT-2）。Mutationやtagの再解決後、実行へ渡す最終状態にも判断を適用する（ARTIFACT-ADMIT-3）。
3. **別経路と失敗を通さない。** 作成・更新・rollback・controller・直接作成など、実行物を変えられる全経路に同じ強制を適用する（ARTIFACT-ADMIT-4）。Artifactや判断材料を取得・評価できない場合は通常の起動を止める（ARTIFACT-ADMIT-5）。許可した結果は対象artifact群、環境、policy版、判断時刻へ結び付け、変更・失効・再評価を管理する（ARTIFACT-ADMIT-6）。

## 起動の判断と実際の稼働を分ける

起動前の検査（Admission）では、過去のCI結果だけを信頼しません。利用者の受入条件、成果物の内容、実行先を、一つの判断記録へ結び付けます。
この`ALLOW`は使用開始を許す判断であり、指定したdigestが実際に稼働した証拠ではありません。Node・runtime側で観測したdigestと照合する責任は後段に残します。

## 起動の判断に必要な情報

| 要素 | 必要な意味 | 避ける状態 |
|---|---|---|
| 実行する成果物 | Repository／package identity、digest、各containerやmoduleの役割。OCI indexなら選択されるplatformとmanifestの関係 | Tag、名前、一つ目のimageだけ |
| 受入条件 | Consumer policyで評価したsignature、provenance、builder、source、parameter | Producerのlevel自己申告、`verified: true` annotation |
| 実行先 | Cluster、environment、tenant、workload class等、policyが区別する範囲 | 別環境へreceiptを流用 |
| 判断に使ったルール | Version、trust root／identity profile、変更時刻 | 「最新」だけで再現不能 |
| 判断結果 | ALLOW／DENY／ERROR、reason、decision ID、評価時刻、期限 | Booleanだけ、ERRORをALLOWへ変換 |
| 監査記録 | Request identity、artifact digest、policy、結果、enforcement point | Secret、token、provenance全文、image内容の複製 |

事前の判断記録（receipt）を使う場合は、利用者側の検証サービスが発行元と改ざんの有無を確認します。署名が有効でも、対象環境やルールの版が違う記録は流用しません。

Registryの公開記録から、descriptorの種類、digest、必要ならindexと選択されたmanifestの対応を受け取ります。Lifecycleが使用許可に影響する場合は、同じidentityの現在の使用可否と期限を照合します。`deprecated`は決めた用途と期限の範囲で許す設計もあります。`quarantined`など使用停止を決めた状態、または状態を確認できない場合に、古いreceiptだけで許可を再開しません。公開・保持・使用許可の判断主体を混ぜないことが必要です。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| 起動前にその場で検証 | 使用時に証拠を取得し、待ち時間やAPI制限を許容できる場合。新しい情報で判断できるが、registryや証拠の提供サービスが止まると配備も止まる |
| 事前に評価した判断記録を検証 | 起動時の通信や待ち時間を減らしたい場合。記録の期限・失効、対象環境との一致、再利用できる条件、ルール更新後の再評価を決める |
| 管理基盤のルールで検査 | 起動要求に含まれるdigest、repository、設定値、判断記録の属性だけで判定できる場合。外部証拠の取得や一般的な暗号検証までこの方式へ押し込まない |
| 外部の検証サービスへ照会 | Registry、来歴、ルールの管理サービスへの照会が必要な場合。冗長化、タイムアウト、接続先の認証、cache、循環依存、更新時の互換性も運用する |
| Nodeで取得・実行を制限 | 起動前検査の後の差替えやnode cacheも制限したい場合。検査で許可した成果物と対応付ける必要があり、申請者や実行先の判断は別に必要 |

参照したKubernetesの公式ガイダンスでは、単純な検査にはCEL-based admissionを優先し、外部データを使う複雑な検査にはdynamic admissionを利用できると説明しています。
これは製品選定の入力であり、CELやwebhookをcontrolの意味にはしません。

## Kubernetesへ適用するときの境界

Kubernetes adapterを作る場合は、少なくとも次を明示します。

- Deployment、StatefulSet、DaemonSet、Job、CronJob等のPod templateと、直接作成されるPodのどこを評価するか
- Regular、init、ephemeral containerと、platformが追加するsidecar等のimageをいつ列挙するか
- Mutating admission後のfinal objectをvalidating boundaryで確認する順序
- `CREATE`、`UPDATE`、ephemeral container等のsubresource、等価なAPI version、rollbackのcoverage
- Validating policy／webhookの`failurePolicy`、timeout、match条件、除外namespace、設定変更権限
- Registry manifestとprovenanceを取得するidentity、TLS、cache、freshness、rate limit
- Image indexと実行先で選ばれるmanifest、registry lifecycleとadmission判断を同じartifactへ結び付ける方法
- Admissionのdigestと、node／runtimeが実際にpull・実行したdigestを後続inventoryでどう照合するか

Runtimeの表示するimage IDが常にadmissionで指定したindex digestと同じ形式とは限りません。取得したindex、選択したmanifest、runtimeの報告値をどう対応付けるかを採用先で確認し、[GOV-005の復旧判断](../../../../engineering/deployed-artifact-recovery.md)には観測できた範囲と未照合の範囲を分けて渡します。

Built-in field policyとexternal verifierを併用する場合、片方の成功だけでallowにしません。全必須decisionが同じartifact setとrequestへ結び付いたときだけallow候補にします。

## 例外と障害時の扱いを決める

対象外namespaceやbreak-glassは、通常policyの穴ではなく[Security exception lifecycle](../../governance-operations/psb-gov-002-security-exception-lifecycle/README.md)へ結び付けます。
Exact target、artifact、property、owner、期限を評価時に確認し、失効・期限切れ・取得不能は通常のdenyへ戻します。

Evaluatorの停止時に可用性を優先する必要があるsystem componentは、一般workloadと同じ暗黙fallbackにしません。
Bootstrap dependency、disaster recovery、cluster add-onを別のscopeと強制点へ分け、誰がどの期間どのartifactを許可したかを残します。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- Tagだけの参照や、別repository・別digest・別環境用の証拠を使って起動できないか。
- Image indexの確認結果を、対応が不明な別platformのmanifestへ流用できないか。
- Init、sidecar、ephemeral、debug用のartifactや、更新・rollback・直接作成の経路が検査を迂回しないか。
- Mutation後の差替え、評価後のtag解決変更、古い許可結果の再利用を許さないか。
- Registry、evidence、policy、評価器の欠落・timeout・部分失敗を、通常の許可へ変えていないか。
- 使用停止と決めたdigestを、古い許可結果、別tag、cacheから再投入できないか。

これらは診断・設計レビューの確認項目であり、実際のclusterでの拒否結果ではありません。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| SLSA Build track v1.2 Build L2「Consumer validates authenticity」 | 実際に使う成果物を、利用者自身の期待値と照合してから許可する段階へつなぐ。 | 検証の中身はREL-001。受入実装とSLSA levelは未確認。 |
| SLSA Build provenance v1.2 | 来歴に記された成果物と、起動するdigestを同じ対象へ結び付ける。 | 来歴の取得・暗号検証はここでは行わない。 |
| NIST SP 800-190 §4.1.5 | 信頼する成果物の正確な同一性を起動前に確認する部分を支える。 | Registry管理、保守、実際の署名検証は別。 |
| NIST SP 800-190 §4.4.5 | 起動前の受入条件と、誰が何を許可したかの記録を支える。 | 配備権限や全ての不正起動経路は扱えない。 |

4件の対象特性と限界は[マッピング](../../../../mappings/frameworks.yaml)にあります。いずれも部分的な設計・受け渡しの関係で、実際の起動拒否や規格への準拠を示しません。

## このコントロールの範囲

対象はdeployment requestから実行へ渡す最終状態と、その受入を強制する全経路です。Registryでの公開と保持は[CONTAINER-002](../psb-container-002-container-registry-publication-boundary/README.md)、利用者の受入条件は[REL-001](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)、実行後の観測は[CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)へ渡します。許可した成果物の無害性や、runtimeで同じbytesが動いたことまでは示しません。

Consumer verifierとadmissionのつなぎ方、判断結果の再利用、障害時の挙動は上の方式説明で選びます。旧offline JSON verifierはliveのAPI経路やmutation後の状態を示さないため移植していません。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-deployment-artifact-admission-001)、[移行記録](../../../../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#deployment-artifact-admission-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。

対策同士のつながりは[公開したコンテナを動かし、侵害の広がりを抑える](../../../../engineering/container-deployment-to-response.md)で確認できます。
