# PSB-GOV-005: Deployed artifact recovery

設計する：[Deployed artifact rebuild and replacement](../../../../engineering/governance-operations/deployed-artifact-recovery/README.md)

## 問い

影響する稼働artifactが判明した後、現在のriskに基づく期限付き判断を行い、信頼できる経路で別digestを再構築・配布し、
元の調査範囲から旧digestが非稼働になったことを確認するまでremediationを閉じない状態にできるか。

## できてはいけないこと

Findingの記録、rebuild jobの成功、新tagの作成、一つのenvironmentへのrolloutだけを復旧完了としてはいけません。
同じbytes、別source、証拠の欠けたbuild、未承認artifactがreplacementになったり、一部environmentに旧digestが残ったり、
inventory・scanner・registry・deploymentの取得障害が`NOT_AFFECTED`または`REMEDIATED`になってはいけません。

## 起点となるシナリオ

稼働imageのbase imageに脆弱性が判明し、teamはpipelineを再実行して同じtagをpushしました。主要clusterは更新されましたが、
実際のnew digestをrelease判断へ結び付けておらず、別regionはold digestを実行しています。Job成功やtag名では、危険なbytesが
本番から消えたことを説明できません。

本controlは影響確定後のrebuild・replacement・旧artifact非稼働のclosureを扱います。影響範囲の特定は
[GOV-001](../psb-gov-001-supply-chain-impact-assessment/README.md)、scanner evidenceの信頼性は
[DETECT-001](../../detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)、artifactのconsumer側受入は
[REL-001](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)の責任です。

## 適用範囲

脆弱性、侵害、support終了、base image・dependency・registry lifecycleの変化により、再構築または置換が必要と判断された
稼働artifactと、そのsource revision、build、provenance、signature、SBOM、release、registry object、deploymentを対象にします。

次は直接の対象ではありません。

- Scanner、SBOM generator、builder、signer、registry、admission controller、deployment collectorを実装すること。
- Vulnerability intake全体、priority policy、一般的なpatch management、credential incidentを定義すること。
- 新artifactの内容が無害であることを、fresh buildやsignatureだけから証明すること。
- 実本番のrollout、削除、rollbackをfixtureやrepository内の状態変更として実行すること。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `ARTIFACT-RECOVERY-1` | 元の調査範囲について、active deployment、environment、immutable artifact digest、artifact-bound SBOM、観測時刻と未観測範囲を一つのrecovery caseへ固定する |
| `ARTIFACT-RECOVERY-2` | Exact digestとcomponentに対するvulnerability applicability、support、base image、registry lifecycleのcurrent evidenceと取得healthを分け、古い署名や空結果を現在安全の証拠にしない |
| `ARTIFACT-RECOVERY-3` | 影響artifactにowner、判断時刻、risk根拠、期限、target environments、clean-build条件、例外またはrollback条件を持つresponse decisionを割り当てる |
| `ARTIFACT-RECOVERY-4` | Replacementをold artifactと異なるdigestへ結び付け、reviewed source、build invocation、provenance、signature、artifact-bound SBOM、release decisionのidentityを照合する |
| `ARTIFACT-RECOVERY-5` | 承認したreplacement digestとregistry publication、admission、各target deploymentのobserved digestを照合し、tagの一致で代用しない |
| `ARTIFACT-RECOVERY-6` | Original scopeのすべてをfreshに再観測し、affected old digestがactiveでないことをreplacement成功とは独立に確認する |
| `ARTIFACT-RECOVERY-7` | `NOT_AFFECTED`、`IN_PROGRESS`、`OVERDUE`、`REMEDIATED`、security failure、evidence errorを分け、欠落・stale・partial・unavailable・配送失敗をclosureへ変換しない |

## 実装判断の羅針盤

GOV-001が渡すexact digestとdeployment scopeをcaseの起点にします。Mutable tag、release名、repository名だけで対象を固定しません。
Vulnerability findingはrebuildの入力ですが、applicability、support、compensating condition、現在の稼働範囲を評価してdecisionを所有させます。

