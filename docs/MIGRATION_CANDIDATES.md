# Migration candidates

この文書は、Source Protection、Dependency Security、CI/CD Securityの旧19件の初回棚卸しと、その後の再編集結果を保持します。
現在地と次作業は[進め方と移行計画](MIGRATION_PLAN.md#現在地と次の作業)を正本とします。
残る8 domainの初回棚卸しは[Portfolio migration review](PORTFOLIO_MIGRATION_REVIEW.md)を参照してください。
個別実装・検証器の全文レビューは未完了です。以下の順序は三領域の追加移行の履歴として扱います。

既存パッケージのIDとパスは追跡用です。新しい成果物の数や名前を一対一で固定するものではありません。
各表の名前と扱いは初回棚卸し時の暫定判断です。その後の変更は下記の再編集結果、[端末管理の対応表](ENDPOINT_MIGRATION.md)、[Git hooksの対応表](GIT_HOOKS_MIGRATION.md)を参照してください。移行済みの記録は[移行台帳](MIGRATION.md)で管理します。

## 判断の根拠

- [参照資料一覧](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md): 参照版、採否、除外理由を移す際の出発点。
- [REF-PORTFOLIO-001](../sources/README.md#ref-portfolio-001): 七つのレイヤーから偏りを確認する分析入力。
- [Supply-chain attack control list](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md): 攻撃段階、主な脅威、前後の境界を確認する索引。
- [参照資料の方針](SOURCE_POLICY.md): 直接の特性根拠と横断分析を分けるルール。

この棚卸しでは、旧資料のレビュー状態を引き継ぎます。外部資料や製品の現在の仕様を再確認した記録ではありません。

## Source Protection

| 移行元 | 主題の候補 | 扱い・残す価値 | 分ける境界 |
|---|---|---|---|
| [PSB-SOURCE-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/README.md) | Developer endpoint trust | `deferred`: 管理端末、ローカル権限、拡張機能、秘密情報の保管に関するガイダンスを選別する | 端末の侵害防止と、侵害後に使えるソース権限は別。SOURCE-004へ統合しない |
| [PSB-SOURCE-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/README.md) | Developer feedback and enforced checks | `deferred`: hooksの導入判断と小さな設定例を分離する | ローカルで回避できる検査と、mergeを止めるサーバー側の強制を区別する |
| [PSB-SOURCE-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/public-repository-exposure/README.md) | Public source exposure | `split`: [control](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)と[pattern](../engineering/source-protection/public-exposure-observation-and-triage/README.md)へ移行。GitHub PoCは非移植 | 公開codeの観測と外部attack surface全般、candidate triageとcredential失効を区別する |
| [PSB-SOURCE-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/source-access-credential-lifecycle/README.md) | Source credential lifecycle | `split`: pilotで再編集済み。製品手順と学習資料を分離 | 通常の有効期限・退職時の失効と、漏えい後の派生権限の封じ込めを区別する |
| [PSB-SOURCE-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/repository-destruction-recovery/README.md) | Source recovery independence | `deferred`: 破壊権限の制限、独立したバックアップ、復旧演習を再構成する | バックアップ処理の成功と、必要な対象を期限内に復元できることは別 |
| [PSB-SOURCE-006](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/README.md) | Organization posture governance | `deferred`: アクセス、既定値、App、監査の主題を分割候補として確認する | IDのライフサイクル、組織全体の設定状態、個別変更の承認・照合を区別する |

## Dependency Security

| 移行元 | 主題の候補 | 扱い・残す価値 | 分ける境界 |
|---|---|---|---|
| [PSB-DEPS-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/release-cooldown/README.md) | Dependency release cooldown / Managed acquisition path | `split`: cooldownはpilotで再編集済み。管理プロキシは独立した主題の候補 | 公開直後の採用制限と、取得先の制限・遮断情報の適用は別 |
| [PSB-DEPS-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/install-script-execution/README.md) | Install execution policy | `split`候補: 実行許可の原則、悪用経路、製品別の設定と確認方法へ分ける | install時の実行を止めても、import、test、pluginによる後続の実行は止まらない |
| [PSB-DEPS-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/lockfile-integrity/README.md) | Dependency artifact identity | `split`候補: graphの固定と取得したbytesの照合を説明し、native install例は製品別に置く | hash一致は内容の安全性を証明しない。更新レビューとは別 |
| [PSB-DEPS-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/dependency-change-review/README.md) | Dependency change review | `split`候補: 直接・推移依存の差分、根拠不足時の判断、独立レビューを残す | review済みgraphと実際の取得・実行状態を接続する。advisory未取得を問題なしにしない |
| [PSB-DEPS-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/dependency-security/ai-model-supply-chain/README.md) | Model and dataset intake | `out-of-scope`: モデル・データセットのsecurityはai-security-foundryへ委ねる | [Security scope](SECURITY_SCOPE.md)に基づく除外。一般パッケージのDependency Securityは引き続き対象 |

## CI/CD Security

| 移行元 | 主題の候補 | 扱い・残す価値 | 分ける境界 |
|---|---|---|---|
| [PSB-CICD-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/action-sha-pinning/README.md) | Workflow dependency identity | `split`候補: 不変な参照、更新判断、再利用workflowの関係を残す | SHA固定と参照先の意味的なレビューは別 |
| [PSB-CICD-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-command-injection/README.md) | Workflow input handling | `split`候補: 外部入力がshell構文になる経路と、境界を保つ小さな例を残す | データとして渡しても、実行先がその値を再解釈すれば別の注入経路になる |
| [PSB-CICD-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-static-analysis/README.md) | Workflow analysis | `deferred`: scannerの比較・採否は教材、固定した実行設定は実装例の候補 | scannerの成功と信頼境界の安全性は別。失敗・未検査を明示する |
| [PSB-CICD-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-least-privilege/README.md) | Workflow authority minimization | `split`候補: jobの目的と実効権限を対応させ、製品設定を分離する | token permissionsだけでsecret、OIDC、hostの権限は制限できない |
| [PSB-CICD-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/untrusted-pr-boundary/README.md) | Untrusted PR boundary | `split`: pilotで再編集済み | PR由来の状態の昇格と、信頼済みrevisionで開始した後の権限は別 |
| [PSB-CICD-006](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/audience-bound-oidc-federation/README.md) | Workload federation boundary | `split`候補: 発行条件、引受先の権限、AWS固有のtrust policyを分離する | 短命tokenでも、広いsubjectや引受先権限を持てば被害は成立する |
| [PSB-CICD-007](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/runner-hardening/README.md) | Runner lifecycle isolation | `split`候補: 一jobの隔離、割当、compute・storage破棄、ログの外部保存を分ける | ephemeral登録とhostの破棄は別。実行中の攻撃検知は独立して検討する |
| [PSB-CICD-009](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/cache-provenance-isolation/README.md) | Cache trust boundary | `split`候補: writer、consumer、内容、取得後の照合を一つの経路として残す | cache keyは内容の真正性を保証しない。runner内の残存stateとも区別する |

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
下記の再編集結果と併せて読み、候補選定と組織への導入済み状態を区別します。

## 横断資料と未着手領域

`REF-CICD-011`のthreat matrixと`REF-CICD-012`のNIST SP 800-204Dは、複数control間の
空白とID・成果物の受け渡しをレビューする資料として移します。CI/CD領域だけを連想させるIDの継承は
資料単位で再検討します。ID変更時も版、旧IDとの関係、採否、除外理由を省略しません。

Runner内のruntime detectionは、runner破棄へ吸収しません。旧`REF-BUILD-001`は
センサー候補の発見にとどまり、導入済みではありません。プロセス・file・networkの何を観測できるか、
センサー停止をどう検出するか、権限と秘密情報をどう扱うかを評価してから採否を決めます。

七つのレイヤーでは、今回の候補はプラットフォームと外部依存へ偏っています。
アプリケーションの設計・実装、PSIRT、本番運用、ガバナンス、教育の棚卸しは[Portfolio migration review](PORTFOLIO_MIGRATION_REVIEW.md)に保持します。
Falco／Sysdig等の本番監視もその対象です。CIの検査や署名だけで、本番の検知・対応を満たしたとは扱いません。

## 初回追加移行の再編集結果

初回の追加移行は[Install execution policy](../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md)へ再編集済みです。
pipの限定した取得・準備段階をローカルで確認し、他製品の実装と実環境導入は未確認として残しました。
順序2のDependency artifact identity / Dependency change reviewも再編集済みです。
共有教材・patternとGitHub参照workflowを追加し、native wrapperの移植とlive確認は未完了として残しました。
順序3のWorkload federation boundaryも再編集済みです。Exact AWS trust例とlive確認手順を分離し、
実際の交換・拒否・失効は未確認として残しました。
順序4のCache trust boundary / Runner lifecycle isolationも再編集済みです。
共有教材・patternを追加し、workflowとprovisionerの移植、実環境のcache・破棄確認は保留しています。
その後、Build、consumer、Application、Operationsの初回再編集と[構造レビュー](STRUCTURE_REVIEW.md)も実施しました。
これらを未着手の次作業として扱いません。

初回のInstall execution policyでは、悪意あるpackageがinstall時に開発端末・CIの権限を使う経路と、
許可が必要な例外を説明するため、control・教材・patternを再編集しました。
pipの比較例・テストは実際の挙動を観測する限定実装とし、importやtestでの後続実行は残余境界に残しました。
今後のNegative testは、[文書品質](CONTENT_QUALITY.md#negative-test)に従い、診断観点の列挙だけでも成立します。

2026-09-23：SOURCE-002をSecret publication boundaryへ再編集し、ローカルhooksと共有先の判断を分離しました。
その後の具体化判断により[Git・Gitleaks代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)を追加しています。
旧独自検出ルール、Docker wrapper、installerは移植せず、実環境への導入は未実施です。
