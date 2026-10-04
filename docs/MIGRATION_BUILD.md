# Build Security — 移行判断

この文書は旧成果物の採否・移行時の判断をdomainごとにまとめた履歴です。現在の要件は各control、現在の進捗は[移行計画](MIGRATION_PLAN.md#現在地と次の作業)を確認してください。

## 収録した主題

- [PSB-BUILD-002 Approved and consistent release build 移行記録](#consistent-build-migration)
- [Platform provenance generation移行記録](#platform-provenance-migration)

<a id="consistent-build-migration"></a>

<a id="consistent-build-migration--psb-build-002-approved-and-consistent-release-build-移行記録"></a>
## PSB-BUILD-002 Approved and consistent release build 移行記録

<a id="consistent-build-migration--結論"></a>
### 結論

旧`PSB-BUILD-002`を[Approved and consistent release build](../controls/records/build-security/psb-build-002-approved-consistent-build/README.md)へ再編集しました。Producerが承認するbuilderと、今回のartifactが実際に通った経路を区別し、build定義・外部入力・release昇格を[設計pattern](../engineering/build-security/approved-release-build-process/README.md)へ配置しました。[教材](../controls/records/build-security/psb-build-002-approved-consistent-build/learning.md)と診断観点も追加しています。

<a id="consistent-build-migration--移行元"></a>
### 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/build-security/hosted-consistent-build/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/build-security/hosted-consistent-build/control.yaml)
- [旧verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/build-security/hosted-consistent-build/scripts/verify.py)
- [旧secure fixture](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/build-security/hosted-consistent-build/secure/build-record.json)

<a id="consistent-build-migration--旧checkの再配置"></a>
### 旧checkの再配置

| 旧check | 新しい扱い | 判断 |
|---|---|---|
| `HCB-001` builder選定 | `CONSISTENT-BUILD-1` | 目標profileに合うbuilderを承認する。Capability文書のURL・hash・申告levelは内容評価の代わりにならない |
| `HCB-002` hosted実行 | `CONSISTENT-BUILD-2・5` | Build L2以上を選ぶ時はhosted実行を確認。Local buildの混入防止はrelease昇格点でも強制する |
| `HCB-003` build定義 | `CONSISTENT-BUILD-3` | 変更不能な定義revisionを保持。Sourceとbuild定義のrevisionが常に同じという旧固定条件は外す |
| `HCB-004` invocation | `CONSISTENT-BUILD-4・5` | 重要なentry point、外部parameter、triggerをproducer期待値へ照合。全parameterの固定値と特定trigger名は普遍化しない |
| `HCB-005` 評価障害 | `CONSISTENT-BUILD-6` | 不一致と評価不能を分け、どちらもrelease昇格を止める |

<a id="consistent-build-migration--旧実装を移植しない理由"></a>
### 旧実装を移植しない理由

旧verifierは二つのJSONを比較し、builderの`hosted`、`executor_control`、`assessed_slsa_build_level`を入力値として信じます。`capability_evidence.sha256`は64桁の形式を確認するだけで、URIから取得した文書のhashや評価内容を確認しません。`record.artifact.sha256`も実artifactから計算していません。したがって旧fixtureの`PASS ... SLSA Build L2 producer requirements`は、hosted実行、platform能力、artifactの出所、release gateを実証した結果ではありません。

旧説明はSLSA Build L2のtargetを全releaseへ固定し、sourceとbuild定義のrevision一致、full Git SHA、HTTPS identity、固定parameter・protected triggerを普遍条件にしていました。[SLSA v1.2のproducer要件](https://slsa.dev/spec/v1.2/build-requirements)は、目標levelに合うplatformの選択と、verifierが期待値を作れる一貫したbuild processを求めます。Build L2ではhostedとplatform側の認証可能なprovenanceが必要ですが、上記のGit・URL・parameter形式を一律には指定しません。これらは採用するrelease profileで必要に応じて決めます。

<a id="consistent-build-migration--主題ごとの具体化判断"></a>
### 主題ごとの具体化判断

今回はprovider-neutralなcontrol、教材、pattern、診断観点、参照資料、mappingを必要な成果物に選びます。技術経路は特定のplatform、provenance発行方式、publish gateによって変わり、旧verifierを移すだけでは実効性がありません。2026-09-28の読み合わせでも文書と診断項目で完了とし、実装例の不在は残作業にしません。採用先で実効性が見込める場合の前提と、実装を選ぶ場合の完了条件は[pattern](../engineering/build-security/approved-release-build-process/README.md#具体化判断)に記載しました。

<a id="consistent-build-migration--参照資料とmapping"></a>
### 参照資料とmapping

2026-09-26にSLSA v1.2の[Build requirements](https://slsa.dev/spec/v1.2/build-requirements)、[Build Track Basics](https://slsa.dev/spec/v1.2/build-track-basics)、[Assessing build platforms](https://slsa.dev/spec/v1.2/assessing-build-platforms)を確認しました。採否と限界は[SPEC-CONSISTENT-BUILD-PRODUCER](../sources/README.md#spec-consistent-build-producer)に保持します。

旧3件のSLSA関係は同じIDを使い、現行特性への`supports / medium / design-reviewed`として再評価しました。旧`verifies / high`は、現在の成果物が実buildを検証していないため継承しません。Platform選定、consistent process、hosted実行のproducer側設計を部分的に支援します。BUILD-003のprovenance生成、REL-002の配布、REL-001のconsumer検証とplatform assessmentを合わせずにBuild level達成を主張しません。

<a id="consistent-build-migration--完了範囲と残る作業"></a>
### 完了範囲と残る作業

6特性のcontrol、教材、設計pattern、診断観点、source、3件のframework mappingと成果物・横断mappingを追加しました。実platformの選定・能力評価、release経路での強制、artifactとprovenanceの確認、live拒否は未実施です。次の移行候補は、記録がないSecure Coding domainの旧`PSB-CODE-005` Unicode source deceptionです。

<a id="platform-provenance-migration"></a>

<a id="platform-provenance-migration--platform-provenance-generation移行記録"></a>
## Platform provenance generation移行記録

旧`PSB-BUILD-003`の5 checkを、[control](../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)の6特性と
[pattern](../engineering/build-security/platform-owned-provenance-generation/README.md)へ再編集しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

<a id="platform-provenance-migration--成果物の分離"></a>
### 成果物の分離

この主題は攻撃段階8で、user-defined buildの自己申告とplatform由来のprovenanceを分けます。
既存`PSB-BUILD-001`はjobの実行権限、旧`PSB-BUILD-002`はproducerによるbuilder選定と一貫したprocess、
`PSB-REL-001`はconsumerによる照合を扱います。Provenance distribution、artifact signing、SBOM binding、deployment admissionをこのcontrolへ統合していません。

| 旧check | 新しい配置 | 判断 |
|---|---|---|
| `PPG-001` automatic generation | `PROV-GEN-1` | Control-plane生成、無効化・置換・bypassの防止として継承 |
| `PPG-002` artifact and build description | `PROV-GEN-2`、`PROV-GEN-3` | Subject bindingとschema／build descriptionを分離。旧`invocationId`一律必須は非継承 |
| `PPG-003` field sources | `PROV-GEN-4` | Platform・tenant・platform検証済みの情報源をfieldごとに区別する設計へ変更 |
| `PPG-004` platform authenticity | `PROV-GEN-5` | 特定の署名方式に固定せず、consumerが検証でき、jobが利用できない認証能力として継承 |
| `PPG-005` verifier failure | `PROV-GEN-6`と`PSB-REL-001` | Producer側の生成・handoff失敗は本control、consumer verifierのparse・crypto失敗はREL-001の責任 |

<a id="platform-provenance-migration--具体化判断"></a>
### 具体化判断

技術的な構造はpatternへ具体化しました。Control-plane generator、artifact subject、field source、platform-owned authentication、fail-closed handoffという構成は、製品を選ばなくても実装判断に使えます。

一方、実行可能な設定やcodeは今回の必須成果物にしません。Native attestation、external generator、keyless bundle、KMS、OCI attestation等で設定・API・identity・配布方式が異なり、採用platformが未選定だからです。
製品選定後も、導入や確認に役立つ場合だけ限定実装を検討します。選んだ場合は`engineering/**/implementations/`へ対象版、変更箇所、実際のstatement、拒否確認、制限をまとめます。実装例の不在は文書移行の未完了理由にしません。

旧synthetic SLSA statement、artifact、Ed25519 key、OpenSSL verifier、secure／insecure JSON、shell testsは非移植です。
これらはJSON field、digest、local signatureの整合を確認しますが、platformが自動生成したこと、fieldがcontrol plane由来であること、tenantがsigning capabilityへ届かないことを証明しません。
問題のある操作や異常は、実行済み結果ではなく、採用先で具体化する確認項目としてcontrolへ保持しました。

<a id="platform-provenance-migration--参照仕様の修正"></a>
### 参照仕様の修正

SLSA v1.2の固定版と2026-09-24の公式公開版を照合しました。Build L1で必須のpredicate fieldは`buildDefinition`と`runDetails`、その配下の`buildType`、`externalParameters`、`builder.id`です。
旧controlが一律に要求した`invocationId`はschemaに存在しますが、同じ必須集合ではありません。今回のcontrolでは運用・build typeに応じた追加情報へ変更しました。

SLSA Build L2はprovenanceのauthenticityとcontrol-plane生成を要求しますが、subjectとL2で必須でないfieldにはtenant由来を許す例外があります。
移行先は「全fieldがplatform由来」と一般化せず、field sourceと例外を明示する特性へ変更しました。2026-09-28の再照合で、L3の生成・検証要件もL2欄の例外を参照することを確認し、例外なしと読めた説明を修正しました。強いsecret保護、偽造防止、build間隔離は別途platform評価が必要で、この移行の達成主張には含めません。

同日の読み合わせで、署名済みの自己申告と基盤が観測した事実を区別する[教材](../controls/records/build-security/psb-build-003-platform-provenance-generation/learning.md)をcontrol配下へ追加しました。旧fixtureを実行した教材ではなく、記録の出所と公開承認を説明するシナリオです。

<a id="platform-provenance-migration--旧framework-mapping"></a>
### 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| SLSA `1.2 / build-l1#platform-generates-provenance` | `PPG-001,002 / verifies / high`、review `2026-07-27` | `PROV-GEN-1,2,3 / supports / medium / design-reviewed`。実装fixtureを外し、生成・subject・必須build情報の設計関係へ縮小 |
| SLSA `1.2 / build-l2#platform-authentic-provenance` | `PPG-003,004 / evidence-for / medium`、review `2026-07-27` | `PROV-GEN-4,5 / supports / medium / design-reviewed`。Field sourceと認証境界の設計関係。Platform assessmentと実行証拠は未実施 |

この移行はSLSA Build Level 1、2、3の達成、platform認定、組織への導入を意味しません。
