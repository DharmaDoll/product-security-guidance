# GitHub organizationの共通設定と適用漏れを確認する

GitHubの画面で共通設定を確認し、必要なrepository・人・Appへ届いているかを照合する手順です。画面と台帳を使い、設定の読返しと、使い捨てrepositoryでの簡単な確認から始められます。

対象はGitHub.comのorganizationです。2026-09-27の公式資料を参照しています。Enterprise Cloudの上位方針、契約、購入したsecurity機能で利用できる設定が異なります。GitHub Enterprise Server、GHE.com、IdP別の操作はこの例の対象外です。

## 始める前に決めること

Organizationの固定ID、確認する方針と対象repository、設定担当と確認担当を決めます。確認用IDには必要な一覧・設定の読取り範囲を選びます。読取りAPIを呼んでも、そのIDが設定変更の権限まで持たないこととは別なので、credentialのgrantも確認します。

2FA・SSOやgrantを変更する前に、影響する利用者、回復手段、変更前の値を確認します。これらの実施判断とIDの手順は[SOURCE-004のGitHub例](../../../source-access-credential-lifecycle/implementations/github/README.md)を使います。初回は画面を読むだけでも構いません。

## 最短の確認・適用手順

1. Organizationの管理画面で現在の対象一覧を確認し、製品・teamが必要とする台帳と照合します。画面のfilter、page、private／internal、archiveも確認します。
2. 次の表から自組織に必要な設定を選び、現在値、意図する値、対象、変更できる主体を記録します。
3. 設定変更が必要なら、影響と承認を確認し、選んだ設定だけを適用します。Security configurationは利用する機能のライセンス消費を画面で確認し、まず使い捨てrepositoryへ適用します。
4. 設定した画面を読み直し、対象repository側の値とconfiguration statusも確認します。進行中や失敗を適用済みとしません。
5. 下のsmoke testを行い、未対応と取得障害を担当へ残します。次のレビュー時点と、重要変更を早く拾う方法も決めます。

| GitHubの場所・対象 | 確認・変更すること | 読み返す際の注意 |
|---|---|---|
| People・Teams・repositoryのManage access | Owner、member、team、外部協力者のgrantを必要対象へ照合 | GitHubの一覧だけで在籍・用途を判断しない。記名した管理者と回復経路を維持する |
| Settings → Security → Authentication security | 選んだ2FA・SSO条件とIdP連携 | APIの2FA値だけでSSO・SCIM・session失効の確認を代替しない |
| Settings → Access → Member privileges | Base permissions、作成できるvisibility、private fork | 全memberへの一括付与が不要ならbaseを`None`にする。個別grant、internalのread可視性、既存private forkは別に確認 |
| Settings → Actions → General | 実行を許すrepository、Action／reusable workflow、SHA条件、token既定値、forkへの権限・secret送信 | Readの既定値だけでjobのwrite要求を止めたことにしない。Full-length SHAの組織条件もreusable workflowのtag参照まで拘束するものではない。直接参照は[CICD-001の具体例](../../../../cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)へ渡す |
| Settings → Third-party Access、Settings → Access → Member privileges | Installed GitHub App、OAuth App、Appの申請・インストール制限、許可範囲、責任者 | 新しい申請・インストールの制限と既存の承認・installationを分ける。OAuth Appアクセス制限を無効化後に再び有効化すると以前の承認が戻る仕様があるため、既存一覧と実効アクセスを再確認する |
| Settings → Personal access tokens | Fine-grained／classic PATのアクセス方針、有効期間、承認条件、現在のtoken | 最大有効期間に違反するmemberのtokenは組織アクセスをブロックされてもtoken自体は失効しない。既存の許可・停止を別に確認する |
| Settings → Security → Advanced Security → Configurations | 選んだ検査機能、適用するrepository、新規作成のdefault、enforcement | 既存対象にも適用する。移管したrepositoryには別に適用し、実statusを確認する。組織・enterprise双方の変更権限を見る |
| Settings → Archive → Logs → Audit log | 必要な変更カテゴリ、期間、検索条件、取得・保存・通知の担当 | イベントなしを全設定良好としない。API・export・streamの契約と保持・取得制限を確認する |

