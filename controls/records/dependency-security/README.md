# Dependency Security

依存パッケージの選択、取得、展開、実行を別々の境界として扱い、外部の公開者が持つ影響力が、
開発者端末、CI、ビルド環境へ無条件に伝わらないようにします。

| コントロール | 問うこと | できてはいけないこと |
|---|---|---|
| [PSB-DEPS-001 Dependency release cooldown](psb-deps-001-dependency-release-cooldown/README.md) | 新しいバージョンに観測期間を設け、その期間中と判定不能時に採用を止められるか | 公開直後、または公開時刻が不明なバージョンを、依存パッケージのコードを実行した後で初めて検査する |
| [PSB-DEPS-002 Install execution policy](psb-deps-002-install-execution-policy/README.md) | install時の外部コード実行を、必要性をレビューした対象だけに限定できるか | 取得の成功や包括的なtrustを理由に、準備用コードへ端末・CIの権限を渡す |
| [PSB-DEPS-003 Dependency artifact identity](psb-deps-003-dependency-artifact-identity/README.md) | 通常buildが承認したgraphとbytesを使い、lockを書き換えないか | 古いlock、暗黙の再解決、hash未検証の別ファイルをreview済みとして使う |
| [PSB-DEPS-004 Dependency change review](psb-deps-004-dependency-change-review/README.md) | 現在の依存差分を判断し、拒否・未評価の変更をmerge前に止められるか | 推移依存の見落としやoptionalな検査により、危険または未評価の変更がmergeされる |

## 読み進め方

更新レビューから通常buildへつなぐには[Dependency artifact identity](psb-deps-003-dependency-artifact-identity/README.md)と
[Dependency change review](psb-deps-004-dependency-change-review/README.md)を使います。
両者の違いは[Reviewed dependency intake教材](../../../docs/learning/reviewed-dependency-intake.md)から読めます。

install時にコードが動く場合は、[Install execution policyの教材](psb-deps-002-install-execution-policy/learning.md)と
[設計パターン](../../../engineering/dependency-security/install-execution-policy/README.md)へ進みます。
Cooldownを通過しても実行許可が完了したとは解釈しません。

1. コントロール記録で、待機期間が保証する範囲を確認する。
2. [学習ノート](psb-deps-001-dependency-release-cooldown/learning.md)で、ロックファイル、スキャナー、プロキシとの違いを理解する。
3. [Dependency release cooldown pattern](../../../engineering/dependency-security/dependency-release-cooldown/README.md)で、強制方法を選ぶ。
4. npmを利用する場合に限り、[npm実装例](../../../engineering/dependency-security/dependency-release-cooldown/implementations/npm/README.md)を読む。
5. [横断分析の軸](../../../docs/ANALYSIS_LENSES.md)で、CI、ビルド、リリース、本番環境へ残る責任を確認する。
