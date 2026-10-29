# PSB-BUILD-003 Platform provenance generation

**ビルドの来歴を、ビルドjob自身の申告ではなく基盤が作っているか。**

## なぜ必要か

例えば、jobが`builder.id`や入力を書いたJSONを作り、基盤がそのまま署名しても、記録の中身が基盤で確認された事実にはなりません。成果物と実行条件を誰が記録し、誰が認証できるかを分けて判断します。

## 満たすべきこと

1. **基盤側で作る。** 対象となる成功ビルドごとに基盤のcontrol planeがprovenanceを生成し、ビルドjobから生成を省略・置換できないようにする（PROV-GEN-1）。対象成果物すべてを実際のbytesのdigestへ結び付ける（PROV-GEN-2）。
2. **記録の中身と情報源を示す。** 採用したschemaとbuild typeに必要な`buildDefinition`、`runDetails`、`buildType`、`externalParameters`、`builder.id`、ソース入力を解釈できるように記録する（PROV-GEN-3）。各fieldが基盤由来か、利用者由来か、基盤で検証されたかを区別する（PROV-GEN-4）。
3. **出所を認証し、失敗時は止める。** 利用者が出所と改変の有無を検証できる形で認証し、その能力をビルドjobへ渡さない（PROV-GEN-5）。記録の欠落、成果物との不一致、認証・生成の失敗を成功に変えず、通常の公開工程へ進めない（PROV-GEN-6）。

## 責任と情報源

| 情報・処理 | 主な情報源／強制点 | 判断すること |
|---|---|---|
| 対象build | Platformが認証したrun・workflow・project | どの成功状態をprovenance生成対象にするか |
| `subject` | 確定したoutput bytesとdigest計算境界 | 複数成果物を含め、配布するbytesと一致するか |
| `builder.id` | Platform security model | 信頼境界と実行modeが一意か。性質の異なるmodeを同じidentityにしないか |
| `buildType` | Version管理したbuild type仕様 | Parameterの意味と起動方法をconsumerが解釈できるか |
| `externalParameters` | Platformが受理した外部入力 | Job内で都合のよい値へ書き換えられないか |
| Source input | Platformが解決したURI・revision、必要に応じ`resolvedDependencies` | branch名だけでなく実際に使ったrevisionを追えるか |
| 認証 | Control planeのidentity・keyless service・KMS等 | Jobに認証能力を渡さず、consumerがissuerとintegrityを検証できるか |
| Handoff status | Generator、認証、保存の各結果 | 欠落・timeout・部分成功を通常公開へ進めないか |

SLSA Provenance v1を使う場合、predicate typeは`https://slsa.dev/provenance/v1`です。
`buildDefinition`と`runDetails`、その中の`buildType`、`externalParameters`、`builder.id`がBuild L1で必須です。
`invocationId`や時刻は有用でも同じ必須集合ではないため、運用上必要ならbuild typeの契約として追加します。

上表は情報源を選ぶ設計です。採用platformが同じ構成を持つとは限りません。SLSA v1.2 Build L2では必須fieldをcontrol planeから得る一方、subjectやL2で必須でないfieldにtenant由来を許す例外があります。L3の生成・検証要件もこの例外を参照するため、「L3なら全fieldがplatform由来」とは読みません。例外を使う場合は、誰が値を作り、platformが何を照合するかをsecurity modelに残します。基盤が受理した`externalParameters`も、値自体は利用者が選べます。正確に記録したことをリリース承認にせず、[作り手側の期待値](../psb-build-002-approved-consistent-build/README.md)と後続consumerの期待値へ渡します。

## 方式の選択

| 方式 | 選ぶ条件・代償 |
|---|---|
| Platform native attestation | Platformが生成境界、field source、identity、bundle取得方法を文書化している場合。最も単純だがproviderのschema、retention、identity lifecycleへ依存する |
| Platform-owned external generator | Build eventと確定outputをcontrol plane APIから取得でき、generatorをtenant jobから隔離できる場合。Adapter、再試行、重複排除、API障害の扱いを所有する必要がある |
| Rebuilderによるprovenance | 独立した再buildを正式なproducerとして扱える場合。元buildとの同一性、再現性、builder identity、配布対象を別に定義する必要がある |
| Job-generated metadata | DebugやL1相当の存在確認には使える場合がある。Platform由来のauthentic provenanceとしては扱わず、後からplatform署名するだけでfieldの信頼性を上げない |

