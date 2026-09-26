# PSB-BUILD-002 Approved and consistent release build 移行記録

## 結論

旧`PSB-BUILD-002`を[Approved and consistent release build](../controls/records/build-security/psb-build-002-approved-consistent-build/README.md)へ再編集しました。Producerが承認するbuilderと、今回のartifactが実際に通った経路を区別し、build定義・外部入力・release昇格を[設計pattern](../engineering/build-security/approved-release-build-process/README.md)へ配置しました。[教材](../controls/records/build-security/psb-build-002-approved-consistent-build/learning.md)と診断観点も追加しています。

## 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/build-security/hosted-consistent-build/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/build-security/hosted-consistent-build/control.yaml)
- [旧verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/build-security/hosted-consistent-build/scripts/verify.py)
- [旧secure fixture](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/build-security/hosted-consistent-build/secure/build-record.json)

## 旧checkの再配置

| 旧check | 新しい扱い | 判断 |
|---|---|---|
| `HCB-001` builder選定 | `CONSISTENT-BUILD-1` | 目標profileに合うbuilderを承認する。Capability文書のURL・hash・申告levelは内容評価の代わりにならない |
| `HCB-002` hosted実行 | `CONSISTENT-BUILD-2・5` | Build L2以上を選ぶ時はhosted実行を確認。Local buildの混入防止はrelease昇格点でも強制する |
| `HCB-003` build定義 | `CONSISTENT-BUILD-3` | 変更不能な定義revisionを保持。Sourceとbuild定義のrevisionが常に同じという旧固定条件は外す |
| `HCB-004` invocation | `CONSISTENT-BUILD-4・5` | 重要なentry point、外部parameter、triggerをproducer期待値へ照合。全parameterの固定値と特定trigger名は普遍化しない |
| `HCB-005` 評価障害 | `CONSISTENT-BUILD-6` | 不一致と評価不能を分け、どちらもrelease昇格を止める |

## 旧実装を移植しない理由

旧verifierは二つのJSONを比較し、builderの`hosted`、`executor_control`、`assessed_slsa_build_level`を入力値として信じます。`capability_evidence.sha256`は64桁の形式を確認するだけで、URIから取得した文書のhashや評価内容を確認しません。`record.artifact.sha256`も実artifactから計算していません。したがって旧fixtureの`PASS ... SLSA Build L2 producer requirements`は、hosted実行、platform能力、artifactの出所、release gateを実証した結果ではありません。

旧説明はSLSA Build L2のtargetを全releaseへ固定し、sourceとbuild定義のrevision一致、full Git SHA、HTTPS identity、固定parameter・protected triggerを普遍条件にしていました。[SLSA v1.2のproducer要件](https://slsa.dev/spec/v1.2/build-requirements)は、目標levelに合うplatformの選択と、verifierが期待値を作れる一貫したbuild processを求めます。Build L2ではhostedとplatform側の認証可能なprovenanceが必要ですが、上記のGit・URL・parameter形式を一律には指定しません。これらは採用するrelease profileで必要に応じて決めます。

## 主題ごとの具体化判断

今回はprovider-neutralなcontrol、教材、pattern、診断観点、参照資料、mappingを必要な成果物に選びます。技術経路は特定のplatform、provenance発行方式、publish gateによって変わり、旧verifierを移すだけでは実効性がありません。実装再開の前提と、正常・拒否・障害の観測を伴う完了条件は[pattern](../engineering/build-security/approved-release-build-process/README.md#具体化判断)に記載しました。

## 参照資料とmapping

2026-09-26にSLSA v1.2の[Build requirements](https://slsa.dev/spec/v1.2/build-requirements)、[Build Track Basics](https://slsa.dev/spec/v1.2/build-track-basics)、[Assessing build platforms](https://slsa.dev/spec/v1.2/assessing-build-platforms)を確認しました。採否と限界は[SPEC-CONSISTENT-BUILD-PRODUCER](../sources/README.md#spec-consistent-build-producer)に保持します。

旧3件のSLSA関係は同じIDを使い、現行特性への`supports / medium / design-reviewed`として再評価しました。旧`verifies / high`は、現在の成果物が実buildを検証していないため継承しません。Platform選定、consistent process、hosted実行のproducer側設計を部分的に支援します。BUILD-003のprovenance生成、REL-002の配布、REL-001のconsumer検証とplatform assessmentを合わせずにBuild level達成を主張しません。

## 完了範囲と残る作業

6特性のcontrol、教材、設計pattern、診断観点、source、3件のframework mappingと成果物・横断mappingを追加しました。実platformの選定・能力評価、release経路での強制、artifactとprovenanceの確認、live拒否は未実施です。次の移行候補は、記録がないSecure Coding domainの旧`PSB-CODE-005` Unicode source deceptionです。
