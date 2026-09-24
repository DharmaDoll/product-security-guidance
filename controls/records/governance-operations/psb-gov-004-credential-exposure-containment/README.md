# PSB-GOV-004: Credential exposure containment

設計する：[Credential exposure containment and recovery](../../../../engineering/governance-operations/credential-exposure-containment/README.md)

## 問い

Credentialの漏えいが疑われた後、旧authorityと派生sessionを封じ込め、既知consumerを必要最小限のreplacementへ移行し、
侵害時間帯の操作を調査して、残存authorityがないことを確認するまでincidentを閉じない状態にできるか。

## できてはいけないこと

新しいcredentialによる疎通だけをrotation完了の証拠にして、旧credential、派生session、忘れられたconsumer、
signing trust、侵害時間帯に作られたartifactやdeploymentを残してはいけません。Inventory、provider response、
拒否確認、audit、通知の欠落を、封じ込め済みまたは影響なしへ変換してもいけません。

## 起点となるシナリオ

Package公開tokenがpublic repositoryへ入ったため、担当者は新しいtokenを発行して主要workflowを更新しました。
しかし旧tokenは失効しておらず、緊急公開用consumerにも残っています。攻撃者は発見から失効までの間にreleaseを作成していました。
新tokenの成功だけを確認してincidentを閉じると、旧authorityと公開済みartifactの両方が残ります。

本controlは漏えい疑いが生じた後の封じ込めと復旧判断を扱います。通常時のcredential発行・棚卸し・失効条件は
[SOURCE-004](../../source-protection/psb-source-004-source-access-credential-lifecycle/README.md)、公開前の拒否は
[SOURCE-002](../../source-protection/psb-source-002-secret-publication-boundary/README.md)、公開面での発見とtriageは
[SOURCE-003](../../source-protection/psb-source-003-public-source-exposure-triage/README.md)の責任です。

## 適用範囲

Source access、CI、package publication、artifact registry、cloud deployment、SSH、signingに使うhuman・workload credentialと、
そのcredentialから生じたsession、grant、certificate、trust、consumer、resourceへ適用します。漏えいが未確定でも、
合理的な疑いから安全側の封じ込めを開始する場面を含みます。

次は直接の対象ではありません。

- Credentialを検出するscanner、公開面のcollector、通常時のcredential lifecycleを実装すること。
- Incident全体の法務、広報、通知、forensics、危機管理能力を定義すること。
- 影響artifact・release・deploymentの最終判断や、削除・rollback・rebuildを実行すること。
- すべてのcredential種別へ一つのrevoke APIや固定した対応順序を適用すること。
- 実credential値をfixture、ticket、log、検証出力へ保存すること。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `CRED-CONTAIN-1` | 漏えい対象をsecret値ではなく安定した識別子、class、owner、scope、resource、consumer、派生authority、推定exposure windowへ結び付ける |
| `CRED-CONTAIN-2` | 利用可能な証拠を保全し、封じ込めの対象・担当・承認・可用性影響を記録する。切迫した被害を止める操作は、証拠保全の完了を無期限に待たず、緊急判断と失う証拠を記録する |
| `CRED-CONTAIN-3` | Credential classに応じて旧authority、派生session、発行条件またはtrustを封じ込め、短命credentialの自然失効だけを修復完了にしない |
| `CRED-CONTAIN-4` | Replacementを旧authority以下のpurpose、scope、resource、consumer、有効期間に限定し、既知consumerをmigrated・removed・quarantined・期限付きnot-applicableのいずれかへ照合する |
| `CRED-CONTAIN-5` | Replacementの成功とは独立に、旧authorityと対象となる派生authorityが拒否されることを、値を拡散しない安全な方法で確認する |
| `CRED-CONTAIN-6` | Exposure windowの操作を調べ、source変更、workflow、package、image、signature、attestation、release、artifact、deploymentのexact identityと未観測範囲を影響調査へ渡す |
| `CRED-CONTAIN-7` | 封じ込め、consumer disposition、旧authority拒否、影響調査の状態を分け、欠落・stale・partial・取得不能・配送失敗を成功へ変換せず、secret-freeな証拠でclosureを判断する |

## 実装判断の羅針盤

最初にcredential値を集めるのではなく、provider上のidentifier、owner、権限、consumer、resource、発行元とsessionの関係を確定します。
完全なinventoryを待つ間にも被害が進む場合は、観測済みのauthorityを先に止め、未知consumerと未観測範囲を未解決として残します。

`rotation`は旧credentialの拒否、派生authorityの処理、consumer移行、影響調査を含む状態遷移です。
Replacementが動くことと旧authorityが使えないことは別の証拠にします。拒否確認は、providerの失効状態・session一覧・
introspection・無害な操作などから、credential classに適した方法を選びます。漏えい値を新たなautomationへ渡す確認を必須にしません。

