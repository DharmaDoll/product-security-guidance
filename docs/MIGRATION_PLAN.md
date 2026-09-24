# 進め方と移行計画

## 移行の方針

本PJを執筆・移行作業の正本とし、旧product-security-controlsから必要な知識を主題ごとに選別・再編集します。
旧パッケージを保つための空ディレクトリや転送READMEは作りません。独立化の範囲は[Repository cutover](REPOSITORY_CUTOVER.md)に記録しています。

主な成果は、何をすべきか、本質をどこで強制すべきか、何を保証しないかを読者が判断できる知識基盤です。
実装、テスト、導入証拠は、この判断を具体化できる場合だけ別の成果物として作ります。

## 現在地と次の作業

2026-09-24更新。この節を現在地と次作業の正本とし、候補一覧は棚卸し、構造レビューと移行台帳は経緯・判断の記録として使います。

| 状態 | 内容 |
|---|---|
| 現在地 | 26件のcontrol記録・26件の設計パターン。Framework mappingは95件 |
| 直近の成果 | [CONTAINER-002の選別](CONTAINER_REGISTRY_MIGRATION.md)。Registry endpoint、authority、immutability、audit、lifecycle、evidence healthを7特性へ移し、旧synthetic verifierは非移植 |
| 次の主題 | CONTAINER-001から分けたworkload confinementを、runtime privilege・host attachment・filesystem／syscall・resource・networkのどこまで一つの成果にするか選別する |
| 次回に残す判断 | Workload confinementを一つのbaselineに保つか、host boundary・resource availability・network segmentationへ分けるか。IaC enforcementとの重複も確認する。SOURCE-004のASI03は公式PDF本文を取得できた時点で再照合する |
| SOURCE-002に残る作業 | 実環境への配布・有効化、全書込経路の接続、負荷評価、例外承認、他OS・SaaS構成は未実施。代表実装の完了と組織導入を区別する |
| 継続する未確認事項 | 全旧実装の意味的レビュー、参照仕様の現行性、読みやすさとcontrol・pattern間navigationの継続レビュー、実環境の導入・強制 |

