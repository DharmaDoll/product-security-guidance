# ENG-REL-002: Provenance distribution and availability

## 利用場面と推奨構造

Build platformが生成したprovenanceを、exact artifactごとにconsumerが発見・取得し続けられる配布設計です。

```text
artifact digest + provenance generation receipt
                    |
                    v
       publish transaction / incomplete release
                    |
          +---------+----------+
          |                    |
          v                    v
 immutable artifact      immutable provenance(s)
          |                    |
          +------ artifact-digest relation ------+
                               |
                         discovery index
                               |
              package / registry / release channel
                               |
                   intended-consumer retrieval probe
                               |
                               v
                    REL-001 consumer verification
```

## 1. Artifact familyと配布経路を決める

Producerが公開する全artifact familyを、package、container image、archive、installer、firmware等の単位で列挙します。同じproduct versionでもOS、architecture、format、channelが違えば別artifactです。Canonical channel、mirror、direct download、internal registryも分けます。

各familyとchannelについて、provenanceがrequiredになる時点、intended consumer、発見方法、取得権限、保持期間、withdrawal方法、ownerを決めます。Source repositoryから直接取得する内容と、repository hostingやproxyが変換して配るarchiveを同じartifactと扱いません。

## 2. Releaseではなくartifact digestへ結ぶ

Release IDはnavigationに使えますが、bindingのidentityにはexact artifact digestを使います。Indexまたはregistry relationは、artifact digest、attestation digestまたはimmutable ID、attestation type、media type、location、publication stateを持ちます。

一つのartifactへ複数attestationを付けられる構造にします。Build provenance、rebuild result、VSA等を一fileへ上書きせず、種類とproducerを区別します。一つのprovenance statementが複数subjectを持つ場合も、各subject digestから同じimmutable statementへたどれるrelationを作ります。

## 3. Publicationを完了状態まで管理する

Artifactとprovenanceを別APIでuploadする場合、完全なatomic transactionにならないことがあります。その場合はreleaseを`preparing`または`incomplete`に置き、次を満たすまでconsumerの通常取得やrelease completeを許しません。

1. Artifact bytesをimmutable identityで保存した。
2. Required provenance bytesをimmutable identityで保存した。
3. Artifact digestからのdiscovery relationを公開した。
4. Intended consumerの経路からrelationとprovenanceを取得できた。
5. Publication receiptと失敗状態を保存した。

Retryは同じcontent identityへの冪等な処理にし、別bytesへの上書きにしません。Artifactを先に公開せざるを得ない場合は、利用不能またはquarantine状態を明示し、許容時間とownerを決めます。時間目標は組織のrelease・consumer riskから決め、固定5分をcontrol要件にしません。

## 4. 配布方式を選ぶ

| 方式 | 向く場面 | 主な注意点 |
|---|---|---|
| Package／OCI registryのnative relation | Consumerが既存clientやregistryを信頼し、artifact digestからattachmentを探せる | Registry API、media type、garbage collection、replication、client対応、delete権限が固有 |
| Release sidecar + immutable manifest | Hosting serviceのreleaseにartifactとattestationを並べる | Filenameだけに頼らずdigest relationが必要。Package registryのconsumerからは別channelになる |
| Metadata API／index | 複数channelを横断し、artifact digestから複数attestationを返す | API identity、availability、pagination、authorization、index freshnessが新しい信頼境界 |
| Transparency serviceへのdigest・pointer登録 | 改変検知とmonitoringを強めたい | Provenance本体の保管・access・retentionを置き換えるとは限らない |

複数方式へ複製する場合、canonical identityとreplica relationを決めます。一つのcopyが成功したことを、全consumer channelで利用可能という意味にしません。

## 5. Consumer viewで発見・取得する

Probeはrelease automationの管理credentialではなく、intended consumerと同等のidentity、network、client、regionから行います。Artifact digestを入力にし、discovery relation、attestation identity、bytesを取得します。

`200`やdownload成功だけでは十分ではありません。返ったbytesのdigest、expected media type、relationのartifact digest、cache freshnessを確認し、REL-001へそのまま渡せる状態にします。Private channelではtokenをURL、manifest、logへ埋め込まず、access failureを欠落と区別します。

## 6. Immutability、retention、withdrawalをそろえる

Artifactが同じidentityで別bytesへ変わらないのと同様に、provenanceとrelationも同じidentityで別内容へ変わらないようにします。誤ったprovenanceを訂正する場合は、古いstatementを見えなく上書きせず、新しいidentity、supersedes／revoked等の状態、consumer通知を設計します。

Retentionは固定日数ではなく、artifactが取得可能、support対象、稼働、監査・incident調査対象となる期間から決めます。Registry garbage collection、object lifecycle、release削除、replica lag、CDN eviction、account closureを含めます。Artifactをwithdrawする時は、既存consumerがwithdrawal理由と過去のprovenanceを必要とする期間を別に判断します。

## 7. No downgradeと観測healthを持つ

Protected artifact familyでrequired provenanceが欠落した時、`legacy`、`optional`、`client unsupported`へ自動分類しません。例外が必要ならexact family、artifact、channel、reason、owner、期限、consumer impactを別のdecisionとして記録します。

Inventoryはrelease一覧、artifact pagination、attestation relation、storage object、replica、access probeを照合します。0 missingと、対象0件、権限不足、page欠落、stale snapshot、parser errorを分けます。Artifact追加後やmirror復旧後も再照合します。

## 典型的な失敗経路

- Release pageに一つprovenance fileを置き、複数artifactの対応を示さない。
- Artifactからattestationを一対一に固定し、複数statementを上書きする。
- Filename、version、tagだけで対応付け、digestを使わない。
- Artifact uploadの成功だけでrelease completeにする。
- Producer credentialからだけ取得確認し、consumer accessを試さない。
- Private access tokenをmanifestやsigned URLの恒久記録へ残す。
- Mutable indexや`latest`が別provenanceへ変わる。
- Artifactより短いlifecycleでprovenanceやrelationを削除する。
- Registry garbage collection、mirror、CDN、replicationの失敗をinventoryへ含めない。
- Probe・pagination・parser失敗を配布済みへ変換する。

## 実装を作る開始条件

具体実装は、次を一組として選べる時に作ります。

1. Artifact ecosystemと対象版。例：一つのOCI distribution実装、package registry、release service。
2. Artifact type、attestation format・media type、digest relationの公式仕様。
3. Producerとintended consumerのidentity、network、client。
4. Immutability、replication、garbage collection、retention、withdrawalの実設定。
5. 使い捨てrepositoryまたはrelease namespace。
6. 正常公開、artifact追加、複数attestation、部分公開、consumer access拒否、上書き、削除、stale index、probe failureの確認とcleanup。

旧JSON verifierのように`immutable: true`、`available: true`、`public`、保持日をmanifestへ自己申告するだけでは、storageとconsumer pathの実効性を示しません。そのため本移行ではprovider-neutralなimplementationを作りません。

## このpatternが満たす特性と限界

[PSB-REL-002](../../../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)の`PROV-DIST-1`〜`7`を、scope、artifact relation、publication state、consumer access、immutability、lifecycle、no downgradeへ配置します。

対象registry・release service、artifact、attestation client、retention policyは未選定です。Live upload、consumer retrieval、replication、deletion、withdrawalは実行していません。Provenance内容のauthenticityとexpectation検証はREL-001、生成はBUILD-003が別に必要です。

## 根拠

- [SPEC-PROVENANCE-DISTRIBUTION](../../../sources/README.md#spec-provenance-distribution)
- [移行判断](../../../docs/PROVENANCE_DISTRIBUTION_MIGRATION.md)
