# Product Security Guidance

プロダクトセキュリティ担当者と開発者のための、設計・実装判断を支援する知識基盤です。
正本は[product-security-guidance](https://github.com/DharmaDoll/product-security-guidance)です。
旧リポジトリから選別した17 control・18設計パターンを初版とし、残る主題の移行をここで継続します。
端末管理、秘密情報の公開境界、公開source exposure、credential封じ込め、vulnerability priority、artifact recovery、platform provenance generation、deployment artifact admission、container registry publicationを追加し、現在は26 control・26設計パターンです。
[独立化の範囲と検査方法](docs/REPOSITORY_CUTOVER.md)を参照してください。ライセンスは未指定です。外部資料の利用条件はSourcesに記録しています。

## 目的

プロダクトセキュリティ担当者と開発者が、実装またはレビューしようとしている分野について、
次の判断をできる知識基盤を作ります。

- 何を守るべきか、何が起きてはいけないか。
- どのセキュリティ特性を、どの境界で強制すべきか。
- 複数の実装方式から、自分の環境に合うものをどう選ぶか。
- ある対策が保証する範囲と、保証しない範囲はどこか。
- ポートフォリオのどこが空白で、攻撃連鎖の次の段階へ何を引き継ぐべきか。
- さらに深く学ぶ場合、どの一次資料、学習資料、洞察を読むべきか。

コードや設定例の数ではなく、設計と実装の判断を誤らないための「羅針盤」を主な成果とします。

## 作業の進め方

現在地と次の主題、主題ごとの作業手順は[進め方と移行計画](docs/MIGRATION_PLAN.md)を正本とします。
Negative testは[脆弱性診断のチェック観点の列挙でも成立](docs/CONTENT_QUALITY.md#negative-test)し、テストコードの作成・実行を必須にしません。

## 入口を二つに分ける

AI Development Securityは、IDE・CLI・CIなどでAIを使う開発環境を対象とします。
アプリケーション自体のAI securityは[ai-security-foundry](https://github.com/DharmaDoll/ai-security-foundry)へ委ねます。
一般的なApplication Securityは引き続き本PJで扱います。具体的な分担と移行除外は[Security scope](docs/SECURITY_SCOPE.md)を参照してください。

### プロダクトセキュリティ担当者

1. [コントロール一覧](controls/README.md)から、満たすべきセキュリティ上の成果を選ぶ。
2. コントロール記録で、適用範囲、セキュリティ特性、境界を確認する。
3. 必要に応じて[学習資料](docs/learning/README.md)と
   [領域横断の洞察](docs/insights/README.md)で理解を深める。
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
├── controls/       # 何を満たすべきか
├── engineering/    # どう安全に設計・実装するか
├── docs/
│   ├── learning/   # 一つのテーマを具体的に理解する
│   ├── insights/   # 複数領域へ持ち運べる洞察
│   └── ANALYSIS_LENSES.md # ポートフォリオの空白と攻撃段階の受け渡し
├── assessments/    # 組織導入をどう判定するか
├── mappings/       # 独立した成果物間の関係
└── sources/        # 仕様、一次資料、ガイダンス、採否、バージョン
```

役割の詳細は[成果物モデル](docs/ARTIFACT_MODEL.md)、設計判断は
[リポジトリ設計](docs/REPOSITORY_DESIGN.md)を参照してください。

## 横断的に探す

[Portfolio migration review](docs/PORTFOLIO_MIGRATION_REVIEW.md)では、初回に棚卸しした8 domainの候補とその後の移行状況、
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

## パイロットの対象

[Runtime threat detection](controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md)と
[初動への設計pattern](engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md)で、本番の検知・health・通知・triageの責任を分けました。Live sensorや自動対応は未追加です。

アプリケーション領域では[Object access boundary](engineering/secure-design/object-access-boundary/README.md)を新規追加しました。
認証と対象への認可を分け、Python / SQLiteの限定実装で許可と拒否を確認します。既存controlの移行や組織チェックリストの復元ではありません。

[Signature and provenance verification](controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)で、consumerが管理する期待値と使用直前の受入判断を追加しました。

[Build containment](controls/records/build-security/psb-build-001-build-containment/README.md)を追加しました。
実行中の権限・通信と観測の健全性を分け、[設計pattern](engineering/build-security/build-execution-boundary/README.md)からconsumerの独立した受入判断へ引き継ぎます。

追加移行には[Workload federation boundary](controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md)も含まれます。
CIからcloud権限を取得する条件と、取得後の操作範囲・有効期間を分けて扱います。

初期pilotは次の三件です。追加移行の現在の一覧は[Controls](controls/README.md)、設計問題から探す入口は[Engineering](engineering/README.md)です。
四種類の構造検証の結果は[Structure review](docs/STRUCTURE_REVIEW.md)、次の主題は[移行計画](docs/MIGRATION_PLAN.md#現在地と次の作業)にまとめています。

| 領域 | コントロール | パイロットで確認すること |
|---|---|---|
| Source Protection | [PSB-SOURCE-004 Source credential lifecycle](controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | ガイダンス中心のコントロールから、学習資料、設計パターン、GitHub固有の手順を分離できるか |
| Dependency Security | [PSB-DEPS-001 Dependency release cooldown](controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) | 公開後の観測期間という抽象的な保証と、npm固有の実装を分離できるか |
| CI/CD Security | [PSB-CICD-005 Untrusted PR boundary](controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | 未信頼PRの境界を、コントロール、学習ノート、設計パターン、実行可能なGitHub Actions例へ分離できるか |

旧成果物との関係と、意図的に移植しなかったものは
[移行台帳](docs/MIGRATION.md)に記録します。
三領域の初回移行候補と分割・隣接境界の判断は[Migration candidates](docs/MIGRATION_CANDIDATES.md)で確認できます。
初回の追加移行として[Install execution policy](controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md)を再編集しました。
三件のpilotに続き、依存パッケージの採用からinstall時の実行許可へ判断をつなげています。
さらに[Reviewed dependency intake](engineering/dependency-security/reviewed-dependency-intake/README.md)で、
依存更新のレビューと通常buildが使うgraph・bytesの同一性をつなげています。
パイロットが参照する仕様とガイダンスは
[参照資料と仕様](sources/README.md)へ移行し、参照した版を
[フレームワーク対応関係](mappings/frameworks.yaml)から追跡できます。

## このパイロットで行わないこと

- 旧リポジトリのコントロール一覧、スキーマ、生成処理の変更。
- 52件のコントロールの一括変換。
- テスト用データの成功を組織導入の証拠とすること。
- 空の学習資料、実装例、評価を数合わせで作ること。
- 新たなフレームワーク準拠や、リスクを完全に網羅したという主張。参照仕様と既存の対応関係は省略せず、
  バージョン付きで保持した上で「移行レビュー中」として扱う。
