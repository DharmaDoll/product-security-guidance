# Platform provenance generation移行記録

旧`PSB-BUILD-003`の5 checkを、[control](../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)の6特性と
[pattern](../engineering/build-security/platform-owned-provenance-generation/README.md)へ再編集しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

## 成果物の分離

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

## 具体化判断

技術的な構造はpatternへ具体化しました。Control-plane generator、artifact subject、field source、platform-owned authentication、fail-closed handoffという構成は、製品を選ばなくても実装判断に使えます。

一方、実行可能な設定やcodeは今回の必須成果物にしません。Native attestation、external generator、keyless bundle、KMS、OCI attestation等で設定・API・identity・配布方式が異なり、採用platformが未選定だからです。
製品を選んだ時点で`engineering/**/implementations/`へ対象版、変更箇所、実際のstatement、拒否確認、制限を追加します。

旧synthetic SLSA statement、artifact、Ed25519 key、OpenSSL verifier、secure／insecure JSON、shell testsは非移植です。
これらはJSON field、digest、local signatureの整合を確認しますが、platformが自動生成したこと、fieldがcontrol plane由来であること、tenantがsigning capabilityへ届かないことを証明しません。
Negative scenariosは実行済み結果ではなく、採用先で具体化する診断観点としてcontrolへ保持しました。

## 参照仕様の修正

SLSA v1.2の固定版と2026-09-24の公式公開版を照合しました。Build L1で必須のpredicate fieldは`buildDefinition`と`runDetails`、その配下の`buildType`、`externalParameters`、`builder.id`です。
旧controlが一律に要求した`invocationId`はschemaに存在しますが、同じ必須集合ではありません。今回のcontrolでは運用・build typeに応じた追加情報へ変更しました。

SLSA Build L2はprovenanceのauthenticityとcontrol-plane生成を要求しますが、subjectとL2で必須でないfieldにはtenant由来を許す例外があります。
移行先は「全fieldがplatform由来」と一般化せず、field sourceと例外を明示する特性へ変更しました。すべてのfieldのplatform生成・検証、強いsecret保護、build間隔離はL3側の評価であり、この移行の達成主張には含めません。

## 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| SLSA `1.2 / build-l1#platform-generates-provenance` | `PPG-001,002 / verifies / high`、review `2026-07-27` | `PROV-GEN-1,2,3 / supports / medium / design-reviewed`。実装fixtureを外し、生成・subject・必須build情報の設計関係へ縮小 |
| SLSA `1.2 / build-l2#platform-authentic-provenance` | `PPG-003,004 / evidence-for / medium`、review `2026-07-27` | `PROV-GEN-4,5 / supports / medium / design-reviewed`。Field sourceと認証境界の設計関係。Platform assessmentと実行証拠は未実施 |

この移行はSLSA Build Level 1、2、3の達成、platform認定、組織への導入を意味しません。
