# マッピング

追加移行の`PSB-DEPS-003`と`PSB-DEPS-004`は、一つの`ENG-DEPS-003: Reviewed dependency intake`へ
対応付けています。採用判断とartifact同一性は別の責任のままです。
GitHub実装との関係は差分・既知脆弱性判定に限定し、通常installやlive merge拒否の確認済み状態を推論しません。

マッピングは、独立して作られたコントロール、設計パターン、実装例、フレームワーク、脅威の関係を評価するものです。
マッピングからコントロールやパターンの意味を逆算しません。

パイロット内の成果物同士の関係は[`pilot.yaml`](pilot.yaml)、既存仕様との関係は
[`frameworks.yaml`](frameworks.yaml)、ポートフォリオのレイヤーと攻撃段階との関係は
[`analysis-lenses.yaml`](analysis-lenses.yaml)にあります。参照仕様の識別情報、採否、限界は
[`参照資料と仕様`](../sources/README.md)が正本です。

例外lifecycleを利用するcontrolと、そのcontrolに残すrisk判断・対象identityは
[`exception-consumers.yaml`](exception-consumers.yaml)にあります。この関係は例外を承認したり、元の不合格を`PASS`へ変更したりしません。

`analysis-lenses.yaml`の`direct`、`adjacent`、`handoff`、`gap`は、探索と設計レビューのための関係です。
コントロールの対応範囲、組織への導入、準拠、フレームワーク要件への対応を表しません。

パイロットでは、旧マッピングが参照していたバージョン、識別子、関係、根拠を省略せず保持しました。
ただし、Source Protectionの17件、Dependency Securityの10件、CI/CD Securityの6件の個別確認項目を、それぞれ6件のセキュリティ特性へ再配置したため、各マッピングは
`migration-review-required`です。削除するのではなく、再レビューが必要な状態を明示しています。

最初に次を確認します。

- コントロールと設計パターンが別々に理解できる。
- 関係を設定した具体的な根拠がある。
- 実装例はコントロール全体ではなく、対応するセキュリティ特性の一部を実現する。
- マッピングの存在を、成熟度、組織への導入、準拠の証明に使わない。
- マッピングの`source_ref`から、参照資料記録の特定の版をたどれる。
- 横断分析では、直接扱う段階と前後の受け渡しを分け、空白を削除しない。
