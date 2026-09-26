# ENG-BUILD-003: Approved release build process

## 利用場面と推奨構造

複数のbuild経路がある製品で、どの実行結果を正規releaseとして公開してよいか決める設計です。開発者は手元で試行錯誤できても、releaseはproducerが承認したbuilderと手順に結び付けます。

```text
製品側のrelease方針 ──> 目標profile / 承認builder / 定義 / 入力 / 許可経路
             |                                      |
             |                              保護したbuild起動
             |                                      |
builder能力の評価                        platform由来の実行・成果物情報
             |                                      |
             +------------> 対象digestと条件を照合 ──> release昇格
```

## 1. Builderを選び、その能力を評価する

Release managerが対象artifact familyと目標profileを決めます。Builderのidentity、管理者、control planeとbuild environmentの境界、provenanceを誰が生成するか、実行方式、能力の評価時点を記録します。Capability documentのURLやSHA-256を固定するだけでは、その中の主張が正しいか分かりません。発行者、内容、対象builder版、評価範囲をレビューし、変更・廃止時に再評価します。

SLSA Build L1で求めるbuilderと、Build L2以上で必要なhosted実行・認証可能なprovenanceは異なります。Hostされたrunnerを選ぶだけではL2になりません。Build L3のbuild間隔離、cache、秘密情報の保護はさらにplatform評価が必要です。[SLSAのplatform評価](../../../sources/README.md#spec-consistent-build-producer)が挙げるexternal parameters、control plane、build environments、caches、outputsを採用時に確認します。

## 2. 正規releaseの手順を定める

Producer側の承認記録へ、対象source、build定義とrevision、build type、entry point、重要な外部parameter、許可する起動経路、出力artifactの種類を記載します。Sourceとbuild定義が同じrepositoryにある場合でも、別repositoryの場合でも、実際に使ったrevisionを追跡します。`main`や`latest`のような可変参照は解決後のrevisionやdigestを確認します。

すべてのparameterを一つの固定値にする必要はありません。例えばrelease versionはrunごとに変わりますが、誰が与え、どの範囲が許され、どこに記録されるかを定めます。外部service、remote execution、未固定dependencyなどの影響は、build typeとplatformの記録能力によって扱いが異なります。見えていない入力を「存在しない」としません。手順を更新する際は、通常のcode reviewやrelease承認で期待値も更新します。

## 3. 実際に通った経路を確認する

通常releaseへの昇格点は、jobが自分で作ったJSONではなく、採用platformから得た実行・成果物情報と結びます。少なくとも、今回のartifact digest、builder identity、source revision、build定義、採用方針に必要な外部parameterと起動経路を照合します。Platformがどのfieldを自身で観測し、どれをtenantやjobから受け取るかも区別します。`builder.id`が認証されても、すべてのfieldがplatform由来とは限りません。

| 経路 | 扱い | 判断の理由 |
|---|---|---|
| 承認builderと承認手順から作った成果物 | 昇格候補 | Evidenceをexact outputへ結び、後続の署名・公開へ渡す |
| Local build、別builder、未承認定義・parameter | 拒否 | 同名artifactでも期待したrelease経路ではない |
| 記録の欠落、署名・取得・parse失敗、能力評価が古い | 評価不能 | 正規経路を確認できないので通常releaseへ渡さない |

Release channelとregistryへのpublish権限は、この判断を経た経路に限定します。別jobが同じrepositoryへ直接uploadできれば、前段の検査は迂回できます。例外で別経路を使う場合も、通常releaseと同じ証拠を装わず、範囲・責任者・期限・consumerへの影響を別に扱います。

## 典型的な失敗経路

- Hosted jobを使っているが、workflow fileを可変branchから読み、レビュー時と別の命令を実行する。
- 同じsource revisionを使い、手動起動時のdebug flagで別の成果物を作る。
- Jobが`hosted: true`を含むJSONを作り、platform-issued recordとして受け入れる。
- Capability文書のdigestだけを照合し、対象builderや評価内容を読まない。
- 承認経路は検査するが、local artifactを別のupload tokenで同じrelease先へ置ける。
- Evidence serviceのtimeoutを「記録なしでよい」へ変え、releaseを進める。

## 具体化判断

旧Python verifierはpolicyとrecordの文字列・boolean・digest形式を比較します。Hostされた実行、platform評価、platform発行のrecord、artifact bytes、publish権限を観測しません。旧`secure/`も合成JSONです。これを新しい実装例として移すと、自己申告した`assessed_slsa_build_level: 2`が実際のBuild L2評価に見えるため採用しません。

今回はcontrol、教材、pattern、診断観点、参照資料、mappingまでを必要な成果物とします。具体実装は一つのbuild platform、artifact family、release先、protected source・build definition、platformのprovenance形式と発行元、publish gateを選んでから作ります。完了には使い捨てreleaseで、正常buildの昇格、別builder・別定義・parameter変更・local uploadの拒否、evidence取得不能時の停止を実際に観測できる必要があります。Platformの実行情報から信頼できないfieldが見つかった場合は、その制限をcontrolの適用範囲とproducerの選択条件へ戻します。

## このpatternの境界

[BUILD-002](../../../controls/records/build-security/psb-build-002-approved-consistent-build/README.md)の`CONSISTENT-BUILD-1〜6`を、builder評価、正規手順、実行経路、release昇格へ配置します。[BUILD-001](../../../controls/records/build-security/psb-build-001-build-containment/README.md)はbuild中の権限と隔離、[BUILD-003](../../../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)はplatformによるprovenance生成、[REL-002](../../../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)は配布、[REL-001](../../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)はconsumer受入れを扱います。

## 根拠

- [SPEC-CONSISTENT-BUILD-PRODUCER](../../../sources/README.md#spec-consistent-build-producer)
- [移行記録](../../../docs/CONSISTENT_BUILD_MIGRATION.md)
