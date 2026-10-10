# 進め方と移行計画

## 移行の方針

本PJを執筆・移行作業の正本とし、旧product-security-controlsから必要な知識を主題ごとに選別・再編集します。
旧パッケージを保つための空ディレクトリや転送READMEは作りません。独立化の範囲は[Repository cutover](MIGRATION_PORTFOLIO.md#repository-cutover)に記録しています。

主な成果は、何をすべきか、本質をどこで強制すべきか、何を保証しないかを読者が判断できる知識基盤です。
実装、テスト、導入証拠は、この判断を具体化できる場合だけ別の成果物として作ります。

## 読みやすさの見直し

2026-10-07、[SOURCE-003](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)を最初の見直し例にしました。公開された場所に自社の情報がないかを調べる、という本題が、検索・通知・状態管理の説明に埋もれていたためです。Controlは「何を確認し、何が見つかったら誰が判断するか」を先に書き、方法の選択はengineeringへ寄せます。

今後は新規作成と既存controlの読み合わせで、次の順に見直します。

1. Controlの冒頭を一文で言えるか確認する。言えなければ、守るもの、直接の失敗、判断する人を整理し直す。
2. 読者が行う判断を少数の条件で示す。診断項目は、現場で試す価値がある代表例に絞る。同じ説明を別の表や判定例に重ねない。
3. 方式の比較、製品の仕様、細かな失敗処理は対応するengineeringへ移す。学習でつまずく場面は教材へ、採否や版の履歴は移行記録・Sourcesへ残す。移した先へcontrolからリンクする。
4. 最後にcontrolだけを読んで本題と限界が分かり、engineeringへ進めば実装判断ができるか確かめる。`control.yaml`の特性ID、参照資料、マッピングと矛盾しないことも確認する。

2026-10-07に[SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)と[GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)を読み合わせ、通常時の権限管理と漏えい後の対応を短い問いで区別しました。Controlと対応するengineeringを再編集し、細かな失効方法や認証情報の種類ごとの違いはengineeringに置きました。特性IDと参照資料の対応は維持し、実環境の権限・失効・影響調査は確認していません。

続いて[DEPS-001](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)と[CICD-005](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)を読み合わせました。DEPS-001はコード実行前の待機判定、CICD-005はPR由来の実行物を権限付き処理へ渡さない境界を中心にし、方式・迂回経路はengineeringへ整理しました。特性IDと根拠は維持しています。実際の依存解決やGitHub上の権限・拒否は未確認です。

続いて[GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)と[GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)を読み合わせました。GOV-003は製品への影響と担当・期限、GOV-005は新成果物の配布と旧成果物の非稼働を別々に確認する判断から始めます。情報源の扱い、再ビルド、配布・観測の詳細はengineeringへ整理し、特性IDと根拠の対応は維持しています。実製品の優先度判定や稼働環境の置換は行っていません。

続いて[GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)と[DETECT-001](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)を読み合わせました。GOV-001は依存から稼働先までの影響調査、DETECT-001は「指摘なし」と言える検査範囲・完了状態を入口に置きました。SBOMの取得地点や分析完了、検査結果の取得失敗と部分結果は引き続き別に扱います。実製品・実スキャナーの確認は行っていません。

続いて[AI Development Security](../controls/records/ai-development-security/README.md)の入口とAI-001〜004・007を読み合わせました。AI-002は審査した拡張と実際の読込み、AI-004は実効権限、AI-007は一作業の累積量を先に示し、各controlの方式と運用上の詳細はengineeringへ案内しました。製品自体のAI securityは[対象範囲](SECURITY_SCOPE.md)どおり本PJへ戻していません。実agentでの読み込み、拒否、失効、費用上限は未確認です。

続いて[GOV-002の例外管理](../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md)を見直し、「承認した対象と期限だけに効き、期限後は元の拒否に戻るか」を入口にしました。申請・承認・使用時照合の設計はengineeringへ整理し、元の検査結果を合格へ書き換えない境界を残しました。特性IDと参照資料の対応は維持しています。実際の台帳、承認、拒否は未確認です。

続いて[DEPS-002](../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md)を見直し、依存の取得と公開者のコードの実行を別の判断として示しました。許可方式と実行環境の隔離は既存のengineeringへ案内し、特性IDと根拠の対応を維持しました。実端末やCIでの実行拒否は未確認です。

Source Protectionへ戻り、[SOURCE-001](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md)と[SOURCE-002](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md)を読み合わせました。SOURCE-001は端末の現在の状態を利用先のアクセスへ反映する判断、SOURCE-002は送信前・共有先の受入・保存後のmergeを別の境界として先に示しました。続いて[SOURCE-005](../controls/records/source-protection/psb-source-005-repository-recovery-independence/README.md)は独立したコピーからの開発再開、[SOURCE-006](../controls/records/source-protection/psb-source-006-source-organization-security-posture/README.md)は共通設定の対象ごとの実適用を入口にしました。[SOURCE-007](../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md)は端末上の値の保管と受け渡し、[SOURCE-008](../controls/records/source-protection/psb-source-008-sensitive-data-repository-admission/README.md)は認証情報以外の機密データの持込み可否を先に示しました。詳しい方式は既存のengineeringへ案内し、特性IDと根拠の対応を維持しています。実端末・GitHub組織・保管先での拒否や復旧は確認していません。

[DEPS-003](../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)は承認した依存と実際の取得ファイルの一致、[DEPS-004](../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)は今回の依存変更の採用判断を入口にしました。特性IDと参照資料の対応は維持しています。実際のビルドやマージ拒否は未確認です。

[CICD-001](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)はレビューした外部コードの版との結び付き、[CICD-002](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md)は外部入力をCIの命令へ変えないことを入口にしました。診断項目と方式の詳細を分け、実CIでの拒否は未確認です。

[CICD-004](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)はjobに実際に渡る権限、[CICD-006](../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md)は承認したjobからクラウド権限への交換を入口にしました。標準token以外の権限、交換後の操作、旧keyの残存も診断項目に残しました。実環境の設定・拒否は未確認です。

[CICD-007](../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md)は前jobの残存状態とhost権限、[CICD-009](../controls/records/cicd-security/psb-cicd-009-cache-trust-boundary/README.md)はcacheの保存者と利用者を入口にしました。Runnerの破棄と外部cacheの再利用を分け、CI/CD Securityの現行7件を読み合わせました。実runnerやcacheの設定・拒否は未確認です。

Control本文を長さだけで一括短縮しません。情報が本当に必要な場合は残し、対象の環境で効果を出すための手順はengineeringや実装例で具体化します。実装例を増やすことは、この見直しの完了条件にしません。

## 全11 domainの進捗

2026-10-09時点。この作業ツリーには11 domainに計53件のcontrol記録があります。下表は**今回の「本題を一文で示す」読みやすさの見直し**を管理します。既存の移行判断や資料照合をやり直したかどうか、実環境へ導入したかどうかを表すものではありません。「未判定」は、書き直しが必要と決まった意味ではありません。

| Domain | 現行control | 今回の読み合わせ済み | これから確認するcontrol |
|---|---:|---|---|
| [Secure Design](../controls/records/secure-design/README.md) | 1 | DESIGN-001 | なし |
| [Secure Coding](../controls/records/secure-coding/README.md) | 1 | CODE-005 | なし。Webアプリ共通要件は[ASVS方針](#secure-codingの進め方)で扱う |
| [Source Protection](../controls/records/source-protection/README.md) | 8 | SOURCE-001〜008 | なし。講義・実環境確認は別。状態は[下表](#source-protectionの進捗) |
| [Dependency Security](../controls/records/dependency-security/README.md) | 5 | DEPS-001〜005 | なし。新規のDEPS-005は本文と診断項目で整理 |
| [CI/CD Security](../controls/records/cicd-security/README.md) | 7 | CICD-001・002・004〜007・009 | なし |
| [Build Security](../controls/records/build-security/README.md) | 3 | BUILD-001〜003 | なし。実環境の確認は別 |
| [Container / Cloud / IaC Security](../controls/records/container-cloud-iac-security/README.md) | 8 | CONTAINER-001〜007・IAC-001 | なし |
| [Release Integrity](../controls/records/release-integrity/README.md) | 5 | REL-001〜005 | なし。実環境の公開・受入は別 |
| [AI Development Security](../controls/records/ai-development-security/README.md) | 5 | AI-001〜004・007 | なし。開発環境に限る[対象範囲](SECURITY_SCOPE.md)を維持 |
| [Detection / Verification](../controls/records/detection-verification/README.md) | 2 | DETECT-001・003 | なし |
| [Governance / Operations](../controls/records/governance-operations/README.md) | 8 | GOV-001〜008 | なし。実運用の確認は別 |

読み合わせ済みは53件、未判定は0件です。件数は今回の本文見直しの所在を示すだけで、domainの網羅率やセキュリティ効果ではありません。旧番号の欠けを埋めるためにcontrolを増やさず、別の重要な問いが見つかった場合にだけ追加を検討します。DEPS-005は取得時の遮断・追跡という独立した問いから追加しました。

今回、53件すべての本文に「なぜ必要か」と「フレームワークとの関係」を置きました。後者は[現行の対応表](../mappings/frameworks.yaml)にある93件をControlごとに読める形にし、対応表に関係がない16件はその状態を明記しています。これは現在照合済みの関係の見える化であり、世の中の全規格を調査した結果や、準拠・実環境での有効性を示すものではありません。新しい対応関係は資料本文と特性を照合したDEPS-005のSSDF PW.4.1だけです。

教材は各control配下に置いています。利用者との講義と振り返りはSOURCE-001〜003とGOV-004で記録済みです。GOV-001はPSIRTの役割を確認して区切り、GOV-003は利用者の希望に合わせてこちらから判断例を説明しました。実装例は主題ごとの[具体化判断](ARTIFACT_MODEL.md#主題ごとの具体化判断)で選び、作成数を進捗率にしません。ローカルのsmoke testと組織の実環境への導入も区別します。現時点で、この表の「読み合わせ済み」は実端末・実サービスでの強制を確認した意味ではありません。

11 domainの入口を読み合わせ、53件すべてがdomain一覧から辿れることを確認しました。既存の教材・設計パターンへの導線に加え、DEPS-005は新規Controlの本文から確認項目へ進めます。Container / Cloud / IaCなどの入口は、読者が判断する問いを平易に直しました。[GOV-003の判断例](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/learning.md#この場面での判断例)まで講義を進めています。個々の移行理由と確認の限界は、下の[現在地と次の作業](#現在地と次の作業)、主題ごとの具体化判断、各domainの移行記録を参照してください。

## Source Protectionの進捗

2026-10-07時点。SOURCE-001〜008はcontrolと教材を作成済みです。SOURCE-001〜007には設計パターンもあり、SOURCE-008は現時点ではガイダンスと診断項目で完了と判断しています。**文書の移行、平易な文章への見直し、講義、実環境への導入は別の進捗**として扱います。

| Control | 今回の読みやすさの見直し | 講義・振り返り | 実装例・手順の現状 |
|---|---|---|---|
| [SOURCE-001](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md) | 完了 | 三問の講義記録あり | 設計ガイドのみ |
| [SOURCE-002](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md) | 完了 | 三問の講義記録あり | Git hooksの二例。ローカル確認あり |
| [SOURCE-003](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md) | 完了 | 三問の講義記録あり | GitHub公開情報の限定例。実GitHub検索は未確認 |
| [SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | 完了 | 教材あり、講義記録なし | GitHub向けの導入判断手順あり |
| [SOURCE-005](../controls/records/source-protection/psb-source-005-repository-recovery-independence/README.md) | 完了 | 教材あり、講義記録なし | Git mirrorのローカル復元例あり |
| [SOURCE-006](../controls/records/source-protection/psb-source-006-source-organization-security-posture/README.md) | 完了 | 教材あり、講義記録なし | GitHub設定の確認手順あり |
| [SOURCE-007](../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md) | 完了 | 教材あり、講義記録なし | 実装例なし。採用先が決まってから要否を判断 |
| [SOURCE-008](../controls/records/source-protection/psb-source-008-sensitive-data-repository-admission/README.md) | 完了 | 教材あり、講義記録なし | 実装例なし。文書と診断項目で完了 |

８件の本文は今回の基準で読み合わせ済みです。次の講義や実装例を件数合わせで増やしません。実端末・実GitHub組織への導入、拒否、失効、通知、復旧の確認はこの表の「完了」に含めません。主題ごとの未確認事項は[現在地と次の作業](#現在地と次の作業)と各実装例に残します。

## 現在地と次の作業

2026-10-10更新。この節を現在地と次作業の正本とし、候補一覧は棚卸し、構造レビューと移行台帳は経緯・判断の記録として使います。

| 状態 | 内容 |
|---|---|
| 現在地 | 53件のcontrol記録・48件の設計パターン。Framework mappingは93件で、いずれも`design-reviewed`。DEPS-005のSSDF関係を部分的な設計関係として追加した。実環境での導入・強制は未確認 |
| Secure Design→Secure Codingの読み順 | 請求書IDの変更を例に、ModelForgeの脅威候補、DESIGN-001の許可判断と診断項目、ASVS 5.0.0のV8.2.1・V8.2.2、設計パターンをたどれる。ModelForgeがこの問題を検出した実績、全endpointの認可、ASVSへの適合は主張しない |
| Source Protectionの読み順 | SOURCE-002の認証情報、SOURCE-008の顧客データ、SOURCE-003の公開候補を入口で分けた。既知の共有は検索を待たず、認証情報をGOV-004、顧客データ等をデータ所有者と組織の情報漏えい対応担当へ渡す。実事案の判断・対応は未確認 |
| 機密データのGit受入 | 旧DEH-010を[SOURCE-008](../controls/records/source-protection/psb-source-008-sensitive-data-repository-admission/README.md)へ再編集。顧客データなど認証情報以外の持込み可否、検査不能、Gitの受入経路を扱う。対象組織のデータ分類と実際の拒否は未確認。実装例は選ばない |
| 脆弱性報告の受付 | PSIRTの受付空白からGOV-006を新規に作成。公開・社内窓口、受領記録、安全な取扱い、担当者への引き渡し、窓口障害を扱う。旧controlの移植ではなく、組織の窓口・当番・実報告は未確認 |
| 脆弱性の告知・通知 | GOV-006→GOV-003の判断から利用者へ渡す空白にGOV-007を新規作成。修正提供・告知公開・対象者への通知、訂正を分ける。実際の告知・配信・利用者の到達は未確認 |
| 脆弱性の修正検証 | GOV-003の影響・期限とGOV-007の告知の間にGOV-008を新規作成。修正する版、問題の解消確認、検証した版の提供を分ける。GOV-005の稼働成果物置換は別の判断。実製品の修正・検証・配布は未確認 |
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
| DEPS-005の具体化判断 | [Dependency acquisition gate](../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md)を、取得時の遮断・経路の迂回防止・事後追跡としてDEPS-001から分離。Control本文と診断項目でチェックリスト生成の入口を作った。製品選定と対象環境がないため実装例は作らず、プロキシ方式の比較や導入手順が必要になった時点で設計パターンを検討する。Takumi Guard資料とNIST SSDF PW.4.1は2026-10-09に再確認し、後者とは部分的な設計関係を記録。実環境での適用・拒否・履歴・通知は未確認 |
| Codex CLI hardening観点の確認範囲 | 利用者提供の固定版と2026-10-01時点の公式設定資料を照合。AI-004の教材・隔離設計・参照資料へ製品固有の問いを追加。設定・実装・テストコードは増やさず、実効権限や通信経路のlive確認は未実施 |
| 直近の成果 | [Secure Codingの入口](../controls/records/secure-coding/README.md#asvsから探す)をASVS 5.0.0固定版に照合。V4のAPIとV15の一般的な設計・コーディングを加え、製品側のsecretと開発端末の認証情報、CODE-005とASVS要件を区別した。利用者の診断チェックリストは原本待ち |
| Control一覧の見直し | 利用者提示の[AI Security Foundryの一覧（mainの`1ea488f`）](https://github.com/DharmaDoll/ai-security-foundry/blob/1ea488f9fe4bbb6a0dab1405da3a929843bce39f/controls/README.md)を配置の参考にした。Domain別の見取り図とIDから直接開く一覧を分けた。右欄はレビュー結果や診断項目ではなく、現在の53件から読む対象を選ぶための一文要約とした。AISVSの分類や製品AIの要件は移していない |
| 直近の教材更新 | [GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/learning.md#講義と振り返りの記録)は二問への回答から、観測失敗と環境故障を分ける見方を本文へ反映。[GOV-006](../controls/records/governance-operations/psb-gov-006-vulnerability-report-intake/learning.md)は転送停止後の引き渡し、[GOV-007](../controls/records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/learning.md)は告知の情報不足・通知失敗・訂正の再連絡、[GOV-008](../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/learning.md)は検証用・保守中・配布する版の違いを判断例として執筆。GOV-006〜008の質疑応答と実際の窓口・配信・修正確認は未実施 |
| GOV-002の教材更新 | [例外は検査の合格ではない](../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/learning.md)を依存の一版だけを認める場面で書き直した。承認と使用時の照合、別版への流用、期限切れ、台帳を確認できない場合、すでに採用した依存の扱いを判断例にした。実際の承認・拒否は未確認。質疑応答は未実施 |
| SOURCE-004の教材更新 | [一つのリポジトリを読むトークンが、ほかも書き換えられるとき](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/learning.md)を、ソース管理サービス側の過剰権限と古い権限の失効に絞って再編集。端末上の値の保管はSOURCE-007、漏えい後の調査はGOV-004へ渡した。実際の権限・ログ・失効は未確認。質疑応答は未実施 |
| SOURCE-008の教材更新 | [DBダンプをGitに入れてよいか](../controls/records/source-protection/psb-source-008-sensitive-data-repository-admission/learning.md)に、送信前なら持込みを保留し、架空データや許可された別の保管先を選ぶ判断例を追加。既に共有先へ届いた場合は、履歴と到達範囲をデータ所有者・情報漏えい対応担当へ渡す。実データでの受入拒否は未確認。質疑応答は未実施 |
| DEPS-001の教材更新 | [公開直後の依存版をいつ止めるか](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/learning.md)を、更新ボットのPRでCIが先にインストールしてしまう場面から書き直した。公開時刻とPR作成時刻の違い、実行前の判定、判定不能時の扱い、ロックファイル・プロキシ・緊急例外との境界を判断例に残し、方式の比較は設計パターンへ委ねた。実際のCIでの拒否や質疑応答は未確認 |
| 次の主題 | [DEPS-002の教材](../controls/records/dependency-security/psb-deps-002-install-execution-policy/learning.md)を読み直す。依存のインストール時に実行されるコードと、レビュー済みの成果物を再利用する場面を具体例から判断できるようにする |
| 学習経過 | [SOURCE-001](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/learning.md#講義と振り返りの記録)、[SOURCE-002](../controls/records/source-protection/psb-source-002-secret-publication-boundary/learning.md#講義と振り返りの記録)、[SOURCE-003](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/learning.md#講義と振り返りの記録)は各三問、[GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/learning.md#講義と振り返りの記録)は二問で区切り、回答と判断の見方を各教材へ反映した。[GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/learning.md#講義と振り返りの記録)はPSIRTの役割を明確にし、二問は未回答のまま区切った。[GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/learning.md#講義と振り返りの記録)は二問を出した後、利用者の希望でこちらから判断例を示した。実際の検索、失効、送信拒否、影響調査は未確認 |
| 技術資料の次回照合 | GitHub／AWSのworkload federation例について、固定したGitHub・AWS仕様、Actionの参照版、対象環境のclaimとrole権限を個別に照合する。資料上の整合と実環境での交換・拒否は分けて記録する |
| 実装経過（直近） | 20件の実装READMEについて、導入対象、変更・制御点、確認方法、解除、制限とmappingを文書上で確認。GitHub／AWS例の導入・解除とnpm例の解除を補った。[判断の履歴](MIGRATION.md#パイロットの移行記録)と各実装READMEに確認範囲を残した。個々の製品での動作と実環境の導入は今回検証していない |
| REL-003限定実装の再確認 | CycloneDX binding例を使い捨てrepositoryへcopyし、正常`0`、artifact不一致`1`、入力欠落`2`、copyの解除を確認。Python 3.13.5で既存9テスト通過。導入先`tools`・`tools/sbom`がsymlinkならcopyを止め、手元の試行を解除する手順をREADMEへ追加。SBOMの生成地点・coverage・storage・analysis・deploymentはこの実装で未確認 |
| SOURCE-002実装例の再確認 | Python版を使い捨てGitへ導入し、正常commit、無効canary拒否、検査器欠落による停止、解除を観測。NULや5 MiB超をfindingと区別して`ERROR/2`へ修正し、READMEのsmokeに検査不能入力を追加。8件のローカルテストは通過。Gitleaks版は導入・解除手順を読んだが、手元binaryのhashが固定配布物と異なり実Gitleaks試験は行っていない。両方式の実環境導入は未確認 |
| 開発者からの読者導線 | Engineering索引の47 patternを点検。各patternからcontrolへ進め、52 controlの教材はcontrol配下へ辿れる。GOV-004は講義の二問を受けて教材を作成した。参照資料への直接リンクが欠けていたSOURCE-003 patternを補修。索引冒頭へ読む順序と実装例あり・なしの例を移し、Object access boundaryの主domain表示をSecure Designへ合わせた。実装の動作・組織導入は未確認 |
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
| DESIGN-001の確認範囲 | OWASP Authorization Cheat SheetとASVS 5.0.0固定版V8に基づくcontrol・教材・設計・診断項目を保持。過去のサンプル試験は移行台帳へ残し、現在の実装・診断結果とは扱わない。HTTP認証、全endpoint、実tenant、組織導入は未確認 |
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

## 学習講義からコンテンツへ

移行済みのcontrolから、一件ずつ講義と振り返りを進めます。全domainの移行完了や実環境での導入を待つ必要はありません。SOURCE-001〜003は各三問、GOV-004は二問で区切りました。[GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/learning.md#講義と振り返りの記録)はPSIRTの役割を明確にし、二問への回答を得ないまま次へ進みました。[GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/learning.md#講義と振り返りの記録)は、利用者の希望でこちらから判断例を示しました。番号順の消化は目的にしません。

1. 講義前に、そのcontrol、`learning.md`、関連pattern・実装例、参照資料を読み、何を判断する講義かを一つの場面で定める。
2. 講義は、なぜそのcontrolが必要かを短いシナリオで説明してから始める。その場面で何を見て、どの結果をどう分けるかという判断の軸と、具体的な判断例を先に平易な言葉で示す。攻撃が成立する条件、守る境界、できてはいけないこと、対策の限界を具体例でたどる。質問で考えたい場合は一回につき2〜3問に区切り、利用者が講義の結果を求めた場合は回答を要求せず、判断例と理由を説明する。理解度や点数は記録しない。
3. 講義後に、実際に出た問い、誤解しやすかった点、そこから得た見方と判断基準を該当controlの`learning.md`へ反映する。根拠の確認が必要な主張は資料へ戻り、確認前に事実として書かない。Controlの特性やpatternの選択条件を変える必要があると分かった場合だけ、それぞれの正本を直す。
4. Controlから教材へ、教材から関連pattern・実装例へ自然にたどれるか読み直す。実装例は導入・制御・確認に役立つ場合だけ追加し、講義を行ったこと自体を成果物の数や実環境での検証結果にしない。

一回の完了条件は、講義で生じた問いの扱いが教材または未確認事項として追跡でき、読者が場面からcontrolの判断と限界へ進めることです。教材に既に十分な説明がある場合は、変更なしと理由を記録して次へ進みます。独立した洞察ファイルは先に作りません。
学習の経過は各controlの`learning.md`に日付付きで短く残し、このページの「学習経過」から現在の講義へ進めるようにします。実装の現在地はこのページの実装関連行、採否や試験範囲の履歴は[移行台帳](MIGRATION.md#パイロットの移行記録)と各実装READMEで追います。いずれも理解度や組織導入済みの記録には使いません。

## 11 domainの空白レビュー

2026-10-04に[全domainの入口](../controls/README.md#domain一覧)、[七レイヤーの空白](ANALYSIS_LENSES.md#プロダクトセキュリティの7レイヤー)、旧項目の採否を照合しました。これは文書で読める問いの確認であり、実環境の導入や全主題の網羅性を評価した結果ではありません。

| Domain | 今回の判断 |
|---|---|
| Secure Design / Secure Coding | 個別システムの脅威モデル作成は[ModelForgeとの境界](REPOSITORY_DESIGN.md#分類領域の選び方)、Webアプリ共通の検証要件は[ASVS方針](REPOSITORY_DESIGN.md#secure-codingとasvs)へ。DESIGN-001の請求書シナリオを全アプリの検証と扱わない。利用者の診断チェックリストは原本待ち |
| Source Protection | [SOURCE-002](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md)は認証情報等のsecret、[SOURCE-003](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)は公開後の候補発見。[SOURCE-008](../controls/records/source-protection/psb-source-008-sensitive-data-repository-admission/README.md)は認証情報以外の機密データをGitへ入れる前の判断を扱う |
| Dependency Security / CI/CD Security / Build Security / Container / Cloud / IaC Security / Release Integrity | 既存の入口では、採用・実行・build・公開・使用の別の判断へ進める。このレビューでは、新controlが必要な別の失敗経路を特定していない。残る実環境の強制・取得・拒否の確認を、controlの欠番と混同しない |
| AI Development Security | 旧AI-005・008・009は、採用する開発agentの保存・委譲・停止経路が決まるまで[保留](MIGRATION_AI_DEVELOPMENT.md#ai-development-scope-review)。製品AIの主題を本PJの空白へ戻さない |
| Detection / Verification | 既存のscanner結果と外部公開候補の判断を読む。旧DETECT-002のAI製品TEVVは[対象外](SECURITY_SCOPE.md#旧controlの移行判断)。実scannerの導入やアプリ診断の未実施を、直ちに新controlの必要性とはしない |
| Governance / Operations | 脆弱性報告から通知までの[読む経路](../controls/records/governance-operations/README.md#一つの脆弱性報告を追う)を確認済み。組織全体の修復完了とPSIRT能力は、採用先の責任者と証拠を選んでから評価する |

旧DEH-010の検討結果は[SOURCE-008の具体化判断](#source-008の具体化判断)に記録しました。拡張子・サイズ・形式の検査は兆候であり、ファイルが安全という証明にはしません。

## SOURCE-008の具体化判断

顧客データを含むDBダンプは、認証情報用のsecret scanが通ってもGit履歴へ入れてよいとは限りません。旧DEH-010の拡張子・サイズ・形式による検出だけでは、誰が持込みを許すか、読めない内容をどう扱うか、別の書込み経路をどう止めるかが決まりません。SOURCE-002はsecret値、SOURCE-003は公開後の候補発見を扱うため、別の直接の失敗として[SOURCE-008](../controls/records/source-protection/psb-source-008-sensitive-data-repository-admission/README.md)を作りました。

必要な成果物はcontrol、DBダンプから判断を学べる[教材](../controls/records/source-protection/psb-source-008-sensitive-data-repository-admission/learning.md)、診断項目、[旧資料の採否](../sources/README.md#ref-sensitive-data-repository-001)です。読者がデータ所有者、代替保管先、Gitの受入境界、検査不能・判断待ちを決められれば文書の完了条件を満たします。既存のGit検査patternは境界の考え方として参照し、機密データの判定をsecret scannerへ任せません。新pattern・実装例・テストコードは追加しません。対象組織のデータ分類、許可する代替先、Gitサービスと全書込み経路が決まり、限定実装が導入と拒否の確認を改善するときにだけ再検討します。実環境の拒否は未確認です。

## GOV-006の具体化判断

報告が届いても担当者へ渡らない失敗を扱うため、[control](../controls/records/governance-operations/psb-gov-006-vulnerability-report-intake/README.md)、[教材](../controls/records/governance-operations/psb-gov-006-vulnerability-report-intake/learning.md)、診断項目、[参照資料の採否](../sources/README.md#ref-vulnerability-report-intake-001)を選びました。読者が窓口の到着、受領連絡、安全な保管、担当者への引き渡し、失敗時の再確認を区別できれば文書の完了条件を満たします。旧controlを移植したものではありません。

受付の方式はメール、Web form、support窓口など組織によって変わります。今回は導入先がないためpatternと実装例を作らず、固定の応答時間や受付方法も指定しません。採用先の窓口・当番・保管先が決まったら、実報告を使わない安全な経路確認、転送障害、担当者への到達、閲覧権限を評価します。実窓口の導入やPSIRT能力は未確認です。

## GOV-007の具体化判断

修正を出しても利用者が自分の対象と行動を分からず、通知失敗も見えない経路を扱うため、[control](../controls/records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/README.md)、[教材](../controls/records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/learning.md)、診断項目、[参照資料の採否](../sources/README.md#ref-vulnerability-advisory-001)を選びました。修正の提供、告知の公開、対象者への通知と訂正を分け、利用者が取るべき行動と未確認の範囲を説明できれば文書の完了条件を満たします。旧controlの移植ではありません。

通知手段、公開時期、関係する他社との調整は事案と組織で変わります。対象製品、利用者群、告知・配信基盤が決まっていないためpattern・実装例・テストコードは追加しません。採用先が決まったら、実脆弱性を使わない安全な配信試験、欠落した宛先、訂正の再連絡を評価します。全利用者への到達や修復完了は主張しません。

## GOV-003の一般的な製品適用性の読み合わせ

GOV-003は既に、影響候補・範囲付き非該当・調査不能を優先度判断へ渡す特性を持ちます。CVE・PURL・SBOMを必須に見せていた記述を改め、自社コードの問題でも、製品担当者が機能・設定・版・稼働先と確認範囲を調べた結果を使えるようにしました。依存が原因ならGOV-001の詳細な調査を使います。既存の特性と別の失敗を定義する必要はないため、新しいcontrolは作りません。

[GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)の本文・機械可読記録・教材、[設計pattern](../engineering/governance-operations/vulnerability-priority-decision/README.md)、診断項目、[参照資料](../sources/README.md#ref-vulnerability-priority-001)を今回の必要な成果物とします。実製品の影響調査や再現、修正の正しさは確認していません。製品ごとに変わる調査手順を、汎用scriptや架空の合格証拠にはしません。

## GOV-008の具体化判断

GOV-003は影響と優先度、GOV-005は稼働する旧成果物の非稼働、GOV-007は利用者への告知を扱います。修正を主張する版で問題が解消したか、検証した変更が実際に提供される版と同じかは、これらの直接の合格条件ではありません。この別の失敗経路に対して[control](../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md)、[教材](../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/learning.md)、診断項目、[参照資料の採否](../sources/README.md#ref-vulnerability-remedy-validation-001)を選びました。旧controlの移植ではありません。

読者が変更の取込み、修正の検証、検証した版の提供、旧版の残存を別々に判断できれば文書の完了条件を満たします。修正手段と検証方法は問題・製品で変わるため、pattern・実装例・テストコードは追加しません。採用先が決まったら、実データを使わない安全な検証、修正版と配布版の同一性、入手不能時の状態を評価します。実製品での修正済みや全利用者の更新は未確認です。

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

2026-10-05に具体化判断を見直し、control、請求書の教材、設計パターン、診断項目で完了とします。読者が、他人の対象へのアクセスをどこで拒否するか、所有者・tenant・操作をどう結び付けるか、別の到達経路で何を確認するかを判断できることが完了条件です。

説明用のPython／SQLiteサンプルと7テストは削除しました。サンプル自身の動作を示しても、読者のアプリケーションの導入や診断には直接つながらず、今回の問いは設計説明と診断項目で伝えられるためです。実装例の不在を残作業にせず、診断項目に対応するテストを一式そろえることも目標にしません。将来、具体的な導入・接続の問題が学習や実案件から見つかった場合に、その問題への実効性で実装の要否を判断します。

[ASVS 5.0.0の固定版V8](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x17-V8-Authorization.md)のV8.2.1は機能ごとの明示的な権限、V8.2.2は対象データごとの明示的な権限を確認します。2026-09-29に追加した`supports / medium / design-reviewed`の部分関係二件は、操作権限と所有者・tenant付きの取得・更新条件という設計上の関係として保持します。V8.2.3のfield別権限、V8.3.1の信頼できるservice層、V8.4.1の全tenant操作は、この請求書シナリオから対応済みとしません。

対象アプリケーションのHTTP認証、全endpoint、一覧・export・一括処理・cache、並行処理は未確認です。[Sources](../sources/README.md#ref-application-authorization-001)にASVSとの採否と限界、[移行台帳](MIGRATION.md#design-001-example-retirement)にサンプルの削除を記録します。利用者の診断チェックリストは引き続き原本待ちです。

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

2026-10-05に[Secure Codingの入口](../controls/records/secure-coding/README.md#asvsから探す)を固定版の章立てと照合しました。V1とV2の違い、V4のAPI、V13.3のアプリケーションsecret、V15の設計・言語固有の問題を案内します。開発端末の認証情報はSOURCE-007へ、UnicodeのソースレビューはCODE-005とその一次資料へたどります。章へのリンクは要件の適用や診断の実施を示しません。

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
2026-10-06の見直し：通常のGitHub.comへの直接pushでは自前のGit受信先を使わない。端末側hookは送信前の補助、GitHub側のpush protectionは製品の対象・設定・迂回条件を確認する別の受入制御とし、両者の検出同等性は主張しない。自前Git受信先の`pre-receive`コードは参考紹介にとどめ、標準的な導入手順やGitHub.com向けの実装として扱わない。

- **配置・範囲**：[Secret checks before publication](../engineering/source-protection/secret-checks-before-publication/README.md)配下の`implementations/`に、一つの代表構成を作る。対象OS・Git・scannerの版を確定し、staged内容・commit message・pushで導入する履歴を検査するローカルhooksとの接続を示す。
- **実装選択**：境界を厳しく扱う実装はGitleaks 8.30.1の組込み検出を採用し、独自scriptをGit objectの取得、上限・未対応形式の拒否、結果の整合確認へ限定した。別に、正規表現とhookの接続を読めるPython標準ライブラリ版を移行した。旧Docker wrapperとinstallerは非移植で、両実装の検出同等性は主張しない。
- **境界**：ローカル実装が担うSECRET-1〜4・6・7の範囲を明示する。SECRET-5はGitHub.comのpush protectionの対象・設定・例外と書込み経路を採用先で確認する必要がある。自前Git受信先の`pre-receive`は隔離したbare repositoryで動きを示す参考コードであり、GitHub.comでのSECRET-5達成の証拠にしない。組織全体の例外承認や全経路の導入済み状態は主張しない。
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
