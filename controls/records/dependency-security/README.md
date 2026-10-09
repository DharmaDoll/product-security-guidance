# Dependency Security

依存パッケージを採用する判断と、ファイルを取得してコードを実行する許可を分けます。公開者が用意したコードを、開発端末やCIでいつ動かすかが重要です。

| コントロール | 問うこと | できてはいけないこと | 教材 |
|---|---|---|---|
| [PSB-DEPS-001 Dependency release cooldown](psb-deps-001-dependency-release-cooldown/README.md) | 公開直後の版を、決めた期間が過ぎる前に実行・採用していないか | 公開直後、または公開時刻が不明な版を、依存パッケージのコードを実行した後で初めて検査する | [観測期間と他の対策の違い](psb-deps-001-dependency-release-cooldown/learning.md) |
| [PSB-DEPS-002 Install execution policy](psb-deps-002-install-execution-policy/README.md) | install時の外部コード実行を、必要性をレビューした対象だけに限定できるか | 取得の成功や包括的な許可を理由に、準備用コードへ端末・CIの権限を渡す | [取得できても実行してよいとは限らない](psb-deps-002-install-execution-policy/learning.md) |
| [PSB-DEPS-003 Dependency artifact identity](psb-deps-003-dependency-artifact-identity/README.md) | 通常buildが承認した依存関係とファイルを使い、lockを書き換えないか | 古いlock、暗黙の再解決、hash未検証の別ファイルをレビュー済みとして使う | [レビューした内容とbuildの入力が違う](psb-deps-003-dependency-artifact-identity/learning.md) |
| [PSB-DEPS-004 Dependency change review](psb-deps-004-dependency-change-review/README.md) | 現在の依存差分を判断し、拒否・未評価の変更をmerge前に止められるか | 推移依存の見落としや必須でない検査により、危険または未評価の変更がmergeされる | [正しいhashでも採用できるとは限らない](psb-deps-004-dependency-change-review/learning.md) |

教材は対応するcontrolのフォルダにあり、各教材から設計patternへ進めます。

## 読み進め方

更新レビューから通常buildへつなぐには[Dependency artifact identity](psb-deps-003-dependency-artifact-identity/README.md)と
[Dependency change review](psb-deps-004-dependency-change-review/README.md)を使います。
両者の違いは[Artifact identity教材](psb-deps-003-dependency-artifact-identity/learning.md)と
[Change review教材](psb-deps-004-dependency-change-review/learning.md)から読めます。

install時にコードが動く場合は、[Install execution policyの教材](psb-deps-002-install-execution-policy/learning.md)と
[設計パターン](../../../engineering/dependency-security/install-execution-policy/README.md)へ進みます。
Cooldownを通過しても実行許可が完了したとは解釈しません。

1. コントロール記録で、待機期間が保証する範囲を確認する。
2. [学習ノート](psb-deps-001-dependency-release-cooldown/learning.md)で、ロックファイル、スキャナー、プロキシとの違いを理解する。
3. [Dependency release cooldown pattern](../../../engineering/dependency-security/dependency-release-cooldown/README.md)で、強制方法を選ぶ。
4. npmを利用する場合に限り、[npm実装例](../../../engineering/dependency-security/dependency-release-cooldown/implementations/npm/README.md)を読む。
5. [横断分析の軸](../../../docs/ANALYSIS_LENSES.md)で、CI、ビルド、リリース、本番環境へ残る責任を確認する。
