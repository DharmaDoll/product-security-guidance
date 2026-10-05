# Product Security Guidance

プロダクトセキュリティ担当者と開発者のための、設計・実装判断を支援する知識基盤です。
正本は[product-security-guidance](https://github.com/DharmaDoll/product-security-guidance)です。
旧リポジトリから必要な主題を選び直し、現在は51件のcontrolと48件の設計パターンを公開しています。全11 domainと各controlの概要・レビュー時の着眼点は[domain→controlのtree](controls/README.md#domain一覧)、設計方式と実装例は[設計・実装](engineering/README.md)から探せます。
[依存の変更から成果物の使用まで](controls/README.md#依存の変更から成果物の使用まで読む)は、複数の領域を続けて読む例です。
[独立化の範囲と検査方法](docs/MIGRATION_PORTFOLIO.md#repository-cutover)を参照してください。ライセンスは未指定です。外部資料の利用条件はSourcesに記録しています。

## 目的

プロダクトセキュリティ担当者と開発者が、実装またはレビューしようとしている分野について、
次の判断をできる知識基盤を作ります。

- 何を守るべきか、何が起きてはいけないか。
- どのセキュリティ特性を、どの境界で強制すべきか。
- 複数の実装方式から、自分の環境に合うものをどう選ぶか。
- ある対策が保証する範囲と、保証しない範囲はどこか。
- ポートフォリオのどこが空白で、攻撃連鎖の次の段階へ何を引き継ぐべきか。
- さらに深く学ぶ場合、どの一次資料、学習資料、設計パターンを読むべきか。

コードや設定例の数ではなく、設計と実装の判断を誤らないための「羅針盤」を主な成果とします。

## 作業の進め方

現在地と次の主題、主題ごとの作業手順は[進め方と移行計画](docs/MIGRATION_PLAN.md)を正本とします。
[診断で確認する項目](docs/CONTENT_QUALITY.md#failure-checks)は、チェックリストだけでも成立します。
すべてをテストコードにしたり、このPJで実行したりする必要はありません。

## 入口を二つに分ける

AI Development Securityは、IDE・CLI・CIなどでAIを使う開発環境を対象とします。
アプリケーション自体のAI securityは[ai-security-foundry](https://github.com/DharmaDoll/ai-security-foundry)へ委ねます。
一般的なApplication Securityは引き続き本PJで扱います。具体的な分担と移行除外は[Security scope](docs/SECURITY_SCOPE.md)を参照してください。
Web application／web serviceの共通のSecure Coding要件は[ASVSを参照する方針](docs/MIGRATION_PLAN.md#secure-codingの進め方)です。利用者が後日提供する独自の脆弱性診断チェックリストも、原本を確認してから独立した入力として扱います。

### プロダクトセキュリティ担当者

1. [コントロール一覧](controls/README.md)から、満たすべきセキュリティ上の成果を選ぶ。
2. コントロール記録で、適用範囲、セキュリティ特性、境界を確認する。
3. コントロールに`learning.md`があれば、具体的なシナリオと判断の問いを続けて読む。
4. 実装方針は対応する設計パターンで検討する。
5. [横断分析の軸](docs/ANALYSIS_LENSES.md)で、ポートフォリオの空白と攻撃段階の受け渡しを確認する。
6. 判断根拠のバージョンと採否は[参照資料と仕様](sources/README.md)で確認する。

### 開発者・プラットフォーム担当者

1. [設計・実装](engineering/README.md)から、解こうとしている設計問題を選ぶ。
2. 設計パターンで推奨構成、選択肢、トレードオフを確認する。
3. 利用技術に対応する実装例があれば、そこだけを採用・検証する。
4. [横断分析の軸](docs/ANALYSIS_LENSES.md)で、前後の工程に残る責任を確認する。

コントロールと設計パターンは別々に成立します。両者の関係は
[マッピング](mappings/README.md)で後から評価します。

## 成果物の構成

```text
.
├── README.md
├── AGENTS.md
├── PRINCIPLES.md
├── controls/       # 何を満たすべきか。各controlのlearning.mdもここに置く
├── engineering/    # どう安全に設計・実装するか
├── docs/            # 対象範囲、文書の方針、横断分析、移行の記録
├── assessments/    # 組織導入をどう判定するか
├── mappings/       # 独立した成果物間の関係
└── sources/        # 仕様、一次資料、ガイダンス、採否、バージョン
```

役割の詳細は[成果物モデル](docs/ARTIFACT_MODEL.md)、設計判断は
[リポジトリ設計](docs/REPOSITORY_DESIGN.md)を参照してください。`docs/`は判断のルールと移行履歴に絞り、
controlの内容は[domain→controlのtree](controls/README.md#domain一覧)を入口にたどれます。

## 横断的に探す

[Portfolio migration review](docs/MIGRATION_PORTFOLIO.md#portfolio-migration-review)では、初回に棚卸しした8 domainの候補とその後の移行状況、
アプリケーション領域の空白、参照資料と攻撃段階の受け渡し、次の構造検証の順序を確認できます。

実装・レビューする分野が分かる場合は、[11 domainの一覧](controls/README.md#domain一覧)から探してください。
現行のdomainを移行先の基本分類として維持し、移行済みの主題と未移行領域を一覧に示しています。
七つのレイヤーと攻撃段階は、この分類を横断して偏り・脅威・受け渡しを分析する軸です。

領域名やコントロールIDが分からない場合は、[横断分析の軸](docs/ANALYSIS_LENSES.md)から探せます。

- `REF-PORTFOLIO-001`から継承した七つのレイヤーで、分野の偏りと未移行領域を見る。
- サプライチェーン攻撃一覧から継承した十二段階で、攻撃経路とコントロール間の受け渡しを見る。
- `直接`、`隣接`、`受け渡し`、`空白`を区別し、試作版の存在を組織への導入証拠にしない。

分析結果の機械可読な正本は[`mappings/analysis-lenses.yaml`](mappings/analysis-lenses.yaml)、
参照資料の版、採否、限界は[参照資料と仕様](sources/README.md)にあります。

## 移行の記録

初期の三件から、現在は11 domainの主題を選んで移行・再編集しています。現在の成果物は[domain→controlのtree](controls/README.md#domain一覧)と[設計・実装](engineering/README.md)、次の作業は[移行計画](docs/MIGRATION_PLAN.md#現在地と次の作業)で確認できます。旧成果物との対応と採否は[移行台帳](docs/MIGRATION.md)から、domain別の判断と初期の構造レビューへたどれます。
