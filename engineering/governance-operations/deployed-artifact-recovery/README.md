# Deployed artifact rebuild and replacement

`ENG-GOV-004` / `governance-operations`

## 解く設計問題

影響を受ける稼働artifactの発見を、本番からaffected bytesがなくなったという復旧判断へ接続します。対象読者はPSIRT、
release manager、build platform、registry・deployment platform、service ownerです。

## 推奨構造

```text
GOV-001 exact affected digest + original deployment scope
  → current applicability / support / lifecycle evidence
  → GOV-003 priority + deadline for vulnerability cases, or another owned risk decision
  → owned execution plan; GOV-002 exception if temporarily continuing use
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
| Response handoff | 脆弱性対応ではGOV-003の優先度・期限。その他は現在のrisk・support・lifecycle evidence | Ownerと対象環境、元の期限と例外期限の区別 | Rebuild/replace plan |
| Clean build | Reviewed sourceと修復済みinput | Causeを再導入しないbuilder・dependency・cache条件 | Distinct digestとbuild evidence |
| Release / publish | Replacement digestとconsumer expectation | Provenance・signature・SBOM、immutable publication | Accepted registry object |
| Admission / rollout | Accepted digestとtarget set | 置換targetのdigest-based admission・observed state、廃止targetの停止・削除と再起動経路 | Targetごとの置換・廃止・未解決状態 |
| Closure | Original scopeとpost-rollout observations | Old digest 0、coverage・freshness・health | REMEDIATEDまたはopen/error |

Provenance生成は[BUILD-003](../../build-security/platform-owned-provenance-generation/README.md)、registry publicationは[CONTAINER-002](../../container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md)、artifactの使用許可は[CONTAINER-001](../../container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)へ接続します。
いずれもlive実装は未確認です。本patternは設計成果物の存在を実装済みに変えず、REL-001のconsumer acceptanceとGOV-001の観測を接続点として示します。

脆弱性対応ではGOV-003の組織期限を、置換計画の作業日程とは別に保持します。別の起点では担当者が決めた対応期限を保持します。GOV-002が旧digestの一時使用を承認しても、元の期限は上書きせず、旧digestが残るケースを`REMEDIATED`へ移しません。元の期限を超えたら`OVERDUE`を保持します。例外の取消・期限切れ・評価不能が利用許可へ反映される経路を、実際の使用判断と結び付けます。

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

`REMEDIATED`には少なくとも、置換targetでのreplacementの受入とobserved new digest、廃止targetでの停止・削除と再起動経路の確認、original scopeのfresh observation、
old digestの非稼働が必要です。Scale-to-zero中のworkload、rollback slot、disconnected environmentをどう扱うか事前に決めます。
Rollbackが旧digestを再投入できるなら、その経路を制限・更新した記録も確認します。元の調査範囲に未観測の環境が残る場合、そこを除外した狭い完了判断へ黙って変えません。

Closureには、元の各targetに対する現在の稼働digest、観測時刻、collectorの対象範囲・取得結果と、停止中または廃止したtargetの扱いを対応付けます。検知アラートの不在やrolloutの成功表示は、このinventoryを代用しません。Desired stateが新digestでも旧processが残り得るため、採用先で実際の稼働状態を確認します。対象が廃止された場合も、単に検索から消えたのか、旧digestを再投入する設定まで失効したのかを分けます。

## 失敗経路と確認方法

Mutable tagによる対象誤認、古いscannerによる非該当判定、同じdigestを再build済みとする処理、別artifactのSBOM・signature、
一部だけのrollout、collector停止を0件とする処理、期限超過の成功化を確認します。テストコードがない場合も、
[controlの診断で確認する項目](../../../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md#failure-checks)をチェックリストとして使えます。

Tabletopでは架空digestとenvironmentを使い、evidence欠落・partial rollout・緊急rollbackがclosureを止めることを確認します。
Live testは非本番の専用artifactとtargetで行い、本番削除やrollbackをrepository testから実行しません。

## 具体実装を追加する条件

Builder、registry、admission、deployment inventoryの組合せで実装が変わるため、provider-neutralなverifierを移植しません。
採用先で導入・確認に実効性があり、次を選定できる場合だけ実装を検討します。

1. Artifact format、builder、registry、deployment platform、target scopeが明確である。
2. Digest、provenance、signature、SBOM、publication、admission、observed deploymentを取得する公式contractを確認できる。
3. Non-productionでsame-digest、mismatch、partial rollout、collector failureを安全に再現できる。
4. Fixture stateとlive mutation evidenceを区別し、mutation権限をread-only verifierから分離できる。

旧JSON case、policy、Python verifierはmetadataの整合しか検証せず、live rebuildとrolloutを証明しないため非移植です。

## 関連資料と限界

[Control](../../../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)、
[教材](../../../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/learning.md)、
[移行記録](../../../docs/DEPLOYED_ARTIFACT_RECOVERY_MIGRATION.md)、
[参照資料](../../../sources/README.md#ref-deployed-artifact-recovery-001)を参照してください。
本patternは設計と確認項目を示すものであり、稼働環境で復旧できたことを証明しません。