各主題は、読者が問い・直接の失敗・適用範囲・セキュリティ特性・隣接境界を判断でき、
参照資料と旧項目との関係を追跡できるところまで整理します。文書の完成に加え、
[主題ごとの具体化判断](ARTIFACT_MODEL.md#主題ごとの具体化判断)で選んだ成果物を完了条件に含めます。
必要な具体実装が残る主題は、文書作成済み・実装未完了として記録します。実環境への導入・診断は別に扱います。
Negative testは[診断観点の列挙で成立する方針](CONTENT_QUALITY.md#negative-test)に従い、実施結果とは区別します。

Git hooksの主題は利用者の指定により先に整理し、代表実装まで追加しました。SOURCE-004は8件中7件の追加照合も完了し、
OWASP ASI03だけを資料取得待ちとして残しました。
その後の主題は、次回のレビュー結果、読者の需要、実装予定、攻撃経路の受け渡しの欠落から選びます。
一つのdomainを全件移してから次へ進む方式や、旧52件を一対一で移す方式にはしません。
候補は[三領域の棚卸し](MIGRATION_CANDIDATES.md)と[残る八domainの棚卸し](PORTFOLIO_MIGRATION_REVIEW.md)に保持します。

## SOURCE-002の具体実装計画

2026-09-23の具体化判断：Git hooksとsecret scannerを接続する技術経路を絞れ、検査対象の取り出し方、拒否への接続、
障害・出力の扱いを具体化すると読者が導入判断をできるため、実装例を必要な成果物に選びます。
文書とNegative testの観点に加え、2026-09-23に[Git・Gitleaks代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)を追加しました。
実装例としての完了条件は満たしました。組織の導入、実環境診断、全経路の強制は別の未実施事項です。

- **配置・範囲**：[Secret checks before publication](../engineering/source-protection/secret-checks-before-publication/README.md)配下の`implementations/`に、一つの代表構成を作る。対象OS・Git・scannerの版を確定し、staged内容・commit message・pushで導入する履歴を検査するローカルhooksとの接続を示す。
- **実装選択**：Gitleaks 8.30.1の組込み検出を採用し、独自scriptはGit objectの取得、上限・未対応形式の拒否、結果の整合確認へ限定した。旧Python検出ルール、Docker wrapper、installerは非移植。旧ルールとの検出範囲の同等性は主張しない。
- **境界**：ローカル実装が担うSECRET-1〜4・6・7の範囲を明示する。SECRET-5は独立した受信側検査の具体設定・確認手順を一構成で示す。受信側が未完なら残作業として記録し、ローカルhooksや送信後のCIで達成した扱いにしない。組織全体の例外承認や全経路の導入済み状態は主張しない。
- **導入と更新**：既存hooks・設定への影響、明示的な導入方法、版の更新、解除・切り戻しを示す。未レビューのhookを自動実行しない。本PJ自身へのhooks有効化は実装例の追加と別の作業とする。
- **確認**：隔離した一時worktreeとbare repository、未発行で無効な検出用文字列により23件を確認した。正常入力、indexと作業ツリーの不一致、履歴・メッセージ・タグ・複数ref・force push・merge、ローカル省略時の受信拒否、設定弱体化、未対応形式、障害、非表示を含む。
- **完了状態**：設定・コード、対象版と取得物digest、導入・解除手順、特性への対応、23件の確認、未検証範囲を実装例から追跡できる。全診断観点の自動化、全OS、SaaS、複数scanner、旧実装の全移植は範囲外。実環境への適用は行っていない。

## 基本分類と横断分析

[Security scope](SECURITY_SCOPE.md)に従い、AI Development SecurityはAIを使う開発環境へ限定します。
製品自体のAI securityはai-security-foundryの担当です。旧AI-010・AI-011・DEPS-005・DETECT-002は`out-of-scope`、旧AI-005〜009は開発環境部分の`scope-review-required`とします。旧52件との差をそのまま未移行の残件数として扱いません。

現行の11 domainを移行先の基本分類として維持します。[Domain一覧](../controls/README.md#domain一覧)を
読者の入口にし、未移行領域も明示します。成果物がない領域の空ディレクトリは作りません。
七つのレイヤーは偏り・空白、十二の攻撃段階は脅威・受け渡しを分析するために使います。
これらをdomainの置換や、領域ごとの全control移行の義務にしません。

一つの主題を移すたびに主なdomain、隣接domain、前後の受け渡しを確認し、Domain一覧と移行台帳を更新します。
初期三領域に加え、残る八domainの初回棚卸しも完了しています。今後は棚卸し結果と七つのレイヤーで優先主題を選びます。
PSIRTはGovernance / Operations、runner内の検知はCI/CD・Buildとの境界、本番runtimeは
Container / Cloud / IaCとの境界を検討します。教育・洞察は各domainに関係する共有成果物として扱います。
基本分類の変更はADRに記録します。境界の詳細は[リポジトリ設計](REPOSITORY_DESIGN.md)を参照してください。

## 初期パイロットで確認した構造

| パイロット | 検証する情報設計 | 残す実装価値 |
|---|---|---|
| [PSB-SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | ガイダンス中心の主題を、成果、教材、設計、製品手順へ分ける | GitHubとIdPの導入判断。架空のJSON検査による導入済み判定は移さない |
| [PSB-DEPS-001](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) | 抽象的な観測期間とresolver／proxy固有の挙動を分ける | 小さなnpm設定例。汎用検証器とproxy clientの一括移植は行わない |
| [PSB-CICD-005](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | 信頼境界、攻撃教材、設計パターン、実行可能な設定を分ける | 無権限PR検証とmerge後のfresh run。危険な比較例は隔離する |

初期三件と、その後のBuild・consumer・Application・Operationsで、成果物を分ける構造をレビューしました。
詳細は[構造レビュー](STRUCTURE_REVIEW.md)に保持します。教材はcontrol・patternへ辿れるnavigationを維持し、受講者個人の理解度や受講記録は本PJで管理しません。

## 参照資料の名称と構造を見直す

参照資料の影響を強めるとは、参考文献を増やすことではありません。資料の役割、採否、変更した判断、
残余境界を、各成果物の設計に反映することです。

移行する資料ごとに次を行います。

1. 主な役割を、規範仕様、脅威、製品仕様、実装候補、ポートフォリオ分析、統合資料に分ける。
2. その役割を誤解させるIDと見出しを見直す。AI、GitHub、toolなどの目立つ語だけで命名しない。
3. 参照版、確認日、ライセンス、採用／変更して採用／不採用、利用先、限界を記録する。
4. 直接の特性根拠と、横断分析だけに使う資料を別の関係として記録する。
5. 廃止したIDは[移行台帳](MIGRATION.md)にだけ残し、新しいツリーや索引へ別名を持ち込まない。

この見直しの最初の対象は`REF-PORTFOLIO-001`でした。七つのレイヤーによる全体分析と、個別のAI境界の
解釈を区別します。他のIDも自動的には継承せず、対応する主題を移す時に資料単位で判断します。

## 一つの主題を移す手順

三領域の初回棚卸しは[Migration candidates](MIGRATION_CANDIDATES.md)を参照してください。
残る8 domainの初回棚卸しは[Portfolio migration review](PORTFOLIO_MIGRATION_REVIEW.md)を参照してください。
個別実装の詳細レビューは未完了です。

```text
旧成果物と参照資料を読む
  -> 直接の失敗、信頼境界、読者の問いを再定義
  -> 主題の具体化判断を行い、必要な成果物・理由・範囲・完了条件を決める
  -> control／教材／pattern／実装／評価へ必要な内容だけ分ける
  -> 参照資料の役割・ID・採否を見直す
  -> 隣接境界と前後の受け渡し、Negative testの診断観点を整理
  -> リンク、版、マッピングを検査。実装を変更した場合は必要な挙動を検証
  -> 読み通しレビュー
  -> 移行台帳と横断索引、この計画の現在地・次作業を更新
```

一回の移行は一つの主題を単独でレビューできる大きさにします。旧52件を一対一変換することや、
旧READMEの全項目を移行先のどこかへ必ず残すことは目標にしません。ただし参照仕様と重要な除外判断は省略しません。

## 独立化後に残る運用判断

公開先と初版の範囲は[Repository cutover](REPOSITORY_CUTOVER.md)で確定しています。
ライセンスは未指定です。旧版READMEからの案内の反映状況と、旧版の維持期間・アーカイブ化は別途確認・判断します。
これらをcontrolの移行完了や実環境の導入済み状態と混同しません。

## 分析の正本

- [参照資料の方針](SOURCE_POLICY.md)
- [参照資料と仕様](../sources/README.md)
- [横断分析の軸](ANALYSIS_LENSES.md)
- [移行台帳](MIGRATION.md)
