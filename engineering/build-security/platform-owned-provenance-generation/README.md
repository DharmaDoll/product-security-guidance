# ENG-BUILD-002: Platform-owned provenance generation

## 利用場面と推奨構造

Release artifactを作るcodeと、そのbuildについて証言する主体を分ける設計です。
Platform control planeが、build eventと確定した出力を基にprovenanceを生成し、consumerが検証できるidentityで認証します。

```text
承認されたbuild要求 ───────┐
                            v
                   user-defined build
                            |
                    確定したoutput bytes
                            |
                            v
platform event ──> control-plane generator ──> artifact digestに結合したprovenance
                            |                              |
                 platform-owned identity                  v
                            └──────────────────> 認証bundle／handoff
                                                           |
                                                           v
                                            consumer-owned policyで照合
```

Generatorと認証能力はuser-defined buildの外側に置きます。Build jobは出力を渡せても、信頼済みbuilderの主張、platform event、認証結果を任意に作れない構造にします。

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

## 方式の選択

| 方式 | 選ぶ条件・代償 |
|---|---|
| Platform native attestation | Platformが生成境界、field source、identity、bundle取得方法を文書化している場合。最も単純だがproviderのschema、retention、identity lifecycleへ依存する |
| Platform-owned external generator | Build eventと確定outputをcontrol plane APIから取得でき、generatorをtenant jobから隔離できる場合。Adapter、再試行、重複排除、API障害の扱いを所有する必要がある |
| Rebuilderによるprovenance | 独立した再buildを正式なproducerとして扱える場合。元buildとの同一性、再現性、builder identity、配布対象を別に定義する必要がある |
| Job-generated metadata | DebugやL1相当の存在確認には使える場合がある。Platform由来のauthentic provenanceとしては扱わず、後からplatform署名するだけでfieldの信頼性を上げない |

認証方式は、provider発行の短命certificateとbundle、platform service key、KMS／HSM等から選びます。
署名方式だけで決めず、identityのscope、失効、時刻、transparency、offline verification、consumerのtrust root更新を一つのprofileとして決めます。

## 生成とhandoffの状態遷移

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
Handoff完了は、公開先でのdiscoverabilityやretentionを証明しません。それらはprovenance distributionの別設計です。

## Consumerへ渡す契約

Consumerが独立に判断できるよう、少なくとも次を渡します。

- Artifactの取得位置と、そのbytesに対するsubject digest
- Statement、predicate type、builder identity、build type
- External parameterとsource inputを解釈する仕様
- 認証bundleと、issuer・identityを評価するための情報
- Generation、authentication、handoffの最終状態と対象run
- Builder identity、build type、認証profileを変更する際の移行情報

[Consumer artifact acceptance](../../release-integrity/consumer-artifact-acceptance/README.md)は、この契約をconsumer自身のtrusted identity、source、parameter、artifact expectationへ照合します。
Producerやplatformの「SLSA level」自己申告を、そのままconsumer policyにしません。

## 導入時の確認

設定画面の有効化だけで完了にせず、[controlの診断観点](../../../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md#negative-testの診断観点)をproviderの無害な試験projectへ具体化します。
成功、policy violation、evidence unavailableを区別して記録し、実secretや本番signing keyを試験へ入れません。

Platform固有の実装例を追加する場合は、対象版、生成を有効化する設定、実際のstatement取得、identityとfield source、consumerでの確認、失敗時のrelease gate、既知の制限を一組で示します。
本patternだけではそのどれも導入済みになりません。

## このpatternの範囲

旧OpenSSL fixtureは、local test keyでsynthetic statementを検証していましたが、platform control planeやkey protectionを構築していません。そのため移植していません。
承認builderと一貫したbuild process、provenanceの配布、artifact signing、SBOM、consumer verification、admissionは独立した成果物として接続します。

- [Control](../../../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)
- [参照仕様と採否](../../../sources/README.md#spec-platform-provenance-generation)
- [Consumer artifact acceptance](../../release-integrity/consumer-artifact-acceptance/README.md)
- [Build execution boundary](../build-execution-boundary/README.md)