Clean rebuildは同じpipelineの再実行という意味ではありません。侵害原因、dependency resolution、cache、builder、credential、source、
署名経路を見直し、原因を再導入しない経路を選びます。Replacementのdigestが異なるだけでも十分ではなく、consumerの期待値へ
source・build・artifact evidenceを結び直します。

New digestの稼働とold digestの非稼働は別の主張です。Targetごとのdeployment観測をoriginal scopeと照合し、未知environment、
停止collector、rollback可能性を未解決として残します。緊急rollbackでold digestを再導入する場合は、新しいrisk decisionと期限を必要とします。

## Negative testの観点

次は脆弱性診断、設計レビュー、tabletop exerciseで列挙する観点です。テストコードの実行済み状態を意味しません。

- Image tagやrelease名だけで稼働artifactを同定し、実digestとSBOMが一致しない。
- Scanner、advisory、support、registry lifecycle evidenceがstale・partial・unavailableでも`NOT_AFFECTED`にする。
- 影響があるのにowner・期限がない、または手動でpriority・deadlineを弱めても記録しない。
- Old bytesをnew tagで再公開する、同じdigestをrebuild済みとする、異なるsource revisionから作る。
- Build、provenance、signature、SBOMのいずれかが別artifactを指してもreplacementを受け入れる。
- Registryへnew digestを置いただけで、admission・deploymentのobserved digestを確認しない。
- 一つのclusterだけ更新してcaseを閉じ、別region、停止workload、rollback slotにold digestが残る。
- Collector停止、pagination欠落、観測権限不足、通知失敗をold digest 0件として扱う。
- `IN_PROGRESS`や`OVERDUE`を成功exitまたはclean dashboardへ正規化する。
- Fixtureの`REMEDIATED`をlive rebuild・publication・rollout・old digest removalの証拠にする。
- Evidence outputへcredential、exploit payload、customer data、internal endpointを含める。

## 判定例

| 観測した状態 | このcontrolでの判断 |
|---|---|
| Exact digestはaffectedだが、期限内でrebuild中 | `IN_PROGRESS`。合格やremediatedではない |
| New digestを全targetで観測したが、original scopeの一部collectorが停止 | Closureを裏付けない。Evidence errorまたは未解決 |
| Completeなcurrent evidenceがexact digestを非該当と判断した | 範囲付き`NOT_AFFECTED`になり得る。将来の安全は保証しない |
| New digestが受入済みで、freshなoriginal-scope観測にold digestがない | `REMEDIATED`の証拠になり得る。Case外の未知環境は保証しない |
| Signatureは正しいがsupport終了したold digestが稼働中 | 不合格候補。真正性は現在の運用riskを解消しない |

## 保証しない範囲

Fresh rebuildは未知脆弱性や悪意ある変更の不存在を保証しません。Inventoryとcollectorのcoverage外、停止中のworkload、
未管理環境、将来のrollbackも残余リスクです。本成果物はlive rebuild、registry、admission、deploymentを検証していません。

## 関連資料

- [Deployed artifact rebuild and replacement](../../../../engineering/governance-operations/deployed-artifact-recovery/README.md)
- [Supply-chain impact assessment](../psb-gov-001-supply-chain-impact-assessment/README.md)
- [Scanner evidence trust boundary](../../detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)
- [Consumer artifact acceptance](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)
- [旧成果物との対応](../../../../docs/DEPLOYED_ARTIFACT_RECOVERY_MIGRATION.md)
- [参照資料と採否](../../../../sources/README.md#ref-deployed-artifact-recovery-001)

## Framework mapping

NIST SSDF 1.1の`RV.1.1`を`ARTIFACT-RECOVERY-2`、`RV.2.1`を`ARTIFACT-RECOVERY-3`へ、
それぞれ`supports / medium / design-reviewed`として部分対応させます。ATT&CK v19.1の`T1195.002 Compromise Software Supply Chain`は
`ARTIFACT-RECOVERY-4,5,6 / mitigates / medium / design-reviewed`です。旧OSPS `OSPS-DO-04.01`はsupport文書の公開要件であり、
本controlの実行成果ではないため非継承です。詳細は[移行記録](../../../../docs/DEPLOYED_ARTIFACT_RECOVERY_MIGRATION.md#旧framework-mapping)に保持します。
