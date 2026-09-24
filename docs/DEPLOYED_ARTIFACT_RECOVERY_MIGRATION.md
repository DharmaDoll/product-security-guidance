# Deployed artifact recovery移行記録

## 結論

旧`PSB-GOV-005`から、current risk evidence、期限付きresponse decision、clean rebuild、exact digest replacement、
old digest非稼働、closure stateをcontrolとpatternへ移しました。旧offline fixtureとverifierは移植しません。

- [PSB-GOV-005 Deployed artifact recovery](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)
- [ENG-GOV-004 Deployed artifact rebuild and replacement](../engineering/governance-operations/deployed-artifact-recovery/README.md)

移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`の
`controls/governance-operations/deployed-artifact-refresh/`です。

## Checkの対応

| 旧check | 新しいproperty | 判断 |
|---|---|---|
| `DAR-001` Active deployment inventory | `ARTIFACT-RECOVERY-1` | GOV-001から受け取るoriginal scopeとrecovery caseの結合へ整理 |
| `DAR-002` Current risk evidence | `ARTIFACT-RECOVERY-2` | Vulnerability applicability、support、base image、registry lifecycleと取得healthを分離 |
| `DAR-003` Bounded rebuild decision | `ARTIFACT-RECOVERY-3` | Owner・期限・target・clean-build・例外条件へ継承。Synthetic deadlineは非継承 |
| `DAR-004` Clean rebuild evidence | `ARTIFACT-RECOVERY-4` | Distinct digestとsource・build・artifact evidenceの結合へ継承 |
| `DAR-005` Publication and admission | `ARTIFACT-RECOVERY-5` | Registry・admission・observed deploymentのexact digest照合へ継承 |
| `DAR-006` Old digest inactive | `ARTIFACT-RECOVERY-6` | Replacement成功と独立したoriginal-scope再観測として継承 |
| `DAR-007` States and failure semantics | `ARTIFACT-RECOVERY-7` | Open・overdue・remediated・failure・errorの区別として継承 |

## 旧実装の扱い

| 旧成果物 | 判断 | 理由 |
|---|---|---|
| JSON policyとcase fixtures | 非移植 | Synthetic timestamp、digest、receiptはlive scope・rebuild・rolloutを証明しない |
| `scripts/verify.py` | 非移植 | Provider-neutral metadataの整合検査であり、builder・registry・admission・deploymentの実状態を読まない |
| Fixture mutation tests | 非移植 | Verifier contractのtestであり、observable security outcomeのtestではない |
| Negative scenarios | 観点として移行 | 診断・設計review・tabletopで利用し、実行済みとは扱わない |

GOV-005は複数platformのidentity chainとmutationを必要とし、SOURCE-002のscanner gateのように狭い一実装へ
収束しません。Artifact formatとplatformが選定され、安全な非本番targetがある場合にだけ実装を追加します。

## 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SSDF `1.1 / RV.1.1` | `DAR-001,002,007 / supports / high`、review `2026-08-12` | `ARTIFACT-RECOVERY-2 / supports / medium / design-reviewed`へ縮小。RV.1.1はsoftware・componentのpotential vulnerability情報収集とcredible report調査を支えるが、deployment inventoryとfailure stateは直接定義しない |
| NIST SSDF `1.1 / RV.2.1` | `DAR-003..006 / supports / high`、review `2026-08-12` | `ARTIFACT-RECOVERY-3 / supports / medium / design-reviewed`へ縮小。Risk情報を集めremediation等を計画するtaskであり、clean rebuild・publication・rollout・old digest removalは本PJの拡張 |
| OpenSSF OSPS `2026.02.19 / OSPS-DO-04.01` | `DAR-002,003 / related-to / medium`、review `2026-08-12` | 非継承。Releaseごとのsupport scope・durationをproject documentationへ記載する要件であり、本controlはその情報を入力として消費するだけ |
| MITRE ATT&CK `v19.1 / T1195.002` | `DAR-004..006 / mitigates / medium`、review `2026-08-12` | `ARTIFACT-RECOVERY-4,5,6 / mitigates / medium / design-reviewed`へ部分継承。Compromised artifactの残存を減らす設計関係 |

2026-09-24にSSDF公式本文、OSPS版付き本文、ATT&CK版付きSTIXを再照合しました。Framework mappingは
準拠、導入、完全なmitigationを意味しません。

## 境界と残るgap

GOV-001はaffected artifactとdeploymentを特定し、GOV-005はそのscopeのrecovery closureを所有します。
DETECT-001はscanner acquisition・data・execution evidenceを所有し、REL-001はconsumerがartifactを受け入れる判断を所有します。
Provenance生成は後続の[BUILD-003移行](PLATFORM_PROVENANCE_MIGRATION.md)、registry publicationは[CONTAINER-002移行](CONTAINER_REGISTRY_MIGRATION.md)、artifactの使用許可は[CONTAINER-001移行](DEPLOYMENT_ARTIFACT_ADMISSION_MIGRATION.md)で直接成果物を追加しました。
いずれもlive provider／deployment実装は未確認であり、GOV-005の存在で実装済みとは扱いません。
旧GOV-003のpriority・deadline責任は[別の移行](VULNERABILITY_PRIORITY_MIGRATION.md)で再編集しました。
