# ENG-CONTAINER-001: Deployment artifact admission boundary

## 利用場面と推奨構造

Release時に受け入れたartifactと、実際に使おうとしているartifactを同じexact identityで結び、最後の使用許可へ接続する設計です。

```text
Consumer policy + trust root
            |
            v
exact artifact digest ──> acceptance decision / authenticated receipt
            |                           |
            └──────────────┬────────────┘
                           v
deployment request -> 全artifactを列挙 -> final-state admission -> ALLOW / DENY / ERROR
                                                   |
                                                   v
                                        runtime observationへdecisionを引継ぐ
```

Admissionは過去のCI passを読むだけの処理にしません。Consumer policy、artifact bytes、実行targetのうち、どれに対する判断かを一つのdecisionへ結び付けます。

## Decision contract

| 要素 | 必要な意味 | 避ける状態 |
|---|---|---|
| Artifact set | Repository／package identity、digest、各containerやmoduleの役割 | Tag、名前、一つ目のimageだけ |
| Acceptance | Consumer policyで評価したsignature、provenance、builder、source、parameter | Producerのlevel自己申告、`verified: true` annotation |
| Target | Cluster、environment、tenant、workload class等、policyが区別する範囲 | 別環境へreceiptを流用 |
| Policy identity | Version、trust root／identity profile、変更時刻 | 「最新」だけで再現不能 |
| Decision | ALLOW／DENY／ERROR、reason、decision ID、評価時刻、期限 | Booleanだけ、ERRORをALLOWへ変換 |
| Audit | Request identity、artifact digest、policy、結果、enforcement point | Secret、token、provenance全文、image内容の複製 |

Receiptを使う場合は、このcontractをconsumer policy serviceが認証します。Receiptの署名が有効でも、targetやpolicy versionが違う場合は使いません。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| Admission内でconsumer verification | Evidenceを使用時に取得でき、latency・availability・rate limitを許容できる場合。最も新しい判断を使えるが、registryやevidence serviceの障害がdeploymentへ影響する |
| 事前評価した認証済みreceipt | Release gateとadmissionを疎結合にし、offline確認や低latencyが必要な場合。期限、revocation、target binding、replay防止、policy更新後の再評価を設計する必要がある |
| Control-plane内のdeclarative policy | Requestだけでdigest pin、repository、field、receipt metadataを評価できる場合。外部evidence取得や一般的な暗号検証を無理に埋め込まない |
| External validating service | Registry・provenance・policy serviceとの照会が必要な場合。HA、timeout、TLS identity、cache、dependency loop、upgrade compatibilityを所有する |
| Runtime／node側のpull enforcement | Admission後の差替えやnode cacheも制限する必要がある場合。Admission decisionとのidentity連携が必要で、request時のowner・target判断を単独では代替しない |

Kubernetesの現在の公式ガイダンスは、単純なvalidationにはCEL-based admissionを優先し、外部dataを扱う複雑な検査にはdynamic admissionを利用できると説明しています。
これは製品選定の入力であり、CELやwebhookをcontrolの意味にはしません。

## Kubernetesへ適用するときの境界

Kubernetes adapterを作る場合は、少なくとも次を明示します。

- Deployment、StatefulSet、DaemonSet、Job、CronJob等のPod templateと、直接作成されるPodのどこを評価するか
- Regular、init、ephemeral containerと、platformが追加するsidecar等のimageをいつ列挙するか
- Mutating admission後のfinal objectをvalidating boundaryで確認する順序
- `CREATE`、`UPDATE`、ephemeral container等のsubresource、等価なAPI version、rollbackのcoverage
- Validating policy／webhookの`failurePolicy`、timeout、match条件、除外namespace、設定変更権限
- Registry manifestとprovenanceを取得するidentity、TLS、cache、freshness、rate limit
- Admissionのdigestと、node／runtimeが実際にpull・実行したdigestを後続inventoryでどう照合するか

Built-in field policyとexternal verifierを併用する場合、片方の成功だけでallowにしません。全必須decisionが同じartifact setとrequestへ結び付いたときだけallow候補にします。

## Bypassと障害を設計する

対象外namespaceやbreak-glassは、通常policyの穴ではなく[Security exception lifecycle](../../governance-operations/security-exception-decision-boundary/README.md)へ結び付けます。
Exact target、artifact、property、owner、期限を評価時に確認し、失効・期限切れ・取得不能は通常のdenyへ戻します。

Evaluatorの停止時に可用性を優先する必要があるsystem componentは、一般workloadと同じ暗黙fallbackにしません。
Bootstrap dependency、disaster recovery、cluster add-onを別のscopeと強制点へ分け、誰がどの期間どのartifactを許可したかを残します。

## 導入時の確認

[Controlの診断観点](../../../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md#negative-testの診断観点)を、隔離したtest environmentで各deployment経路へ具体化します。
正常なexact digest、policy violation、evidence unavailableを区別し、本番credentialや悪性imageを試験へ使いません。

実装例を追加する場合は、cluster／platform version、admission API、変更するpolicy、consumer verifierまたはreceipt schema、registry取得方法、全経路のcoverage、deny・errorの観測、rollbackを一組で示します。

## このpatternの範囲

旧verifierはsynthetic AdmissionReview、OCI manifest、provenance、platform-evidence JSONを一つのPython processで検査しました。
Live API serverのmutation order、policy coverage、registry、CNI、runtimeを検証していないため移植していません。

旧`CNT-003..008`のnon-root、capability、host、filesystem、seccomp、resource、networkは、artifact admissionとは別のworkload confinement主題です。
Artifactが正規でも、それらの設定やapplicationの安全性は保証されません。

- [Control](../../../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)
- [Consumer artifact acceptance](../../release-integrity/consumer-artifact-acceptance/README.md)
- [Runtime detection to triage](../runtime-detection-to-triage/README.md)
- [参照資料と採否](../../../sources/README.md#ref-deployment-artifact-admission-001)
