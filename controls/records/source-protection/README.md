# Source Protection

ソースコードそのものだけでなく、ソースコードを読み、変更し、リリースやワークフローへ影響できる権限を守ります。

| コントロール | 問うこと | できてはいけないこと |
|---|---|---|
| [PSB-SOURCE-001 Developer endpoint trust](psb-source-001-developer-endpoint-trust/README.md) | 現在の端末状態を業務アクセスの判断へ結び付けられるか | 状態不明・基準違反・紛失を良好扱いし、定めた期限後もアクセスを残す |
| [PSB-SOURCE-002 Secret publication boundary](psb-source-002-secret-publication-boundary/README.md) | 秘密情報をどの公開経路で検査・拒否するか | 検査省略や履歴の欠落を検出なしとして共有先へ進める |
| [PSB-SOURCE-003 Public source exposure triage](psb-source-003-public-source-exposure-triage/README.md) | 外部から発見できる公開source候補と観測できなかった状態を区別し、所有者の判断へ渡せるか | Collection gap、staleな判断、重複抑制、通知失敗によって公開候補を未対応のまま残す |
| [PSB-SOURCE-004 Source credential lifecycle](psb-source-004-source-access-credential-lifecycle/README.md) | 誰が、何の目的で、どのリポジトリへ、どの操作を、いつまで行えるかを把握し、不要時に失効できるか | 盗難、異動、退職、用途終了後も、認証情報またはセッションを利用できる状態が残る |

## 読み進め方

Git hooksによる検査と共有先の独立した受入判断は[Secret checks before publication](../../../engineering/source-protection/secret-checks-before-publication/README.md)で検討します。
共有後または管理外の公開面に現れた候補は[Public exposure observation and triage](../../../engineering/source-protection/public-exposure-observation-and-triage/README.md)で、coverage、再出現、responseへの引渡しを検討します。

端末そのものの保護は[Managed developer endpoint](../../../engineering/source-protection/managed-developer-endpoint/README.md)から確認できます。
SOURCE-001のcontrol記録と設計は端末管理の範囲で移行済みです。製品実装・実環境診断は未実施です。[29項目の対応表](../../../docs/ENDPOINT_MIGRATION.md)に隣接領域と保留事項を残しています。

1. コントロール記録で保証の境界を確認する。
2. [学習ノート](psb-source-004-source-access-credential-lifecycle/learning.md)で、認証情報の窃取がソース管理上の権限へ変わる流れを追う。
3. [Source credential lifecycle pattern](../../../engineering/source-protection/source-access-credential-lifecycle/README.md)で、IDの選択とライフサイクルを設計する。
4. GitHubを利用する場合に限り、[GitHub実装例](../../../engineering/source-protection/source-access-credential-lifecycle/implementations/github/README.md)を読む。
5. [横断分析の軸](../../../docs/ANALYSIS_LENSES.md)で、端末、AIツール、ソース管理、CI/CDのIDへ続く経路を確認する。
