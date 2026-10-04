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

`frameworks.yaml`の`design-reviewed`は、資料本文と指定したcontrol特性の**設計上の部分関係**を照合した状態です。`migration-review-required`は旧関係の再評価待ちで、`relationship: verifies`や`confidence: high`も旧判断を保持した値です。どちらも要件の合格、対策の実効性、組織への導入を示しません。機械処理で現在の対応を表示する場合は`status`、`scope_review`、`limitation`を合わせて読み、再評価待ちを検証済みへ数えないでください。

`pilot.yaml`の`implements`はpatternがcontrolの特性を設計上扱う関係、`realizes`は実装例がpatternの一部を具体化する関係です。`scope`は対応する判断・経路を示し、control全体の合格や実環境での強制を表しません。試験で観測したことと未確認事項は各実装例の本文で確認します。

例外lifecycleを利用するcontrolと、そのcontrolに残すrisk判断・対象identityは
[`exception-consumers.yaml`](exception-consumers.yaml)にあります。この関係は例外を承認したり、元の不合格を`PASS`へ変更したりしません。

`analysis-lenses.yaml`の`direct`、`adjacent`、`handoff`、`gap`は、探索と設計レビューのための関係です。
前段から条件や証拠を受け取るだけなら`adjacent`、成果物から別段階へ判断・証拠を渡すなら`handoff`とします。対応・復旧から前段の実行系へ戻す経路も後者です。
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

SOURCE-001の旧4件は[移行照合](../docs/MIGRATION_SOURCE_PROTECTION.md#endpoint-migration--旧実装とframework-mapping)に履歴として保持し、現行mappingへ継承しません。新たに確認したSSDF PO.5.2の`design-reviewed`は部分的な設計関係のレビュー状態であり、準拠や実環境検証ではありません。

SOURCE-004は[照合記録](../docs/MIGRATION_SOURCE_PROTECTION.md#source-credential-mapping)でSSDF、GitHub guidance 4件、ATT&CK 2件、OSPS 1件を
property単位で再評価しました。`design-reviewed`は資料本文と設計範囲を照合した状態です。SOURCE-004のOWASP ASI03も
開発用agentのソース管理アクセスに限って再照合しました。公式PDF本体のhashと実環境の認可は未確認です。

SOURCE-003は[移行照合](../docs/MIGRATION_SOURCE_PROTECTION.md#public-exposure-migration--旧framework-mapping)で旧4件を再評価し、
public code repository reconnaissanceとの関係が直接説明できるATT&CK `T1593.003`だけを現行mappingへ追加しました。
`detects`は公開候補の観測を表し、攻撃者の検索行動、完全なcoverage、実環境の検知を意味しません。
