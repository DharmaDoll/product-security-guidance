# 構造と移行対象の判断履歴

独立化、移行候補、構造レビューの判断をまとめています。現在の構造は[リポジトリ設計](REPOSITORY_DESIGN.md)、全体の見取り図は[コントロール一覧](../controls/README.md#domain一覧)、現在の作業は[移行計画](MIGRATION_PLAN.md#現在地と次の作業)を確認してください。

## 収録した記録

- [Repository cutover](#repository-cutover)
- [三領域の移行状況](#migration-candidates)
- [Portfolio migration review](#portfolio-migration-review)
- [Structure review](#structure-review)

<a id="repository-cutover"></a>

<a id="repository-cutover--repository-cutover"></a>
## Repository cutover

<a id="repository-cutover--独立化の範囲"></a>
### 独立化の範囲

2026-09-21、全controlの移行完了を待たず、現在の17 control・18設計パターンを初版として切り出す方針へ変更しました。
SOURCE-001のcontrol記録、未移行主題、保留した実装は切り出し後に継続します。

移行元は`DharmaDoll/product-security-controls`の`experiments/next-repository/`です。
内容の履歴は移行台帳に保持し、外部参照に用いる旧ツリーはコミット
`f429877`の完全なSHAで固定しています。旧実装・参照資料へのリンクは、移行済み本文の正本ではなく根拠と履歴です。
旧リポジトリをローカルに配置する必要はありませんが、外部の参考資料を開くにはネットワークが必要です。

<a id="repository-cutover--初版に持ち込まないもの"></a>
### 初版に持ち込まないもの

- 旧ツリー全体、生成済みチェックリスト、組織固有の入力、作業メモ、認証情報。
- 再配布条件が不明な提供原文の複製。固定版へのリンクと採否・限界を保持します。
- 旧GitHub Actionsの自動実行設定。学習用workflowは実装例の配下に置き、新リポジトリのCIとして起動しません。
- 新しい包括ライセンスの付与。移行元にライセンスファイルが見つからないため、所有者の指定まで保留します。外部資料固有のライセンスはSourcesの記録を維持します。

<a id="repository-cutover--単独での検査"></a>
### 単独での検査

Python 3.10以降とmakeで、リポジトリルートから実行します。文書検査には追加パッケージもネットワークも不要です。

```sh
make check
make test
make test-examples
```

`check`は現在使っているインラインMarkdownリンクのファイル・見出し、リポジトリ外への相対参照、control IDの重複を検査します。
`test`は検査器の正常系・欠落・境界逸脱・重複の扱いを検証します。YAML全体のschema検証やframeworkの意味的妥当性、外部URLの到達性は対象外です。
`test-examples`は[Makefile](../Makefile)に列挙したローカル実装例を検証します。pipを使うテストを含むため、実行環境の版と各実装READMEの条件を確認してください。
いずれも実環境への導入を証明するものではありません。

<a id="repository-cutover--公開先と継続方針"></a>
### 公開先と継続方針

2026-09-22の所有者の指定により、移行先を[Publicリポジトリ](https://github.com/DharmaDoll/product-security-guidance)として確定しました。
`DharmaDoll/product-security-guidance`が今後の執筆・移行作業の正本です。旧`experiments/next-repository/`は切り出し時点の記録として残し、二重に更新しません。
ライセンス未決定の状態を、利用・再配布を自由に許可するものとして扱いません。
旧版READMEからの案内の反映状況は、この文書では未確認です。旧版への案内は確認後に更新します。
旧版の削除・アーカイブ化は別途判断し、今回自動的には行いません。

独立化後の執筆・移行の現在地と次作業は[進め方と移行計画](MIGRATION_PLAN.md#現在地と次の作業)で管理します。

<a id="migration-candidates"></a>

<a id="migration-candidates--三領域の移行状況"></a>
## 三領域の移行状況

Source Protection、Dependency Security、CI/CD Securityの旧19件から、現在の成果物へたどる索引です。2026-09-27に移行先と表記を照合しました。
現在地と次作業は[進め方と移行計画](MIGRATION_PLAN.md#現在地と次の作業)を正本とします。
残る8 domainの初回棚卸しは[Portfolio migration review](MIGRATION_PORTFOLIO.md#portfolio-migration-review)を参照してください。
対象内の18件には主な問いを扱うcontrolまたはpatternへの行き先があり、DEPS-005は対象外です。旧CICD-003の共通要件は既存DETECT-001へ配置し、独立controlは作っていません。旧実装全体の移植や実環境への導入が完了したという意味ではありません。

既存パッケージのIDとパスは追跡用です。新しい成果物の数や名前を一対一で固定するものではありません。
以下の三表は現在の移行先と採否を示します。初回の作業順序は後半に履歴として残し、個別の経緯と旧実装の扱いは[移行台帳](MIGRATION.md)および各対応表を正本とします。

<a id="migration-candidates--判断の根拠"></a>
### 判断の根拠

- [参照資料一覧](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md): 参照版、採否、除外理由を移す際の出発点。
- [REF-PORTFOLIO-001](../sources/README.md#ref-portfolio-001): 七つのレイヤーから偏りを確認する分析入力。
- [Supply-chain attack control list](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md): 攻撃段階、主な脅威、前後の境界を確認する索引。
- [参照資料の方針](SOURCE_POLICY.md): 直接の特性根拠と横断分析を分けるルール。

この索引の更新は、外部資料や製品仕様を再確認した記録ではありません。確認日と採否は移行先の参照資料へたどってください。

<a id="migration-candidates--source-protection"></a>
### Source Protection

| 移行元 | 現在の主題・移行先 | 扱い・残す価値 | 分ける境界 |
|---|---|---|---|
| [PSB-SOURCE-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/README.md) | [Developer endpoint trust](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md) | `split`：端末管理のcontrol、教材、設計へ再編集。[29項目の対応](MIGRATION_SOURCE_PROTECTION.md#endpoint-migration)を保持 | 端末の状態と、侵害後に使えるソース権限は別。実端末の管理・拒否は未確認 |
| [PSB-SOURCE-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/README.md) | [Secret publication boundary](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md) | `split`：公開前の検査、設計、Gitleaks・Python例へ再編集。[旧13項目の対応](MIGRATION_SOURCE_PROTECTION.md#git-hooks-migration)を保持 | ローカルhooksと共有先の強制、例の完成と実導入を分ける |
| [PSB-SOURCE-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/public-repository-exposure/README.md) | [Public source exposure triage](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md) | `split`：公開候補の観測と精査へ再編集。利用者が選んだ公開GitHubの少数指標を[限定実装](../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)。旧PoCの一括移植はしない | 公開ソースの観測、外部サービス台帳、credential失効は別。実検索・通知・対応運用は未確認 |
| [PSB-SOURCE-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/source-access-credential-lifecycle/README.md) | [Source credential lifecycle](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | `split`：control、教材、設計、GitHub手順へ再編集 | 通常の有効期限・退職時の失効と、漏えい後の派生権限の封じ込めを区別する |
| [PSB-SOURCE-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/repository-destruction-recovery/README.md) | Repository recovery independence | `split`: [control](../controls/records/source-protection/psb-source-005-repository-recovery-independence/README.md)、教材、[pattern](../engineering/source-protection/independent-repository-backup-and-restore/README.md)、Git mirror例へ再編集。旧4項目の[採否](MIGRATION_SOURCE_PROTECTION.md#repository-recovery-migration)を保持 | Gitの復元と開発再開、独立した保持、実環境の導入は別 |
| [PSB-SOURCE-006](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/README.md) | Source organization security posture | `split`: [control](../controls/records/source-protection/psb-source-006-source-organization-security-posture/README.md)、教材、[pattern](../engineering/source-protection/organization-baseline-and-drift-review/README.md)、GitHub手順へ移行。旧10項目の[採否](MIGRATION_SOURCE_PROTECTION.md#source-organization-posture-migration)を保持 | ID・公開・CI・復旧の意味と、組織の実適用・確認障害を分ける。Live導入は未確認 |

<a id="migration-candidates--dependency-security"></a>
### Dependency Security

| 移行元 | 現在の主題・移行先 | 扱い・残す価値 | 分ける境界 |
|---|---|---|---|
| [PSB-DEPS-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/release-cooldown/README.md) | [Dependency release cooldown](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) | `split`：control、教材、設計、npm例へ再編集。管理プロキシの取得時遮断・追跡は新規の[DEPS-005](../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md)へ分離 | 公開直後の採用制限と、取得先の制限・遮断情報の適用は別 |
| [PSB-DEPS-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/install-script-execution/README.md) | [Install execution policy](../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md) | `split`：実行許可のcontrol、教材、設計、pip比較例へ再編集 | install時の実行を止めても、import、test、pluginによる後続の実行は止まらない |
| [PSB-DEPS-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/lockfile-integrity/README.md) | [Dependency artifact identity](../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md) | `split`：通常buildの入力を特定するcontrol、教材、共通[設計](../engineering/dependency-security/reviewed-dependency-intake/README.md)へ再編集 | 依存関係の固定、取得したファイルの照合、採用判断を分ける。旧native wrapperは非移植 |
| [PSB-DEPS-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/dependency-change-review/README.md) | [Dependency change review](../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md) | `split`：更新判断のcontrol、教材、共通設計、GitHub review例へ再編集 | レビューした依存関係と実取得を接続する。Advisory未取得・実merge拒否は別に確認 |
| [PSB-DEPS-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/ai-model-supply-chain/README.md) | Model and dataset intake | `out-of-scope`: モデル・データセットのsecurityはai-security-foundryへ委ねる | [Security scope](SECURITY_SCOPE.md)に基づく除外。一般パッケージのDependency Securityは引き続き対象 |

<a id="migration-candidates--cicd-security"></a>
### CI/CD Security

| 移行元 | 現在の主題・移行先 | 扱い・残す価値 | 分ける境界 |
|---|---|---|---|
| [PSB-CICD-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/action-sha-pinning/README.md) | [Workflow dependency identity](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md) | `split`: 直接参照・更新review・内部取得・受入条件へ再編集。限定Python実装、pinact手順、教材まで移行 | [旧6項目と実装・mappingの採否](MIGRATION_CI_CD.md#workflow-dependency-migration)。形式確認と出所・全依存の確認、local成功と実merge保護を分ける |
| [PSB-CICD-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-command-injection/README.md) | [Workflow input handling](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md) | `split`: 原則・教材・設計・診断項目で完了。独自scannerと中央配布は移さない | [旧4項目と実装・mappingの採否](MIGRATION_CI_CD.md#workflow-input-migration)。引数の保持と操作の許可、直接補間と後段の再解釈を分ける |
| [PSB-CICD-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-static-analysis/README.md) | Workflow analysis | `split`：[既存DETECT-001・教材とENG-CICD-007へ配置](MIGRATION_CI_CD.md#workflow-analysis-migration)。独立control・独自scanner・SARIF parserは追加しない | 検査・表示・merge条件を分け、終了0・部分解析・設定変更を確認する。文書と診断項目で完了、実環境の強制は未確認 |
| [PSB-CICD-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-least-privilege/README.md) | [Workflow authority minimization](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md) | `split`: 用途・実効権限・開始条件・委譲へ再編集。GitHub設定と無権限・読取り専用smoke例を追加 | [旧6項目と実装・mappingの採否](MIGRATION_CI_CD.md#workflow-authority-migration)。形式と最小性、標準tokenと追加権限、ローカル確認と実GitHubの拒否を分ける |
| [PSB-CICD-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/untrusted-pr-boundary/README.md) | [Untrusted PR boundary](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | `split`：control、教材、設計、GitHub Actions例へ再編集 | PR由来の状態の昇格と、信頼済みrevisionで開始した後の権限は別 |
| [PSB-CICD-006](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/audience-bound-oidc-federation/README.md) | [Workload federation boundary](../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md) | `split`：発行条件・交換先権限のcontrol、教材、設計、AWS trust例へ再編集 | 短命tokenでも広いsubjectや交換先権限の影響は残る。実交換・拒否・失効は未確認 |
| [PSB-CICD-007](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/runner-hardening/README.md) | [Runner lifecycle isolation](../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md) | `split`：一jobの隔離・破棄のcontrol、教材、共通[設計](../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)へ再編集 | 登録解除とhost破棄は別。実行時検知と実環境の破棄確認は別途必要 |
| [PSB-CICD-009](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/cache-provenance-isolation/README.md) | [Cache trust boundary](../controls/records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md) | `split`：保存者・利用者・内容のcontrol、教材、共通設計へ再編集 | Key一致と内容の真正性は別。Runner内の残存状態と実cacheの権限も分ける |

廃止したcontrolの扱いは[ADR-0003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/adr/0003-privileged-change-runbook.md)に従います。
共通変更管理はrunbookとして移行を検討し、独立したcontrolとして復活させません。

<a id="migration-candidates--初回追加移行の順序履歴"></a>
### 初回追加移行の順序（履歴）

| 順序 | 主題 | 攻撃段階・脅威 | 次の読者の判断 | 参照資料を反映する方法 |
|---|---|---|---|---|
| 1 | Install execution policy | 4→7: 採用したdependencyのhookやbuild backendがCI権限で動く | 必要なinstall-time executionだけをどこで許可し、未承認実行をどう止めるか | 旧DEPS-002の製品仕様・mappingを保持。製品挙動は公式仕様で再確認してから実装例へ移す |
| 2 | Dependency artifact identity / Dependency change review | 4→7: 差し替え、未reviewの推移依存、根拠不足 | reviewしたgraphと実際に取得・実行する内容をどう接続するか | `REF-DEPS-002`とnative lockfile仕様を分けて扱い、欠落したadvisoryを明示する |
| 3 | Workload federation boundary | 5→6→10: CI状態からcloud・deploy権限を取得 | revision、workflow、発行条件、引受先権限のどれを制限するか | `REF-CICD-009`を脅威・設計入力に使い、GitHubとAWSの仕様・版を別に追跡する |
| 4 | Cache trust boundary / Runner lifecycle isolation | 5→7: 低信頼の永続stateが後続jobへ届く | 再利用するstateと破棄する資産をどこで分けるか | `REF-CICD-014`の登録・host破棄・ログ保存の違いを反映し、BUILD-001へ渡す責任を示す |

この順序は、[攻撃段階の索引](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md)から選んだ移行上の優先順位です。
現在の移行先は上の三表へ反映しています。この初回の順序を今後の作業指示や組織への導入順とは扱いません。

<a id="migration-candidates--横断資料と未確認範囲"></a>
### 横断資料と未確認範囲

旧`REF-CICD-011`のthreat matrixと旧`REF-CICD-012`のNIST SP 800-204Dは、横断分析の追加入力候補です。原文と版、資料の役割、既存資料との重複を確認して採否を決めます。ここでの旧IDは追跡用で、移行先の参照資料IDや個別要件ではありません。採用する場合も版・旧IDとの関係・採否・限界を記録します。

Runner内のruntime detectionは、runner破棄へ吸収しません。旧`REF-BUILD-001`は
センサー候補の発見にとどまり、導入済みではありません。プロセス・file・networkの何を観測できるか、
センサー停止をどう検出するか、権限と秘密情報をどう扱うかを評価してから採否を決めます。

七つのレイヤーでは、三領域の主題はプラットフォームと外部依存へ偏っています。
アプリケーションの設計・実装、PSIRT、本番運用、ガバナンス、教育の棚卸しは[Portfolio migration review](MIGRATION_PORTFOLIO.md#portfolio-migration-review)に保持します。
Falco／Sysdig等の本番監視もその対象です。CIの検査や署名だけで、本番の検知・対応を満たしたとは扱いません。

<a id="migration-candidates--文書の完成と実環境の確認"></a>
### 文書の完成と実環境の確認

Control・教材・設計の移行先は上の三表からたどれます。旧実装の不在を一律に未完了とせず、必要な成果物は[実効性の基準](ARTIFACT_MODEL.md#主題ごとの具体化判断)で選びます。[診断で確認する項目](CONTENT_QUALITY.md#failure-checks)はチェックリストでも完成します。

実際の検査範囲、権限、merge拒否、runner破棄、復元、通知・対応運用は、採用対象と許可された確認方法を決めてから評価します。必要な実装を選んだのに前提が不足する場合だけ、理由と再開条件を計画へ残します。全旧実装・検証器の意味的レビューや、全製品の現行仕様を確認済みとは扱いません。

<a id="portfolio-migration-review"></a>

<a id="portfolio-migration-review--portfolio-migration-review"></a>
## Portfolio migration review

<a id="portfolio-migration-review--今回の判断"></a>
### 今回の判断

この文書は初回に棚卸しした8 domainの候補と、その後の移行判断を保持します。現在の全件一覧は[Controls](../controls/README.md)、現在地と次作業は[進め方と移行計画](MIGRATION_PLAN.md#現在地と次の作業)を正本とします。
読者が判断できる内容を増やすことが目的であり、旧パッケージの数を新構造へ揃えることは目的ではありません。

2026-09-27追加：[SOURCE-005の移行判断](MIGRATION_SOURCE_PROTECTION.md#repository-recovery-migration)で、攻撃段階2の破壊権限から段階12の独立した保管・復元・開発再開へ接続しました。三領域の候補は[別の棚卸し](MIGRATION_PORTFOLIO.md#migration-candidates)に保持し、ローカルGit復元の成功を全復旧の完了にはしません。

同日追加：[SOURCE-006の移行判断](MIGRATION_SOURCE_PROTECTION.md#source-organization-posture-migration)で、段階2・6の組織設定と管理権限から、段階5のCIと段階12の調査へ現在状態・適用漏れ・確認障害を渡します。個別controlの意味と、共通方針の実適用を区別します。

同日追加：[CICD-001の移行判断](MIGRATION_CI_CD.md#workflow-dependency-migration)で、段階5の外部コードの選択を段階2の受入ルール、段階4の依存採用判断、段階7の実行へ接続しました。直接参照の検査、選ぶコードと内部取得のレビュー、jobの権限を分け、権限は下記CICD-004へ接続しています。

同日追加：[CICD-004の移行判断](MIGRATION_CI_CD.md#workflow-authority-migration)で、段階5・6のjob用途と実効権限、開始条件、委譲を、段階7・9・10の実行・公開・deployへ渡します。GitHubの具体設定と無権限smoke手順を示し、実付与・承認・拒否を確認済みとはしません。

同日追加：[CICD-002の移行判断](MIGRATION_CI_CD.md#workflow-input-migration)で、段階5の外部入力と命令の解釈を整理しました。引数の保持と操作の許可、呼出先までの扱いを分け、文書と診断項目で完了としています。独自scanner・中央配布の追加は必要とせず、実際の拒否・導入は未確認です。

同日追加：[旧CICD-003の移行判断](MIGRATION_CI_CD.md#workflow-analysis-migration)では、共通要件と教材を既存DETECT-001、workflow固有の設計をENG-CICD-007へ配置しました。[三領域の索引](MIGRATION_PORTFOLIO.md#migration-candidates)は現在の行き先へ更新し、教材への導線と古い状態表記の補修は[構造レビュー](MIGRATION_PORTFOLIO.md#structure-review--2026-09-27移行状況と教材への導線)に記録しています。

2026-09-16時点の旧`controls/*/*/control.yaml`には52件ありました。初回棚卸しの3 domainが19件、
今回の8 domainが33件で、旧Secure Design controlは0件でした。2026-09-25にrepository pilotから
[PSB-DESIGN-001](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)を追加しています。
これは旧controlの移行や組織への導入を意味しません。

2026-09-20の[スコープ決定](SECURITY_SCOPE.md)により、製品自体のAI securityはai-security-foundryの担当です。
下記の旧件数は棚卸しの履歴です。`out-of-scope`を残作業へ加えません。旧AI-005〜009の範囲選別は[別記録](MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review)にまとめました。

今回の対象はメタデータ、READMEの主題・参照先、既存の計画と参照資料記録です。
実装コード・全検証器の意味的レビュー、製品の現在の仕様、実環境の採用状態は未確認です。
以下は候補の判断と移行状態です。移行済みでも実装・導入の完了やframework要件の充足を意味しません。

<a id="portfolio-migration-review--分析の根拠"></a>
### 分析の根拠

- [参照資料一覧](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md): 版、採否、除外理由、重要仕様を保持する出発点。参照資料の継承と本文の圧縮を別に扱う。
- [REF-PORTFOLIO-001](../sources/README.md#ref-portfolio-001): 七つのレイヤーで偏りを確認する。個別の要件へ自動変換しない。
- [Supply-chain attack control list](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md): 攻撃段階と前後の責任を確認する。アプリケーション固有の悪用経路をこの12段階だけへ押し込めない。
- [参照資料の方針](SOURCE_POLICY.md)、[成果物モデル](ARTIFACT_MODEL.md): control、教材、pattern、製品実装、評価を役割で分ける。

<a id="portfolio-migration-review--初回に棚卸しした8-domainと現在の扱い"></a>
### 初回に棚卸しした8 domainと現在の扱い

表の`split候補`は必要な知識を再編集して実装と分ける方針、`deferred`は今回の追加pilotより後に扱う方針です。
教材は各controlの問いに分けるか正本へリンクし、controlの異なる保証境界は統合しません。旧controlへのリンクは移行元、新しい記録へのリンクは移行先です。

<a id="portfolio-migration-review--secure-design--旧control-0件repository-pilot-1件"></a>
#### Secure Design — 旧control 0件、repository pilot 1件

既存controlから移植できる内容はありません。[計画済み主題](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/PLANNED_CONTROLS.md)を起点に、
資産・主体・データフロー・信頼境界から設計を判断する教材を新たに検討します。
[REF-USER-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-user-004)の組織チェックリストは原本未提供です。
ASVS等から原本を復元したり、空のcontrolを作ったりせず、原本の受領を待つ作業と公開教材の設計を分けます。

最初の候補だった「利用者が指定する対象へのアクセスを、どこで認可するか」は、2026-09-17に教材、pattern、
Python / SQLiteの限定実装として具体化し、2026-09-25に[PSB-DESIGN-001](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)として
保証目標を明示しました。既存IDの移行ではなく、未提供の組織チェックリストやexact ASVS mappingを補完したものでもありません。

2026-10-05の[具体化判断の見直し](MIGRATION.md#design-001-example-retirement)で説明用サンプルと7テストを削除し、control・教材・設計・診断項目で完了としました。

<a id="portfolio-migration-review--secure-coding--1件"></a>
#### Secure Coding — 1件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-CODE-005 Unicode source review](../controls/records/secure-coding/psb-code-005-unicode-source-review/README.md) | `移行済み`: 表示と解釈が異なるソース、レビューで見落とす条件、Python 3.10限定の検出実装を分離。旧項目との対応は[移行記録](UNICODE_SOURCE_MIGRATION.md) | Pythonの狭い拒否profileを一般要件にしない。Review UIとprotected CIは未確認。認可・入力処理等の欠陥は別 |

唯一の既存例を移すだけではSecure Codingの情報設計を検証したとは扱いません。
Web application／web serviceに共通する認証、認可、入力処理等の要件は[ASVS 5.0.0](../sources/README.md#spec-owasp-asvs-5-0-0)を参照します。旧計画の`PSB-CODE-001〜004`を一対一で新controlへ移しません。具体的な失敗経路、強制点、教材、実装の選択に独自の価値がある主題だけを掘り下げます。[Secure Codingの進め方](MIGRATION_PLAN.md#secure-codingの進め方)を判断の正本とします。

利用者の経験由来の脆弱性診断チェックリストは後日受領する独立入力です。原文・由来・公開可否を確認してから、ASVSとの重複や補完関係を項目ごとに判断します。旧`REF-USER-004`と同一資料かは未確認です。まだ項目を作らず、ASVSで代用もしません。

<a id="portfolio-migration-review--build-security--3件"></a>
#### Build Security — 3件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-BUILD-001 Build containment](../controls/records/build-security/psb-build-001-build-containment/README.md) | `移行済み`: 入力、通信、権限、隔離、検知の役割を分けたガイダンス | 実sandbox・通信拒否・sensorは未確認 |
| [PSB-BUILD-002 Approved and consistent release build](../controls/records/build-security/psb-build-002-approved-consistent-build/README.md) | `移行済み`: producerが承認するbuilder、build定義・重要入力、実際の経路とrelease昇格を分ける。旧合成verifierは非移植 | Hostedであることは再現性・隔離・SLSA levelの証明ではない。実platformとgateは未選定 |
| [PSB-BUILD-003 Platform provenance generation](../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md) | `移行済み`: platform側の来歴生成とjob側の自己申告を区別する | 来歴の生成、配布、consumerによる照合は別の責任。製品実装は未選定 |

<a id="portfolio-migration-review--container--cloud--iac-security--5件"></a>
#### Container / Cloud / IaC Security — 5件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-CONTAINER-001 Deployment artifact admission](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md) | `分割移行済み`: Exact artifact、consumer acceptance、final-stateの拒否境界。Privilege・host・filesystemは[PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)、networkは[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)、resourceは[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)へ移行 | Live admission、workload・CNI・resource runtime enforcementは未確認 |
| [PSB-CONTAINER-002 Container registry publication boundary](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md) | `移行済み`: Endpoint、repository権限、変更不能性、audit、lifecycle | 登録内容の安全性とadmissionは別。Provider実装は未選定 |
| [PSB-CONTAINER-003 Container host and daemon boundary](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md) | `移行済み`: Runtime・kubelet・host管理面、node identity、更新・隔離・再登録を分けた。[旧成果物](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-host-daemon-hardening/README.md)のsynthetic evaluatorは非移植 | Workload設定はCONTAINER-005。対象OS／runtime／provider未選定のため実装は作らず、live nodeは未確認 |
| [PSB-CONTAINER-004 Runtime threat detection](../controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md) | `移行済み`: 観測、rule、配送、sensor health、対応判断を分けたガイダンス | Live sensor・配送・対応は未確認。CIの検知を本番の導入証拠にしない |
| [PSB-IAC-001 Infrastructure change authorization and drift](../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md) | `移行済み`: Golden Pathを入口へ位置付け、source・依存、resolved plan、apply、provider状態、driftを結ぶ。旧synthetic verifierは非移植 | Plan検査、provider側の強制、現在状態を分けて接続。対象provider／resource未選定のため実装は作らず、live cloudは未確認 |

<a id="portfolio-migration-review--release-integrity--5件"></a>
#### Release Integrity — 5件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-REL-001 Signature / provenance verification](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md) | `移行済み`: consumerが管理する署名者・builder・sourceの期待値をガイダンス化 | Crypto実装は保留。有効な署名でも期待しない生成条件なら拒否する |
| [PSB-REL-002 Provenance distribution and availability](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md) | `移行済み`: Artifact digestから一つ以上のprovenanceを発見・取得し、publication completion、immutability、retention、no downgradeを管理。旧synthetic verifierは非移植 | 生成はBUILD-003、consumer検証はREL-001。対象ecosystem未選定のためlive distributionは未確認 |
| [PSB-REL-003 Release SBOM identity and analysis](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md) | `移行済み`: Source・build・operations観測を分け、exact artifact、coverage、公開、analysis処理を接続。CycloneDX bindingを限定実装 | `complete`はcoverageの自動証明ではない。Live storage・Dependency-Track・deployment catalogは未確認 |
| [PSB-REL-004 Supplier SBOM intake trust](../controls/records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md) | `移行済み`: 利用者側の期待値、出所・対象の確認、隔離、評価不能、限定取込を設計 | 署名はSBOMの網羅性や製品の無害性を証明しない。供給者と方式が未選定のため具体実装は保留 |
| [PSB-REL-005 Artifact signing generation](../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/README.md) | `移行済み`: 承認したexact artifact、署名権限、鍵、署名結果、公開完了を分ける。旧合成receiptは非移植 | sign-only権限と署名対象の正当性は別。signer・公開先未選定のため具体実装とlive署名は未確認 |

<a id="portfolio-migration-review--ai-development-security--旧11件を範囲別に選別"></a>
#### AI Development Security — 旧11件を範囲別に選別

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-AI-001 Repository agent guidance](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md) | `記録移行済み`: 開発agentの指示の読込み、変更レビュー、安全と作業達成の比較 | [旧合成benchmarkとの違い](MIGRATION_AI_DEVELOPMENT.md#repository-agent-guidance-migration)。GitHub変更レビュー例は未導入。製品AIの設計・TEVVは別PJ |
| [PSB-AI-002 Agent extension dependency governance](../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md) | `移行済み`: 拡張の内容・権限・審査・期限・失効と実行環境への受け渡し | 稼働版の証明、内容審査の質、実行時強制は未確認 |
| [PSB-AI-003 Development content injection boundary](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md) | `記録移行済み`: repository文書・Issue・PR・tool出力から開発agentへの間接注入を扱う | [旧fixtureとの違い](MIGRATION_AI_DEVELOPMENT.md#development-content-injection-migration)。製品のchatbot・RAGは別PJ、実agentの拒否は未検証 |
| [PSB-AI-004 AI coding agent runtime hardening](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/README.md) | `記録移行済み`: [操作認可](../engineering/ai-development-security/development-action-authorization/README.md)・教材と[実行環境の隔離](../engineering/ai-development-security/development-runtime-isolation/README.md)を再編集 | [Control記録](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)を再編集。製品adapter・実環境は未検証 |
| [PSB-AI-005 Agent memory / context lifecycle](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-memory-context-lifecycle/README.md) | `deferred`: 開発agentが作業をまたいでcontextを保存・再読込する場合に再開 | 製品のmemory・tenant境界は別PJ。[選別詳細](MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review) |
| [PSB-AI-006 Agent action integrity / output validation](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-action-integrity-output-validation/README.md) | `split`: 開発agentの操作認可と結果不明はAI-004へ接続。別controlは作らない | 製品内agentのaction処理は別PJ。[選別詳細](MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review) |
| [PSB-AI-007 Development agent work budget](../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md) | `記録移行済み`: 開発作業の累積量・予約・並列・停止を設計。GNU timeoutのローカル実行期限を六件で確認 | 製品AIの予算は別PJ。費用・呼び出しの共通予約と実agentは未検証。[移行詳細](MIGRATION_AI_DEVELOPMENT.md#development-work-budget-migration) |
| [PSB-AI-008 Multi-agent trust / delegation](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/multi-agent-trust-delegation/README.md) | `deferred`: 開発agent間の実際の委譲経路を採用した場合に再開 | 製品のmulti-agent構成は別PJ。[選別詳細](MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review) |
| [PSB-AI-009 Rogue agent containment / recovery](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/rogue-agent-containment-recovery/README.md) | `deferred`: 長時間・自律実行する開発agentと停止経路を採用した場合に再開 | 製品AI機能の封じ込め・復旧は別PJ。[選別詳細](MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review) |
| [PSB-AI-010 AI application gateway / data egress](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-application-gateway-data-egress/README.md) | `out-of-scope`: ai-security-foundryへ委ねる | AI application gatewayは本PJへ移行しない |
| [PSB-AI-011 RAG corpus integrity / retrieval](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/rag-corpus-integrity-retrieval/README.md) | `out-of-scope`: ai-security-foundryへ委ねる | RAG corpus・retrievalは本PJへ移行しない |

AI領域は開発環境で守る資産と権限を特定してから、一般的な認可・外部入力・依存受入との共通教材を検討します。別PJの担当は[Security scope](SECURITY_SCOPE.md)で確認します。
製品固有のhookやadapterを一般原則へ置き換えず、現行仕様を再確認した実装だけを別に移します。

<a id="portfolio-migration-review--detection--verification--3件"></a>
#### Detection / Verification — 3件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-DETECT-001 Scanner evidence trust boundary](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md) | `移行済み`: scanner自身の出所・DB・終了状態と検査対象を分離 | 実行成功、findingなし、coverage十分は別 |
| [PSB-DETECT-002 AI TEVV release gate](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/detection-verification/ai-tevv-release-gate/README.md) | `out-of-scope`: AI製品のTEVVはai-security-foundryへ委ねる | 開発用guidance・拡張の限定評価は旧AI-001の別境界として扱う |
| [PSB-DETECT-003 External attack surface reconciliation](../controls/records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md) | `移行済み`: 所有範囲、外部観測、帰属、再出現、観測障害をcontrol・教材・patternへ分離 | 自社domainが指す第三者IPをscan権限へ拡張しない。旧fixtureをlive coverageと扱わない |

<a id="portfolio-migration-review--governance--operations--5件"></a>
#### Governance / Operations — 5件

| 移行元 | 扱い・残す判断材料 | 分ける境界 |
|---|---|---|
| [PSB-GOV-001 Supply-chain impact assessment](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md) | `移行済み`: packageからbuild・artifact・稼働製品への逆引きと初動のガイダンス | 実組織の対応能力と実対応は未確認 |
| [PSB-GOV-002 Security exception lifecycle](../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md) | `移行済み`: 共通lifecycleとcontrol固有risk判断を分離 | 例外が有効でも元の不合格が合格になるわけではない |
| [PSB-GOV-003 Product vulnerability priority decision](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md) | `migrated-guidance`: 適用性、known exploitation、severity、priority、期限、担当者 | 旧composite verifierは非移植。Adapterは観測可能な単位へ分ける |
| [PSB-GOV-004 Credential exposure containment](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md) | `migrated-guidance`: 漏えい疑い、派生権限、consumer移行、古い権限の拒否、影響調査 | 旧synthetic verifierは非移植。Providerとcredential classを選定してから実装する |
| [PSB-GOV-005 Deployed artifact recovery](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md) | `migrated-guidance`: current riskからclean rebuild・replacement・旧digest非稼働まで | 旧synthetic verifierは非移植。Builder・registry・deployment platform選定後に実装する |

<a id="portfolio-migration-review--参照資料を移す優先単位"></a>
### 参照資料を移す優先単位

この表は旧資料記録への追跡です。まだ移行していない資料へ新IDを確定せず、各pilotで役割・命名を見直します。
外部リンク、exact version、integrity記録、利用条件・除外理由は旧記録を正本として保持します。

| 主題 | 保持する仕様・資料 | 設計へ反映する判断 |
|---|---|---|
| Build→Release | [REF-BUILD-001](../sources/README.md#ref-build-001)、[NIST SP 800-204D記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-cicd-012)、[threat matrix記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-cicd-011)、[SLSA registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/slsa/README.md)、[Sigstore記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-rel-003) | containment、来歴生成、署名、consumer照合を別の強制点としてつなぐ。SLSA source/build要件を区別する |
| Runtime / cloud / IaC | [IaC change資料](../sources/README.md#ref-iac-change-boundary-001)、[Container host資料](../sources/README.md#ref-container-host-daemon-001)、[Runtime detection資料](../sources/README.md#ref-container-003) | IaC plan・apply・actual state、container admission、host、観測、配送、health、対応を分ける。旧製品版やmutableな文書を現在の仕様と断定しない |
| PSIRT / exposure / refresh | [SBOM lifecycle](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-rel-002)、[Dependency-Track](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-rel-001)、[REF-USER-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-user-005)、[KEV](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-002)、[FIRST maturity](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-003)、[FIRST Services 1.1](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-004)、[CVSS 4.0記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-005)、[NIST SP 800-61 Rev.3記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-006) | 正確な製品適用、担当者、対応期限・連絡、置換完了をつなぐ。PSIRT能力評価と個別controlの合格を分ける |
| Application / AI / scanner | [REF-USER-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-user-004)、[AI設計資料一覧](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md)、[ASVS registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/owasp-asvs/README.md)、[AISVS registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/owasp-aisvs/README.md)、[ATLAS registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/mitre-atlas/README.md)、[Trivy記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-detect-001) | 外部入力を権限へ昇格させない原則と製品固有の実装を分ける。exact要件・ATLAS content/format版を保持し、欠けた組織原本を補完しない |

上記の組合せと優先順位はリポジトリでの解釈です。資料の推奨を一括採用したという意味ではありません。

<a id="portfolio-migration-review--攻撃段階と受け渡しのレビュー"></a>
### 攻撃段階と受け渡しのレビュー

| 攻撃段階 | 主な脅威 | 対応候補・次の境界 |
|---|---|---|
| 3: AI開発経路 | 外部指示や拡張がtool権限へ昇格し、処理の反復が長引く | [AI-001](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)でrepository指示、[AI-002](../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md)で拡張採用、[AI-003](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)で資料と依頼、[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)で実効権限、[AI-007](../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md)で作業予算を分ける。旧AI-006の開発環境部分はAI-004へ接続。実agentの強制と結果は未検証 |
| 7→8: Build実行・来歴 | build中に秘密情報を取得し、自己申告の証跡を正規の来歴にする | [BUILD-001](../controls/records/build-security/psb-build-001-build-containment/README.md)→[BUILD-002](../controls/records/build-security/psb-build-002-approved-consistent-build/README.md)→[BUILD-003](../controls/records/build-security/psb-build-003-platform-provenance-generation/README.md)。実行境界、承認builder、platform生成境界を分離済み。製品実装とlive builder評価は未確認 |
| 9→10: Release・admission | 署名済みでも期待しない成果物を配布・実行し、正規workloadへ過大なhost権限を渡す | [REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)→[CONTAINER-001](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)でartifactを、[CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)でruntime authorityを別に判断する。Live enforcementは未確認 |
| 11→12: 本番・対応 | sensor停止、通知不達、未知資産、適用製品の誤認で対応が遅れる | [CONTAINER-004](../controls/records/container-cloud-iac-security/psb-container-004-runtime-threat-detection/README.md)、[DETECT-003](../controls/records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md)→[GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)→[GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)。収集異常とsecurity findingを別に扱う |

Secure Design / Secure Codingは、この供給経路とは別に、正規利用者が他者のデータへアクセスする等の
アプリケーション内の悪用経路を扱います。ソースや署名が正規でも認可欠陥は成立します。

<a id="portfolio-migration-review--次の作業順序と一区切り"></a>
### 次の作業順序と一区切り

2026-09-17更新: [構造レビュー](MIGRATION_PORTFOLIO.md#structure-review)で集約表・索引・参照anchorを修正しました。
2026-09-20更新: GOV-001、GOV-002、DETECT-001、AI-002の追加後に横断レビューと補修を行い、AI-004は操作認可の設計・教材を先行移行しました。その後の補修は[構造レビュー](MIGRATION_PORTFOLIO.md#structure-review)、現在地と次作業は[移行計画](MIGRATION_PLAN.md#現在地と次の作業)に記載します。

<a id="portfolio-migration-review--初回の作業順序履歴現在の指示ではない"></a>
#### 初回の作業順序（履歴・現在の指示ではない）

2026-09-17追記: Operations pilotとしてPSB-CONTAINER-004、教材、ENG-RUNTIME-001を再編集しました。
GOV-001はcontrol・教材・patternへ分離済みです。実対応・PSIRT能力評価は未実施です。
四つの異なる主題の初回再編集は揃いました。次は構造レビューで重複・参照欠落・入口の整合性を確認し、次batchを決めます。

2026-09-17追記: Application pilotとして[Object access boundary](../engineering/secure-design/object-access-boundary/README.md)、教材、Python / SQLiteの限定実装を追加しました。
既存control IDや組織チェックリストを流用せず、認証済みcontextの契約とDB条件を分けています。全endpoint・HTTP認証・並行処理は未確認。次はOperations pilotです。

2026-09-25追記: 上記教材を[PSB-DESIGN-001](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)の隣へ移し、repository pilotとしてcontrol記録を追加しました。

2026-09-17追記: Consumer pilotの記録・教材・patternの再編集も完了しました。Crypto実装は保留し、次はApplication pilotへ進みます。

2026-09-17更新: Build pilotのcontrol・教材・pattern・参照資料の再編集は完了しました。
[移行台帳](MIGRATION.md)に保留した実装と未確認範囲を記録しています。次はConsumer pilotです。

1. **Build pilot**: PSB-BUILD-001を再編集。実行中の権限・通信をどこで制限するかと、sensorの観測・health・対応を分ける。実装を移す場合だけ実際の拒否挙動を検証する。
2. **Consumer pilot**: PSB-REL-001で、Buildの出力を誰の期待値で受け入れるか検証する。producerの自己申告をconsumer policyにしない。
3. **Application pilot**: Secure Designの一つの認可シナリオからSecure Codingの小さな実装・拒否テストへつなぐ。仕様・IDは着手時に決定し、原本未提供のチェックリストとは分離する。
4. **Operations pilot**: PSB-CONTAINER-004とPSB-GOV-001のうち一つの検知→初動シナリオを選ぶ。イベント、sensor health、配送、製品適用、担当者をつなぎ、PSIRT全体を満たすとは扱わない。
5. **構造レビュー**: control・教材・pattern・評価の重複、参照仕様の欠落、担当者と開発者の入口を読み通す。その結果で構造を調整し、次の移行batchを決める。

各回で有用な教材を正本として作り、複数domainへ複製しません。講義で生じた横断的な問いや見方は
まず教材の文脈に残し、独立成果物を先に作りません。ファイル数・移行件数・全レイヤーの充足は完了条件にしません。

この一区切りでは、基盤・consumer・アプリケーション・運用という異なる性質の内容で新構造が機能することを確認します。
個別実装の採否、exact mappingの再割当、参照IDの名称改革、現在の製品仕様の確認は各pilotの台帳へ残します。
棚卸しだけではcontrol indexやframework mappingに移行済みの関係を追加しません。

<a id="structure-review"></a>

<a id="structure-review--structure-review"></a>
## Structure review

この文書は構造レビューの結果と、その後の補修の記録です。現在地と次作業は[進め方と移行計画](MIGRATION_PLAN.md#現在地と次の作業)を参照してください。

<a id="structure-review--2026-10-04ai領域の対象とsource-004のasi03関係"></a>
### 2026-10-04：AI領域の対象とSOURCE-004のASI03関係

AI domainの5 controlと対応する教材・pattern・機械可読記録を点検しました。現行の本文は開発用agentとその環境を扱い、製品AIの設計要件を取り込んでいません。AI-004のREADMEと機械可読記録で人による重要操作の承認を同じ文に揃えました。[対象範囲](SECURITY_SCOPE.md)と[移行台帳](MIGRATION.md#2026-10-04source-004のasi03関係とai領域の範囲を確認)に判断を残しました。

SOURCE-004の旧ASI03関係はソース管理の認証情報に限定して`mitigates/medium`へ変更。全92件のframework関係は資料本文と特性の設計上の関係を再照合済みです。公式OWASP PDF本体のhash、実環境の権限・失効・拒否、開発者の理解度は確認していません。新しい実装・テストコードは追加していません。

<a id="structure-review--2026-10-04ai-004のowasp-agentic-top-10関係"></a>
### 2026-10-04：AI-004のOWASP Agentic Top 10関係

旧ASI02〜05の4件を、開発用agentの実行時境界に当たる部分へ絞りました。ASI02は正規toolの誤用、ASI03は継承した権限、ASI04は実行時の拡張・toolの読込み、ASI05は意図しないcode実行を扱います。いずれも`mitigates/medium`の部分的な設計関係です。旧ASI04の`detects`は、実行時の照合を悪意ある内容の検知と読み違えるため変更しました。[資料記録](../sources/README.md#spec-owasp-agentic-2026)と[移行台帳](MIGRATION.md#2026-10-04ai-004のowasp-agentic-top-10関係を再照合)に根拠と限界を記録しました。

全92件のうち91件を設計関係としてレビュー済み、1件を再レビュー待ちとしました。AI-004の旧15関係の再照合はここまでで完了。実環境のtool・権限・拡張・code実行の強制は未確認で、新しい実装・テストコードは追加していません。

<a id="structure-review--2026-10-04ai-004のatlas関係"></a>
### 2026-10-04：AI-004のATLAS関係

固定版ATLASの旧6件を[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)と照合しました。Toolの権限悪用、書込みtoolを使う漏えい、toolからの認証情報取得に関する3件を、対象特性を絞って残しました。旧`T0053`の検知・監査データ関係は実際の検知に結び付かず、`T0097`は攻撃分類の意味が旧記録と違うため外しました。[資料記録](../sources/README.md#spec-mitre-atlas-202605)と[移行台帳](MIGRATION.md#2026-10-04ai-004のatlas関係を再照合)に根拠と旧関係を残しました。

全92件のうち87件を設計関係としてレビュー済み、5件を再レビュー待ちとしました。実toolの拒否、漏えいの阻止、認証情報の保護、検知・通知は確認していません。新しい実装・テストコードは追加していません。

<a id="structure-review--2026-10-04ai-004のaisvs関係"></a>
### 2026-10-04：AI-004のAISVS関係

旧5件を固定版AISVSのC9・C10と[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)の特性へ照合しました。人による重要操作の承認、tool・pluginの隔離、toolと引数の認可、MCP serverの許可リストに関する4件を、`supports/medium`の部分的な設計関係として残しました。暗号学的に結び付けた承認を求めるC9.2.8は、現行controlが方式を限定しないため非継承としました。[資料記録](../sources/README.md#ref-development-runtime-reconciliation-001)と[移行台帳](MIGRATION.md#2026-10-04ai-004のaisvs関係を再照合)に判断を残しています。

全95件のうち84件を設計関係としてレビュー済み、11件を再レビュー待ちとしました。実環境の隔離・承認・拒否は確認していません。新しい実装・テストコードは追加していません。

<a id="structure-review--2026-10-04ai-002のframework関係"></a>
### 2026-10-04：AI-002のframework関係

[AI-002](../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md)の旧5関係を固定版のATLAS、OWASP ASI04、AISVS C10.1と照合しました。開発用agentの拡張を採用する前の確認に合う4件だけを、対象特性を絞った設計関係として残しました。AISVSの旧`verifies/high`は実検証を示さないため`supports/medium`へ変更。ATLASの「導入後にtoolが汚染される」攻撃は、このcontrolだけでは止められないので旧関係を外しました。[資料記録](../sources/README.md#spec-mitre-atlas-202605)と[移行台帳](MIGRATION.md#2026-10-04ai-002のframework関係を再照合)に根拠と旧関係を残しました。

全96件のうち80件を設計関係としてレビュー済み、16件を再レビュー待ちとしました。実際の拡張の導入・更新・失効・実行時拒否は確認していません。新しい実装・テストコードは追加していません。

<a id="structure-review--2026-10-04cicd-005のframework関係"></a>
### 2026-10-04：CICD-005のframework関係

旧5件をGitHubの固定版Secure use、pull_request_target、runner侵害、Actions設定とOSPS BR-01.03に照合しました。Secure useとPRイベント資料は未信頼コードの実行、別runの成果物、runner資産に関わる`PR-BOUNDARY-2・3・4`へ絞りました。Actions設定はfork workflowと既定token権限を見る`PR-BOUNDARY-2`だけ、OSPSも特権credentialと資産への到達防止という三特性だけに絞っています。Runner侵害の概説は被害を説明する資料であり、分離を強制する要件ではないため旧`mitigates`関係を非継承にしました。[資料記録](../sources/README.md#spec-github-security-guidance)と[移行台帳](MIGRATION.md)に判断を残しました。

全97件のうち76件を設計関係としてレビュー済み、21件を再レビュー待ちとしました。実GitHubでfork設定、job権限、runner隔離、成果物の受け渡しや拒否は確認していません。今回は既存文書と対応表の整理で完了し、新しい実装・テストコードは追加しません。

<a id="structure-review--2026-10-04cicd-006のframework関係"></a>
### 2026-10-04：CICD-006のframework関係

旧4件をGitHubの固定版OIDC資料、OSPS AC-04.02、ATT&CK T1552.001と照合しました。GitHubのOIDC参照は`FED-2・3`の受け入れ条件とtoken取得権限、OSPSは`FED-3`のjob権限だけに絞り、`supports/medium`の設計関係へ変更しました。OIDC概説は仕組みの説明なので、独立したframework関係には残しません。旧鍵の停止はファイル内の認証情報の発見・除去を必須としないため、ATT&CKとの旧関係も非継承です。[資料記録](../sources/README.md#spec-workload-federation)、[現行mapping](../mappings/frameworks.yaml)、[移行台帳](MIGRATION.md)に判断を残しました。

全98件のうち72件を設計関係としてレビュー済み、26件を再レビュー待ちとしました。Tokenの発行・交換、拒否、cloud操作、旧鍵と派生sessionの停止は実環境で確認していません。今回は文書とmappingの整理で完了し、新しい実装やテストコードは追加しません。

<a id="structure-review--2026-10-04cicd-009のframework関係"></a>
### 2026-10-04：CICD-009のframework関係

[Cache trust boundary](../controls/records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md)の旧三関係を再照合し、SITF T-C007とOSPS BR-01.03だけを部分的な設計関係として残しました。SITFは共有cache汚染への防御経路に絞り、旧`mitigates/high`を`mitigates/medium`へ変更。GitHub Secure useはcache固有の仕様を指定しないため旧`supports/high`を非継承にし、製品挙動は[cache仕様記録](../sources/README.md#spec-ci-cache-boundary)へ分けました。[Mapping](../mappings/frameworks.yaml)と[移行台帳](MIGRATION.md)に範囲と理由を記録しました。全100関係のうち70件が設計関係のレビュー済み、30件が再レビュー待ちです。実GitHubのcache拒否・復元・内容照合は未確認で、新しい実装・テストコードは追加していません。

<a id="structure-review--2026-10-04cicd-007のframework関係"></a>
### 2026-10-04：CICD-007のframework関係

[Runner lifecycle isolation](../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md)の旧六関係を再照合し、GitHub Secure use、OSPS BR-01.03、ATT&CK T1552.005の三件だけを部分的な設計関係として残しました。旧GitHub `verifies/high`は`supports/medium`、ATT&CK `mitigates/high`は`mitigates/medium`へ絞っています。GitHubの侵害時解説、SSDF PW.6.1、ATT&CK T1133は非継承です。[現行mapping](../mappings/frameworks.yaml)と[移行台帳](MIGRATION.md)、[資料記録](../sources/README.md#ref-cicd-014)に理由と限界を記録しました。全101関係のうち68件が設計関係のレビュー済み、33件が再レビュー待ちです。実runnerの割当・破棄・ログ配送・metadata到達拒否は未確認で、新しい実装やテストコードは追加していません。

<a id="structure-review--2026-10-04rel-003の限定実装を手元から試す"></a>
### 2026-10-04：REL-003の限定実装を手元から試す

[CycloneDX artifact binding例](../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)を使い捨てGit repositoryへcopyし、同梱SBOMとの一致`0`、artifact変更の拒否`1`、artifact欠落の評価不能`2`、copyの解除を確認しました。Python 3.13.5で既存9テストも通過しました。導入先の`tools`・`tools/sbom`がsymlinkならcopyを止める条件と、手元の試行を解除する短い手順をREADMEへ追加しました。使い捨て対象でsymlink時の停止と通常copyも確認しています。[REL-003のcontrol](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)・教材・patternの主張とは整合し、実装は文書内のphaseとhashを照合するだけです。SBOMを実際に完成物から生成した証拠、coverage、公開、分析、稼働先との対応は得ていません。新しいadapterやテストコードは追加していません。

<a id="structure-review--2026-10-03source-002の実装例を手元から試す"></a>
### 2026-10-03：SOURCE-002の実装例を手元から試す

[Git hooksとGitleaks](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)と[Python pattern scanner](../engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner/README.md)の導入・smoke test・解除を読み合わせました。Python版は使い捨てGit repositoryへ配置し、正常commit、無効canaryの拒否、scanner欠落時の停止、設定解除を確認しました。検査不能なNUL入りファイルと5 MiB超のファイルが以前はfindingと同じ終了値`1`になっていたため、`ERROR/2`へ分離し、READMEのsmokeにもその経路を追加しました。実際のGit操作はhookの終了値`2`をそのまま返すとは限らず、検査不能時にcommitが止まることを観測しました。[SOURCE-002 control](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md)と[pattern](../engineering/source-protection/secret-checks-before-publication/README.md)は検出・検査不能の区別を既に要求しており、今回の実装挙動をそこへ揃えました。8件のPython版テストは通過しています。Gitleaks版は固定配布物と手元binaryのhashが一致しないため、実Gitleaksによる試験は行っていません。組織のrepository、受信側、全書込み経路での強制は未確認です。

<a id="structure-review--2026-10-03開発者の設計実装入口"></a>
### 2026-10-03：開発者の設計・実装入口

[Engineering索引](../engineering/README.md)の47 patternから、対応control・教材・Sourcesへの道筋を点検しました。Controlは各patternから辿れ、46 controlの教材はcontrol配下から読めます。GOV-004には教材がありませんが、control本文に具体的な漏えい後のシナリオがあり、本文を複製した教材は作りません。SOURCE-003 patternだけSourcesへの直接リンクがなかったため、参照資料記録を結びました。索引の末尾にあった読む順序を冒頭へ移し、実装例があるSOURCE-002と文書で完了するBUILD-002を例に、実装例の有無を導入済み状態と混同しない案内を加えました。Object access boundaryの索引上のdomainも主配置のSecure Designへ揃えました。リンクと文書上の導線の確認であり、実装の動作や利用者の読書評価は未確認です。実装例・テストコード・mappingは増やしていません。

<a id="structure-review--2026-10-03依存の採用から使用許可までの読者導線"></a>
### 2026-10-03：依存の採用から使用許可までの読者導線

依存の変更判断からbuild中の実行、成果物と来歴の生成・配布、consumer受入、containerの使用許可まで、関係するcontrolの境界と教材・設計patternへの導線を確認しました。個々の境界は説明されていましたが、11 domainの一覧から順に辿る案内と、BUILD-003からREL-002、REL-001からCONTAINER-001への直接リンクが不足していました。[control一覧の読む順序](../controls/README.md#依存の変更から成果物の使用まで読む)と当該リンクを補修しました。署名生成は要求する場合、admissionはcontainer imageの場合に限って案内しています。文書内の受け渡しを確認した範囲であり、実際の依存取得・build・公開・検証・使用拒否は未確認です。新しい実装・mapping・テストコードは追加していません。

<a id="structure-review--2026-10-03build-001のframework関係"></a>
### 2026-10-03：BUILD-001のframework関係

SLSA Build L3の隔離とOSPS BR-01.03の特権CI/CD資産へのアクセス防止を、BUILD-001の該当特性へ絞った部分的な設計関係として残しました。旧OSPS `verifies/high`は`supports/medium`へ改め、SSDF PW.6.1はcompiler・build toolの機能・保守という別の対象のため非継承です。[資料記録](../sources/README.md#spec-build-containment)、[mapping](../mappings/frameworks.yaml)、[移行台帳](MIGRATION.md)へ採否と限界を記録しました。全104関係のうち65件が設計関係のレビュー済み、39件が再レビュー待ちです。実際の隔離、拒否、SLSA level・OSPS適合は未確認。新しい実装やテストコードは追加しません。

<a id="structure-review--2026-10-03rel-001のframework関係"></a>
### 2026-10-03：REL-001のframework関係

SLSA v1.2のBuild L2利用者側の来歴認証とBuild Provenanceの項目照合だけを、REL-001の`ACCEPT-1・2・3`との部分的な設計関係として残しました。旧`verifies/high`を`supports/medium`に改め、使用時の実検証やBuild L2達成を主張しません。SSDF PS.2.1とOSPS BR-06.01は検証情報の提供・releaseの署名という作り手側の成果のため、利用者側のREL-001からは非継承にしました。[資料記録](../sources/README.md#spec-consumer-artifact-verification)、[mapping](../mappings/frameworks.yaml)、[移行台帳](MIGRATION.md)に理由と限界を記録しました。全105関係のうち63件が設計関係のレビュー済み、42件が再レビュー待ちです。新しい実装やテストコードは追加しません。

<a id="structure-review--2026-10-03gov-002のframework関係"></a>
### 2026-10-03：GOV-002のframework関係

SSDF RV.2.1の脆弱性分析とGOV-002の共通例外lifecycleは対象成果が異なるため、旧関係を非継承としました。SSDF PW.1.2の承認済み例外記録・見直しへ、`EXCEPTION-3・4`の部分的な設計関係を新しく記録しています。OSPS QA-03.01の主ブランチ受入とmanual bypassはGOV-002だけでは強制できないため非継承です。[資料記録](../sources/README.md#ref-security-exception-lifecycle-001)、[mapping](../mappings/frameworks.yaml)、[移行台帳](MIGRATION.md)に採否と限界を残しました。全107関係のうち61件が設計関係のレビュー済み、46件が再レビュー待ちです。新規実装・テストコードは追加していません。

<a id="structure-review--2026-10-03gov-001のframework関係"></a>
### 2026-10-03：GOV-001のframework関係

SSDF RV.1.1の報告後の製品影響調査とRV.2.1の対応計画に必要な適用性情報を、GOV-001の部分的な設計関係として残しました。旧ATT&CK T1195.001の`detects`は、既知版の利用先特定を攻撃行動の検知と取り違えるため非継承です。[資料記録](../sources/README.md#ref-supply-chain-impact-001)、[現行mapping](../mappings/frameworks.yaml)、[移行台帳](MIGRATION.md)に範囲と理由を記録しました。全108関係のうち60件が設計関係のレビュー済み、48件が再レビュー待ちです。実inventory・稼働先の網羅性と対応実施は未確認で、新しい実装やテストコードは追加しません。

<a id="structure-review--2026-10-03detect-001のframework関係"></a>
### 2026-10-03：DETECT-001のframework関係

NIST SP 800-190 §4.1.1のイメージ脆弱性検査に必要な証拠の範囲と状態だけを、DETECT-001の`SCAN-2・3・4`に対する`design-reviewed`の部分関係として残しました。旧SSDF RV.1.1・PW.4.1、OSPS VM-06.02、NIST SP 800-190 §4.4.1は、継続収集・調査、第三者部品の採用、全変更の自動拒否、稼働中ランタイムの監視をDETECT-001自身が要求しないため非継承です。[資料記録](../sources/README.md#ref-scanner-evidence-001)と[移行台帳](MIGRATION.md)に理由を記録しました。全109関係のうち58件が設計関係のレビュー済み、51件が再レビュー待ちです。実scannerと受入gateは未確認で、新しい実装やテストコードは追加しません。

<a id="structure-review--2026-10-03deps-004のframework関係"></a>
### 2026-10-03：DEPS-004のframework関係

OSPS VM-05.03のうち変更依存の既知脆弱性gateと、SSDF PW.4.1の採用レビューへ絞った二関係を`design-reviewed`にしました。OSPS VM-05.01のライセンスを含む是正閾値、VM-05.02のrelease前対応、ATT&CK T1195.001の悪意ある依存・開発ツール改変は、現行DEPS-004の必須特性からは説明できず非継承です。[資料記録](../sources/README.md#ref-deps-002)、[mapping](../mappings/frameworks.yaml)、[移行台帳](MIGRATION.md)に採否と限界を記録しました。全113関係のうち57件が設計関係のレビュー済み、56件が再レビュー待ちです。実環境のmerge拒否、悪意ある依存の検知、準拠は未確認です。必要な成果物は既存文書の補修で、新しい実装やテストコードは追加しません。

<a id="structure-review--2026-10-03deps-003のframework関係"></a>
### 2026-10-03：DEPS-003のframework関係

旧ATT&CK T1195.001の`high`は、承認済み依存から未レビューの内容へずれる経路に限る`medium`の部分関係へ改めました。NIST SSDFの旧PW.4.1は継承せず、取得した部品の完全性確認を例示するPW.4.4の一部へ新しく対応付けました。OSPS BR-05.01の標準ツール使用はDEPS-003の特性が要求しないため、旧関係を外しました。根拠と限界は[資料記録](../sources/README.md#spec-dependency-lock-identity)と[現行mapping](../mappings/frameworks.yaml)、非継承理由は[移行台帳](MIGRATION.md)へ記録しています。全116関係のうち55件が設計関係のレビュー済み、61件が再レビュー待ちです。実際の通常build・取得物照合は確認していません。必要な成果物は既存mapping・control案内・資料記録の補修で、新しい実装やテストコードは追加しません。

<a id="structure-review--2026-10-02deps-002のframework関係"></a>
### 2026-10-02：DEPS-002のframework関係

ATT&CK T1195.001のうち、悪意ある依存の準備時コードを実行する経路に対して、DEPS-002の既定拒否・対象を絞った承認・迂回と評価失敗の扱いを照合しました。脅威技法全体の緩和ではないため旧`high`を`medium`へ下げ、部分的な設計関係としました。NIST SSDF PW.4.1は部品の取得・評価・維持を求め、準備処理の実行可否そのものを示す要件ではありません。旧関係は現行mappingから外し、理由を[移行台帳](MIGRATION.md)へ記録しました。実際のinstall拒否や組織導入の確認は行っていません。必要な成果物は既存mapping・control案内・資料記録の補修だけで、新しい実装やテストコードは追加しません。

<a id="structure-review--2026-10-01deps-001のframework関係"></a>
### 2026-10-01：DEPS-001のframework関係

MITRE ATT&CK v19のT1195.001とNIST SP 800-218最終版のPW.4.1を、DEPS-001の特性へ照合しました。待機期間が扱うのは新しく公開された依存版の早期採用であり、ATT&CKの開発ツール侵害や古い悪意ある版には対応しません。SSDFは第三者部品の取得・維持を求めますが、公開後の待機時間は指定しません。両者とも部分的な設計関係として`design-reviewed`へ進め、例外管理のDEP-AGE-6を対象propertyから外しました。残るreview待ちは66件です。実際の依存解決、インストール前の拒否、SSDF準拠は未確認です。必要な成果物は既存mapping・control案内・資料記録の補修であり、新たな実装やテストコードは追加しません。

根拠の版と採否は[資料記録](../sources/README.md#ref-deps-004)へ、propertyごとの範囲は[framework mapping](../mappings/frameworks.yaml)へ記録しています。

<a id="structure-review--framework-mapping-review"></a>

<a id="structure-review--2026-10-01framework-mappingの状態と実証表現"></a>
### 2026-10-01：Framework mappingの状態と実証表現

`frameworks.yaml`の118関係は、資料と現在のcontrol特性を照合した`design-reviewed`が50件、旧関係の再レビュー待ちが68件でした。後者の`relationship: verifies`や`confidence: high`は過去の判断を保持した値で、現在の要件検証や導入結果ではありません。その読み方を機械可読のpolicyとmappingの入口へ明記しました。

旧`verifies/high`の14件を確認し、Release・Buildの説明に残る「直接実装」「policy testで検証」を設計の説明へ直しました。AI拡張の二行も、出所・完全性・実行時許可を確認済みとする語を外しました。14件すべてに未確認範囲が分かる`limitation`があります。`design-reviewed`のCONTAINER-004は、既存のNIST SP 800-190 §4.4.4照合記録に沿って部分関係の範囲・限界を追記しました。今回の補修は新たな規範資料のレビュー、準拠判定、実環境のテストではありません。

確認結果：118件のproperty参照はすべて現行controlに解決し、50件の`design-reviewed`にはレビュー範囲・限界、14件の旧`verifies/high`には限界があります。`make test`で2698件のローカルリンク、47 control ID、文書検査4件はエラー0件。`git diff --check`も成功しました。

<a id="structure-review--2026-10-01成果物間mappingと限定実装の境界"></a>
### 2026-10-01：成果物間mappingと限定実装の境界

`pilot.yaml`のpattern→controlと実装例→patternの関係を点検しました。既存の19実装例のscope・rationaleには、未導入を明記したものが多い一方、SOURCE-002のGitleaks版とPython版は設計から辿る関係がありませんでした。両例を別々に結び、受信側を含むGit経路とローカルhookのみの経路、検出・書込み経路・例外の残る範囲を記録しました。

KubernetesのResourceQuota＋CEL例は`RESOURCE-1〜4・7`の全特性を満たすように読めるscopeと、live API拒否を確認済みと読める説明を持っていました。各特性のうちnamespace quota・admissionで示せる部分に限定し、live clusterでは未実行としました。Mappingの入口でも`implements`は設計上の関係、`realizes`は具体化した部分との関係であり、controlの合格や導入証拠ではないと明記しました。必要な成果物はmappingと読み方の補修で、新しい実装・テストコードは追加しません。

確認結果：`pilot.yaml`の72関係（設計51、実装例21）の参照先・重複・control特性IDを確認。`make test`で2698件のローカルリンク、47 control ID、文書検査4件はエラー0件。`git diff --check`も成功しました。

<a id="structure-review--2026-10-01設計patternと実装例の横断mapping"></a>
### 2026-10-01：設計patternと実装例の横断mapping

横断mappingに収録した33設計patternと6実装例の関係一覧・制限を点検しました。Build、Release、IaC、AI Developmentの設計で、前段からsource・artifact・権限条件を受け取るだけの関係を`handoff`としていた12箇所を`adjacent`へ直しました。対応・復旧からclean buildや権限の停止を前段の実行系へ戻す関係は、実際に判断を渡すため`handoff`のままです。六つの実装例は対象と未確認事項を本文と照合し、対応範囲を広げる変更はしませんでした。

関係の意味を横断分析とmappingの入口に明記しました。これらは導入・強制の証拠ではありません。全pattern本文の詳細な妥当性、実装例のlive動作、収録していないpatternの追加要否は未確認です。必要な成果物はmappingとその読み方の補修で、新しい実装・テストコードは追加しません。

確認結果：`make test`で2698件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。YAMLの86成果物のID重複・参照先欠落・横断資料IDの混入はなく、`git diff --check`も成功しました。

<a id="structure-review--2026-10-01横断mappingとcontrolの対応"></a>
### 2026-10-01：横断mappingとcontrolの対応

横断mappingの86成果物と47 control記録を読み込み、各controlに明記された主レイヤー・直接段階・引き渡し段階を照合しました。SOURCE-003は公開候補を探し所有者が判断するところまでが直接の責任で、インシデント対応は引き渡しです。CICD-007のrelease段階とCICD-009の対応段階には、本文に独立した受け渡しを定義していなかったため、control記録から外しました。十二段階の表は代表的な直接対応を補い、CONTAINER-005の稼働時観測への引き渡しを明示しました。

`REF-PORTFOLIO-001`と`LOCAL-SUPPLY-CHAIN-ATTACK-STAGES`はmappingの分析軸にのみ置かれ、成果物別の`source_refs`には混在していません。構造的な照合で明示された段階関係の食い違いは0件です。残るpattern・実装例の関係を含めた意味的妥当性、組織導入、実環境の強制は確認していません。必要な成果物はcontrol記録と横断分析の補修であり、新しい実装例・テストコードは追加しません。

確認結果：`make test`で2698件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

<a id="structure-review--2026-10-01横断分析と入口の状態表記"></a>
### 2026-10-01：横断分析と入口の状態表記

READMEとcontrol・engineeringの入口を、Sourceから復旧までの横断分析と照合しました。READMEに残っていた初期pilot中心の対象・制限事項を現在の使い方と移行記録への案内にまとめました。横断分析では、署名境界の完了をrelease全体の完了と誤読させる表現、CONTAINER-002移行後もregistry publicationが未実装と読める表現、移行済みのworkflow権限を「次の主題」とする表現を補修しました。十二段階の表でもSOURCE-006、CODE-005、CICD-004などの既存成果物と、GOV-002の隣接関係を見えるようにしました。

必要な成果物は入口と横断分析の補修です。新しいcontrol、実装例、テストコードは追加しません。組織への導入、実環境での強制・復旧、機械可読mapping全件と本文の意味的な一致は未確認です。次はそのmappingを確認します。

確認結果：`make test`で2698件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

<a id="structure-review--2026-10-01稼働観測から復旧完了への受け渡し"></a>
### 2026-10-01：稼働観測から復旧完了への受け渡し

GOV-001からGOV-005へ渡す元の調査範囲、CONTAINER-001の使用許可、CONTAINER-004のruntime検知を読み合わせました。検知アラートの不在、rollout成功、desired stateの新digestは旧digestの非稼働を示しません。GOV-005のcontrol・機械可読記録・教材・patternに、元のtargetごとの実稼働digest、観測時刻・収集範囲、停止・切り戻し経路の確認を明記しました。対象の一部を廃止する場合は、新digestを配置したとみなさず、実体の停止・削除と再起動経路を確認します。

必要な成果物は既存文書の補修と診断項目です。新しいcollector、verifier、テストコードは追加しません。判断の根拠と旧成果物との関係は[資料記録](../sources/README.md#ref-deployed-artifact-recovery-001)と[移行記録](MIGRATION_GOVERNANCE_OPERATIONS.md#deployed-artifact-recovery-migration--2026-10-01の横断レビュー)へ残しました。Live inventory、再投入拒否、復旧完了は未確認です。

確認結果：`make test`で2707件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。GOV-005の機械可読記録の読取りと`git diff --check`も成功しました。

<a id="structure-review--2026-10-01releaseから使用許可稼働観測への受け渡し"></a>
### 2026-10-01：Releaseから使用許可・稼働観測への受け渡し

Release IntegrityとCONTAINER-001・002の既存control・教材・設計を読み合わせました。個別の本文では区別できていた「registryに公開・保持した」「admissionで使用を許した」「runtimeで実際に稼働した」を、両分野の入口から順に辿れるようにしました。Admission patternでも`ALLOW`を稼働証拠へ置き換えず、後段のdigest観測へ渡すと明記しました。旧digestの非稼働と復旧完了はGOV-005の判断です。

必要な成果物は既存の入口とpatternの補修です。採用するregistry・cluster・runtime collectorが未定のため新しい実装例やテストコードは追加しません。実registryの公開・状態、admissionの拒否、runtimeのdigest対応、旧digestの非稼働は未確認です。

確認結果：`make test`で2701件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

<a id="structure-review--2026-10-01cicdからrelease-integrityへの受け渡し"></a>
### 2026-10-01：CI/CDからRelease Integrityへの受け渡し

CIのPR境界・job権限・cloud交換から、BUILD-002・003とRelease Integrity五controlへ渡す内容を読み合わせました。CIの検査成功や権限取得だけでは公開対象のbytesや承認内容が決まらないこと、署名・来歴配布・SBOM公開は必要な条件ごとに確認し、一つの成功をrelease全体の完了へ変換しないことをRelease分野の入口へ示しました。五controlから教材と設計patternへ直接辿れるようにもしました。

署名patternの図と説明では、`SIGNED_AND_AVAILABLE`を署名境界の結果として明示しました。今回の成果物は既存文書の補修で、新しい実装例・テストコードは作りません。実公開・配布、利用者側の検証・使用拒否、稼働中のdigestとの対応は未確認です。

確認結果：`make test`で2694件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

<a id="structure-review--2026-09-30cicd-006の診断項目"></a>
### 2026-09-30：CICD-006の診断項目

CI/CD Securityの検査結果、job権限、PR境界、runner・cacheと、cloudへの権限交換の役割を読み合わせました。CICD-006は要件・教材・設計に交換条件と操作権限の違いがありましたが、control本文から直接使える診断項目がありませんでした。そこで、別issuer・audience・workload文脈の拒否、未信頼状態からのtoken取得、交換後の不要操作、旧key・派生session、確認不足を分けて列挙しました。

必要な成果物は既存control・pattern・資料記録の補修です。製品共通の診断チェックリストで判断できるため、新しい実装例・テストコードは追加しません。[GitHubとAWSの公式資料](../sources/README.md#spec-workload-federation)でtokenのclaimと受け入れ先の実際の条件を区別しました。実trust、交換、操作拒否、旧keyの失効は未確認です。

確認結果：`make test`で2684件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

<a id="structure-review--2026-09-30cicd-securityの横断レビュー"></a>
### 2026-09-30：CI/CD Securityの横断レビュー

七つのcontrolの入口と設計への導線を照合し、各controlから対応するpatternをたどれるようにしました。特にCICD-005のGitHub例では、`main`へのpushで新しいrunを始め、SHAを照合しても、その変更がレビュー済みとは言えません。そこでworkflowの名称・marker、controlの診断項目と判定例、patternと導入手順に、branch保護・rulesetの対象、直接push、bypassを確かめる判断を加えました。[GitHub公式資料](../sources/README.md#spec-github-security-guidance)の可変Web版を2026-09-30に確認しています。

必要な成果物は既存文書とGitHub例の補修です。新しい実装例やテストコードは作りません。Review経路とbypassの実効設定、直接push拒否、実runは未確認です。設定例のmarkerは権限操作をしないため、実環境での権限処理の安全性も未確認です。

確認結果：`make test`で2681件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。GitHub例のYAML読取りと`git diff --check`も成功しました。

<a id="structure-review--2026-09-30source-protectionの横断レビュー"></a>
### 2026-09-30：Source Protectionの横断レビュー

六つのcontrolの入口、各教材、設計pattern、限定実装への導線を照合しました。分野READMEは六つの教材を列挙しながら「読み進め方」がSOURCE-004だけの順路だったため、各controlに設計への直接リンクを置き、端末・権限、公開前検査・公開後の観測、復旧の三つの読み筋へ整理しました。Engineering索引でも六つのpatternを一箇所にまとめ、一覧名を現在の収録範囲へ揃えました。

横断分析に残っていた「SOURCE-003にはprovider実装がない」「SOURCE-002はガイダンスのみ」という古い制限表記を、限定実装の存在とlive導入未確認の区別へ直しました。新しいcontrol・実装・テストコードは追加していません。これは導線と状態表記の執筆者レビューであり、実組織への導入や利用者による読書評価ではありません。

確認結果：`make test`で2674件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。横断分析YAMLの読取りと`git diff --check`も成功しました。

<a id="structure-review--2026-09-30source-002003の読み合わせ"></a>
### 2026-09-30：SOURCE-002・003の読み合わせ

既存control・教材・pattern、GitHubの公開情報監視例を照合しました。実際の認証情報が共有先へ届いたと分かっている事象は、非公開リポジトリでも所有者に渡し、到達範囲・失効・利用履歴を判断します。受信側の拒否は送信前の拒否と異なります。SOURCE-003の公開検索は既知経路外の候補や追加のcopyを探すもので、再発見まで対応を待たせないよう文書を補修しました。[Gitの受信側仕様とGitHub資料](../sources/README.md#ref-secret-publication-001)を再確認し、この受け渡しは本PJの解釈として記録しています。

新しい実装・テストコードは追加していません。実GitHubの受信・検索、認証情報の失効、通知と対応は未確認です。具体化と導入の残りは[計画](MIGRATION_PLAN.md#source-002003の読み合わせと具体化判断)を参照してください。

確認結果：`make test`で2677件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

<a id="structure-review--2026-09-30source-005の読み合わせ"></a>
### 2026-09-30：SOURCE-005の読み合わせ

既存control・教材・pattern・Git mirror例を照合しました。取得前に不正変更された世代は、Git objectの整合性と取得時のref一覧との比較に成功し得ます。そこで、復旧する世代の選択をGitの復元成否から分け、変更の経緯、承認済みの変更記録、以前の世代で判断する流れを診断項目・教材・設計・実装説明へ補いました。判断できない場合は復旧完了にしません。[NIST SP 800-61 Rev.3](../sources/README.md#ref-repository-recovery-001)の復旧用資産と復元後の資産を確認する考え方を参照しました。具体的なGitの選び方は本PJの解釈です。

新しい実装・テストコードは追加していません。七つのローカルGit試験は整合性と復元経路の確認で、侵害前の世代選択や実組織での開発再開の証拠ではありません。残る実評価は[具体化判断](MIGRATION_PLAN.md#source-005の具体化判断)を参照してください。

確認結果：`make test`で2668件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`make test-repository-recovery`の実Git試験7件、SOURCE-005の機械可読記録のJSON読取り、`git diff --check`も成功しました。

<a id="structure-review--2026-09-30source-006の読み合わせ"></a>
### 2026-09-30：SOURCE-006の読み合わせ

既存control・教材・pattern・GitHub手順を照合しました。組織のApp申請・インストール制限、OAuth Appの承認、PATの有効期間方針は、既存の認可を同じ方法で失効させません。方針変更後の現在のgrantと実効アクセスを確認し、不要なものはSOURCE-004の失効判断へ渡すよう、診断項目・教材・設計・GitHub手順を補修しました。GitHub公式のApp、OAuth、organizationのPAT方針の現行Web本文を[Sources](../sources/README.md#spec-github-organization-posture)へ追記しました。

新しいcontrol・教材・実装・テストコードは増やしていません。実組織での方針変更、既存token・App、拒否、通知は未確認です。実導入と確認の残りは[具体化判断](MIGRATION_PLAN.md#source-006の具体化判断)を参照してください。

確認結果：`make test`で2665件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。GitHubの実組織は操作していません。

<a id="structure-review--2026-09-30source-004の読み合わせ"></a>
### 2026-09-30：SOURCE-004の読み合わせ

端末状態の悪化から失効を求めるとき、元のトークンを止めるだけでは、既存セッションや別に発行した鍵・アプリ権限が残り得ます。Controlに診断項目を設け、教材・pattern・GitHub実装案へ失効単位と拒否確認を戻しました。[GitHub Enterprise CloudのSAML管理](https://docs.github.com/en/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization)、[fine-grained PATの失効](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-programmatic-access-to-your-organization/reviewing-and-revoking-personal-access-tokens-in-your-organization)、[認可取消と認証情報削除](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/respond-to-incidents/revoke-authorizations-or-tokens)の可変文書を照合しています。

これらは製品固有の失効範囲を示す資料であり、組織への導入や実際の拒否を示しません。今回の成果物は文書と診断項目で、追加のコードやテストはありません。旧framework mappingは再割当せず、[具体化判断](MIGRATION_PLAN.md#source-004の読み合わせと具体化判断)に限界を記録します。

確認結果：`make test`で2661件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。SOURCE-004のYAML読取りと`git diff --check`も成功しました。GitHubの実組織やテスト用認証情報は操作していません。

<a id="structure-review--2026-09-30source-001の読み合わせ"></a>
### 2026-09-30：SOURCE-001の読み合わせ

登録と現在の観測が分かれていても、端末状態の悪化を資産側の既存セッションへ反映できなければアクセス制限になりません。既存control・教材・patternへ、新規ログインと継続中の接続で再評価時点を分け、反映までの時間と残る権限を確認する判断を補いました。旧Linux adapterはローカル設定の一部を読むものの、MDM・通知・資産側の失効は観測しません。

[NIST SP 800-207 §3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf)の端末状態を用いたアクセス判断と接続終了の役割を設計入力にしました。資産別の再評価時点と許容時間は本PJの解釈です。新しい実装例・テストコードは追加せず、実MDM・端末・ソース管理・遠隔開発環境の連携は未確認です。[具体化判断](MIGRATION_PLAN.md#source-001の読み合わせと具体化判断)に範囲を記録します。

確認結果：`make test`で2654件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。SOURCE-001のYAML読取りと`git diff --check`も成功しました。実端末・実セッションは操作していません。

<a id="structure-review--2026-09-29detect-001の読み合わせ"></a>
### 2026-09-29：DETECT-001の読み合わせ

既存control・機械可読記録・教材・patternを照合しました。予定した対象の一部で指摘が出て別の対象が解析不能な場合、`FINDING`だけでは完了を誤認させ、`ERROR`だけでは既知の指摘を失います。全体は`ERROR`として受入を止め、指摘を別に保持して調査へ渡す判断を補いました。`CLEAN`／`FINDING`の集約も対象と検出カテゴリが完了した範囲に限定します。

[zizmor公式Usage](https://docs.zizmor.sh/usage/)でSARIF時の終了状態と部分的な解析失敗の説明を再確認しました。この集約判断は本PJの解釈であり、旧製品版やTrivy・DockSecの現行挙動を確認した意味ではありません。新しい実装例・テストコードは追加していません。完了条件と未確認範囲は[具体化判断](MIGRATION_PLAN.md#detect-001の読み合わせと具体化判断)に記録します。

確認結果：`make test`で2649件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。実scannerとCI受入は未確認です。

<a id="structure-review--2026-09-29detect-003の読み合わせ"></a>
### 2026-09-29：DETECT-003の読み合わせ

旧Python verifierは入力済みの候補と台帳を照合し、是正済み候補の再出現を判定しますが、外部collector、台帳の正しさ、通知先の受領を観測しません。既存control・教材・patternに、部分取得で新たに見えた候補は調査し、見えなかった既存候補は保持する判断を補いました。台帳や収集pageの取得不足を全件一致や是正完了へ変換しません。

[NIST CSF 2.0](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final)の公開ページと[CISA BOD 23-01](https://www.cisa.gov/news-events/directives/bod-23-01-improving-asset-visibility-and-vulnerability-detection-federal-networks)の公開検索本文を確認しました。後者の直接取得は403でした。状態遷移は資料からの引用要件ではなく、本PJの設計判断です。新規実装・テストコードは追加していません。完了条件と未確認の実環境は[具体化判断](MIGRATION_PLAN.md#detect-003の読み合わせと具体化判断)に記録します。

確認結果：`make test`で2643件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。実APIと台帳の照合は行っていません。

<a id="structure-review--2026-09-29design-001の読み合わせ"></a>
### 2026-09-29：DESIGN-001の読み合わせ

請求書の単体read／updateを起点に、認証された主体と対象データへの権限を分けました。Python／SQLite実装はowner・tenant付きqueryを行いますが、`Principal`の生成元、HTTP、全endpoint、並行処理は実装外です。実装READMEの古い`experiments/next-repository` pathを直し、手元の使い捨てrepositoryへコピーして試す手順と解除を追加しました。

ASVS 5.0.0固定版V8.2.1・V8.2.2とcontrol特性を照合し、二件の部分的な設計関係を追加しました。Field別権限、信頼できるservice層、全tenant操作の要件にまで拡張しません。完了条件と未確認範囲は[具体化判断](MIGRATION_PLAN.md#design-001の読み合わせと具体化判断)に記録しています。

確認結果：Python 3.10.4で既存7件の実装testと、使い捨てrepositoryへのコピー後の同じ7件を確認しました。`make test`で2637件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。Framework mappingはYAMLとして読め、118件です。`git diff --check`も成功しました。

<a id="structure-review--2026-09-29code-005の読み合わせ"></a>
### 2026-09-29：CODE-005の読み合わせ

UTS #55固定版のline break spoofingとPython 3.10の物理行・コメントの字句規則を照合しました。既存Python例は、U+000B、U+000C、U+0085、U+2028、U+2029を含むコメントを`PASS`にしていたため、`display-line-break`として報告するよう修正しました。Control・教材・pattern・参照記録にも表示と処理系の改行差を戻し、Python限定profileを一般要件にはしません。

Review UIとprotected CIの採用先は未選定です。必要な成果物と完了条件は[具体化判断](MIGRATION_PLAN.md#code-005の読み合わせと具体化判断)に記録しました。

確認結果：Python 3.10.4と手元のPythonで実装test各13件が成功しました。`make test`で2632件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。YAMLの読取りと`git diff --check`も成功しました。実repositoryのmerge拒否は未確認です。

<a id="structure-review--2026-09-29iac-001の読み合わせ"></a>
### 2026-09-29：IAC-001の読み合わせ

利用者提供のGolden Path原文、既存control・教材・patternと、Terraformのplan／apply・依存lock・refresh、OPAの公開資料を照合しました。Golden Pathを作業の入口、保存planに結び付いた承認を実行前の判断、apply結果とprovider inventoryを実状態の確認として分けています。保存planの指定だけでTerraform側の対話承認が不要になること、途中失敗も自動で元に戻らないことを補いました。

文書と診断項目を今回の成果物とし、実装例・テストコードは追加していません。対象provider・resource・plan store・cloud identityが未選定で、live apply、provider側の迂回拒否、driftは未確認です。[具体化判断](MIGRATION_PLAN.md#iac-001の読み合わせと具体化判断)に記録しました。

確認結果：`make test`で2626件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。実cloud操作は行っていません。

<a id="structure-review--2026-09-29container-005007の読み合わせ"></a>
### 2026-09-29：CONTAINER-005〜007の読み合わせ

Workload権限、通信、資源のcontrol・教材・patternと既存Kubernetes例を照合しました。CONTAINER-005の受付時policyを既存Podのruntime強制と混同せず、CONTAINER-006では拒否probeの宛先listenerも確認し、CONTAINER-007はcontainer単位budgetを選ぶtest profileと明記しました。Kubernetes 1.37で利用できるPod-level CPU・memory予算を、共通要件から除外したわけではありません。

三つの`verify.sh`で使い捨て対象の事前確認を揃え、既存のnamespace・cluster-scoped policy・binding、またはAPI errorによる確認不能を変更前に停止する条件にしました。新しい実装例・テストコードは追加していません。必要な成果物とlive clusterで未確認の範囲は[具体化判断](MIGRATION_PLAN.md#container-005007の読み合わせと具体化判断)に記録しています。

確認結果：`make test`で2621件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。三つのshell構文と`git diff --check`も成功しました。使い捨ての`kubectl` mockでは、三つのscriptすべてで既存対象・API errorのどちらも変更前に終了することを確認しました。Live clusterの受付拒否、通信、資源制限は未確認です。

<a id="structure-review--2026-09-28container-003004の読み合わせ"></a>
### 2026-09-28：CONTAINER-003・004の読み合わせ

CONTAINER-003のhost・node管理面とCONTAINER-004のruntime検知を照合しました。侵害が疑われるnode上のsensorによる「異常なし」は独立した健全性証拠にせず、node外の受信記録や管理面の状態と照合する条件を加えました。CONTAINER-004には診断項目を追加し、eventの対象ID欠落、sensor・配送障害、担当者の受領、無承認の破壊的対応を確認できるようにしました。

機械可読記録の製品横断の過剰な前提を本文へ揃え、NIST SP 800-190 §4.4.4のmappingを部分関係へ縮小しました。Falco・Sysdigの現行公開資料で、event fieldと転送方式が設定・製品によって異なることを確認しています。必要な成果物と実環境で未確認の範囲は[具体化判断](MIGRATION_PLAN.md#container-003004の読み合わせと具体化判断)に記録しました。新規実装・テストコードはありません。

確認結果：`make test`で2612件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。Framework mappingはYAMLとして読み取れ、116件を保持しました。`git diff --check`も成功しました。Live node、sensor、配送、担当者の対応は未確認です。

<a id="structure-review--2026-09-28container-001002の読み合わせ"></a>
### 2026-09-28：CONTAINER-001・002の読み合わせ

両control・設計・旧移行記録を照合し、registryの公開・保持とadmissionの使用許可を分けました。`deprecated`を一律の拒否と読める箇所を修正し、使用停止を決めたartifactの状態をconsumerへ渡す条件を補いました。OCI image indexと選択manifestのdigestが別であることを[OCI Image Index v1.1.1](https://github.com/opencontainers/image-spec/blob/v1.1.1/image-index.md)で確認し、使用先との照合を明示しました。

[CONTAINER-001](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/learning.md)と[CONTAINER-002](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/learning.md)の教材をそれぞれの問いに分けて追加しました。GOV-005へ渡す新digestの公開、使用許可、稼働、旧digestの非稼働を区別しています。製品未選定の実装は追加していません。必要な成果物と未確認の範囲は[具体化判断](MIGRATION_PLAN.md#container-001002の読み合わせと具体化判断)に記録しています。

確認結果：`make check`で2594件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。Live registry、admission、runtimeは未確認です。

<a id="structure-review--2026-09-28gov-002005の読み合わせ"></a>
### 2026-09-28：GOV-002・005の読み合わせ

GOV-002のcontrol・機械可読記録・教材・設計と、GOV-005のcontrol・機械可読記録・設計を照合しました。旧YAML形式の必須化を外し、例外の対象・承認・期限・取消・評価不能という判断を残しています。GOV-005には別環境と切り戻し経路に旧digestが残る具体的な教材を追加し、GOV-003の元の期限、GOV-002の一時使用許可、GOV-005の復旧完了を区別しました。

GOV-003とGOV-005の例外consumer mappingを追加し、承認された例外でもfindingと旧digestの残存を消さない条件を明示しています。NIST SSDF 1.1・SP 800-61 Rev.3とOpenSSF Baseline 2026.02.19の公開ページを再確認しました。必要な成果物と実環境で未確認の範囲は[具体化判断](MIGRATION_PLAN.md#gov-002005の読み合わせと具体化判断)に記録しています。新規実装・テストコードはありません。

確認結果：`make check`で2563件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。例外の承認・取消、実際の使用拒否、置換後の旧digest非稼働は実環境で確認していません。

<a id="structure-review--2026-09-28gov-001003の読み合わせ"></a>
### 2026-09-28：GOV-001・003の読み合わせ

両control・設計とGOV-001の教材を照合し、GOV-003配下に具体的な場面から学ぶ教材を追加しました。問題の部品が見つかった製品と、閲覧権限や完成物の収集が不足する製品を分け、検索0件・取込通知・悪用情報の取得失敗を非該当や低優先度へ変換しない判断を示しました。GOV-001には診断項目を、GOV-003には再調査の担当・期限と暫定判断の条件を補いました。

GOV-001からGOV-003へ渡す対象・時点・根拠・不足情報を設計で明確にしました。FIRST CVSS v4.0仕様、NIST SSDF 1.1公開ページ、CISA管理のKEV配布mirrorを確認し、CISA本体catalogの内容・live取得は今回確認していません。必要な成果物と未確認の範囲は[具体化判断](MIGRATION_PLAN.md#gov-001003の読み合わせと具体化判断)に記録しています。新規実装・テストコードは追加していません。

確認結果：`make check`で2525件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。実環境での影響調査や優先度判断は行っていません。

<a id="structure-review--2026-09-28rel-003004の読み合わせ"></a>
### 2026-09-28：REL-003・004の読み合わせ

両control・既存教材・設計とCycloneDX限定実装を照合しました。REL-003の教材を「どこを調べて作ったSBOMか」から辿る説明へ改め、供給者や共通base imageのSBOMと最終製品の一覧の違いを補いました。利用者提供資料の固定原文、CycloneDXの生成段階、Dependency-Track 4.14.3の通知順を確認し、取込完了を脆弱性分析完了と扱わない設計へ修正しました。

実装READMEに最短導入手順、phaseの申告と実際の生成経路の違い、root・最上位componentに限る検査範囲を明記しました。既存9テストがPython 3.13.5で成功し、空白を含むパスへのコピー・正常例・上書き防止・配置先制限・成果物変更・入力不足を使い捨てrepositoryで確認しました。実装・テストコードは増やしていません。

旧check・framework関係は保持します。必要な成果物と実環境で未確認の範囲は[具体化判断](MIGRATION_PLAN.md#rel-003004の読み合わせと具体化判断)、資料の版と採否は[Sources](../sources/README.md#ref-release-sbom-lifecycle-001)に記録しています。

確認結果：`make check`で2493件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。実生成・公開・分析・供給者からの受入れは未確認です。

<a id="structure-review--2026-09-28rel-001002005の読み合わせ"></a>
### 2026-09-28：REL-001・002・005の読み合わせ

三つのcontrol・既存教材・設計を照合しました。REL-001に診断項目を追加し、機械可読記録へ本文の外部パラメーター照合、取得・検証不能時の使用停止を反映。来歴の種類の確認と、検証後も同じ内容を使用する判断を補いました。

REL-002の教材はWindows版の利用者から配布経路を辿る説明へ書き直し、用語の列挙と本文の重複を減らしました。公開準備中の表示と実際の取得・使用制限を分けています。REL-005からは成果物署名、来歴の認証、利用者の期待値の違いを辿れるようにしました。一次資料はSLSA v1.2の検証・配布と、Sigstoreの公式署名・検証文書を確認しました。

旧check・参照資料・framework関係は保持し、文書と診断項目で完了としました。必要な成果物と実環境で未確認の範囲は[具体化判断](MIGRATION_PLAN.md#rel-001002005の読み合わせと具体化判断)に記録しています。

確認結果：`make check`で2466件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。実signer・配布先・使用経路での拒否試験は行っていません。

<a id="structure-review--2026-09-28build-001003の読み合わせ"></a>
### 2026-09-28：BUILD-001〜003の読み合わせ

三つのcontrolと設計、既存二教材を照合しました。BUILD-001へ診断項目を追加し、機械可読記録のHTTPS固定・短い観測宣言を本文の特性へ揃えています。実行権限、承認手順、来歴情報の出所を分け、取得時に準備コードが動く境界も既存の依存実行設計へ接続しました。

BUILD-003には、正しい署名が付いていても記録の内容を誰が決めたか確認する教材を追加しました。基盤が入力を正確に記録することと、その入力での公開承認を区別し、domain入口・control・教材・設計を往復できるようにしています。SLSA v1.2の一次資料でL3のfield例外への参照を再照合し、以前の説明を補修しました。

今回は文書と診断項目を成果物に選び、製品未選定の実装や合成検証器は増やしていません。旧check・framework関係は保持します。必要な成果物と実環境で未確認の範囲は[具体化判断](MIGRATION_PLAN.md#build-001003の読み合わせと具体化判断)を参照してください。

確認結果：`make check`で2442件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。文書・記録の整合性検査であり、実基盤での生成・隔離・拒否試験は実行していません。

<a id="structure-review--2026-09-27cicd-005009007の読み合わせ"></a>
### 2026-09-27：CICD-005・009・007の読み合わせ

三つのcontrol・既存教材、Untrusted PR boundaryとCI state and runner lifecycle、既存GitHub例を読みました。未信頼の内容を権限処理へ渡す経路、外部cache、同じrunnerに残る状態を分け、controlへ診断項目、教材と設計へ隣接する問いへのリンクを追加しました。Cacheとrunnerの機械可読記録に残った製品固有の条件も本文へ揃えています。

Cacheの取得範囲・key一致・job成功は内容の正しさとは別であり、runner名・登録解除・破棄記録は実体の破棄とは別だと説明しました。登録・破棄・外部ログを世代で追い、取消・破棄失敗・ログ不足を成功へ丸めない設計へ戻しています。データの形式・出所が正しくても、PR runの自己申告を独立した検査や公開承認へ置き換えません。

既存GitHub例にはcacheを使わない設定、push SHAのcheckoutと一致確認、最短copy・smoke test・解除を補いました。文書・ローカルcopy・構文・実Gitのrevision照合と、実GitHubの拒否・実runnerの世代別破棄を区別します。新しいcontrol・教材・実装は増やしていません。必要な成果物と確認範囲は[具体化判断](MIGRATION_PLAN.md#cicd-005009007の読み合わせと具体化判断)、一次資料は[cache資料](../sources/README.md#spec-ci-cache-boundary)と[runner資料](../sources/README.md#ref-cicd-014)へ記録しました。

<a id="structure-review--2026-09-27deps-002004の読み合わせ"></a>
### 2026-09-27：DEPS-002〜004の読み合わせ

三つのcontrol・既存教材、Install execution policyとReviewed dependency intake、既存pip・GitHub例を読みました。更新の採用、依存内容の照合、準備コードの実行許可を別の問いとして渡す構成へ補修し、各controlへ製品非依存の診断項目を追加しています。新しいcontrol・教材・実装は増やしていません。

Lockを書き換えないこととmanifestとの一致、取得時のhash照合と既存の展開済み環境、Actionの成功と必要な評価の完了を教材で区別しました。pipは新しい専用環境を使う導入と解除、GitHubは配置・必須検査への接続・データ不足・smoke test・解除を整理しました。固定Actionのsnapshot警告が期限後も判定を止めないことを、sourceと配布コードで照合しています。

確認した一次資料と観測版は[Sources](../sources/README.md#spec-install-execution-policy)、必要な成果物とローカル確認・実導入の境界は[具体化判断](MIGRATION_PLAN.md#deps-002004の読み合わせと具体化判断)へ記録しました。npm・uvの実行、実GitHubの取得・必須判定・merge拒否、採用先の全依存・platform・CI配線は今回の確認に含みません。

<a id="structure-review--2026-09-27source-002003の読み合わせ"></a>
### 2026-09-27：SOURCE-002・003の読み合わせ

両control・patternと、Git / Gitleaks、Python pattern scanner、GitHub indicator watchの既存コード・READMEを読みました。検査場所の違いと検索後の判断を説明する教材を各controlへ置き、入口、機械可読記録、設計と実装から相互にたどれるようにしました。

SOURCE-002の未検証という表記を、ローカルの代表実装と実導入へ分けました。SOURCE-003は候補0件だけで完了と判断しない説明、診断項目の問い、投稿単位の重複抑制の限界を明確にしています。既存Python版のmerge時の検査漏れは修正前に再現し、修正後8件、監視は模擬HTTPで6件の既存テストを確認しました。Git / Gitleaksの再実行、実GitHubと組織での導入・対応は含みません。必要な成果物と残る判断は[計画](MIGRATION_PLAN.md#source-002003の読み合わせと具体化判断)へ記録しました。

<a id="structure-review--2026-09-27移行状況と教材への導線"></a>
### 2026-09-27：移行状況と教材への導線

[三領域の索引](MIGRATION_PORTFOLIO.md#migration-candidates)を現在の成果物へ照合しました。SOURCE-001・002、DEPS-002〜004、CICD-006・007・009の古い「候補・保留」を補修し、SOURCE-003の限定実装とCICD-003の既存controlへの配置も反映しています。旧19件のうち対象内18件は主な問いの行き先があり、DEPS-005は別PJの範囲です。旧実装全体の移植・導入完了という判定にはしません。

全47 controlについて、全体一覧・domainの入口・設計へのリンクを照合しました。全体一覧から漏れていたIAC-001を追加し、Domain一覧と同じ分野順・ID順へ揃えています。Detection / Verificationの概要へDETECT-003も反映しました。

既存39教材はcontrolから読め、教材から元のcontrolと設計へ戻れます。三領域では既存15教材への直接リンクを一覧に追加しました。SOURCE-002・003は独立教材がないため、その状態を示し、controlと設計を入口にしています。教材の数を揃えるための新設はしません。

次作業への案内を移行計画へ揃え、現在件数の重複記載と「将来実装する」とだけ記した古い案内を補修しました。以下の初回レビューや日付付きの記録は経緯として保持します。今回の確認は索引・配置・リンクと、状態表記に関する執筆者のレビューです。全教材・実装の意味的レビュー、利用者による読書評価、製品の現行性、実環境への導入は含みません。

<a id="structure-review--結論と範囲"></a>
### 結論と範囲

2026-09-17時点で、Build、consumer、Application、Operationsの四種類について、
control・教材・pattern・実装を別の更新単位へ分ける構造を維持します。
ただし、これは執筆者による読み通し・構造検査であり、独立した利用者テストやセキュリティ監査ではありません。

初回レビューではcontrolを追加せず、12件の記録と11patternを入口で整理しました。その後GOV-001、GOV-002、DETECT-001、AI-002を追加しました。2026-09-20にAI-004の設計部分を先行移行し、その時点で17件の記録と17patternになりました。AI-004のcontrol記録を追加しました。操作認可に続き、開発用実行環境の隔離を設計資料へ分離しました。

<a id="structure-review--四種類で確認した境界"></a>
### 四種類で確認した境界

| 主題 | 判断の正本 | 実装・検証の状態 | 残る境界 |
|---|---|---|---|
| [Build](../engineering/build-security/build-execution-boundary/README.md) | 実行コードへ渡す権限、外側の通信・隔離、観測 | ガイダンス。旧JSON計画検査は保留 | 実sandbox・通信拒否・sensorは未確認 |
| [Consumer](../engineering/release-integrity/consumer-artifact-acceptance/README.md) | 同一性・認証・利用者の期待値・使用gate | ガイダンス。旧crypto fixtureは公開鍵欠落等で保留 | 実署名・失効・使用gateは未確認 |
| [Application](../engineering/secure-design/object-access-boundary/README.md) | 主体・対象・操作・tenantを使う認可設計 | PSB-DESIGN-001、教材・設計・診断項目。説明用サンプルは2026-10-05に削除 | HTTP認証、全endpoint、並行処理、組織導入は未確認 |
| [Operations](../engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md) | 検知・観測障害・配送・対象・担当者・独立承認 | ガイダンス。旧synthetic adapterは保留 | Live sensor、通知、対応、PSIRT能力は未確認 |

教材は具体的なシナリオから誤解を解き、patternは方式・責任・代償を選ぶ材料とします。
同じ概念が現れても全文を統合せず、この役割分担と正本へのリンクを維持します。
「検証成功だけで安全とは言えない」のような一般論を別ファイルへ切り出さず、具体的なシナリオと問いがある教材の中で扱います。

<a id="structure-review--修正した不一致"></a>
### 修正した不一致

- ファイルリンクが存在していてもSources内の短いID anchorが欠けていた6リンクを修正。
- Application・Operations・攻撃段階9／11の集約を最新成果物と一致させた。直接対応は文書が保証目標を扱う意味で、導入済みではない。
- Control・engineering索引を一つの一覧へ整理。CacheとRunner、Buildとconsumer、CI観測と本番監視を別の境界として維持。
- 初期三件のpilotと追加の構造検証を区別し、過去の「次に作業する」という案内を最新状態へ更新。

<a id="structure-review--引き続き残す制限"></a>
### 引き続き残す制限

初回検査: YAML parse、当時12件のID一意性とcontrol索引、ローカルMarkdownのファイル・見出しanchor、
`git diff --check`を確認。SQLiteの7テストも再実行して成功しました。
これらは構造と限定実装の確認であり、全本文の正確さや本番導入を保証する検査ではありません。

Sourcesに保留・取得失敗・mutable版の記録がある資料は、現在の仕様へ再確認済みと読み替えません。
Framework mappingは旧版・ID・関係を保持した移行レビュー中の関係です。PSB-DESIGN-001のexact ASVS mappingは未追加です。
初回レビュー時は旧ツリーへの相対参照が独立化を妨げていました。2026-09-21に固定コミットへの外部参照へ変更し、[単独検査](MIGRATION_PORTFOLIO.md#repository-cutover)を追加しました。2026-09-22には本PJを正本とする公開先が確定しました。独立化の範囲と残る運用判断は[Repository cutover](MIGRATION_PORTFOLIO.md#repository-cutover)を参照してください。
全legacy実装の意味的レビュー、全参照仕様の現在の有効性、独立した読者による理解度確認は未完了です。

<a id="structure-review--2026-09-20の横断補修"></a>
### 2026-09-20の横断補修

- DETECT-001の旧fixtureに関する根拠を`legacy_rationale`へ分け、現在のガイダンスとの関係と未検証範囲を記載。
- 候補一覧・横断分析の移行済み／未移行を更新。過去の作業順序は履歴と明記。
- GOV-002の設計上の接続先をDependencyの2件とDETECT-001の計3件へ統一。
- Scanner設計本文の日英混在を補修。これは全資料の文章校正完了を意味しない。
- [Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md)と教材を追加。AI-004の認可部分のみの再編集で、control全体・製品実装・framework mappingは未移行。

レビューは内部整合性を対象とし、外部仕様全体の現行性や実環境の導入は検証していません。新規資料で確認した外部資料の範囲はSourcesに記載します。

補修後の確認：YAML 20件の構文、control ID 16件の一意性、設計パターン16件、framework mapping 62件の旧版・ID・関係・confidenceの保持、property参照、ローカルMarkdownリンク761件のファイルと見出し、`git diff --check`を確認しました。コード・製品設定は変更していないため、実装テストや実環境の認可試験は実行していません。

<a id="structure-review--追加移行と受け渡しのレビュー記録"></a>
### 追加移行と受け渡しのレビュー記録

[Security scope](SECURITY_SCOPE.md)により、AI-004は開発環境に限定します。製品自体のAI securityはai-security-foundryの担当であり、移行待ちとして補完しません。

追加batchで[PSB-GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)をガイダンス移行しました。
Runtimeの対象identityから、SBOM・build・artifact・稼働deploymentへ影響調査を渡す境界を再編集しました。
「該当なし」と「inventory不完全」、対応計画と実対応、PSIRTの組織能力を分けることが受入条件です。

端末隔離・認証情報・通信制限は[Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md)へ移行し、Source Protection・Build・runner・操作認可との責任分界を示しました。AI-004は[全26項目の対応表](MIGRATION_AI_DEVELOPMENT.md#ai-runtime-migration)、10特性のcontrol記録、旧15件のframework関係を整理し、2026-09-21にAI-002との失効時の受け渡しを補修しました。

続いてSOURCE-001を[29項目の対応表](MIGRATION_SOURCE_PROTECTION.md#endpoint-migration)へ棚卸しし、[Managed developer endpoint](../engineering/source-protection/managed-developer-endpoint/README.md)を追加しました。登録・現在の観測・業務アクセスを分け、11項目の設計を先行移行しています。端末管理範囲のcontrol記録と旧4件のframework関係の照合は、このレビュー時点で残っています。認証情報・実行隔離・公開防止を一つへ再集約しません。製品設定を移す場合のみ現行仕様と実際の拒否挙動を確認します。Domainを一つずつ全件移す方式へ戻しません。
この記録は追加の依存や実環境での操作を承認するものではありません。次作業の優先順位は移行計画で管理します。
