# ENG-CONTAINER-002: Container registry publication and lifecycle

## 利用場面と推奨構造

```text
release decision -> short-lived publisher -> exact repository@digest
                         |                         |
                  scoped push authority      protected reference
                                                   |
registry audit + inventory health -----------------+
                                                   v
                              active / deprecated / quarantined / removed
                                                   |
                                                   v
                              consumer verification -> deployment admission
```

Publisher、registry administrator、lifecycle owner、consumerを分けます。Publisherがpushできることを、既存releaseの置換・削除・policy変更権限に広げません。

## 設計する契約

| 境界 | 決めること |
|---|---|
| Endpoint | Exact hostname／service identity、trust root、mirror、client、TLS failure時の動作 |
| Authority | Human／workload identity、repository、pull／push／delete／admin、default deny、break-glass |
| Publication | Manifest／index descriptor、digest、tag、publisher、release decision、成功時刻 |
| Protection | いつtag／digestを保護し、置換・削除をどう拒否し、例外を誰が承認するか |
| Audit | Sensitive read、mutation、policy change、denyをrequest単位で取得し、collector healthをどう確認するか |
| Lifecycle | Active等の状態、deployability、期限、scanner／incident／support decision、admissionへの伝達 |

OCI descriptorのdigestはcontent addressです。取得したbytesのdigestとsizeをconsumerが照合できるようにし、tagは同一性の根拠にしません。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| Provider native immutability | Tag protection、delete protection、auditが必要範囲を満たす場合。Providerのedition、API、例外権限、retention挙動へ依存する |
| Append-only release repository | Releaseを新digest・新referenceだけで公開できる場合。Storage、cleanup、rollback inventoryの費用が増える |
| Promotion repository | Build／stagingからrelease repositoryへexact digestをpromotionする場合。Copy時のdigest保持、authority、evidence bindingを確認する |
| External policy／audit reconciliation | Provider native機能が不足する場合。Race、event loss、pagination、remediation権限、collector identityを所有する |

Lifecycleのnon-deployable状態はregistry削除だけで実現しません。Admission deny list、repository policy、consumer trust decisionを同じdigestへ結び、replicaやcacheも含めて状態を観測します。

## 実装を作る条件

Providerを選んだら、対象service／edition／API version、identity exchange、role、immutability、audit event、pagination、inventory、retention、replication、error contractを公式仕様で固定します。
隔離repositoryと無害なartifactで[診断観点](../../../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md#negative-testの診断観点)を確認し、本番credentialや実releaseを試験に使いません。

Provider-neutral JSON verifierは設定の自己申告を再検査するだけなので作りません。Adapterはlive APIの現在値、拒否挙動、audit deliveryを観測できる単位に分けます。

## このpatternの範囲

Artifact signature／provenanceは[Consumer artifact acceptance](../../release-integrity/consumer-artifact-acceptance/README.md)、publish後の使用許可は[Deployment artifact admission](../deployment-artifact-admission-boundary/README.md)、侵害後の置換は[Deployed artifact recovery](../../governance-operations/deployed-artifact-recovery/README.md)へ接続します。

- [Control](../../../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md)
- [参照資料と採否](../../../sources/README.md#ref-container-registry-publication-001)
