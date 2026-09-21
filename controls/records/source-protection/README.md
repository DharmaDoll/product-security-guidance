# Source Protection

ソースコードそのものだけでなく、ソースコードを読み、変更し、リリースやワークフローへ影響できる権限を守ります。

| コントロール | 問うこと | できてはいけないこと |
|---|---|---|
| [PSB-SOURCE-004 Source credential lifecycle](psb-source-004-source-access-credential-lifecycle/README.md) | 誰が、何の目的で、どのリポジトリへ、どの操作を、いつまで行えるかを把握し、不要時に失効できるか | 盗難、異動、退職、用途終了後も、認証情報またはセッションを利用できる状態が残る |

## 読み進め方

端末そのものの保護は[Managed developer endpoint](../../../engineering/source-protection/managed-developer-endpoint/README.md)から確認できます。
SOURCE-001の設計を先行移行したもので、control記録は未移行です。[29項目の対応表](../../../docs/ENDPOINT_MIGRATION.md)に隣接領域と保留事項を残しています。

1. コントロール記録で保証の境界を確認する。
2. [学習ノート](psb-source-004-source-access-credential-lifecycle/learning.md)で、認証情報の窃取がソース管理上の権限へ変わる流れを追う。
3. [Source credential lifecycle pattern](../../../engineering/source-protection/source-access-credential-lifecycle/README.md)で、IDの選択とライフサイクルを設計する。
4. GitHubを利用する場合に限り、[GitHub実装例](../../../engineering/source-protection/source-access-credential-lifecycle/implementations/github/README.md)を読む。
5. [横断分析の軸](../../../docs/ANALYSIS_LENSES.md)で、端末、AIツール、ソース管理、CI/CDのIDへ続く経路を確認する。