Security configurationの`attached`は適用された状態、`enforced`は制御する項目の変更を制限する状態です。`attaching`・`updating`は完了前、`failed`は適用失敗です。`removed`は個別設定等との衝突で全設定を継承しなくなった状態、`detached`はconfiguration管理がない状態です。画面名だけで結論を出さず、[現在のstatus仕様](https://docs.github.com/en/code-security/reference/security-at-scale/configuration-statuses)で原因と必要な処置を確認します。

## 必要ならread-only APIで一覧を補う

補助コマンドのCLIはGitHub CLI **2.95.0**のhelpと公式manualで構文を確認しました。REST API版は**2026-03-10**です。実organizationへのAPI実行は本PJでは未確認です。

承認されたcredentialをCLIの認証経路で利用します。Tokenを引数やURLへ埋め込みません。以下は明示したGETだけで、設定を変更しません。

```bash
SOURCE_POSTURE_ORG='your-organization'
gh api --method GET --hostname github.com \
  -H 'X-GitHub-Api-Version: 2026-03-10' \
  "/orgs/$SOURCE_POSTURE_ORG" \
  --jq '{id,node_id,two_factor_requirement_enabled,default_repository_permission}'
gh api --method GET --hostname github.com --paginate \
  -H 'X-GitHub-Api-Version: 2026-03-10' \
  "/orgs/$SOURCE_POSTURE_ORG/repos?type=all&per_page=100" \
  --jq '.[] | {id,node_id,visibility,archived}'
```

組織IDを期待する対象と照合し、返ったrepository IDを承認した台帳へ照合します。`--paginate`で取得しても、credentialから見えない対象は補えません。APIを匿名で呼ぶとpublicだけの成功結果にもなり得ます。Organizationの全詳細にはOwnerによる認証が必要なため、fieldの欠落・`null`を設定無効や良好へ変換せず、画面での確認または適切な取得経路へ戻します。

Member、team、App、security configuration、IdP、auditの一覧・実値はこの二つのGETで取得できません。APIを増やす場合はendpointごとに必要な読取り権限とpaginationを確認します。部分出力後の失敗、rate limit、空一覧、時点の変化を見落とさず、前回の結果を今回の成功としません。出力を保存する場合は組織の許可された場所を使い、本PJへ非公開IDを記録しません。

OAuth Appのアクセス制限やGitHub Appのインストール制限をPATの失効と同じ操作として扱わず、対象別に現在の許可と必要な停止方法を確認します。組織全体のApp方針をsmoke testのために切り替えず、必要な拒否確認は承認された使い捨て対象で計画します。

## 簡単なsmoke test

以下は、許可されたorganizationの使い捨てrepositoryだけで実施する確認手順です。本PJで実施済みの結果ではありません。実データや秘密情報は不要です。

| 確認 | 操作と期待する観測 |
|---|---|
| 適用成功 | テスト用repositoryへ必要なconfigurationを適用し、処理完了後のstatusとrepository側の実値を読む。新規defaultを選ぶ場合は新規作成でも確認する |
| 個別変更の拒否 | Enforcedにした項目を、設定を迂回できないrepository管理者の確認用IDで変更しようとする。操作の拒否と実値が変わらないことを確認する |
| 適用漏れ・上書き | Configurationを適用していない別のテスト用repositoryを一覧に含め、未適用として抽出できることを確認する。上書きの試験は未強制のテスト用configurationだけで行う |
| 移管経路 | 移管を利用する組織では、許可されたテスト用repositoryの移管後にconfigurationが別途必要か確認し、適用と再確認を行う。新規作成の結果を代用しない |
| 観測不足 | 読取り範囲を限定した確認用IDの結果を必要対象へ照合し、見えない対象を未確認として残す。取得できない設定を良好にしない |
| 対応完了 | 試験で見つけた未適用を修正し、担当者が再取得した実値で確認する。通知経路を採用する場合は、無害な試験通知と受領も別に確認する |

未契約・未対応でこの確認をできない機能は、利用できない理由と代替の確認方法を残します。試験用の設定一致から、別の全repository、workflow実効権限、検査精度、全IdP連携へ結果を広げません。

## 解除・失敗時の戻し方

この文書とGET例だけでは設定を加えません。練習で作ったrepository・configurationを一覧で特定し、影響先が練習対象だけと確認してから、適用前の値へ戻し、練習対象を廃棄します。個別configurationの解除と各機能の値の復元は別なので、解除後も実値を読みます。

本番方針を元へ戻す場合は項目ごとに影響を判断します。SSO障害をOwnerの恒久追加、workflow障害を全Action許可、App障害を全repositoryのwrite許可で解消する一律手順にはしません。例外が必要なら[例外の設計](../../../../governance-operations/security-exception-decision-boundary/README.md)へ渡します。

## 完了範囲

具体的な画面、対象の照合、GETによる補助、使い捨て対象での成功・拒否・未確認の手順を示しました。Live設定変更・拒否・適用、APIの全page取得、IdP、監査配送、通知、組織への導入は未確認です。手順の作成と実導入を分け、実結果は組織側の記録へ残します。

資料の確認日・採否・制約は[SPEC-GITHUB-ORGANIZATION-POSTURE](../../../../../sources/README.md#spec-github-organization-posture)、設計へ戻す境界は[pattern](../../README.md)からたどれます。
