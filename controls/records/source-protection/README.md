# Source Protection

ソースコード、リポジトリへ入るデータ、そこへアクセスするための権限を守る領域です。たとえば「端末にトークンをどう保管するか」「秘密情報を含むコミットをどう止めるか」「リポジトリを失ったらどう戻すか」から選べます。

開発端末の`.env`へ実際の認証情報を置かない話は[SOURCE-007](psb-source-007-developer-local-credential-storage/README.md)から読んでください。ソース管理サービス側の権限と失効はSOURCE-004です。Gitへ入れる内容は、認証情報ならSOURCE-002、顧客データなどならSOURCE-008で判断します。

| コントロール | 問うこと | できてはいけないこと | 教材 | 設計 |
|---|---|---|---|---|
| [PSB-SOURCE-001 Developer endpoint trust](psb-source-001-developer-endpoint-trust/README.md) | 端末の更新・監視が止まったら、利用先へのアクセスも見直せるか | 登録済みという理由だけで、状態不明の端末からのアクセスを続ける | [管理済みでも信用できるとは限らない](psb-source-001-developer-endpoint-trust/learning.md) | [Managed developer endpoint](../../../engineering/source-protection/managed-developer-endpoint/README.md) |
| [PSB-SOURCE-002 Secret publication boundary](psb-source-002-secret-publication-boundary/README.md) | 秘密情報を含むコミットやpushを、どこで見つけて止めるか | 検査できなかった変更を検査済みとして共有先へ送る | [ファイルから消した秘密情報がpushで届く](psb-source-002-secret-publication-boundary/learning.md) | [Secret checks before publication](../../../engineering/source-protection/secret-checks-before-publication/README.md) |
| [PSB-SOURCE-003 Public source exposure triage](psb-source-003-public-source-exposure-triage/README.md) | 公開コード・Issue・PRに自社の情報がないか調べ、見つけたら誰が確認するか | 検索漏れや通知失敗で、公開された情報を放置する | [自社ドメインが見つかった後に何を確認するか](psb-source-003-public-source-exposure-triage/learning.md) | [Public exposure observation and triage](../../../engineering/source-protection/public-exposure-observation-and-triage/README.md) |
| [PSB-SOURCE-004 Source credential lifecycle](psb-source-004-source-access-credential-lifecycle/README.md) | Git用のトークンや鍵で何ができるかを絞り、不要時に止められるか | 退職や端末紛失の後も古いトークン・セッションが使える | [盗まれた認証情報で何ができるか](psb-source-004-source-access-credential-lifecycle/learning.md) | [Source credential lifecycle](../../../engineering/source-protection/source-access-credential-lifecycle/README.md) |
| [PSB-SOURCE-005 Repository recovery independence](psb-source-005-repository-recovery-independence/README.md) | リポジトリを消されても、別に守ったコピーから開発を再開できるか | 元のリポジトリとバックアップを同じ権限で消せる | [ソースを戻した後も修正を続けられるか](psb-source-005-repository-recovery-independence/learning.md) | [Independent repository backup and restore](../../../engineering/source-protection/independent-repository-backup-and-restore/README.md) |
| [PSB-SOURCE-006 Source organization security posture](psb-source-006-source-organization-security-posture/README.md) | 組織の共通設定が、既存・新規・移管したリポジトリにも効いているか | 管理画面の設定だけを見て、適用漏れや不要な権限を見逃す | [共通設定を入れたのに一つだけ漏れる](psb-source-006-source-organization-security-posture/learning.md) | [Organization baseline and drift review](../../../engineering/source-protection/organization-baseline-and-drift-review/README.md) |
| [PSB-SOURCE-007 Developer credential storage](psb-source-007-developer-local-credential-storage/README.md) | 開発端末で使う実際の認証情報をどこに置き、どの処理へ渡すか | `.env`などの作業ファイルや広い受け渡しから、無関係な処理に値を使われる | [`.env`をGitに入れなければ十分か](psb-source-007-developer-local-credential-storage/learning.md) | [Developer credential storage and handoff](../../../engineering/source-protection/developer-credential-storage-and-handoff/README.md) |
| [PSB-SOURCE-008 Sensitive data repository admission](psb-source-008-sensitive-data-repository-admission/README.md) | 認証情報ではない機密データをGitに入れてよいか、どこで止めるか | secret scanで見つからない実データを、判断しないまま履歴へ入れる | [DBダンプをGitに入れてよいか](psb-source-008-sensitive-data-repository-admission/learning.md) | 対象データと書込み経路が決まるまではcontrolのガイダンスを使う |

教材は対応するcontrolのフォルダにあります。実装例がある場合は、表の設計から導入・確認手順へ進めます。

## 読み進め方

端末の状態から考えるならSOURCE-001、端末で使う認証情報の保管はSOURCE-007、その権限と失効はSOURCE-004です。複数のリポジトリへ共通方針を適用するならSOURCE-006、リポジトリを失った後の復旧はSOURCE-005から読んでください。

Gitへ内容を入れる前には、認証情報を[SOURCE-002](psb-source-002-secret-publication-boundary/README.md)、顧客データやDBダンプなどを[SOURCE-008](psb-source-008-sensitive-data-repository-admission/README.md)で判断します。拡張子やファイルサイズだけで「機密情報なし」とは言えません。両方とも手元の検査、共有先の受入、送信後の検査を区別しますが、探す内容と持込みを許す基準は異なります。

既に共有先へ届いたことが分かっているなら、公開検索を待ちません。認証情報は所有者から[GOV-004](../governance-operations/psb-gov-004-credential-exposure-containment/README.md)の封じ込めへ、顧客データなどはデータの所有者と組織の情報漏えい対応担当へ、到達した範囲を渡します。外部の公開コード・Issue・PRに未知の候補がないか探す場合は[SOURCE-003](psb-source-003-public-source-exposure-triage/README.md)です。検索結果が0件でも、既知の共有がなかった証明にはなりません。

移行済みの文書と実環境への導入は別です。８件ごとの[文書・講義・実装の進捗](../../../docs/MIGRATION_PLAN.md#source-protectionの進捗)、主題ごとの[未確認事項](../../../docs/MIGRATION_PLAN.md#現在地と次の作業)、前後の攻撃経路は[横断分析](../../../docs/ANALYSIS_LENSES.md)で確認できます。
