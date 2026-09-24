# Credential exposure containment移行記録

## 結論

旧`PSB-GOV-004`から、credential漏えい後のauthority封じ込め、限定したreplacement、consumer照合、旧authority拒否、
影響調査へのhandoff、closure条件をcontrolとpatternへ移しました。旧provider-neutral JSON fixtureとPython verifierは移植しません。

新成果物:

- [PSB-GOV-004 Credential exposure containment](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)
- [ENG-GOV-003 Credential exposure containment and recovery](../engineering/governance-operations/credential-exposure-containment/README.md)

移行元は旧repository commit `f42987759218c9b8daf3924320542a1935ef78e0`の
`controls/governance-operations/credential-exposure-containment/`です。旧IDと10 checkを履歴として保持し、
新しい7特性へ役割を統合しました。これは実環境への導入やincident対応の完了を意味しません。

## Checkの対応

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

## 旧実装の扱い

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

## 旧framework mapping

| Framework | 旧関係 | 新判断 |
|---|---|---|
| MITRE ATT&CK `v19.1 / T1078 Valid Accounts` | `CRR-004..007 / mitigates / medium`、review `2026-08-10` | `CRED-CONTAIN-3,4,5 / mitigates / medium / design-reviewed`へ部分継承。旧正規credentialと派生authorityの継続利用を制限する関係 |
| NIST SSDF `1.1 / RV.2.1` | `CRR-001,003..009 / supports / high`、review `2026-08-10` | 非継承。RV.2.1はsoftware vulnerabilityのriskを分析してremediation等を計画するtaskであり、credential authorityの失効・session・consumer移行を直接定義しない |
| OpenSSF OSPS `2026.02.19 / OSPS-AC-04.01` | `CRR-005,006 / supports / medium`、review `2026-08-10` | 非継承。AC-04.01はCI/CD taskでpermission未指定時のdefaultをpipeline内の最低権限にする要件であり、incident replacementのscope比較ではない |

ATT&CKの版付きSTIX、SSDF公式本文、OSPS版付き本文を2026-09-24に再照合しました。Mappingは設計上の関係であり、
技術の完全なmitigation、framework準拠、実運用を示しません。

## 参照資料の採否

NIST SP 800-61 Rev.3はincident responseをrisk managementへ統合し、Detect・Respond・Recoverと継続改善を扱う
上位の運用ガイダンスとして部分採用します。Credential classごとの失効、replacement比較、拒否probeは同文書の
具体要件ではなく、旧controlを再評価した本リポジトリの設計判断です。

製品固有のcredential revocation、session invalidation、signing trust、audit APIを参照資料へ追加するのは、
実装対象providerを選定した時点です。変更可能な最新文書を集めて、汎用controlの導入済み証拠にはしません。
