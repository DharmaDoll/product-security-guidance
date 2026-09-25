# PSB-REL-002: Provenance distribution and availability boundary

学ぶ：[A release can have provenance and still leave an artifact unverifiable](learning.md) ·
設計する：[Provenance distribution and availability](../../../../engineering/release-integrity/provenance-distribution-and-availability/README.md)

## 問い

利用者が取得するexact artifactごとに、対応するprovenanceを決められた配布経路から発見・取得でき、必要な期間中に欠落・上書き・取得不能へdowngradeしないか。

## できてはいけないこと

Release pageにprovenanceが一つ存在するだけで、複数artifactのどれを説明するか分からない状態にしてはいけません。Artifact名、release名、mutable tagだけで対応付け、別platform・別digest向けのprovenanceを取得させてはいけません。

Artifactは利用可能なのにrequired provenanceの公開が未完了、取得権限がない、indexが古い、objectが上書き・削除された状態をrelease完了としてはいけません。Registry、release storage、mirror、CDN、metadata APIの部分的な失敗や未確認を「provenanceなしでも許可」へ変えてはいけません。

## 適用範囲と非適用

Release artifactのdigest identity、provenance objectまたはattestation、artifactからprovenanceを見つけるindex・relation、配布channel、consumer access、publication completion、immutability、availability、retention、withdrawal、no-downgrade policy、収集healthが対象です。

Provenanceの生成とfield sourceは[PSB-BUILD-003](../../build-security/psb-build-003-platform-provenance-generation/README.md)、署名・subject・builder・sourceを利用者の期待値で検証する処理は[PSB-REL-001](../psb-rel-001-signature-provenance-verification/README.md)が扱います。このcontrolは、取得できたprovenanceの内容が真正・正確であることや、artifactが無害であることを保証しません。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `PROV-DIST-1` | Artifact family、distribution channel、consumerごとにprovenanceが必要な範囲を決め、releaseに含まれる各artifactをexact digestで列挙する。Release名やtagだけを対応identityにしない |
| `PROV-DIST-2` | 各artifact digestから対応する一つ以上のprovenance identityとlocationを一意にたどれる。複数artifact・複数attestationを許容し、release単位の曖昧な一対一へ潰さない |
| `PROV-DIST-3` | Required provenanceとdiscovery relationがdurable storageへ公開され、intended consumerから取得できるまでartifactをrelease completeまたは検証可能として扱わない。部分公開と再試行状態を明示する |
| `PROV-DIST-4` | Intended consumerがcredentialを埋め込まず、認証したchannelと許可されたaccessでartifact identityからprovenanceを発見・取得できる。Producer viewだけでなくconsumer viewのprobeを持つ |
| `PROV-DIST-5` | Artifact、provenance、indexのidentityをcontent digestまたは同等の変更不能なversionへ結び、既存objectやrelationの上書き・別内容への再解決を防ぐ。訂正は新しいidentityと明示した関係で行う |
| `PROV-DIST-6` | Provenanceとdiscovery metadataを、artifactが取得・利用・調査される期間に合わせて保持する。Mirror・replication・cache・lifecycle・withdrawal後もavailabilityと削除状態を説明できる |
| `PROV-DIST-7` | Protected artifact familyとchannelで、欠落、取得不能、削除、access低下、index漏れをlegacyまたはoptionalへ自動downgradeしない。Inventory不足、probe失敗、parser error、stale observationを正常と分ける |

## 実装判断の羅針盤

最初にartifact ecosystemと、利用者が実際にartifactを取得する経路を決めます。Package registry、OCI registry、source hostingのrelease、専用download serviceでは、provenanceのattachment、index、認証、immutability、retentionの仕組みが異なります。

一つのreleaseにはOS・architecture・package形式の異なるartifactがあり、後からartifactが追加される場合もあります。Releaseへprovenance fileがあるかではなく、利用者が取得したartifactのdigestから対応するattestationを選べるかを見ます。一artifactへbuild provenance、SBOM attestation、verification summary等が複数付く場合も、種類とidentityを保持します。

Public accessを普遍要件にしません。Private productではintended consumerのidentityで取得できる必要があります。Signed URL等を使う場合も、短命なaccess URLをprovenanceの恒久identityにせず、credentialやtokenをmanifest・logへ残しません。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

次は「できてはいけないこと」が実際に起きないかを確認する項目です。実施済みの診断結果ではありません。

- 一release内のLinux、macOS、Windows、container、package等に同じrelease-level provenanceを返し、artifact digestごとの対応が失われないか。
- Artifact digest Aから、subjectが別digest Bのprovenanceや、別artifact向けのsidecarを発見しないか。
- 同じartifactへ複数attestationがある時、一件だけに上書きしたり、attestation type・predicate・producerの違いを失わないか。
- Mutable tag、`latest`、filename、query付き一時URLだけを恒久identityにし、同じ参照が別bytesへ変わらないか。
- Artifact upload成功後、provenanceまたはindexのupload失敗・遅延中にrelease completeとなり、consumerが先にartifactを取得できないか。
- Producer accountでは取得できるが、実際のconsumer identity、network、region、repository clientから403、404、timeout、unsupported media typeにならないか。
- Private provenanceのcredential、signed URL、tokenをrelease manifest、log、ticket、cacheへ保存していないか。
- Registry attachment、release manifest、metadata API、transparency pointerのどれかが古く、削除済みまたは置換済みobjectを返さないか。
- Provenance objectまたはartifactとのrelationを同じidentityのまま上書きできないか。MirrorやCDNが古い内容を別digestとして扱わないか。
- Artifactがsupport・download・incident調査対象である間に、storage lifecycle、cache eviction、repository cleanup、account削除でprovenanceだけが消えないか。
- Canonical channelからwithdrawした後もmirrorだけがartifactを配り、provenanceとwithdrawal情報を取得できない状態にならないか。
- Protected familyの新releaseだけprovenance requirementを外し、legacy、manual exception、unsupported clientとして通せないか。
- Pagination、artifact family漏れ、追加artifact、replica failure、access probe失敗、parser error、stale inventoryを「全artifact配布済み」に変換していないか。

## 境界と受け渡し

- [PSB-BUILD-003](../../build-security/psb-build-003-platform-provenance-generation/README.md)からexact artifact subjectを持つprovenance identityと生成結果を受け取ります。
- Registry・release serviceへartifactとprovenanceを公開し、各channelのrelation、immutability、consumer access、retentionをこのcontrolで管理します。
- [PSB-REL-001](../psb-rel-001-signature-provenance-verification/README.md)へ、consumerがexact artifactから取得したprovenance bytesとchannel identityを渡します。配布側の「available」表示を検証成功にしません。
- 欠落、取得不能、削除、replica不整合、downgradeをRelease Operationsへ渡し、公開中artifactの利用停止・復旧・consumer通知を判断します。

## 参照資料とマッピング

- [SPEC-PROVENANCE-DISTRIBUTION](../../../../sources/README.md#spec-provenance-distribution)
- [SLSA v1.2](../../../../sources/README.md#spec-slsa-1-2)
- [成果物間の関係](../../../../mappings/pilot.yaml)
- [Framework mapping](../../../../mappings/frameworks.yaml)
- [横断分析](../../../../docs/ANALYSIS_LENSES.md)
- [移行記録](../../../../docs/PROVENANCE_DISTRIBUTION_MIGRATION.md)

対象ecosystemとlive distribution serviceを選んでいないため、今回は具体実装を作っていません。実装開始条件はpatternと移行記録に残しています。