認証方式は、提供者が発行する短命の証明書とbundle、基盤のサービス鍵、KMS／HSM等から選びます。
署名方式だけで決めず、身元・権限の範囲、失効、時刻、透明性ログ、オフライン検証、利用者側の信頼根拠の更新を一組の条件にします。

## 生成から引き渡しまでの状態

```text
build_started
  -> output_finalized
  -> provenance_generated
  -> provenance_authenticated
  -> handoff_ready

各段階の欠落・不一致・timeout
  -> unresolved_generation
  -> 通常のrelease promotionを停止
```

再試行時は、run identity、artifact digest、statement identityを用いて二重発行や別runへの結合を防ぎます。
Artifactを再生成した場合はdigestが同じでもrunとの関係を新しいprovenanceとして扱い、どのevidenceを配布するかを明示します。
生成側の引き渡しが完了しても、公開先で見つけて取得できることや、保持される期間は分かりません。REL-002で別に確認します。

## 利用者へ渡す情報

利用者が独立して判断できるよう、少なくとも次を渡します。

- Artifactの取得位置と、そのbytesに対するsubject digest
- Statement、predicate type、builder identity、build type
- External parameterとsource inputを解釈する仕様
- 認証bundleと、issuer・identityを評価するための情報
- Generation、authentication、handoffの最終状態と対象run
- Builder identity、build type、認証profileを変更する際の移行情報

[Consumer artifact acceptance](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)は、この契約をconsumer自身のtrusted identity、source、parameter、artifact expectationへ照合します。
Producerやplatformの「SLSA level」自己申告を、そのままconsumer policyにしません。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- ビルド定義から生成処理を外す、失敗を無視する、job製のstatementへ差し替える場合に公開へ進めないか。
- Jobが`builder.id`、ソースrevision、外部入力を偽っても、基盤由来の事実として認証されないか。
- 成果物の変更、digestの差替え、一部出力の欠落、別runのstatement再利用を拒否するか。
- 認証前後の改変、未承認の認証identity、generatorや保存先の障害を成功に変えないか。
- 基盤が記録した利用者由来の入力を、承認済みのリリース入力と取り違えないか。

これらは診断・設計レビューの確認項目であり、実際の基盤で試した結果ではありません。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| SLSA Build track v1.2 Build L1「Platform generates provenance」 | ビルド基盤が来歴を自動生成し、出力した成果物へ結び付ける責任に関係する。 | 実際に生成した来歴は未確認。 |
| SLSA Build track v1.2 Build L2「Platform authentic provenance」 | 基盤が確認した事実とjobから渡る値を分け、基盤の権限で来歴を認証する責任に関係する。 | 基盤の信頼境界、署名権限、利用者側の検証は未確認。 |

対象特性と例外は[マッピング](../../../../mappings/frameworks.yaml)にあります。このControlだけでSLSA Build L1・L2の達成を示しません。

## このコントロールの範囲

対象は基盤側の来歴生成、成果物との対応、各fieldの情報源、出所の認証です。SLSAの版やlevelによって利用者由来のfieldを許す条件は異なります。すべてを基盤が直接作ったと推測せず、[上の方式説明](#責任と情報源)で採用方式の境界を確認します。来歴が正確でも、入力がリリース用に承認されたとは限りません。

ビルド中の権限は[BUILD-001](../psb-build-001-build-containment/README.md)、承認した手順との照合は[BUILD-002](../psb-build-002-approved-consistent-build/README.md)、来歴の配布は[REL-002](../../release-integrity/psb-rel-002-provenance-distribution-availability/README.md)、利用者の受入判断は[REL-001](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)へ渡します。来歴は成果物の無害性を示しません。旧synthetic JSONとlocal keyによる例は基盤側の生成やidentity保護を示さないため移植していません。

[教材](learning.md)、特性IDと根拠を残した[control.yaml](control.yaml)、[Sources](../../../../sources/README.md#spec-platform-provenance-generation)、[移行記録](../../../../docs/MIGRATION_BUILD.md#platform-provenance-migration)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。

工程間の受け渡しは[ビルドした成果物を署名・公開し、使用するまで](../../../../engineering/release-build-to-use.md)で確認できます。
