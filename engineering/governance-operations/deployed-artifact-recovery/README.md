# Deployed artifact rebuild and replacement

`ENG-GOV-004` / `governance-operations`

## 解く設計問題

影響を受ける稼働artifactの発見を、本番からaffected bytesがなくなったという復旧判断へ接続します。対象読者はPSIRT、
release manager、build platform、registry・deployment platform、service ownerです。

## 推奨構造

```text
GOV-001 exact affected digest + original deployment scope
  → current applicability / support / lifecycle evidence
  → owned response decision + deadline
  → cause-aware clean build → distinct digest + bound evidence
  → release acceptance → immutable publication → per-target admission and rollout
  → fresh original-scope observation → old digest inactive
  → REMEDIATED or unresolved state
```

一つのorchestratorへ全権限を集めません。Evidence reader、rebuild initiator、release approver、deployment operator、
post-deployment observerを分け、各段階をexact digestとcase identityで接続します。

## 境界と強制点

| 境界 | 入力 | 強制・確認 | 出力 |
|---|---|---|---|
| Impact handoff | GOV-001のdigest・SBOM・deployment scope | Scope・鮮度・未観測範囲 | Recovery case |
| Risk decision | Vulnerability・support・lifecycle evidence | Applicability、owner、期限、例外 | Rebuild/replace decision |
| Clean build | Reviewed sourceと修復済みinput | Causeを再導入しないbuilder・dependency・cache条件 | Distinct digestとbuild evidence |
| Release / publish | Replacement digestとconsumer expectation | Provenance・signature・SBOM、immutable publication | Accepted registry object |
| Admission / rollout | Accepted digestとtarget set | Digest-based admission、targetごとのobserved state | Deployment observations |
| Closure | Original scopeとpost-rollout observations | Old digest 0、coverage・freshness・health | REMEDIATEDまたはopen/error |

Provenance生成は[BUILD-003](../../build-security/platform-owned-provenance-generation/README.md)、registry publicationは[CONTAINER-002](../../container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md)、artifactの使用許可は[CONTAINER-001](../../container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)へ接続します。
いずれもlive実装は未確認です。本patternは設計成果物の存在を実装済みに変えず、REL-001のconsumer acceptanceとGOV-001の観測を接続点として示します。

## Clean rebuildの判断

Rebuild前に、何がartifactを危険にしたかを分類します。Dependencyやbase imageの更新だけで済む場合と、source・builder・credential・
signerまで侵害された場合では、再利用できる入力と基盤が異なります。侵害された可能性のあるcache、workspace、secret、runner、
build definitionから同じ経路を再実行してもclean rebuildとは呼べません。

Replacement evidenceはold digestとの相違だけでなく、reviewed source revision、解決したdependency graph、build invocation、
provenance、signature、artifact-bound SBOM、release decisionを同じnew digestへ結びます。各隣接controlがない場合はclosure blockerです。

## 状態とevidence contract

`NOT_AFFECTED`、`IN_PROGRESS`、`OVERDUE`、`REMEDIATED`をsuccess booleanへ潰しません。Security invariantへの違反と、
証拠を取得・解釈できないerrorも分けます。Evidenceにはcase ID、scope identity、digestの参照、source・build・release・deployment
receipt identity、owner、時刻、状態、未観測範囲を残し、credential、exploit payload、customer dataを複製しません。

`REMEDIATED`には少なくとも、replacementの受入、全targetのobserved new digest、original scopeのfresh observation、
old digestの非稼働が必要です。Scale-to-zero中のworkload、rollback slot、disconnected environmentをどう扱うか事前に決めます。

## 失敗経路と確認方法

Mutable tagによる対象誤認、stale scannerによる非該当判定、same-digest rebuild、別artifactのSBOM・signature、partial rollout、
collector停止を0 instancesとする処理、期限超過の成功化を負のシナリオとして確認します。Test codeがない場合も、
controlのnegative test観点をdiagnostic checklistとして使用できます。

Tabletopでは架空digestとenvironmentを使い、evidence欠落・partial rollout・緊急rollbackがclosureを止めることを確認します。
Live testは非本番の専用artifactとtargetで行い、本番削除やrollbackをrepository testから実行しません。

## 具体実装を追加する条件

Builder、registry、admission、deployment inventoryの組合せで実装が変わるため、provider-neutralなverifierを移植しません。
実装は次を選定できる場合に追加します。

1. Artifact format、builder、registry、deployment platform、target scopeが明確である。
2. Digest、provenance、signature、SBOM、publication、admission、observed deploymentを取得する公式contractを確認できる。
3. Non-productionでsame-digest、mismatch、partial rollout、collector failureを安全に再現できる。
4. Fixture stateとlive mutation evidenceを区別し、mutation権限をread-only verifierから分離できる。

旧JSON case、policy、Python verifierはmetadataの整合しか検証せず、live rebuildとrolloutを証明しないため非移植です。

## 関連資料と限界

[Control](../../../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)、
[移行記録](../../../docs/DEPLOYED_ARTIFACT_RECOVERY_MIGRATION.md)、
[参照資料](../../../sources/README.md#ref-deployed-artifact-recovery-001)を参照してください。
本patternは設計と診断観点であり、稼働環境のremediationを証明しません。
