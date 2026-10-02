# Source Protection

ソースコードそのものだけでなく、ソースコードを読み、変更し、リリースやワークフローへ影響できる権限を守ります。

| コントロール | 問うこと | できてはいけないこと | 教材 | 設計 |
|---|---|---|---|---|
| [PSB-SOURCE-001 Developer endpoint trust](psb-source-001-developer-endpoint-trust/README.md) | 現在の端末状態を業務アクセスの判断へ結び付けられるか | 状態不明・基準違反・紛失を良好扱いし、定めた期限後もアクセスを残す | [管理済みでも信用できるとは限らない](psb-source-001-developer-endpoint-trust/learning.md) | [Managed developer endpoint](../../../engineering/source-protection/managed-developer-endpoint/README.md) |
| [PSB-SOURCE-002 Secret publication boundary](psb-source-002-secret-publication-boundary/README.md) | 秘密情報をどの公開経路で検査・拒否するか | 検査省略や履歴の欠落を検出なしとして共有先へ進める | [ファイルから消した秘密情報がpushで届く](psb-source-002-secret-publication-boundary/learning.md) | [Secret checks before publication](../../../engineering/source-protection/secret-checks-before-publication/README.md) |
| [PSB-SOURCE-003 Public source exposure triage](psb-source-003-public-source-exposure-triage/README.md) | 公開ソースの候補と観測できなかった状態を区別し、所有者の判断へ渡せるか | 収集漏れ、古い判断、重複抑制、通知失敗で公開候補が未対応のまま残る | [自社ドメインが見つかった後に何を確認するか](psb-source-003-public-source-exposure-triage/learning.md) | [Public exposure observation and triage](../../../engineering/source-protection/public-exposure-observation-and-triage/README.md) |
| [PSB-SOURCE-004 Source credential lifecycle](psb-source-004-source-access-credential-lifecycle/README.md) | 誰が、何の目的で、どのリポジトリへ、どの操作を、いつまで行えるかを把握し、不要時に失効できるか | 盗難、異動、退職、用途終了後も、認証情報またはセッションを利用できる状態が残る | [盗まれた認証情報で何ができるか](psb-source-004-source-access-credential-lifecycle/learning.md) | [Source credential lifecycle](../../../engineering/source-protection/source-access-credential-lifecycle/README.md) |
| [PSB-SOURCE-005 Repository recovery independence](psb-source-005-repository-recovery-independence/README.md) | ソースを失っても独立した保管世代から開発を再開できるか | 同じ権限でbackupも消せる、または不完全・不正変更後の世代を復旧へ採用する | [ソースを戻した後も修正を続けられるか](psb-source-005-repository-recovery-independence/learning.md) | [Independent repository backup and restore](../../../engineering/source-protection/independent-repository-backup-and-restore/README.md) |
| [PSB-SOURCE-006 Source organization security posture](psb-source-006-source-organization-security-posture/README.md) | 共通方針が必要対象へ届き、後の設定変更や確認漏れを追えるか | 既定値や部分取得だけで全対象を良好と扱い、未適用や不要な権限を残す | [共通設定を入れたのに一つだけ漏れる](psb-source-006-source-organization-security-posture/learning.md) | [Organization baseline and drift review](../../../engineering/source-protection/organization-baseline-and-drift-review/README.md) |

教材は対応するcontrolのフォルダにあります。実装例がある場合は、表の設計から導入・確認手順へ進めます。

## 読み進め方

端末の状態から権限を見直すならSOURCE-001→004→006、秘密情報の混入と公開面の発見ならSOURCE-002→003の順に読むと、別の判断へ渡す箇所が分かります。実際の認証情報が共有先へ届いたと分かっている場合は、公開検索を待たずに[GOV-004](../governance-operations/psb-gov-004-credential-exposure-containment/README.md)の封じ込めへ進みます。ソースを失った場合はSOURCE-005から、戻す世代と開発再開の条件を確認します。

移行済みの文書と実環境への導入は別です。各主題の確認範囲は[移行計画](../../../docs/MIGRATION_PLAN.md#現在地と次の作業)、前後の攻撃経路は[横断分析](../../../docs/ANALYSIS_LENSES.md)で確認できます。
