# 共通設定を入れたのに、なぜ一つだけ漏れたのか

対象controlは[SOURCE-006 Source organization security posture](README.md)です。組織で一度設定すれば全repositoryが同じ状態になる、という思い込みから考えます。

## 方針はあるが、対象に届いていない

あるチームは、GitHubの検査機能の設定をまとめたsecurity configurationを用意し、新規repositoryへ適用する既定値にしました。後日、別組織から製品repositoryを移管します。担当者は「組織の既定値があるから検査も有効」と判断しました。

しかしGitHubの確認時の仕様では、新規作成用の既定configurationは移管したrepositoryへ自動適用されません。移管先で必要なconfigurationを別に適用します。方針を持つこと、設定を適用する操作が成功すること、対象ごとの状態を確認することは別です。[製品仕様と確認日](../../../../sources/README.md#spec-github-organization-posture)を参照してください。

この失敗は、対象一覧を持つORG-POSTURE-1と、適用状態を見るORG-POSTURE-3を結び付けると見つけられます。新規・既存・移管・archiveからの再開について、適用する対象を先に決めておく必要があります。

## 似ている言葉を分ける

| 言葉 | 判断すること |
|---|---|
| 方針（baseline） | この組織の何を、どの状態にしたいか。項目ごとの担当と適用条件を決める |
| 既定値（default） | 指定がないときに選ばれる値。個別に変更できるなら権限の上限ではない |
| 強制（enforcement） | 誰の、どの変更が拒否されるか。設定されていない項目まで強制されるとは限らない |
| 適用範囲（coverage） | 必要な対象のうち、現在どれに何が効いているか。画面に表示された一pageだけを母集団にしない |
| 方針からのずれ（drift） | 意図した方針と現在の実値の差。前回も誤設定なら、前回との差だけでは見つからない |
| 変更記録（audit event） | 誰がいつ何を変えたかの調査入力。現在の全対象や全設定を表す台帳ではない |
| 付与済みの権限（grant） | 現在、誰がどの対象へ何をできるか。在籍や用途と照合して、残す必要があるかを決める |
| ログイン基盤（IdP） | 本人の認証や所属を管理する別のシステム。その状態とGitHub側の権限が一致しているか確認する |

例えば、GitHubの組織設定で`GITHUB_TOKEN`の既定値を読取り専用にしても、workflowの`permissions`で権限を変更できる経路があります。「readという文字が見えた」だけでは、実行されるjobがwriteを持たないとは言えません。

また、base permissionを`None`にしても、個別grant、外部協力者、internal repositoryの可視性をまとめて消す設定ではありません。ORG-POSTURE-2の共通方針とORG-POSTURE-4のgrant照合を分け、詳細な権限判断を[SOURCE-004](../psb-source-004-source-access-credential-lifecycle/learning.md)やCIの担当へ渡します。

Appやtokenの方針も、設定の表示だけでは既存のアクセスを説明できません。例えばGitHubでAppのインストールをownerだけに制限する設定は、今後repository管理者がインストール・対象追加する経路を制限します。既にあるinstallationの対象と権限は別に読みます。OAuth Appの組織アクセス制限を一度無効にして再び有効にした場合、以前に承認されたAppが自動的に組織へアクセスを許される仕様もあります。方針の変更後は、既存の承認・grantと実際の拒否を確認し、不要な認可の処置をSOURCE-004へ渡します。[GitHubの仕様](../../../../sources/README.md#spec-github-organization-posture)を参照してください。

## 見つからなかった理由も残す

監視用IDのアクセス範囲が狭く、対象repositoryの一部を取得できなかったとします。取得した全pageで設定違反がゼロでも、組織全体を確認したことにはなりません。必要な対象と取得できた対象を照合し、見えなかった部分を未確認として扱います。

APIが止まったときも、昨日の良好な記録は昨日の記録です。ORG-POSTURE-6は「設定の違反を見つけた」「確認ができなかった」「理由を確認して対象外にした」を区別します。確認不能ならどの判断が止まるかを決め、全員の業務アクセスを必ず停止するという一律の扱いにはしません。

変更イベントが途切れても、定期的な現在状態の取得は適用漏れを見つける手掛かりになります。一方で現在の設定だけでは、変更した主体や途中の経路を調べきれません。ORG-POSTURE-5で二つを組み合わせます。

## 読者が次に決めること

1. 自組織で共通にしたい項目、対象、許される個別変更、確認期限を選ぶ。
2. 手作業でも全対象を追えるか、API等による補助が必要かを判断する。
3. 適用失敗・方針との差・取得障害を誰へ渡し、何を再確認したら閉じるかを決める。

[設計パターン](../../../../engineering/source-protection/organization-baseline-and-drift-review/README.md)はこの選択に使います。[GitHub手順](../../../../engineering/source-protection/organization-baseline-and-drift-review/implementations/github/README.md)のsmoke testは使い捨てrepositoryでの確認方法であり、本PJで実施した組織診断ではありません。