Auditが空でも、collectorの対象・権限・retention・時刻・paginationを説明できなければ「悪用なし」と判断できません。
影響候補のexact identityと調査不能範囲を[PSB-GOV-001](../psb-gov-001-supply-chain-impact-assessment/README.md)へ渡し、
artifact削除やdeployment変更は独立した承認を経ます。

## Credential classごとの確認点

| Class | 封じ込めで確認する対象 |
|---|---|
| Reusable bearer token / API key | Tokenの失効、関連grant・session、全consumer、利用履歴 |
| SSH key / certificate | 登録keyまたはcertificate、CA・revocation、既存session、利用先host |
| Signing key / signer identity | Sign操作の停止、trustとrevocationの伝播、exposure windowのsignatureとartifact |
| Short-lived workload credential | 新規発行の停止、issuer trust・subject・audience・policyの修復、発行済みsessionと利用履歴 |
| Cloud access key / federated session | Key・role trust・session、権限変更、対象resourceと操作履歴 |

Providerによって失効単位、伝播時間、session無効化、audit retentionが異なります。この表はAPI手順ではなく、
「保存値の交換」だけで終えないための確認範囲です。

## Negative testの観点

次は脆弱性診断、tabletop exercise、設計レビューで列挙する観点です。テストコードの実行済み状態を意味しません。

- 主要consumerだけを更新し、緊急用workflow、developer machine、mirror、publisherに旧credentialが残る。
- Credential本体を失効しても、既存session、delegated grant、SSH session、signer trustが残る。
- Short-lived tokenの満了を待つだけで、漏えいしたissuer trustや発行条件を修復しない。
- Replacementがwildcard scope、追加resource、追加consumer、長い有効期間を持つ。
- Consumer一覧に欠落・重複・owner不明があるのに、移行完了と判定する。
- 旧authorityの拒否確認がskipped・unsupported・unavailableでも成功にする、または新credentialの成功で代用する。
- Auditが空、retention外、pagination不明、取得権限不足でも悪用なしと判定する。
- Evidence保全前にhistory rewrite、artifact削除、log消去を行う。緊急操作の理由と失った証拠も記録しない。
- Incident ticket、provider receipt、fixture、通知へcredential値やprivate key materialを複製する。
- Synthetic fixtureの`PASS`をlive providerでの失効、session拒否、consumer移行の証拠にする。
- 影響調査や通知が未完了・失敗した状態でincidentを`CLOSED`にする。

## 判定例

| 観測した状態 | このcontrolでの判断 |
|---|---|
| 新tokenでpublishできるが、旧tokenの状態と他consumerを確認していない | 不合格候補。Service復旧だけが確認済み |
| 旧tokenを直ちに失効し、証拠不足と未知consumerをopen itemとして記録した | 緊急封じ込めは成立し得る。Incident closureはまだ判断できない |
| Provider上で失効を確認し、既存sessionにも無害な操作が拒否された | `CRED-CONTAIN-5`の証拠になり得る。未観測sessionや伝播時間は別に記録する |
| Audit 0件だが、retentionよりexposure windowが古い | 影響なしを裏付けない。調査不能範囲として渡す |
| Signing keyを交換したが、旧keyへのtrustと発行済みartifactを調べていない | 不合格候補。Credential classに必要な封じ込めと影響調査が不足 |

## 保証しない範囲

本controlはprovider APIの完全性、全consumerの発見、すべての派生sessionの強制失効、過去操作の完全なaudit、
または組織のincident response能力全体を保証しません。Design guidanceとdiagnostic viewpointsはlive response evidenceではありません。

## 関連資料

- [Credential exposure containment and recovery](../../../../engineering/governance-operations/credential-exposure-containment/README.md)
- [Supply-chain impact assessment](../psb-gov-001-supply-chain-impact-assessment/README.md)
- [Source credential lifecycle](../../source-protection/psb-source-004-source-access-credential-lifecycle/README.md)
- [旧成果物との対応](../../../../docs/CREDENTIAL_EXPOSURE_MIGRATION.md)
- [参照資料と採否](../../../../sources/README.md#ref-credential-exposure-containment-001)
- [横断分析](../../../../docs/ANALYSIS_LENSES.md)

## Framework mapping

Enterprise ATT&CK v19.1の`T1078 Valid Accounts`を、`CRED-CONTAIN-3,4,5 / mitigates / medium / design-reviewed`として
部分的に対応させます。漏えいした正規credentialと派生authorityの継続利用を制限する関係であり、すべてのvalid account利用を
検知・排除したことを意味しません。旧SSDF `RV.2.1`とOSPS `OSPS-AC-04.01`は対象成果が異なるため非継承です。
詳細は[移行記録](../../../../docs/CREDENTIAL_EXPOSURE_MIGRATION.md#旧framework-mapping)に保持します。
