# PSB-BUILD-003: Platform provenance generation

## 問い

リリース候補を作ったjob自身の申告に依存せず、build platformが成果物と実行条件を結び付けたprovenanceを生成し、その出所と改変の有無を後続consumerが確認できるか。

## できてはいけないこと

User-defined build stepが、provenance生成を無効化したり、信頼された`builder.id`や無害なparameterを自己申告したり、platformのidentityで任意のstatementを認証できてはいけません。
成果物のbytesと一致しないsubject、必須情報の欠落、生成・認証の失敗を、provenanceありとして公開工程へ渡してはいけません。

## 適用範囲と非適用

Build platformのcontrol plane、provenance generator、成果物との結合、fieldの情報源、provenanceを認証するidentity、生成結果のhandoffが対象です。
[Build containment](../psb-build-001-build-containment/README.md)はuser-defined buildの実行権限、[BUILD-002](../psb-build-002-approved-consistent-build/README.md)はproducerによるbuilder選定と一貫したbuild processを扱います。
[Signature and provenance verification](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)はconsumerの期待値による照合を扱います。Provenanceの公開・retention、artifact自体の署名、SBOM binding、deployment admissionは別の境界です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `PROV-GEN-1` | 対象となる成功buildごとにcontrol planeがprovenanceを生成し、user-defined build stepから生成を無効化、置換、成功扱いにできない |
| `PROV-GEN-2` | Statementのsubjectが実際に生成した全対象成果物を暗号学的digestで一意に識別し、別のbytesや一部だけの出力へ流用できない |
| `PROV-GEN-3` | 採用したschemaとbuild typeに従い、少なくとも`buildDefinition`、`runDetails`、`buildType`、`externalParameters`、`builder.id`と、top-level source inputを解釈できる情報を記録する |
| `PROV-GEN-4` | 信頼判断に使うfieldごとに情報源とtrust boundaryを定め、platform由来の値、tenant由来を許す値、platformが検証する値を区別する |
| `PROV-GEN-5` | Provenanceの完全性と発行元をconsumerが検証できる方式で認証し、その認証能力をuser-defined build stepへ渡さない |
| `PROV-GEN-6` | 欠落、subject不一致、schema不適合、未承認のbuilderまたはbuild type、認証不能、generator障害を成功と区別し、対象成果物を通常の公開handoffへ進めない |

`invocationId`、時刻、`resolvedDependencies`等は調査や再現に有用ですが、SLSA v1.2のすべてのlevelで一律に必須とはしません。
採用するbuild type、consumerの期待値、組織の調査要件に基づいて追加し、その値の情報源を明示します。

## 実装判断の羅針盤

最も強い境界は、成果物の確定後にplatform control planeがstatementを組み立て、build jobから利用できないidentityで認証する方式です。
JobがJSONを作りplatformがそのまま署名するだけでは、署名はjobの自己申告をplatform由来の事実へ変えません。

SLSA v1.2 Build L2では、必須fieldはcontrol planeから得る一方、subjectやL2で必須でないfieldにはtenant由来を許す例外があります。
例外を利用する場合は、どのfieldを誰が作り、platformが何を照合するかをbuild platformのsecurity modelに記録します。
L3の強いunforgeability、build間隔離、すべてのfieldのplatform生成・検証は、このcontrolを満たしたというだけでは成立しません。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

採用先では、次の操作や異常があっても公開を許可しないことを確認します。ここにあるのは確認項目であり、
本PJが実際に試した結果ではありません。テストコードがなくても、設計レビューや診断に利用できます。

- Build定義からprovenance生成を外す、生成stepをskipする、または生成失敗を無視しても公開へ進めないか
- Jobが信頼済み`builder.id`、`buildType`、source revision、parameterを偽装したstatementへ差し替えられないか
- Artifactの一byte変更、digest差替え、複数出力の一部欠落、別runのstatement再利用を拒否できるか
- 認証前後のstatement改変、未承認identity、期限・失効・transparency情報の不成立を採用方式に応じて拒否できるか
- Provenance generator、署名・認証service、platform API、保存handoffのtimeoutや部分失敗を`no issue`に変換しないか
- User-defined build stepからplatformのprovenance認証能力を直接・間接に利用できないか
- Builderの実行modeやbuild typeが変わったとき、同じidentityのまま異なるsecurity propertyを主張しないか

## 保証しない範囲

Provenanceは「何が、どこで、どの入力から作られたとplatformが述べたか」を検証可能にします。成果物が無害、sourceが正当、build platformが未侵害、依存が完全、buildが再現可能という保証にはなりません。
今回は特定platformを選んでいないため、provider設定、API、bundle形式、keyless／KMS、transparency、retentionの実装例は追加していません。
旧synthetic JSON、local key、OpenSSL verifierはcontrol-plane生成やidentity保護を証明しないため移植していません。

- [Platform-owned provenance generation pattern](../../../../engineering/build-security/platform-owned-provenance-generation/README.md)
- [参照仕様と採否](../../../../sources/README.md#spec-platform-provenance-generation)
- [Framework mapping](../../../../mappings/frameworks.yaml)
- [移行記録](../../../../docs/PLATFORM_PROVENANCE_MIGRATION.md)
