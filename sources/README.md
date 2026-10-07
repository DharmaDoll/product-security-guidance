# 参照資料と仕様

このディレクトリは、コントロール、学習資料、設計パターン、実装例、横断分析の判断根拠を追跡するための
参照資料一覧です。旧リポジトリの
[`docs/SECURITY_GUIDANCE_SOURCES.md`](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md)が担っていた役割を継承し、
資料を末尾の参考文献として並べるだけでなく、採用した判断、採用しなかった提案、限界まで記録します。

<a id="ref-modelforge-001"></a>

## REF-MODELFORGE-001

区分は`adjacent project`、管理者はDharmaDoll。[ModelForge README](https://github.com/DharmaDoll/ModelForge/blob/4188fa1cce41974b3e43b7e60aedc6cc7ec98b3d/README.md)と[Roadmap](https://github.com/DharmaDoll/ModelForge/blob/4188fa1cce41974b3e43b7e60aedc6cc7ec98b3d/ROADMAP.md)を2026-10-04に確認し、手元のcommitとremote HEADが一致することを確認しました。利用先は[Secure Designの境界](../docs/REPOSITORY_DESIGN.md#分類領域の選び方)と[領域の入口](../controls/records/secure-design/README.md)です。

- 採用：システム情報の構造化、DFD、STRIDE等による脅威候補の作成はModelForgeで進め、本PJのSecure Designは再利用できる設計上の判断を扱う。
- 不採用：生成された脅威候補をそのままcontrolへ変換しない。ModelForgeの出力をレビュー済みの脅威モデル、脆弱性、対策の導入証拠とは扱わない。
- 限界：ModelForgeのREADMEは脅威モデルの初稿生成を説明する。RoadmapにあるModel Diffやレビュー状態管理は計画中であり、実装済みとみなさない。両PJの自動連携や実案件での利用は未確認。

<a id="ref-vulnerability-remedy-validation-001"></a>

## REF-VULNERABILITY-REMEDY-VALIDATION-001

区分は`primary guidance`、発行者はFIRST。対象は[PSIRT Services Framework v1.1](https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1-1)のService 4.2、特にFunction 4.2.1〜4.2.3です。2026-10-04に公式の公開本文を確認しました。[PSB-GOV-008](../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md)と[教材](../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/learning.md)の直接の設計入力です。

- 採用：影響する製品・版と変種を特定し、修正を公開する前にQA・セキュリティの確認を行う。必要に応じて報告者と検証し、修正の提供先と開示時期を調整する。
- 変更して採用：本PJでは変更の取込み、修正の検証、検証した版の提供を別の状態として扱う。各版・構成のうち修正を主張する範囲と、未解決の範囲を明示するのは資料の修正・検証・提供の記述を具体化した判断です。
- 不採用：全件に同じテストコード、全報告者の承認、全影響版の一律の修正、固定の公開期限を求めない。修正しない版は黙って消さず、別のリスク判断と利用者への説明へ渡す。
- 限界：公開Web本文の固定digest、採用先の製品・検証環境・修正内容・提供経路は未確認。修正、検証、公開、利用者の更新を実施した証拠ではない。本文が更新された場合は採用版を再確認する。

<a id="ref-vulnerability-advisory-001"></a>

## REF-VULNERABILITY-ADVISORY-001

区分は`primary guidance`、発行者はFIRST。対象は[PSIRT Services Framework v1.1](https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1-1)のService 5.1〜5.3とFunction 1.5.4です。2026-10-04に公式の公開本文を確認しました。[PSB-GOV-007](../controls/records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/README.md)と[教材](../controls/records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/learning.md)の直接の設計入力です。

- 採用：報告者・関係する他社との調整、影響する製品と修正情報を伝える告知、対象者に応じた通知経路、告知のレビュー・承認、公開後の更新履歴。
- 変更して採用：本PJでは修正の提供、告知の公開、対象者への通知を別の状態として扱う。配信不能・対象先の欠落と訂正の再連絡を未完了として残すのは、資料の通知と公開のサービスを具体化した本PJの判断です。
- 不採用：固定の公開期限、特定の通知媒体、全事案へのCVE・CSAF必須化、関係する他社との調整を理由にした無期限の通知延期は求めない。資料のPSIRTサービス全体を一つのcontrolへ取り込まない。
- 限界：公開Web本文の固定digest、対象組織の契約・法的義務、実際の告知・配信・利用者の到達は未確認。資料は組織の導入証拠ではなく、本文が更新された場合は採用版を再確認する。

<a id="ref-vulnerability-report-intake-001"></a>

## REF-VULNERABILITY-REPORT-INTAKE-001

区分は`primary guidance`、発行者はFIRST。対象は[PSIRT Services Framework v1.1](https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1-1)のService 2.1、Function 1.5.2、Service 3.1です。2026-10-04に公式の公開本文を確認しました。[PSB-GOV-006](../controls/records/governance-operations/psb-gov-006-vulnerability-report-intake/README.md)と[教材](../controls/records/governance-operations/psb-gov-006-vulnerability-report-intake/learning.md)の直接の設計入力です。

- 採用：見つけやすい報告窓口、社内からの転送経路、窓口の監視、受領連絡、未公開情報と報告者を守る通信、報告を安全に処理する環境。
- 変更して採用：本PJでは到着・受領連絡・担当者への引き渡しを別の状態として記録し、重複判定や窓口障害で新しい情報を失わないことを受付の完了条件にする。これは資料のサービス記述を具体化した本PJの判断です。
- 不採用：特定のメールアドレス、暗号方式、固定の応答時間、PSIRTの組織形態を全組織の必須条件にしない。資料のService 3.1が扱う脆弱性の適格性と優先度判断を受付controlへ取り込まない。
- 限界：公開Web本文の固定digestと組織の窓口・当番・隔離環境は未確認。窓口の導入、報告の受領、調査、開示、PSIRT成熟度を検証した記録ではない。本文が更新された場合は採用版を再確認する。

## REF-WORKFLOW-ANALYSIS-001

区分は`repository interpretation`、発行者は本PJ。[旧CICD-003](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-static-analysis)を固定revision `f42987759218c9b8daf3924320542a1935ef78e0`で2026-09-27に確認しました。利用先は[DETECT-001](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)のSCAN-3・4、教材と[ENG-CICD-007](../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)です。

採用するのは、検査と結果公開の権限を分け、tool・policy・対象・完了状態を受入条件へ結ぶ判断です。変更して採用したのは、共通要件を既存controlへ配置し、結果公開を方式の選択へ分ける点です。特定の二job構成、`main`という名前、persona auditor、終了コード`0/1/2`、SARIF内の成功文字列を普遍的な合格条件にしません。

独自の行scanner・SARIF parserの移植、旧人工fixtureや`PASS`の導入証拠化は不採用です。旧比較記事だけを採用根拠にせず、Actionlint・poutineを自動的に追加しません。旧5項目・14 file・2 framework関係の採否は[移行判断](../docs/MIGRATION_CI_CD.md#workflow-analysis-migration)へ記録しています。文書と診断項目が今回の完了範囲であり、実scanner・GitHubの実行・拒否・導入は未確認です。

## SPEC-ZIZMOR-WORKFLOW-ANALYSIS

区分は`vendor specification`、発行者zizmorcore。2026-09-27に公式Webと以下の固定sourceを確認しました。利用先は[DETECT-001の教材](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/learning.md)と[ENG-CICD-007](../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)です。

- [Usage](https://docs.zizmor.sh/usage/)：SARIF modeでは指摘による非0終了が無効になる点、対象なしと監査障害の状態、部分的な解析失敗とstrict collection、収集範囲・ignore・personaを判断材料にする。指摘の採否は組織の方針へ接続する。
- [Configuration](https://docs.zizmor.sh/configuration/)：設定探索、明示する設定、ルールの無効化・ignoreを確認する。候補内の設定とinline ignoreが結果を弱め得る経路を、変更保護と例外の確認対象にする。
- 固定[Action v0.6.1のaction.yml](https://github.com/zizmorcore/zizmor-action/blob/6fc4b006235f201fdab3722e17240ab420d580e5/action.yml)、[action.sh](https://github.com/zizmorcore/zizmor-action/blob/6fc4b006235f201fdab3722e17240ab420d580e5/action.sh)、[version table](https://github.com/zizmorcore/zizmor-action/blob/6fc4b006235f201fdab3722e17240ab420d580e5/support/versions)：versionからdigest付きimageを選び、結果公開modeでSARIFを生成する構造を確認した。`fail-on-no-inputs`は対象なしの扱いで、strict collectionを指定する入力・引数の組立てはない。

旧選定値はzizmor **1.28.0**、reviewed source `6ea55f583ef6681a59b1c180950e47861a3c0293`です。旧Action commitは`6fc4b006235f201fdab3722e17240ab420d580e5`、tableにある1.28.0のimage digestは`sha256:8e6b3e4fb74d1aa5d23e83ea369f386c66eced0d1fb944d32cd8b2aac100b00d`です。Source commitは旧選定記録から保持した値、Action構造とtableは今回確認した事実として分けます。Imageの取得・実行、publisherやregistryの現在状態は検証していません。

変更して採用するのは、固定版の再配布から、採用版・出力mode・収集と受入条件の確認へ移す点です。旧固定Actionを部分的な解析失敗まで拒否する完成例としては不採用です。対応版のCLI等を選ぶ判断が必要で、全指摘personaやオンライン監査を一律に要求しません。

Web本文は可変で固定digest未記録のため`re-review-required`です。現在の文書には1.28.0後の変更もあり、設定探索や新しい検査対象を旧版へ遡って適用しません。静的な定義解析を、呼出先script・動的取得・実効権限・実行時の完全な検査へ一般化しません。固定digestだけで発行者の真正性やコードの安全性を証明したとも扱いません。

2026-09-29に公式UsageのSARIF時の終了状態と部分的な解析失敗の説明を再確認しました。指摘の有無と解析完了を別に保持する一般的な集約判断は、zizmor固有の出力契約ではなく本PJの解釈です。旧固定版の動作を再実行した意味ではありません。

## SPEC-GITHUB-SCANNING-ACCEPTANCE

区分は`vendor specification`、発行者GitHub。2026-09-27に以下の公式Web本文を確認しました。可変文書で固定digestは未記録のため`re-review-required`です。利用先は[ENG-CICD-007](../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)とDETECT-001の教材です。

- [SARIF support](https://docs.github.com/en/code-security/reference/code-scanning/sarif-support)：対応する形式と制限、結果の扱いを確認する。SARIF内の項目は実行の真正性の証拠にはならず、旧parserの必須項目をGitHubの普遍的な必須条件にしない。
- [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-status-checks-to-pass-before-merging)：必須check、期待する発行元、code scanningの必要tool・解析中・未設定と受入条件を確認する。Check名やuploadの成功だけをmerge保護にしない。
- [Set code scanning merge protection](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/set-merge-protection)：適用できるrepository・契約、rulesetの有効化、必要toolと指摘のしきい値を方式選択に使う。

採用するのは、表示とmerge条件を分け、契約・機能・有効設定を対象ごとに確認する判断です。結果公開を全repositoryの必須要件にする提案、公開済み結果だけから導入・強制・完全な対象範囲を認定する扱いは不採用です。権限と開始条件は[Workflow authority](#spec-github-workflow-authority)に接続し、重複して定義しません。実設定、upload、拒否、閲覧・保持、bypassは未確認です。

## REF-WORKFLOW-INPUT-001

区分は`repository interpretation`、発行者は本PJ。[旧CICD-002](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-command-injection)を固定revision `f42987759218c9b8daf3924320542a1935ef78e0`で2026-09-27に確認しました。利用先は[CICD-002](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md)のCI-INPUT-1・4〜6、教材と[ENG-CICD-006](../engineering/cicd-security/workflow-data-and-command-boundary/README.md)です。

採用するのは、値を変更できる主体・到達性・解釈箇所とjobの実効権限を分け、環境変数への移動後も呼出先の再解釈を確認する判断です。変更して採用したのは、全直接式禁止を組織が選ぶprofileへ分け、表示用の式・対象不足・解析不能を区別する点です。引数を保持する対策と、許可する操作・対象の制限を別に説明します。製品挙動は次の一次資料へ分けます。

旧scannerの無変更copy、全controlへの同じ自動検査、中央配布の先回り、生成済み`PASS`の導入証拠化は不採用です。文書と診断項目を今回の完了範囲とし、実GitHubや呼出先の拒否・scanner導入は未確認です。旧4項目・14 file・3 framework関係の採否は[移行判断](../docs/MIGRATION_CI_CD.md#workflow-input-migration)へ残しています。

## SPEC-GITHUB-WORKFLOW-INPUT

区分は`vendor specification`、発行者GitHub。2026-09-27に以下の公式Web本文を確認しました。GitHub.comの可変文書で固定digestは未記録のため`re-review-required`です。利用先は[CICD-002](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md)のCI-INPUT-1・2・5、教材、[設計pattern](../engineering/cicd-security/workflow-data-and-command-boundary/README.md)です。

- [Script injections](https://docs.github.com/en/actions/concepts/security/script-injections)：題名・本文・branch等が入力になり、式の結果をshell起動前に一時スクリプトへ埋め込む経路を採用する。Contextの名称だけで信頼度や到達性を判断しない。
- [Secure use reference — script injection](https://docs.github.com/en/actions/reference/security/secure-use#good-practices-for-mitigating-script-injection-attacks)：環境変数へ渡す方式と、Actionへ入力として渡す方式を採用する。引数を引用することとコード生成を除くことを区別し、Action内部の再解釈を未確認のまま安全とは扱わない。
- [Workflow syntax — run・shell](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsrun)：`run`を実行するshellと一時ファイルを確認する。教材の断片は`bash`を明示し、Windows・PowerShell・custom shellに同じ引用規則を流用しない。

全`run:`の直接式を禁止する規則、限定scanner、中央配布をGitHubの必須要件としては採用しません。公式例を全workflowの安全性や権限の最小性へ一般化せず、実jobの実行・拒否・呼出先・全shellの挙動は未確認です。入力元、shell、呼出先、provider仕様が変わった時に再確認します。

## SPEC-BASH-SHELL-EXPANSION-5-2

区分は`vendor specification`、発行者GNU／Free Software Foundation。参照本文はローカルに配布されたGNU Bash **5.2**の`bash(1)` manual（2022-09-19版）のEXPANSION、Word Splitting、Pathname Expansion、Simple Command Expansion、`eval`節です。2026-09-27に本文を確認しました。配布物`bash.1.gz`のSHA-256は`3ca7a67df55bd2f80a2de111f8d44df359f7a795573aaaadce09a52a22bcedeb`、利用環境のbinaryは**5.2.37(1)-release**です。仕様本文の読解であり、workflowの実行試験ではありません。

[公式manualの入口](https://www.gnu.org/software/bash/manual/)へリンクします。Web上のShell Expansions、Shell Operation、Builtinsの本文は取得失敗のため確認済みとせず、別版・他shellへ広げる際は`re-review-required`です。利用先は[CICD-002 / CI-INPUT-3](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md)と教材です。

採用するのは、通常の変数展開とソースの構文解析を区別し、未引用の展開結果が分割・ファイル名展開の対象になること、`eval`が値を連結して命令として読み直すことです。引用した値がオプション・対象として許可されるかは呼出先の仕様へ分けます。算術式等の別の解釈箇所、PowerShell・cmd・他言語の規則、全Bashプログラムの安全性は、この限定した本文確認から推定しません。

## REF-COMMAND-INPUT-DEFENSE

区分は`primary guidance`、発行者OWASP Cheat Sheet Series。[OS Command Injection Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)のArgument Injection、Primary Defensesを2026-09-27に確認しました。可変Web文書で固定digestは未記録のため`re-review-required`です。利用先は[CICD-002](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md)のCI-INPUT-2〜4、教材、patternです。

採用するのは、OSコマンドを生成しないAPIの検討、命令とデータの分離、許可する操作・引数の意味の制限です。一つの引数でもオプションを指定し得るという説明を、quoteだけで操作が安全になるという誤解の補正へ使います。`--`は呼出先の対応と有効な位置を確認する方式へ限定します。

変更して採用したのは、一般的なapplication向け説明をCIの入力経路へ適用する点です。特定の言語のescape関数、固定の文字・長さ制限、全shell共通の無害化を要求しません。個別ASVS項目への対応や準拠をこの資料から追加せず、実製品の引数仕様・対象の認可・診断結果は別に確認します。

## REF-WORKFLOW-AUTHORITY-001

区分は`repository interpretation`、発行者は本PJ。固定した[旧CICD-004](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-least-privilege)を2026-09-27に確認し、[新control](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)のJOB-AUTH-2・3・5・7、教材、[ENG-CICD-005](../engineering/cicd-security/purpose-bound-job-authority/README.md)へ使います。製品挙動は次の一次資料へ分けます。

採用するのは、実際の操作から権限を選び、同じjobの共有範囲、発行許可、開始条件、呼出元の委譲、現在の正常・拒否・未確認を分ける判断です。変更して採用したのは、旧GitHub token中心の問いをjobの実効権限として読み直し、PAT・App・cloud key・host等が標準tokenの制限に従わないことを明示する点です。認証情報の発行・失効やrunnerの隔離は既存controlへ渡し、同じ本文を複製しません。

全処理への同じref・Environment・手動承認、形式だけからの権限の必要性判定、scanner成功によるlive最小権限の認定、合成JSONの採用済み判定は不採用です。具体例の無権限markerは環境の開始条件を確認する手段で、writeやcloud交換を実行したことにはしません。旧6項目・6 framework関係・実装判断と未確認は[移行記録](../docs/MIGRATION_CI_CD.md#workflow-authority-migration)へ残します。

## SPEC-GITHUB-WORKFLOW-AUTHORITY

区分は`vendor specification`、発行者GitHub。2026-09-27に以下の公式本文を確認しました。GitHub.com／Enterprise Cloudの可変Web文書で固定digestは未記録のため`re-review-required`です。利用先は[CICD-004](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)のJOB-AUTH-1〜6、教材、pattern、[GitHub実装例](../engineering/cicd-security/purpose-bound-job-authority/implementations/github/README.md)です。

- [GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token)と[Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)：job用tokenと、Actionが`github.token`から利用できる権限を扱う。必要最小限の付与を採用し、明示的に引数へ渡さないだけで使えないとはしない。追加PAT・App等の範囲とrunnerの共有状態は別に確認する。
- [Workflow syntax — permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions)：既定値からworkflow・job・fork条件へ調整される順序、`{}`と未指定scopeの`none`、操作別scopeを採用する。既定readをjobの上限やtokenの不在とは扱わない。全現行scopeの一覧を本文へ複製しない。
- [OIDC reference](https://docs.github.com/en/actions/reference/security/oidc)：`id-token: write`は発行に必要で、他資源へのwrite許可そのものではない。必要な交換jobだけに付け、cloud側の受入条件はCICD-006へ分ける。
- [Reusing workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)：callerの明示権限、呼出先と入れ子の権限増加禁止、caller jobで使えるkeyを採用する。Callerへ`environment`を置く構成や、委譲先が広いcaller権限を自動で減らす前提は採らない。
- [Managing environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)、[deployment protection](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)、[reviewing deployments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/review-deployments)：保護条件を満たす前のjob開始とsecret利用を制限する。誤記した未作成環境の自動作成、self-review、bypass、branch・tag制限を区別する。環境名だけで保護されたとは扱わない。機能は契約・公開範囲に依存する。
- [Actions permissions REST API](https://docs.github.com/en/rest/actions/permissions)と[API versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions)：repositoryのworkflow既定設定を読むGETとAPI版`2026-03-10`を採用する。Fine-grained tokenの`Administration: read`は設定確認用で、実jobへ追加する権限ではない。GETからEnvironment、全job、別credentialの実効権限は推論しない。
- [GitHub CLI gh api](https://cli.github.com/manual/gh_api)：`--method GET`、host、版header、出力項目の限定を使う。ローカルのCLI **2.95.0**のversion・helpを確認した。実API取得は未実行。

Workflow先頭のdeny-all、全jobの明示、先に設定したEnvironment、無権限markerを使う確認は本PJの具体化です。GitHub全利用者への唯一の方式、全scopeの最小性、正式準拠にはしません。Checkout例は[既存の固定tool記録](#ref-workflow-reference-tools)のcommitを保持します。実token付与、承認待機・拒否・迂回、設定GET、公開・交換、GHESは未確認です。Provider仕様・scope・委譲先・契約・開始条件が変わった時に再確認します。

## REF-WORKFLOW-DEPENDENCY-001

区分は`repository interpretation`、発行者は本PJ。固定した[旧CICD-001](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/action-sha-pinning)を2026-09-27に確認し、[新control](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)のWORKFLOW-REF-3〜5、教材、[ENG-CICD-004](../engineering/cicd-security/reviewed-workflow-dependency-binding/README.md)へ使います。一次資料の製品挙動は次の記録へ分けます。

採用するのは、直接参照の固定を更新reviewへ結び、固定コード内の追加取得と未確認を別に残し、受入検査の障害・改変・迂回を確認する判断です。変更して採用したのは製品固有の桁数・終了値を実装へ分け、外部参照のない有効なworkflowを入力不足と区別することです。旧行scannerの無変更copy、参照形式からの出所・無害性・全依存固定の推論、自己申告の採用済み証拠は不採用です。

全GitHub構文、remote source・release・脆弱性情報、内側の動的取得、実merge保護はこのローカル検査で確かめません。旧6項目、3 framework関係、旧調査資料ID、実装変更の理由と未確認事項は[移行判断](../docs/MIGRATION_CI_CD.md#workflow-dependency-migration)にあります。

## SPEC-WORKFLOW-DEPENDENCY-REFERENCES

区分は`vendor specification`。発行者はGitHubとDocker。2026-09-27に以下の一次資料本文を確認しました。可変Web文書で固定digestは未記録のため`re-review-required`です。[CICD-001](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)のWORKFLOW-REF-1〜3と、教材・pattern・[実装例](../engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)に使います。

- [GitHub Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)：full-length commit SHA、正規repositoryのcommitの確認、Action sourceのauditを採用。固定だけでコードや内部取得の無害性を確かめたとはしない。
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)：stepのAction、jobのreusable workflow、外部Git参照とcontainer、ローカル`./`とGitHub.comの`$/`を区別する。`$/`のreusable呼出しはGHESで利用できない。全構文のvalidatorは実装しない。
- [Organization Actions settings](https://docs.github.com/en/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization)：SHA条件はActionへ適用され、reusable workflowのtag参照は残ることを採用。全workflow参照をpolicyだけで固定したと扱わない。実適用はSOURCE-006へ渡す。
- [Docker image pull by digest](https://docs.docker.com/reference/cli/docker/image/pull/#pull-an-image-by-digest-immutable-identifier)：digestで内容を選び、更新時にdigest変更が必要という判断を採用。Containerの出所、実行時取得、job container・serviceの管理を、Git参照の確認で代替しない。

40桁SHAと64桁sha256、対象keyの列挙、失敗時のCI停止は、この製品例での具体化です。全製品の不変条件やframeworkへの正式準拠にしません。Actions policy・構文・対象製品が変わった時は再確認します。Live実行、provider設定、全依存の取得・reviewは未確認です。

## REF-WORKFLOW-REFERENCE-TOOLS

区分は`tool implementation reference`。[Python実装例](../engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)の取得・解析・修正手順に使います。確認日は2026-09-27です。

- PyYAML project、[6.0.3 release](https://pypi.org/project/PyYAML/6.0.3/)、[公式release metadata](https://pypi.org/pypi/PyYAML/6.0.3/json)、[parser documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)。MIT License。採用は`compose`と`BaseLoader`でnode treeを読み、Python objectを構築しない方式。CPython 3.10〜3.14のLinux glibc x86_64／arm64・macOS Intel／Apple Siliconの20 wheel hashをrequirementsへ保持。Linux CPython 3.10 wheelのSHA-256 `9c7708761fccb9397fe64bbc0395abcae8c4bf7b0eac081e12b809bf47700d0b`を実取得物で確認し、hash付きで導入して12件を実行した。他platformとPython版は未実行。
- Shunsuke Suzuki、[pinact v4.1.1](https://github.com/suzuki-shunsuke/pinact/releases/tag/v4.1.1)、source commit [`b1a554a82ef4f55533237e49c19a24ddf0045100`](https://github.com/suzuki-shunsuke/pinact/tree/b1a554a82ef4f55533237e49c19a24ddf0045100)、[固定README](https://github.com/suzuki-shunsuke/pinact/blob/b1a554a82ef4f55533237e49c19a24ddf0045100/README.md)。MIT License。採用は明示したworkflowのGit参照修正を補助するCLI。旧四archive checksumを保持し、Linux x86_64 archive `d1cffebe5704b74e2e5f8a864efb9f7e54768972dc686188c008033fb1797841`と実binary版・helpを確認。既存取得物の再検証であり、他archiveと現在の推奨最新版は確認していない。DefaultのAPI通信・書換えを明記し、自動commit・一括最新更新・cooldown・Docker固定の代替は採らない。実API修正は未実行。
- GitHub、[actions/checkoutの固定commit](https://github.com/actions/checkout/commit/de0fac2e4500dabe0009e67214ff5f5447ce83dd) `de0fac2e4500dabe0009e67214ff5f5447ce83dd`。旧v6.0.2の参照をgate例へ保持し、公式commit pageを再確認。`persist-credentials: false`を使用する。全sourceや推移依存を今回auditしたとは扱わず、live workflowも未実行。

Version・hashだけからtoolの安全性を推論しません。PyYAMLのkey重複・merge・custom tag・循環aliasの扱いは本PJの限定検査方針です。Pinactは修正補助で、直接参照検査や更新reviewの代替ではありません。取得・依存・構文・実行対象が変わった時に再確認します。

## REF-SOURCE-ORGANIZATION-POSTURE-001

[SOURCE-006](../controls/records/source-protection/psb-source-006-source-organization-security-posture/README.md)のORG-POSTURE-1〜7、[教材](../controls/records/source-protection/psb-source-006-source-organization-security-posture/learning.md)、[ENG-SOURCE-006](../engineering/source-protection/organization-baseline-and-drift-review/README.md)で使う設計入力です。区分は`repository interpretation`、発行者は本PJです。元の[GitHub organization governance](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance)を固定revision `f42987759218c9b8daf3924320542a1935ef78e0`で2026-09-27に確認しました。外部規範や組織の導入済み証拠ではありません。製品挙動の根拠は次の`SPEC-GITHUB-ORGANIZATION-POSTURE`へ分けます。

採用するのは、共通方針と必要対象、実grant・実適用、現在状態とaudit、確認のhealth、対応担当を結ぶ判断です。変更して採用したのは、GitHub固定設定の合否から、組織が必要な方針を選び対象へ照合するprovider非依存の問いへ表すことです。個別のID・公開・CI・復旧の意味は既存controlへ戻し、同じ本文を複製しません。

不採用は、Owner 2〜3名、24時間の証拠・失効、90日のreview、180日の保持、30日のcanary、外部協力者のread／triage固定、全Appのwrite禁止、全fork禁止、固定policy floor、自己申告snapshotの`PASS`です。GitHubの契約や用途に応じた確認方法を選び、対象外と取得不能を区別します。旧11 mapping、verifier、runbook、旧資料IDの扱いは[移行判断](../docs/MIGRATION_SOURCE_PROTECTION.md#source-organization-posture-migration)に保持します。

限界は、必要対象や方針自体の正しさ、IdP、provider、収集・通知経路に依存することです。今回の成果は判断材料と具体手順であり、live設定・適用・拒否・収集・通知は未確認です。第三者Appを採用する判断やcollectorの実装を、文書の存在で代替しません。

## SPEC-GITHUB-ORGANIZATION-POSTURE

区分は`vendor specification`、発行者GitHub。[SOURCE-006](../controls/records/source-protection/psb-source-006-source-organization-security-posture/README.md)と[GitHub手順](../engineering/source-protection/organization-baseline-and-drift-review/implementations/github/README.md)で使います。2026-09-27に公開Web本文を確認しました。GitHub.com／Enterprise Cloud `latest`の可変文書で、固定digestは未記録のため`re-review-required`です。REST API版は**2026-03-10**、CLIはローカルのGitHub CLI **2.95.0**のversion・helpも確認しました。

- [Base permissions](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/setting-base-permissions-for-an-organization)：memberの初期権限、個別grant、outside collaborator、internal visibility、private forkの変更範囲を区別する仕様。
- [Organization Actions settings](https://docs.github.com/en/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization)：上位enterprise方針、対象repository・Action、full-length SHA、forkの権限とsecret、token既定値を扱う。Workflowの`permissions`で権限を変更でき、SHA条件はreusable workflowのtag参照を拘束しないことを確認した。
- [Custom security configurationの適用](https://docs.github.com/en/code-security/how-tos/secure-at-scale/configure-organization-security/establish-complete-coverage/apply-custom-configuration)：新規作成用defaultと移管先での別途適用、既存・archive対象、設定した項目の強制範囲を判断する。
- [Configuration statuses](https://docs.github.com/en/code-security/reference/security-at-scale/configuration-statuses)：適用、処理中、失敗、enforcement、設定衝突、detachを区別する。名前が表示されるだけで全設定の継承を判断しない。
- [Audit logの確認](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization)：変更カテゴリ、期間・filter、exportの制限、APIの契約条件を扱う。Provider内の保持と、組織が選ぶ独立した保存期間を同一視しない。
- [Get an organization](https://docs.github.com/en/rest/orgs/orgs#get-an-organization)、[List organization repositories](https://docs.github.com/en/rest/repos/repos#list-organization-repositories)、[pagination](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api)：固定IDと一覧のGET。Repository一覧はtokenの可視範囲に依存し、全organization詳細には認証したOwnerが必要なことを確認した。
- [API versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions)、[gh api](https://cli.github.com/manual/gh_api)：版の指定、明示したGET、page取得、結果抽出の仕様。CLIのhelp確認は実API収集の証拠ではない。
- [Appの申請・インストール制限](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/limiting-oauth-app-and-github-app-access-requests-and-installations)、[OAuth Appアクセス制限](https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/about-oauth-app-access-restrictions)、[Organization PAT方針](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization)：2026-09-30に現行Web本文を追加確認。Appの申請・インストール制限、OAuthの以前の承認が再有効化で戻ること、PAT最大有効期間方針によるmemberのtokenのアクセス拒否とtoken失効が別であることを区別する。組織での実挙動は未確認。

採用するのは、既定値と強制、共通設定と個別status、必要対象とAPIの可視範囲を区別して実値を読み返す判断です。変更して採用したのは、providerの機能一覧を全有効化の要求にせず、採用先の項目・対象・担当へ絞ることです。不採用は、APIの`null`を無効・良好に変換すること、全page取得を必要対象の完全性へ自動変換すること、設定scoreやsample JSONからlive導入を判断することです。

契約、security機能、上位policy、identity方式で利用できる設定と必要権限が変わります。GitHub Enterprise ServerやGHE.comへ自動適用せず、UI・APIが将来変わる場合は再照合します。Live拒否・適用・収集・IdP・audit配送・通知は未確認です。原文を転載せず要約とlinkだけを置き、Web資料の再利用licenseは個別未確認です。

## REF-REPOSITORY-RECOVERY-001

[SOURCE-005](../controls/records/source-protection/psb-source-005-repository-recovery-independence/README.md)のRECOVERY-1〜6、[教材](../controls/records/source-protection/psb-source-005-repository-recovery-independence/learning.md)、[ENG-SOURCE-005](../engineering/source-protection/independent-repository-backup-and-restore/README.md)の直接の設計入力です。公開Web文書は2026-09-26に確認しました。GitHub Enterprise Cloudの`latest`とAWSのWeb資料は可変で、固定digestを収録していないため`re-review-required`です。

- 発行者GitHub、[削除・移管権限](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/setting-permissions-for-deleting-or-transferring-repositories)：repository adminを持つmemberの削除・移管を、organization ownerだけに限定する設定。Ownerの破壊権限をなくす資料ではありません。確認時には柔軟なrepository policyがpublic previewとして案内されていましたが、本例の実装対象にはしません。
- 発行者GitHub、[rulesetのrule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)：対象branch・tagの削除制限、force push制限、bypass主体を扱う製品仕様。Repository自体の削除防止と別の境界であり、利用planと対象の公開範囲にも依存します。
- 発行者GitHub、[repositoryのbackup](https://docs.github.com/en/repositories/archiving-a-github-repository/backing-up-a-repository)：Git mirrorとLFSの別取得、wiki、metadataのarchive等の保存範囲を判断する資料。確認時のmigration archiveにはLFS・discussions・packagesが含まれず、GitHub上でarchiveをrestoreするsupported・documentedな方法も示されていません。Archiveの取得を復元可能性の証拠にしません。
- 発行者AWS、[S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)：versioning、object version単位の保持、COMPLIANCEとGOVERNANCEの違い、bypass、delete markerの製品仕様。保護versionへの削除と、新version・delete markerの追加を区別します。特定modeを全組織の要件にしません。
- 発行者NIST、[SP 800-61 Rev.3（2025年4月最終版）](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r3.pdf)のRC.RP-02・03・05：2026-09-30に公式PDF本文を確認。復旧の対象と方法を選び、復旧用資産・復元後の資産を侵害の兆候、破損、整合性の問題から確認する考え方をRECOVERY-5の入力にしました。Gitの世代選択手順、ref比較、合格値をNISTが定めたとは扱いません。
- 旧[repository destruction recovery](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/repository-destruction-recovery)：固定revision `f42987759218c9b8daf3924320542a1935ef78e0`。製品の必要対象、RPO・RTO、独立した保持世代、開発再開の問いを採るリポジトリ内の解釈であり、組織導入や外部規範の証拠ではありません。

採用するのは、破壊権限を絞ること、保存範囲を明示すること、世代を破壊から守ること、実際に戻せるかを確認する判断です。変更して採用したのは、GitHubから独立した保管という主題をprovider非依存の権限・障害境界へ表すこと、Git復元と設定・関連データを含む開発再開を分けることです。必要対象・鍵・復旧用ID、取得時点の照合、変更経緯からの世代選択、旧workflowを実行する前の確認は本PJの設計解釈です。外部資料がその全手順を規定したとは扱いません。

不採用は、同じ管理権限のprivate forkだけを独立backupとすること、最新mirrorだけを保持すること、四半期等の固定間隔、特定のObject Lock mode、exportの取得成功をrestore成功へ変換することです。Live設定、保持・削除拒否、LFS・metadata復元、鍵・accountの独立性、製品の開発再開は未確認です。旧framework関係は[移行判断](../docs/MIGRATION_SOURCE_PROTECTION.md#repository-recovery-migration--参照と旧framework関係)に記録し、自動継承しません。原文は転載せず要約とlinkだけを置き、各Web資料の再利用licenseは個別未確認です。

## REF-GIT-MIRROR-RECOVERY-001

[Git mirror実装例](../engineering/source-protection/independent-repository-backup-and-restore/implementations/git-mirror/README.md)とRECOVERY-5の限定的な仕様根拠です。発行者Git Project、参照版は[git-clone 2.47.0](https://git-scm.com/docs/git-clone/2.47.0)と[git-fsck 2.47.0](https://git-scm.com/docs/git-fsck/2.47.0)。2026-09-26に確認しました。実行した版はGit **2.47.2**、Linux、Bash **5.2.37**、Python **3.10.4**です。Tool本体やmanualを収録しません。

採用した仕様は、mirrorがrefを写すこと、通常のlocal cloneがobjectをhard linkし得ること、`--no-local`がGitの転送経路を使うこと、`--no-hardlinks`、`--reject-shallow`、bare cloneとtemplate、`fsck --full`によるobjectの整合性確認です。`--shared`や`--reference`で元のobjectへ依存する選択は採りません。

本PJの解釈として、取得時のbranch・tagのobject IDと復元後のIDを別に照合し、元の接続設定を外し、使い捨て対象で七つの代表経路を観測します。`fsck`だけで製品の必要対象を判断しません。Git仕様は保管先の独立権限・保持・真正性、サービス側のmetadata、LFS実体、RPO・RTO、開発再開を定義しません。確認した実装もその限定範囲を超える成功証拠にしません。

## REF-DEVELOPMENT-WORK-BUDGET-001

開発agentの一作業の利用量と、次の実行前の停止を設計する入力です。[AI-007](../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md)のDEV-BUDGET-1〜6と[設計パターン](../engineering/ai-development-security/development-work-budget-gate/README.md)で使用します。2026-09-26確認。以下のOWASP Web資料は可変で、今回固定digestを記録していないため`re-review-required`です。

- OWASP Cheat Sheet Series、[AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)：無制限の反復による費用消費、token・費用・retry・tool-chainの制限、利用量と異常の監視を扱う汎用agentガイダンス。規範要件や製品挙動の証拠ではありません。
- OWASP Cheat Sheet Series、[Secure Coding with AI](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html)、Section 5：開発agentの実行環境を隔離し、CPU・memory・disk・process数を制限する開発向けガイダンス。環境の資源制限とAPI利用予算を区別するために使用します。
- 旧[AI-007のcontrol・合成検査](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-resource-budget-monitoring)：固定revision `f42987759218c9b8daf3924320542a1935ef78e0`、旧レビュー2026-08-05。累積量、独立した停止、結果不明、並列予約という問いの履歴です。外部製品の実効性を示す資料ではありません。

採用するのは、反復する呼び出しを有限にし、利用量と異常を独立して扱う判断です。本PJの解釈として、session単位から責任を持つ開発作業へ範囲を絞り、再開・子作業・実行中の予約と強制点を明示しました。残り予算の不可分な予約、料金不明時の制限、終了処理の有限な枠は、本PJの設計判断であってOWASPの固定仕様ではありません。旧閾値、特定providerの組合せ、警告だけの停止、fixtureの`PASS`は採用しません。製品AI、provider請求、live利用量・停止・通知の効果は未確認です。旧framework関係と旧資料IDの扱いは[移行判断](../docs/MIGRATION_AI_DEVELOPMENT.md#development-work-budget-migration)へ保持します。

## REF-LINUX-PROCESS-DEADLINE-001

[Linux timeout例](../engineering/ai-development-security/development-work-budget-gate/implementations/linux-timeout/README.md)で使用する製品仕様です。発行者はGNU Project、[GNU coreutilsのtimeout manual](https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html)は2026-09-26に検索結果の公式本文を確認しました。可変manualは9.11表記で`re-review-required`です。実行した対象はDebianのGNU coreutils **9.7**（package **9.7-3**）で、ローカルの`timeout --version`・`timeout --help`と六件のprocessテストを確認しました。ToolはGPLv3+であり、tool本体を本PJへ転載しません。

TERMとKILL猶予、終了コード、`0`による期限無効化、`--foreground`での子processの非対象、KILLの終了コードだけでは停止対象を識別できない点を採用します。実装例では非対話の同じprocess groupに限定し、具体的な時間は説明用の値として使います。対話agent、離脱したprocess、親終了後のbackground処理、別job、遠隔処理を停止済みとは扱いません。Provider費用やtoken・toolの予約仕様をこの資料から補完しません。

## REF-DEVELOPMENT-GUIDANCE-001

開発agentのrepository所有指示を変更・評価するための設計入力です。[AI-001](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)のDEV-GUIDE-1〜5、[設計パターン](../engineering/ai-development-security/repository-agent-guidance-review/README.md)、[GitHub例](../engineering/ai-development-security/repository-agent-guidance-review/implementations/github-codeowners/README.md)に使用します。次のWeb資料を2026-09-26に確認しました。固定digestを記録していない可変資料は`re-review-required`です。

- OWASP Cheat Sheet Series、[Secure Coding with AI](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html)：開発agentのrules fileを持続する変更入力として扱い、変更レビュー、予期しない編集の確認、AI生成テストの独立した検査を勧める開発向けガイダンス。規範要件や製品仕様にはしない。
- OWASP Cheat Sheet Series、[AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)：tool権限と指示を分離し、高影響操作を独立に承認するガイダンス。固定版は[commit `9feea5a6b5afdeb3277ad5f49262a62f86e018fb`](https://github.com/OWASP/CheatSheetSeries/blob/9feea5a6b5afdeb3277ad5f49262a62f86e018fb/cheatsheets/AI_Agent_Security_Cheat_Sheet.md)。現行Web版との全文同一性は未確認。
- GitHub公式の[CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)、[protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)、[ruleset rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)：GitHub.comの所有者指定、PR承認、bypassと再レビューの製品仕様・設定候補。対象repositoryの実効設定や承認結果の証拠ではない。
- 旧[AI-001記録と合成benchmark](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/repository-owned-ai-security-guidance/README.md)：`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、旧レビュー2026-08-05。変更の追跡、独立した意味の確認、安全と作業達成の分離という問いを履歴として採用。実agentの有効性を示す一次資料ではない。

採用するのは、指示の変更と効果の判断を分け、変更のレビューを保護された受入経路へ結び、比較時の条件と採点者を明示する考えです。本PJの解釈として、旧単一bundle・SHA-256、固定課題数や数値閾値を共通controlから外し、agentが実際に読んだ版と正当な開発作業を確認する条件へ変えました。Hashの一致、AI自身が作った承認記録、同じagentのテスト成功、合成結果を独立した実効証拠にはしません。GitHub設定例の実効性、開発agentの読込み、モデル挙動、製品AIの安全性は未検証です。旧framework関係の非継承は[移行記録](../docs/MIGRATION_AI_DEVELOPMENT.md#repository-agent-guidance-migration)に残します。

## REF-DEVELOPMENT-INPUT-TRUST-001

開発agentが読む内容と作業指示・実行権限を分けるための設計入力です。[AI-003](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)のDEV-CONTENT-1〜5と[設計パターン](../engineering/ai-development-security/untrusted-development-content-boundary/README.md)で使用します。次の公開資料を2026-09-26に確認しました。Web版は可変で、固定digestを記録していないため`re-review-required`です。

- OWASP Cheat Sheet Series、[Secure Coding with AI](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html)：開発agentが読むIssue、PR、README、error出力、依存の変更履歴、Webの内容を未信頼入力として扱う開発向けガイダンス。出所とレビューの選択に使用。
- OWASP Cheat Sheet Series、[AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)：外部資料の区別、tool権限の限定、高影響操作の明示的な認可、認可をmodel出力だけに頼らない設計のガイダンス。関連部分は固定版[commit `9feea5a6b5afdeb3277ad5f49262a62f86e018fb`](https://github.com/OWASP/CheatSheetSeries/blob/9feea5a6b5afdeb3277ad5f49262a62f86e018fb/cheatsheets/AI_Agent_Security_Cheat_Sheet.md)にも遡れる。固定版と現行Web版の全文同一性は未確認。
- OWASP Gen AI Security Project、[LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)：外部のfileやWebからの間接注入と、内容の分離・権限制限・人の承認を説明するリスク資料。製品AI向けの記述から開発環境に当たる攻撃経路だけを選別。
- 旧[AI-003 controlと合成検査](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/prompt-document-injection-containment/README.md)：`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、旧レビュー2026-08-05。シナリオと「拒否後も正当な作業をする」という問いを歴史的入力として使用。外部製品の現在の挙動を示す一次資料ではない。

採用した判断は、出所と変更主体の識別、資料から指示への昇格防止、実行側での独立した許可、正当な作業結果の確認です。開発agent向けに絞り、旧6種類の入力・5種類の操作を固定の合格数としない点は本PJの解釈です。Filter、区切り、別modelによる要約は補助であり、単独で実行許可を作る方式は採用しません。旧合成JSONの`PASS`、固定SHA-256、監査の自己申告、旧frameworkの`verifies`を実agentの有効性や準拠へ変換しません。製品別のinstruction優先順位、tool仲介、sandbox、live拒否と作業の正しさは未確認です。

## REF-DEVELOPMENT-RUNTIME-RECONCILIATION-001

2026-09-21の受け渡しレビューでは、旧AI-002のAID-006〜007、AI-004のAAR-011・018・023と、SOURCE-004の認証情報ライフサイクルを突き合わせました。[失効時の責任分界](../engineering/ai-development-security/agent-extension-admission/README.md#失効を実行環境へ渡す)は本PJの統合的な設計判断です。外部規格がこの表や時間上限を規定するという主張ではありません。新規呼出しの拒否と既存処理の停止、認証情報の失効、外部結果の照合を分けています。製品の即時失効・停止機能、同期遅延、offline端末の対応は今回未検証です。

AI-004の記録への再編集時に、AISVS 1.0の固定commit `78775233666a2022dcfb82037e5e029116955c00`の[C9](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)と[C10](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)を2026-09-20に確認しました。対象はC9.2.1・C9.2.8・C9.3.1・C9.5.1・C10.1.2です。C9.2.8の暗号学的結合は方式依存のため保留、他の4件も開発環境の設計部分への対応です。旧`verifies`とconfidenceは履歴であり、実検証を意味しません。
2026-10-04には同じ固定版の本文と現行特性を再照合しました。C9.2.1の人による実行前承認、C9.3.1のtool・plugin隔離、C9.5.1のtoolと引数の実行時認可、C10.1.2のMCP server許可リストを、AI-004の部分的な設計関係に限って採用します。C9.2.8は承認を要求内容・依頼者・実行文脈・一回限りのnonceへ**暗号学的に**結び付ける要件です。現行controlは方式を限定しないため旧`verifies/high`関係を採用せず、実装を選ぶ際の問いとして残します。いずれも実環境での強制、AISVS要件の達成や準拠は未確認です。

### 役割と参照版

ENG-AI-001〜003の実行時照合・操作認可・通信・監査の追補に使用します。2026-09-20の[旧項目との対応表](../docs/MIGRATION_AI_DEVELOPMENT.md#ai-runtime-migration)が移行範囲の正本です。

- 旧[AI-004 control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/control.yaml)、`product-security-controls@3bfbeb21246bb2f58c55fa5212068805bca1719b`のAAR-012〜021、025〜026。旧実装の契約とリポジトリ独自の判断として保持し、現行製品仕様とは扱いません。
- MCP公式[Tools specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)、2026-09-20確認。Tool一覧のpagination・変更通知、annotationsの信頼、入力検証・アクセス制御・監査に関する記述を参照。版付きURLですが取得物の固定digestは未記録のため`re-review-required`です。
- [拡張審査の固定資料](#ref-agent-extension-admission-001)、[操作認可](#ref-development-action-authorization-001)、[隔離](#ref-development-runtime-isolation-001)の参照版・採否を継承し、重複した仕様一覧を作りません。

### 採否・変更・限界

MCPの未信頼serverによるannotationsを許可判断へ昇格させず、tool追加時に再照合する判断を採用します。定期照合と未確認toolの拒否は本PJの運用設計です。Protocolへの対応だけで実装の安全性や完全な棚卸しを保証しません。
旧版の確認回数、1時間の鮮度、SQLite、公開HTTPS限定profile、固定した署名方式は普遍化せず、目的に応じた方式・閾値と実際の強制確認へ分けます。旧仕様や設定は削除しません。
通信許可と情報の送信許可、署名の正しさと収集データの真実性、事前判断と外部実行結果を区別します。Path制限にはその情報を確認できる強制点が必要であり、ホスト照合だけで実現したとは扱いません。
旧fixtureの成功、署名付きの合成snapshot、配送receiptを本番の採用証拠へ変換しません。製品adapter、暗号検証、実通信、中央ログ、通知先への配送は今回実行していません。

## REF-DEVELOPMENT-RUNTIME-ISOLATION-001

[ENG-AI-003](../engineering/ai-development-security/development-runtime-isolation/README.md)の設計入力です。2026-09-20に整理しました。

Codex CLI固有の追加観点と、製品仕様との照合結果は[REF-CODEX-CLI-HARDENING-001](#ref-codex-cli-hardening-001)に分けます。Claude Codeの設定がCodexにも効くとは推定しません。

- 旧[AI-004の記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/control.yaml)、`product-security-controls@3bfbeb21246bb2f58c55fa5212068805bca1719b`のAAR-001〜007を継承。隔離、保護対象、認証情報、通信、公開承認、迂回禁止、管理方針の優先を設計へ再配置しました。AAR-005の公開承認の詳細はENG-AI-002へ渡します。
- [okdtとOWASPの固定版記録](#ref-agent-extension-admission-001)を保持。okdtのcommit `ffee64dfc818a5cd024628c1523d857685e0cc14`、OWASPのcommit `9feea5a6b5afdeb3277ad5f49262a62f86e018fb`、各CC BY-SA 4.0、旧レビュー2026-07-29を継承します。製品固有例を他のagentへそのまま適用しません。
- Anthropic公式[Sandboxing](https://code.claude.com/docs/en/sandboxing)、2026-09-20確認、可変資料のため`re-review-required`。OS境界と承認の違い、隔離を使えない場合と例外経路の確認が必要なことを設計入力にしました。設定例や既定値は移植せず、他製品への挙動推定もしません。

旧サンプルのダミー認証情報パスを守る条件は、実環境のファイル・環境変数・サービスへの到達経路を調べる設計へ広げました。これは本PJの解釈であり、旧fixtureがその全範囲を検証したという主張ではありません。
Hookや指示だけを隔離とする方式、隔離障害時の無制限な続行、許可ホストなら任意の情報を送信できるという判断は採用しません。
製品adapter、実際の拒否試験、端末全体の防御は未移行または未確認です。詳細な宛先制御AAR-020〜021とframework mappingは旧記録に保持します。

## REF-CODEX-CLI-HARDENING-001

- 区分: `user-supplied-input`。Riotaro OKADA / okdtの[Codex CLI Hardening Cheatsheet](https://github.com/okdt/codex-cli-hardening-cheatsheet/blob/c356693e8f2ef8b0048a4d4feb2e5c9a6d9fe112/Codex_CLI_Hardening_Cheat_Sheet.ja.md)、commit `c356693e8f2ef8b0048a4d4feb2e5c9a6d9fe112`、v1.3・検証対象Codex CLI 0.146.0（2026-08-03）、CC BY-SA 4.0、2026-10-01確認。コミュニティの設定ガイドであり、OpenAIの仕様書ではない。
- 利用先: [AI-004の教材](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/learning.md)と[隔離設計](../engineering/ai-development-security/development-runtime-isolation/README.md)。Claude Code版と並ぶ製品別の入力として、trusted repositoryの設定優先順位、shell以外の通信経路、ローカル履歴・設定に残る情報を確認する問いを採用する。Controlの新要件や組織での導入証拠には変換しない。
- 公式仕様との照合: OpenAIの[Config basics](https://developers.openai.com/codex/config-basic)と[Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)、[Configuration reference](https://developers.openai.com/codex/config-reference)を2026-10-01に確認。Trusted projectの`.codex/config.toml`はuser configより優先され、untrusted projectではproject-scoped `.codex/`層が読み込まれない。管理requirementsは通常設定と別の強制層を持つ。`history.persistence`は`history.jsonl`への保存を扱う。これらは導入するclient・版で再確認する。
- 変更・不採用: チートシートのテンプレートや設定値を普遍的な安全構成として移植しない。特に同資料に残る`approval_policy = "untrusted"`は、確認時点の[公式案内](https://developers.openai.com/codex/enterprise/managed-configuration#migrate-the-retired-untrusted-approval-policy)では廃止されている。`allowed_approval_policies`内の`untrusted`との違いも含め、現行の仕様と実効設定を優先する。`AGENTS.md`などの指示文、hook、shellのネットワーク制限だけを全経路の強制と見なさない。
- 限界: この追加ではCodexを起動して実効権限、Web検索・MCP・hookの通信、履歴ファイルや承認拒否を検証していない。Claude Code版との機能同等性も主張しない。

## REF-DEVELOPMENT-ACTION-AUTHORIZATION-001

### 役割・参照版

[Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md)と[教材](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/learning.md)の設計入力です。開発環境に限定します。

- OWASP Cheat Sheet Series、AI Agent Security Cheat Sheet：固定版は[拡張審査の資料記録](#ref-agent-extension-admission-001)のcommit `9feea5a6b5afdeb3277ad5f49262a62f86e018fb`、CC BY-SA 4.0を継承。2026-09-20に[現行公開版のHuman-in-the-Loop Controls](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html#4-human-in-the-loop-controls)も確認。公開版は可変であり`re-review-required`、固定版との全文一致を確認した意味ではありません。
- 旧[AI-004 control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/ai-coding-agent-runtime-hardening/control.yaml)、`product-security-controls@3bfbeb21246bb2f58c55fa5212068805bca1719b`：AAR-008〜011、AAR-022〜024の設計判断を再編集。これはリポジトリ独自の解釈と合成検証の契約であり、製品仕様ではありません。
- OS隔離を前提とする判断の旧出典は[同資料記録](#ref-agent-extension-admission-001)のokdt固定版`ffee64dfc818a5cd024628c1523d857685e0cc14`へ追跡できます。製品別設定は今回移植せず、現在の挙動も未確認です。

### 採否と限界

採用するのは、提案と実行を分け、承認を特定の対象・引数・期限へ結び付け、再利用と評価失敗を拒否する判断です。
旧資料の設計を開発用の公開・変更操作へ絞り、300秒の固定期限は組織が決める値へ変更しました。Shell経由の迂回、応答喪失時の再送、承認台帳の並行使用は旧AI-004から引き継ぐ設計課題です。
単純な承認済みフラグ、操作名だけのリスク分類、hookだけによる強制、秘密情報を含む監査は採用しません。サンプルコードも移植していません。
資料はガイダンスであり、認可サービス、実行先の重複防止、製品のhook、実環境の監査を検証した証拠ではありません。旧mappingの原記録を保持し、移行先には現在の設計との対応理由と保留範囲を別記しました。

## REF-AGENT-EXTENSION-ADMISSION-001

この資料の利用範囲は[AIを使う開発環境](../docs/SECURITY_SCOPE.md)です。AISVSやAgentic Top 10を参照しても、製品自体のAI securityを本PJの対象へ拡張しません。

### 役割・利用先・参照時点

PSB-AI-002のEXT-1〜7、ENG-AI-001、Reviewing an agent extensionの設計入力です。
2026-09-20に旧資料記録とcontrolの判断を再編集しました。以下の版と確認日は旧レビューの記録であり、製品の現行仕様を再確認した日ではありません。
旧verifierは審査結果の申告や合成benchmarkを照合しており、内容審査の品質・実環境の強制を自動で証明するものではありません。

| 資料・参照版 | 今回採用する判断 | 採用しない範囲・残る確認 |
|---|---|---|
| OWASP Cheat Sheet Series: [AI Agent Security Cheat Sheet](https://github.com/OWASP/CheatSheetSeries/blob/9feea5a6b5afdeb3277ad5f49262a62f86e018fb/cheatsheets/AI_Agent_Security_Cheat_Sheet.md)、commit `9feea5a6b5afdeb3277ad5f49262a62f86e018fb`（2026-06-27）、旧レビュー2026-07-29、CC BY-SA 4.0 | Tool権限の限定、明示的な認可、反復可能な悪用シナリオ評価、機微情報を除いた証拠を設計へ使う | ガイダンスであり検証標準ではない。Input sanitizationや追加model呼出しを認可境界としない。Memory・RAG・予算・multi-agentの推奨は今回の対象外 |
| Riotaro OKADA / okdt: [Claude Code Hardening Cheat Sheet](https://github.com/okdt/claude-code-hardening-cheatsheet/blob/ffee64dfc818a5cd024628c1523d857685e0cc14/Claude_Code_Hardening_Cheat_Sheet.en.md)、commit `ffee64dfc818a5cd024628c1523d857685e0cc14`（2026-04-02）、旧レビュー2026-07-29、CC BY-SA 4.0 | 外部指示の審査から、OS隔離・ファイル・通信制限を実行環境へ引き渡す境界に使う | コミュニティ資料。Command patternやhookだけによる隔離は採用しない。製品固有設定の移植や他clientの挙動推定はしない |
| [GitHub MCP公式資料の固定記録](#ref-ai-004)、commit `3778a41476e31a072430cfee7c5d31c5f72def60`、旧レビュー2026-08-05、MIT | 正規の取得元、tool schema、更新方式を審査し、認証情報と実行権限の担当を分ける | Floating imageや広いscopeを採用しない。固定したsourceがremote serverの稼働内容と同じだとは推定しない。認証方式の現行対応は導入時に再確認 |

変更して採用する点: 旧5件のfixtureの成功を成功状態から外し、実際に読み込む内容へ承認を対応付けられることを保証目標にする。
旧profileのMCP・Skillのinventory照合、plugin・外部promptの`deny-not-installed`は歴史的な実装範囲として残す。
AI-001の比較評価は[設計として移行](../engineering/ai-development-security/repository-agent-guidance-review/README.md)しましたが、旧合成benchmarkを実装や実agentの結果として移していません。AI-004はcontrol記録をガイダンス移行しましたが、実行時強制の実装・導入は未確認です。

分析には[REF-PORTFOLIO-001](#ref-portfolio-001)の外部依存・platform・governanceと、[攻撃段階](#local-supply-chain-attack-stages)の段階3を用いる。これらをEXT特性の検証要件へ変換しない。

## SPEC-MITRE-ATLAS-2026.05

- 区分: `threat-taxonomy`。発行者MITRE。Content release `2026.05`、data format `6.0.0`、旧registryレビュー2026-07-27。
- 固定source: [ATLAS data](https://github.com/mitre-atlas/atlas-data/tree/da9ebf9b66e6902ad97c267e2a20af0bd996a60f)、tag `v2026.05`、commit `da9ebf9b66e6902ad97c267e2a20af0bd996a60f`。
- 対象`dist/v6/ATLAS-2026.05.yaml`のSHA-256: `defd9014c6d5f5954460ef438faea583fcb1830ff81e85709628efb43037cc3a`。旧[registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/mitre-atlas/registry.json)から継承。
- 今回の利用: 2026-10-04に固定版の`AML.T0010.005`と`AML.T0110`を再確認。前者は開発用agent toolの供給経路としてAI-002の部分的な設計関係に採用した。後者は導入済みtoolの後からの汚染を扱うため、AI-002との旧`mitigates/high`関係は採用しない。脅威の説明として保持し、実行時の扱いはAI-004の別レビューで判断する。旧mappingレビュー2026-08-05。
- AI-004での利用: 2026-10-04に上記SHA-256と一致する固定版の`AML.T0053`、`AML.T0086`、`AML.T0097`、`AML.T0098`を再確認。tool呼出し、書込みtoolによる漏えい、toolからの認証情報取得は開発用agentの部分的な設計関係に採用する。`T0086`はメールや文書更新も含むため通信先制限だけへ縮めない。`T0097`は仮想環境・分析環境を見分けて振る舞いを変える攻撃で、管理方針の迂回や隔離からの脱出とは異なる。旧AI-004関係は採用しない。`T0053`への旧`detects`と監査の真正性だけの`supports`も、攻撃行動そのものの検知を示さないため採用しない。
- 限界: 攻撃行動の分類であり、準拠要件や実行時の防御成功を意味しない。移行による完全対応の主張はしない。

## SPEC-OWASP-AISVS-1.0

- 区分: `normative-specification`。発行者OWASP。Version `1.0`、CC BY-SA 4.0、旧registry・mappingレビュー2026-08-25。
- 固定source: [AISVS 1.0](https://github.com/OWASP/AISVS/tree/78775233666a2022dcfb82037e5e029116955c00/1.0)、commit `78775233666a2022dcfb82037e5e029116955c00`、English requirements tree `a8102d4e67cdf92348a32a18bbee2417d633a075`。
- 公式PDF `1.0/dist/AISVS-1.0.pdf`のSHA-256: `ff15584843a53d4fd2b52940c98cb15f9ebe1340151d90d54bb74db9cf8468f6`。旧[registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/owasp-aisvs/registry.json)から継承。
- 今回の利用: 2026-10-04に固定版の[C10.1 Component Integrity](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-01-Component-Integrity.md)を再確認。`C10.1.1`は信頼できる取得元からのMCP component取得と暗号学的検証、`C10.1.2`は許可リスト内のMCP serverだけを認める要件。AI-002では前者をEXT-1、後者をEXT-7の部分的な設計関係に限り、旧`verifies/high`は採用しない。
- 限界: 取得物の暗号学的検証やserverの実際の拒否は確認していない。AISVS level達成・準拠を主張せず、一般applicationのASVS評価も代替しない。

## 何に使うか

この一覧は「どの外部資料を、どのバージョンで、どう解釈し、何を採用・除外したか」に答えます。
各成果物は、参照資料IDを使って「その資料が、この判断のどこに影響したか」という問いに答えます。

参照資料記録はコントロール要件そのものではなく、組織への導入や準拠の証拠でもありません。
フレームワーク対応関係は[フレームワーク対応関係](../mappings/frameworks.yaml)で別に管理します。

## 参照資料の区分

| 値 | 用途 | 例 |
|---|---|---|
| `normative-specification` | 要件または仕様の正確な意味を確認する | NIST SSDF |
| `threat-taxonomy` | 攻撃者の挙動やリスク分類を整理する | MITRE ATT&CK |
| `vendor-guidance-registry` | 製品固有の安全な構成と、提供元の証拠を解釈する | GitHub Docs |
| `product-specification` | 設定項目、メタデータ、依存関係の解決時の挙動を確認する | npm CLI文書 |
| `implementation-guidance` | 設計・導入候補を発見し、採否を判断する | Dependency Cooldowns |
| `portfolio-analysis-input` | 分野の偏りや空白を横断的に確認する | AwesomeProductSecurity Overview |
| `repository-synthesis` | 複数コントロールを攻撃経路や受け渡しで読み直す | サプライチェーン攻撃コントロール一覧 |
| `user-supplied-input` | リポジトリ利用者が提供した原文を追跡する | 開発端末ハードニング資料 |
| `threat-research` | 攻撃経路と設計上の落とし穴を具体化する | GitHub Security Lab |
| `incident-research` | 脅威シナリオを具体化する | 公開インシデント報告 |

## 利用ルール

1. 公開リポジトリがある資料は、可能な限りコミット、タグ、ダイジェストで固定する。
2. 最新URLしかない資料は、確認日と`re-review-required`を持たせ、固定済みと表現しない。
3. 製品文書を、製品に依存しないコントロールの境界へそのまま昇格させない。
4. コミュニティの一覧は機能発見に使えても、公式な製品仕様の代わりにはしない。
5. 資料の推奨を採用しない場合も、セキュリティ上重要であれば除外理由を残す。
6. フレームワークIDとの関係はマッピングで表し、参照資料記録を準拠マッピングにしない。
7. コントロールや実装例を変更する際、参照する仕様を削除せず、置換先または非採用理由を残す。
8. 資料へのリンクだけで採用済みとせず、どの判断に使い、どこを変更し、何を採用しなかったかを記録する。
9. ポートフォリオ資料と攻撃段階の一覧は、空白を発見する分析軸として使う。表を埋めるために要件や成果物を自動生成しない。

## パイロットで使用する参照資料

### 規範仕様と脅威分類

<a id="spec-owasp-asvs-5-0-0"></a>

#### SPEC-OWASP-ASVS-5.0.0 — Application Security Verification Standard

- 区分: `normative-specification`。発行者OWASP。[ASVS 5.0.0公式release](https://github.com/OWASP/ASVS/releases/tag/v5.0.0_release)、tag `v5.0.0_release`、source commit `5cf9b032440be53ce345ab3c130fda46ba1ce7a2`。[公式English JSON](https://github.com/OWASP/ASVS/releases/download/v5.0.0_release/OWASP_Application_Security_Verification_Standard_5.0.0_en.json)のSHA-256は`bcdbec214d70abcfad9284a31d4f9e5134305831d628aad3aa85d7e26626cb35`。旧[固定registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/owasp-asvs/README.md)から版・digestを継承し、releaseと固定commitを2026-09-26に確認。
- 利用先: [Secure Codingの入口](../controls/records/secure-coding/README.md)と[領域方針](../docs/REPOSITORY_DESIGN.md#secure-codingとasvs)。Web application／web serviceの共通検証要件をたどる基準とする。個別の関係を記録する際は、版を含む`v5.0.0-<chapter>.<section>.<requirement>`で本文とscopeを照合する。[DESIGN-001](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md)ではV8.2.1・V8.2.2の部分関係を設計レビューした。
- DESIGN-001の追加確認日: 2026-09-29。[固定releaseのV8 Authorization](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x17-V8-Authorization.md)で、V8.2.1は機能ごとの明示的権限、V8.2.2は対象データごとの明示的権限を求めると確認。請求書のread／update操作とowner・tenant条件へ限定して`supports / medium / design-reviewed`とし、全endpoint・全データ・組織導入への対応とは扱わない。V8.2.3のfield別権限、V8.3.1の信頼できるservice層、V8.4.1の全tenant操作についてはこの請求書シナリオから対応を主張しない。
- 章案内の追加確認日: 2026-10-05。[固定releaseの目次](https://github.com/OWASP/ASVS/tree/v5.0.0_release/5.0/en)とV1・V2・V4・V13・V15の本文を確認。V1は注入防止と符号化、V2は入力検証と業務ロジック、V4はAPI、V13.3はアプリケーション側のsecret管理、V15は設計・言語固有の問題・並行処理を探す入口として採用する。章の案内は要件の適用判断や診断結果を示さない。
- 変更して採用: ASVSの章や要件を一対一で独自controlへ変換せず、固有の失敗経路、強制点、教材、実装判断を追加する価値がある場合だけ成果物を作る。
- 不採用・限界: ASVS levelの選択、全要件への対応、準拠、組織への導入は主張しない。一般的なsource reviewや非Web製品をASVSだけで覆ったとみなさない。利用者が後日提供する診断チェックリストの内容をASVSから推定しない。

<a id="spec-unicode-source-handling-2"></a>

#### SPEC-UNICODE-SOURCE-HANDLING-2 — Unicode Source Code Handling

- 区分: `normative-specification`。発行者Unicode Consortium。UTS #55 Version 2、Revision 5、2024-01-29。[固定版](https://www.unicode.org/reports/tr55/tr55-5.html)を2026-09-26に確認。
- 利用先: [CODE-005](../controls/records/secure-coding/psb-code-005-unicode-source-review/README.md)の表示・不可視文字・識別子の判断と[pattern](../engineering/secure-coding/unicode-source-review/README.md)。字句構造に沿う表示、不可視文字を見せる選択、表示と処理系の改行のずれを文脈に応じて評価する判断を採用。
- 変更して採用: 付属のPython例は、導入先が選ぶ狭いprofileとして一部の制御文字を拒否する。UTS #55は双方向文字の一律禁止を解決策としていないため、拒否リストを一般要件へ昇格しない。
- 不採用・限界: 例はUTS #55の表示アルゴリズムやconfusable検出を実装しない。言語処理系、editor、review UI全体への準拠も主張しない。
- 追加確認日: 2026-09-29。固定版の§1.2.1と§3.2で、表示側と処理系の改行認識が異なる場合の偽装と、認識しない行末文字をコメント内でも扱う必要を再確認。Python例では表示上の改行候補5種を限定して報告する。

<a id="spec-unicode-security-mechanisms"></a>

#### SPEC-UNICODE-SECURITY-MECHANISMS — Unicode Security Mechanisms

- 区分: `normative-specification`。発行者Unicode Consortium。UTS #39 Version 18.0.0、Revision 34、2026-08-27。[固定版](https://www.unicode.org/reports/tr39/tr39-34.html)を2026-09-26に確認。
- 利用先: [CODE-005](../controls/records/secure-coding/psb-code-005-unicode-source-review/README.md)の識別子profileと[pattern](../engineering/secure-coding/unicode-source-review/README.md)。Confusableとmixed-scriptを別の検出概念として扱う判断を採用。
- 変更して採用: Python例のASCII識別子制限は、UTS #39のGeneral Security Profileやconfusable algorithmではなく、導入先が選ぶ狭いproject policyと明記。
- 不採用・限界: Confusable dataの収集は文字種や版に限界があり、script混在だけを拒否しても全ての紛らわしさは検出できない。例はUTS #39準拠を主張しない。

<a id="spec-python-source-lexical-3-10"></a>

#### SPEC-PYTHON-SOURCE-LEXICAL-3-10 — Python 3.10 lexical analysis

- 区分: `product-specification`。発行者Python Software Foundation。[Python 3.10字句規則](https://docs.python.org/3.10/reference/lexical_analysis.html)と[Python 3.10 tokenize](https://docs.python.org/3.10/library/tokenize.html)、2026-09-26確認。Version付きURLだがページ改訂の固定digestは未記録のため`re-review-required`。
- 利用先: [Python実装](../engineering/secure-coding/unicode-source-review/implementations/python/README.md)。Source encoding宣言と識別子のNFKC解釈、`tokenize`による元の綴り取得を確認。
- 追加確認日: 2026-09-29。§2.1.2–2.1.3でPython 3.10の物理行がLF・CRLF・CRで終わり、コメントは物理行末まで続くことを再確認。U+000B、U+000C、U+0085、U+2028、U+2029を表示上の改行候補として拒否するのは、本PJの限定した実装profileである。
- 変更して採用: PythonはUTF-8以外のencoding宣言やBOMを扱えるが、例はUTF-8 bytesだけを受け入れるproject policy。非ASCII識別子も言語仕様上は有効だが例のprofileでは拒否する。
- 不採用・限界: 別Python版、他言語、review UI、protected CIの挙動をこの資料から推定しない。例はPython 3.10.4でのみ実行確認した。

<a id="spec-github-security-guidance"></a>

#### SPEC-GITHUB-SECURITY-GUIDANCE — GitHubのセキュリティガイダンス一覧

- 区分: `vendor-guidance-registry`
- 発行者: GitHub
- 基準とするコミット: `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`
- 参照コミット日: `2026-07-24`
- 一覧のレビュー日: `2026-07-27`
- 変更不能な参照元:
  [github/docs commit](https://github.com/github/docs/commit/b17436de8f10c3e7f6a185d6813bf94bc82d22f8)
- パイロットで使用する参照ページID:
  - `GHSC-SECURE-ACCOUNTS` — アカウントの保護
  - `GH-ADMIN-CREDENTIAL-TYPES` — GitHubの認証情報種別
  - `GH-ADMIN-SAML-IAM` — SAMLによるIDとアクセス管理
  - `GH-ADMIN-SCIM-ORGANIZATIONS` — 組織のSCIMライフサイクル
  - `GHAS-REF-SECURE-USE` — GitHub Actionsの安全な利用
  - `GHAS-REF-PULL-REQUEST-TARGET` — 権限付きPRイベントの信頼境界
  - `GHAS-CONCEPT-COMPROMISED-RUNNERS` — runner侵害時の影響範囲
  - `GHAS-CONCEPT-OIDC` — OIDCによる交換の流れ
  - `GHAS-REF-OIDC` — tokenのclaimと取得権限
  - `GH-ADMIN-ACTIONS-REPOSITORY` — repository単位のActions設定
- 利用箇所: `PSB-SOURCE-004`／`SRC-AUTH-1..6`、`PSB-CICD-005`／`PR-BOUNDARY-2・3・4`（repository設定のページは`2`のみ）、`PSB-CICD-007`／`RUNNER-1・2・4・5・6`、`PSB-CICD-006`／`FED-2・3`（CICD三件は部分的な設計関係）
- SOURCE-004照合: 2026-09-24に固定commitの4文書を確認。Credential types
  `a32f63447dc398af6c8f4ec19af95557f0e1ea96bf2aca062df99e8ce935a167`、SAML
  `d8a3f3bf0fdcd1594bbb1a46a7d140d54780ba3a674a5a8d094d675f92c8d83e`、SCIM
  `703054c52df8ad431d6201252f83293a884d0ebef47213bdc16ade66f53c575b`は旧registryのSHA-256と一致。
  Account securityは旧registryにhashがなく、今回
  `5def696244c0bc300adf532acdb4d4a40ae0eabd0c218afbc969a028847c3e1b`を記録。
  採否とproperty割当は[SOURCE-004照合記録](../docs/MIGRATION_SOURCE_PROTECTION.md#source-credential-mapping)を参照。
- SOURCE-004追加確認: 2026-09-30にGitHub Enterprise Cloudの可変な公式文書、[組織のSAMLアクセス管理](https://docs.github.com/en/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization)、[fine-grained PATの失効](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-programmatic-access-to-your-organization/reviewing-and-revoking-personal-access-tokens-in-your-organization)、[Enterpriseの認可取消・認証情報削除](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/respond-to-incidents/revoke-authorizations-or-tokens)、[PAT作成](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)、[Contents API](https://docs.github.com/en/rest/repos/contents)を確認。SAML認可の取消は元のPAT・SSH鍵を削除せず、fine-grained PATの失効後もそれを使って作成したSSH鍵は機能し、利用者認証情報への一括操作はGitHub Appインストール用認証情報を含まない。Contents APIの読取りには`Contents: read`を使い、使い捨ての非公開リポジトリ二件で対象制限と失効を確認する手順を[GitHub実装例](../engineering/source-protection/source-access-credential-lifecycle/implementations/github/README.md)へ採用する。可変文書は固定digest未記録で`re-review-required`。旧固定commitの再照合や実環境の拒否確認をした意味ではない。
- CICD-005追加確認: 2026-09-27に下記Web版のSecure use・Securely using pull_request_target・Compromised runnersと、[イベント仕様](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)を確認。Tokenを読取り専用へ絞ること、PRコードの読込み経路、参照secretとrunner資産、イベントとrevisionを別に見る判断を[教材](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/learning.md)・[GitHub例](../engineering/cicd-security/untrusted-pr-boundary/implementations/github-actions/README.md)へ採用。可変Web版の確認日であり、固定registryの改訂や全項目の再照合ではない。Cacheの製品仕様は[SPEC-CI-CACHE-BOUNDARY](#spec-ci-cache-boundary)へ分ける。
- CICD-005追加確認: 2026-09-30にGitHubの[保護branch](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)と[有効なrulesetのrule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)を確認。PR必須条件、対象branch、管理者等のbypassを、`main`へのpushとは別の判断へ採用。レビュー経路を前提にする権限処理は、直接push・bypassで未レビューのrevisionが届かないか確認する。可変Web版の確認であり、採用先の設定や拒否は未確認。
- CICD-005照合: 2026-10-04に固定commitの[Secure use](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/actions/reference/security/secure-use.md)、[pull_request_target](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/actions/reference/security/securely-using-pull_request_target.md)、[runner侵害](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/actions/concepts/security/compromised-runners.md)、[Actions設定](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository.md)を確認。前二者は未信頼コードと権限付き処理、別runの成果物、runner資産との関係を一部採用。設定資料はfork workflowと既定のtoken権限の確認先として`PR-BOUNDARY-2`へ限定。Runner侵害の概説は被害を理解する資料として残すが、`mitigates`の旧関係は非継承。製品資料はレビュー済みrevisionやliveの権限・拒否を証明しない。
- CICD-007照合: 2026-10-04に固定commitの[Secure use reference](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/actions/reference/security/secure-use.md)と公式の[self-hosted runners reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)、[Compromised runners](https://docs.github.com/en/actions/concepts/security/compromised-runners)を確認。前者のrunner group・未信頼job・JIT一job・clean environment・hostのcredentialとmetadataへの到達を、CICD-007の一部へ採用。JITの登録解除はhost・storageの破棄を示さず、外部ログ配送はself-hosted referenceの別の説明である。侵害時の影響解説は脅威の説明として保持し、runner lifecycleを`mitigates`するframework関係としては非継承。組織runnerの設定・実動作は未確認。
- CICD-009照合: 2026-10-04に固定commitのSecure use referenceを再確認。権限付き`pull_request_target`・`workflow_run`で未信頼codeをcheckoutすると、mainと共有するcacheを含む権限境界が危険になるという説明は採用する。ただし、この文書はcacheの保存範囲、`cache-mode`、exact hit、内容検証や「特権jobはcacheを使わない」条件を指定しない。旧`GHAS-REF-SECURE-USE / supports/high`のcache controlへのframework関係は非継承とし、cache固有の仕様は[SPEC-CI-CACHE-BOUNDARY](#spec-ci-cache-boundary)に置く。
- CICD-006照合: 2026-10-04に固定commitの[OIDC概説](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/actions/concepts/security/openid-connect.md)と[OIDC参照](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/actions/reference/security/oidc.md)を確認。概説は仕組みの理解に使い、旧`GHAS-CONCEPT-OIDC / verifies/high`は非継承。参照文書は`audience`・`subject`を受け入れ先の条件へ使う説明と`id-token: write`のjob単位の付与に限り、`FED-2・3 / supports/medium`で採用。Issuerやtokenの期限をclaimとして列挙するだけで、採用先の署名・期限検証やcloud操作権限は確認できない。固定版の本文照合であり、実tokenの発行・交換・拒否は未確認。
- GitHub例の固定Action: [checkout README](https://github.com/actions/checkout/blob/de0fac2e4500dabe0009e67214ff5f5447ce83dd/README.md)、[action.yml](https://github.com/actions/checkout/blob/de0fac2e4500dabe0009e67214ff5f5447ce83dd/action.yml)、[input-helper](https://github.com/actions/checkout/blob/de0fac2e4500dabe0009e67214ff5f5447ce83dd/src/input-helper.ts)、[git-source-provider](https://github.com/actions/checkout/blob/de0fac2e4500dabe0009e67214ff5f5447ce83dd/src/git-source-provider.ts)を2026-09-27に確認。Node.js 24・最低Runner版2.327.1、SHA入力の扱い、認証情報の非保持を採用。Mainへのpush SHAをcheckoutしてHEADと照合する例にし、mergeやpushイベントだけを内容の承認根拠にしない。静的なsource読解であり、配布コード全体の監査や実Action実行ではない。
- 限界: GitHub固有の実装根拠であり、GitHub環境の安全性や正式な準拠を証明しない。SAMLを
  phishing-resistant MFA、SCIMを全credentialとsessionの失効、credential taxonomyを保管・audit要件と解釈しない。

製品文書へのリンク:

- [Best practices for securing accounts](https://docs.github.com/en/code-security/tutorials/implement-supply-chain-best-practices/securing-accounts)
- [GitHub credential types](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/github-credential-types)
- [SAML identity and access management](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on)
- [SCIM for organizations](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization/about-scim-for-organizations)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
- [Compromised runners](https://docs.github.com/en/actions/concepts/security/compromised-runners)
- [Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)

<a id="spec-nist-ssdf-1-1"></a>

#### SPEC-NIST-SSDF-1.1 — NIST SP 800-218

- 区分: `normative-specification`
- 基準とする刊行物: NIST SP 800-218、SSDFバージョン`1.1`、2022年
- 公式資料: [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final)
- 現行mappingで使用する要件ID: `PO.5.2`、`PS.1.1`、`PS.2.1`、`PS.3.2`、`PW.1.2`、`PW.4.1`、`PW.4.4`、`RV.1.1`、`RV.2.1`。初期パイロットのSOURCE-004は`PS.3.1`を使用していたが、2026-09-23の公式本文照合で非継承とし、`PS.1.1`への部分的な設計関係を新規評価した。[SOURCE-004照合記録](../docs/MIGRATION_SOURCE_PROTECTION.md#source-credential-mapping)を参照。`PW.4.4`は2026-10-03にDEPS-003の取得物完全性、`PW.1.2`は同日にGOV-002の例外記録との部分関係を確認
- 利用箇所: `PSB-SOURCE-001 / ENDPOINT-1・2・3・4・7`、`PSB-SOURCE-004 / SRC-AUTH-1〜6`、`PSB-REL-002 / PROV-DIST-1〜7`、`PSB-REL-003 / SBOM-REL-1〜8`、`PSB-DEPS-001`、`PSB-DEPS-003 / DEP-ID-2・3・5`、`PSB-DEPS-004 / DEP-REVIEW-1・2`、Governance／Detectionの各mapping。REL-001の旧`PS.2.1`関係は非継承
- CICD-007照合: 2026-10-04に[PW.6.1の公式本文](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)を再確認。対象はcompiler・interpreter・build toolの安全な機能、更新と完全性であり、runnerの割当・実行環境破棄への旧関係は非継承。旧版と関係は[移行台帳](../docs/MIGRATION.md)に保持
- 限界: マッピングは特定のプラクティスを支援する関係であり、SSDF準拠を意味しない。

<a id="spec-mitre-attack-v19-1"></a>

#### SPEC-MITRE-ATTACK-v19.1 — MITRE ATT&CK Enterprise

- 区分: `threat-taxonomy`
- 基準とするコンテンツのバージョン: `v19.1`
- 公式資料: [MITRE ATT&CK version history](https://attack.mitre.org/resources/versions/)
- 固定取得物: `attack-stix-data` tag `v19.1`、commit `6c3719993d0401de199203ecc3f369544d9e091c`、
  Enterprise STIX SHA-256 `bdf1ce86a4e604214c5076d37ae4dcb322678afc528df8492e6fdc1b554f5da3`。
  2026-09-24に取得hashの一致と`T1078`・`T1552.001`本文を確認。
- パイロットで使用する技術ID: `T1078`、`T1552.001`、`T1552.005`、`T1593.003`、`T1195.001`。CICD-007の旧`T1133`は非継承
- 利用箇所: `PSB-SOURCE-003`, `PSB-SOURCE-004`, `PSB-DEPS-001`、`PSB-DEPS-002`、`PSB-DEPS-003`、`PSB-CICD-007 / RUNNER-5`。GOV-001の旧`detects`は非継承とし、移行台帳に履歴を保持
- CICD-006照合: 2026-10-04に固定版で確認済みの`T1552.001`と[公式の技法説明](https://attack.mitre.org/techniques/T1552/001/)を、`FED-5`に照合。技法はファイル内の認証情報の取得を扱うが、`FED-5`は旧鍵consumerの移行とprovider側の停止が主題で、ファイル内の認証情報の発見・除去を必須としない。旧`mitigates/medium`は現行mappingへ継承しない。旧版と判断は[移行台帳](../docs/MIGRATION.md#2026-10-04cicd-006のframework関係を再照合)に保持
- CICD-007照合: 2026-10-04に公式の[T1552.005](https://attack.mitre.org/techniques/T1552/005/)と[T1133](https://attack.mitre.org/techniques/T1133/)の技法説明を確認。Metadata endpointへのjobからの到達拒否だけを前者の部分的な緩和関係として採用。後者の外部公開されたremote serviceによる初期アクセス・永続化は、runner登録用credentialの分離や緊急管理の別扱いだけでは直接制御できず非継承。公開ページは可変であり、固定STIXの当該2技法の本文hash照合や実環境の拒否試験は未実施
- 限界: 攻撃者の挙動との関係を示すもので、検証要件や準拠要件ではない。SOURCE-004との採否と範囲は
  [照合記録](../docs/MIGRATION_SOURCE_PROTECTION.md#source-credential-mapping)を参照。

<a id="spec-openssf-osps-2026-02-19"></a>

#### SPEC-OPENSSF-OSPS-2026.02.19 — OpenSSF OSPS Baseline

- 区分: `normative-specification`
- バージョン／タグ: `2026.02.19`／`v2026.02.19`
- 参照コミット: `e67ae247ebfb2fd758c9d186335e60cad0a74e78`
- レビュー対象文書のSHA-256:
  `54d13befdb1ae4c63b8612acabc1f0d716874be4187d25801d6ba2d6eee98271`
- パイロットで使用する要件ID: `OSPS-AC-01.01`、`OSPS-BR-01.03`。SOURCE-002で`OSPS-BR-07.01`を追加（2026-09-23に版付き公式本文を確認）。DEPS-004で`OSPS-VM-05.03`の既知脆弱性gateとの部分関係を確認（2026-10-03）。CICD-006で`OSPS-AC-04.02`のjob権限との部分関係を確認（2026-10-04）
- 参照先: [OpenSSF OSPS Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19)
- SOURCE-004照合: 2026-09-24に`OSPS-AC-01.01`のrequirementとrecommendationを確認。
  機微なrepository resourceのreadまたはmodify時のMFAに対し、SRC-AUTH-2はcredential発行・機微変更だけを扱う
  部分対応とした。
- CICD-006照合: 2026-10-04に[AC-04.02](https://baseline.openssf.org/versions/2026-02-19#osps-ac-0402)の本文を確認。CI/CD jobに作業上必要な最小権限だけを割り当てる要件を、`FED-3`のtoken取得権限へ限定して採用。OIDCのissuer・claimや交換後のcloud roleの操作権限まで、この項目が指定すると読まない。
- 利用箇所: `PSB-SOURCE-004`／`SRC-AUTH-2`、`PSB-CICD-005`／`PR-BOUNDARY-2・3・4`、`PSB-DEPS-004`／`DEP-REVIEW-1..3`、`PSB-BUILD-001`／`BUILD-1・2`、`PSB-CICD-007`／`RUNNER-1・4・5`、`PSB-CICD-009`／`CACHE-3・6`（CICD-005・BUILD・007・009は`OSPS-BR-01.03`への部分的な設計関係）、`PSB-CICD-006`／`FED-3`（`OSPS-AC-04.02`のjob権限のみ）
- CICD-005照合: 2026-10-04に[BR-01.03](https://baseline.openssf.org/versions/2026-02-19#osps-br-0103)を現行の`PR-BOUNDARY-2・3・4`へ照合。未信頼コードから特権CI/CD credentialと資産への到達を防ぐ範囲だけを採用。PR全経路の台帳、レビュー済みrevision、特定のeventやcache設定、実環境での拒否を要件本文から推定しない。
- 限界: プロジェクトの成熟度またはOSPS適合性の判定ではない。

<a id="spec-owasp-agentic-2026"></a>

#### SPEC-OWASP-AGENTIC-2026 — OWASP Top 10 for Agentic Applications

- 区分: `threat-taxonomy`
- 基準とする刊行物: `OWASP Top 10 for Agentic Applications 2026`
- 公開日: `2025-12-09`
- パイロットで使用する分類: `ASI02`・`ASI03`・`ASI04`・`ASI05`（AI-004の開発環境に当たる部分）、`ASI04`（AI-002の拡張採用）、`ASI03`（SOURCE-004の開発用agentによるソース管理アクセス）
- 公式資料:
  [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- 成果物metadata: 2026-10-04に公式WordPress APIのmedia ID `52216`、公開日`2025-12-09`、
  PDF size `1,274,186 bytes`、[公式`source_url`](https://genai.owasp.org/wp-content/uploads/dlm_uploads/2025/12/OWASP-Top-10-for-Agentic-Applications-2026-12.6-1.pdf)を再確認。直接取得はHTTP 403で拒否された。[公式PDFの公開経路](https://genai.owasp.org/download/52117/?tmstv=1765059207)の検索索引にあるASI02〜05本文と[公式の公開説明](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)を照合した。公式PDF本体のhashと両公開経路のファイル同一性は未確認。
- 利用箇所: `PSB-SOURCE-004`のGitHub MCP適用時
- 追加利用箇所: `PSB-AI-002`のEXT-1・3・5・6。ASI04が挙げる第三者tool・plugin・指示文の取得、審査、失効を開発用agent拡張に限って採用。旧レビュー2026-08-05の全特性への`mitigates/high`は継承しない。公式PDFの本文確認をPDFの完全性検証と読み替えない。
- AI-004での利用: ASI02の正規toolの誤用、ASI03の継承権限・認証情報の悪用、ASI04の実行時component読込み、ASI05の意図しないcode実行から、開発用agentの実行時境界に当たる部分だけを採用。旧4件の`high`とASI04の`detects`は継承しない。製品AIのagent・model・RAG・A2Aの設計へ対象を広げない。
- 限界: エージェント型AIのリスク分類全体への対応や、AIエージェントの安全性を意味しない。
  SOURCE-004のASI03関係は、開発用agentがソース管理基盤へ接続する場合の認証情報に限り、`SRC-AUTH-1・3・4・5 / mitigates/medium`の部分的な設計関係として記録する。SRC-AUTH-6の監査を緩和に数えず、agent固有identityや下流の操作認可をSOURCE-004へ割り当てない。

### ポートフォリオ分析の入力

<a id="ref-portfolio-001"></a>

#### REF-PORTFOLIO-001 — AwesomeProductSecurityのプロダクトセキュリティ概観

- 区分: `portfolio-analysis-input`
- 状態: `adopted-partially`
- 発行者: DharmaDoll
- 対象: AIおよびエージェント型システムを含む、ソフトウェアライフサイクル全体のプロダクトセキュリティ
- 基準とするコミット: `DharmaDoll/AwesomeProductSecurity@50f2e81f0062de112f7522280e76b92d8849fa1e`
- コミット日: `2026-07-10`
- ソースのSHA-256: `5b524004739bc00eae0faabb0f8c12fc3d37a976249e0650131fce8143903ffc`
- レビュー日: `2026-08-05`
- 変更不能な参照元:
  [Overview.md](https://github.com/DharmaDoll/AwesomeProductSecurity/blob/50f2e81f0062de112f7522280e76b92d8849fa1e/Overview.md)
- 最新の参照先:
  [AwesomeProductSecurity Overview](https://github.com/DharmaDoll/AwesomeProductSecurity/blob/main/Overview.md)
- ライセンス: レビューしたリポジトリでは未宣言。本文を複製せず、参照と独自の分析結果だけを保持する。
- 利用箇所: [横断分析の軸](../docs/ANALYSIS_LENSES.md)、`PSB-SOURCE-004`、`PSB-DEPS-001`、`PSB-CICD-005`

採用した内容:

- アプリケーション、プラットフォームとインフラストラクチャ、運用、PSIRTと脆弱性管理、外部依存と
  サプライチェーン、ガバナンス、教育と文化という七つの観点で、試作版の偏りと空白を確認する。
- モデル出力を信頼済み入力にせず、認可と強制をモデルの外側に置く。この判断は、MCPやAIツールへ
  認証情報を渡した後のツール認可を`PSB-SOURCE-004`の外側に残す根拠の一つとする。
- 本番監視、復旧、ガバナンス、教育の対象内の空白を、技術コントロールの存在で埋めたことにしない。
- 資料が扱うAI application gateway、モデル／データ、RAG、AI製品のTEVVは[Security scope](../docs/SECURITY_SCOPE.md)に従いai-security-foundryの担当とし、本PJの移行待ちへ追加しない。

採用しなかった内容:

- 資料に登場する製品名を、この試作版の必須依存関係にはしない。
- 例示されたKPIや期間を、既定の合格基準にはしない。
- 資料に挙げられたフレームワークを、個別に版と出典を確認せずマッピングしない。

限界:

- 項目単位の参考文献を持つ規範資料ではないため、フレームワーク識別子や準拠主張の根拠には使わない。
- 七つのレイヤーとの対応は、ポートフォリオ上の位置を示すだけで、実装済み、導入済み、十分な対応範囲を意味しない。
- コンテンツフィルターやガードレールモデルは多層防御であり、独立した認可境界の代わりにはしない。

### 旧一覧から引き継いだレビュー済みガイダンス

<a id="ref-cicd-005"></a>

#### REF-CICD-005 — GitHub Actions Best Practice 2025

- 区分: `implementation-guidance`
- 状態: `adopted-partially`
- 発行者・著者: Shunsuke Suzuki
- 発表日: `2025-03-11`、旧レビュー日: `2026-07-30`
- 変更不能な参照元: [発表資料](https://github.com/suzuki-shunsuke/slides/blob/9a323208ecda2b3e27ffe279098537182566cee0/marp/github-actions-best-practice-2025.md)
- 最新の参照先: [GitHub Actions Best Practice 2025](https://suzuki-shunsuke.github.io/slides/github-actions-best-practice-2025)
- 基準版のライセンス: [MIT](https://github.com/suzuki-shunsuke/slides/blob/9a323208ecda2b3e27ffe279098537182566cee0/LICENSE)
- 利用箇所: `PR-BOUNDARY-2`、GitHub Actions実装例。
- 採用した内容: default denyとjob単位のpermission、checkout後にcredentialを残さない設定、full commit SHA、fork PRを未信頼として扱う設計。
- 変更して採用した内容: 個別のGitHub設定をコントロール要件にせず、製品非依存の権限境界とGitHub固有の実装へ分離した。
- 採用しなかった内容: 資料に登場するtool、App、組織全体のremediation手順を、この例の必須依存関係にはしない。
- 限界: 製品挙動は公式仕様とlive runで確認する。性能や開発者体験の推奨は、境界の迂回や確認漏れに関係する場合だけ扱う。

<a id="ref-cicd-010"></a>

#### REF-CICD-010 — Preventing pwn requests

- 区分: `threat-research`
- 旧一覧の状態: `adopted`、新構造での状態: `adopted-partially`
- 発行者: GitHub Security Lab、著者: Jaroslav Lobačevski
- 公開日: `2021-08-03`、旧レビュー日: `2026-07-30`
- 参照先: [Keeping your GitHub Actions and workflows secure Part 1](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)
- 変更不能な公開版: 未特定、`re-review-required`
- 再利用可能な記事ライセンス: 未特定。本文を複製せず、リンクと独自の要約だけを保持する。
- 利用箇所: `PR-BOUNDARY-1`、`PR-BOUNDARY-2`、`PR-BOUNDARY-4`、`PR-BOUNDARY-5`、学習ノート、設計パターン。
- 採用した内容: fork PRと派生成果物を未信頼として扱う。権限イベントでPR headを実行しない。actor、label、古い承認を恒久的な信頼判断にしない。
- 変更して採用した内容: 最初の実装は、metadata-only例外や`workflow_run`を実装せず、無権限のPR検証とmerge後のfresh runへ分ける。
- 採用しなかった内容: 記事のartifact受け渡し例を、そのまま実装しない。受動的なデータにもconsumer側の独立した設計と検証が必要なため。
- 限界: 記事は脅威と設計根拠であり、現在のGitHubの既定値や導入済み状態を証明しない。例の存在をlive evidenceにしない。
- 追加確認: 2026-09-27に上記記事を再確認。学習で問う「正しいrunから届いた形式どおりのデータでも、独立した検査や公開承認を置き換えない」は本PJの解釈として[教材](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/learning.md)へ残す。新しい洞察ファイルや、記事のartifact受渡し実装は作らない。

<a id="ref-ai-004"></a>

#### REF-AI-004 — GitHub MCPの公式な認証・ガバナンスガイダンス

- 区分: `implementation-guidance`
- 状態: `adopted-partially`
- 発行者: GitHub
- 基準とするリポジトリのコミット: `github/github-mcp-server@3778a41476e31a072430cfee7c5d31c5f72def60`
- コミット日／レビュー日: `2026-08-05`
- 基準版のライセンス: MITライセンス
- 変更不能な参照元:
  - [README](https://github.com/github/github-mcp-server/blob/3778a41476e31a072430cfee7c5d31c5f72def60/README.md)
  - [Policies and governance](https://github.com/github/github-mcp-server/blob/3778a41476e31a072430cfee7c5d31c5f72def60/docs/policies-and-governance.md)
- 最新の製品文書:
  [Setting up the GitHub MCP Server](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/set-up-the-github-mcp-server)
- 利用箇所: `SRC-AUTH-1`、`SRC-AUTH-3..6`、GitHub実装例
- 採用した内容: OAuthの優先、範囲を限定したPATによる代替、子プロセスだけへの受け渡し、読み取り専用のツール公開。
- 証明できないこと: IDEでの秘密情報の保存方法、実際の組織ポリシー、実行ファイルの完全性、実行時の認可。

<a id="ref-user-001"></a>

#### REF-USER-001 — 開発端末ハードニングガイドライン

- 区分: `user-supplied-input`
- 旧リポジトリでの状態: `adopted`、パイロットでの利用: `adopted-partially`
- 提供日: `2026-07-28`
- 旧リポジトリの[提供原文](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/user-supplied-endpoint-hardening-guideline-ja.md)
- 外部参考文献／ライセンス: 未提供
- 利用箇所: `SRC-AUTH-2`、`SRC-AUTH-4`、`ENG-SOURCE-002`（2026-09-21追加）、[SOURCE-007の設計入力](#ref-developer-local-credentials-001)。詳細は下の参照資料記録に記載。
- 採用した内容: フィッシング耐性のある認証、保護された鍵／秘密情報の保管、短命な認証情報という考え方。SOURCE-007では原文の`.bashrc`・`.zshrc`・`.env`へのPATやアクセスキーの平文保存を避ける指摘、必要時のsecret managerからの取得、端末に残る長期の値を減らす判断を採用。
- 限界: 開発端末ハードニング全体は`PSB-SOURCE-004`へ統合しない。原文を再配布できるかも未確定。

<a id="ref-developer-local-credentials-001"></a>

#### REF-DEVELOPER-LOCAL-CREDENTIALS-001 — 開発端末上の認証情報

- 区分: `repository-synthesis`。開発者の認証情報を作業領域へ残さない設計の入力。確認日: `2026-10-04`。
- 入力: 利用者提供の[開発端末ハードニング資料](#ref-user-001)の「シークレット管理の仕組み化」を固定した旧版で再確認、旧DEH-001〜003・END-005の[移行記録](../docs/MIGRATION_SOURCE_PROTECTION.md#endpoint-migration)、[OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)、[MITRE ATT&CK T1552.001 Credentials In Files](https://attack.mitre.org/techniques/T1552/001/)（公開版1.3、2026-05-12更新）。OWASPのWeb文書は固定版を確保しておらず再確認が必要。
- 採用: 原文の`.bashrc`・`.zshrc`・`.env`にPATやアクセスキーを平文保存しないこと、secret managerから必要時に取得すること、端末に長期の固定値を残す方式を減らすこと。OWASPから保管と利用時の受け渡しを分ける考え方、MITREからファイル内認証情報を探す攻撃経路を採用。
- 変更して採用: 原文が例示する特定のsecret manager、FIDO2製品、SSH鍵方式、OIDCの短い固定時間を全員の一律要件にしない。利用するサービスが対応する場合に短命な認証や持ち出せない鍵を選び、保管庫から値を渡した後の広がりも確認する。
- 本PJの判断: 再利用できる実際の認証情報を作業リポジトリの`.env`などの平文ファイルへ保管しない。環境変数は保管庫ではなく一時的な受け渡し経路として扱う。これは特定の外部仕様がすべての`.env`を禁止するという主張ではない。
- 非採用: 原文のGit hook、IDE scanner、sandbox、MDM等をSOURCE-007だけで満たしたとみなすこと。これらは別のcontrol・patternまたは導入判断で扱う。
- 利用先: [PSB-SOURCE-007](../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md)、[教材](../controls/records/source-protection/psb-source-007-developer-local-credential-storage/learning.md)、[設計パターン](../engineering/source-protection/developer-credential-storage-and-handoff/README.md)。
- 限界: 開発端末の製品設定、保管庫の実効権限、ログや同期先の網羅性、認証情報の失効を検証していない。SOURCE-004のソース管理側の権限・失効、SOURCE-002の送信前検査、AI-004のagent操作認可を代替しない。

<a id="ref-sensitive-data-repository-001"></a>

#### REF-SENSITIVE-DATA-REPOSITORY-001 — 機密データのリポジトリ受入

- 区分: `repository-synthesis`。旧DEH-010と利用者提供資料を、認証情報以外のデータの受入判断へ再編集した記録。確認日: `2026-10-05`。
- 入力: [旧control](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/control.yaml)の`DEH-010`、[旧実装ガイド](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/check-implementation-guide.md)、[旧baseline](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/operational-baseline.md)の`DEH-010`。旧版の由来は[端末資料の記録](#ref-developer-endpoint-baseline-001)を参照。利用者提供の[原文](#ref-user-001)はGit hookによる「機密情報」のブロックを述べるが、DBダンプ・顧客データの分類や網羅的検出を定義しない。
- 採用: 認証情報用の正規表現だけではDB・アーカイブ等を扱えないこと、ファイルの大きさ・形式・内容を兆候にすること、無害な試験データで拒否を確認し検出内容を表示しないこと。
- 変更して採用: 「コミット前検出」を、データ所有者による持込み可否とGitの全書込み経路での受入判断へ広げる。ローカルhook、受信側の拒否、CIのmerge拒否は到達時点が違うため別に扱う。検査不能は許可にせず、別の置き場か所有者の確認へ戻す。これらは本PJの設計判断。
- 不採用: `sensitive_data_file_guard=required`という宣言、固定した拡張子・サイズのリスト、旧assessmentの状態値を、内容の安全性や実際の強制の証拠とすること。全PIIの検出、全流出経路の防止、特定製品の必須化も主張しない。
- 利用先: [PSB-SOURCE-008](../controls/records/source-protection/psb-source-008-sensitive-data-repository-admission/README.md)、[教材](../controls/records/source-protection/psb-source-008-sensitive-data-repository-admission/learning.md)、[旧項目の対応](../docs/MIGRATION_SOURCE_PROTECTION.md#endpoint-migration--29項目の配置)。
- 限界: 元のbaselineの外部参考文献と再配布条件は未提供。対象組織のデータ分類、保存先、ソース管理サービス、書込み経路と実効的な拒否は未確認。

<a id="ref-developer-endpoint-baseline-001"></a>

#### REF-DEVELOPER-ENDPOINT-BASELINE-001 — Developer endpoint design inputs

- 区分: `repository-synthesis`。利用者提供資料と旧controlの実装ガイドを、端末管理の設計へ再編集した記録。
- 状態: `adopted-partially`。棚卸し日: `2026-09-21`。外部製品の現行仕様を検証した日ではない。
- 参照したリポジトリの版: `3bfbeb21246bb2f58c55fa5212068805bca1719b`。
- 入力を区別して保持:
  - [REF-USER-001](#ref-user-001)の2026-07-28提供原文。製品名は例示で、独立した規範資料ではない。
  - [10項目のCSV](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/developer-endpoint-operational-baseline.csv)と[対応説明](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/operational-baseline.md)。引用元は`source 1`のみで、題名・著者・版・URLは未提供。Phase 2という原入力のラベルを移行順序の根拠にしない。
  - [29項目の実装ガイド](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/check-implementation-guide.md)と[旧metadata](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/control.yaml)。DEH-011はリポジトリ独自の追加で、10項目の原入力へ混ぜない。
- 利用先: [PSB-SOURCE-001](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md)のENDPOINT-1〜8、[ENG-SOURCE-002](../engineering/source-protection/managed-developer-endpoint/README.md)、[教材](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/learning.md)、[29項目の対応表](../docs/MIGRATION_SOURCE_PROTECTION.md#endpoint-migration)。旧DEH-002・END-005の端末上の認証情報は[SOURCE-007の参照記録](#ref-developer-local-credentials-001)へ分けた。REF-USER-001を廃止・改名するものではない。
- 採用: 暗号化、画面ロック、更新、権限、アプリ、バックアップ、EDRの稼働確認、集中管理、物理保護を個人の注意に依存させない設計。
- 変更して採用: 「最新版」をサポート対象・適用期限・例外管理へ具体化。登録済み、現在の観測、アクセス許可を分離し、通知・失効・復旧の責任を接続。通信設定の配布だけを迂回防止と見なさない。これらはリポジトリの設計判断で、外部仕様の要求とは主張しない。
- 不採用: ローカルhookやrequired checkによるあらゆる流出の防止、署名によるコード安全性や端末健全性の保証、遠隔環境への移動による接続元端末保護の省略。特定MDM・EDR・クラウド製品の必須化と、宣言fixtureの成功による導入済み判定も採らない。
- 2026-09-22の追加レビュー: 旧commit `3bfbeb21246bb2f58c55fa5212068805bca1719b`のcontrolと実装ガイドを確認し、直接扱う11項目をENDPOINT-1〜8へ再編集。診断で確認する項目を記載し、実施済みとは扱わない。
- 2026-09-30の追加レビュー: NIST [SP 800-207 Zero Trust Architecture](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf)、2020-08最終版の§3で、管理側の端末状態をアクセス判断へ入力し、policy administratorとenforcement pointが接続の開始・終了を扱う構造を確認。ENDPOINT-1の新規・継続中のアクセスを分ける設計入力として採用する。資産ごとの再評価時点、残存時間、失効方法は本PJの判断であり、同資料の一律の期限や製品要件として扱わない。実端末と資産側の接続・終了は未検証。
- Framework照合: [NIST SSDF 1.1公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)のPO.5.2（本文p.9）、PS.3.1（p.10）、PW.4.1（p.12）を2026-09-22確認。端末保護のPO.5.2を部分的な設計根拠として採用。PS.3.1のrelease保存を端末保護全般へ転用せず、PW.4.1の部品取得は隣接領域に残す。
- 脅威分類の照合: MITRE公式[T1552.001](https://attack.mitre.org/techniques/T1552/001/)・[T1555](https://attack.mitre.org/techniques/T1555/)の公開本文を2026-09-22確認。ファイル・password storeからの認証情報取得は、今回分離した認証情報保管・検査側の境界として扱う。可変ページのため`re-review-required`であり、旧v19.1全体の再検証ではない。旧4件は[対応表](../docs/MIGRATION_SOURCE_PROTECTION.md#endpoint-migration--旧実装とframework-mapping)に原記録と非継承理由を保持する。
- 変更・不採用: PO.5.2の実装例を固定製品・暗号方式・期限の一律要件に変換しない。MFAは認証情報側の責任と接続し、旧4件の対応を新controlへ機械的に割り当てない。診断で確認する項目と状態によるアクセス判断は本PJでの具体化。
- 保留: Linux収集器、製品別設定、実際の通知・隔離・失効・復旧。旧参照仕様は削除せず、対応表から追跡する。
- 限界: 提供資料の外部参考文献と再配布条件は未解決。今回は原文を複製せず参照する。提供原文は複製せず固定した旧版へリンクし、再配布条件は引き続き未確認として保持する。

<a id="ref-deps-001"></a>

#### REF-DEPS-001 — Takumi Guard — 依存パッケージレジストリプロキシ

- 区分: `implementation-guidance`
- 状態: 隣接パターンとして`adopted-partially`
- 発行者: Flatt Security／Shisho Cloud
- レビュー日: `2026-07-31`
- 変更不能な文書の版: 未特定、`re-review-required`
- 最新の参照先:
  - [Takumi Guard](https://shisho.dev/docs/t/guard/)
  - [Quickstart](https://shisho.dev/docs/t/guard/quickstart/)
  - [npm proxy configuration](https://shisho.dev/docs/t/guard/quickstart/npm/)
  - [Limitations](https://shisho.dev/docs/t/guard/limitation/)
- 利用箇所: `PSB-DEPS-001`に隣接する管理プロキシの選択肢。
- 限界: 提供元の遮断一覧は168時間の待機を強制するものではなく、待機期間の代わりにしない。

<a id="ref-deps-004"></a>

#### REF-DEPS-004 — Dependency Cooldownsの運用互換性一覧

- 区分: `implementation-guidance`
- 状態: `adopted-partially`
- 発行者: mprpic／Dependency Cooldownsのコントリビューター
- ライセンス: MIT
- レビュー日: `2026-08-10`
- レビュー対象を変更不能な版で固定していないため、状態は`re-review-required`
- 機能発見に使った資料:
  - [Dependency Cooldowns](https://cooldowns.dev/)
  - [mprpic/cooldowns](https://github.com/mprpic/cooldowns)
- 候補の確認に使用した公式製品仕様:
  - [npm configuration](https://docs.npmjs.com/cli/v11/using-npm/config/)
  - [npm install](https://docs.npmjs.com/cli/install/)
  - [npm ci](https://docs.npmjs.com/cli/commands/npm-ci/)
  - [uv dependency resolution](https://docs.astral.sh/uv/concepts/resolution/)
  - [uv settings](https://docs.astral.sh/uv/reference/settings/)
  - [pnpm dependency resolution settings](https://pnpm.io/settings/dependency-resolution)
  - [Yarn configuration](https://yarnpkg.com/configuration/yarnrc/)
  - [Yarn security features](https://yarnpkg.com/features/security)
  - [pip install](https://pip.pypa.io/en/stable/cli/pip_install/)
- 利用箇所: `DEP-AGE-1..6`、npm実装例。
- 採用した内容: パッケージマネージャー標準の制限、CIの検査、プロキシを区別し、設定の優先順位、
  メタデータ欠落、回避経路を確認する。
- 採用しなかった内容: 補助スクリプトの実行、全体設定の暗黙変更、外部例の時間をポリシー基準にすること。

2026-10-01にDEPS-001のframework関係を再照合しました。ATT&CKの[version 19のT1195.001](https://attack.mitre.org/versions/v19/techniques/T1195/001/)は依存パッケージと開発ツールの改変を含む脅威分類です。待機期間は新しく公開された依存版の早期採用だけを遅らせる設計として採用し、タイポスクワッティング、古い悪意ある版、開発ツールの侵害まで緩和したとは扱いません。NIST [SP 800-218最終版のPW.4.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)は、第三者部品の取得・維持、利用文脈の評価、来歴、承認済み部品、更新を扱います。公開後の最低待機時間は規定していません。本PJでは採用前の時間的な判断を部分的な支援として採用し、出所や内容の評価を代替しません。両者の対象property・残余範囲は[framework mapping](../mappings/frameworks.yaml)を正本とします。

### リポジトリ内で継承する分析資料

<a id="local-supply-chain-attack-stages"></a>

#### LOCAL-SUPPLY-CHAIN-ATTACK-STAGES — サプライチェーン攻撃段階と代表経路

- 区分: `repository-synthesis`
- 状態: `adopted-partially`
- 作成者: このリポジトリ
- 基準とする版: `product-security-controls@511fcb4d0e17a1e177c2bca802d9473233688e16`
- 原文: [`docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md`](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SUPPLY_CHAIN_ATTACK_CONTROL_LIST.md)
- 利用箇所: [横断分析の軸](../docs/ANALYSIS_LENSES.md)、`PSB-SOURCE-004`、`PSB-DEPS-001`、`PSB-CICD-005`

採用した内容:

- 開発端末から検知・復旧までの十二段階を、コントロールの配置と前後の受け渡しを確認する軸にする。
- 「開発ツールからソース改ざん」「悪意ある依存パッケージから本番環境」という代表経路を、
  単一コントロールで終わらない残余リスクの確認に使う。
- リポジトリ内のテスト用データに合格したことと、実環境へ導入済みであることを分ける。

採用しなかった内容:

- 原文にある全コントロールを、この三件のpilotへ移したことにはしない。
- 攻撃段階との関係を、各コントロールの合格条件やフレームワーク対応関係に置き換えない。

限界:

- このリポジトリが編集した横断索引であり、外部の規範資料や脅威分類ではない。
- 段階は調査順序を助けるもので、攻撃が常に同じ順番で進むことや、脅威を網羅することを意味しない。
- 原文の多くのリンク先は試作対象外であり、`experiments/next-repository/`へ移行済みとは扱わない。

### パイロットで使用する製品仕様

<a id="spec-npm-cli-11"></a>

#### SPEC-NPM-CLI-11 — npmの最低待機時間の挙動

- 区分: `product-specification`
- 旧コントロールから引き継いだ実装の最低バージョン: npm `11.10.0`
- 対象設定: `min-release-age`、単位は日
- 公式文書:
  - [npm configuration v11](https://docs.npmjs.com/cli/v11/using-npm/config/)
  - [npm install](https://docs.npmjs.com/cli/install/)
  - [npm ci](https://docs.npmjs.com/cli/commands/npm-ci/)
- 旧レビューで使用したリリース履歴:
  [npm CLI changelog for 11.10.0](https://github.com/npm/cli/blob/latest/CHANGELOG.md#11100-2026-02-11)
- レビュー状態: npm CLIのソースを特定のタグまたはコミットで固定していないため、`re-review-required`。
- 利用箇所: npm実装例、`DEP-AGE-3..5`。
- 限界: 未知の設定キーが保存されることや、`npm config get`に値が表示されることだけでは、
  依存関係の解決時に設定が強制されることを証明しない。

<a id="spec-npm-registry-metadata"></a>

#### SPEC-NPM-REGISTRY-METADATA — npmレジストリのパッケージメタデータ

- 区分: `product-specification`
- 公式資料:
  [npm registry package metadata response](https://github.com/npm/registry/blob/main/docs/responses/package-metadata.md)
- レビュー状態: URLは変更され得る`main`を指すため、本番向け連携を採用する前に、変更不能な改訂で固定する。
- 利用箇所: `DEP-AGE-1`、`DEP-AGE-2`。
- 限界: レジストリメタデータのスキーマを参照しても、レジストリ自体が侵害されていないことや、
  公開時刻の真正性は証明しない。

<a id="incident-context-retained-for-learning"></a>

### 学習用に残すインシデント事例

- `RESEARCH-DEPS-CHECKMARX`:
  [Bitwarden statement on the Checkmarx supply-chain incident](https://community.bitwarden.com/t/bitwarden-statement-on-checkmarx-supply-chain-incident/96127)
- `RESEARCH-DEPS-AXIOS`:
  [Axios npm supply-chain compromise postmortem](https://github.com/axios/axios/issues/10636)

これらは脅威シナリオを具体化する資料です。待機期間のしきい値、製品仕様、コントロールの合格条件は定義しません。

## パイロットの追跡関係

<a id="spec-install-execution-policy"></a>

### SPEC-INSTALL-EXECUTION-POLICY — Install-time executionの製品仕様と設計ガイダンス

- 区分: `product-specification`。下記の横断ガイダンスは実装候補・設計入力として区別する。
- 移行元: `controls/dependency-security/install-script-execution/README.md`と`control.yaml`。
- 利用先: `PSB-DEPS-002 / DEP-EXEC-1..4`、[教材](../controls/records/dependency-security/psb-deps-002-install-execution-policy/learning.md)、`ENG-DEPS-002`、pip実装例。
- 固定改訂: 未特定。変更可能なURLのため`re-review-required`。
- 採用判断: パッケージの取得と準備用コードの実行許可を分け、未承認実行を拒否する。
- 変更して採用: 製品ごとのdefault・設定キーをcontrolの定義にせず、製品別実装へ置く。
- 不採用: 全許可、名前だけのtrustを将来versionの承認にすること、拒否後の無条件source fallback。
- 限界: 製品文書は組織の実効設定、CI配線、実行環境の隔離を証明しない。各リンクの本文は複製しない。

2026-10-02に旧framework関係も再照合しました。[ATT&CK Enterprise v19のT1195.001](https://attack.mitre.org/versions/v19/techniques/T1195/001/)は、改変された依存や開発ツールを通じた侵害を扱います。未承認のinstall時コードを起動しない設計は、このうち依存取得後の準備時実行を妨げ得ます。後続のimport・testや開発ツール自体の侵害は残します。NIST [SP 800-218最終版のPW.4.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)は、安全な第三者部品の取得・維持と用途別評価、来歴、承認済み部品、更新などを扱います。準備処理の実行可否だけでは部品を評価・維持したと説明できないため、旧`supports/high`関係は非継承としました。[移行台帳](../docs/MIGRATION.md)に旧関係を保持します。製品仕様の現在の実効性はこのframework照合では検証していません。

#### pip — 今回確認した仕様

発行者はpip project。公式文書の表示版は`26.2.1`、確認日は`2026-09-16`。
source候補を除外するoptionとhash確認を別の特性として採用する。
build用依存の分離をOS権限のsandboxと解釈しない。直接指定のsource入力やlocal projectを
wheel限定のindex取得経路へ混ぜず、製品設定と入力の両方を確認する。

- [pip install](https://pip.pypa.io/en/stable/cli/pip_install/)
- [Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/)
- [Build System Interface](https://pip.pypa.io/en/stable/reference/build-system/)

ローカルテストの使用版は出力に記録する。上記文書の表示版とテスト環境の版は同一とは限らず、
新しい版を導入する際は再確認が必要。wheelの安全性や後続実行の隔離は保証しない。

2026-09-27にpip install・Secure installsを表示版`26.2.1`で再確認しました。
[`prepare_installed_requirement`](https://github.com/pypa/pip/blob/26.2.1/src/pip/_internal/operations/prepare.py)は、既存のインストール済み依存を満たす場合にhashを照合しない実装です。新しい専用環境を使う[pip手順](../engineering/dependency-security/install-execution-policy/implementations/pip/README.md)へ採用しました。
ローカルの既存4テストはPython 3.10.4 / pip 23.3.1で成功しています。別の使い捨てvenvでは、無害なwheelを入れた後、誤ったhashの入力でも既存状態を再利用する経路をpip 22.0.4で観測しました。どちらも観測版であり、推奨版や26.2.1の実行済み証拠にはしません。

[Python venv](https://docs.python.org/3/library/venv.html)も2026-09-27に表示版3.14.7で確認しました。既定ではbase環境のsite-packagesを分離し、既存directoryは再利用する仕様です。手順では未使用pathを先に確認し、`--system-site-packages`を付けない判断へ採用しています。Pythonの版と同梱pipの版は別に確認し、venvをOSのsandboxとは扱いません。

#### npm、pnpm、Bun — 保持した仕様と次のレビュー対象

以下は旧成果物の参照仕様を保持したもの。今回は現在の製品挙動・版を再確認しておらず、
旧READMEのdefaultや最低versionを新構造へ確定仕様として移さない。
許可機能、許可単位、優先順位、更新時の違いを再確認してから実装例へ移す。

- npm / 発行者npm・GitHub: [npm 12 default変更の告知](https://github.blog/changelog/2026-06-09-upcoming-breaking-changes-for-npm-v12/)、[install-script approvals](https://docs.npmjs.com/cli/v11/commands/npm-install-scripts/)、[lifecycle scripts](https://docs.npmjs.com/cli/using-npm/scripts/)
- pnpm / 発行者pnpm: [Build Settings](https://pnpm.io/settings/build)、[approve-builds](https://pnpm.io/cli/approve-builds)、[supply-chain security](https://pnpm.io/supply-chain-security)
- Bun / 発行者Bun: [install](https://bun.com/docs/pm/cli/install)、[trusted dependencies](https://bun.com/guides/install/trusted)、[bunfig.toml](https://bun.com/docs/runtime/bunfig)

#### 横断ガイダンスとmapping候補 — 省略せず保持

以下は旧成果物から引き継ぐ設計・調査入力。今回は全文再レビューしておらず、追加要件や必須製品へ変換しない。

- OWASP: [NPM Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html)、[Software Supply Chain Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)
- CISAほか: [Recommended Practices for Developers](https://www.cisa.gov/sites/default/files/2023-12/ESF_SECURING_THE_SOFTWARE_SUPPLY_CHAIN_DEVELOPERS.pdf)、旧リンクの版は`2023-12`パス。刊行版・digestを追加確認する。
- OpenSSF OSPS: `2026.02.19 / OSPS-BR-05.01`は旧READMEにあった関連候補。標準package manager利用だけで実行抑止を証明しないため、direct mappingは追加しない。[参照要件](https://baseline.openssf.org/versions/2026-02-19#osps-br-0501)

旧`control.yaml`のATT&CK `v19.1 / T1195.001`、SSDF `1.1 (SP 800-218, 2022) / PW.4.1`は
版・ID・関係・confidenceを保持し、特性への再配置は`migration-review-required`とする。
旧レビュー担当は`product-security`、日付は`2026-07-27`。これは今回のレビュー日ではない。

| 成果物 | 直接参照する資料ID | マッピングが参照する資料ID |
|---|---|---|
| `PSB-GOV-003`、`ENG-GOV-005` | `REF-VULNERABILITY-PRIORITY-001` | `SPEC-NIST-SSDF-1.1 / RV.1.1・RV.2.1` |
| `PSB-GOV-005`、`ENG-GOV-004` | `REF-DEPLOYED-ARTIFACT-RECOVERY-001` | `SPEC-NIST-SSDF-1.1 / RV.1.1・RV.2.1`、`SPEC-MITRE-ATTACK-v19.1 / T1195.002`。旧OSPS関係の非継承理由は移行記録に保持 |
| `PSB-GOV-004`、`ENG-GOV-003` | `REF-CREDENTIAL-EXPOSURE-CONTAINMENT-001` | `SPEC-MITRE-ATTACK-v19.1 / T1078`。旧SSDF・OSPS関係の非継承理由は`MIGRATION_GOVERNANCE_OPERATIONS.md#credential-exposure-migration`に保持 |
| `PSB-SOURCE-003`、`ENG-SOURCE-004` | `REF-PUBLIC-SOURCE-EXPOSURE-001` | `SPEC-MITRE-ATTACK-v19.1 / T1593.003`。旧3件の非継承理由は`MIGRATION_SOURCE_PROTECTION.md#public-exposure-migration`に保持 |
| `PSB-SOURCE-004` | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-AI-004`, `REF-USER-001` | `SPEC-NIST-SSDF-1.1`, `SPEC-MITRE-ATTACK-v19.1`, `SPEC-OPENSSF-OSPS-2026.02.19`, `SPEC-OWASP-AGENTIC-2026` |
| GitHubのソースアクセス認証情報実装例 | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-AI-004` | 同上。ただしMCP利用時に限るマッピングを含む |
| `PSB-DEPS-001` | `REF-DEPS-004`, `SPEC-NPM-REGISTRY-METADATA` | `SPEC-NIST-SSDF-1.1`, `SPEC-MITRE-ATTACK-v19.1` |
| npmの待機期間実装例 | `SPEC-NPM-CLI-11`, `REF-DEPS-004` | コントロールのマッピングを自動継承しない |
| 管理プロキシの選択肢 | `REF-DEPS-001` | 待機期間のマッピングを自動継承しない |
| `PSB-CICD-005` | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-CICD-005`, `REF-CICD-010` | `SPEC-OPENSSF-OSPS-2026.02.19` |
| GitHub ActionsのPR境界実装例 | `SPEC-GITHUB-SECURITY-GUIDANCE`, `REF-CICD-005`, `REF-CICD-010` | コントロールのマッピングを自動継承しない |
| 横断分析 | `REF-PORTFOLIO-001`, `LOCAL-SUPPLY-CHAIN-ATTACK-STAGES` | コントロールやフレームワークの対応関係へ自動変換しない |
| `PSB-DEPS-002` | `SPEC-INSTALL-EXECUTION-POLICY` | `SPEC-MITRE-ATTACK-v19.1 / T1195.001`の準備時実行に限る。旧SSDF `PW.4.1`は非継承 |
| Install execution policy pattern、pip実装例 | `SPEC-INSTALL-EXECUTION-POLICY` | controlのATT&CK関係を自動継承しない |
| `PSB-CONTAINER-005`、`ENG-CONTAINER-003`、Kubernetes実装例 | `REF-WORKLOAD-CONFINEMENT-001` | `SPEC-NIST-SP-800-190 / 4.4.3`。Credential、resource、networkへ自動拡張しない |
| `PSB-CONTAINER-006`、`ENG-CONTAINER-004`、Kubernetes実装例 | `REF-WORKLOAD-NETWORK-SEGMENTATION-001` | `SPEC-NIST-SP-800-190 / 4.3.3・4.4.2`。Kubernetes固有fieldやlive CNI enforcementへ自動拡張しない |
| `PSB-CONTAINER-007`、`ENG-CONTAINER-005`、Kubernetes実装例 | `REF-WORKLOAD-RESOURCE-BOUNDS-001` | `SPEC-NIST-SP-800-190 / 4.4.3`。固定resource値やKubernetes固有のquota・evictionへ自動拡張しない |
| `PSB-CONTAINER-003`、`ENG-CONTAINER-006` | `REF-CONTAINER-HOST-DAEMON-001` | `SPEC-NIST-SP-800-190 / 4.3.1・4.3.5・4.5.1〜4.5.5・4.6`。特定OS／runtime／providerの設定やlive node evidenceへ自動拡張しない |
| `PSB-IAC-001`、`ENG-CONTAINER-007` | `REF-IAC-CHANGE-BOUNDARY-001` | Framework mappingは非継承。特定IaC tool・provider・resource・live stateへ自動拡張しない |
| `PSB-REL-002`、`ENG-REL-002` | `SPEC-PROVENANCE-DISTRIBUTION` | `SPEC-SLSA-1.2 / producer-distributes-provenance`、`SPEC-NIST-SSDF-1.1 / PS.2.1`。Level達成・live配布へ自動拡張しない |
| `PSB-REL-003`、`ENG-REL-003`、CycloneDX限定実装 | `REF-RELEASE-SBOM-LIFECYCLE-001` | `SPEC-NIST-SSDF-1.1 / PS.3.2・RV.1.1`。SBOM完全性、live publication、analysis完了、SSDF準拠へ自動拡張しない |
| `PSB-REL-004`、`ENG-REL-004` | `REF-SUPPLIER-SBOM-INTAKE-001` | `SPEC-NIST-SSDF-1.1 / PW.4.1`。供給者の採用審査、SBOM完全性、live取込、準拠へ自動拡張しない |
| `PSB-REL-005`、`ENG-REL-005` | `REF-ARTIFACT-SIGNING-BOUNDARY-001` | `SPEC-NIST-SSDF-1.1 / PS.2.1`。Cosignを必須製品、署名生成をSLSA Build level、文書をlive署名・公開の証拠にしない |
| `PSB-BUILD-002`、`ENG-BUILD-003` | `SPEC-CONSISTENT-BUILD-PRODUCER` | `SPEC-SLSA-1.2 / producer-appropriate-build-platform・producer-consistent-build・producer-hosted-build-platform`。Producer側設計だけでBuild level達成を主張しない |

<a id="spec-consistent-build-producer"></a>

## SPEC-CONSISTENT-BUILD-PRODUCER — Builder選定と一貫したrelease build

区分はSLSAの`normative-specification`と、このリポジトリのrelease境界への解釈です。[PSB-BUILD-002](../controls/records/build-security/psb-build-002-approved-consistent-build/README.md)、[ENG-BUILD-003](../engineering/build-security/approved-release-build-process/README.md)、教材、[移行記録](../docs/MIGRATION_BUILD.md#consistent-build-migration)の直接の設計入力です。

- 発行者・版: SLSA `1.2`、status `Approved`。既存の[SPEC-SLSA-1.2](#spec-slsa-1-2)と同じtag `v1.2`、commit `19e4e2f005f871270c4f555fc47afecfb37f3efe`。Community Specification License 1.0。
- 2026-09-26に[Build requirements](https://slsa.dev/spec/v1.2/build-requirements)、[Build Track Basics](https://slsa.dev/spec/v1.2/build-track-basics)、[Assessing build platforms](https://slsa.dev/spec/v1.2/assessing-build-platforms)の公式公開版を確認。後者はplatform評価の問いであり、特定platformへの認定証ではありません。
- 追加確認日: 2026-09-28。同じv1.2の三資料でproducer責任と基盤評価の境界を再照合。基盤が記録した入力とproducerが承認した入力の照合を教材へ補い、一貫した手順を毎回同じbytesができる保証とは扱わない。
- 移行元の[旧control](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/build-security/hosted-consistent-build/control.yaml)は固定profileと合成verifierの出発点。採否の詳細は移行記録へ残します。

採用するのは、producerが目標levelに合うbuild platformを選び、verifierが期待値を形成できる一貫したbuild processを用い、Build L2以上ではhosted実行を確認することです。Platform評価ではexternal parameters、control plane、build environments、caches、outputsとbuilder identityの信頼境界を見ます。変更して採用するのは、release用のsource・定義・entry point・重要入力・triggerをproducer期待値へ具体化し、別repositoryの定義やrunごとに変わる承認済み入力を扱えるようにすることです。

不採用とするのは、Build L2固定、同一Git revision・40桁SHA・HTTPS identity・全parameter完全一致・固定trigger名をSLSAの普遍要件とする解釈です。旧JSONの`hosted`や`assessed_slsa_build_level`、形式だけ確認したassessment hashを実platform能力の証拠にしません。Platformによるprovenance生成・認証は[別の仕様記録](#spec-platform-provenance-generation)、配布とconsumer検証も別境界です。文書・mappingの存在はlive実行やBuild level達成を示しません。

<a id="ref-artifact-signing-boundary-001"></a>

## REF-ARTIFACT-SIGNING-BOUNDARY-001 — 成果物署名の生成と配布境界

区分は公式製品ガイダンスと旧controlの再解釈です。[PSB-REL-005](../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)、[ENG-REL-005](../engineering/release-integrity/artifact-signing-boundary/README.md)、教材、[移行記録](../docs/MIGRATION_RELEASE.md#artifact-signing-migration)の直接の設計入力です。

- Sigstore projectの[blob/file署名](https://docs.sigstore.dev/cosign/signing/signing_with_blobs/)、[検証](https://docs.sigstore.dev/cosign/verifying/verify/)、[Cosign取得とrelease検証](https://docs.sigstore.dev/cosign/system_config/installation/)を2026-09-26に確認。可変の公式文書であり、採用するCosign clientの版と実行bytesを固定した記録ではありません。以前のレビュー日は2026-08-10です。
- 追加確認日: 2026-09-28。上記のblob署名・検証文書で、fileとbundle、期待するidentity・issuer、および`--check-claims=false`がpayloadの主張を検証しない点を再照合。対象digest照合を外した署名成功を受入成功へ変換しない設計へ反映。CLIの実行・版の固定・実サービスでの署名確認はしていません。
- [NIST SP 800-218 SSDF 1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)の`PS.2.1`を2026-09-26に確認。これはmappingの根拠であり、controlの全特性や特定製品を規定する資料ではありません。
- [旧PSB-REL-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/artifact-signing-generation/control.yaml)は独自statementと合成fixtureの出発点。現行providerの仕様や導入証拠としては扱いません。

採用したのは、対象の実bytesと署名の結合、署名者を限定するconsumer側の期待値、bundleなどの検証材料を取得可能にする判断です。Cosignのkeyless署名ではcertificate identityとOIDC issuer、bundle中の時刻・透明性証拠が検証に関係することを方式固有の選択として記録します。Cosign binary自身の出所も確認してから使用する設計を採用します。

変更して採用したのは、旧固定5分、Ed25519、full Git revision、KMS/HSM/keyless列挙、公開HTTPSと透明性ログを普遍要件から方式・policy選択へ戻したことです。採用方式に必要な証拠を省く意味ではありません。旧fixtureの`key_exportable: false`、`immutable: true`、`included: true`、`ALLOW`は自己申告なのでlive状態の証拠として不採用です。署名があっても成果物の安全性、build来歴、consumerの受入、SLSA level、組織導入は示せません。

<a id="spec-workload-federation"></a>

## SPEC-WORKLOAD-FEDERATION — GitHub・AWS・OIDCのfederation仕様

- 区分: `product-specification`。OIDC Coreはprotocol仕様、Terraformは実装候補として区別する。
- 発行者: GitHub、AWS、OpenID Foundation、HashiCorp。
- 利用先: `PSB-CICD-006 / FED-1..6`、`ENG-CICD-002`、学習ノート、GitHub Actions / AWS実装例。
- 移行元: `controls/cicd-security/audience-bound-oidc-federation/README.md`と`control.yaml`。
- 今回確認日: `2026-09-16`。GitHub OIDC reference、AWS OIDC role、STS APIを確認。他資料の全文再レビューは未完了。
- 文書の固定改訂: 未特定の製品URLは`re-review-required`。ActionとOIDC Coreは下記の参照版を保持。
- 採用: Token検証、audience・subject、保護job、操作権限と有効期間を別の判断として扱う。
- 変更して採用: 旧AWS例の900秒・account・roleをcontrol全体の固定値にせず、製品別profileへ置く。
- 明確化: 旧長期keyの保管場所の削除と、provider側の失効・旧権限が使えないことの確認を区別する。派生sessionはインシデント対応と接続する。
- 不採用: Token識別子やsynthetic ledgerからAWSのsingle-use replay防止を主張すること、Environment subjectだけでbranch・workflowを固定したと扱うこと。
- 限界: 現在のtrust・Environment・role権限・inventory・交換結果は、live確認なしに導入済みとは言えない。

旧参照仕様を以下へ保持する。今回確認した資料と引き継いだ未再確認資料を混同しない。

- GitHub: [OIDC concept](https://docs.github.com/en/actions/concepts/security/openid-connect)、[OIDC reference](https://docs.github.com/en/actions/reference/security/oidc)、[OIDC REST API](https://docs.github.com/en/rest/actions/oidc)、[deployment environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- AWS: [OIDC role作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html)、[AssumeRoleWithWebIdentity](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html)、[IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html)、[CloudTrail userIdentity](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html)、[STS condition keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html#condition-keys-sts)
- AWS Action: [固定commit e6de054238d6b7531b4efff3b6587d9aade6a06c](https://github.com/aws-actions/configure-aws-credentials/commit/e6de054238d6b7531b4efff3b6587d9aade6a06c)、[project](https://github.com/aws-actions/configure-aws-credentials)。旧例のv6.2.3を保持し、今回runtimeやAction全体を再レビューしたとは扱わない
- Protocol: [OpenID Connect Core 1.0 / errata set 1参照版](https://openid.net/specs/openid-connect-core-1_0-18.html)。Provider固有のclaim対応・session・replayの保証に読み替えない
- Terraform AWS provider: [OIDC provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_openid_connect_provider)、[IAM role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role)、[role policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy)。旧導入候補を保持するのみで、provider pin・lock・実環境planは別途必要

旧framework関係はGitHub固定commitの`GHAS-CONCEPT-OIDC / verifies/high`と`GHAS-REF-OIDC / verifies/high`、OSPS `2026.02.19 / OSPS-AC-04.02 / supports/high`、ATT&CK `v19.1 / T1552.001 / mitigates/medium`。旧レビューは`product-security / 2026-09-06`。[2026-10-04の採否](../docs/MIGRATION.md#2026-10-04cicd-006のframework関係を再照合)ではGitHub参照とOSPSだけを対象を絞って残した。OIDC概説とATT&CKの旧関係は移行台帳に保持し、現行mappingへは継承しない。

2026-09-30にGitHubの[OIDC reference](https://docs.github.com/en/actions/reference/security/oidc)・[再利用workflowのOIDC](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-with-reusable-workflows)とAWSの[OIDC condition keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html)を再確認しました。Tokenのclaim、受け入れ先が実際に条件へ使う値、Environmentやworkflowの保護を分ける判断をCICD-006の診断項目へ採用しました。これらは可変Web版で、固定registryの更新、採用先のtrust設定や交換拒否の確認ではありません。

2026-10-04に旧framework関係4件を固定版GitHub資料、OSPSの版付き本文、ATT&CKの固定版記録と公開本文へ照合しました。GitHub参照とOSPSは一部の特性への設計関係として残し、OIDC概説とATT&CKの旧関係は[移行台帳](../docs/MIGRATION.md#2026-10-04cicd-006のframework関係を再照合)にのみ保持します。旧`verifies/high`は実際の交換や拒否を確認した結果ではありません。

<a id="ref-cicd-009"></a>

## REF-CICD-009 — OIDC・Trusted Publishingの残存リスク分析

- 区分: `threat-research`、状態: `adopted-partially`、発行者: GMO Flatt Security。
- 公開日: `2026-07-02`、旧レビュー日: `2026-07-30`。今回は旧参照記録を移行し、記事全文の再レビューは未完了。
- [原文](https://blog.flatt.tech/entry/2026-github-actions-security-part3)。固定公開版・再利用ライセンスは未特定。本文を複製せず、リンクと独自の解釈を保持する。
- 利用先: `FED-2..4`、学習ノート、pattern。製品claim仕様はSPEC-WORKLOAD-FEDERATIONで別に確認する。
- 採用: 短命化を窃取防止と解釈せず、buildと認証・公開jobを分け、交換後の権限と監査も限定する。
- 変更して採用: Cloud federationとpackage-registry Trusted Publishingを独立した受け入れ境界として扱う。
- 不採用: 旧記録にあるoffline replay契約をAWSのsingle-use保証として残すこと。
- 限界: 旧一覧はoffline contractと記述するが、現行旧controlはlive確認を必要とするmanual reference。記事とfixtureの存在は実環境導入を証明しない。

横断分析にはREF-PORTFOLIO-001とLOCAL-SUPPLY-CHAIN-ATTACK-STAGESを使い、直接の製品仕様・特性根拠と区別する。

<a id="spec-ci-cache-boundary"></a>

## SPEC-CI-CACHE-BOUNDARY — CI cacheの読み書きと内容の信頼

- 役割・発行者: GitHubの製品仕様を直接の根拠とし、周辺資料は設計レビューに使う。
- 版: GitHubのmutableな公式仕様を2026-09-16に確認、2026-09-27にcache referenceとworkflow syntaxを再確認。固定改訂・digestは未特定のため`re-review-required`。旧workflowのruntimeとAction固定値は再検証前の履歴として保持する。
- 利用先: `PSB-CICD-009 / CACHE-1..7`、`PSB-CICD-005 / PR-BOUNDARY-4`、`ENG-CICD-003`、各教材、Untrusted PR boundaryのGitHub例。
- 採用: writerとconsumerの信頼、cache scope、内容の制限、復元後の照合を分ける。現在の`cache-mode`によるread/write制限と再利用workflowの実効設定も確認する。
- 変更して採用: 共通controlは取得ファイルのcacheへ絞り、展開済み環境・toolの再利用と区別する。Protected mainへのpush保存、SHA-256を含むkeyの具体構成、pipのwheel-only installは製品profileへ分け、全採用先の唯一の要件にしない。
- 不採用: Keyの一致を内容の認証と扱うこと、PRのmerge-ref cacheが作られただけでdefault branchを汚染できたと断定すること、jobの成功表示だけで保存・復元・拒否を確認済みとすること。
- 限界: key一致、hit、署名のないarchiveの展開を真正性の証拠にしない。公式仕様の確認は組織の設定・実行結果の確認ではない。

保持した参照仕様・ガイダンス:

- [GitHub cache concepts](https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching)、[cache reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)、[REST cache API](https://docs.github.com/en/rest/actions/cache)、[actions/cache](https://github.com/actions/cache)。
- [Workflow syntax / cache-mode](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#cache-mode)。2026-09-27確認。`read`は復元だけ、`none`は読書きとも拒否。Job値はworkflow値を上書きし、再利用workflowには呼出元の明示的な上限が必要。操作の拒否・省略を必ずjob失敗にする仕様ではない。GitHub.comの仕様確認であり、旧Action固定版・GHES・独自clientの動作確認ではない。
- 2026-10-04の追加照合: [GitHub dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)は、cacheのbranch・merge refの取得範囲、default branchの低信頼triggerの既定読取り、明示的な書込みmodeによる迂回、prefix復元、秘密情報の保存禁止を説明する。これを保存者・利用者・exact復元の確認へ採用する。`cache-mode`の実効権限、setup Actionや呼出先workflowの全経路、復元bytesの検証を実組織で確認した証拠ではない。旧Secure useの高confidenceなframework関係は非継承とし、理由を[移行台帳](../docs/MIGRATION.md)へ記録。
- [zizmor cache-poisoning audit](https://docs.zizmor.sh/audits/#cache-poisoning): 静的な候補検出。実効scopeや内容の安全性を証明しない。
- [pip secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/): download cacheを復元した後も、承認済みhashと通常installの照合を行うための仕様。
- [OWASP CI/CD-SEC-9](https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-09-Improper-Artifact-Integrity-Validation)、[SLSA v1.2 Build track basics](https://slsa.dev/spec/v1.2/build-track-basics)、`SPEC-NIST-SSDF-1.1`: 隣接する設計入力。cache制限だけでartifact integrityやbuild levelを満たすとは扱わない。
- 旧実装のPython [3.13.15](https://www.python.org/downloads/release/python-31315/)、actions/cache `27d5ce7f107fe9357f9df03efb73ab90386fccae`、checkout `de0fac2e4500dabe0009e67214ff5f5447ce83dd`、setup-python `a309ff8b426b58ec0e2a45f0f869d46889d02405`を保持。今回はworkflowを移植せず、runtimeと実効挙動を再レビューする。
- 旧frameworkレビュー: product-security、2026-09-07。2026-10-04に旧三関係を照合し、SITF T-C007とOSPS BR-01.03の部分関係を保持。GitHub Secure use関係は非継承。採否は[移行台帳](../docs/MIGRATION.md)を参照。実cacheの保存・復元・拒否は未確認。

<a id="ref-cicd-014"></a>

## REF-CICD-014 — Runner lifecycleの製品ガイダンス

- 発行者・役割: GitHubのrunner運用仕様を直接の根拠とし、Takumi RunnerとStepSecurityは実装・検知の候補として扱う。
- 版: 旧資料レビュー2026-08-11。GitHub self-hosted referenceは2026-09-16、2026-09-27に確認。固定文書改訂・digestは未特定で`re-review-required`。他リンクの現在の挙動は再レビューが必要。
- 利用先: `PSB-CICD-007 / RUNNER-1..9`、`ENG-CICD-003`、PSB-CICD-007の教材。
- 採用: job単位の割当、compute・storage破棄、外部ログ保存を別の条件として扱う。
- 変更して採用: JIT登録や特定のproviderイベントを共通controlの唯一の方式にせず、job・実行環境の世代・破棄結果の対応を要件にする。登録権限の限定とjobからの分離、取消・破棄失敗時の再利用停止を設計判断へ戻す。
- 不採用・限界: ephemeral登録やjob終了だけをhost破棄の証拠にしない。製品候補は導入済みでも必須でもない。旧資料のE3 syntheticと旧controlのE1 external-referenceは実環境の採用証拠へ昇格させない。

保持した仕様・候補:

- [GitHub-hosted runners](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners)、[self-hosted runner reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)、[secure use](https://docs.github.com/en/actions/reference/security/secure-use)。
- 2026-09-27にself-hosted referenceの一job後のephemeral登録解除、利用者側のwipe処理、外部ログ保存を再確認。取消・破棄の失敗・ログ不足を別に追う構成は、本PJの[設計判断](../engineering/cicd-security/ci-state-and-runner-lifecycle/README.md#取消破棄失敗とログ不足を扱う)。実runner・provider・世代別の破棄や配送は未観測。
- [Runner group access](https://docs.github.com/en/enterprise-cloud@latest/actions/how-tos/manage-runners/self-hosted-runners/manage-access)、[旧一覧のaccess URL](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access)、[monitor and troubleshoot](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/monitor-and-troubleshoot)、[self-hosted REST / JIT registration](https://docs.github.com/en/rest/actions/self-hosted-runners)。
- Takumi Runnerの[quickstart](https://shisho.dev/docs/t/runner/quickstart/)、[ephemeral architecture](https://shisho.dev/docs/t/runner/architecture/ephemeral/)、[limitations](https://shisho.dev/docs/t/runner/limitation/)。
- [StepSecurity detections](https://docs.stepsecurity.io/harden-runner/detections): 実行中の検知候補。host破棄・隔離の代替ではない。
- 旧frameworkレビュー: product-security、2026-09-02。2026-10-04にGitHub、SSDF、OSPS、ATT&CKの旧六関係を再照合し、三関係だけを範囲を絞って保持。採否は[移行台帳](../docs/MIGRATION.md)へ記録。実runnerの隔離、破棄、ログ配送は未確認。

<a id="ref-build-001"></a>

## REF-BUILD-001 — CI/CD runtime sensorの調査候補

- 発行者: cicd-sensor project。役割は製品候補の発見であり、直接の導入要件ではない。
- 参照版: [commit `6e08deb2221c19a854d8d3be7ce37c659c15bce9`](https://github.com/cicd-sensor/cicd-sensor/tree/6e08deb2221c19a854d8d3be7ce37c659c15bce9)、旧レビュー2026-07-30。
- 利用先: `ENG-CICD-003`のruntime detectionとの境界、次のBuild Security移行の評価入力。
- 採用: process・file・networkの観測、sensor health、検知後の対応を独立して評価する。
- 保留: 未導入。旧時点ではinterfaceはpre-releaseとして扱っていた。採用前に版・integrity、kernelと実行権限、秘密情報の除去、収集失敗を再確認する。
- ライセンス: 同commitの[Apache-2.0 LICENSE](https://github.com/cicd-sensor/cicd-sensor/blob/6e08deb2221c19a854d8d3be7ce37c659c15bce9/LICENSE)とeBPF等の構成要素のライセンスを個別に確認する。
- 限界: telemetryの取得はsandbox、通信制限、runner破棄の代替ではない。sensor停止をclean判定へ変換しない。

## SPEC-SITF-1.0.0 — Supply-chain Infrastructure Threat Framework

- 発行者・役割: Wizの脅威分類。準拠要件ではない。
- 参照版: `1.0.0@d1d1536`、[commit `d1d1536da5cbc7107fb90ab3f5a4b1f62b21ea59`](https://github.com/wiz-sec-public/SITF/tree/d1d1536da5cbc7107fb90ab3f5a4b1f62b21ea59)。
- 利用先: `PSB-CICD-009 / CACHE-1・3・5・6`との部分的な設計関係。
- 2026-10-04の照合: 固定commitの[Technique Library / T-C007](https://github.com/wiz-sec-public/SITF/blob/d1d1536da5cbc7107fb90ab3f5a4b1f62b21ea59/TECHNIQUE_LIBRARY.md)を確認。共有Action cacheの汚染、隔離と検証の欠如に対し、保存者・保存先の限定、復元後の照合、特権jobによる不使用へ範囲を絞る。正確なkey構成、download cacheのpath、hash方式はこの分類の規定ではない。旧`mitigates/high`は`mitigates/medium`へ変更した。
- 限界: 攻撃行動との関係であり、cacheの安全性、導入済み状態、分類体系の完全な網羅を証明しない。

## パイロット対象外の移行状態

<a id="ref-container-003"></a>

## REF-CONTAINER-003 — Falco runtime event / health guidance

- 発行者・役割: Falco Projectの製品ガイダンス。利用先はPSB-CONTAINER-004、ENG-RUNTIME-001と教材。
- 旧参照版: [Falco 0.44.0](https://github.com/falcosecurity/falco/releases/tag/0.44.0)、レビュー2026-07-31。今回binaryを取得・導入していない。
- 保持する仕様: [JSON output](https://falco.org/docs/outputs/formatting/#json-output)、[supported fields](https://falco.org/docs/reference/rules/supported-fields/)、[metrics](https://falco.org/docs/metrics/)。
- 追加確認日: 2026-09-28。[Output Channels](https://falco.org/docs/concepts/outputs/channels/)、[Supported Fields](https://falco.org/docs/reference/rules/supported-fields/)、[Dropping Events](https://falco.org/docs/troubleshooting/dropping/)、[Missing Fields](https://falco.org/docs/troubleshooting/missing-fields/)の現行公式ページを確認。JSONの`output_fields`はruleの出力指定に依存し、container情報が欠ける場合もある。Dropの計測は観測不完全を示すが、dropゼロだけでは全行動の検知を保証しない。現行ページは可変で、採用版では再確認が必要。
- 採用: Structured event、対象identity、rule/configの版、kernel・store・output dropをイベント件数と別に評価する。
- 変更して採用: 旧fixtureのsequence・完全性は収集契約として扱い、全kernel挙動の観測を証明するとは解釈しない。
- リポジトリでの解釈: 欠けたcontainer・image情報を稼働inventoryへ照合し、未確定のまま残す。安全な試験eventがreceiverへ届いたことと担当者の受領は別に確認する。Falcoの全版がこれらの業務判断を提供するという意味ではない。
- 保留・限界: 旧metrics URLは移転したため、2026-09-17時点の本文未取得は履歴として保持する。現行資料の確認はlive sensor・driver・kernel・権限・性能・更新integrity・retentionの検証ではない。製品必須要件ではない。

<a id="ref-container-004"></a>

## REF-CONTAINER-004 — Sysdig runtime forwarding / health guidance

- 発行者・役割: Sysdigの製品ガイダンス。利用先はPSB-CONTAINER-004、ENG-RUNTIME-001と教材。
- 旧contractレビュー: 2026-07-31。Immutable文書commitは未確定。`13.0.0-fixture`は合成schema値で推奨versionではない。
- 保持する仕様: [Event forwarding](https://docs.sysdig.com/en/sysdig-secure/event-forwarding/)、[runtime policy events](https://docs.sysdig.com/en/sysdig-secure/runtime-policy-events/)、[agent health](https://docs.sysdig.com/en/sysdig-monitor/integrations/integration-library/sysdig-agent-health/)。
- 追加確認日: 2026-09-28。[SIEM and Data Platforms](https://docs.sysdig.com/en/sysdig-secure/siem-data-platforms/)、[View Agent Health](https://docs.sysdig.com/en/sysdig-secure/classic-agent-health/)、[Events Feed](https://docs.sysdig.com/en/sysdig-secure/threats-event-feed/)の現行公式ページを確認。標準転送とagent local forwardingでは対象event・認証方式・metadataが異なるため、通知の完全性やimage digestの有無を共通fixtureから推定しない。現行ページは可変で、採用版では再確認が必要。
- 採用: Event配列の正規化、workload/imageとの結合、agent・connection・license・drop・forwarding・配送の独立確認。
- リポジトリでの解釈: 転送方式ごとの利用可能なeventとmetadataを確認し、image digest欠落時の稼働inventory照合、担当者の受領、破壊的対応の独立承認を別の設計にする。Sysdigの全構成がこれらを自動で保証するという意味ではない。
- 保留・限界: 旧forwardingページは2026-09-17に取得失敗し、今回も本文を確認できなかった。確認できた現行ページは転送方式とhealthの設計入力であり、API、subscription、導入、通知先、retention、対応の証拠ではない。購入推薦・製品必須要件ではない。

<a id="ref-runtime-response-handoff-001"></a>

## REF-RUNTIME-RESPONSE-HANDOFF-001 — 初動と製品適用の入力

- 役割: 旧資料記録を用いた横断設計入力。利用先はENG-RUNTIME-001のtriage→製品適用→対応境界。
- 保持する正本: [NIST SP 800-61 Rev.3記録](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-006)、[FIRST maturity](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-003)、[FIRST Services Framework 1.1](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-gov-004)、[Dependency-Track](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-rel-001)、[SBOM lifecycle](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-rel-002)。版・snapshot・integrity・採否・除外理由の詳細は旧記録を保持し、移植は各主題で再レビューする。
- 採用: Evidence保全、担当者、独立承認、正確なartifact/deployment同一性と完全性の区別。
- 不採用・限界: Eventだけで全製品の影響を確定しない。PSIRT成熟度をこのpilotの存在から推定しない。GOV-001はガイダンス移行済みだが、組織能力評価は未実施。

<a id="ref-release-sbom-lifecycle-001"></a>

## REF-RELEASE-SBOM-LIFECYCLE-001 — Release SBOMの観測・同一性・analysis境界

### 役割・利用先・参照版

[PSB-REL-003](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)、
[ENG-REL-003](../engineering/release-integrity/release-sbom-identity-and-analysis/README.md)、教材、
[CycloneDX限定実装](../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)の直接の設計入力です。

- CycloneDX `1.7`: [JSON reference](https://cyclonedx.org/docs/1.7/json/)、[公式JSON Schema](https://github.com/CycloneDX/specification/blob/4b3f59453366e27c8073fd24e98bf21ef8892c8e/schema/bom-1.7.schema.json)、[lifecycle phases](https://cyclonedx.org/guides/sbom/lifecycle_phases/)、[component compositions](https://cyclonedx.org/use-cases/compositions-components/)を2026-09-25に確認。固定commit `CycloneDX/specification@4b3f59453366e27c8073fd24e98bf21ef8892c8e`は旧source記録から継承。Schema SHA-256は`df472ef4aaf593904c479293723a1a5c191d6672715c93b3c0b5c318f3914221`。同梱する正常例をこのschemaで検証済み。SpecificationとschemaはApache License 2.0。
- OWASP Dependency-Track: [CI/CD](https://docs.dependencytrack.org/usage/cicd/)、[notifications](https://docs.dependencytrack.org/integrations/notifications/)、[users and permissions](https://docs.dependencytrack.org/administration/users-and-permissions/)、[REST API](https://docs.dependencytrack.org/integrations/rest-api/)を2026-09-25に確認。旧adapter対象の[4.14.3 release](https://github.com/DependencyTrack/dependency-track/releases/tag/4.14.3)と旧JAR SHA-256 `11a5c85616b745803b5653016d9da2195f2e23ac66fe6a85d2ae2b4661d393a9`は履歴として保持するが、現在推奨する実行版やlive adapterを意味しない。
- CISA、August 2024: [Recommended Practices for SBOM Consumption](https://www.cisa.gov/sites/default/files/2024-08/SECURING_THE_SOFTWARE_SUPPLY_CHAIN_RECOMMENDED_PRACTICES_FOR_SOFTWARE_BILL_OF_MATERIALS_CONSUMPTION-508.pdf)と[SBOM Resources Library](https://www.cisa.gov/topics/cyber-threats-and-advisories/sbom/sbomresourceslibrary)。ConsumerがSBOMを継続利用し、製品・componentの影響調査へ結ぶ設計入力。
- SPDX: [Specifications](https://spdx.dev/use/specifications/)と[SPDX 3.0.1](https://spdx.dev/wp-content/uploads/sites/31/2024/12/SPDX-3.0.1-1.pdf)。Interchange候補として保持するが、本移行のparser／implementation対応は主張しない。
- 利用者提供資料、受領日`2026-07-31`: [固定した旧正本](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/docs/user-supplied-sbom-lifecycle-guidance-ja.md)。PR・push時のsource、image build直後の完成物、deployment・稼働中という三つの取得地点と、commit・artifact・deploymentをつなぐ考えを設計入力にした。外部書誌と再配布条件は別途提供されておらず、一次仕様やframework mappingの根拠にしない。
- NIST SP 800-218、SSDF `1.1`: [SPEC-NIST-SSDF-1.1](#spec-nist-ssdf-11--nist-sp-800-218)の`PS.3.2`と`RV.1.1`を2026-09-25に再評価。Version 1.2はInitial Public Draftであり、現行mappingはfinalの1.1を使用する。
- 移行元: 旧[PSB-REL-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/README.md)。旧check、実装、mappingの採否は[移行記録](../docs/MIGRATION_RELEASE.md#release-sbom-migration)に保持。

### 採用・変更・不採用

- 採用: 利用者提供資料のsource・build・deployment／operationsという取得地点、各地点で観測できる対象と異なる用途、commitからartifact・deploymentへたどる関係。加えて一次仕様からcomponentとrelationshipの機械可読なidentity、明示されたcomposition state、exact artifactへのdigest binding、consumerが取得できる公開、least-privilege analysis intake、非同期処理の完了・失敗状態を採用。
- 変更して採用: 提供資料のPR・push、image build直後、deployment・稼働中は代表例として扱い、全製品への固定triggerにしない。Build／post-build SBOMをrelease authorityにするが、final artifactを実際に観測した場合に限り、`complete`を自動的な事実にしない。Source、build、operationsを一つのserialへ上書きせず関係でつなぎ、稼働中memoryの完全観測を仮定しない。共通base imageや供給者のSBOMも、その後の追加・削除・更新を含む最終製品の一覧とは分ける。Dependency-Track固有eventは本PJの`ACCEPTED`、`VALIDATED`、`INGESTED`、`ANALYZED`、`REJECTED`、`ERROR`という状態の意味へ照合する。これらは製品APIの状態名ではない。
- 不採用: 固定5分、365日、24時間、public HTTPSを全productの要件にすること。`immutable: true`、permission配列、手書きprocessing receipt、analyzer health等の自己申告だけでlive stateを証明すること。Format validityやcomponent countからcomplete coverageを推論すること。
- 今回の対象外: SPDX parser、supplier signature、live release storage、Dependency-Track adapter、deployment collector。追加実装は既定にせず、採用先で導入・確認に役立つ場合だけ選ぶ。選んだ場合は対象製品・版・接続先・権限を明らかにし、正常系と拒否・失敗を実際に観測する。

2026-09-28の再確認：利用者提供資料はローカルの旧repositoryにある上記固定commitから原文を確認しました。三地点と供給者・共通base imageの区別を教材と設計へ反映しています。CycloneDXのlifecycle URLは『Authoritative Guide to SBOM』第三版（2025-10-21、v1.7、CC BY 4.0）へ遷移し、生成段階と収集方法の説明を確認しました。生成段階のfieldを追記するだけでは、実際に観測した対象は変わらないという点は本PJの解釈です。

同日、Dependency-Trackの通知文書と[4.14.3のBomUploadProcessingTask](https://github.com/DependencyTrack/dependency-track/blob/4.14.3/src/main/java/org/dependencytrack/tasks/BomUploadProcessingTask.java)を確認しました。`processBom`で後続の脆弱性分析イベントを登録して`BOM_PROCESSED`を通知し、`processEvent`へ戻ってイベントを配送します。このため従来の`PROCESSED`を取込と分析へ分け、この通知だけでは分析完了と扱わない判断を採用しました。確認は版指定のソースであり、live処理の観測ではありません。

### Mappingと限界

SSDF `PS.3.2`を`SBOM-REL-1〜5・8`、`RV.1.1`を`SBOM-REL-6〜8`へ`supports / medium / design-reviewed`で部分割当します。SBOMはcomponent・dependency provenance dataと継続的なvulnerability調査を支える一つの仕組みであり、これだけでtask全体やSSDF準拠を満たしません。旧`PS.3.1 / supports / high`はrelease archive全体との範囲差があるため非継承です。

CycloneDX schema validityはgenerator coverage、SBOM authenticity、componentの無害性を証明しません。Dependency-Trackの処理完了もadvisory dataやidentifier matchingの完全性を証明しません。限定実装はartifact bindingと文書内の一部contractだけを確認し、live publication・analysis・deploymentは未検証です。

<a id="ref-supplier-sbom-intake-001"></a>

## REF-SUPPLIER-SBOM-INTAKE-001 — 供給者SBOMの受領と信頼境界

### 役割・利用先・参照版

[PSB-REL-004](../controls/records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md)、
[ENG-REL-004](../engineering/release-integrity/supplier-sbom-intake-boundary/README.md)、教材の直接の設計入力です。

- CISAほか、2024-08、[Recommended Practices for SBOM Consumption](https://www.cisa.gov/sites/default/files/2024-08/SECURING_THE_SOFTWARE_SUPPLY_CHAIN_RECOMMENDED_PRACTICES_FOR_SOFTWARE_BILL_OF_MATERIALS_CONSUMPTION-508.pdf)を2026-09-25に再確認。受領したSBOMの出所・完全性、取込前の不一致解消、既知の欠落の確認を設計入力にした。署名または事前合意した配送方法を一律の唯一方式にしない。
- CycloneDX `1.7`の[JSON reference](https://cyclonedx.org/docs/1.7/json/)と[固定schema](https://github.com/CycloneDX/specification/blob/4b3f59453366e27c8073fd24e98bf21ef8892c8e/schema/bom-1.7.schema.json)を2026-09-25に再確認。形式・参照・署名情報を記述できるが、文書内の鍵や`complete`表明を利用者の信頼根拠・網羅性の証明へ昇格させない。版とhashは[Release SBOM資料](#ref-release-sbom-lifecycle-001)に保持。
- Sigstoreの[Bundle format](https://docs.sigstore.dev/about/bundle/)と[検証手順](https://docs.sigstore.dev/cosign/verifying/verify/)を2026-09-25に確認。採用する署名方式の候補であり、bundle内の署名、署名者identity、信頼根拠、時刻・透明性証拠を検証する設計に使う。特定の供給者やbundleへの対応済み状態は主張しない。随時更新される製品文書のため`re-review-required`。
- 利用者提供の[SBOM lifecycle資料](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/sbom-binding-publication/docs/user-supplied-sbom-lifecycle-guidance-ja.md)、受領日`2026-07-31`。調達時の署名付きsupplier SBOMを別の受入境界にする着想を採用。書誌と再配布条件は別途提供されておらず、規範やframework mappingの直接根拠にしない。取得地点全体の採否は[Release SBOM資料](#ref-release-sbom-lifecycle-001)が正本。
- NIST SP 800-218、SSDF `1.1`の[PW.4.1](#spec-nist-ssdf-11--nist-sp-800-218)を2026-09-25に確認。第三者componentの出所情報を得てリスクを評価するtaskの一部を支援する関係として別途mappingする。
- 移行元: [旧PSB-REL-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/supplier-sbom-trust/README.md)。旧checkと合成実装の採否は[移行記録](../docs/MIGRATION_RELEASE.md#supplier-sbom-migration)に保持。

### 採用・変更・不採用

- 採用: 供給者からの受領を隔離し、利用者側の期待値で出所・対象製品・成果物を照合してから通常台帳へ渡すこと。不一致、検証障害、既知の欠落を区別し、訂正・撤回に追従すること。
- 変更して採用: 署名を唯一の受渡し方法に固定せず、合意した方式ごとに必要な出所・完全性の証拠を選ぶ。署名者の期限だけで過去の署名を決めず、採用方式の時刻・失効・侵害方針を確認する。`ACCEPTED_FOR_PORTFOLIO_IMPORT`という旧表現は取込や処理の完了を連想させるため、取込前の`INTAKE_CANDIDATE`へ狭める。
- 不採用: 合成Ed25519 envelopeと手書きstatus snapshotを、全供給者向けの実装にすること。JSON内の権限配列で実際の台帳権限を証明すること。署名・schema適合をSBOMの完全性や供給者製品の安全性に変換すること。
- 今回の対象外: 署名または配送方式を選んだ製品固有の検証器、信頼根拠・失効source、台帳のlive隔離・権限検証。文書と診断項目で今回の範囲は完了とし、供給者、対象成果物、方式、状態source、使い捨て取込先が決まり、導入・確認に役立つ場合だけ実装例を検討する。利用者提供資料の2026-09-28再確認は[Release SBOM資料](#ref-release-sbom-lifecycle-001)に記録した。

### Mappingと限界

SSDF `PW.4.1`へ`supports / medium / design-reviewed`で部分割当します。SBOMの出所と対象を確認することは第三者componentの情報を得て評価するための入力ですが、component自体の採用審査、更新、脆弱性調査、SSDF準拠は示しません。旧`RV.1.1`は脆弱性情報の継続収集・調査というtaskへこの受入境界だけでは十分に直接つながらないため継承しません。

## REF-SUPPLY-CHAIN-IMPACT-001

### 役割・利用先・参照時点

[PSB-GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)、[ENG-GOV-001](../engineering/governance-operations/incident-impact-and-response-planning/README.md)、その教材の設計入力。2026-09-17に旧参照記録を移行したもので、外部仕様を現行版へ一括再確認した記録ではありません。
旧REF-REL-001・REF-REL-002の確認日2026-07-31と、旧GOV-001のfixture契約を保持します。

### 保持する参照仕様

- Dependency-Track、CISA SBOM consumption、CycloneDX 1.7、SPDX 3.0.1、利用者提供SBOM lifecycle資料の版・採否・実装境界は[REF-RELEASE-SBOM-LIFECYCLE-001](#ref-release-sbom-lifecycle-001--release-sbomの観測同一性analysis境界)を正本とする。GOV-001はそのinventoryを影響検索の入力として使い、release SBOMの生成・公開・analysis処理を重複して定義しない。
- Incident対応のNIST・FIRST資料は[REF-RUNTIME-RESPONSE-HANDOFF-001](#ref-runtime-response-handoff-001--初動と製品適用の入力)を正本とする。Frameworkのexact版は[SSDF](#spec-nist-ssdf-11--nist-sp-800-218)、[ATT&CK](#spec-mitre-attack-v19-1)に保持し、現行関係は[mapping](../mappings/frameworks.yaml)で示す。

2026-10-03にNIST SSDF 1.1の`RV.1.1`・`RV.2.1`とATT&CK v19.1の`T1195.001`をGOV-001の特性へ再照合しました。SSDF `RV.1.1`はcredible reportを受けた後の製品影響調査（`IMPACT-1・4・6・7`）、`RV.2.1`はリスク対応を計画するための適用性・未確認範囲の入力（`IMPACT-1・4・5・7`）だけを`supports / medium / design-reviewed`とします。脆弱性情報の継続収集、悪用可能性・被害規模の評価、優先度と対応の決定・実行はこの関係から導きません。旧`T1195.001 / detects`は、既知の汚染版の利用先調査が攻撃者による依存・開発ツール改変の検知を示さないため非継承です。旧関係の版・confidenceと理由は[移行台帳](../docs/MIGRATION.md)に残します。

### 採用・変更・不採用・限界

採用: exact componentからSBOM、build、artifact、deploymentへの照合、検索の全page・ACL・鮮度・処理health、owner承認付きdry-run。
変更: 旧保全先頭の固定runbookを、緊急封じ込めとの並行条件も決める設計判断として説明する。検索一致を侵害確定へ昇格させない。
不採用: 分析基盤だけを真実の正本にすること、検索結果からの破壊的自動対応、fixtureの成功による導入済み判定。
2026-09-28の読み合わせでは、[REL-003資料で再確認した取得地点と分析状態](#ref-release-sbom-lifecycle-001)を影響調査の入力へ戻しました。検索0件は、対象製品・時点・収集範囲・検索の完了範囲を示せる部分にだけ非該当とし、残りは調査不能としてGOV-003へ渡します。この三状態と受け渡し方法は本PJの設計判断であり、参照資料が全製品へ要求する固定手順とは主張しません。
Uploadは事前作成project UUIDとBOM_UPLOADを基本とし、検索用VIEW_PORTFOLIO・VIEW_VULNERABILITYから分離する。受付と取込を分け、待機に上限を置くという旧判断を保持する。2026-09-28の[Release SBOM資料の再確認](#ref-release-sbom-lifecycle-001)に従い、BOM_PROCESSEDだけで脆弱性分析完了とは判断しない。採用版の権限・event契約と分析完了の確認方法はadapter実装前に再確認する。
AutoCreateのためのPROJECT_CREATION_UPLOADや広い管理権限は既定にしない。Validation失敗、timeout、pagination不足をcleanへ変換しない。
5系のAPI・配布・notification変更は再レビューしてから対応する。旧記録にある5.0.3観測やSPDX 3.1 RC情報を現在の最新情報として引き継がない。
Supplier signatureの旧REL-004 fixtureは別の保証対象であり、このcontrolへ統合しない。
Live API・collectorの完全性、process-loaded component、実対応・復旧は資料だけでは証明できない。

## REF-SECURITY-EXCEPTION-LIFECYCLE-001

### 役割と参照資料

[PSB-GOV-002](../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md)と[ENG-GOV-002](../engineering/governance-operations/security-exception-decision-boundary/README.md)における例外lifecycleの設計入力。旧controlで2026-08-05にレビューした
[NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)と
[OpenSSF Security Baseline 2026-02-19](https://baseline.openssf.org/versions/2026-02-19)を保持します。
Exact framework関係はmappingへ分離し、この資料記録だけから準拠を主張しません。

### 採用・変更・不採用・限界

採用: exact control/check/target、独立したowner・reviewer・approver、理由・risk・代替策・是正先、上限付き期限、使用時の状態評価、取得・解析障害のfail-closed処理。
変更: 旧`psb-security-exception/v1`の具体schemaと30日上限は唯一の標準ではなく、設計patternの一候補として保留する。新構造ではproperty identityと組織policyに合わせる。
不採用: 例外による元checkの`PASS`化、全controlのrisk判断を共通serviceへ移すこと、SHA-256だけによる承認真正性の主張、fixture成功による組織導入判定。
限界: NIST SSDFとOpenSSF Baselineは、repository固有のrole数、state名、schema、期間を直接規定する資料として扱わない。Ticket system、信頼時刻、取消、通知、policy engine、実gateの証拠は別途必要。

2026-09-28に上記[NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)の公開ページと[OpenSSF Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19)を再確認しました。旧YAML全件・固定SHA-256・`psb-security-exception/v1`を全利用者へ要求する記述は機械可読記録から外しました。どの記録形式でも、評価対象の台帳の欠落・改変、承認の独立性、期限、使用時の失効・取得障害を見分けることは本PJの設計判断です。GOV-003の脆弱性risk受入とGOV-005の旧digest一時使用を[consumer mapping](../mappings/exception-consumers.yaml)へ設計上の関係として追加し、元のfinding・対応期限・復旧未完了を残します。Live gateでの利用は未確認です。

2026-10-03に[SSDF 1.1の公式本文](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)を再照合しました。旧`RV.2.1`は脆弱性ごとのリスク分析を求めますが、GOV-002はcontrol固有の分析結果を受けて例外decisionを記録・再評価する共通lifecycleです。旧関係は非継承とし、承認済み例外の理由・リスク対応の記録と見直しを例示する`PW.1.2`へ新しく`supports / medium / design-reviewed`の部分関係を作りました（`EXCEPTION-3・4`）。SSDFはGOV-002の固定期限・役割分離を指定せず、GOV-002は全security requirements・設計判断の追跡や未使用例外の定期レビューを要求しません。

[OSPS Baseline 2026.02.19のQA-03.01](https://baseline.openssf.org/versions/2026-02-19#osps-qa-0301)は、主ブランチへのcommit時に自動status checkが通るか手動でbypassされることを要求します。GOV-002の例外decisionが、そのGit上のstatus checkとmanual bypassを実際に制御するとは言えません。旧関係は非継承とし、旧版・confidenceを[移行台帳](../docs/MIGRATION.md)に残します。実際の承認、失効、主ブランチの受入やSSDF・OSPSの適合は未確認です。

<a id="spec-nist-sp-800-190"></a>

## SPEC-NIST-SP-800-190 — Container security guidance

- 発行者・版: NIST、SP 800-190、September 2017。[公式publication](https://csrc.nist.gov/pubs/sp/800/190/final)。
- 固定PDF SHA-256: `0ebad52c4a3aba971b3a707b056e57238d1c4ad8f212dffd461ff9f5fed1bdb6`。旧registry review `2026-07-30`から保持し、2026-09-24に`4.1.5`と`4.4.5`、2026-09-25に`2.3`、`3.4.3`、`4.3.1`、`4.3.3`、`4.3.5`、`4.4.2`、`4.4.3`、`4.5.1`〜`4.5.5`、`4.6`を公式PDFで再照合。2026-09-28に`4.4.4`のprocess・保護file・network異常の記述を再照合。
- 利用先: `PSB-CONTAINER-001`の`4.1.5`・`4.4.5`関係、`PSB-CONTAINER-003`の`4.3.1`・`4.3.5`・`4.5.1`〜`4.5.5`・`4.6`関係、`PSB-CONTAINER-005`と`PSB-CONTAINER-007`の`4.4.3`関係、`PSB-CONTAINER-006`の`4.3.3`・`4.4.2`関係、`PSB-CONTAINER-004`の`RUNTIME-2,3,4,7`と`4.4.4`の部分関係、`PSB-DETECT-001`の`SCAN-2..4`と`4.1.1`の部分関係。
- 限界: 2017年のcontainer guidanceであり、現在のKubernetes APIや製品設定を規定しない。Exact部分関係を、実導入・完全coverage・準拠の証拠へ昇格させない。

<a id="ref-container-host-daemon-001"></a>

## REF-CONTAINER-HOST-DAEMON-001 — Container nodeのruntime・管理・identity境界

### 役割・利用先・参照版

[PSB-CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)と
[ENG-CONTAINER-006](../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)の設計入力です。

- NIST SP 800-190、September 2017: [固定記録](#spec-nist-sp-800-190--container-security-guidance)の`4.3.1`、`4.3.5`、`4.5.1`〜`4.5.5`、`4.6`を2026-09-25に公式PDFで再照合。Orchestrator admin、node identity・isolation、minimal host、shared kernel、component update、host access・audit、filesystem、hardware trustの上位成果に使用。
- Kubernetes `1.37`: [Kubelet authentication／authorization](https://kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/)、[API server bypass risks](https://kubernetes.io/docs/concepts/security/api-server-bypass-risks/)、[Node authorization](https://kubernetes.io/docs/reference/access-authn-authz/node/)、[Security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)を2026-09-25に確認。Kubelet endpoint、`nodes/proxy`、static Pod、runtime socket、Node authorizer、NodeRestrictionの設計入力に使用。現行URLは可変で`re-review-required`。
- Containerd: [Operator Security Guidelines](https://github.com/containerd/containerd/blob/82f33ce76db81e47393be1cbdb6eba3343687fc5/docs/security/OPERATOR_GUIDELINES.md)、`containerd/containerd@82f33ce76db81e47393be1cbdb6eba3343687fc5`を2026-09-25に確認。Kernel・containerd・runc／shimのpatch、runtime／NRI socket、directory・binary・service・config、trusted plugin、debug／metrics endpointの実装候補に使用。
- Docker公式: [Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/)と[Rootless mode](https://docs.docker.com/engine/security/rootless/)を2026-09-25に確認。Local socket、SSH／mutual TLS、credential authority、daemonとcontainerのuser namespace化を方式比較へ使用。可変資料であり、導入時に対象Docker Engine版で再確認する。
- 移行元: 旧[PSB-CONTAINER-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-host-daemon-hardening/README.md)。旧check、fixture、mappingの採否は[移行記録](../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#container-host-daemon-migration)に保持。

### 採否と限界

- 採用: Purposeとsensitivityを持つnode pool、complete component inventory、bounded update／replacement、runtime・kubelet・補助endpoint、protected state、unique node identity、least node authority、host-side isolation、管理操作、live evidence health、侵害nodeの隔離・失効・再登録。
- 変更して採用: 旧rootless／user namespace／kernel lockdownとSecure Boot／TPMを全platform共通の合格条件にせず、threat、runtime、provider capabilityに応じて選び、unsupportedやfallbackを通常状態へ変換しない。固定path・modeはcontainerd等の対象実装へ限定する。
- 分離: Workloadのnon-root、capability、hostPath、seccomp profile指定等はCONTAINER-005、runtime eventとdeliveryはCONTAINER-004、resource pressureはCONTAINER-007が扱う。Cluster control plane全体、cloud account、developer endpoint、CI runnerはこの資料から自動的に対応済みとしない。
- 不採用: Provider-neutralな`policy.json`とsynthetic host evidenceによる実装済み判定、`Ready`状態によるnode trust、rootless名称だけによる隔離証明、CIS Docker Benchmarkの未確認版へのmapping、hardware attestationを提供しないplatformの無条件合格。
- 限界: Kubernetes、containerd、Docker資料は各製品の一部の仕様・guidanceであり、他runtime・OS・managed providerの挙動を規定しない。Live node、socket、listener、process、credential、patch service、audit delivery、attestationは未確認。具体実装は対象platformと使い捨てnode poolを選んでから追加する。

<a id="ref-deployment-artifact-admission-001"></a>

## REF-DEPLOYMENT-ARTIFACT-ADMISSION-001 — Exact artifactを使用許可へ結ぶ資料

### 役割・利用先・参照版

[PSB-CONTAINER-001](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)と
[ENG-CONTAINER-001](../engineering/container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)の設計入力です。

- SLSA `1.2`: [Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts)と[Build provenance](https://slsa.dev/spec/v1.2/build-provenance)。固定版・限界は[SPEC-SLSA-1.2](#spec-slsa-12--slsaのversion付き仕様)。Exact subject、consumer-owned expectation、authenticityをadmission decisionへ渡す根拠として利用。
- NIST SP 800-190、September 2017: 固定版は[SPEC-NIST-SP-800-190](#spec-nist-sp-800-190--container-security-guidance)。`4.1.5`のtrusted image／registry、discrete cryptographic identity、execution前のsignature validationと、`4.4.5`のrun前baseline、user identity、auditを2026-09-24に公式PDFで確認。
- Kubernetes project: `kubernetes/website@e95679cfa58a843e90bf8575d8b0db548dae452b`の[Admission webhook good practices](https://github.com/kubernetes/website/blob/e95679cfa58a843e90bf8575d8b0db548dae452b/content/en/docs/concepts/cluster-administration/admission-webhooks-good-practices.md)を旧`REF-CONTAINER-002`から保持。2026-09-24に現行の[Policies](https://kubernetes.io/docs/concepts/policy/)、[Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/)、[webhook guidance](https://kubernetes.io/docs/concepts/cluster-administration/admission-webhooks-good-practices/)も確認。現行URLは可変で`re-review-required`。
- 追加確認日: 2026-09-28。[Kubernetes Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)でmutationとvalidationの段階を再確認し、[OCI Image Index v1.1.1](https://github.com/opencontainers/image-spec/blob/v1.1.1/image-index.md)でindexがplatform別manifestを参照する構造を確認。Indexと選択manifestの照合方法、runtimeの表示値は本PJの設計判断であり、OCI仕様だけからlive clusterの実行内容は証明できない。
- 移行元: 旧[PSB-CONTAINER-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-admission-baseline/README.md)。旧check、fixture、mappingの採否は[移行記録](../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#deployment-artifact-admission-migration)に保持。

### 採否と限界

- 採用: 全artifactのexact digest、consumer expectation、final-state validation、作成・更新経路のcoverage、評価障害の拒否、policy・decision identityとaudit。複数platform向けindexでは選択manifestとの対応を照合する。
- 変更して採用: 使用境界でREL-001を直接再実行する方式に固定せず、exact digest・target・policy・期限へ結合した認証済みdecision receiptも許す。KubernetesのCEL・webhookは選択肢でありcontrol要件にしない。
- 分離: Non-root、capability、host、filesystem、seccompは[PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)、networkは[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)、resource availabilityは[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)へ分割した。Registry access・immutability・retentionは旧CONTAINER-002の責任。
- 不採用: Tag、annotation、CIのpass表示、producerのSLSA level自己申告、署名成功だけによる無害性判断、evaluator障害時の通常allow。
- 限界: Kubernetes公式文書は製品仕様・guidanceであり、live clusterの強制証拠ではない。Current docsには将来versionを含む可変内容があるため、実装時に対象cluster versionとAPIを固定する。NIST 4.4.5全体やSLSA level、全deployment platformへの適用を主張しない。

<a id="ref-workload-confinement-001"></a>

## REF-WORKLOAD-CONFINEMENT-001 — Workload privilegeとhost境界

### 役割・利用先・参照版

[PSB-CONTAINER-005](../controls/records/container-cloud-iac-security/psb-container-005-workload-privilege-confinement/README.md)、
[ENG-CONTAINER-003](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/README.md)、
[Kubernetes代表実装](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/implementations/kubernetes-psa-cel/README.md)の設計・実装入力です。

- NIST SP 800-190、September 2017: [固定記録](#spec-nist-sp-800-190--container-security-guidance)の`3.4.3`と`4.4.3`を2026-09-25に公式PDFで再照合。Privileged mode、sensitive host mount、MAC、seccomp、read-only root filesystemを、侵害されたcontainerからhost・他containerへ進む経路とruntime configuration baselineの根拠に使用。
- Kubernetes `1.37`: [Release一覧](https://kubernetes.io/releases/)で2026-08-26 releaseとsupported minorを2026-09-25に確認。[Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)、[Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)、[Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/)、[Service Accounts](https://kubernetes.io/docs/concepts/security/service-accounts/)の現行公式文書を同日に確認。実装例の対象minor、field、mode、failure behaviorの根拠に使用。現行URLは可変で、別minorへの導入時は再確認する。
- 追加確認日: 2026-09-29。[Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)でPod作成時のenforceと一部更新の検査免除を再確認。代表実装のserver-side dry runは新規Podの受入・拒否だけを確認し、既存Podの実効状態や全更新経路を証明しない。
- 移行元: 旧[PSB-CONTAINER-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-admission-baseline/README.md)の`CNT-003..008`。項目ごとの採否は[移行記録](../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#workload-confinement-migration)に保持。

### 採否と限界

- 採用: 全container経路の列挙、non-root、privilegedと権限昇格の拒否、capabilityの既定drop、runtime既定以上のseccompと利用可能なMAC、host接続の拒否、read-only root filesystem、不要なcontrol-plane credentialの自動付与禁止、final workloadのfail-closed強制。
- 変更して採用: Kubernetesの`restricted`を製品非依存のcontrol要件にせず、代表実装でversionを`v1.37`へ固定する。Pod Security Standardsが一括して扱わないread-only root filesystemとservice account tokenはValidating Admission Policyで補う。
- 分離: `CNT-007`は[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)、`CNT-008`は[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)へ移行した。Node／daemon hardeningは[PSB-CONTAINER-003](../controls/records/container-cloud-iac-security/psb-container-003-container-host-daemon-boundary/README.md)、実行後の観測は`PSB-CONTAINER-004`へ渡す。
- 不採用: `warn`・`audit`だけによる強制済み判定、profile versionの`latest`追従、広いnamespace／user exemption、IaC検査のpassによるlive cluster強制の証明、旧synthetic verifierによる導入済み判定。
- 限界: Kubernetes資料は製品仕様・guidanceであり、live clusterの設定・拒否・runtime適用の証拠ではない。代表実装はLinux PodとKubernetes 1.37向けで、Windows、全runtime class、実際のAppArmor／SELinux状態、明示的にprojectしたtokenのRBAC・audience・期限、resource、networkを確認しない。Networkは別の実装例で扱い、この実装の検証結果へ混ぜない。NIST 4.4.3をKubernetes固有fieldや完全なhost境界の規定として扱わない。

<a id="ref-workload-network-segmentation-001"></a>

## REF-WORKLOAD-NETWORK-SEGMENTATION-001 — Workload networkのallow境界

### 役割・利用先・参照版

[PSB-CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)、
[ENG-CONTAINER-004](../engineering/container-cloud-iac-security/workload-network-allow-boundary/README.md)、
[Kubernetes代表実装](../engineering/container-cloud-iac-security/workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)の設計・実装入力です。

- NIST SP 800-190、September 2017: [固定記録](#spec-nist-sp-800-190--container-security-guidance)の`3.3.3`、`3.4.2`、`4.3.3`、`4.4.2`を2026-09-25に公式PDFで再照合。Sensitivityに応じたvirtual network、狭いinterface、network境界でのegress制御、application-aware filtering、flowと異常の観測を上位の設計根拠に使用。
- Kubernetes `1.37`: [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)、[NetworkPolicy API](https://kubernetes.io/docs/reference/kubernetes-api/networking-resources/network-policy-v1/)、[Multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)を2026-09-25に確認。既定では非分離、ingressとegressの独立性、allowの加算、通信両端の許可、default deny、DNSへの影響、CNIによる強制、反映遅延、`hostNetwork`・NAT・L4/APIの限界を採用。
- 追加確認日: 2026-09-29。[Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)でCNIによる強制、両端の独立したallow、node・hostNetwork・非TCP/UDP/SCTP経路の限界を再確認。代表実装の拒否probeでは、sourceのexecとdestinationのlocal listenerを別に確認する。
- Kubernetes `v1.37.0` source: [test image manifest](https://github.com/kubernetes/kubernetes/blob/v1.37.0/test/utils/image/manifest.go)と[agnhost VERSION](https://github.com/kubernetes/kubernetes/blob/v1.37.0/test/images/agnhost/VERSION)を2026-09-25に確認。代表実装の`registry.k8s.io/e2e-test-images/agnhost:2.66.1`、`connect`、`netexec`の版を固定する根拠に使用。
- 移行元: 旧[PSB-CONTAINER-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-admission-baseline/README.md)の`CNT-008`。採否は[移行記録](../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#network-segmentation-migration)に保持。

### 採否と限界

- 採用: Workload間の通信契約、ingress／egressの既定拒否、source egressとdestination ingressの双方での最小allow、基盤flowの明示、sensitivity zoneと外部egress、enforcement coverage、live connectivityによる許可・拒否の確認。
- 変更して採用: 旧default-deny policyの存在確認を、実際の通信が両側の許可で成立することと、一時的な片側許可の削除で再び拒否されることの確認へ広げる。Kubernetes NetworkPolicyをcontrol全体の必須技術にはせず、代表実装に限定する。
- 分離: Process・kernel・host・filesystem権限は`PSB-CONTAINER-005`、実行後の検知・triageは`PSB-CONTAINER-004`が扱う。Core NetworkPolicyで表せないFQDN、service identity、gateway強制、TLS、明示deny、全cluster共通policyは製品固有の実装判断へ渡す。
- 不採用: API objectの存在、syntheticな`enforcement_available: true`、単一のdefault-deny YAMLだけによる実効性の主張。DNSや外向き通信を全環境へ共通する固定allowとして埋め込むこと。
- 限界: Kubernetes公式文書は製品仕様・guidanceであり、対象clusterのCNI、NetworkPolicy coverage、反映完了、実通信を証明しない。代表実装はKubernetes 1.37、IPv4、TCP/8080、Pod IP間の通信だけを扱い、DNS、IPv6、SCTP、ICMP、`hostNetwork`、node traffic、NAT後のidentity、service mesh、外部egress、network telemetryを確認しない。NISTの上位成果をKubernetesのselectorや具体policyへ自動変換しない。

<a id="ref-workload-resource-bounds-001"></a>

## REF-WORKLOAD-RESOURCE-BOUNDS-001 — Workload resource budgetとpressure境界

### 役割・利用先・参照版

[PSB-CONTAINER-007](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)、
[ENG-CONTAINER-005](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/README.md)、
[Kubernetes代表実装](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)の設計・実装入力です。

- NIST SP 800-190、September 2017: [固定記録](#spec-nist-sp-800-190--container-security-guidance)の`2.3`、`3.4.3`、`4.4.3`を2026-09-25に公式PDFで再照合。Containerごとのresource allocation、runtimeがresource usageを分離する役割、runtime configuration standardの継続的な評価・強制を上位の設計根拠に使用。
- Kubernetes `1.37`: [Resource management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)、[Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)、[Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/)、[Node-pressure Eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/)、[PID limits and reservations](https://kubernetes.io/docs/concepts/policy/pid-limiting/)、[Reserve Compute Resources for System Daemons](https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/)、[Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/)、[Kubernetes CEL](https://kubernetes.io/docs/reference/using-api/cel/)を2026-09-25に確認。Request／limit、in-place resize、quota、default mutation、node allocatable、reservation、pressure／eviction、PID、local storage、CEL failure behaviorの根拠に使用。
- 追加確認日: 2026-09-29。[Resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#pod-level-resource-specification)でPod-level CPU／memory budgetが1.37で利用できることを確認。[Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)ではephemeral-storage quotaが未指定Podを必ず拒否するわけではない。代表実装は個別containerの明示request／limitを選ぶ限定profileであり、Pod-levelのみの有効な設定を拒否する。
- Kubernetes `v1.37.0` source: Network実装と同じ[test image manifest](https://github.com/kubernetes/kubernetes/blob/v1.37.0/test/utils/image/manifest.go)と[agnhost VERSION](https://github.com/kubernetes/kubernetes/blob/v1.37.0/test/images/agnhost/VERSION)を使用し、代表実装のtest imageを`2.66.1`へ固定。
- 移行元: 旧[PSB-CONTAINER-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-admission-baseline/README.md)の`CNT-007`。採否は[移行記録](../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#resource-consumption-migration)に保持。

### 採否と限界

- 採用: Workload resource budget、requestとruntime ceilingの区別、tenant aggregate quota、PID・local storage、node allocatable・reservation・pressure、create／update／resize／debugの強制、quota・runtime・event・healthの観測。
- 変更して採用: 旧CPU `1000m`、memory `512Mi`、PID `256`を普遍的な上限にせず、workload測定とcapacity reviewで決める実装profileへ移す。Admission fieldの確認をruntime enforcementの証明にせず、各強制点の証拠を分ける。
- 分離: Applicationのrate limit、autoscaling、replica冗長性、PDB、persistent storage durability／IOPS、network bandwidth、availability SLOは別の設計へ渡す。Process・host権限はCONTAINER-005、network reachabilityはCONTAINER-006、runtime異常のtriageはCONTAINER-004が扱う。
- 不採用: 固定上限を全workloadへ適用すること、`pids_limit_enforced: true`等のsynthetic Booleanを実効証拠にすること、requestだけをceiling、namespace quotaだけをcluster capacity、limitの存在だけをapplication availabilityとして扱うこと。
- 限界: Kubernetes公式文書は製品仕様・guidanceであり、対象clusterのquota admission、kubelet、runtime、cgroup、filesystem計測、node reservation、pressure、event deliveryを証明しない。代表実装はCPU／memory／ephemeral-storageのcontainer fieldとnamespace quotaをlive APIで確認する構成で、Pod-levelのみの予算、PID、node pressure、cgroup実効値、storage hard cap、capacity、全controller・providerを確認しない。NISTのresource allocationをKubernetesの具体値や完全なavailability保証へ変換しない。

<a id="ref-container-registry-publication-001"></a>

## REF-CONTAINER-REGISTRY-PUBLICATION-001 — OCI registry publicationとlifecycle

- 利用先: `PSB-CONTAINER-002 / REGISTRY-1..7`、`ENG-CONTAINER-002`、移行記録。
- NIST SP 800-190、September 2017: [固定記録](#spec-nist-sp-800-190--container-security-guidance)の`4.2.1`〜`4.2.3`を2026-09-24に公式PDFで再照合。Registry接続、stale image、authentication／authorizationの上位成果に使用。
- Open Container Initiative: [Distribution Specification v1.1.1](https://github.com/opencontainers/distribution-spec/releases/tag/v1.1.1)と[Image Specification v1.1.1のdescriptor](https://github.com/opencontainers/image-spec/blob/v1.1.1/descriptor.md)を2026-09-24に確認。どちらも当時の確認版。Descriptorの必須`mediaType`、`digest`、`size`と取得bytesの照合をartifact identityの入力に使う。
- 追加確認日: 2026-09-28。[Image Index v1.1.1](https://github.com/opencontainers/image-spec/blob/v1.1.1/image-index.md)でindexとplatform別manifestの参照関係を確認。公開したindex digestと選択されたmanifest digestを区別する。本PJが定める`active`・`deprecated`・`quarantined`等の状態と使用可否はOCI仕様の要件ではない。
- 旧実装根拠: [OWASP Docker Security Cheat Sheet固定版](https://github.com/OWASP/CheatSheetSeries/blob/cb62ae45198d07302082d4725fc3bdfe24b25dd3/cheatsheets/Docker_Security_Cheat_Sheet.md)、commit `cb62ae45198d07302082d4725fc3bdfe24b25dd3`、旧review `2026-07-30`。製品commandを普遍要件にせず、registry／supply-chain設計の補助資料に限定。
- 移行元: 旧[PSB-CONTAINER-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/container-registry-security/README.md)。採否は[移行記録](../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#container-registry-migration)に保持。
- 採用: Exact endpoint、repository／action scope、short-lived publisher、descriptor digest、protected release、attributable audit、使用可否を明示したlifecycle、evidence health。
- 変更して採用: NISTの上位成果をprovider-neutral contractへ分解する。`active`等のstate名、期限、federation、tag protectionはrepository interpretationでありNIST要件とは扱わない。
- 不採用: Digestだけによるpublisher信頼、tagの同一性、scanner errorをquarantine成功にすること、削除だけによる全consumerからのwithdrawal、synthetic policyによるlive導入証明。
- 限界: OCI specificationはcontent identityとdistribution APIを定義しても、組織の認可・immutability・audit・retention policyを規定しない。Indexを承認しただけで選択manifestやruntimeの実行状態を観測したことにもならない。Provider、edition、API、replication、backup、legal retentionは実装時に別途確認する。

<a id="ref-application-authorization-001"></a>

## REF-APPLICATION-AUTHORIZATION-001 — Object認可の設計ガイダンス

- 発行者・役割: OWASP、[Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)。設計ガイダンスであり規格のrequirement IDではない。
- 参照版: Mutableな公式文書を2026-09-17確認。固定commitは未確定、`re-review-required`。再配布せずリンク・要約で使用。
- 利用先: `PSB-DESIGN-001 / OBJECT-AUTH-1..6`、`ENG-DESIGN-001`、請求書の教材と診断項目。
- 採用: 認証と認可を分け、既定拒否、対象と操作ごとの確認、信頼する情報源、サーバー側の強制、拒否テストを設計へ反映。
- 変更して採用: 一般的な属性・関係の設計を、このpilotではtenant・owner・操作scopeへ限定。List・export等は要検討として残す。
- 本PJの具体化判断: 文書と診断項目で完了とする。説明用のPython / SQLiteサンプルとテストは、設計説明に対する追加価値が小さいため2026-10-05に削除した。参照資料が実アプリケーションでの検証を不要としているという意味ではない。
- 不採用: 複雑なpolicy engineの追加、roleだけで個々の対象を許可する設計、IDの推測困難性だけによる保護。
- 限界: HTTP認証、session失効、並行処理、監査配送、全endpointと実組織の導入は未確認。
- ASVSとの関係: 2026-09-29に[固定releaseのV8 Authorization](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x17-V8-Authorization.md)のV8.2.1・V8.2.2を意味的に照合した。[部分的な設計関係](../mappings/frameworks.yaml)を追加したが、HTTP認証、全機能・全データの検証、ASVS level達成は示さない。規格の固定版とSHA-256は[SPEC-OWASP-ASVS-5.0.0](#spec-owasp-asvs-5-0-0)に保持。
- [組織チェックリストREF-USER-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/docs/SECURITY_GUIDANCE_SOURCES.md#ref-user-004)は引き続き原本未提供。この公開教材をその原本の復元・代替として扱わない。

<a id="spec-consumer-artifact-verification"></a>

## SPEC-CONSUMER-ARTIFACT-VERIFICATION — Consumerの受入仕様

- 利用先: `PSB-REL-001 / ACCEPT-1..5`、`ENG-REL-001`、教材。期待値の管理と強制点の選択はリポジトリでの解釈。
- 仕様: [SLSA v1.2 Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts)、[Build provenance](https://slsa.dev/spec/v1.2/build-provenance)、predicate `https://slsa.dev/provenance/v1`を保持。2026-09-17確認。
- 追加確認日: 2026-09-28。SLSA v1.2 Verifying artifactsで署名・subject・predicate type、利用者の期待値、監視と使用判断の境界を再照合。機械可読記録へ外部パラメーターと使用停止条件を補い、製品非依存の診断項目を追加しました。
- 採用: Consumer-owned trust root、署名者とbuilderの対応、subjectとの結合、build type・外部parameter等の期待値照合。受取側・registry・monitorの設置場所を分ける。
- 変更して採用: Producer提供policyも独立した認証・変更承認を通す。初回値を基準にする方式は初回信頼の限界を教材へ残す。
- 不採用: Builderが自己申告したlevelの自動承認、署名成功だけでの無害性判定、欠落時の無検証fallback。
- 保持した隣接仕様: [npm CLI v9 audit signatures](https://docs.npmjs.com/cli/v9/commands/npm-audit/#audit-signatures)。Registry signatureの補助検証であり、このcontrolの来歴期待値照合の代替ではない。旧版URLを保持し、採用時に`re-review-required`。
- Mapping根拠: `SPEC-SLSA-1.2`のBuild L2利用者側の来歴認証とBuild Provenance項目。旧`SPEC-NIST-SSDF-1.1 / PS.2.1`、`SPEC-OPENSSF-OSPS-2026.02.19 / OSPS-BR-06.01`は2026-10-03に非継承とした。旧レビューproduct-security、2026-07-27の関係と理由は[移行台帳](../docs/MIGRATION.md)に保持。
- 2026-10-03の再照合: [SLSA v1.2 Build Track Basics](https://slsa.dev/spec/v1.2/build-track-basics)、[Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts)、[Build Provenance](https://slsa.dev/spec/v1.2/build-provenance)の利用者による署名・subject・predicate type・builder・build type・external parametersの確認へ`ACCEPT-1・2・3`を限定して対応付ける。SLSA Build L2はproducerとplatformの要件も含み、このcontrolだけでlevel達成は示さない。旧`verifies/high`は実行結果ではないため`supports/medium`へ変更した。
- 同日に[SSDF 1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)の`PS.2.1`と[OSPS Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19#osps-br-0601)の`BR-06.01`も照合した。前者はsoftware acquirerへrelease integrity検証情報を提供すること、後者はofficial releaseを署名または各assetのhashを含むsigned manifestで扱うことが要件である。REL-001は利用者側の受入判断であり、提供・署名の実施はREL-002・005側の責任として旧二関係を非継承にした。
- 具体化判断: 文書と診断項目で完了。旧Ed25519 JSON署名fixtureは移植せず、採用先で導入・確認に役立つ場合だけ限定実装を検討する。Keyless、失効、timestamp、transparency、使用gateの実環境は未確認。


<a id="spec-build-containment"></a>

## SPEC-BUILD-CONTAINMENT — Buildの実行権限と強制境界

- 役割: 旧Build controlの設計根拠と参照仕様を保持する記録。製品非依存の構造・確認方法はリポジトリでの解釈。
- 利用先: `PSB-BUILD-001 / BUILD-1..6`、`ENG-BUILD-001`、学習ノート。
- 採用: 実行コードから秘密情報・公開権限を分離し、外側で通信・隔離を強制する。観測とhealthを区別する。
- 変更して採用: 旧JSONのread-only、telemetry等の宣言を実効性の証拠にせず、採用先の拒否・収集確認へ分ける。
- 追加確認日: 2026-09-28。機械可読記録を本文の通信強制・観測健全性・昇格停止へ揃え、診断項目を追加。HTTPS origin allowlistを唯一の方式に固定しない。これは本PJの設計解釈であり、SLSAが通信遮断やsensor導入を一律に要求するという意味ではない。
- 不採用: 旧JSON計画・検証器・期待結果を実行時封じ込めの実装として移植しない。短命OIDCの15分上限は旧例のpolicyであり、一般要件として継承しない。
- 限界: Provider固有の強制、sensor、実環境は未確認。旧frameworkレビューproduct-security、2026-07-27の版・ID・関係は[移行台帳](../docs/MIGRATION.md)に履歴として保持する。

保持した参照仕様:

- [GitHub automatic token authentication](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication): 旧参照URLを保持。現在の設定・実効権限は採用時に再確認する（`re-review-required`）。Token permissionsはhostやcloud権限を制限するものではない。
- [SLSA v1.2 Build track basics](https://slsa.dev/spec/v1.2/build-track-basics): 2026-09-17確認、2026-09-28に[Build requirements](https://slsa.dev/spec/v1.2/build-requirements)と併せて再照合。Build L3のrun間隔離・来歴署名用secret分離を設計入力に使う。Build trackへの関係でありSource trackやlevel達成の主張ではない。
- 2026-10-03に[SLSA v1.2 Build Track Basics](https://slsa.dev/spec/v1.2/build-track-basics)と[Build Requirements](https://slsa.dev/spec/v1.2/build-requirements)を再照合。`BUILD-1・4`の秘密情報・管理面と一時環境の分離だけをBuild L3隔離の部分的な設計関係とする。Run間の影響、cache改変、署名secretの実保護、基盤評価とlevel達成は未確認。
- 2026-10-03に[OSPS Baseline BR-01.03](https://baseline.openssf.org/versions/2026-02-19#osps-br-0103)を再照合。未信頼code snapshotを扱うCI/CDから特権credential・assetへ届かせない要件に、`BUILD-1・2`の設計が部分的に対応する。旧`verifies/high`は実証済みを意味しないため`supports/medium`へ改める。Live pipelineでの拒否や全経路の適用は未確認。
- 旧`SPEC-NIST-SSDF-1.1 / PW.6.1 / supports/high`は[SSDF公式本文](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)でコンパイラ・インタプリタ・ビルドツールのsecurity機能・更新・完全性確認を扱う。BUILD-001はビルド対象コードの実行権限と隔離を扱い、ツールの選定・保守を要求しないため非継承。旧関係は[移行台帳](../docs/MIGRATION.md)へ残す。
- [cicd-sensor固定snapshot](https://github.com/cicd-sensor/cicd-sensor/tree/6e08deb2221c19a854d8d3be7ce37c659c15bce9): 採否・ライセンス・制限は`REF-BUILD-001`を正本とし、未導入の候補として保持。

<a id="spec-slsa-1-2"></a>

## SPEC-SLSA-1.2 — SLSAのversion付き仕様

- 発行者・版: SLSA、1.2。[Build track basics](https://slsa.dev/spec/v1.2/build-track-basics)と[Build requirements](https://slsa.dev/spec/v1.2/build-requirements)を2026-09-24確認。
- 固定source: tag `v1.2`、commit `19e4e2f005f871270c4f555fc47afecfb37f3efe`。正確なlocal identifierと責任主体は旧[registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/slsa/README.md)を保持。
- 利用先: `PSB-BUILD-001`のBuild L3隔離への部分的な設計関係、`PSB-BUILD-003`のprovenance生成2件、`PSB-REL-001`の利用者側の部分的な設計関係2件、`PSB-REL-002`のproducer distribution関係。
- 採用: Buildの隔離と来歴の生成・署名権限を分ける設計根拠。
- 限界: 各controlは責任主体の一部だけを扱う。Platform assessment、level全体、Source track、組織のSLSA達成を保証しない。

<a id="spec-provenance-distribution"></a>

## SPEC-PROVENANCE-DISTRIBUTION — Artifactとprovenanceの配布仕様

### 役割・利用先・参照版

[PSB-REL-002](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)、
[ENG-REL-002](../engineering/release-integrity/provenance-distribution-and-availability/README.md)と教材の直接の設計入力です。

- SLSA、version `1.2`、status `Approved`。[Build requirements](https://slsa.dev/spec/v1.2/build-requirements)のproducer `Distribute provenance`と[Distributing provenance](https://slsa.dev/spec/v1.2/distributing-provenance)を2026-09-25に確認。固定sourceは[SPEC-SLSA-1.2](#spec-slsa-1-2)と同じtag `v1.2`、commit `19e4e2f005f871270c4f555fc47afecfb37f3efe`。Community Specification License 1.0。
- 追加確認日: 2026-09-28。Distributing provenanceで成果物と証明の関係を再照合。教材を利用者の取得経路から読み直し、公開準備中という状態表示と実際の取得・使用制限を区別しました。具体的な強制点の選択は本PJの設計解釈であり、実配布先での動作確認ではありません。
- NIST SP 800-218、SSDF `1.1`、2022年。[SPEC-NIST-SSDF-1.1](#spec-nist-ssdf-11--nist-sp-800-218)の`PS.2.1`を利用。2026-09-25にtask title「software integrity verification informationをsoftware acquirerへ利用可能にする」範囲を再照合。
- 移行元: 旧[PSB-REL-002](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/provenance-publication-distribution/README.md)。旧check、fixture、mappingの採否は[移行記録](../docs/MIGRATION_RELEASE.md#provenance-distribution-migration)に保持。

### 採用・変更・不採用

- 採用: Producerがprovenanceをconsumerへ配布する責任、artifact単位のbinding、artifactからattestationへのrelation、publish時の同伴、複数の配布場所、immutability、consumerが受け入れられるformat。
- 変更して採用: SLSAの上位仕様を、artifact family・channel scope、exact digest inventory、partial publication、consumer-view access、retention、no downgrade、collection healthへ具体化する。Package ecosystemへ委譲する場合もconsumer retrievalを確認する。
- 不採用: 一releaseにつき一provenance、一artifactにつき一attestationへの固定、public accessの必須化、同じhost・pathだけを許すこと、固定5分・365日、`immutable: true`・`available: true`の自己申告による導入済み判定。

### Mappingと限界

SLSA `build-l1#producer-distributes-provenance`とSSDF `PS.2.1`を`supports / medium / design-reviewed`で現行特性へ部分割当する。SLSA local IDは固定版registryの識別子であり、controlだけによるBuild L1以上の達成を示さない。SSDFのtaskはprovenanceだけを唯一の実現方法として指定しない。

SLSAは特定registry、release service、API、認証方式、保持日数、availability SLOを規定しません。SSDFもartifact-attestation relationや配布実装を規定しません。Live publication、consumer retrieval、immutability、replication、garbage collection、retention、withdrawalは未検証です。

<a id="spec-platform-provenance-generation"></a>

## SPEC-PLATFORM-PROVENANCE-GENERATION — Platform provenance生成仕様

- 区分: `normative-specification`と、このリポジトリでの責任分離。
- 発行者・版: SLSA、1.2。固定sourceは`SPEC-SLSA-1.2`と同じtag `v1.2`、commit `19e4e2f005f871270c4f555fc47afecfb37f3efe`。
- 確認日: 2026-09-24、2026-09-28に再照合。[Build requirements](https://slsa.dev/spec/v1.2/build-requirements)、[Build provenance](https://slsa.dev/spec/v1.2/build-provenance)、[Assessing build platforms](https://slsa.dev/spec/v1.2/assessing-build-platforms)の公式v1.2公開版を確認。
- 利用先: `PSB-BUILD-003 / PROV-GEN-1..6`、[教材](../controls/records/build-security/psb-build-003-platform-provenance-generation/learning.md)、`ENG-BUILD-002`、移行記録。
- 採用: Platformによるprovenance生成、output digestによるsubject識別、`buildDefinition`・`runDetails`・`buildType`・`externalParameters`・`builder.id`、control-plane由来の必須data、consumerが検証できるauthenticity、tenantの改変を抑止する境界。
- 変更して採用: SLSA level profileをcontrolの合否にせず、生成coverage、artifact binding、field source、認証、失敗時のhandoffへ分解する。Signatureは代表的方式だが、consumerがauthenticityを検証できる別方式も排除しない。
- 不採用: `invocationId`を全採用先で必須とする旧要件、jobが作ったJSONへplatformが署名すれば全fieldがplatform由来になるという解釈、provenanceが成果物の無害性や完全な依存inventoryを証明するという解釈。
- 限界: SLSA Build L2ではsubjectとL2必須でないfieldにtenant由来の例外があり、`resolvedDependencies`の完全性はbest effort。L3の生成・検証要件もこの例外を参照するため、例外なく全fieldがplatform由来とは読まない。強いunforgeability、signing secret保護、build間隔離は別途platform assessmentが必要。
- 実装判断: Providerと認証profileが未選定のため製品実装は作らない。旧synthetic statementとlocal OpenSSL検証をplatform実装の証拠として移植しない。

<a id="spec-dependency-lock-identity"></a>

### SPEC-DEPENDENCY-LOCK-IDENTITY — Native lockとartifact完全性の仕様

- 区分: `product-specification`。下記の横断ガイドは設計入力として区別する。
- 発行者: npm、pnpm、pip、Astral、Yarn、Bunの各project。
- 利用先: `PSB-DEPS-003 / DEP-ID-1..5`、`ENG-DEPS-003`、[DEPS-003の教材](../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/learning.md)。
- 移行元: `controls/dependency-security/lockfile-integrity/README.md`と`control.yaml`。
- 固定した文書改訂: 未特定。変更可能なURLは`re-review-required`。
- 今回の確認日: `2026-09-16`。npm ci v11とuv project syncの公式文書を確認。他製品の現在の挙動は未再確認。
- 追加確認日: `2026-09-27`。npm ci v11のmanifest不一致拒否・lock非更新と、uvの`--locked`による鮮度確認・`--frozen`による鮮度確認の省略を再確認。全製品のCLIを実行した意味ではない。
- 採用: manifestとlockの対応、全対象依存の記録、hash照合、通常buildでlockを書き換えないことを別特性として扱う。
- 変更して採用: package manager別wrapperとsynthetic fixtureの一括移植をせず、設計判断と製品仕様を残す。
- 不採用: frozenという名前だけでmanifest鮮度を推論すること、versionだけでbytesの同一性を主張すること。
- 追加して採用: 展開済みの依存環境と取得ファイルのhash照合を分け、既存状態を承認した入力へ結び付けて確認できない場合は新しい環境で取得する。pipの具体的な根拠は[SPEC-INSTALL-EXECUTION-POLICY](#spec-install-execution-policy)へ分ける。
- 限界: 配布ファイルの同一性は安全性・originの正当性・導入済み状態を証明しない。

旧成果物が参照した仕様は以下を保持する。旧runtimeのpnpm `11.25.0`等は旧実装の基準であり、
今回の新しい実装対応版として認定しない。YarnとBunの旧例はreference-only、他製品の旧tamper testも
移行先で再実行したとは扱わない。

- npm: [package-lock.json v10](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json/)、[npm ci v11](https://docs.npmjs.com/cli/v11/commands/npm-ci/)、[version指定なしのnpm ci](https://docs.npmjs.com/cli/commands/npm-ci/)
- pnpm: [lockfile](https://pnpm.io/lockfile)、[install](https://pnpm.io/cli/install)
- pip: [Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/)。今回のpip挙動検査は[SPEC-INSTALL-EXECUTION-POLICY](#spec-install-execution-policy)の限定範囲のみ
- uv: [project lock layout](https://docs.astral.sh/uv/concepts/projects/layout/#the-lockfile)、[project sync](https://docs.astral.sh/uv/concepts/projects/sync/)、[CLI / uv pip sync](https://docs.astral.sh/uv/reference/cli/#uv-pip-sync)。`--locked`による鮮度確認と`--frozen`による更新回避を区別する
- Yarn: [install](https://yarnpkg.com/cli/install)、[checksumBehavior](https://yarnpkg.com/configuration/yarnrc/#checksumBehavior)
- Bun: [install](https://bun.com/docs/pm/cli/install)、[lockfile](https://bun.com/docs/pm/lockfile)、[auto-install](https://bun.com/docs/runtime/auto-install)

隣接ガイドも省略しない。下記は今回全文を再レビューしておらず、direct mappingの追加根拠にはしない。

- [SLSA v1.2](https://slsa.dev/spec/v1.2/)：build input・provenanceとの受け渡し。旧来どおりdirect mappingなし
- [OWASP SCVS](https://scvs.owasp.org/)：component検証の設計入力。採用する要件・版は別途レビュー
- [CISA developer supply-chain guide](https://www.cisa.gov/resources-tools/resources/securing-software-supply-chain-recommended-practices-guide-developers)：取得・利用の連鎖を考える入力。正確な刊行版は再確認

旧mappingにはATT&CK `v19.1 / T1195.001`、SSDF `1.1 (SP 800-218, 2022) / PW.4.1`、
OSPS `2026.02.19 / OSPS-BR-05.01`がありました。旧レビューは`product-security / 2026-08-31`。
これは再照合前の履歴であり、現在の採否は次段落を参照してください。

2026-10-03にDEPS-003の三関係を再照合しました。[ATT&CK v19のT1195.001](https://attack.mitre.org/versions/v19/techniques/T1195/001/)に対し、レビュー後の再解決と取得物の差し替えを拒否する設計は一部の侵入経路を狭めます。承認したlockやhash自体が悪意ある場合は止められません。[NIST SP 800-218最終版](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)では、旧`PW.4.1`の部品取得・維持全体より、`PW.4.4`の例6にある部品完全性確認が直接の接点です。Hashは事前にレビューしたbytesとの一致だけを示し、出所や無害性を示しません。[OSPS-BR-05.01](https://baseline.openssf.org/versions/2026-02-19#osps-br-0501)は標準的な依存管理ツールの使用を求めますが、DEPS-003の特性は製品非依存の入力・bytes照合であり、標準ツールの使用自体を必須にしていません。旧OSPS関係は非継承とし、旧`PW.4.1`関係も新`PW.4.4`関係へ自動継承せず、[移行台帳](../docs/MIGRATION.md)に採否を記録します。

<a id="ref-deps-002"></a>

### REF-DEPS-002 — GitHub dependency review guidance

- 区分: `implementation-guidance`、発行者: GitHub、状態: `adopted-partially`。
- 旧一覧のレビュー日: `2026-07-31`、今回のconcept文書確認日: `2026-09-16`。
- 固定文書改訂: 未特定、`re-review-required`。ActionのREADMEのみ下記のcommitで固定。
- 利用先: `PSB-DEPS-004 / DEP-REVIEW-1..3`、`ENG-DEPS-003`、[DEPS-004の教材](../controls/records/dependency-security/psb-deps-004-dependency-change-review/learning.md)、GitHub実装例。
- 採用: current base/head比較、対応依存の差分と既知脆弱性判定、必須merge gateへの接続。
- 変更して採用: GitHubを必須製品にせず、比較・判定・強制の責任を製品非依存で定義する。
- 不採用: license・Scorecard・origin・provenance等を基本workflowが判定済みと扱うこと。追加policyは別に明示する。
- 限界: advisoryのない悪意、coverage不足、実効ruleset、全platform・依存の完全性をActionの存在だけで証明しない。

参照仕様:

- [Dependency review concepts](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review)
- [Configure dependency review action](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-dependency-review-action)
- [Dependency review REST API](https://docs.github.com/en/rest/dependency-graph/dependency-review)
- [Reviewing dependency changes](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-dependency-changes-in-a-pull-request)
- [Action README / configuration](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/README.md#configuration)：旧実装のfull SHAを保持。更新時はsemantic diffをレビュー
- [同revisionのgetComparisonとrun](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/src/main.ts)、[dependency graph比較](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/src/dependency-graph.ts)、[action.yml](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/action.yml)、[配布コードの同じ処理](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/dist/index.js#L677-L703)。2026-09-27にsourceと配布コードを確認。Snapshot警告の再試行期限後も比較結果を返して判定を続け、警告だけを失敗にする条件はない。未評価の拒否を別に確認する[実装ガイド](../engineering/dependency-security/reviewed-dependency-intake/implementations/github/README.md)へ反映。
- [GitHub required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)。2026-09-27に`skipped`・`neutral`も受理し得る仕様を確認。必須検査の登録と必要な評価の完了を同一視せず、実対象の拒否確認へ採用。
- [Trivy filesystem](https://trivy.dev/docs/latest/target/filesystem/)、[repository](https://trivy.dev/docs/latest/target/repository/)：旧READMEの隣接比較資料。今回未再確認。継続SCAや代替profile候補であり、base/head差分を自動的に満たさない

旧参照一覧はlicense、取得元、来歴、独立承認、期限付き例外を拡張提案として掲げ、synthetic fixture中心と
記述している。一方、移行元の現行`PSB-DEPS-004`はGitHub Actionの既知脆弱性gateとlive ruleset確認を中心とする。
この範囲差を隠さず、拡張提案を基本実装の保証に昇格させない。追加する際は根拠と観測範囲を別途レビューする。
固定Actionの成功だけで依存データの完全性や未評価の拒否を主張しません。今回のsource・配布コード確認は静的な読解で、実GitHubのデータ準備・Action実行・必須判定・merge拒否は未確認です。

旧mappingのOSPS `2026.02.19 / OSPS-VM-05.01..03`、SSDF `1.1 (SP 800-218, 2022) / PW.4.1`、
ATT&CK `v19.1 / T1195.001`は、旧レビュー`product-security / 2026-09-03`からの移行時に一旦保持した関係です。
2026-10-03に[OSPSの固定版](https://baseline.openssf.org/versions/2026-02-19#osps-vm-0503)を照合しました。`OSPS-VM-05.03`のうち、変更された依存の既知脆弱性を明示方針で評価してmerge前に拒否する部分だけ採用します。悪意ある依存の検知、すべてのコード変更の自動評価、非悪用の宣言と抑制はDEPS-004の必須特性ではありません。`OSPS-VM-05.01`は脆弱性とライセンスのSCA所見を扱う文書化された是正閾値、`OSPS-VM-05.02`は任意のrelease前にSCA違反へ対応する方針を求めます。変更依存の採用前gateだけでは直接の対応関係を説明できず、旧二関係を非継承とします。

[NIST SP 800-218最終版のPW.4.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)は、第三者部品の採用・維持と用途別評価を扱います。差分を見せて採用を判定する部分だけに対応させ、承認済み部品の維持、来歴確認、利用文脈全体の評価へ拡張しません。[ATT&CK T1195.001](https://attack.mitre.org/versions/v19/techniques/T1195/001/)は悪意ある依存・開発ツールの改変という攻撃技法です。既知脆弱性の差分gateは悪意ある内容の検知を要求しないため、旧`mitigates`関係を非継承とします。両資料の利用範囲、限界、旧関係の採否は[現行mapping](../mappings/frameworks.yaml)と[移行台帳](../docs/MIGRATION.md)で区別します。実GitHubでのmerge拒否やOSPS・SSDF適合性は確認していません。

| 追加移行の成果物 | 直接の根拠 | 横断分析の入力 |
|---|---|---|
| PSB-DEPS-003 | SPEC-DEPENDENCY-LOCK-IDENTITY | REF-PORTFOLIO-001、LOCAL-SUPPLY-CHAIN-ATTACK-STAGES |
| PSB-DEPS-004 | REF-DEPS-002 | 同上 |
| ENG-DEPS-003、PSB-DEPS-003・004の各教材 | 上記二資料の役割を分けて利用 | 同上 |

旧`docs/SECURITY_GUIDANCE_SOURCES.md`にある他の`REF-*`は削除または否定していません。このパイロットの対象外として
旧参照資料一覧に残し、対応するコントロール／パターンを移すときに、参照資料記録ごと移行します。

## REF-EXTERNAL-SURFACE-001

### 役割・利用先・参照時点

[DETECT-003](../controls/records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md)と[ENG-DETECT-002](../engineering/detection-verification/external-observation-and-inventory-reconciliation/README.md)の設計入力。2026-09-26に以下のNIST・CISAの一次資料と移行元の旧controlを確認した。これは組織の資産台帳や実際の外部観測の証拠ではない。

- NIST、[The NIST Cybersecurity Framework (CSF) 2.0](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final)、CSWP 29、2024-02-26最終版。資産・サービスを管理する成果（ID.AM）と、実現方法を一律に指定しない枠組みとして参照。
- CISA、[BOD 23-01: Improving Asset Visibility and Vulnerability Detection on Federal Networks](https://www.cisa.gov/news-events/directives/bod-23-01-improving-asset-visibility-and-vulnerability-detection-federal-networks)、2022年発行。資産発見と脆弱性列挙を別の活動とする説明を参照。連邦民間行政府向けの指令であり、対象組織と周期は本PJの一般要件にしない。
- 移行元の[旧PSB-DETECT-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/detection-verification/external-attack-surface-reconciliation/README.md)、commit `f42987759218c9b8daf3924320542a1935ef78e0`。外部観測の帰属、台帳との照合、再出現、収集障害を分ける設計材料。

### 採否と限界

採用: 管理責任のある起点から候補を探し、台帳と照合し、未登録・期待外・再出現を担当者へ渡す。資産発見と脆弱性診断を分ける。観測の範囲と失敗を結果へ結ぶ。

変更して採用: 旧実装のdomain-only、CT・DNS・HTTPS三手段必須、HTTPS 443番、固定の鮮度・見直し日数は限定profileへ留め、対象と収集元に応じて選ぶ。IPや応答情報は一律禁止せず、目的・権限・保存先に応じて最小化する。

不採用: 旧fixtureの成功をliveな外部公開面の網羅・是正完了・脆弱性不在の証拠にしない。BODの連邦機関向け周期を一般組織へ移さない。

限界: NISTとCISAの資料は外部収集APIの仕様、ドメインの所有、第三者IPの調査許可、実環境の発見率を保証しない。観測元固有の仕様と許可は実装時に再確認する。旧ATT&CKとSSDFの関係は[移行記録](../docs/EXTERNAL_ATTACK_SURFACE_MIGRATION.md#参照とmapping)で非継承とした。

2026-09-29の読み合わせでNIST CSF 2.0の公開ページを再確認し、CISA BOD 23-01は検索結果の公開本文を確認した（直接取得は403）。部分取得時に前回候補を保持し、成功した範囲の新候補だけ調査へ進める状態遷移は、両資料の具体的な指定ではなく本PJの解釈として[pattern](../engineering/detection-verification/external-observation-and-inventory-reconciliation/README.md#観測障害と状態)に記録した。

## REF-SCANNER-EVIDENCE-001

### 役割・利用先・参照時点

PSB-DETECT-001、ENG-DETECT-001、Zero findings教材の設計入力。旧`REF-DETECT-001..003`を役割に合わせて統合しました。
旧レビュー日2026-07-30（Trivy）・2026-07-31（DockSec）・2026-08-14（Checkov比較）を保持します。初回移行と今回のframework照合では、製品仕様や現在の配布物を再確認していません。

2026-09-27、DETECT-001の機械可読記録を製品非依存の本文へ揃えました。特定の署名方式・終了コード・全カテゴリfixture・DockSecの固有挙動を共通要件にしません。旧製品資料の確認を更新したという意味ではなく、workflow検査の追加確認は[別の仕様記録](#spec-zizmor-workflow-analysis)へ分けています。

### 保持する製品資料とidentity

- Trivy: [v0.72.0](https://github.com/aquasecurity/trivy/releases/tag/v0.72.0)、reviewed source `8a32853686209a428179bb3a1688802b25691564`、Linux archive SHA-256 `bbb64b9695866ce4a7a8f5c9592002c5961cab378577fa3f8a040df362b9b2ea`、[signature verification](https://trivy.dev/latest/docs/advanced/signatures/)、[offline operation](https://trivy.dev/latest/docs/advanced/air-gap/)、[GHSA-69fq-xp46-6x23](https://github.com/advisories/GHSA-69fq-xp46-6x23)。旧GitHub API観測では2026-07-30にimmutable。現在推奨するversionという意味ではない。
- OWASP DockSec: [project](https://owasp.org/DockSec/)、reviewed source `4ddcb5285f437c0e84a42c748b0f61f56543e344`、[PyPI 2026.7.5](https://pypi.org/project/docksec/2026.7.5/)、wheel SHA-256 `7f8781db7651216556c86c71ab45527bc484801b974ff264fe0ebe7f70a6f5fb`。旧確認時はTrusted Publishingなし。
- Checkov: 旧比較対象3.3.8 sdist SHA-256 `a65e5cda0337e7770436eeadabb1f65c6ce4ad7f5b145a7f801bfdf14f1aea05`、[mutable policy index](https://www.checkov.io/5.Policy%20Index/github_configuration.html)。実行dependencyとしては不採用。
- Frameworkのexact版は[SSDF](#spec-nist-ssdf-11--nist-sp-800-218)、[OpenSSF Baseline](#spec-openssf-osps-20260219--openssf-osps-baseline)、[NIST SP 800-190](#spec-nist-sp-800-190--container-security-guidance)をmappingから参照する。

### 採用・変更・不採用・限界

採用: Scanner release・publisher・実行binaryのidentity、DB・policy identity、network取得とoffline scanの分離、clean・finding・errorの区別、secret redaction、固有価値に基づくtool選定、AI remediationとgateの分離。
変更: Trivyをcontrolの名前や唯一の実装にせず、scanner acquisitionとevidence contractへ一般化。DockSecは製品固有の実装候補として保留する。
不採用: DockSec公式Actionは旧review時に内部でmutable `latest`と`curl | sh`を使用していたため不採用。External tool installer、`install-skill`、`--no-redact`、AI scoreによるrelease decisionも不採用。Checkovは固有のblocking valueが示されるまで追加しない。
限界: 固定hashはpublisher identity・semantic safety・transitive dependency完全性を単独で保証しない。Application-level offline optionはOS network isolationではない。Fixture detectionはlive coverage、最新DB、未知脆弱性を証明しない。製品採用時に現行release、署名方式、依存、CLI contractを再レビューする。

2026-09-29の読み合わせでは、指摘が見つかった範囲と解析に失敗した範囲が同時にある場合、全体の受入を止めながら既知の指摘も残す判断を[pattern](../engineering/detection-verification/scanner-acquisition-and-evidence-boundary/README.md#境界を分ける)へ追加しました。旧製品資料からの直接要件ではなく本PJの結果集約の解釈です。TrivyやDockSecの配布物・実行挙動を再確認したとは扱いません。

2026-10-03にDETECT-001の旧framework五関係を一次資料と再照合しました。[NIST SP 800-190 §4.1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)は、イメージの全層を扱うコンテナ固有の脆弱性管理、buildからregistry・runtimeまでの可視性、方針によるgateを説明します。本PJではそのうち、イメージ検査結果に対象・検出データ・対象範囲・完了状態を結び付ける部分だけを設計上の支援として採用します。実際のイメージ検査や全工程のgateは示しません。同資料の§4.4.1は稼働中ランタイムの脆弱性監視・修復を扱い、DETECT-001の一般的なartifact検査結果の扱いとは対象が異なるため非継承です。

[NIST SSDF 1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)の`RV.1.1`は脆弱性情報の継続的な収集・調査、`PW.4.1`は製品へ取り込む第三者部品の採用・維持を扱います。Scanner結果の信頼性、scanner自身の取得と選定だけでは、それぞれの成果を直接説明できません。[OSPS VM-06.02](https://baseline.openssf.org/versions/2026-02-19#osps-vm-0602)は、全コード変更を文書化された方針で自動評価し違反を拒否することを求めます。DETECT-001は証拠の扱いを定めますが、全変更の検査やmerge拒否は実装しません。旧三関係とNIST §4.4.1を非継承とし、旧版・判断は[移行台帳](../docs/MIGRATION.md)に残します。Trivy・DockSecの現行版、実scanner、live DB、組織導入は今回確認していません。


## REF-SECRET-PUBLICATION-001

### 役割・利用先・参照版

PSB-SOURCE-002のSECRET-1〜7とENG-SOURCE-003の設計入力です。2026-09-23に公開文書を確認しました。
2026-09-27に[教材](../controls/records/source-protection/psb-source-002-secret-publication-boundary/learning.md)を利用先へ追加し、Git公式のgithooks・git-receive-packを再確認しました。
同日、[git-diff-tree](https://git-scm.com/docs/git-diff-tree)のmerge差分を確認し、[Python版](../engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner/README.md)のpush検査で各親との差分を使う判断へ採用しています。実装の修正前後は無効canaryを使ったローカルGitで観測しました。その他の製品資料全体を同日に再確認した意味ではありません。
2026-09-30にGit公式のgit-receive-pack隔離説明とGitHub公式のpush protection説明を再確認しました。受信側の拒否と送信前の拒否が異なることを確認し、実際の認証情報が共有先へ届いたときは公開検索を待たずに所有者へ渡す判断を本PJの解釈として追加しました。拒否されたobjectの保持・閲覧範囲や実漏えいはproviderと状況ごとに確認します。
Git仕様は実行箇所の根拠、GitHub文書は製品での対応確認の入力、旧資料は移行判断の履歴として分けます。
下記のGit・GitHub公開URLは可変資料で固定digest未記録のため`re-review-required`です。製品実装を採用する時点で再確認します。

- Git公式：[githooks](https://git-scm.com/docs/githooks)（確認時の文書表示は2.54.0最終更新）、[git-config / core.hooksPath](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corehooksPath)、[git-push](https://git-scm.com/docs/git-push)。Hookの呼出し点、実行権限、設定変更・省略可能性を確認。
- Git公式：[git-receive-pack / Quarantine environment](https://git-scm.com/docs/git-receive-pack#_quarantine_environment)。受信したオブジェクトの隔離とref更新の境界を確認。受入拒否を、送信前の阻止と同じ意味にしない。
- GitHub公式：[Push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)。受入時検査とbypass・除外権限の区別を設計へ使用。全経路・全形式の検出や導入済み状態を推論しない。[Troubleshootingの参照URL](https://docs.github.com/en/code-security/secret-scanning/troubleshooting-secret-scanning-and-push-protection/troubleshooting-push-protection-and-secret-scanning)は今回本文取得に失敗し、制限値・全対応範囲は確認できていない。
- 旧SOURCE-002：[README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/README.md)と[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/control.yaml)。Commit `f42987759218c9b8daf3924320542a1935ef78e0`の13項目・4件の旧関係を[対応表](../docs/MIGRATION_SOURCE_PROTECTION.md#git-hooks-migration)へ保持。
- 旧実装候補：[Gitleaks v8.30.0 release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.0)。旧READMEのcontainer digest `sha256:691af3c7c5a48b16f187ce3446d5f194838f91238f27270ed36eef6359a574d9`は履歴として保持し、現行実装へ継承しない。

### 規範資料と旧mappingの扱い

[OpenSSF OSPS Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19)のOSPS-BR-07.01本文と推奨を2026-09-23に確認しました。
暗号化されていない機微情報をVCSへ意図せず保存しないという成果を、検査範囲と拒否境界の設計へ採用します。
版・既存固定commitは[SPEC-OPENSSF-OSPS-2026.02.19](#spec-openssf-osps-20260219--openssf-osps-baseline)を継承し、要件全体への適合は主張しません。

旧ATT&CK v19.1 / T1552.001は認証情報保管と公開の範囲を分け、今回の新特性への直接割当を保留します。
SSDF 1.1 / PS.3.1は[端末管理の照合](../docs/MIGRATION_SOURCE_PROTECTION.md#endpoint-migration--旧実装とframework-mapping)と同じくrelease保存との意味の不一致があるため継承しません。
CISA/FBIの[Product Security Bad Practices Version 2, January 2025](https://www.cisa.gov/sites/default/files/2025-01/joint-guidance-product-security-bad-practices-508c_0.pdf)は今回本文取得に失敗しました。
旧[registry](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/frameworks/cisa-product-security-bad-practices/registry.json)のPDF SHA-256 `c0431ac502e8bcf5ae2e4f2f47249a2aae6ead00e0af6542bd29adac850a9d3e`を保持し、現物を再照合したとは扱いません。
`CISA-PSBP-PP-08`は旧registryのローカルIDであり、CISAが発行した恒久IDではありません。旧関係と根拠は対応表に保存し、新規割当は保留します。

### 採否と限界

- 採用：コミット予定の内容・メッセージ・導入履歴の区別、検査障害の拒否、検出値の非表示、ローカルhooksから独立した受入判断。
- 変更して採用：repository-owned hooksを唯一の方式にせず、中央配布も変更権限と実効設定から評価。対象ref・内容と結果の結合、除外の期限・承認は本PJで具体化する。
- 不採用：固定した5 MiB、拡張子だけの安全判定、特定のhook frameworkやDockerの必須化、Gitleaks併用だけによる全検出の主張。CIでのmerge拒否を送信前の防止と扱わない。

2026-10-06に[Gitの受信仕様](https://git-scm.com/docs/git-receive-pack)、[GitHub Enterprise Serverのpre-receive仕様](https://docs.github.com/en/enterprise-server@3.21/admin/enforcing-policies/enforcing-policy-with-pre-receive-hooks/about-pre-receive-hooks)、[GitHub.comのpush protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)を確認しました。自前のbare Git受信側hook、GitHub Enterprise Serverの管理機能、GitHub.comの製品機能を別の導入先として扱います。このPJのGitleaks bundleが後二者で動くことや、push protectionが同じ検出範囲を持つことは採用しません。
- 限界：未知形式、符号化・分割された値、全PII・機密データ、LFS等の外部内容の完全検査は保証しない。代表実装の隔離テストは実施したが、実環境への導入・診断は未実施。旧自動テストの成功を今回の成果へ移さない。

<a id="ref-public-source-exposure-001"></a>

## REF-PUBLIC-SOURCE-EXPOSURE-001

### 役割・利用先・参照版

[PSB-SOURCE-003](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)と
[ENG-SOURCE-004](../engineering/source-protection/public-exposure-observation-and-triage/README.md)の設計入力です。
2026-09-27に[教材](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/learning.md)を利用先へ追加しました。
同日に[公式REST search](https://docs.github.com/en/rest/search/search)の`incomplete_results`と認証による検索範囲の違いを再確認しています。
投稿単位の重複抑制、部分取得の保存、通知済み状態の説明は、本PJの限定実装のコード・ローカルテストを読んだ解釈です。GitHub側や人の対応の実績には変換しません。
公開検索が非公開の共有先や受信側で拒否された送信内容を観測しないため、既知の認証情報到達をSOURCE-003で再発見するまで待たないのは本PJの責任分界です。GitHub Searchが完全な露出台帳を提供するという主張ではありません。
GitHub固有の実装をcontrolへ固定せず、public observationのcoverage、値の最小化、occurrence state、
triage、failure semanticsを具体化するために使います。

- 発行者: GitHub。区分: `product-specification-and-guidance`
- 固定commit: `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`、commit日`2026-07-24`
- 2026-09-24に確認した固定文書:
  - [REST search](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/rest/search/search.md)、SHA-256 `5d843ab038a0ab6475fafef13c7b79e3ec0566df006755aae0c63632f334417e`
  - [REST gists](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/rest/gists/gists.md)、SHA-256 `ee298d05e995f5b3b44e91292a27ea9ac496ff697eaea57a042cb8d4a5caf9e4`
  - [Code Search syntax](https://github.com/github/docs/blob/b17436de8f10c3e7f6a185d6813bf94bc82d22f8/content/search-github/github-code-search/understanding-github-code-search-syntax.md)、SHA-256 `8c5ae09003613732a13c3924c07f3acf77c1d655bc1c5d8e58247f478afc68cb`
- 移行元: [旧SOURCE-003](https://github.com/DharmaDoll/product-security-controls/blob/91fdb7661b38723ce6fb38da93cf3c68b701e521/controls/source-protection/public-repository-exposure/README.md)。
  旧PoCのcheck、実装、mappingは[移行記録](../docs/MIGRATION_SOURCE_PROTECTION.md#public-exposure-migration)で再配置。

### 採用・変更・不採用

- 採用: Searchにはresult・repository scope・rate・timeoutによる制限があり、`incomplete_results`を返し得ること、
  Gist contentとfile listがtruncatedになり得ること、query syntaxとqualifierがprovider仕様であること。
  これらを0 findingsとcollection failureを分ける設計根拠にする。
- 変更して採用: GitHubの具体的な上限値やqueryをcontrolの普遍要件にせず、採用実装がproviderごとの上限、
  cursor、truncation、認証viewを記録するpropertyへ一般化する。Public-only identity、deduplication、期限付きreview、
  notification handoffは旧PoCから継承した本リポジトリの設計判断として区別する。
- 不採用: GitHub Actions、Python、専用Git state branch、browser GET queryを唯一または必須の解法にしない。
  Match本文の永続保存、credential validation、HTML scraping、rate-limit回避、第三者資産のactive probingを採用しない。
- Mapping照合: 2026-09-24に固定版の原文を確認し、ATT&CK `T1593.003`だけを現行6特性へ部分割当。
  ATT&CK `T1552.001`、SSDF `RV.1.1`、OSPS `OSPS-BR-07.01`は対象成果が異なるため非継承。
  詳細は[移行記録](../docs/MIGRATION_SOURCE_PROTECTION.md#public-exposure-migration--旧framework-mapping)を参照。

### 限界

2026-09-26、[GitHub REST Code Searchの旧構文](https://docs.github.com/en/search-github/searching-on-github/searching-code)で記号が検索語として扱われないこと、既定branchなどの検索制限を再確認。[Issue・PR検索](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests)の`is:public`と`in:title,body`も同日に確認。これらは[GitHub indicator watch](../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)のquery、手動精査、公開対象の範囲を選ぶ根拠です。現行URLは可変のため`re-review-required`。

固定GitHub文書は一つのprovider仕様であり、他providerや一般Web indexのcoverageを説明しません。
Searchは公開contentの完全なinventoryではなく、0件は過去・cache・clone・画像・binary・難読化された値の不存在を
示しません。今回、実GitHub search、Gist収集、組織indicator、credential、通知、responseを実行していません。
新しい限定実装のlocal mock testは実際のGitHub検索・通知を確かめません。導入時にはAPI版、認証要件、利用条件、retention、料金・plan、provider変更を再確認します。

<a id="ref-credential-exposure-containment-001"></a>

## REF-CREDENTIAL-EXPOSURE-CONTAINMENT-001

### 役割・利用先・参照版

[PSB-GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)と
[ENG-GOV-003](../engineering/governance-operations/credential-exposure-containment/README.md)のincident response設計入力です。

- 発行者: National Institute of Standards and Technology (NIST)。区分: `incident-response-guidance`。
- 参照刊行物: `NIST SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile`。
- 公開日: `2025-04-03`。確認日: `2026-09-24`。
- 公式資料: [NIST CSRC publication page](https://csrc.nist.gov/pubs/sp/800/61/r3/final)、[DOI 10.6028/NIST.SP.800-61r3](https://doi.org/10.6028/NIST.SP.800-61r3)。Rev.3がRev.2を置き換えたこともpublication pageで確認。
- 補足の製品ガイダンス: 発行者GitHub。[secret scanning alert対応](https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-secret-scanning-alerts/resolving-alerts)と[認証情報の有効性による優先付け](https://docs.github.com/en/code-security/tutorials/remediate-leaked-secrets/evaluating-alerts)を2026-10-06に確認。非公開リポジトリのsecretも対応対象とし、有効性・権限・到達範囲を見ずに公開／非公開だけで緊急度を固定しない判断へ利用する。GitHubの可変文書であり`re-review-required`。実際の認証情報や組織の優先度方針は未確認。
- 移行元: [旧PSB-GOV-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/governance-operations/credential-exposure-containment/README.md)。旧check、実装、mappingの採否は[移行記録](../docs/MIGRATION_GOVERNANCE_OPERATIONS.md#credential-exposure-migration)に保持。

### 採用・変更・不採用

- 採用: Incident responseを一回の秘密情報交換ではなく、準備、検知、対応、復旧と継続改善をrisk managementへ統合する考え方。RespondとRecoverを分け、組織のowner・communication・証拠・復旧判断へ接続する。
- 変更して採用: Credential incidentに必要なsecret-free authority graph、class別封じ込め、bounded replacement、consumer disposition、旧authorityの独立した拒否確認、exposure-window identityを本リポジトリで具体化する。
- 不採用: 旧controlにあった4時間のauthorization上限、七つのsurface、固定したevidence-first順序をNIST要件として扱わない。緊急封じ込めが必要な場合は、保全と並行して判断理由・失う証拠を記録する。
- 実装判断: NIST自身がRev.3の実施詳細は技術・環境・組織により変わると説明しているため、provider-neutralなrevoke scriptを作らない。Providerとcredential classが決まった時点で公式API仕様を別のimplementation sourceとして追加する。

### Mappingと限界

ATT&CK `v19.1 / T1078`は漏えいしたvalid accountの継続利用を制限する設計関係として部分割当します。
NIST SSDF `RV.2.1`はsoftware vulnerabilityのrisk response計画、OSPS `AC-04.01`はCI/CDの未指定permissionのdefaultを
対象とするため非継承です。NIST SP 800-61 Rev.3は本リポジトリのframework mappingや準拠判定には使いません。

同刊行物は特定providerのcredential失効、session invalidation、signing trust、replacement scope比較、audit retention、
安全なdenial probeを規定しません。これらは旧成果物と攻撃経路を再評価したrepository interpretationです。
本移行ではlive provider、credential、consumer、audit、response exerciseを検証していません。

<a id="ref-deployed-artifact-recovery-001"></a>

## REF-DEPLOYED-ARTIFACT-RECOVERY-001

### 役割・利用先・参照版

[PSB-GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)と
[ENG-GOV-004](../engineering/governance-operations/deployed-artifact-recovery/README.md)の設計入力です。

- NIST SP 800-218、SSDF `1.1`、2022年。[公式資料](https://csrc.nist.gov/pubs/sp/800/218/final)の`RV.1.1`と`RV.2.1`を2026-09-24に照合。固定版と限界は[SPEC-NIST-SSDF-1.1](#spec-nist-ssdf-11--nist-sp-800-218)を使用。
- NIST SP 800-61 Rev.3、2025年4月。[公式資料](https://csrc.nist.gov/pubs/sp/800/61/r3/final)を2026-09-24に確認。Incident responseとrecoveryをrisk managementへ接続する上位ガイダンスとして利用。
- 旧成果物: [PSB-GOV-005 Deployed artifact refresh](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/governance-operations/deployed-artifact-refresh/README.md)。旧check・fixture・mappingの採否は[移行記録](../docs/MIGRATION_GOVERNANCE_OPERATIONS.md#deployed-artifact-recovery-migration)に保持。

### 採用・変更・不採用

- 採用: Softwareとcomponentのpotential vulnerability情報を継続して収集・調査し、risk情報からremediation等を計画するSSDFの成果。RespondとRecoverを分け、復旧判断を継続的risk managementへ戻すNIST SP 800-61 Rev.3の考え方。
- 変更して採用: Exact deployed digest、artifact-bound SBOM、current evidence、distinct replacement digest、targetごとのobserved deployment、old digest非稼働を一つのcaseへ結ぶ。これは旧controlを再評価した本リポジトリの具体化。
- 不採用: 旧fixtureのsynthetic deadlineを組織SLAにしない。Signatureやfresh rebuildだけで現在安全と判断しない。Tag更新、build success、partial rolloutをclosureにしない。
- 実装判断: Builder、registry、admission、deployment platformを選定していないため、provider-neutralなverifierを作らない。採用先で接続・確認に実効性がある場合だけ、各製品の公式contractを確認して具体化する。

2026-09-28に上記NIST SSDF 1.1とSP 800-61 Rev.3の公開ページを再確認しました。GOV-003の元の対応期限、GOV-002で承認した旧digestの一時使用、GOV-005の復旧完了を別の判断としてつなぐのは本PJの設計判断です。例外が有効でも旧digestの非稼働は証明されず、元の範囲を新しく観測できなければケースを閉じません。Builder・registry・稼働環境での実確認は行っていません。

2026-10-01の横断レビューでは、検知アラートの不在やrollout成功を旧digest非稼働の証拠にせず、元のtargetごとの稼働inventory、取得時刻、coverage、停止・切り戻し経路を照合する判断を補いました。対象の一部を廃止する場合も、検索結果からの消失と実体の停止・再投入経路の解消を区別します。これは本PJの復旧完了条件の具体化であり、上記NIST資料が特定のinventory方式や状態名を要求するとの主張ではありません。Liveの観測や拒否は行っていません。

### Mappingと限界

SSDF `RV.1.1`は`ARTIFACT-RECOVERY-2`、`RV.2.1`は`ARTIFACT-RECOVERY-3`だけへ部分割当します。
ATT&CK `T1195.002`はcompromised application softwareの残存を減らすrebuild・replacementとの設計関係です。
OSPS `DO-04.01`はreleaseごとのsupport scope・durationをproject documentationへ記載する要件であり、
support evidenceを消費する本controlの実行成果ではないため非継承です。

これらの資料はclean rebuildの具体条件、provenance生成、registry publication、admission、全deploymentの観測、old digest removalを
単独では定義しません。Provenance生成は`PSB-BUILD-003`、registry publicationは`PSB-CONTAINER-002`、artifactの使用許可は`PSB-CONTAINER-001`へ分離し、live provider／admissionは未実装です。End-to-end recoveryは未検証です。

<a id="ref-vulnerability-priority-001"></a>

## REF-VULNERABILITY-PRIORITY-001

[PSB-GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)と
[ENG-GOV-005](../engineering/governance-operations/vulnerability-priority-decision/README.md)、[教材](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/learning.md)の設計入力です。

- NIST SP 800-218、SSDF `1.1`の`RV.1.1`・`RV.2.1`。固定版は[SPEC-NIST-SSDF-1.1](#spec-nist-ssdf-11--nist-sp-800-218)。2026-09-24に公式本文を照合。
- CISA [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)と公式JSON・CSV・JSON Schema。継続更新data sourceであり、2026-09-24に公式pageがprioritization inputと説明することを確認。Snapshotの時刻・完全性・schema・digest・healthを別途必要とする。
- 2026-09-28に[CISA管理のKEV data mirror](https://github.com/cisagov/kev-data)を確認。READMEはCISAサイトを正本、mirrorを少し遅れて更新される配布先と説明している。収録形式はJSONとCSVでschemaも置かれる。これは随時更新される参照先であり、固定snapshotやlive取得を本PJで検証した記録ではない（`re-review-required`）。
- FIRST [CVSS v4.0 Specification Document](https://www.first.org/cvss/v4.0/specification-document)、document version `1.2`。2026-09-24にBase・Threat・Environmental・Supplementalの役割を確認。
- FIRST [PSIRT Services Framework v1.1](https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1-1)。2026-09-24に公式version一覧と高水準frameworkであることを確認。2026-10-04にService 3.3のFunction 3.3.5（影響製品と変種）、Service 4.1のSub-function 4.1.1.1（製品inventory）、Service 4.2のSub-function 4.2.1.2（影響製品・版）を公開本文で再確認。
- 旧成果物: [PSB-GOV-003](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/governance-operations/exploited-vulnerability-prioritization/README.md)。採否は[移行記録](../docs/MIGRATION_GOVERNANCE_OPERATIONS.md#vulnerability-priority-migration)に保持。

採用するのは、credible vulnerability情報を継続収集・調査すること、risk responseを計画すること、KEV掲載・非掲載・取得不能を
分けること、CVSS metricの意味とprovenanceを保持すること、PSIRT caseへownerと次の処理を割り当てることです。
CVSSをbusiness risk・SLA・悪用予測にせず、KEV非掲載を未悪用・低riskにせず、CISA due dateを組織期限へ自動変換しません。
PSIRT frameworkからは、報告の検証時に影響製品と変種を調べ、修正対象の製品・版を見定める視点も採用します。CVE・PURL・SBOMは自社コードの問題の必須入力にせず、機能・構成・製品版と確認範囲を調べるのは本PJの具体化です。FIRSTの記述を、全製品の再現試験や特定の調査方法の義務とは扱いません。PSIRT frameworkの参照を組織能力の導入証拠にしません。Live feed、calculator、inventory、ticket、PSIRT運用は未検証です。

2026-09-28にFIRSTのCVSS v4.0仕様（文書版1.2）とNIST SP 800-218 final 1.1の公開ページを再確認しました。KEVのCISA本体ページは今回取得できず、上記CISA管理mirrorの説明を確認しています。製品担当者の調査からの「影響候補・範囲付き非該当・調査不能」と、KEVの「掲載・非掲載・取得不能」を別の入力として扱い、調査不能なら再調査の担当者・期限、必要に応じた暫定対応を決めるのは本PJの設計判断です。依存が原因ならGOV-001の調査結果を使います。未確認を低優先度へ自動変換せず、最高優先度へも自動固定しません。

## REF-GITLEAKS-HOOKS-001

### 役割・利用先・参照版

[Git・Gitleaks代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)の製品仕様と取得物の記録です。
2026-09-23にGitleaks公式release API、v8.30.1のREADME・source、Git公式文書を確認しました。

- Gitleaks `v8.30.1`、release公開日時 `2026-03-21T02:17:58Z`。[同tagのLICENSE](https://github.com/gitleaks/gitleaks/blob/v8.30.1/LICENSE)はMIT License。Binaryやsourceを本repositoryへ収録せず、利用者が取得・照合する手順だけを示す。
- Linux x64 archive `gitleaks_8.30.1_linux_x64.tar.gz`：release assetのSHA-256 `551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb`と取得物が一致。
- archive内の`gitleaks` binary：本PJで計算したSHA-256 `88f91962aa2f93ac6ab281d553b9e125f5197bbbce38f9f2437f7299c32e5509`。実行結果は`8.30.1`。
- Gitleaks公式：[v8.30.1 release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1)、[README](https://github.com/gitleaks/gitleaks/blob/v8.30.1/README.md)、[`stdin`実装](https://github.com/gitleaks/gitleaks/blob/v8.30.1/cmd/stdin.go)、[共通設定とtimeout・redact](https://github.com/gitleaks/gitleaks/blob/v8.30.1/cmd/root.go)、[file input処理](https://github.com/gitleaks/gitleaks/blob/v8.30.1/sources/file.go)、[組込み設定](https://github.com/gitleaks/gitleaks/blob/v8.30.1/config/gitleaks.toml)。
- Git公式：[githooks](https://git-scm.com/docs/githooks)、[git-receive-packのquarantine](https://git-scm.com/docs/git-receive-pack#_quarantine_environment)、[git cat-file](https://git-scm.com/docs/git-cat-file)、[git rev-list](https://git-scm.com/docs/git-rev-list)。

### 採否と限界

- 採用：固定binary、固定した組込みrule、`stdin`、完全redaction、JSON report、timeout、検出専用exit code。候補repositoryの設定・ignore・allow commentを受け入れない。
- 変更して採用：Gitleaks自身にGit履歴範囲を求めさせず、管理側adapterがGit object graphを列挙して内容を渡す。これによりローカルと受信側で同じ検査処理を使い、候補内の設定変更から分離する。
- 不採用：hook実行時のdownload、mutable tag、Docker必須化、候補repositoryの`.gitleaks.toml`・`.gitleaksignore`、無期限baseline、検出値を含むverbose出力。
- 限界：GitHub release assetのdigest照合は独立したpublisher署名ではない。組込みルールとallowlist、stdinのpath文脈欠落、scannerの解析・MIME識別、分割処理に由来する検出限界が残る。代表実装は未知形式を安全とせず拒否するが、全秘密情報の検出を保証しない。Gitleaks文書とrelease URLは可変であり、更新時は再確認する。

<a id="ref-iac-change-boundary-001"></a>

## REF-IAC-CHANGE-BOUNDARY-001

### 役割・利用先・参照時点

[PSB-IAC-001](../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md)、
[ENG-CONTAINER-007](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)と教材の設計入力です。
Terraform／OPAの公開仕様と、旧成果物を作る際のユーザー提供guidanceを区別します。公開URLは可変で固定digestを記録していないため、implementationを選ぶ時点で再確認が必要です。

- HashiCorp Terraform [plan command](https://developer.hashicorp.com/terraform/cli/commands/plan)、[CLI workflow](https://developer.hashicorp.com/terraform/cli/run)、[show command](https://developer.hashicorp.com/terraform/cli/commands/show)、[JSON output format](https://developer.hashicorp.com/terraform/internals/json-format)。2026-09-25に確認。Speculative planと保存plan、保存planをapplyする経路、create／update／delete／replace、unknown・sensitive表現、JSON format versionを確認。
- HashiCorp Terraform [apply command](https://developer.hashicorp.com/terraform/cli/commands/apply)。2026-09-29に現行公開のv1.16.x文書を確認。保存planを指定すると追加の対話承認なしで実行し、途中失敗時には変更済みresourceを自動rollbackしない。承認記録をplanへ結ぶ条件と、実行後のprovider状態を確認する条件の根拠に使用。
- HashiCorp Terraform [dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock)。2026-09-25に確認。Lock fileは現在provider dependencyだけを追跡し、remote moduleのversion selectionは記録しない。Provider checksumはtrust on first use等の限界を持つ。
- HashiCorp Terraform [refresh command](https://developer.hashicorp.com/terraform/cli/commands/refresh)、[refresh-only](https://developer.hashicorp.com/terraform/tutorials/state/refresh)、[resource drift](https://developer.hashicorp.com/terraform/tutorials/state/resource-drift)、[import](https://developer.hashicorp.com/terraform/cli/import)。2026-09-25に確認。`refresh`はdeprecatedで、review可能な`-refresh-only`が推奨される。Terraform stateへの取込みとprovider全体のresource inventoryを同じ成果にしない。
- Open Policy Agent [Terraform integration](https://www.openpolicyagent.org/docs/terraform)。2026-09-25に確認。Terraform plan JSONをpolicy inputにできる一方、unknown value、dynamic block、function evaluation等、plan時点で得られない情報がある。同tutorialの例はTerraform 0.12.6を前提とし、latestで未テストと明記されているため、現行implementationのversion根拠には使わない。
- 旧ユーザー提供資料：[IaC・CI・Policy as CodeによるGolden Path](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/docs/user-supplied-golden-path-guideline-ja.md)。提供日`2026-07-28`、提供元`repository user`、区分`user-supplied guidance`。外部標準、正式な組織policy、独立検証済み資料ではない。
- 旧成果物：[README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/README.md)、[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/control.yaml)、[verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/scripts/verify.py)。旧12項目、fixture、mappingの採否は移行記録に保持する。

### 採用・変更・不採用

- 採用：安全な既定値と狭いinterfaceを持つGolden Path、sourceよりresolved planを評価すること、保存planをapplyへ渡すこと、planのunknown・sensitive data、provider上の現在状態との照合。
- 変更して採用：Golden Pathを合格条件ではなく使いやすい入口とする。Module／provider／policy／targetをchange identityへ含め、plan decisionを保存plan・apply・receiptへ結ぶ。Provider hookは実coverageだけを記録し、driftは管理resourceと未管理resource、collection healthを分ける。
- 不採用：AWS／GCP／Azureの共通fieldを一つのJSON contractで自己申告すること、固定15分・24時間等を普遍要件にすること、reusable workflowへ他controlの`implemented`一覧を複製すること、provider側の全経路強制を文字列で宣言すること、破壊的修正をgeneric scriptへ許すこと。

### Mappingと限界

旧OpenSSF OSPS `OSPS-QA-03.01`・`OSPS-QA-04.02`・`OSPS-AC-04.01`、NIST SSDF `PW.6.1`、GitHub Secure Buildsは、IaC plan・apply・provider状態への直接要件ではないため継承しない。詳細は[旧framework mapping](../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#iac-change-boundary-migration--旧framework-mapping)に記録する。

Terraform資料はTerraform固有の挙動であり、OpenTofu、CloudFormation、Pulumi、managed IaC platformへ自動適用しません。OPA資料もpolicy engine一般の完全性や、個々のprovider schema・resource security ruleを定義しません。本移行では実plan、cloud apply、provider guardrail、inventory、drift、remediationを実行していません。
参照したWeb文書の再利用licenseは個別に確認しておらず、本repositoryには原文を収録せず要約とlinkだけを置きます。ユーザー提供資料のlicenseも未指定です。
