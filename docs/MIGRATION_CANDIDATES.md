# 三領域の移行状況

Source Protection、Dependency Security、CI/CD Securityの旧19件から、現在の成果物へたどる索引です。2026-09-27に移行先と表記を照合しました。
現在地と次作業は[進め方と移行計画](MIGRATION_PLAN.md#現在地と次の作業)を正本とします。
残る8 domainの初回棚卸しは[Portfolio migration review](PORTFOLIO_MIGRATION_REVIEW.md)を参照してください。
対象内の18件には主な問いを扱うcontrolまたはpatternへの行き先があり、DEPS-005は対象外です。旧CICD-003の共通要件は既存DETECT-001へ配置し、独立controlは作っていません。旧実装全体の移植や実環境への導入が完了したという意味ではありません。

既存パッケージのIDとパスは追跡用です。新しい成果物の数や名前を一対一で固定するものではありません。
以下の三表は現在の移行先と採否を示します。初回の作業順序は後半に履歴として残し、個別の経緯と旧実装の扱いは[移行台帳](MIGRATION.md)および各対応表を正本とします。

## 判断の根拠

- [参照資料一覧](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md): 参照版、採否、除外理由を移す際の出発点。
- [REF-PORTFOLIO-001](../sources/README.md#ref-portfolio-001): 七つのレイヤーから偏りを確認する分析入力。
- [Supply-chain attack control list](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md): 攻撃段階、主な脅威、前後の境界を確認する索引。
- [参照資料の方針](SOURCE_POLICY.md): 直接の特性根拠と横断分析を分けるルール。

この索引の更新は、外部資料や製品仕様を再確認した記録ではありません。確認日と採否は移行先の参照資料へたどってください。

## Source Protection

| 移行元 | 現在の主題・移行先 | 扱い・残す価値 | 分ける境界 |
|---|---|---|---|
| [PSB-SOURCE-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/README.md) | [Developer endpoint trust](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md) | `split`：端末管理のcontrol、教材、設計へ再編集。[29項目の対応](ENDPOINT_MIGRATION.md)を保持 | 端末の状態と、侵害後に使えるソース権限は別。実端末の管理・拒否は未確認 |
| [PSB-SOURCE-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/README.md) | [Secret publication boundary](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md) | `split`：公開前の検査、設計、Gitleaks・Python例へ再編集。[旧13項目の対応](GIT_HOOKS_MIGRATION.md)を保持 | ローカルhooksと共有先の強制、例の完成と実導入を分ける |
| [PSB-SOURCE-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/public-repository-exposure/README.md) | [Public source exposure triage](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md) | `split`：公開候補の観測と精査へ再編集。利用者が選んだ公開GitHubの少数指標を[限定実装](../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)。旧PoCの一括移植はしない | 公開ソースの観測、外部サービス台帳、credential失効は別。実検索・通知・対応運用は未確認 |
| [PSB-SOURCE-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/source-access-credential-lifecycle/README.md) | [Source credential lifecycle](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | `split`：control、教材、設計、GitHub手順へ再編集 | 通常の有効期限・退職時の失効と、漏えい後の派生権限の封じ込めを区別する |
| [PSB-SOURCE-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/repository-destruction-recovery/README.md) | Repository recovery independence | `split`: [control](../controls/records/source-protection/psb-source-005-repository-recovery-independence/README.md)、教材、[pattern](../engineering/source-protection/independent-repository-backup-and-restore/README.md)、Git mirror例へ再編集。旧4項目の[採否](REPOSITORY_RECOVERY_MIGRATION.md)を保持 | Gitの復元と開発再開、独立した保持、実環境の導入は別 |
| [PSB-SOURCE-006](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/README.md) | Source organization security posture | `split`: [control](../controls/records/source-protection/psb-source-006-source-organization-security-posture/README.md)、教材、[pattern](../engineering/source-protection/organization-baseline-and-drift-review/README.md)、GitHub手順へ移行。旧10項目の[採否](SOURCE_ORGANIZATION_POSTURE_MIGRATION.md)を保持 | ID・公開・CI・復旧の意味と、組織の実適用・確認障害を分ける。Live導入は未確認 |

## Dependency Security

| 移行元 | 現在の主題・移行先 | 扱い・残す価値 | 分ける境界 |
|---|---|---|---|
| [PSB-DEPS-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/release-cooldown/README.md) | [Dependency release cooldown](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) | `split`：control、教材、設計、npm例へ再編集。管理プロキシは別の選択肢として残す | 公開直後の採用制限と、取得先の制限・遮断情報の適用は別 |
| [PSB-DEPS-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/install-script-execution/README.md) | [Install execution policy](../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md) | `split`：実行許可のcontrol、教材、設計、pip比較例へ再編集 | install時の実行を止めても、import、test、pluginによる後続の実行は止まらない |
| [PSB-DEPS-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/lockfile-integrity/README.md) | [Dependency artifact identity](../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md) | `split`：通常buildの入力を特定するcontrol、教材、共通[設計](../engineering/dependency-security/reviewed-dependency-intake/README.md)へ再編集 | 依存関係の固定、取得したファイルの照合、採用判断を分ける。旧native wrapperは非移植 |
| [PSB-DEPS-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/dependency-change-review/README.md) | [Dependency change review](../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md) | `split`：更新判断のcontrol、教材、共通設計、GitHub review例へ再編集 | レビューした依存関係と実取得を接続する。Advisory未取得・実merge拒否は別に確認 |
| [PSB-DEPS-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/ai-model-supply-chain/README.md) | Model and dataset intake | `out-of-scope`: モデル・データセットのsecurityはai-security-foundryへ委ねる | [Security scope](SECURITY_SCOPE.md)に基づく除外。一般パッケージのDependency Securityは引き続き対象 |

## CI/CD Security

| 移行元 | 現在の主題・移行先 | 扱い・残す価値 | 分ける境界 |
|---|---|---|---|
| [PSB-CICD-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/action-sha-pinning/README.md) | [Workflow dependency identity](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md) | `split`: 直接参照・更新review・内部取得・受入条件へ再編集。限定Python実装、pinact手順、教材まで移行 | [旧6項目と実装・mappingの採否](WORKFLOW_DEPENDENCY_MIGRATION.md)。形式確認と出所・全依存の確認、local成功と実merge保護を分ける |
| [PSB-CICD-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-command-injection/README.md) | [Workflow input handling](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md) | `split`: 原則・教材・設計・診断項目で完了。独自scannerと中央配布は移さない | [旧4項目と実装・mappingの採否](WORKFLOW_INPUT_MIGRATION.md)。引数の保持と操作の許可、直接補間と後段の再解釈を分ける |
| [PSB-CICD-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-static-analysis/README.md) | Workflow analysis | `split`：[既存DETECT-001・教材とENG-CICD-007へ配置](WORKFLOW_ANALYSIS_MIGRATION.md)。独立control・独自scanner・SARIF parserは追加しない | 検査・表示・merge条件を分け、終了0・部分解析・設定変更を確認する。文書と診断項目で完了、実環境の強制は未確認 |
| [PSB-CICD-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-least-privilege/README.md) | [Workflow authority minimization](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md) | `split`: 用途・実効権限・開始条件・委譲へ再編集。GitHub設定と無権限・読取り専用smoke例を追加 | [旧6項目と実装・mappingの採否](WORKFLOW_AUTHORITY_MIGRATION.md)。形式と最小性、標準tokenと追加権限、ローカル確認と実GitHubの拒否を分ける |
| [PSB-CICD-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/untrusted-pr-boundary/README.md) | [Untrusted PR boundary](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | `split`：control、教材、設計、GitHub Actions例へ再編集 | PR由来の状態の昇格と、信頼済みrevisionで開始した後の権限は別 |
| [PSB-CICD-006](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/audience-bound-oidc-federation/README.md) | [Workload federation boundary](../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md) | `split`：発行条件・交換先権限のcontrol、教材、設計、AWS trust例へ再編集 | 短命tokenでも広いsubjectや交換先権限の影響は残る。実交換・拒否・失効は未確認 |
| [PSB-CICD-007](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/runner-hardening/README.md) | [Runner lifecycle isolation](../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md) | `split`：一jobの隔離・破棄のcontrol、教材、共通[設計](../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md)へ再編集 | 登録解除とhost破棄は別。実行時検知と実環境の破棄確認は別途必要 |
| [PSB-CICD-009](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/cache-provenance-isolation/README.md) | [Cache trust boundary](../controls/records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md) | `split`：保存者・利用者・内容のcontrol、教材、共通設計へ再編集 | Key一致と内容の真正性は別。Runner内の残存状態と実cacheの権限も分ける |

廃止したcontrolの扱いは[ADR-0003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/adr/0003-privileged-change-runbook.md)に従います。
共通変更管理はrunbookとして移行を検討し、独立したcontrolとして復活させません。

## 初回追加移行の順序（履歴）

| 順序 | 主題 | 攻撃段階・脅威 | 次の読者の判断 | 参照資料を反映する方法 |
|---|---|---|---|---|
| 1 | Install execution policy | 4→7: 採用したdependencyのhookやbuild backendがCI権限で動く | 必要なinstall-time executionだけをどこで許可し、未承認実行をどう止めるか | 旧DEPS-002の製品仕様・mappingを保持。製品挙動は公式仕様で再確認してから実装例へ移す |
| 2 | Dependency artifact identity / Dependency change review | 4→7: 差し替え、未reviewの推移依存、根拠不足 | reviewしたgraphと実際に取得・実行する内容をどう接続するか | `REF-DEPS-002`とnative lockfile仕様を分けて扱い、欠落したadvisoryを明示する |
| 3 | Workload federation boundary | 5→6→10: CI状態からcloud・deploy権限を取得 | revision、workflow、発行条件、引受先権限のどれを制限するか | `REF-CICD-009`を脅威・設計入力に使い、GitHubとAWSの仕様・版を別に追跡する |
| 4 | Cache trust boundary / Runner lifecycle isolation | 5→7: 低信頼の永続stateが後続jobへ届く | 再利用するstateと破棄する資産をどこで分けるか | `REF-CICD-014`の登録・host破棄・ログ保存の違いを反映し、BUILD-001へ渡す責任を示す |

この順序は、[攻撃段階の索引](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md)から選んだ移行上の優先順位です。
現在の移行先は上の三表へ反映しています。この初回の順序を今後の作業指示や組織への導入順とは扱いません。

## 横断資料と未確認範囲

旧`REF-CICD-011`のthreat matrixと旧`REF-CICD-012`のNIST SP 800-204Dは、横断分析の追加入力候補です。原文と版、資料の役割、既存資料との重複を確認して採否を決めます。ここでの旧IDは追跡用で、移行先の参照資料IDや個別要件ではありません。採用する場合も版・旧IDとの関係・採否・限界を記録します。

Runner内のruntime detectionは、runner破棄へ吸収しません。旧`REF-BUILD-001`は
センサー候補の発見にとどまり、導入済みではありません。プロセス・file・networkの何を観測できるか、
センサー停止をどう検出するか、権限と秘密情報をどう扱うかを評価してから採否を決めます。

七つのレイヤーでは、三領域の主題はプラットフォームと外部依存へ偏っています。
アプリケーションの設計・実装、PSIRT、本番運用、ガバナンス、教育の棚卸しは[Portfolio migration review](PORTFOLIO_MIGRATION_REVIEW.md)に保持します。
Falco／Sysdig等の本番監視もその対象です。CIの検査や署名だけで、本番の検知・対応を満たしたとは扱いません。

## 文書の完成と実環境の確認

Control・教材・設計の移行先は上の三表からたどれます。旧実装の不在を一律に未完了とせず、必要な成果物は[実効性の基準](ARTIFACT_MODEL.md#主題ごとの具体化判断)で選びます。[診断で確認する項目](CONTENT_QUALITY.md#failure-checks)はチェックリストでも完成します。

実際の検査範囲、権限、merge拒否、runner破棄、復元、通知・対応運用は、採用対象と許可された確認方法を決めてから評価します。必要な実装を選んだのに前提が不足する場合だけ、理由と再開条件を計画へ残します。全旧実装・検証器の意味的レビューや、全製品の現行仕様を確認済みとは扱いません。
