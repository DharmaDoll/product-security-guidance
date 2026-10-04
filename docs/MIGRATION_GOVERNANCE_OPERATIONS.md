# Governance / Operations — 移行判断

この文書は旧成果物の採否・移行時の判断をdomainごとにまとめた履歴です。現在の要件は各control、現在の進捗は[移行計画](MIGRATION_PLAN.md#現在地と次の作業)を確認してください。

## 収録した主題

- [Credential exposure containment移行記録](#credential-exposure-migration)
- [Deployed artifact recovery移行記録](#deployed-artifact-recovery-migration)
- [Product vulnerability priority移行記録](#vulnerability-priority-migration)

<a id="credential-exposure-migration"></a>

<a id="credential-exposure-migration--credential-exposure-containment移行記録"></a>
## Credential exposure containment移行記録

<a id="credential-exposure-migration--結論"></a>
### 結論

旧`PSB-GOV-004`から、credential漏えい後のauthority封じ込め、限定したreplacement、consumer照合、旧authority拒否、
影響調査へのhandoff、closure条件をcontrolとpatternへ移しました。旧provider-neutral JSON fixtureとPython verifierは移植しません。

新成果物:

- [PSB-GOV-004 Credential exposure containment](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)
- [ENG-GOV-003 Credential exposure containment and recovery](../engineering/governance-operations/credential-exposure-containment/README.md)

移行元は旧repository commit `f42987759218c9b8daf3924320542a1935ef78e0`の
`controls/governance-operations/credential-exposure-containment/`です。旧IDと10 checkを履歴として保持し、
新しい7特性へ役割を統合しました。これは実環境への導入やincident対応の完了を意味しません。

<a id="credential-exposure-migration--checkの対応"></a>
### Checkの対応

| 旧check | 新しいproperty | 判断 |
|---|---|---|
| `CRR-001` Relationship inventory | `CRED-CONTAIN-1` | Secret-free identity、consumer、resource、derived authority、windowへ再構成 |
| `CRR-002` Failure semantics | `CRED-CONTAIN-7` | Missing・partial・adapter errorをclosure blockerとして継承 |
| `CRR-003` Evidence and authorization | `CRED-CONTAIN-2` | 継承。ただしevidence-first固定順序を、緊急封じ込めと保全を並行できる条件へ修正 |
| `CRR-004` Class-specific containment | `CRED-CONTAIN-3` | 継承。Token、SSH、signing、short-lived、cloudの確認対象をpatternへ配置 |
| `CRR-005` Bounded replacement | `CRED-CONTAIN-4` | 継承。Provider-neutralなset比較を実装済み証拠にはしない |
| `CRR-006` Consumer disposition | `CRED-CONTAIN-4` | Replacementとconsumer移行を一つの判断へ接続 |
| `CRR-007` Old-authority denial | `CRED-CONTAIN-5` | 継承。漏えい値を使うactive probeを必須にせず、安全なprovider-specific方法を選ぶ |
| `CRR-008` Exposure-window impact | `CRED-CONTAIN-6` | Exact identityと未観測範囲をGOV-001へ渡す責任として継承 |
| `CRR-009` Closure state | `CRED-CONTAIN-7` | 固定state machineではなく、必須状態と未解決範囲の分離として継承 |
| `CRR-010` Secret-free evidence | `CRED-CONTAIN-1,5,7` | 値の非複製とfixture/live evidenceの区別を継承 |

旧checkの「4時間以内のauthorization」「七つのsurface」「固定したstate順序」は一般要件へ継承していません。
参照資料が裏付けない具体値であり、incidentの緊急性、provider、credential classによって安全な順序が異なるためです。

<a id="credential-exposure-migration--旧実装の扱い"></a>
### 旧実装の扱い

| 旧成果物 | 判断 | 理由 |
|---|---|---|
| `secure/`、`insecure/`のpolicy・response bundle | 非移植 | 架空のmetadataとreceiptであり、live inventory・mutation・denialを証明しない |
| `scripts/verify.py` | 非移植 | Providerのpermission hierarchy、session、trust、伝播、auditを扱わず、synthetic stateの整合だけを検査する |
| `tests/test.sh`、fixture mutation | 非移植 | Verifier自身のcontract testにはなるが、controlの観測可能なsecurity outcomeを検証しない |
| Negative scenario | 観点として移行 | 実行コードを必須にせず、診断・設計レビュー・tabletop exerciseへ使える形にした |

SOURCE-002のGit/Gitleaks実装とは性質が異なります。SOURCE-002は候補contentをscannerへ渡し、検出時に拒否する
狭い技術境界を一つの隔離実装で観測できます。GOV-004は複数providerとcredential classを横断し、実APIと安全な
検証環境を選ばなければコードが成果を証明できません。この差は
[主題ごとの具体化判断](ARTIFACT_MODEL.md#主題ごとの具体化判断)に従います。

<a id="credential-exposure-migration--旧framework-mapping"></a>
### 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| MITRE ATT&CK `v19.1 / T1078 Valid Accounts` | `CRR-004..007 / mitigates / medium`、review `2026-08-10` | `CRED-CONTAIN-3,4,5 / mitigates / medium / design-reviewed`へ部分継承。旧正規credentialと派生authorityの継続利用を制限する関係 |
| NIST SSDF `1.1 / RV.2.1` | `CRR-001,003..009 / supports / high`、review `2026-08-10` | 非継承。RV.2.1はsoftware vulnerabilityのriskを分析してremediation等を計画するtaskであり、credential authorityの失効・session・consumer移行を直接定義しない |
| OpenSSF OSPS `2026.02.19 / OSPS-AC-04.01` | `CRR-005,006 / supports / medium`、review `2026-08-10` | 非継承。AC-04.01はCI/CD taskでpermission未指定時のdefaultをpipeline内の最低権限にする要件であり、incident replacementのscope比較ではない |

ATT&CKの版付きSTIX、SSDF公式本文、OSPS版付き本文を2026-09-24に再照合しました。Mappingは設計上の関係であり、
技術の完全なmitigation、framework準拠、実運用を示しません。

<a id="credential-exposure-migration--参照資料の採否"></a>
### 参照資料の採否

NIST SP 800-61 Rev.3はincident responseをrisk managementへ統合し、Detect・Respond・Recoverと継続改善を扱う
上位の運用ガイダンスとして部分採用します。Credential classごとの失効、replacement比較、拒否probeは同文書の
具体要件ではなく、旧controlを再評価した本リポジトリの設計判断です。

製品固有のcredential revocation、session invalidation、signing trust、audit APIを参照資料へ追加するのは、
実装対象providerを選定した時点です。変更可能な最新文書を集めて、汎用controlの導入済み証拠にはしません。

<a id="deployed-artifact-recovery-migration"></a>

<a id="deployed-artifact-recovery-migration--deployed-artifact-recovery移行記録"></a>
## Deployed artifact recovery移行記録

<a id="deployed-artifact-recovery-migration--結論"></a>
### 結論

旧`PSB-GOV-005`から、current risk evidence、期限付きresponse decision、clean rebuild、exact digest replacement、
old digest非稼働、closure stateをcontrolとpatternへ移しました。旧offline fixtureとverifierは移植しません。

- [PSB-GOV-005 Deployed artifact recovery](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)
- [ENG-GOV-004 Deployed artifact rebuild and replacement](../engineering/governance-operations/deployed-artifact-recovery/README.md)

移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`の
`controls/governance-operations/deployed-artifact-refresh/`です。

<a id="deployed-artifact-recovery-migration--checkの対応"></a>
### Checkの対応

| 旧check | 新しいproperty | 判断 |
|---|---|---|
| `DAR-001` Active deployment inventory | `ARTIFACT-RECOVERY-1` | GOV-001から受け取るoriginal scopeとrecovery caseの結合へ整理 |
| `DAR-002` Current risk evidence | `ARTIFACT-RECOVERY-2` | Vulnerability applicability、support、base image、registry lifecycleと取得healthを分離 |
| `DAR-003` Bounded rebuild decision | `ARTIFACT-RECOVERY-3` | Owner・期限・target・clean-build・例外条件へ継承。Synthetic deadlineは非継承 |
| `DAR-004` Clean rebuild evidence | `ARTIFACT-RECOVERY-4` | Distinct digestとsource・build・artifact evidenceの結合へ継承 |
| `DAR-005` Publication and admission | `ARTIFACT-RECOVERY-5` | Registry・admission・observed deploymentのexact digest照合へ継承 |
| `DAR-006` Old digest inactive | `ARTIFACT-RECOVERY-6` | Replacement成功と独立したoriginal-scope再観測として継承 |
| `DAR-007` States and failure semantics | `ARTIFACT-RECOVERY-7` | Open・overdue・remediated・failure・errorの区別として継承 |

<a id="deployed-artifact-recovery-migration--旧実装の扱い"></a>
### 旧実装の扱い

| 旧成果物 | 判断 | 理由 |
|---|---|---|
| JSON policyとcase fixtures | 非移植 | Synthetic timestamp、digest、receiptはlive scope・rebuild・rolloutを証明しない |
| `scripts/verify.py` | 非移植 | Provider-neutral metadataの整合検査であり、builder・registry・admission・deploymentの実状態を読まない |
| Fixture mutation tests | 非移植 | Verifier contractのtestであり、observable security outcomeのtestではない |
| Negative scenarios | 観点として移行 | 診断・設計review・tabletopで利用し、実行済みとは扱わない |

GOV-005は複数platformのidentity chainとmutationを必要とし、SOURCE-002のscanner gateのように狭い一実装へ
収束しません。Artifact formatとplatformが選定され、安全な非本番targetがある場合にだけ実装を追加します。

<a id="deployed-artifact-recovery-migration--旧framework-mapping"></a>
### 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SSDF `1.1 / RV.1.1` | `DAR-001,002,007 / supports / high`、review `2026-08-12` | `ARTIFACT-RECOVERY-2 / supports / medium / design-reviewed`へ縮小。RV.1.1はsoftware・componentのpotential vulnerability情報収集とcredible report調査を支えるが、deployment inventoryとfailure stateは直接定義しない |
| NIST SSDF `1.1 / RV.2.1` | `DAR-003..006 / supports / high`、review `2026-08-12` | `ARTIFACT-RECOVERY-3 / supports / medium / design-reviewed`へ縮小。Risk情報を集めremediation等を計画するtaskであり、clean rebuild・publication・rollout・old digest removalは本PJの拡張 |
| OpenSSF OSPS `2026.02.19 / OSPS-DO-04.01` | `DAR-002,003 / related-to / medium`、review `2026-08-12` | 非継承。Releaseごとのsupport scope・durationをproject documentationへ記載する要件であり、本controlはその情報を入力として消費するだけ |
| MITRE ATT&CK `v19.1 / T1195.002` | `DAR-004..006 / mitigates / medium`、review `2026-08-12` | `ARTIFACT-RECOVERY-4,5,6 / mitigates / medium / design-reviewed`へ部分継承。Compromised artifactの残存を減らす設計関係 |

2026-09-24にSSDF公式本文、OSPS版付き本文、ATT&CK版付きSTIXを再照合しました。Framework mappingは
準拠、導入、完全なmitigationを意味しません。

<a id="deployed-artifact-recovery-migration--境界と残るgap"></a>
### 境界と残るgap

GOV-001はaffected artifactとdeploymentを特定し、GOV-005はそのscopeのrecovery closureを所有します。
DETECT-001はscanner acquisition・data・execution evidenceを所有し、REL-001はconsumerがartifactを受け入れる判断を所有します。
Provenance生成は後続の[BUILD-003移行](MIGRATION_BUILD.md#platform-provenance-migration)、registry publicationは[CONTAINER-002移行](MIGRATION_CONTAINER_CLOUD_IAC.md#container-registry-migration)、artifactの使用許可は[CONTAINER-001移行](MIGRATION_CONTAINER_CLOUD_IAC.md#deployment-artifact-admission-migration)で直接成果物を追加しました。
いずれもlive provider／deployment実装は未確認であり、GOV-005の存在で実装済みとは扱いません。
旧GOV-003のpriority・deadline責任は[別の移行](MIGRATION_GOVERNANCE_OPERATIONS.md#vulnerability-priority-migration)で再編集しました。

<a id="deployed-artifact-recovery-migration--2026-09-28の読み合わせ"></a>
### 2026-09-28の読み合わせ

GOV-003の元の優先度・対応期限を、GOV-005の置換計画へ明示的に渡しました。[教材](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/learning.md)では、新しいイメージを配布しても別環境と切り戻し経路に旧digestが残る場面から復旧完了を考えます。旧digestの一時使用をGOV-002で認めても、元の期限を消さず、`REMEDIATED`にも変えません。設計上の例外consumer関係は[マッピング](../mappings/exception-consumers.yaml)に記録しました。

NIST SSDF 1.1とSP 800-61 Rev.3の公開ページを再確認しました。例外と復旧完了を分ける具体的な条件は本PJの解釈であり、資料が特定の状態名やdigest検査を直接要求するとは主張しません。参照版と採否は[Sources](../sources/README.md#ref-deployed-artifact-recovery-001)が正本です。文書と診断項目で今回の範囲を完了し、追加の実装・テストコードは作りません。Live build、配布、稼働観測、例外利用停止は未確認です。

<a id="deployed-artifact-recovery-migration--2026-10-01の横断レビュー"></a>
### 2026-10-01の横断レビュー

稼働観測から復旧完了への受け渡しを再確認しました。検知アラート0件、rollout成功、desired stateの新digestは、元の範囲から旧digestが非稼働になった証拠の代わりにはなりません。元のtargetを保持し、置換先では実稼働digest、廃止先では実体の停止・削除と再起動経路を確認する判断へcontrolとpatternを揃えました。停止中のworkloadや切り戻し設定も、旧digestの再投入経路として確認します。これは[Sources](../sources/README.md#ref-deployed-artifact-recovery-001)に記録した本PJの解釈です。Liveのdeployment inventoryや復旧は未確認です。

<a id="vulnerability-priority-migration"></a>

<a id="vulnerability-priority-migration--product-vulnerability-priority移行記録"></a>
## Product vulnerability priority移行記録

旧`PSB-GOV-003`の8 checkを同じID範囲の`VULN-PRIORITY-1..8`へ再編集し、
[control](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)と
[pattern](../engineering/governance-operations/vulnerability-priority-decision/README.md)へ移しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`です。

旧Python verifier、synthetic KEV feed・schema・receipt、3-vector CVSS calculator、case fixturesは非移植です。
これらはcomposite metadata contractを検査しますが、live feedの完全性、任意CVSS vector、製品inventory、ticket delivery、
PSIRT運用を証明しません。問題のある操作や異常は、実行コードではなく確認項目として保持しました。

<a id="vulnerability-priority-migration--旧framework-mapping"></a>
### 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| NIST SSDF `1.1 / RV.1.1` | `VPR-001..004,008 / supports / high`、review `2026-08-05` | `VULN-PRIORITY-1,2,4,8 / supports / medium / design-reviewed`へ縮小。Potential vulnerability情報の収集・credible report調査との部分関係 |
| NIST SSDF `1.1 / RV.2.1` | `VPR-002,005..007 / supports / high`、review `2026-08-05` | `VULN-PRIORITY-5,6,7 / supports / medium / design-reviewed`へ縮小。Risk分析とremediation等の計画との部分関係 |

CVSS v4、CISA KEV、FIRST PSIRT Services Frameworkは仕様・data source・能力モデルとして参照記録へ残し、
controlへの準拠mappingにはしません。KEV非掲載は未悪用を意味せず、CVSSはbusiness riskやSLAではなく、
PSIRT frameworkの参照は組織能力の導入済み状態を証明しません。

<a id="vulnerability-priority-migration--2026-09-28の読み合わせ"></a>
### 2026-09-28の読み合わせ

GOV-001の影響調査から受け取る「影響候補・範囲付き非該当・調査不能」を、GOV-003の優先順位判断へ明示的につなぎました。[control配下の教材](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/learning.md)では、完成物を未調査の製品と、既知悪用情報の取得失敗を別の不足として扱います。調査不能を低優先度へ自動変換せず、再調査の担当者・期限と暫定判断を残します。

FIRSTのCVSS v4.0仕様、NIST SSDF 1.1の公開ページとCISA管理のKEV配布mirrorを確認しました。CISA本体のcatalogページは今回取得できず、現行catalogの内容・完全性やlive取得は確認していません。参照時点と本PJの解釈は[参照資料記録](../sources/README.md#ref-vulnerability-priority-001)を正本とします。

旧checkとframeworkの部分対応は維持し、文書と診断項目で今回の範囲を完了しました。新しい実装・テストコードは追加していません。採用先の優先度方針、feed、製品inventory、ケース配送と実対応は未確認です。
