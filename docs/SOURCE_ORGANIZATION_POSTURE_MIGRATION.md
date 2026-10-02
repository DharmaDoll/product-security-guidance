# Source organization security postureの移行判断

旧[PSB-SOURCE-006](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/control.yaml)の10項目を、共通方針、必要対象への実適用、grantの照合、状態の変化、確認障害と対応へ分けました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-27です。README、metadata、verifier、二つのrunbookがこの固定revisionと一致することも確認しました。

## 旧項目の行き先

| 旧項目 | 行き先・採否 |
|---|---|
| GHO-001 | [ORG-POSTURE-1・6](../controls/records/source-protection/psb-source-006-source-organization-security-posture/README.md)：固定組織、方針、必要対象、取得範囲、時点、障害。旧24時間とpolicy SHA-256を全組織の必須形式にしない |
| GHO-002 | ORG-POSTURE-2・4：組織の認証条件とIdP連携の現状。Credentialの発行・失効はSOURCE-004へ渡す。SAML／SCIM／EMUと24時間のoffboardingを一律に要求しない |
| GHO-003 | ORG-POSTURE-2・4：共通設定を変更する管理者の帰属、必要性、回復経路。Ownerを必ず2〜3名とする数値、90日のreviewを共通要件にしない |
| GHO-004 | ORG-POSTURE-4：member・team・外部協力者の実grantを所有者・用途へ照合。外部協力者を必ずpull／triageだけにする旧固定policyは採らない |
| GHO-005 | ORG-POSTURE-2〜3：初期権限、作成・公開・fork、既定値と実適用。Base None、全作成・全private fork禁止という組合せを唯一の正解にしない |
| GHO-006 | ORG-POSTURE-2〜3：組織のActions条件と対象ごとの適用。外部参照は続いて移行した[CICD-001](WORKFLOW_DEPENDENCY_MIGRATION.md)、workflow権限は[CICD-004](WORKFLOW_AUTHORITY_MIGRATION.md)へ渡す |
| GHO-007 | ORG-POSTURE-4：Appのowner・用途・対象・権限の現在値とreview。業務上必要なwriteやadministrationを全Appで一律に不合格にしない |
| GHO-008 | ORG-POSTURE-3：選んだsecurity機能の必要対象と実適用。検査機能の全一律有効化やSOURCE-003への合格を本controlの成功条件へ複製しない |
| GHO-009 | ORG-POSTURE-5〜7：現在状態とaudit、取得・保存・通知のhealth、担当者と再確認。180日保持、30日canary、zero sequence gap、全open driftゼロを普遍条件にしない |
| GHO-010 | ORG-POSTURE-6〜7：方針の承認、未確認と取得障害、秘密情報の持込防止、限定例外、再確認。旧policyの固定floorや例外の全禁止を移さない |

SOURCE-004はID・credential自体の必要範囲と失効、SOURCE-002は公開境界の検査、SOURCE-003は公開候補の観測・精査、SOURCE-005は破壊制限と復旧を扱います。新controlに残す問いは、それらの設定・grantが組織の必要対象へ届き、後の上書き・漏れ・確認障害を見つけられるかです。本文やテストを複製せず、担当成果物へリンクします。

## 具体化判断

必要な成果物はcontrol、control配下の教材、設計pattern、診断観点です。GitHubを使う場合の確認経路は明確なので、[GitHubの具体手順](../engineering/source-protection/organization-baseline-and-drift-review/implementations/github/README.md)も完成条件に含めました。現在の画面、項目の選択、最短の確認・適用、GETでの補助、使い捨て対象でのsmoke test、解除方法を記載します。

この手順の完成とlive導入を分けます。GitHub CLI 2.95.0のhelpとREST API 2026-03-10の公式仕様は確認しましたが、実organizationの設定変更、API収集、適用・拒否、IdP、監査配送、通知は実行していません。SaaSの設定を架空のテストで成功扱いにせず、実環境の確認は組織側に残します。

