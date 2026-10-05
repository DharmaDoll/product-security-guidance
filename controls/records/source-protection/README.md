# Source Protection

ソースコードと、そこへアクセスするための権限を守る領域です。たとえば「端末にトークンをどう保管するか」「秘密情報を含むコミットをどう止めるか」「リポジトリを失ったらどう戻すか」から選べます。

開発端末の`.env`へ実際の認証情報を置かない話は[SOURCE-007](psb-source-007-developer-local-credential-storage/README.md)から読んでください。ソース管理サービス側の権限と失効はSOURCE-004、コミット・push時の検査はSOURCE-002です。

| コントロール | 問うこと | できてはいけないこと | 教材 | 設計 |
|---|---|---|---|---|
| [PSB-SOURCE-001 Developer endpoint trust](psb-source-001-developer-endpoint-trust/README.md) | 端末の更新・監視が止まったら、利用先へのアクセスも見直せるか | 登録済みという理由だけで、状態不明の端末からのアクセスを続ける | [管理済みでも信用できるとは限らない](psb-source-001-developer-endpoint-trust/learning.md) | [Managed developer endpoint](../../../engineering/source-protection/managed-developer-endpoint/README.md) |
| [PSB-SOURCE-002 Secret publication boundary](psb-source-002-secret-publication-boundary/README.md) | 秘密情報を含むコミットやpushを、どこで見つけて止めるか | 検査できなかった変更を検査済みとして共有先へ送る | [ファイルから消した秘密情報がpushで届く](psb-source-002-secret-publication-boundary/learning.md) | [Secret checks before publication](../../../engineering/source-protection/secret-checks-before-publication/README.md) |
| [PSB-SOURCE-003 Public source exposure triage](psb-source-003-public-source-exposure-triage/README.md) | 公開コード・Issue・PRに自社の情報がないか調べ、見つけたら誰が確認するか | 検索漏れや通知失敗で、公開された情報を放置する | [自社ドメインが見つかった後に何を確認するか](psb-source-003-public-source-exposure-triage/learning.md) | [Public exposure observation and triage](../../../engineering/source-protection/public-exposure-observation-and-triage/README.md) |
| [PSB-SOURCE-004 Source credential lifecycle](psb-source-004-source-access-credential-lifecycle/README.md) | Git用のトークンや鍵で何ができるかを絞り、不要時に止められるか | 退職や端末紛失の後も古いトークン・セッションが使える | [盗まれた認証情報で何ができるか](psb-source-004-source-access-credential-lifecycle/learning.md) | [Source credential lifecycle](../../../engineering/source-protection/source-access-credential-lifecycle/README.md) |
| [PSB-SOURCE-005 Repository recovery independence](psb-source-005-repository-recovery-independence/README.md) | リポジトリを消されても、別に守ったコピーから開発を再開できるか | 元のリポジトリとバックアップを同じ権限で消せる | [ソースを戻した後も修正を続けられるか](psb-source-005-repository-recovery-independence/learning.md) | [Independent repository backup and restore](../../../engineering/source-protection/independent-repository-backup-and-restore/README.md) |
| [PSB-SOURCE-006 Source organization security posture](psb-source-006-source-organization-security-posture/README.md) | 組織の共通設定が、既存・新規・移管したリポジトリにも効いているか | 管理画面の設定だけを見て、適用漏れや不要な権限を見逃す | [共通設定を入れたのに一つだけ漏れる](psb-source-006-source-organization-security-posture/learning.md) | [Organization baseline and drift review](../../../engineering/source-protection/organization-baseline-and-drift-review/README.md) |
| [PSB-SOURCE-007 Developer credential storage](psb-source-007-developer-local-credential-storage/README.md) | 開発端末で使う実際の認証情報をどこに置き、どの処理へ渡すか | `.env`などの作業ファイルや広い受け渡しから、無関係な処理に値を使われる | [`.env`をGitに入れなければ十分か](psb-source-007-developer-local-credential-storage/learning.md) | [Developer credential storage and handoff](../../../engineering/source-protection/developer-credential-storage-and-handoff/README.md) |

教材は対応するcontrolのフォルダにあります。実装例がある場合は、表の設計から導入・確認手順へ進めます。

## 読み進め方

端末の状態はSOURCE-001、端末に置く認証情報はSOURCE-007、ソース管理で使える権限と失効はSOURCE-004を読んでください。秘密情報を含むコミットの防止はSOURCE-002、公開済みの候補を探すならSOURCE-003です。実際の認証情報が共有先へ届いたと分かっている場合は、公開検索を待たずに[GOV-004](../governance-operations/psb-gov-004-credential-exposure-containment/README.md)の封じ込めへ進みます。ソースを失った場合はSOURCE-005から、戻す世代と開発再開の条件を確認します。

顧客データやDBダンプなど、認証情報ではない機密データをGitへ入れない判断は、SOURCE-002のsecret scanだけでは完結しません。[旧DEH-010の保留理由](../../../docs/MIGRATION_SOURCE_PROTECTION.md#endpoint-migration--29項目の配置)を確認し、守るデータの範囲と公開経路を決めてから別の主題が必要か判断します。拡張子やファイルサイズだけで「機密情報なし」とは判定できません。

移行済みの文書と実環境への導入は別です。各主題の確認範囲は[移行計画](../../../docs/MIGRATION_PLAN.md#現在地と次の作業)、前後の攻撃経路は[横断分析](../../../docs/ANALYSIS_LENSES.md)で確認できます。
