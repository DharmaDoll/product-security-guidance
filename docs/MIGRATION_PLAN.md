# 進め方と移行計画

## 移行の方針

本PJを執筆・移行作業の正本とし、旧product-security-controlsから必要な知識を主題ごとに選別・再編集します。
旧パッケージを保つための空ディレクトリや転送READMEは作りません。独立化の範囲は[Repository cutover](MIGRATION_PORTFOLIO.md#repository-cutover)に記録しています。

主な成果は、何をすべきか、本質をどこで強制すべきか、何を保証しないかを読者が判断できる知識基盤です。
実装、テスト、導入証拠は、この判断を具体化できる場合だけ別の成果物として作ります。

## 現在地と次の作業

2026-10-04更新。この節を現在地と次作業の正本とし、候補一覧は棚卸し、構造レビューと移行台帳は経緯・判断の記録として使います。

| 状態 | 内容 |
|---|---|
| 現在地 | 48件のcontrol記録・48件の設計パターン。Framework mappingは92件。92件を`design-reviewed`とし、旧関係の再レビュー待ちは0件。実環境での導入・強制を意味しない |
| 開発端末上の認証情報 | SOURCE-007で実際の値の保管・利用時の受け渡し・平文の残存を整理した。SOURCE-001の端末状態、SOURCE-004のソース管理側の権限、SOURCE-002の公開前検査と分けた。製品別の導入と実端末の状態は未確認 |
| AI領域の対象確認 | AI-001〜004・007のcontrol・教材・pattern・機械可読記録は開発用agentとその環境に絞られている。製品AIのmodel・RAG・推論gateway・TEVVは含めない。AI-004の人による重要操作承認の文言をREADMEと機械可読記録で一致させた |
| SOURCE-004のASI03関係 | 開発用agentからソース管理へ接続する場合に限り、認証情報の範囲・自動処理用ID・受け渡し・失効に関する4特性を`mitigates/medium`の部分的な設計関係として残した。Agent全体の権限や実際の拒否は未確認 |
| SOURCE-004のASI03具体化判断 | 最後の旧関係を公式資料の本文と現行特性へ照合し、対応表・資料記録・移行台帳で完了とする。実装例とテストコードは増やさない。公式PDF本体のhash、実環境の権限・失効・拒否は未確認 |
| AI-004のOWASP関係 | ASI02〜05の4件を、開発用agentの正規toolの誤用、継承権限、実行時の拡張読込み、意図しないcode実行へ限定した設計関係に変更。旧ASI04の`detects`は採用せず、4件とも`mitigates/medium`とした。実際の強制は未確認 |
| AI-004のOWASP具体化判断 | 公式資料の本文と開発用agentの特性を照合し、対応表・資料記録・移行台帳で完了とする。実装例とテストコードは増やさない。公式PDF本体のhash、製品ごとのtool・権限・code実行の拒否は未確認 |
| AI-004のATLAS関係 | tool呼出し、書込みtoolによる漏えい、toolからの認証情報取得の3件を限定して残した。監査だけの旧検知・支援関係と、攻撃分類を取り違えた環境回避の旧関係は外した。実際の拒否・検知は未確認 |
| AI-004のATLAS具体化判断 | 固定版のSHA-256と攻撃本文を現行特性へ照合し、対応表・資料記録・移行台帳で完了とする。実装例・テストコードは増やさない。実toolの権限、送信内容、認証情報への到達と監査の観測は導入先で確認する |
| AI-004のAISVS関係 | C9.2.1、C9.3.1、C9.5.1、C10.1.2の4件を開発用agentの実行時設計へ絞って残した。暗号学的に結び付けた承認を求めるC9.2.8の旧関係は外した。実際の隔離・承認・拒否は未確認 |
| AI-004のAISVS具体化判断 | 固定版の要件本文、現行control特性、設計patternを照合し、対応表・資料記録・移行台帳で完了とする。実装例とテストコードは増やさない。暗号学的承認方式と製品ごとの実行時強制は導入先の判断へ残す |
| AI-002のframework関係 | ATLASのagent tool供給経路、OWASP ASI04の開発用拡張、AISVSのMCP取得元・許可リストに限る4件を部分的な設計関係として残した。導入後のtool汚染をAI-002で防ぐ旧ATLAS関係は外した。実際の導入・失効・拒否は未確認 |
| AI-002の具体化判断 | 旧5関係の採否と対応特性を固定版の資料本文へ照合し、対応表・資料記録・移行台帳・controlからの案内で完了とする。実装例とテストコードは増やさない。採用後の変化と実行時の強制はAI-004の別判断と導入先の確認に渡す |
| CICD-005のframework関係 | GitHubのSecure use・PRイベント資料は未信頼コード、別runの成果物、runner資産への経路へ限定。Actions設定はforkと既定token権限のみ。OSPS BR-01.03は特権credential・資産への到達防止に限定。Runner侵害の概説は対応表から外し、脅威の説明として残した。実際のfork設定・権限・拒否は未確認 |
| CICD-005の具体化判断 | 今回は旧5関係の採否、対応する特性、根拠と限界を記録する。対象を絞った対応表、資料記録、移行台帳、controlからの案内で完了とし、実装例・テストコードは増やさない。実際の境界は採用先の設定とrunで確認する |
| CICD-006のframework関係 | GitHubのOIDC参照は受け入れ先の`audience`・`subject`条件とtoken取得権限、OSPS AC-04.02はjobの最小権限へ限定した設計関係。OIDC概説とATT&CK T1552.001の旧関係は非継承。実際の交換・拒否・旧鍵停止は未確認 |
| CICD-006の具体化判断 | 今回必要なのは旧4関係の採否、対応する特性、根拠と限界の記録。対象を絞った現行mapping、資料記録、移行台帳、controlからの案内で完了とする。実装例とテストコードは増やさない。実際の権限交換・拒否・旧鍵停止は導入先が決まってから確認する |
| CICD-009のframework関係 | SITF T-C007の共有cache汚染経路とOSPS BR-01.03の未信頼codeから特権CI/CD資産への経路へ限定した部分的な設計関係。旧GitHub Secure useのcache固有ではない説明は非継承し、GitHubの保存範囲・`cache-mode`は直接の製品仕様記録へ分けた。実cacheの拒否・復元・内容照合は未確認 |
| CICD-007のframework関係 | GitHub Secure useのrunner group・JIT・host境界、OSPS BR-01.03の特権CI/CD資産へのアクセス防止、ATT&CK T1552.005のmetadata credential取得経路へ限定した部分的な設計関係。旧GitHub侵害時解説、SSDF PW.6.1、ATT&CK T1133は非継承。実runnerの破棄・ログ配送・到達拒否は未確認 |
| BUILD-001のframework関係 | SLSA Build L3の隔離・署名secret分離とOSPS BR-01.03の特権資産へのアクセス防止へ限定した部分的な設計関係。旧SSDF PW.6.1は非継承。実隔離・拒否、SLSA level・OSPS適合は未確認 |
| REL-001のframework関係 | SLSA v1.2の利用者側の来歴認証とBuild Provenance項目だけを部分的な設計関係として保持。旧SSDF PS.2.1とOSPS BR-06.01は作り手側の提供・署名要件として非継承。実暗号検証・使用拒否は未確認 |
| GOV-002のframework関係 | SSDF PW.1.2は承認済み例外の理由・リスク対応の記録と見直しに限る部分的な設計関係。旧SSDF RV.2.1とOSPS QA-03.01は非継承。実gateと主ブランチの受入は未確認 |
| GOV-001のframework関係 | SSDF RV.1.1は報告後の影響調査、RV.2.1は対応計画に必要な製品適用性の情報へ限定した部分的な設計関係。旧ATT&CK T1195.001の`detects`は非継承。実inventory・deploymentの網羅性、リスク対応は未確認 |
| DETECT-001のframework関係 | NIST SP 800-190 §4.1.1はイメージ検査結果の対象・範囲・完了状態に限る部分的な設計関係。旧SSDF RV.1.1・PW.4.1、OSPS VM-06.02、NIST SP 800-190 §4.4.1は非継承。実scanner・CI拒否は未確認 |
| DEPS-004のframework関係 | OSPS VM-05.03は変更依存の既知脆弱性gate、NIST SSDF PW.4.1は第三者部品の採用レビューへ限定した部分的な設計関係。旧OSPS VM-05.01・05.02とATT&CK T1195.001は非継承。実GitHubでの拒否は未確認 |
| DEPS-003のframework関係 | ATT&CK T1195.001はレビュー後の再解決・取得物差し替え、NIST SSDF PW.4.4は取得物の完全性確認に絞った部分的な設計関係。旧PW.4.1とOSPS BR-05.01は非継承。実際のbuildでの拒否は未確認 |
| DEPS-002のframework関係 | ATT&CK T1195.001は準備時実行経路への部分的な設計関係として再記録。NIST SSDF PW.4.1の旧関係は、実行制御だけでは部品の取得・評価・維持へ直接対応しないため非継承。実環境の拒否は未確認 |
| DEPS-001のframework関係 | ATT&CK T1195.001とNIST SSDF PW.4.1の本文・control特性を再照合し、公開直後の依存版採用と第三者部品の採用判断に限る部分的な設計関係として2件を記録。実際の依存解決や組織導入は未確認 |
| Codex CLI hardening観点の確認範囲 | 利用者提供の固定版と2026-10-01時点の公式設定資料を照合。AI-004の教材・隔離設計・参照資料へ製品固有の問いを追加。設定・実装・テストコードは増やさず、実効権限や通信経路のlive確認は未実施 |
| 直近の成果 | AI領域の対象を再確認し、SOURCE-004のASI03関係をソース管理の認証情報へ限定して見直した。[構造レビュー](MIGRATION_PORTFOLIO.md#structure-review--2026-10-04ai領域の対象とsource-004のasi03関係)と[移行台帳](MIGRATION.md#2026-10-04source-004のasi03関係とai領域の範囲を確認)に判断を記録 |
| 次の主題 | 11 domainの[棚卸し](MIGRATION_PORTFOLIO.md#migration-candidates)と[横断分析](ANALYSIS_LENSES.md)を照合し、未移行領域と次に扱う具体的な失敗経路を選ぶ。対応表の件数を増やすこと自体を目的にしない |
| REL-003限定実装の再確認 | CycloneDX binding例を使い捨てrepositoryへcopyし、正常`0`、artifact不一致`1`、入力欠落`2`、copyの解除を確認。Python 3.13.5で既存9テスト通過。導入先`tools`・`tools/sbom`がsymlinkならcopyを止め、手元の試行を解除する手順をREADMEへ追加。SBOMの生成地点・coverage・storage・analysis・deploymentはこの実装で未確認 |
| SOURCE-002実装例の再確認 | Python版を使い捨てGitへ導入し、正常commit、無効canary拒否、検査器欠落による停止、解除を観測。NULや5 MiB超をfindingと区別して`ERROR/2`へ修正し、READMEのsmokeに検査不能入力を追加。8件のローカルテストは通過。Gitleaks版は導入・解除手順を読んだが、手元binaryのhashが固定配布物と異なり実Gitleaks試験は行っていない。両方式の実環境導入は未確認 |
| 開発者からの読者導線 | Engineering索引の47 patternを点検。各patternからcontrolへ進め、46 controlの教材はcontrol配下へ辿れる。GOV-004はcontrol本文にシナリオがあり、教材の数合わせはしない。参照資料への直接リンクが欠けていたSOURCE-003 patternを補修。索引冒頭へ読む順序と実装例あり・なしの例を移し、Object access boundaryの主domain表示をSecure Designへ合わせた。実装の動作・組織導入は未確認 |
| 依存採用→使用許可の読者導線 | DEPS-004・001・003・002→BUILD-001・002・003→REL-005（必要時）・002・001→CONTAINER-001（container時）をcontrol一覧から辿れるようにした。BUILD-003→REL-002とREL-001→CONTAINER-001の直接リンクも追加。関係するcontrolの境界と教材・patternへの導線を確認したが、実環境の強制・証拠の受け渡しは未確認。実装・mapping・テストコードは追加していない |
| Framework mappingレビューの確認範囲 | 2026-10-01の横断レビュー時点では118関係のうち50件が`design-reviewed`、68件が再レビュー待ち。14件の旧`verifies/high`全てに限界があることを確認。後続のDEPS-001二件は別途本文を再照合した。いずれも組織導入を意味しない |
| 成果物間mappingレビューの確認範囲 | `pilot.yaml`のpattern→controlと実装例→patternの関係、19件の既存実装例のscope・rationaleを一覧で確認。SOURCE-002の二例を追加し、資源制限例の部分的な特性対応と未実施のlive検査を明示。全実装の挙動再検証とlive導入は未確認。新しい実装・テストコードは追加していない |
| 設計pattern・実装例の横断mapping確認範囲 | 33設計patternと6実装例の関係一覧、実装例の対象・制限、前段入力の関係を照合。入力だけを受ける12関係を修正し、復旧から前段の実行系へ戻す引き渡しは保持。全pattern本文の詳細検証とlive導入は未確認。新しい実装・テストコードは追加していない |
| 横断mappingレビューの確認範囲 | `analysis-lenses.yaml`の86成果物・47 controlの配置と参照資料IDを構造的に確認。controlが明示した主レイヤー・直接段階・引き渡し段階のmappingとの食い違いを0件にした。設計pattern・実装例を含む全関係の意味的妥当性と実環境の導入は未確認。新しい実装・テストコードは追加していない |
| 横断分析・入口レビューの確認範囲 | README、control・engineering索引、七レイヤー・十二段階の本文と主題別追記を確認。古い「次の主題」表記とAIスコープの説明を補修。Mapping全件の意味的照合、実環境での導入・強制・復旧は未確認。新しい実装・テストコードは追加していない |
| 稼働観測→復旧完了の確認範囲 | GOV-001・005、CONTAINER-001・004の境界を照合。GOV-005のcontrol・機械可読記録・教材・pattern、資料と移行記録を補修。検知アラート不在やrollout成功を旧digest非稼働と扱わない。Live inventory・再投入拒否・復旧は未確認。新しい実装・テストコードは追加していない |
| Release→使用許可の横断レビューの確認範囲 | REL-001・002・003・005、CONTAINER-001・002、GOV-005と既存設計・教材の責任を照合。分野の入口とadmission patternのみ補修。実registry、admission、runtimeの観測・旧digest非稼働は未確認。新しい実装・テストコードは追加していない |
| CI/CD→Release横断レビューの確認範囲 | CIのPR・権限境界、BUILD-002・003、Release Integrity五controlと設計の入口を照合。文書のみ補修。署名・来歴・SBOMの実公開、利用者側検証、使用拒否は未確認。新しい実装・テストコードは追加していない |
| CICD-006診断項目の確認範囲 | 既存control・教材・pattern・GitHub/AWS例と公式のOIDC claim・trust条件を照合。文書と診断項目で完了し、新規実装・テストコードは追加していない。実trust、交換拒否、role操作、旧key・sessionは未確認 |
| CI/CD Security横断レビューの確認範囲 | 七つのcontrolの入口、PR境界のcontrol・pattern・既存GitHub例、公式のbranch保護・rulesetを照合。文書とmarkerのみ補修し、実GitHubでの直接push・bypass・review・権限配送は未確認。新規実装・テストコードは追加していない |
| Source Protection横断レビューの確認範囲 | 六つのcontrol・教材・設計の入口、engineering索引、横断分析のSOURCE-002・003の状態表記を照合。文書とマッピングを補修し、新しいcontrol・実装・テストコードは追加していない。実環境への導入・利用者による読書評価は未確認 |
| SOURCE-002・003の確認範囲 | 既存control・教材・pattern・GitHub監視例、Gitの受信側隔離とGitHubのpush protection公開資料を照合。実GitHubの受信・検索、認証情報の失効、通知・対応は未確認。新規実装・テストコードは追加していない |
| SOURCE-005の確認範囲 | 既存control・教材・pattern・Git mirror例と七つのローカルGit試験、NIST SP 800-61 Rev.3の復旧資産確認を照合。実保管世代、変更経緯、採用時点、関連データ・設定、開発再開は未確認。新規実装・テストコードは追加していない |
| SOURCE-006の確認範囲 | 既存control・教材・pattern・GitHub手順、GitHub公式のApp申請・インストール制限、OAuthアクセス制限、organizationのPAT方針を照合。実組織の方針変更、既存token・App、拒否、通知は未確認。新規実装・テストコードは追加していない |
| SOURCE-004の確認範囲 | 既存control・教材・pattern・GitHub実装案、GitHub Enterprise Cloud公式のSAML、fine-grained PAT、認可取消・認証情報削除の可変文書を照合。実組織の設定、IdP、認証情報、既存セッション、拒否は未確認。新規実装・テストコードは追加していない |
| SOURCE-001の確認範囲 | 既存control・教材・pattern、旧Linux adapter、NIST SP 800-207最終版の§3を照合。実MDM、対象端末、資産側のセッション終了、失効の遅延は未確認。新規実装・テストコードは追加していない |
| DETECT-001の確認範囲 | 既存control・機械可読記録・教材・pattern、zizmor公式UsageのSARIF終了状態と解析失敗を照合。指摘と評価不能の同時保持を補修。現行Trivy・DockSec、実scanner、DB、実対象のcoverage、CI受入は未確認。新規実装・テストコードは追加していない |
| DETECT-003の確認範囲 | 旧Python verifierの照合・再出現判定と既存control・教材・pattern、NIST CSF 2.0公開ページ、CISA BOD 23-01の公開検索本文を照合。部分取得時の候補保持を補修。実収集API、台帳、状態保存、通知、能動的調査は未確認。新規実装・テストコードは追加していない |
| DESIGN-001の確認範囲 | OWASP Authorization Cheat SheetとASVS 5.0.0固定版V8、既存control・教材・pattern・Python／SQLite例を照合。Python 3.10.4で既存7テストを実行。HTTP認証、全endpoint、実tenant、組織導入は未確認 |
| CODE-005の確認範囲 | UTS #55固定版、Python 3.10字句規則、既存scanner・教材・patternを照合。Python 3.10.4と手元のPythonで13件の実装testを実行。Review UI、protected CI、実repositoryのmerge拒否は未確認 |
| IAC-001の確認範囲 | 利用者提供Golden Path資料、Terraformのplan・apply・dependency lock・refresh仕様、OPAのTerraform資料と文書・診断項目を照合。実IaC tool・cloud provider・保存plan・apply・driftは未実行。新規実装・テストコードは追加していない |
| CONTAINER-005〜007の確認範囲 | Kubernetes 1.37のPod Security Admission、NetworkPolicy、Pod-level resource・ResourceQuotaの公式資料と既存例を照合。Shell構文とrepository検査を実施。使い捨てclusterのadmission拒否、CNIによる到達性、quotaとruntime enforcementは未実行 |
| CONTAINER-003・004の確認範囲 | 文書・診断項目、NIST SP 800-190 §4.4.4、FalcoとSysdigの現行公開資料を照合。Live node、sensor、rule、event、配送、担当者受領、隔離・失効は未確認。新規実装・テストコードは追加していない |
| CONTAINER-001・002の確認範囲 | 文書・診断項目、OCI Image Specification v1.1.1のindex／descriptor、Kubernetesのadmission段階を照合。Live registry、consumer、admission、node／runtimeの実行内容と使用停止は未確認。文書と診断項目で完了し、新規実装・テストコードは追加していない |
| GOV-002・005の確認範囲 | 文書・診断項目、旧例外consumer関係、NIST SSDF 1.1・SP 800-61 Rev.3の公開ページ、OpenSSF Baseline 2026.02.19を照合。実例外台帳・取消・使用gate、live build・registry・admission・稼働観測は未確認。新規実装・テストコードは追加していない |
| GOV-001・003の確認範囲 | 文書と診断項目、FIRST CVSS v4.0仕様、NIST SSDF 1.1公開ページ、CISA管理のKEV配布mirrorを照合。CISA本体ページ、live feed、製品inventory、優先度方針、ケース配送、実対応は未確認。新規実装・テストコードは追加していない |
| REL-003・004の確認範囲 | 利用者提供の固定資料、CycloneDXの生成段階、Dependency-Track 4.14.3の通知順を照合。既存9テストをPython 3.13.5で実行し、READMEのコピー・正常例・上書き防止・成果物変更・入力不足を確認。実生成、公開、分析、供給者からの受入れは未確認。新規実装・テストコードは追加していない |
| REL-001・002・005の確認範囲 | 文書、SLSA v1.2の検証・配布、Sigstoreの公式署名・検証仕様を照合。実signer、公開・取得、検証器と使用拒否は未確認。文書と診断項目で完了とし、実装例の不在は残作業にしない |
| BUILD-001〜003の確認範囲 | 文書とSLSA v1.2のproducer・生成・隔離・基盤評価を照合。L3のfield例外への参照も反映。実sandbox・通信拒否・sensor配送、platform生成・認証、release拒否は未確認。文書と診断項目で完了とし、実装例の不在は残作業にしない |
| CICD-005・009・007の確認範囲 | 文書、公式のcache・runner・workflow・イベント仕様、固定checkoutのsourceを確認。既存GitHub例のYAML・shell構文、ローカルcopy・上書き防止・revision照合を確認。実GitHubのfork PR・配送権限・cache拒否・merge拒否、実runnerの割当・隔離・世代別破棄・ログ配送は未確認。対象・版・権限・保存先と許可された確認方法を選べた時に実評価へ戻る |
| DEPS-002〜004の確認範囲 | pipの既存4テスト、使い捨て環境の通常installと導入ガード、固定Actionのsource・配布コードと公式文書を確認。実GitHubのデータ準備・評価・必須検査・merge拒否、採用先の全依存・platform・CI配線は未確認。対象・版・入力と強制点を選べた時に実評価へ戻る |
| CICD-003の確認範囲 | 旧14 fileと採用workflowの固定revision一致、固定Actionのsource、公式の出力・収集・受入仕様、文書を確認。実scanner、GitHubの必須check・権限・結果公開・拒否・bypassは未確認。採用対象と確認方法を選んだ時に実評価へ戻る |
| CICD-002の確認範囲 | 文書・診断項目は完了。実GitHubでの実行・拒否、対象のshell・Action・呼出先、CI強制は未確認。実診断は対象の入力元・イベント・権限・呼出先と許可された確認方法を選んだ時に行う。実装例がないことは残作業にしない |
| CICD-004に残る作業 | YAML・固定参照・shell構文・ローカルcopyとsource確認まで検査。実GitHub設定、token付与、Environmentの承認・開始拒否・bypass、GET、実公開・交換は未確認。許可されたrepository、用途・scope・追加credential、保護branch・tag、利用可能な環境機能と担当者を選んだ時に実評価へ戻る |
| CICD-001に残る作業 | Linuxのhash付きparser導入と12件のローカルCLIは確認済み。実GitHub APIによるpinact修正、remote commitの存在・出所・release対応、固定コード内部の取得review、GitHub required check・policy・review・迂回拒否、macOSは未確認。採用repository・版・用途・保護branch・担当者を選べた時に実評価へ戻る |
| SOURCE-006に残る作業 | GitHub CLI 2.95.0の構文とAPI版2026-03-10の仕様は確認済み。Live設定・適用・拒否・API収集、IdP、監査配送、通知は未確認。必要対象、契約、取得元、読取り権限、保存先、通知先、確認期限を選べた時にcollectorや実評価を具体化する |
| SOURCE-005に残る作業 | ローカルGit復元の代表七経路は確認済み。Live GitHubの拒否、保管先・鍵・accountの独立性、保持lock、LFS・metadata・設定の復元、製品の開発再開、RPO・RTO、通知は未確認。Provider・保管先・必要データ・復元先・許可された確認方法を選べた時に限定実装・評価へ戻る |
| AI-007に残る作業 | 六件のローカルprocessテストは完了。実agent・子process方式・遠隔操作の結果、費用・token・tool呼び出しの共通予約、再開時の永続予算台帳、provider quotaは未確認。Agent・版・取得元・実行前強制点を選んだ時に限定実装へ戻る |
| 次回に残す判断 | AI-001のGitHub例は保護branch・レビュー担当・bypassの採用先が未定で、実拒否は未確認。開発agentの効果比較も未実施。AI-003の製品別実装はagent・版・toolの強制点・使い捨て対象を選んだ時に再開する。AI-005・008・009は採用する開発agentの保存・委譲・停止経路が決まるまで保留する。SOURCE-003の実GitHub検索、精査、Webhook受領、対応運用は未確認。DETECT-003の公開サービス台帳照合は、対象環境・収集元とAPI・正本台帳・許可範囲・通知先を選べた時に限定実装へ戻る。CODE-005のreview UIとprotected CI、採用先のpathと例外は未確認。BUILD-001〜003の文書範囲は完了。採用先で実効性を見込める場合だけ実装例の要否を再判断する。REL-001・002・005は採用先で導入・確認への実効性を見込める場合だけ限定実装を検討する。REL-004は文書と診断項目で完了。採用先で導入・確認に役立つ場合だけ限定実装を検討する。REL-003のlive storage・Dependency-Track・deployment catalogは未実施 |
| Secure Codingに残る作業 | ASVS 5.0.0を共通要件の参照先とする方針を記録済み。個別の要件対応は対象主題ごとに確認する。利用者の経験由来の診断チェックリストは後日受領予定で、原本と公開可否の確認前に項目・ASVS対応を作らない |
| SOURCE-002に残る作業 | 実環境への配布・有効化、全書込経路の接続、負荷評価、例外承認、他OS・SaaS構成は未実施。代表実装の完了と組織導入を区別する |
| 継続する未確認事項 | 全旧実装の意味的レビュー、参照仕様の現行性、読みやすさとcontrol・pattern間navigationの継続レビュー、実環境の導入・強制 |

各主題は、読者が問い・直接の失敗・適用範囲・セキュリティ特性・隣接境界を判断でき、
参照資料と旧項目との関係を追跡できるところまで整理します。文書の完成に加え、
[主題ごとの具体化判断](ARTIFACT_MODEL.md#主題ごとの具体化判断)で選んだ成果物を完了条件に含めます。
必要と判断した具体実装が残る主題は、文書作成済み・実装未完了として記録します。実装例を必要としない主題は、
文書と診断項目で完了にできます。実環境への導入・診断は別に扱います。
[診断で確認する項目](CONTENT_QUALITY.md#failure-checks)は、チェックリストだけでも成立し、実際に試した結果とは区別します。

Git hooksの主題は利用者の指定により先に整理し、代表実装まで追加しました。SOURCE-004の8件の追加照合は完了しました。
OWASP ASI03は開発agentのソース管理アクセスに限る部分的な設計関係として残し、公式PDF本体のhashと実環境での強制は未確認です。
その後の主題は、次回のレビュー結果、読者の需要、実装予定、攻撃経路の受け渡しの欠落から選びます。
一つのdomainを全件移してから次へ進む方式や、旧52件を一対一で移す方式にはしません。
移行先と採否は[三領域の移行状況](MIGRATION_PORTFOLIO.md#migration-candidates)と[残る八domainの棚卸し](MIGRATION_PORTFOLIO.md#portfolio-migration-review)に保持します。

## 実装例を選ぶ方針の見直し

2026-09-27、利用者の指摘を受け、「技術経路を絞れる主題では具体実装を原則として選ぶ」という方針を見直しました。
今後は[実効性の判断基準](ARTIFACT_MODEL.md#主題ごとの具体化判断)で要否を選び、実装例の追加を移行の既定路線にしません。
既存例も、読者の導入・判断・確認に役立つかをレビューします。追加・拡張する効果を説明できなければ、実装やテストを増やしません。

## SOURCE-004の読み合わせと具体化判断

2026-09-30、既存control・機械可読記録・教材・pattern・GitHub実装案を読み合わせました。今回必要な成果物は、失効対象の違いを判断できる文書と診断項目です。端末紛失や異動の通知を受けた後、認証情報、組織への認可、既存セッション、別に残る鍵・アプリ権限を列挙し、止めたい資産・操作に対して拒否を確認できることを完了条件としました。新しいコード・テストは選びません。

GitHub Enterprise Cloudの可変な公式資料では、SAML認可の取消と元のPAT・SSH鍵の削除、fine-grained PATの失効とそれで作成したSSH鍵、利用者認証情報への一括操作とGitHub Appインストール用認証情報は、それぞれ別の範囲です。[Sources](../sources/README.md#spec-github-security-guidance)に確認日・採否・限界を記録し、旧固定版のframework mappingをこの確認だけで更新しません。既存[GitHub実装案](../engineering/source-protection/source-access-credential-lifecycle/implementations/github/README.md)へ使い捨て対象での確認点を補いました。実組織のIdP、権限一覧、失効操作、既存セッション、拒否は未確認です。

## SOURCE-001の読み合わせと具体化判断

2026-09-30、既存control・機械可読記録・教材・patternと旧Linux assessmentを読み合わせました。今回必要な成果物は、端末状態の悪化を新規と継続中のアクセスへどう反映するかを判断できる文書と診断項目です。資産ごとの再評価時点、反映に要する時間、残る権限を確認し、端末管理画面の不適合表示だけを資産側の制限完了にしないことを完了条件としました。新しい実装例・テストコードは選びません。

旧Linux adapterはworkspaceのblock-device chainや一部のOS設定を実際に観測します。しかし管理基盤の状態、所有者、ソース管理側のセッションや発行済み認証情報、通知の受領を測りません。端末全体の良好状態やアクセス制限の証拠として移植するのは不適切です。[NIST SP 800-207](../sources/README.md#ref-developer-endpoint-baseline-001)の接続開始・終了の役割を設計入力にし、旧成果物との関係は[移行対応表](MIGRATION_SOURCE_PROTECTION.md#endpoint-migration)に保持します。対象端末、MDM、認証基盤、ソース管理、許容遅延を選べた時に、使い捨て端末での限定的な確認を検討します。今回は実端末・実セッションを操作していません。

旧DEH-001〜003・END-005にある開発端末上の認証情報は、[SOURCE-007](../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md)へ整理しました。利用者提供原文を確認し、`.env`などへの平文保存を避けること、必要時の取得、端末に残る長期の値を減らすことをcontrol、教材、設計パターン、診断項目へ反映しました。SOURCE-001の端末状態、SOURCE-004のソース管理側の権限・失効、SOURCE-002の公開前検査、AI-004のagent操作認可と分けています。特定製品への導入と実端末での確認は行っていません。実装例は採用先が決まり、導入・確認に役立つ場合だけ検討します。

## DETECT-001の読み合わせと具体化判断

2026-09-29、既存control・機械可読記録・教材・設計patternの状態表現を読み合わせました。今回必要な成果物は、指摘と解析失敗が同時に起きる場合を説明する文書と診断項目です。検査した範囲と得られた指摘を別に保持し、必要な範囲に解析失敗があれば全体の受入を止め、既知の指摘も調査へ残せることを完了条件としました。新しい実装例・テストコードは選びません。

[zizmorの公式Usage](../sources/README.md#spec-zizmor-workflow-analysis)は、SARIF出力時の終了コードと部分的な解析失敗が、単純な「終了コード0＝検査完了・指摘なし」と一致しない具体例です。一方、全体状態と指摘を別に保持する方式は本PJの解釈です。旧Trivy・DockSec adapterとfixtureは引き続き移植せず、製品と導入先を選んだ時にtool、検出データ、方針、対象と出力modeを再確認します。実scanner、DB、予定した全対象の解析、CI受入・拒否は未確認です。[Sources](../sources/README.md#ref-scanner-evidence-001)に採否と限界を記録しました。

## DETECT-003の読み合わせと具体化判断

2026-09-29、既存control・機械可読記録・教材・patternと旧Python verifierを読み合わせました。今回必要な成果物は、部分取得時の状態更新を明確にした文書と診断項目です。収集できた範囲の新候補は調査へ進め、取得できなかった範囲の既存候補は保持し、収集や台帳の欠落を「公開なし」や「是正済み」に変えないことを完了条件としました。新しい実装例・テストコードは選びません。

旧verifierは入力済みの観測と台帳の照合、是正済み候補の再出現を実際に判定します。一方で外部collector、管理責任、台帳の正しさ、通知の受領を観測しません。NIST CSF 2.0とCISA BOD 23-01は資産の把握と脆弱性診断を分ける設計入力であり、部分取得時の状態遷移は本PJの解釈です。[Sources](../sources/README.md#ref-external-surface-001)と[旧成果物の採否](EXTERNAL_ATTACK_SURFACE_MIGRATION.md)に根拠と限界を残します。対象環境・収集元とAPI・正本台帳・許可範囲・通知先が決まった時に限り、限定実装を再検討します。実収集、台帳更新、通知、再出現のlive観測、能動的な調査は未確認です。

## DESIGN-001の読み合わせと具体化判断

2026-09-29、必要な成果物を既存control・教材・設計・Python／SQLite例の導線と、ASVSとの限定したmappingの補修に絞りました。認証済みの主体と対象への操作許可を区別し、請求書のread／updateでowner・tenantをサーバー側の条件として確認できること、実アプリへの導入範囲を誇張しないことを完了条件としました。新しいcontrol・実装・テストコードは追加しません。

[ASVS 5.0.0の固定版V8](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x17-V8-Authorization.md)のV8.2.1は機能ごとの明示的な権限、V8.2.2は対象データごとの明示的な権限を確認します。既存controlの操作scopeとowner・tenant付きqueryはこれらを支えるため、`supports / medium / design-reviewed`の部分関係を二件だけ追加しました。V8.2.3のfield別権限、V8.3.1の信頼できるservice層、V8.4.1の全tenant操作は、この限定例から対応済みとしません。

Python／SQLite例は実queryの許可・拒否・所有者変更後の書込拒否を観測できますが、`Principal`が認証層から正しく来たこと、HTTP endpoint全体、list・export・batch・cache、並行処理を証明しません。古い`experiments/next-repository`のテストpathを現在の配置へ直し、手元の使い捨てrepositoryで試す最短手順と解除を補いました。[Sources](../sources/README.md#ref-application-authorization-001)にはASVSとの採否と限界を記録し、組織チェックリストの未提供状態は変えません。

## CODE-005の読み合わせと具体化判断

2026-09-29、既存control・機械可読記録・教材・patternとPython限定実装を読み合わせました。必要な成果物を表示と処理系の改行差の補修、既存scannerの限定的な修正、代表経路のtest、参照記録の更新に絞りました。コメント内の表示上の改行を処理系も行末とみなす誤解を解き、受入前に位置とcode pointを示せることを完了条件としました。

Python 3.10ではLF・CRLF・CRが物理行末です。UnicodeのU+000B、U+000C、U+0085、U+2028、U+2029は表示環境で改行になり得ますが、Pythonのコメントをそこで終えません。既存scannerはこの5種類を`PASS`にしていたため、`display-line-break`として拒否する限定profileへ修正しました。[UTS #55](../sources/README.md#spec-unicode-source-handling-2)と[Python字句規則](../sources/README.md#spec-python-source-lexical-3-10)に根拠と解釈を分けています。

既存例のPythonソースを読む利点があり、局所的な検出欠落の補修に実効性があるため、この限定実装は維持します。一方、全言語の改行方針やreview UIの表示、採用先CIの強制へ同じ拒否リストを拡張しません。実repositoryの対象path・例外・受入権限が未定であり、新しいCI実装は選びません。[旧成果物の扱い](UNICODE_SOURCE_MIGRATION.md)も更新しました。

## IAC-001の読み合わせと具体化判断

2026-09-29、必要な成果物を既存control・機械可読記録・教材・pattern・診断項目の補修に絞りました。Reviewしたsourceと依存、解決済みplan、実行前の承認、apply結果、provider上の現在状態を混同しないことを完了条件としました。新しい実装例やテストコードは選びません。

Terraformの[apply仕様](https://developer.hashicorp.com/terraform/cli/commands/apply)では、保存planを指定すると追加の対話承認なしに実行し、途中失敗も自動rollbackしません。そこで、保護されたapply jobが呼出し前に承認記録・plan・targetを照合し、失敗後も変更済みresourceの有無を確認する条件を戻しました。旧利用者提供資料はGolden Pathの出発点として参照し、module・CI templateの利用だけを実効的な強制や導入証拠にしません。

旧項目・旧fixtureの採否は[IaC移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#iac-change-boundary-migration)、一次資料の版・確認日・限界は[Sources](../sources/README.md#ref-iac-change-boundary-001)に残します。対象provider・resource・強制点が未選定なので、文書と診断項目で今回の判断を完了し、実cloudの受入・拒否、途中失敗、driftは未確認です。

## CONTAINER-005〜007の読み合わせと具体化判断

2026-09-29、必要な成果物を既存教材・pattern・Kubernetes限定実装の補修に絞りました。権限、通信、資源の宣言と実効状態を別に追えること、既存対象や確認不能な対象を使い捨てtestで変更しないこと、遮断を宛先停止と取り違えないことを完了条件としました。新しいcontrol・pattern・実装例・テストコードは追加しません。

CONTAINER-005のAdmissionは新規Pod等の受付を扱い、既存Podのruntime状態を自動で修正しません。CONTAINER-006のNetworkPolicyはpluginの強制が必要であり、拒否probeはsourceのexecとdestinationのlocal listenerを確認してから判断します。CONTAINER-007の例はcontainer単位のCPU・memory・ephemeral-storage予算を選んだtest profileです。Kubernetes 1.37のPod-level CPU・memory予算だけを指定したPodも有効ですが、この例のCELでは拒否するため、共通controlの要件と混同しないようにしました。

三つの`verify.sh`は、名前が衝突する対象だけでなく、API errorで有無を確認できない場合も変更前に停止します。Kubernetes資料の確認日と採否は[Sources](../sources/README.md#ref-workload-confinement-001)、[Network](../sources/README.md#ref-workload-network-segmentation-001)、[Resource](../sources/README.md#ref-workload-resource-bounds-001)へ、旧成果物の扱いは[移行台帳](MIGRATION.md)へ記録しました。Live clusterがなく、Pod Security Admission・CELの実拒否、CNIの強制、quota・cgroup・pressureは未確認です。

## CONTAINER-003・004の読み合わせと具体化判断

2026-09-28、必要な成果物を既存control・機械可読記録・教材・設計の補修、CONTAINER-004の診断項目、NIST 4.4.4 mappingの再評価に絞りました。Node管理面がsensorの信頼へ影響すること、eventの対象と稼働artifactの照合、観測障害と検知なし、検知と破壊的対応を別に判断できることを完了条件とし、この文書範囲を完了しました。新しいcontrol・教材ファイル・pattern・実装・テストコードは追加しません。

CONTAINER-004の旧機械可読記録にあった署名付き試験event、全dropゼロ、event内の完全なdigestを共通要件とする表現を本文へ揃えました。対象IDが欠けるeventも調査へ残し、対象未確定のまま停止対象を選びません。Host侵害が疑われる場合はnode上sensorの「異常なし」だけを信じず、CONTAINER-003の隔離・credential失効へ渡します。Artifactの置換が必要な場合に限りGOV-005へ旧・新digestと稼働範囲を渡します。

[NIST SP 800-190 §4.4.4](../sources/README.md#spec-nist-sp-800-190--container-security-guidance)はprocess・保護file・network異常とcontainer-awareな検知の部分根拠に限定し、旧10特性の`detects / high`関係を4特性の`supports / medium / design-reviewed`へ縮小しました。FalcoとSysdigの確認済み公開資料、旧URLの取得限界、製品ごとの差を[Sources](../sources/README.md#ref-container-003)に記録しています。Live sensor・通知・対応の効果は未確認です。採用先と導入・確認の実効性が定まるまで、実装例は選びません。

## CONTAINER-001・002の読み合わせと具体化判断

2026-09-28、必要な成果物を既存control・機械可読記録・設計の補修、両control配下の教材、診断項目に絞りました。OCI image indexを公開したとき、実行先が選ぶmanifestとの対応を追えること、registryでの公開・保持・lifecycle状態を使用許可と混同しないこと、旧digestの非稼働確認をGOV-005へ渡せることを完了条件とし、この文書範囲を完了しました。新しいcontrol・pattern・実装・テストコードは追加しません。

`deprecated`は一律の拒否状態にせず、対象と期限を決めて使用可否を判断します。使用停止を決めた`quarantined`等は取得可能でもadmission側の拒否に反映します。Indexと選択manifestは異なるdigestを持つため、runtime報告値も含めて採用先で対応関係を確認します。[Sources](../sources/README.md#ref-container-registry-publication-001)へOCI v1.1.1と本PJの解釈を区別して記録しました。旧実装の採否は[registry移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#container-registry-migration)と[admission移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#deployment-artifact-admission-migration)に保持します。

Provider、対象cluster、consumer policy、runtimeの観測方法が未定であり、合成JSONやgeneric adapterは実効性を示しません。文書・診断項目で今回の判断を支えられるため実装例は選びません。Live registryの権限・監査・状態通知、実admissionの拒否、cacheやreplica、稼働中のmanifestと旧digestの非稼働は未確認です。採用先で導入・確認に役立つ場合だけ限定実装を再検討します。

## GOV-002・005の読み合わせと具体化判断

2026-09-28、必要な成果物をGOV-002のcontrol・機械可読記録・既存教材・設計の補修と診断項目、GOV-005のcontrol・機械可読記録・設計の補修とcontrol配下の教材、例外consumer mappingの追加に絞りました。GOV-003の元の優先度・対応期限、GOV-002が承認する一時使用、GOV-005が確認する旧digestの非稼働を別に辿れることを完了条件とし、この文書範囲は完了しました。新しいcontrol・pattern・実装・テストコードは追加しません。

GOV-002の本文が方式を固定しないのに、旧YAML形式・固定SHA-256・旧versionを一律に要求していた機械可読記録を修正しました。GOV-003とGOV-005が例外を直接使う境界を[マッピング](../mappings/exception-consumers.yaml)へ追加しました。GOV-005では新digestの受入・配布と旧digestの非稼働を別に確認し、例外が有効でも復旧ケースを閉じません。切り戻しで旧digestを再投入できる経路も判断対象に残します。

NIST SSDF 1.1、SP 800-61 Rev.3、OpenSSF Baseline 2026.02.19の公開ページを再確認し、共通形式や状態名は本PJの設計判断として[Sources](../sources/README.md#ref-security-exception-lifecycle-001)へ区別して記録しました。文書と診断項目で今回の判断を支えられるため、実装例は選びません。実例外台帳・取消・使用gate、live build・registry・admission・稼働観測は未確認です。旧成果物とmappingの関係は[移行台帳](MIGRATION.md)と[Recovery移行記録](MIGRATION_GOVERNANCE_OPERATIONS.md#deployed-artifact-recovery-migration)に保持します。

## GOV-001・003の読み合わせと具体化判断

2026-09-28、必要な成果物をGOV-001のcontrol・教材・設計と診断項目、GOV-003のcontrol・設計と診断項目の補修、GOV-003配下の教材に絞りました。検索0件から影響候補・範囲付き非該当・調査不能を区別し、対象・時点・根拠・不足情報を次の判断へ渡せることを完了条件とし、この文書範囲は完了しました。新しいcontrol・pattern・実装・テストコードは追加しません。

GOV-001ではソースSBOMの収集範囲と完成物、SBOM取込と分析完了、検索権限・全page、成果物digestと稼働先を確認します。GOV-003では影響調査の状態と既知悪用情報の状態を別々に保持し、調査不能な対象に再調査の担当者・期限、必要なら暫定的な保護策を置きます。低優先度にも最高優先度にも自動固定せず、組織方針と見直し条件を記録します。[Sources](../sources/README.md#ref-vulnerability-priority-001)に一次資料の確認範囲と本PJの解釈を分けました。

既存の合成verifierを移植せず、組織の実データや判断経路を自己申告の成功へ変換しません。実製品の収集範囲、分析完了、live KEV取得、組織の優先度方針、ケース配送と実対応は未確認です。製品・データ源・責任者・確認方法が定まり、導入・確認への実効性がある場合だけ限定実装を検討します。旧項目と部分mappingは[移行記録](MIGRATION_GOVERNANCE_OPERATIONS.md#vulnerability-priority-migration)と[GOV-001の台帳](MIGRATION.md#gov-001追加移行2026-09-17)に保持します。

## REL-003・004の読み合わせと具体化判断

2026-09-28、必要な成果物を既存control・教材・設計の補修と、REL-003限定実装の導入手順の明確化に絞りました。取得地点と実際の収集範囲、成果物への対応、供給者からの受入れ、取込と分析の状態を区別し、隣接する判断へ辿れることを完了条件とし、この範囲は完了しました。新しいcontrol・pattern・実装・テストコードは追加しません。

利用者提供資料の固定原文を読み直し、共通base imageのSBOMと最終製品の一覧の違いも補いました。既存スクリプトの成功はphaseの申告とhashなどの照合であり、完成物を実際に調べた証明とは分けます。Dependency-Track 4.14.3のソースに従い、取込完了通知を後続の脆弱性分析完了へ変換しない設計にしました。一次資料と解釈の区別は[Sources](../sources/README.md#ref-release-sbom-lifecycle-001)に記録しました。

既存9テストはPython 3.13.5で成功しました。READMEのコピー手順、正常例、上書き防止と配置先の制限、成果物変更・入力不足も使い捨てrepositoryで確認しています。実際のSBOM生成・収集範囲、公開・取得、分析完了、稼働先、供給者の認証・受入れは未確認です。追加実装は採用先で導入・確認への実効性を見込める場合だけ選びます。旧項目との対応は[Release SBOM](MIGRATION_RELEASE.md#release-sbom-migration)と[Supplier SBOM](MIGRATION_RELEASE.md#supplier-sbom-migration)の移行記録に保持します。

## REL-001・002・005の読み合わせと具体化判断

2026-09-28、必要な成果物を既存control・教材・設計の補修と、REL-001の診断項目に絞りました。成果物署名、来歴の認証、配布、利用者の受入条件を区別し、検証した内容を使用時まで維持する判断ができることを完了条件とし、この文書範囲は完了しました。新しいcontrol・教材ファイル・pattern・実装・テストコードは追加しません。

REL-001の機械可読記録を本文の期待値照合と使用停止へ揃え、来歴の種類の確認も明記しました。REL-002はWindows版の利用者が来歴を取得できない場面から教材を読み直し、準備中という表示だけでは使用を止められない点を設計へ戻しました。REL-005は対象照合を外した署名成功を受入成功としない条件を補っています。一次資料の版・確認範囲はSourcesの各主題へ記録しました。

旧合成recordや暗号検査の一括移植は行いません。採用する形式、検証器・signer、信頼根拠、配布先、実際の使用経路と許可された確認方法が決まり、導入・確認に役立つ場合だけ限定実装を検討します。実環境の署名・公開・取得・上書き拒否・使用停止は未確認です。

## BUILD-001〜003の読み合わせと具体化判断

2026-09-28、必要な成果物を三つのcontrol・設計の補修、BUILD-001の診断項目、既存教材の補修とBUILD-003配下の教材に絞りました。実行中の権限、承認した手順、来歴情報を作る主体を別に判断でき、前後のcontrolへ戻れることを完了条件とし、この文書範囲は完了しました。新しいcontrol・pattern・実装・テストコードは追加しません。

BUILD-001の機械可読記録を本文の通信強制、観測の健全性、公開への昇格停止へ揃えました。BUILD-003では署名済みでもジョブの申告を基盤が観測した事実と扱わず、正確に記録された入力も公開承認とは分けます。SLSA v1.2の公式資料で、L3の生成・検証要件にもtenant由来fieldの例外への参照があることを確認し、例外なしと読める説明を補修しました。直接の仕様根拠と本PJでの設計解釈は[Sources](../sources/README.md#spec-platform-provenance-generation)へ記録しています。

旧JSON計画検査、合成recordとlocal署名の検証は、実行権限の強制や基盤による来歴生成を確認しないため移植しません。実装例の不在は残作業にしません。実行基盤、対象成果物、情報取得元、認証方式、公開を止める仕組み、許可された確認方法が決まり、導入・確認に役立つ場合だけ限定実装を検討します。実環境の隔離・観測・生成・認証・拒否は未確認です。

## CICD-005・009・007の読み合わせと具体化判断

2026-09-27、必要な成果物を三つのcontrolの診断項目、既存教材・設計の補修と、既存GitHub例の導入・確認・解除に絞りました。PR由来の内容の受渡し、外部cacheの保存・取得、同じhostに残る状態と実体の破棄を分け、後続の権限処理へ届く経路を選んで確認できることを完了条件としています。この文書範囲は完了しました。Provider未選定のcache client・runner provisioner・合成判定器は追加しません。

機械可読記録に残ったprotected mainだけの保存、pipのwheel-only install、一律JIT登録、providerイベントだけによる破棄証明を、本文の共通特性へ揃えました。具体的なGitHub条件は設計・資料記録へ残し、旧check IDとframework関係は維持します。Cache不使用を選んだ既存PR分離例では、`cache-mode: none`を明示し、mainへのpushから始めるrunへpush SHAのcheckoutとHEAD照合を加えました。この照合は取得したrevisionの一致だけを示し、review済みの証拠にはならないため、2026-09-30の横断レビューで直接push・bypassの確認を補いました。

ローカルでは導入copy、既存二file・入力不足・repository内の非root指定時の開始拒否、YAML・shell構文と実Gitのrevision一致・不一致を確認しました。Revisionの期待値の空欄・欠落とGit repository不在も拒否されました。PyYAML 6.0.2は検査環境の観測版です。GitHub.comの現行仕様と固定checkout sourceの読解を、実token・cache拒否・必須判定・merge拒否の成功へ変換しません。Hosted runnerの契約、組織runnerの隔離・破棄・外部ログ、復元cacheの全内容は採用先の実評価へ残します。

## DEPS-002〜004の読み合わせと具体化判断

2026-09-27、必要な成果物を三つのcontrolの診断項目、既存教材・設計の補修と、既存pip・GitHub例の導入手順に絞りました。更新を採用する判断、承認した内容の照合、準備用コードの実行許可を分け、通常buildへ何を渡すか選べることを完了条件とし、この文書範囲は完了しました。新しいwrapper・scanner・実装例は追加しません。

pip例には新しい専用環境での最短手順と解除を示しました。取得ファイルのhash照合と既存の展開済み状態を分け、manifestとの対応・全推移依存まで確認する例とは扱いません。固定Dependency Review Actionではsnapshot警告の待機期限後も判定を続けることをsourceと配布コードで確認し、成功表示から全対象を評価済みと推論する説明を直しました。未評価を止める必須判断の接続は採用先で選びます。

既存のpip 4テストはPython 3.10.4 / pip 23.3.1で確認しました。使い捨てvenvでは、無害なwheelの通常install、既存環境を拒否する導入ガードと、既に入っている依存のhashを再確認しない経路をpip 22.0.4で観測しました。これらは観測版であり推奨版ではありません。公式pip文書の表示版26.2.1、npm ci v11、uvのlock動作、GitHubの必須検査仕様の確認を、各最新版CLIや実GitHubの実行済み証拠へ変換しません。既存workflowの配置・上書き防止はローカルで確認し、実GitHubのデータ準備・判定・merge拒否は未確認として残します。

## SOURCE-002・003の読み合わせと具体化判断

2026-09-27、必要な成果物を既存文書の補修と二つのcontrol配下の教材に絞りました。
SOURCE-002は検査対象・送信・受入・mergeの違い、SOURCE-003は検索・精査・通知・対応と重複抑制の限界を、一つの場面から読めることを完了条件としています。
各教材からcontrol、設計、既存実装と後続の対応へたどれるようにし、この文書範囲は完了しました。新しい実装例は選びません。

既存Python hookは、merge時だけに追加された内容をpush検査で見逃すことを使い捨てGitで観測したため、小さな修正と一件の回帰テストを必要な作業へ追加しました。
修正前の失敗と修正後の8件成功、公開情報監視の模擬HTTPで6件成功を確認しました。Git / Gitleaks例の再実行や実GitHub検索は今回行っていません。
組織での有効化・全書込み経路・負荷、監視の内容変更・再出現・判断期限・人の対応は、限定実装から推測せず別の導入判断として残します。

## CICD-003の具体化判断

2026-09-27、[旧CICD-003](MIGRATION_CI_CD.md#workflow-analysis-migration)の共通要件は既存DETECT-001、教材はそのcontrol配下へ配置し、workflow固有の受入・結果公開を[ENG-CICD-007](../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)へ分けました。必要な成果物はこれらの文書、診断項目、資料記録と旧項目の対応です。方式・失敗経路・既存controlとの分担を選べることを完了条件とし、この範囲は完了しました。

既存scannerの仕様で判断できるため、独立control、独自scanner・SARIF parser・配布workflowは追加しません。旧固定profileを完成した導入例にせず、実対象の版・収集・出力mode・受入条件・権限と拒否は未確認として残します。実装例の不在は残作業にしません。

## CICD-002の具体化判断

2026-09-27、[旧CICD-002](MIGRATION_CI_CD.md#workflow-input-migration)からcontrol、control配下の教材、設計pattern、診断項目を選びました。題名を扱う短いstep断片で命令とデータの違いを読めるため、独自scanner・導入workflow・中央配布は追加しません。方式、失敗経路、引数と操作の意味の違いを判断でき、旧4項目と資料の採否を追えることを完了条件とし、この範囲は完了しました。

旧scannerの回帰試験や生成済み`PASS`を引き継がず、実GitHub・対象shell・呼出先の拒否は未確認です。将来の自動化は、既存方式で残る具体的な不足と保守に見合う効果から選びます。現時点の「実装保留」にはしません。

## CICD-004の具体化判断

2026-09-27、[旧CICD-004](MIGRATION_CI_CD.md#workflow-authority-migration)からcontrol、教材、設計pattern、診断観点を選びました。GitHubの権限と開始条件は具体化できるため、[GitHub設定・smoke workflow](../engineering/cicd-security/purpose-bound-job-authority/implementations/github/README.md)を必要な成果物に含めました。最短導入、各操作からの権限選択、無権限・読取り専用job、Environmentを先に作る手順、条件のskipとprovider側の拒否の分離、解除を完成条件にしています。

必要な権限はjobの用途と操作を読むレビューが必要です。静的なpermission判定器やSaaSを合成JSONで良好とするテストは作りません。ローカルのcopy・source確認・構文検査を、実tokenやGitHubの承認・拒否の観測へ変換しません。旧6項目、6 framework関係、既定値・追加credential・委譲・環境名の境界は[移行判断](MIGRATION_CI_CD.md#workflow-authority-migration)へ残しています。

## CICD-001の具体化判断

2026-09-27、[旧CICD-001](MIGRATION_CI_CD.md#workflow-dependency-migration)からcontrol、教材、設計pattern、診断観点を選びました。直接参照の検査は低コストで具体化できるため、[Python / GitHub実装](../engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)を必要な成果物へ含め、手元への導入・安全なsmoke test・解除・代表CLI経路を完了条件にしました。既存pinactは任意の修正補助とし、更新判断や内部取得の確認は自動化成功から推測しません。

旧行scannerを無変更で移さず、hash固定したPyYAML 6.0.3で実参照の構造を読みます。依存取得の代償、未対応構文のerror、参照数ゼロと入力不足の違いをpatternとcontrolへ戻しました。今回の完了は限定した実装例と文書です。GitHubの受入ルール・迂回拒否、remote参照の出所、内部取得の確認、組織への導入完了は含めません。旧6項目・3 framework関係、sourceと実装の採否は[移行判断](MIGRATION_CI_CD.md#workflow-dependency-migration)へ残しています。

## SOURCE-006の具体化判断

2026-09-27、[旧SOURCE-006](MIGRATION_SOURCE_PROTECTION.md#source-organization-posture-migration)からcontrol、教材、設計pattern、診断観点を選びました。既存controlの本文を複製せず、組織の共通方針と対象ごとの実状態を結ぶ問いを残しました。GitHubの設定確認は具体化できるため、[画面とread-only GETの手順](../engineering/source-protection/organization-baseline-and-drift-review/implementations/github/README.md)、安全なsmoke test、解除方法を完成条件に含めました。

今回は具体的なガイダンスの完成です。組織の変更や実API、拒否、通知は実施しておらず、SaaS設定をfixtureで合格にするテストは作りません。対象数や必要な確認頻度で手作業が負担になり、取得元・権限・保存・通知が決まった場合にcollectorへ進みます。実観測の完了条件と旧10項目の採否は[移行判断](MIGRATION_SOURCE_PROTECTION.md#source-organization-posture-migration)に記録しています。

## SOURCE-005の具体化判断

2026-09-27、[旧SOURCE-005](MIGRATION_SOURCE_PROTECTION.md#repository-recovery-migration)からcontrol、教材、設計pattern、診断観点を選びました。Gitの取得・復元は経路が明確であるため、[Git mirror実装例](../engineering/source-protection/independent-repository-backup-and-restore/implementations/git-mirror/README.md)の最短手順、安全なsmoke test、解除方法も完成条件に含め、七件の実Gitテストを確認しました。独自のbackupサービスや自己申告JSON判定器は作りません。

今回の限定範囲はGitのbranch・tagとobjectの復元です。実保管世代、独立した削除権限、LFS・関連データ、設定、修正・buildの確認が必要な採用先では、この例だけで完了にしません。資料の採否、旧4項目との関係、実装から戻した境界は[移行判断](MIGRATION_SOURCE_PROTECTION.md#repository-recovery-migration)にあります。

## AI-007の具体化判断

2026-09-26、[旧AI-007](MIGRATION_AI_DEVELOPMENT.md#development-work-budget-migration)を開発agentの一作業の上限へ絞り、control、教材、設計pattern、診断観点を必要な成果物として完成しました。時間・費用・呼び出し数を一律に同じ実装で制限せず、計測元、実行中の予約、並列・再開、上限前の実行側判断と停止結果を分けます。旧固定値、合成breaker・通知、製品AI全体のframework関係は成功証拠として継承しません。

ローカル実行時間は技術経路を限定できるため、[GNU coreutils 9.7のtimeout例](../engineering/ai-development-security/development-work-budget-gate/implementations/linux-timeout/README.md)を具体実装として選びました。導入、六件の安全なprocessテスト、解除、子process・再起動・遠隔処理の限界まで確認しました。この例の完了を費用・呼び出し数の制限や実agentへの導入完了としません。後者はagent・版、利用量・料金の取得元、実行前強制点、使い捨て対象を選べた時に再開します。

## 旧AI-005〜009の具体化判断

2026-09-26、[範囲と旧項目の行き先](MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review)を確認しました。旧5件を件数どおりに移すのではなく、AI-006の開発agent操作は既存AI-004へ接続します。AI-007は上記の作業予算へ具体化しました。AI-005・008・009はそれぞれ持続的context、agent間委譲、長時間・自律実行の採用条件が確定するまで保留します。製品AIの機能をこの移行へ戻しません。

## AI-001の具体化判断

2026-09-26、旧[AI-001](MIGRATION_AI_DEVELOPMENT.md#repository-agent-guidance-migration)を開発agentが実際に読むrepository指示の変更レビューと、開発作業への効果比較へ選別しました。[Control](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)、教材、[設計pattern](../engineering/ai-development-security/repository-agent-guidance-review/README.md)、診断観点を必要な成果物としました。GitHubでの受入れ経路は技術的に具体化できるため、[CODEOWNERS・branch保護の例](../engineering/ai-development-security/repository-agent-guidance-review/implementations/github-codeowners/README.md)に変更箇所、使い捨てrepositoryでの確認方法、解除方法を示しました。

例の設定には実在するレビュー担当者と保護branchが必要です。本PJはGitHub上のルール設定や拒否をまだ観測しておらず、導入・実効性の完了とはしません。比較評価の実装もagent・版・課題・実行権限・独立した採点元が定まるまで保留します。旧合成JSONの62.50%→93.75%や固定閾値は採用しません。この主題は開発環境だけを扱い、製品のAI機能の設計やTEVVを含めません。Framework mappingは旧関係を継承せず、116件のままです。

## AI-003の具体化判断

2026-09-26、[旧AI-003](MIGRATION_AI_DEVELOPMENT.md#development-content-injection-migration)を開発agentが読む未信頼資料の主題へ絞りました。読者は、Issue・文書・tool出力の出所と指示権限を区別し、agentの提案から実行までの強制点を選ぶ必要があります。このため[control](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)、control配下の教材、[設計pattern](../engineering/ai-development-security/untrusted-development-content-boundary/README.md)、診断観点を必要な成果物とし、本文と旧項目の対応まで完了しました。Framework mappingは旧`verifies`関係を継承せず、116件のままです。

実装例は採用するagent・版、入力取得元、toolの実行前強制点、保護対象、使い捨て環境を選べば限定して作れます。現時点ではこれらが未指定で、旧verifierも合成JSONの自己申告を検査するだけなので保留します。実装再開時の完了条件は、無害なcanaryで元の作業の成功、不要操作の拒否、取得・判定障害を実際に観測し、解除方法と未対応経路を示すことです。診断項目を記載したことを試験済みとしません。

## Secure Codingの進め方

Web application／web serviceに共通するSecure Codingの要件観点は、固定した[OWASP ASVS 5.0.0](../sources/README.md#spec-owasp-asvs-5-0-0)を参照先とします。旧計画の`PSB-CODE-001〜004`（アプリケーションsecret、認証・session、認可、injection）は、番号や計画があることだけを理由に独自controlへ一対一で移行しません。対象製品に適用する要件を選ぶ際は、ASVSの版・exact要件ID・原文・適用条件を確認します。ASVSのlevel達成や領域全体のcoverageは、この索引やmappingから推定しません。

利用者は経験由来の独自の脆弱性診断チェックリストを後日提供する予定です。これはASVSを置き換える資料でも、ASVSから復元する資料でもありません。受領時には次の順で扱います。

1. 題名、作成者または管理者、版・更新日、項目IDと原文、適用対象、公開可能な範囲を確認する。非公開項目や実案件の証拠を公開repositoryへ転記しない。旧`REF-USER-004`と同じ資料かどうかも、この時点で確認する。
2. 原文と由来を保持したまま、各項目が何を診断するかを整理する。ASVS 5.0.0のexact要件と重なる、補足する、ASVSの対象外、判断保留のどれかを理由付きで記録する。重ならない実務観点も捨てず、ASVSの語彙へ無理に言い換えない。
3. 読者の判断に役立つシナリオ・診断観点は関連する教材やcontrolへ結び付ける。独立control・pattern・実装例は、固有の失敗経路と強制点を説明でき、実装判断に価値がある場合だけ作る。チェックリスト項目をテストコードへ一律に変換しない。

原本はまだ受領していません。項目、適用範囲、ASVSとの対応、公開可能性は未確認です。[Secure Codingの入口](../controls/records/secure-coding/README.md)には、この状態を明示します。

## SOURCE-003の限定実装

2026-09-26、利用者が公開GitHubのコード・Issue・PRを対象に、少数の自社ドメイン名・メールアドレスから候補を探す経路を選んだため、[GitHub indicator watch](../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)を具体実装として追加した。完了条件は、使い捨てのHTTP環境で候補発見、人の精査前の非通知、同じ候補の重複抑制、Webhookへの一度の通知、不完全結果と壊れたstateの失敗を観測すること。旧1300行超のPoCをコピーせず、第一ページの少数クエリ、ローカルstate、人が選んだ候補だけの通知に絞る。

この実装はSOURCE-003の公開ソース情報の観測を具体化し、DETECT-003の公開サービス・台帳照合は実装しない。実GitHub検索、組織の認証情報と指標、通知先、精査と対応運用は未確認。詳細は[実装README](../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)と[旧PoCの扱い](MIGRATION_SOURCE_PROTECTION.md#public-exposure-migration)を参照してください。

## DETECT-003の具体化判断

2026-09-26に旧`PSB-DETECT-003`を[External attack surface reconciliation](../controls/records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md)へ移した。外部公開候補の所有・台帳照合・再出現・収集障害・調査許可は、control、教材、pattern、診断観点として整理した。旧Python verifierには実際の台帳照合・再出現判定があるが、旧packageにはCT・DNS・HTTPSのcollectorがなく、台帳の正しさも観測しない。限定profileをそのまま移植せず、CT・DNS・HTTPSを全対象に必須とはしない。HTTPS 443番や固定期限も製品非依存の要件にしない。

実装例の開始条件は、使い捨てまたは明示的に許可された対象、採用する収集元とAPI、正本台帳、能動的確認の許可範囲、通知先を決めること。正常な一致、未登録・期待外、収集の部分取得・失敗、再出現を実際に観測できる形にする。旧ATT&CKの`detects`とSSDF `RV.1.1`は直接性が不足するため非継承とした。詳細は[移行記録](EXTERNAL_ATTACK_SURFACE_MIGRATION.md)を参照してください。

## CODE-005の具体化判断

2026-09-26に旧`PSB-CODE-005`を[Unicode source review](../controls/records/secure-coding/psb-code-005-unicode-source-review/README.md)へ移しました。文字と識別子を実ソースから読めるため、control、教材、pattern、診断観点に加え[Python 3.10限定scanner](../engineering/secure-coding/unicode-source-review/implementations/python/README.md)を必要な成果物としました。導入・smoke test・解除、正常・検出・評価不能の観測を含みます。

旧ASCII識別子と文字拒否リストはPython向けの狭いprofileとして保持し、全言語の普遍要件にしません。UTS #55／#39に照らし、多言語テキストと表示支援を設計上の選択肢として残します。Protected CI、レビュー画面、採用先path・例外、別言語の実装は未確認です。詳細は[移行記録](UNICODE_SOURCE_MIGRATION.md)を参照してください。

## CONTAINER-005の具体化判断

2026-09-25の選別では、旧`CNT-003..006`を一つのWorkload privilege confinementへまとめました。Application processの侵害からroot、kernel機能、host attachment、writable root filesystem、control-plane credentialへ進む経路は、全containerを同じ実効runtime profileで扱う必要があるためです。

`CNT-007`のresource availabilityはquota、scheduling、eviction、node capacity、runtime PIDを、`CNT-008`のnetwork segmentationはCNI、identity、ingress／egress、DNS、外部境界を扱うため分離しました。その後、resourceはCONTAINER-007、networkはCONTAINER-006へ移行しました。IaC／CI検査は早いfeedback、live admissionはcontroller生成後を含む最終強制点とし、同じ成果として扱いません。項目ごとの判断は[Workload confinement移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#workload-confinement-migration)に保持します。

この主題はKubernetesの技術経路が明確なので、文書に加えて[Kubernetes 1.37 Pod Security Admission + CEL実装](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/implementations/kubernetes-psa-cel/README.md)を必要な成果物に選びました。対象版、変更箇所、使い捨てclusterでの確認、解除、制限を記載し、YAMLとscriptをrepositoryで検査します。Live clusterの拒否とruntimeの実効状態は導入証拠として別に残します。

## CONTAINER-006の具体化判断

2026-09-25の選別では、旧`CNT-008`をWorkload network segmentationとして独立させました。Process権限を絞っても、侵害されたworkloadにneighbor、管理service、外部宛ての通信が残ればlateral movementやexfiltrationが成立するため、CONTAINER-005へ統合しません。

この主題ではKubernetes core NetworkPolicyの技術経路が明確であり、policy objectを受理するだけでdata planeの強制を証明できない失敗も具体的です。そのため[Kubernetes 1.37 NetworkPolicy実装](../engineering/container-cloud-iac-security/workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)を必要な成果物に選びました。三つの使い捨てnamespaceでdefault denyを先に配置し、source egressとdestination ingressの片側allowを個別に追加・削除して実通信の成功・拒否を確認します。

DNS、external destination、IPv6、hostNetwork、node traffic、NAT、L7 identityには共通の安全な固定値がありません。代表実装へ架空のallowを足さず、flow contractと採用CNI・gateway・proxyに応じて具体化する項目としてpatternへ残しました。RepositoryではYAMLとshellを静的に検査します。Live CNI enforcementは未実行であり、導入証拠にはしません。項目ごとの判断は[Network segmentation移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#network-segmentation-migration)に保持します。

## CONTAINER-007の具体化判断

2026-09-25の選別では、旧`CNT-007`をWorkload resource consumption boundsとして独立させました。Process privilegeとnetwork reachabilityを制限しても、loop、fork、log、replica増加が共有nodeや別tenantのCPU、memory、PID、local storage、object capacityを枯渇させるためです。

Workloadのrequest／limit、namespaceのaggregate quota、node allocatable・reservation・pressureは別の強制点ですが、直接の失敗は「一workloadの消費が共有capacityへ広がること」です。一つのcontrolの別特性として保持し、[Kubernetes 1.37 ResourceQuota + CEL実装](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)はnamespace admissionとquotaだけを具体化しました。

旧固定値を普遍的な安全値として移さず、test profileに限定しました。Live APIでは必須値不足、aggregate quota超過、正常PodのQoSとquota usageを確認する構成です。PID、node reservation、pressure／eviction、cgroup、capacityはproviderとnode構成に依存するため、架空のplatform evidenceで完了させません。RepositoryではYAMLとshellを静的に検査し、live clusterでは未実行です。項目ごとの判断は[Resource consumption移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#resource-consumption-migration)に保持します。

## CONTAINER-003の具体化判断

2026-09-25の選別では、旧`PSB-CONTAINER-003`をContainer host and daemon boundaryとして再編集しました。Workload specのnon-root、capability、hostPath、seccomp等はCONTAINER-005へ残し、CONTAINER-003はruntime socket、kubelet・補助endpoint、host上のprotected state、node identity、host側isolation、管理操作、更新・隔離・再登録を扱います。

Provider-neutralなcontrol、教材、[Node runtime and management boundary](../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)は必要な成果物に選びました。一方、具体実装は対象OS distribution、runtime、Kubernetes distribution、managed／self-managed provider、node image build、identity、network、attestationで変更箇所と確認方法が変わるため追加していません。

旧synthetic `policy.json`、`host-evidence.json`、exception fixture、Python verifierはlive hostを観測せず、自己申告値の比較を実効的なhost implementationに見せるため非移植です。対象platform、変更箇所、使い捨てnode pool、更新・隔離・rollback、取得可能なlive evidenceを一組で選び、導入・確認に役立つ場合だけ限定実装を検討します。詳細は[Container host and daemon移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#container-host-daemon-migration)に保持します。

## IAC-001の具体化判断

2026-09-25の選別では、旧Secure IaC Golden Pathを[Infrastructure change authorization and drift boundary](../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md)へ再編集しました。Golden Pathは標準moduleとworkflowによって安全な変更を作りやすくする入口です。Controlの合格は、reviewしたsource・module／provider・入力・policy・targetがresolved plan、policy decision、保存plan、apply authority、provider上の実resourceへ結ばれることで判断します。

Provider-neutralなcontrol、教材、[Infrastructure plan, apply, and drift boundary](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)は必要な成果物に選びました。旧Python verifierとJSON fixtureはTerraform、OPA、provider APIを実行せず、全変更経路、drift、identity、remediation等を自己申告fieldで表していたため非移植です。

具体実装は、exact IaC tool・policy engine、一provider、一resource、一つのsecurity invariant、使い捨てcloud環境、protected apply、provider-side bypass test、drift・cleanupを一組で選べる時に作ります。Localだけのsynthetic planやmulti-cloud共通fieldを実効的なimplementationとして追加しません。詳細は[IaC移行記録](MIGRATION_CONTAINER_CLOUD_IAC.md#iac-change-boundary-migration)に保持します。

## REL-002の具体化判断

2026-09-25の選別では、旧`PSB-REL-002`を[Provenance distribution and availability boundary](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)へ再編集しました。一releaseに複数artifact、一artifactに複数attestationが存在できる前提で、artifact digestからprovenance identityを発見し、intended consumerが取得できる関係を扱います。

Provider-neutralなcontrol、教材、[Provenance distribution and availability](../engineering/release-integrity/provenance-distribution-and-availability/README.md)は必要な成果物に選びました。旧Python verifierとJSON fixtureはnetwork、registry、release API、storage、consumer clientを実行せず、`immutable`・`available`・`public`等の自己申告fieldを比較していたため非移植です。

2026-09-28の読み合わせで文書範囲を完了とし、実装例の不在は残作業にしない判断へ更新しました。導入・確認に役立つ場合だけ、artifact ecosystemと対象版、artifact・attestation形式、producer／consumer identity、使い捨てrepository、immutability・retention・garbage collectionを選んで限定実装を検討します。固定5分・365日を普遍値として移さず、artifactのconsumption・support・investigation windowへ合わせます。詳細は[Provenance distribution移行記録](MIGRATION_RELEASE.md#provenance-distribution-migration)に保持します。

## BUILD-002の具体化判断

2026-09-26の選別では、旧Hosted consistent buildを[Approved and consistent release build](../controls/records/build-security/psb-build-002-approved-consistent-build/README.md)へ再編集しました。SLSA v1.2のproducer責任に合わせ、目標profileに合うbuilder選定と、verifierが期待値を作れる一貫した手順を分けます。Hosted実行はBuild L2以上の選択時に必要です。

Provider-neutralなcontrol、教材、[Approved release build process](../engineering/build-security/approved-release-build-process/README.md)、診断観点を必要な成果物としました。2026-09-28の読み合わせで、この文書範囲を完了とし、実装例の不在は残作業にしない判断へ更新しました。旧verifierは`hosted`・`assessed_slsa_build_level`等のJSON値を読み、実platformやartifactを観測していません。再開時は一つのplatform、artifact family、provenance形式、protected publish gateを選び、正常、別builder・定義・parameter・local uploadの拒否、証拠障害の停止を使い捨てreleaseで確認します。詳細は[移行記録](MIGRATION_BUILD.md#consistent-build-migration)に保持します。

## REL-005の具体化判断

2026-09-26の選別では、旧`PSB-REL-005`を[Artifact signing generation](../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)へ再編集しました。承認したexact artifactと、署名サービスへ接続できる権限を別の条件として扱い、鍵の管理、署名結果のconsumer条件での検証、公開完了をrelease gateへつなげます。

Provider-neutralなcontrol、教材、[Artifact signing boundary](../engineering/release-integrity/artifact-signing-boundary/README.md)、診断観点を必要な成果物に選びました。旧OpenSSL verifierは暗号計算とbytes照合を実行しますが、KMS/HSM、鍵状態、透明性ログ、公開先、release gateは合成JSONの自己申告です。Artifact形式、signer、承認の強制点、公開先、consumer条件が未選定のため、旧envelopeを実装例へ移しません。再開時は使い捨てのrelease先で正常署名、別digest・別identity・signer障害・公開失敗・取得不能の拒否を観測します。詳細は[Artifact signing移行記録](MIGRATION_RELEASE.md#artifact-signing-migration)に保持します。

## REL-004の具体化判断

2026-09-25の選別では、旧`PSB-REL-004`を[Supplier SBOM intake trust](../controls/records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md)へ再編集しました。Provider-neutralなcontrol、教材、[Supplier SBOM intake boundary](../engineering/release-integrity/supplier-sbom-intake-boundary/README.md)、診断観点を必要な成果物とし、供給者の認証と成果物への結合を台帳取込の前に置きます。

旧verifierのEd25519署名計算は実値を確認しますが、独自envelope、手書き状態snapshot、自己申告の台帳権限をそのまま移すと、実供給者の失効・隔離・権限が確認できたように見えます。2026-09-28の見直しでは、文書と診断項目で完了とします。具体実装は、供給者と製品・成果物、署名または配送方式、利用者側の信頼根拠、時刻・失効・訂正のsource、使い捨ての取込先が決まり、導入・確認に役立つ場合だけ選びます。正常、別製品・改変・未知署名者の拒否、状態取得不能、隔離の迂回を観測できることを完了条件にします。詳細は[Supplier SBOM移行記録](MIGRATION_RELEASE.md#supplier-sbom-migration)に保持します。

## REL-003の具体化判断

2026-09-25の選別では、旧`PSB-REL-003`を[Release SBOM identity and analysis boundary](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)へ再編集しました。Source、build、deployment／operationsのSBOMを同じserialへ上書きせず、final artifactを観測したbuild／post-build SBOMをrelease authorityとしてexact artifact digestへ結びます。

Provider-neutralなcontrol、教材、[Release SBOM identity and analysis intake](../engineering/release-integrity/release-sbom-identity-and-analysis/README.md)に加え、[CycloneDX 1.7 artifact binding実装](../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)を必要な成果物に選びました。実artifact SHA-256、SBOM digest・serial・version、文書に記載されたbuild／post-build phase、root・最上位componentのversion付きPURLと`bom-ref`、それらへのdependency・composition参照、composition stateを確認できるためです。実際の生成経路と観測範囲は別に確認します。9 testで正常、artifact変更、phase違い、dangling reference、型の不一致、JSON key重複、unknown composition、malformed inputを確認しました。

旧verifierのstorage、permission、processing receipt、analyzer healthはJSON内の自己申告を比較していたため非移植です。限定実装もCycloneDX schema全体や`complete`の正当性を証明しません。Productionでは固定schema validator、実generator coverage、release storage、intended-consumer retrieval、採用Dependency-Track版、data source health、deployment catalogを別に接続します。詳細は[Release SBOM移行記録](MIGRATION_RELEASE.md#release-sbom-migration)に保持します。

## SOURCE-002の具体実装計画

2026-09-23の具体化判断：Git hooksとsecret scannerを接続する技術経路を絞れ、検査対象の取り出し方、拒否への接続、
障害・出力の扱いを具体化すると読者が導入判断をできるため、実装例を必要な成果物に選びます。
文書と診断で確認する項目に加え、2026-09-23に[Git・Gitleaks代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)を追加しました。
2026-09-25には、旧scannerを読みやすいローカル用の[Python pattern scanner](../engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner/README.md)として追加しました。
実装例としての完了条件は満たしました。組織の導入、実環境診断、全経路の強制は別の未実施事項です。

- **配置・範囲**：[Secret checks before publication](../engineering/source-protection/secret-checks-before-publication/README.md)配下の`implementations/`に、一つの代表構成を作る。対象OS・Git・scannerの版を確定し、staged内容・commit message・pushで導入する履歴を検査するローカルhooksとの接続を示す。
- **実装選択**：境界を厳しく扱う実装はGitleaks 8.30.1の組込み検出を採用し、独自scriptをGit objectの取得、上限・未対応形式の拒否、結果の整合確認へ限定した。別に、正規表現とhookの接続を読めるPython標準ライブラリ版を移行した。旧Docker wrapperとinstallerは非移植で、両実装の検出同等性は主張しない。
- **境界**：ローカル実装が担うSECRET-1〜4・6・7の範囲を明示する。SECRET-5は独立した受信側検査の具体設定・確認手順を一構成で示す。受信側が未完なら残作業として記録し、ローカルhooksや送信後のCIで達成した扱いにしない。組織全体の例外承認や全経路の導入済み状態は主張しない。
- **導入と更新**：既存hooks・設定への影響、明示的な導入方法、版の更新、解除・切り戻しを示す。未レビューのhookを自動実行しない。本PJ自身へのhooks有効化は実装例の追加と別の作業とする。
- **確認**：Gitleaks版は隔離した一時worktreeとbare repository、未発行で無効な検出用文字列により23件を確認した。正常入力、indexと作業ツリーの不一致、履歴・メッセージ・タグ・複数ref・force push・merge、ローカル省略時の受信拒否、設定弱体化、未対応形式、障害、非表示を含む。Python版は12 rule、near miss、値の非表示、staged内容、削除後も残るpush履歴、Gitによるhook起動を7件で確認した。
- **完了状態**：二つの実装について、設定・コード、前提、確認方法、未検証範囲を追跡できる。Gitleaks版では対象版と取得物digest、導入・解除手順、23件の確認も保持する。全確認項目の自動化、全OS、SaaS、旧installer・Docker wrapperの移植、実環境への適用は範囲外。

## 基本分類と横断分析

[Security scope](SECURITY_SCOPE.md)に従い、AI Development SecurityはAIを使う開発環境へ限定します。
製品自体のAI securityはai-security-foundryの担当です。旧AI-010・AI-011・DEPS-005・DETECT-002は`out-of-scope`です。旧AI-005〜009は[選別済み](MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review)で、開発環境の一部だけを継続候補とします。旧52件との差をそのまま未移行の残件数として扱いません。

現行の11 domainを移行先の基本分類として維持します。[Domain一覧](../controls/README.md#domain一覧)を
読者の入口にし、未移行領域も明示します。成果物がない領域の空ディレクトリは作りません。
七つのレイヤーは偏り・空白、十二の攻撃段階は脅威・受け渡しを分析するために使います。
これらをdomainの置換や、領域ごとの全control移行の義務にしません。

一つの主題を移すたびに主なdomain、隣接domain、前後の受け渡しを確認し、Domain一覧と移行台帳を更新します。
初期三領域に加え、残る八domainの初回棚卸しも完了しています。今後は棚卸し結果と七つのレイヤーで優先主題を選びます。
PSIRTはGovernance / Operations、runner内の検知はCI/CD・Buildとの境界、本番runtimeは
Container / Cloud / IaCとの境界を検討します。教材は主なcontrolの`learning.md`に置き、隣接controlからリンクします。
講義や再学習で育つ問いを、独立した洞察ファイルへ先回りして分離しません。
基本分類の変更はADRに記録します。境界の詳細は[リポジトリ設計](REPOSITORY_DESIGN.md)を参照してください。

## 初期パイロットで確認した構造

| パイロット | 検証する情報設計 | 残す実装価値 |
|---|---|---|
| [PSB-SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | ガイダンス中心の主題を、成果、教材、設計、製品手順へ分ける | GitHubとIdPの導入判断。架空のJSON検査による導入済み判定は移さない |
| [PSB-DEPS-001](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) | 抽象的な観測期間とresolver／proxy固有の挙動を分ける | 小さなnpm設定例。汎用検証器とproxy clientの一括移植は行わない |
| [PSB-CICD-005](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | 信頼境界、攻撃教材、設計パターン、実行可能な設定を分ける | 無権限PR検証とmerge後のfresh run。危険な比較例は隔離する |

初期三件と、その後のBuild・consumer・Application・Operationsで、成果物を分ける構造をレビューしました。
詳細は[構造レビュー](MIGRATION_PORTFOLIO.md#structure-review)に保持します。教材はcontrol・patternへ辿れるnavigationを維持し、受講者個人の理解度や受講記録は本PJで管理しません。

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

三領域の初回棚卸しは[Migration candidates](MIGRATION_PORTFOLIO.md#migration-candidates)を参照してください。
残る8 domainの初回棚卸しは[Portfolio migration review](MIGRATION_PORTFOLIO.md#portfolio-migration-review)を参照してください。
個別実装の詳細レビューは未完了です。

```text
旧成果物と参照資料を読む
  -> 直接の失敗、信頼境界、読者の問いを再定義
  -> 主題の具体化判断を行い、必要な成果物・理由・範囲・完了条件を決める
  -> control／教材／pattern／実装／評価へ必要な内容だけ分ける
  -> 参照資料の役割・ID・採否を見直す
  -> 隣接境界と前後の受け渡し、診断で確認する項目を整理
  -> リンク、版、マッピングを検査。実装を変更した場合は必要な挙動を検証
  -> 読み通しレビュー
  -> 移行台帳と横断索引、この計画の現在地・次作業を更新
```

一回の移行は一つの主題を単独でレビューできる大きさにします。旧52件を一対一変換することや、
旧READMEの全項目を移行先のどこかへ必ず残すことは目標にしません。ただし参照仕様と重要な除外判断は省略しません。

## 独立化後に残る運用判断

公開先と初版の範囲は[Repository cutover](MIGRATION_PORTFOLIO.md#repository-cutover)で確定しています。
ライセンスは未指定です。旧版READMEからの案内の反映状況と、旧版の維持期間・アーカイブ化は別途確認・判断します。
これらをcontrolの移行完了や実環境の導入済み状態と混同しません。

## 分析の正本

- [参照資料の方針](SOURCE_POLICY.md)
- [参照資料と仕様](../sources/README.md)
- [横断分析の軸](ANALYSIS_LENSES.md)
- [移行台帳](MIGRATION.md)