旧[verify.py](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/scripts/verify.py)はPython実装です。Normalized JSONの形、時刻、policy digest、固定floor、申告されたgrant・health・alert等を評価します。GitHub・IdPへ接続せず、設定や実際の通知を観測しません。Verifier、policy、snapshot、mutation fixtureは新実装例へコピーしません。Policyを2〜3OwnerやAppのwrite全禁止等へ縛る旧floorも、本PJのcontrolを定義する根拠にはしません。

旧[adoption runbook](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/docs/github-adoption-runbook.md)は画面・GET・変更影響を判断する価値を選別し、固定のMinimum値と不要なendpoint一覧を外しました。旧[automation options](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/docs/governance-automation-options.md)は、手動、read-only現在状態、auditとの組合せ、第三者Appの選択肢をpatternへ移します。自動収集が必要になる条件と代償を残し、collectorやAllstarを実装済みにはしません。

Collectorの具体化は、必要対象、GitHubの契約とendpoint、IdP、読取り権限、保存先、通知先、取得期限が決まった時に再開します。完了条件は、実取得の必要範囲、pagination・permission denial・rate limit・部分失敗、適用差、通知受領、修正後の実値を観測し、未対応項目を示すことです。Synthetic JSONを増やすことを代替にしません。

実装手順からcontrol・patternへ戻した境界は、新規defaultと移管の違い、configurationの存在と実status、既定tokenとworkflow権限、全page取得とcredentialの可視範囲、2FA fieldとIdP・SSOの違いです。2026-09-30の読み合わせでは、Appの新規申請・インストール制限と既存installation、OAuth制限の再有効化と以前の承認、PAT方針によるブロックとtoken自体の失効も分けました。SOURCE-006は組織側の現在値と方針差を見つけ、不要な認可の失効・拒否確認はSOURCE-004へ渡します。直接資料の確認日・採否は[Sources](../sources/README.md#spec-github-organization-posture)に残します。

## 旧framework関係と旧資料ID

旧レビュー日は2026-08-26です。次の11関係は移行履歴として保持します。今回、固定版のexact項目へ新propertyを割り当て直していないため、新しいframework mappingへ継承しません。特に旧`verifies / high`を実organizationの確認結果として使いません。Framework mappingは116件のままです。

| 旧framework・版 | IDと旧関係 | 旧適用項目 |
|---|---|---|
| GitHub guidance `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24） | GH-ADMIN-AUDIT-EVENTS：verifies / high | GHO-001・009・010 |
| 同上 | GH-ADMIN-SAML-IAM：supports / high | GHO-002・003 |
| 同上 | GH-ADMIN-SCIM-ORGANIZATIONS：supports / high | GHO-002・004 |
| 同上 | GHSC-SECURE-ACCOUNTS：supports / high | GHO-002・003・004 |
| 同上 | GH-ADMIN-ACTIONS-ORGANIZATION：verifies / high | GHO-006 |
| 同上 | GH-ADMIN-CREDENTIAL-TYPES：supports / medium | GHO-007 |
| 同上 | GHSC-SECURE-CODE：supports / medium | GHO-005・008 |
| OpenSSF OSPS `2026.02.19` | OSPS-AC-02.01：supports / high | GHO-003・004・007 |
| 同上 | OSPS-AC-04.01：supports / medium | GHO-006 |
| MITRE ATT&CK `v19.1` | T1078：mitigates / medium | GHO-002・003・004 |
| 同上 | T1098：mitigates / medium | GHO-003・004・007 |

SOURCE-004で確認済みの固定GitHub guidanceは、ORG-POSTURE-4の隣接するID判断へ参照します。それでも旧関係全体を再照合したことにはしません。旧`REF-CICD-015`（DS-202）、`REF-CICD-017`（Flatt Security）、`REF-CICD-018`（Allstar）は調査入力の履歴としてここに保持し、今回未再参照の資料を新propertyの直接根拠に追加しません。新しいIDの別名としても残しません。
