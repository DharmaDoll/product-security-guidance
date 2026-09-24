# PSB-CONTAINER-002: Container registry publication boundary

## 問い

承認したOCI artifactをexact identityのままregistryへ公開し、誰がどのrepositoryを変更・取得できるか、公開後に何を不変とし、いつ使用対象から外すかを追跡できるか。

## できてはいけないこと

Publisherが別製品のrepositoryやregistry管理面へ書き込んだり、公開済みrelease tagを別digestへ付け替えたり、保護したmanifestを証拠なく削除したりしてはいけません。
Audit・inventory・registry APIの欠落を、変更なし・stale artifactなしとして扱ってはいけません。

## 適用範囲と非適用

Registry endpoint、repository、pull／push／delete／administrationのauthority、publisher identity、OCI descriptorとdigest、release reference、audit、deprecated／quarantined／removed lifecycleが対象です。

Artifactのbuild・署名・provenance生成、内容の脆弱性やmalware、consumerの受入は別の成果です。[Deployment artifact admission](../psb-container-001-deployment-artifact-admission/README.md)は非active artifactを使用時に拒否するconsumerです。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `REGISTRY-1` | Clientとautomationが、認証したexact registry endpointへ保護された通信で接続し、credential・manifest・layerを意図しないmirrorやendpointへ渡さない |
| `REGISTRY-2` | Humanとworkloadの権限をexact registry、repository、actionへ限定し、anonymous・unmatched・cross-repositoryの変更と不要なdelete／administrationを既定拒否する |
| `REGISTRY-3` | Automationは実行主体・repository・action・audience・期限へ結合した短命identityを使い、再利用可能なregistry credentialをjobやartifactへ保存しない |
| `REGISTRY-4` | 公開したrelease referenceをexact OCI descriptor digestへ結び、保護後のtag付替え・manifest置換・証拠なき削除を防ぐ。変更は新しいidentityとして扱う |
| `REGISTRY-5` | Sensitive pull、全mutation、権限・policy変更をactor、repository、action、digest、outcome、時刻、request identityへ結び付け、機微情報を除いて監査できる |
| `REGISTRY-6` | Active、deprecated、quarantined、removed等の状態、deployability、期限、判断根拠を分け、stale・revoked artifactを無期限に使用可能なまま残さない |
| `REGISTRY-7` | API、authorization、audit、inventory、lifecycle evidenceの欠落・stale・partial・pagination失敗・schema不一致・取得不能をcleanと区別する |

## 実装判断の羅針盤

OCI digestはbytesのidentityです。誰が公開してよいか、tagを変更できるか、いつ利用を止めるかは別のregistry policyです。
Tagを人向けの参照として残す場合も、release decision、audit、admissionはdigestを正本とし、tagの付替えを新しいartifactの公開として扱います。

Immutabilityとretentionは同じではありません。監査・rollback・incident responseに必要なbytesとevidenceを保持しつつ、deprecatedやquarantined artifactをadmissionで使用不可にできます。
削除を急ぐ場合も、対象digest、依存するdeployment、証拠保全、復旧方法を確認します。

## Negative testの診断観点

- HTTP、予期しないmirror、別CA／service identity、TLS評価不能なendpointへfallbackしないか
- Anonymous write、wildcard repository、cross-repository push、publisherによるdelete／adminを拒否できるか
- 期限切れ・wrong audience・保存済み・別jobのworkload identityを再利用できないか
- 保護したtagを別digestへ付け替え、同じdigest名で異なるbytesを返し、保護manifestを削除できないか
- Sensitive pull、成功・拒否したmutation、policy変更のauditが欠落・改変・遅延したときに検出できるか
- Deprecated／quarantined artifactがtag、digest、cache、replicaの別経路から使用可能にならないか
- Pagination、replication delay、API timeout、collector停止、partial inventoryを「対象なし」に変換しないか

これらは診断観点であり、本PJがlive registryで実施した結果ではありません。

## 保証しない範囲

Registryにあるartifactが安全、脆弱性なし、信頼したsourceからbuild済みであるとは保証しません。Registry管理者やprovider control planeの侵害、availability、backup、geo-replication、法的retentionも別途確認が必要です。

Providerを選んでいないため設定・API・collector実装は追加していません。旧JSON policy、operation、audit、inventory、Python verifierはlive registryの実効権限・immutability・audit完全性を証明しないため移植していません。

- [Container registry publication and lifecycle pattern](../../../../engineering/container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md)
- [参照資料と採否](../../../../sources/README.md#ref-container-registry-publication-001)
- [Framework mapping](../../../../mappings/frameworks.yaml)
- [移行記録](../../../../docs/CONTAINER_REGISTRY_MIGRATION.md)
