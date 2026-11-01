# サプライチェーン攻撃の対策：実践ガイド24章

依存を更新しただけで、インストール処理が端末やCIの秘密を読み取ることがあります。開発者・開発基盤担当者・プロダクトセキュリティ担当者が、外部コードを取得する前、実行する前、公開する前に何を制限し、侵害が疑われたら何を調べるかをまとめます。守る対象はソース、秘密情報、公開権限、配布成果物、稼働環境です。

まず1〜8章で取得と実行の順序を決め、13〜14章で実行時の権限を絞ります。公開者は9〜10章、CI・開発ツールの管理者は19〜22章も確認してください。調査に備える17章と23〜24章は、導入時から担当と記録を決めます。各章の「確かめ方」は導入後の確認項目であり、実施済みの結果ではありません。

本書は[承認された訂正案](https://github.com/DharmaDoll/product-security-guidance/blob/5ab008157aa351d2764ffad2f18bc42cc615fc43/sources/reviews/supply-chain-countermeasures.md)を読者向けに編集したものです。原資料の全文転載ではありません。[資料の識別情報・採否](../sources/README.md#ref-supply-chain-countermeasures-001)と[編集判断の記録](../sources/reviews/supply-chain-countermeasures.md)から根拠をたどれます。工程をまたぐ設計は[多層防御ガイド](supply-chain-defense.md)を参照してください。

製品仕様の確認日は訂正案に記録された**2026-11-01**を引き継ぎます。明記した版以外への適用は確認が必要です。更新される公式文書は`re-review-required`とし、クライアント更新、既定値・優先順位、認証方式、検査対象の変更時に再確認します。設定値は適用範囲と残る経路を合わせて読み、設定しただけで安全と判断しません。モデル・データセットの供給とAIアプリケーション固有の対策は[対象範囲](../docs/SECURITY_SCOPE.md)外です。

## 目次

- [背景](#背景)
- [1. lifecycleスクリプトの無効化](#1-lifecycleスクリプトの無効化)
- [2. クールダウン(最小リリース経過時間)](#2-クールダウン最小リリース経過時間)
- [3. SemVerレンジの制御とバージョン固定](#3-semverレンジの制御とバージョン固定)
- [4. lockfileの厳格な運用](#4-lockfileの厳格な運用)
- [5. lockfileインジェクション対策](#5-lockfileインジェクション対策)
- [6. 新規依存+installスクリプトの検知](#6-新規依存installスクリプトの検知)
- [7. インストール前の事前監査ツール](#7-インストール前の事前監査ツール)
- [8. Provenanceアテステーションとnpm audit signatures](#8-provenanceアテステーションとnpm-audit-signatures)
- [9. OIDC Trusted Publishing(長期トークンの排除)](#9-oidc-trusted-publishing長期トークンの排除)
- [10. アカウント保護(2FA / Passkey)](#10-アカウント保護2fa--passkey)
- [11. プライベートレジストリプロキシ(Dependency Confusion対策)](#11-プライベートレジストリプロキシdependency-confusion対策)
- [12. ad-hoc実行の安全化 (npx / pipx / uvx / go run)](#12-ad-hoc実行の安全化-npx--pipx--uvx--go-run)
- [13. シークレットの保護(.envファイルの扱い)](#13-シークレットの保護envファイルの扱い)
- [14. Dev Container / サンドボックス開発](#14-dev-container--サンドボックス開発)
- [15. 依存ツリーの削減](#15-依存ツリーの削減)
- [16. ネットワーク監視とIOCフィードの運用](#16-ネットワーク監視とiocフィードの運用)
- [17. SBOM(ソフトウェア部品表)の生成と管理](#17-sbomソフトウェア部品表の生成と管理)
- [18. YARA / 静的解析によるパッケージスキャン](#18-yara--静的解析によるパッケージスキャン)
- [19. CIパイプラインのハードニング](#19-ciパイプラインのハードニング)
- [20. コンテナイメージのサプライチェーン](#20-コンテナイメージのサプライチェーン)
- [21. IDE拡張機能・開発ツール](#21-ide拡張機能開発ツール)
- [22. AIコーディング支援・MCPサーバ](#22-aiコーディング支援mcpサーバ)
- [23. インシデント対応ランブック](#23-インシデント対応ランブック)
- [24. ブラストレイディアス評価](#24-ブラストレイディアス評価)
- [対策一覧と着手順](#対策一覧と着手順)

## 背景

普段使っているパッケージの更新でも、追加された依存や準備処理が端末・CIの権限で動くと、製品を起動する前に秘密が盗まれます。2026年3月31日のAxiosの不正な版（1.14.1、0.30.4）では、追加依存`plain-crypto-js`のインストール処理が実行経路になりました。親パッケージの主要コードだけを見ても判断できない例です。[Microsoftの調査報告（2026-04-01）](https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/)

2025年のShai-Huludの調査では、依存の準備処理から認証情報を盗み、その公開権限で別パッケージへ広がる経路が報告されています。取得時の対策と公開権限の分離をつなぐ必要があります。[Unit 42の調査報告（2025年11月更新を含む）](https://unit42.paloaltonetworks.com/npm-supply-chain-attack/) また、CircleCIの2023年の報告は、端末から盗まれた認証済みセッションや、稼働中に利用できる復号鍵の問題を示します。MFAや保存時暗号化だけで実行環境の侵害を防げるとは限りません。[CircleCIの当事者報告](https://circleci.com/blog/jan-4-2023-incident-report/)

悪性コードの混入と、正規ソフトウェアに元からある脆弱性の悪用は区別します。例えばLog4Shellは後者です。[Apacheの脆弱性情報](https://logging.apache.org/security.html) 名前の取り違え、公開権限の侵害、取得物の差替えは代表的な入口であり、ビルド基盤や開発ツールの侵害も残ります。以下の対策は各経路の成立条件を狭めるもので、組合せだけで全攻撃を防ぐ保証ではありません。

**確かめ方。** 自分たちの端末・CI・公開処理のうち、どこで外部コードが最初に動き、どの権限を持つかを追います。

詳しくは：[多層防御ガイド](supply-chain-defense.md)。

## 1. lifecycleスクリプトの無効化

依存を取得する許可と、依存が用意したコードを実行する許可を分けます。不要な準備処理は止め、必要な処理だけを対象の版・取得物と結び付けて審査します。設定は取得・メタデータ生成が始まる前に適用し、失敗したから全許可へ戻す運用にしません。

| 対象と確認資料 | 設定・運用の要点 | 残る実行経路 |
|---|---|---|
| [npm v11 config](https://docs.npmjs.com/cli/v11/using-npm/config/) | `ignore-scripts=true`の保存先を明示する。`npm config set`の既定はuser設定であり、project設定は`--location=project`で区別する | 明示的な`npm run`・`npm test`の主処理は動く。`allow-git=none`はGit依存の取得制限であり、全実行の禁止ではない |
| [pnpm 10.x settings](https://pnpm.io/10.x/settings) | 依存のbuild許可を確認する。`allowBuilds`は10.26.0で追加。未審査のbuild処理を含む依存で失敗させるなら`strictDepBuilds`も確認する | 許可した名前の将来版、project自身のスクリプト、後続のテストは別に判断する |
| [Bun lifecycle](https://bun.com/docs/pm/lifecycle) | 既定のtrusted listがある。`trustedDependencies`を明示した場合の置換と、空リスト・`--ignore-scripts`の範囲を区別する | 許可済みの処理と後続のアプリ実行は残る |
| [pip Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/)・[Build System Interface](https://pip.pypa.io/en/stable/reference/build-system/)（表示版26.2.2） | 配布wheelに限定する方針とhash照合を別に扱う。sourceのメタデータ生成も実行に含める | build isolationは依存環境の分離であり、OS権限の隔離ではない。wheelを後で読み込む際の実行も残る |

他言語でも実行点を確認します。Rubyは[拡張の準備処理](https://guides.rubygems.org/gems-with-extensions/)、Rustは[Cargoのbuild script](https://doc.rust-lang.org/cargo/reference/build-scripts.html)、.NETは[NuGetから取り込むMSBuildのprops/targets](https://learn.microsoft.com/en-us/nuget/concepts/msbuild-props-and-targets)などが対象です。lockを固定しても、それらの実行は止まりません。

**確かめ方。** メタデータ取得だけのつもりの操作でも未承認コードが動かないか、設定の上書きと許可済み依存の更新を確認します。

詳しくは：[DEPS-002](../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md) ／ [BUILD-001](../controls/records/build-security/psb-build-001-build-containment/README.md)。

## 2. クールダウン(最小リリース経過時間)

待機期間は、公開直後の情報不足を補うための時間です。正確な名前・版・取得元の公開時刻で判定し、時刻不明を十分古い版として扱いません。期間は更新の緊急性と組織の判断で決めます。次の7日相当の値は単位の比較例であり、推奨する一律の期間ではありません。

| 確認対象 | 設定と単位の例 |
|---|---|
| [npm CLI v11.10.0の定義](https://github.com/npm/cli/blob/v11.10.0/workspaces/config/lib/definitions/definitions.js) | `min-release-age=7`。数値、単位は日。`7d`ではない |
| [pnpm 10.x（10.16.0で追加）](https://pnpm.io/10.x/settings#minimumreleaseage) | `minimumReleaseAge: 10080`。数値、単位は分 |
| [Bun installの現行文書](https://bun.com/docs/pm/cli/install) | `--minimum-release-age 604800`。数値指定の単位は秒 |
| [Yarnの現行設定文書](https://yarnpkg.com/configuration/yarnrc#npmMinimalAgeGate) | `npmMinimalAgeGate: "7d"`。期間表現。利用版での対応は別途確認する |

[Dependabotのcooldown](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)や[RenovateのminimumReleaseAge](https://docs.renovatebot.com/configuration-options/#minimumreleaseage)は更新作成の制御です。手動install、別クライアント、既存lock、cache、公開時刻を持たない取得先への適用を推測しません。緊急例外は対象版・承認・期限を持たせ、通常条件を満たした結果と分けます。

**確かめ方。** Botが保留した版を手動取得したとき、最初の実行前にも止まるかを確認します。

詳しくは：[DEPS-001](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) ／ [DEPS-005](../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md)。

## 3. SemVerレンジの制御とバージョン固定

版の範囲を狭くすると、意図しない更新を減らせますが、範囲内の版が無害になるわけではありません。直接依存の指定に加え、解決した推移依存、取得先、取得物のhashをレビューし、通常ビルドでその入力を使います。開発依存も端末やCIで動くため保護対象です。製品に同梱されないことを、秘密や公開権限へ到達しない根拠にしません。

版の書式は製品ごとに読みます。[NuGetのVersion ranges](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning)では`1.2.3`は最低版の指定で、完全一致の範囲は`[1.2.3]`です。Goの`go.mod`は[Minimal version selection](https://go.dev/ref/mod#minimal-version-selection)に関わる要求を表すため、一つの直接依存を書いただけで全依存が固定されたとは扱いません。npmでもmanifestの範囲と[package-lockに記録する解決結果](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/)を分けます。

**確かめ方。** 直接依存の行を変えず推移依存だけが変わる場合や、開発依存の準備処理が追加される場合をレビュー対象にできるか確認します。

詳しくは：[DEPS-003](../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md) ／ [DEPS-004](../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)。

## 4. lockfileの厳格な運用

依存更新時は解決結果を変更してレビューし、通常ビルドでは承認済みのmanifest・lock・取得物を照合します。lockを作り直して不一致を解消した処理を、通常ビルドの成功にしません。書換え禁止、manifestとの整合、取得物の一致、準備処理の停止は別の条件です。

| 確認対象 | 保証と限界 |
|---|---|
| [npm ci v11](https://docs.npmjs.com/cli/v11/commands/npm-ci/) | manifestとの不一致を拒否しlockを更新しない。script停止は別設定。`npm install`にもlockを参照する動作があり、名称だけで比較しない |
| [uv project sync](https://docs.astral.sh/uv/concepts/projects/sync/) | `--locked`はlockの鮮度を確認し、不一致なら失敗する。`--frozen`はその鮮度確認を省略するため等価ではない |
| [Go modules reference](https://go.dev/ref/mod) | `go.sum`はchecksumの記録。依存の選択は`go.mod`等と合わせて判断する。`-mod=readonly`による更新制限と、`go mod verify`のcache検証は役割が違う |

同じhashでも、承認した内容自体が不正なら通ります。展開済みcache、OS別・optional依存、ローカルやVCSの依存など、選んだ方式で照合できない範囲も明示します。

**確かめ方。** manifestだけの変更、取得物の不一致、古い展開済みcacheで止まるかを確認します。

詳しくは：[DEPS-003](../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)。

## 5. lockfileインジェクション対策

lockfileの変更者が取得先と期待hashを同時に変更すると、別ファイルでもhash照合は成功します。承認済みの入力から何が変わったかを確認し、名前・版・取得元・hashを一緒にレビューします。許可したregistryの中にある不正なパッケージも残るため、hostの許可と内容の採用判断は分けます。

検査は、対象依存やPR内のスクリプトを動かす前に、独立して用意した信頼できる検査器で行います。npmの[root lifecycleの実行順序](https://docs.npmjs.com/cli/v11/using-npm/scripts/)から、root `preinstall`を依存インストール全体の前段とは見なせません。`ignore-scripts`でその検査自体が省略される構成も避けます。[package-lockのresolved・integrity](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/)を構造として読み、[lockfile-lint](https://github.com/lirantal/lockfile-lint)のhost・方式検査などを判断材料にできますが、同じ未審査の依存から検査器を先にinstallしては順序が逆になります。

Goでは、[既定の`sum.golang.org`と除外設定`GONOSUMDB`](https://go.dev/ref/mod#authenticating)を確認します。checksum照合は記録された配布物との一致のための材料であり、内容の無害性や社内の取得元方針を証明しません。

**確かめ方。** 無害な別ファイルへ取得先とhashを同時に差し替えた差分が、hashの成功だけで採用されないかを確認します。

詳しくは：[DEPS-004](../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md) ／ [依存更新ガイド](dependency-update-to-build.md)。

## 6. 新規依存+installスクリプトの検知

現在のbaseとheadの解決結果を構造として比較し、新しい推移依存、取得元の変更、準備処理の追加・変更をレビュー担当へ示します。名前・版・配布物に結び付いた情報を使い、最新版の情報でPR内の版を代用しません。開発用・optionalの依存も、その環境で実行されるなら対象です。

npmのlockには[`hasInstallScript`](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/)がありますが、フラグがないことだけで実行経路がないとは判断しません。取得できないmetadataや対応外の形式は未評価として残し、必要に応じて対象配布物を実行せず調べます。差分検知は重点レビューへの入口であり、実行の許可を自動で与えるものではありません。

**確かめ方。** manifestの直接依存名が増えない変更で、新規推移依存と既存依存の準備処理追加を拾えるか確認します。

詳しくは：[DEPS-004](../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md) ／ [依存更新ガイド](dependency-update-to-build.md)。

## 7. インストール前の事前監査ツール

ツールは、何を入力し、何を検出し、どこで使用を止めるかで選びます。

| 問い | 判断材料と限界 |
|---|---|
| 既に知られた脆弱性があるか | 名前・版とDBを照合する。未登録の悪意や、検査対象外の依存は分からない |
| 不審なコード・配布情報があるか | 対象配布物の静的解析やmetadataを使う。検出規則の対象と誤判定を確認し、指摘なしを無害と読まない |
| 拒否対象の取得を止められるか | 管理経路で遮断する。対象形式、直接取得の迂回、後日判明した版の追跡を確認する |
| 審査を終えるまで使わないか | 現在の差分に対する承認・拒否・未評価を実行／マージ条件へ接続する。通知だけとは区別する |

検査の前処理も実行経路です。[pip-auditのSecurity Model（mainの確認時点）](https://github.com/pypa/pip-audit#security-model)は、依存解決が`pip install`相当のコード実行を伴い得ると説明しています。`--fix`も入力を変更する操作で、読取りだけの監査ではありません。対象を実行しない照会方法を選ぶか、秘密と高い権限を渡さない環境に置きます。検査器自身の取得元・版・更新経路も管理します。

[GuardDogのv3ブランチのREADME（確認時点）](https://github.com/DataDog/guarddog/tree/v3)では、単一package・配布物等の`scan`と、requirements等に並ぶ依存の`verify`を区別します。操作に合ったサブコマンドと入力を選びます。[Takumi Guardの制限](https://shisho.dev/docs/t/guard/limitation/)も、すべての悪性版を事前遮断できる保証とはしません。aliasやラッパーの外からの取得にも同じ制御が届くかは別に確認します。

**確かめ方。** 監査・metadata収集の途中で対象コードが動く場合、検査対象外、DB取得失敗、途中終了を成功へ変えていないか確認します。

詳しくは：[依存更新ガイド](dependency-update-to-build.md) ／ [GOV-009](../controls/records/governance-operations/psb-gov-009-scanner-evidence-trust-boundary/README.md) ／ [DEPS-005](../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md)。

## 8. Provenanceアテステーションとnpm audit signatures

署名は「誰のどの主張を、どの成果物について確認したか」で読みます。利用側が期待する公開元・repository・生成経路と、実際に使用する取得物を結び付けます。正しい署名が付く不正コードもあり、出所の正当性と無害性は別です。

[`npm audit signatures`（v11文書）](https://docs.npmjs.com/cli/v11/commands/npm-audit/)は取得済み依存を対象に、registry署名や提供されたattestationを検証します。[v11.10.0の実装](https://github.com/npm/cli/blob/v11.10.0/lib/utils/verify-signatures.js)でも、全packageに来歴があるとは仮定していません。したがって、必要な来歴の欠落を拒否する方針と、期待する生成条件の照合を別に設けます。検査のためのinstallで先にscriptを動かさず、取得時の実行を止めた状態で検証し、使用可否を決めてから必要な処理を実行します。

[pnpm 10.xの`trustPolicy: no-downgrade`](https://pnpm.io/10.x/settings#trustpolicy)は、過去の公開版より信頼の証拠が弱くなる場合を扱う設定です。最初から来歴がないpackageにも来歴を一律要求するものとは区別し、除外設定も確認します。

**確かめ方。** 来歴なし、取得失敗、正しい署名だが別repository、検証後の別取得物という場合に、保護対象の使用が止まるか確認します。

詳しくは：[REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md) ／ [多層防御ガイド](supply-chain-defense.md)。

## 9. OIDC Trusted Publishing(長期トークンの排除)

Registry側で承認するCIのidentityと公開対象を限定し、その実行だけが短命の公開権限を取得できるようにします。workflowの変更・呼出し元・Environmentの審査と、公開前のビルドへの権限非付与も必要です。短命でも、取得したjob内の不正コードからは悪用され得ます。

| 一次資料と確認対象 | 設定・運用の要点 |
|---|---|
| [npm Trusted publishing](https://docs.npmjs.com/trusted-publishers/)（文書の前提はnpm 11.5.1以上・Node 22.14.0以上） | trusted publisherの登録は既存tokenや手動公開の自動廃止ではない。公開アクセスのtoken禁止設定と旧tokenの失効を別に行う |
| [PyPI Trusted publishers](https://docs.pypi.org/trusted-publishers/) | 認めたpublisherのidentityから短命tokenを得る仕組み。登録したworkflow等の条件と、別の公開経路を確認する |
| [crates.ioの公式説明（2025-07-11）](https://blog.rust-lang.org/2025/07/11/crates-io-development-update-2025-07/) | 認証用Actionで取得したtokenを`CARGO_REGISTRY_TOKEN`として渡す。古い記事のprovider対応範囲を現行の網羅表にしない |
| [NuGet Trusted publishing](https://learn.microsoft.com/en-us/nuget/nuget-org/trusted-publishing) | OIDCから一時API keyへ交換し、そのkeyで公開する。`dotnet nuget push`が無条件に自動認証するとは扱わない |

**確かめ方。** 別repository・branch・workflowからの交換と、旧token・手動公開の残存を確認します。

詳しくは：[CICD-006](../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md) ／ [REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)。

## 10. アカウント保護(2FA / Passkey)

公開者・管理者のログインにはフィッシングへの耐性を持つ認証方式を選び、復旧用メール、予備の認証器、連携identity、管理者による復旧も同じ権限への入口として管理します。アカウントを保護しても、既存sessionやAPI tokenが盗まれる経路は残ります。

Passkeyは同期可能なものと、特定の認証器に結び付くものを区別します。[W3C WebAuthn Level 3のbackup eligibility・backup state](https://www.w3.org/TR/webauthn-3/)を根拠に、すべてのPasskeyが同じ鍵保護・復旧特性を持つとは扱いません。サービスごとの必須認証・復旧・tokenの扱いを現在の設定で確認し、端末侵害で認証済みsessionを盗まれる経路には[CircleCIの事例](https://circleci.com/blog/jan-4-2023-incident-report/)のような別対策が必要です。

**確かめ方。** 通常ログインを強化しても、弱い復旧手段や古いsessionで公開権限を取り戻せないか確認します。

詳しくは：[SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) ／ [GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)。

## 11. プライベートレジストリプロキシ(Dependency Confusion対策)

社内の名前は承認した社内供給元だけから取得し、同名の公開packageへ解決されないようにします。proxy内のremote repositoryへの転送規則と、端末・CIからの直接接続を両方確認します。名前の予約は補助策であり、別名・別クライアント・直接URLの経路を閉じる代わりにはなりません。

[pip install文書](https://pip.pypa.io/en/stable/cli/pip_install/)は、`--extra-index-url`によるprivate package取得にdependency confusionの注意を示しています。社内indexを追加しただけで優先順位が保証されたとは扱いません。[Goのproxy・private module設定](https://go.dev/ref/mod#private-modules)では、`GOPROXY`のfallbackや`GONOPROXY`が別経路を作ります。`GONOSUMDB`はchecksum DBの除外であり、取得元の限定とは別です。npmのscope別設定なども、対象外の名前やクライアントを含む全経路の強制とは分けます。

**確かめ方。** 社内名と同名の公開候補、proxy停止、手動URL、cache利用で方針を迂回しないか確認します。

詳しくは：[DEPS-005](../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md) ／ [DEPS-001](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)。

## 12. ad-hoc実行の安全化 (npx / pipx / uvx / go run)

一時利用でも、名前・版・取得元と実行権限を確認します。審査済みのツールを用意し、取得・確認・実行の順序を分ける運用を選びます。取得ファイルを確認したら、再ダウンロードした別のbytesへ切り替えず、その対象を限定した権限で実行します。

[npm exec v11](https://docs.npmjs.com/cli/v11/commands/npm-exec/)の`--no`／`yes=false`は不足packageのinstall要求への否定です。既存のローカルCLI等の実行を禁止する機能ではなく、`ignore-scripts`もCLI本体の実行を止めません。[uv toolの環境分離](https://docs.astral.sh/uv/concepts/tools/)や[Python venv](https://docs.python.org/3/library/venv.html)は依存環境の分離です。pipx等で別環境へ入れても、そのプロセスへ渡るファイル・環境変数・通信権限は別に制限します。[版付きの`go run`](https://pkg.go.dev/cmd/go#hdr-Compile_and_run_Go_program)は現在のprojectの`go.mod`を使わずに動くため、projectの審査で承認済みと推測しません。

**確かめ方。** 未導入・cache済み・ローカル導入済みの各経路で、何が取得され何が実行されるか確認します。

詳しくは：[DEPS-005](../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md) ／ [DEPS-002](../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md) ／ [BUILD-001](../controls/records/build-security/psb-build-001-build-containment/README.md)。

## 13. シークレットの保護(.envファイルの扱い)

秘密を安全に保管することと、その値をどのプロセスへ渡すかは別の判断です。参照だけを設定ファイルへ置く方式でも、実行時に環境変数やファイルへ値を展開すれば、受け取ったコードは読めます。[1Passwordの`op run`](https://www.1password.dev/cli/reference/commands/run)も、参照を解決して子プロセスの環境へ渡す方式です。出力のマスクは、受け取ったコードによる読取りや外部送信の禁止ではありません。

依存の取得・検査・ビルドには不要な署名鍵・公開用token・本番秘密を渡しません。必要な操作だけに、対象を限定した短命の権限を渡します。読み出せる秘密、別の秘密を取得できる認証経路、子プロセスへの継承、ログや一時ファイルへのコピーを確認します。`.gitignore`はGitへの追加を避ける補助であり、端末上の読取りを拒否しません。漏えいした値は削除だけでなく失効と利用履歴調査へつなぎます。

**確かめ方。** 実秘密を使わず、環境変数・一時ファイル・読取り専用mountに置いた無害な目印へ実行コードが到達できるか確認します。

詳しくは：[SOURCE-007](../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md) ／ [BUILD-001](../controls/records/build-security/psb-build-001-build-containment/README.md)。

## 14. Dev Container / サンドボックス開発

コンテナの外へ出られなくても、渡した秘密や接続先は使われます。開発用環境へ渡すdirectory、環境変数、SSH agent、Docker等の管理socket、cloud metadata、共有cacheを洗い出し、不要なものを渡しません。[Dockerのread-only bind mount](https://docs.docker.com/engine/storage/bind-mounts/)は書込みを制限するもので、秘密ファイルの読取りを防ぎません。

通信先とhostへのアクセスは、実行されるコード自身が解除できない外側の制御で絞ります。共有cacheや成果物を介して後続jobへ不正な状態が残らないようにし、初期化・セットアップ処理が制限の適用前にhostで動かないかも確認します。OS環境の分離、権限の縮小、通信の制限、実行後の廃棄を、それぞれ確認できる構成を選びます。

**確かめ方。** 秘密の目印、hostのsocket、共有cache、許可外の通信への到達を、準備処理から終了まで確認します。

詳しくは：[BUILD-001](../controls/records/build-security/psb-build-001-build-containment/README.md) ／ [cache・runnerの設計](ci-state-and-runner-lifecycle.md) ／ [多層防御ガイド](supply-chain-defense.md)。

## 15. 依存ツリーの削減

使っていない依存や機能を外し、実行する公開者のコードと更新の判断を減らします。削減の候補は、利用箇所、実行時点、必要な権限、推移依存、保守状況、代替による互換性と保守負担で選びます。特に暗号・認証などを件数削減のためだけに自作しません。

件数は棚卸しの目安であり、同じ公開者・ビルド基盤に集中する依存や、高権限で動く少数のツールを評価する代わりにはなりません。[OpenSSF ScorecardのREADME（確認時点）](https://github.com/ossf/scorecard)も、検査をheuristicsとして扱い、総合点だけでは個別の状態が分からないと説明しています。点数・人気・更新頻度は調査の入口に留めます。削除後は必要な動作と、別の依存・外部通信で機能が復活していないことを確認します。

**確かめ方。** 不要と判断した依存が対象OSや開発・ビルド工程で再導入されないか、代替が必要以上の権限を増やさないか確認します。

詳しくは：[DEPS-004](../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)。

## 16. ネットワーク監視とIOCフィードの運用

必要な通信を許す方針と、何が実際に通信したかを記録する仕組みを組み合わせます。パッケージ管理ツールのindex設定だけでは、動き始めたコードの通信先を制限できません。実行環境の外側で制限し、名前解決・redirect・proxy以外の経路と、許可された共有サービスへの情報送信も考慮します。

IOCは発行元、対象となる指標、取得時刻、適用範囲、訂正・失効を管理し、古い指標や取得失敗を「該当なし」にしません。[CISA KEV](https://github.com/cisagov/kev-data)は悪用が確認された脆弱性のcatalogで、C2 domainやpackage hashの一覧とは役割が異なります。EDRや通信ログは、観測できた端末・期間と動作状態を合わせて記録します。通信が見えない場合も、遮断に成功したのか、記録が欠けたのかを分けます。

**確かめ方。** 無害な通信で許可・拒否・記録を確認し、監視停止や対象外の端末を未観測として扱えるか確認します。

詳しくは：[CONTAINER-006](../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md) ／ [GOV-011](../controls/records/governance-operations/psb-gov-011-security-event-evidence/README.md)。

## 17. SBOM(ソフトウェア部品表)の生成と管理

SBOMには、何をどの時点で観測したかを示し、source revision、build、成果物digest、稼働先へ結び付けます。配布物に含まれない開発・ビルド依存も、端末・CI侵害の調査には必要です。形式は、受け手が扱える版、識別子、依存関係、必要な証拠の保持で選びます。[CycloneDXのBOM-Link](https://cyclonedx.org/capabilities/bomlink/)のような参照機能があっても、対応する対象の収集と維持は利用者の作業です。

生成器、照合器、集約基盤を役割で分けます。例えば[OSV-Scanner v2の出力文書](https://google.github.io/osv-scanner/output/)にはSPDX・CycloneDX出力もありますが、出力形式の対応と、調査に必要な全依存を収集できたことは別です。[Dependency-Track](https://github.com/DependencyTrack/dependency-track)へ登録しただけで、収集範囲・分析完了・脆弱性情報の鮮度・稼働先の対応まで確認済みとはしません。

[VEX](https://cyclonedx.org/capabilities/vex/)は、特定の製品・版と脆弱性に対する判断を根拠付きで伝えます。発行者、対象、理由、証拠、判断時点を確認して受け入れ、構成や情報が変われば再評価します。抑制した指摘を検査対象外や未調査と混ぜません。Log4Shellの条件は[Apacheの情報](https://logging.apache.org/security.html)に照らし、アプリが明示的にJNDIを呼ばないことだけで除外しません。

**確かめ方。** 同じ名前でも別digestの成果物、開発依存が抜けたSBOM、処理待ちの登録、古いVEXから誤って影響なしにしないか確認します。

詳しくは：[REL-003](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md) ／ [SBOMから影響調査へ](sbom-to-vulnerability-response.md)。

## 18. YARA / 静的解析によるパッケージスキャン

配布物を実行せず調べ、検査したbytes、検査器・ルールの版、対象形式、未検査の内容を記録します。[GuardDogのv3ブランチの文書](https://github.com/DataDog/guarddog/tree/v3)にあるpackage・archive・directoryのスキャンを使う場合も、読めない形式、難読化、後から取得するコードなどを「指摘なし」へ含めません。指摘は採用保留と調査につなぎ、未検出を無害性の証明にしません。

取得の前処理がコードを動かす場合があります。[pipのbuild system文書](https://pip.pypa.io/en/stable/reference/build-system/)に照らし、推移依存を取得しない指定だけでsourceのmetadata生成まで止まるとは判断しません。検査器自身も未信頼のarchiveやmetadataを処理するため、秘密と高い権限を渡さず、対象を実行する動的解析はさらに独立した環境で行います。

**確かめ方。** 途中で解析できなくなった配布物や、検査規則の対象外が合格へ変わらないか確認します。

詳しくは：[DEPS-002](../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md) ／ [GOV-009](../controls/records/governance-operations/psb-gov-009-scanner-evidence-trust-boundary/README.md)。

## 19. CIパイプラインのハードニング

CIで読み込むAction・plugin・wrapper・containerを、審査した出所と変更不能な参照へ結び付けます。[GitHub Actionsの公式ガイダンス](https://docs.github.com/en/actions/reference/security/secure-use)ではfull commit SHAでの固定を案内しています。固定したコードの中から取得する別の実行物も確認し、更新時のレビューと、問題が判明した版の利用停止を用意します。

未信頼PRのコードを、公開・署名・配備権限を持つjobで実行しません。`pull_request_target`等のイベント名だけで判断せず、何をcheckout・実行し、どのtoken・secret・cacheを使うかを追います。jobの権限を必要な範囲にし、依存の準備を行うsetup処理より前に実行方針を適用します。runnerを再利用する場合は前の実行が残した状態も境界に含めます。

[Gradle Wrapper文書](https://docs.gradle.org/current/userguide/gradle_wrapper.html)の`distributionSha256Sum`は配布ZIPの照合で、Wrapper JARの正当性確認は別です。[Mavenのoffline指定](https://maven.apache.org/ref/3-LATEST/maven-embedder/cli.html)によるoffline動作と、社内Nexusなどの取得先の設定を区別します。どちらも実行したplugin全体に対するOSの通信禁止とは扱いません。

**確かめ方。** 参照先の変更、権限付きjobへの未信頼入力、検査前のsetup実行、共有cache経由の影響を確認します。

詳しくは：[CICD-001](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md) ／ [CICD-004](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md) ／ [CICD-005](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) ／ [PRから公開への設計](pull-request-to-release-build.md)。

## 20. コンテナイメージのサプライチェーン

baseと配布imageを審査したdigestへ結び付け、更新時に差分を判断します。[Dockerのdigest固定の説明](https://docs.docker.com/build/building/best-practices/)に沿って、固定後も修正版への更新を計画します。baseを固定しても、その上のbuild処理が取得・実行する依存は別に管理します。

[Cosignの検証](https://docs.sigstore.dev/cosign/verifying/verify/)では、署名の正当性に加え、信頼するidentityとissuer、対象digestを確認します。期待値を広すぎる正規表現で許可せず、必要な来歴の欠落・検証不能も使用を止める条件へ接続します。検証後に可変tagで取得し直さず、実際に使うdigestとの結び付きを保ちます。複数architectureのimageは、検証対象と実行される対象の関係も確認します。

小さなimageや非rootは攻撃に使える機能・権限を減らしますが、残ったプログラムからのファイル読取り・通信は可能です。実行権限、mount、通信先は別に絞ります。

**確かめ方。** 別identityの有効な署名、来歴欠落、検証後のtag変更で実行を許さないか確認します。

詳しくは：[REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md) ／ [CONTAINER-001](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md) ／ [コンテナの実行から初動まで](container-deployment-to-response.md)。

## 21. IDE拡張機能・開発ツール

拡張の出所・版・必要性と実行場所を審査し、許可外の導入、更新、手動配布による迂回を確認します。[VS Code 1.96以降の`extensions.allowed`と組織policy](https://code.visualstudio.com/docs/enterprise/extensions)は、導入・有効化を制限する機能です。ただしローカルVSIXの自己申告identityだけでは出所を検証できず、ローカルファイルの改変や実行時権限も別問題です。

[Workspace Trust](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust)は悪意ある拡張そのものの実行を防ぐsandboxではありません。[Extension Host](https://code.visualstudio.com/api/advanced-topics/extension-host)にはlocal・web・remoteの違いがあり、containerを使っていてもすべてがremoteで動くとは推測しません。実行場所ごとのファイル・秘密・socket・通信への到達を確認し、問題の版を無効にして更新・再起動後も読み込まれないことを確かめます。

**確かめ方。** 手動VSIX、許可済み拡張の更新、local host側に残る処理、失効後の再読込みを確認します。

詳しくは：[SOURCE-001](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md) ／ [SOURCE-007](../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md)。

## 22. AIコーディング支援・MCPサーバ

開発agentが読み込むskills・plugin・MCP serverも、実行物と操作権限の組として管理します。出所、版またはdigest、起動コマンドと引数、接続先、渡す認証情報を審査し、更新で変われば再確認します。repositoryや外部文書に書かれた命令だけで権限を広げず、実際の読取り・書込み・通信・公開操作を外側で制限します。

例えば[Claude Codeのsandbox文書](https://code.claude.com/docs/en/sandboxing)は、shellとその子プロセスの境界と、外側で動くMCP server・hook・ファイル操作等を区別しています。製品内の一機能を有効にしただけで、すべての経路を制限したとは扱いません。[MCPのSecurity Best Practices（2025-11-25版への参照）](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)にあるtokenの宛先確認やtoken passthroughの禁止も、OSの隔離とは別の境界です。

承認時には実際の操作対象・送信先・権限を示し、停止時にはプロセスだけでなくsession、再起動条件、保存した認証情報、後続処理を確認します。出力されたコードや設定が正しいかのレビューも残します。

**確かめ方。** 拡張の差替え、外部文書からの命令、承認後の引数変更、shell以外の操作、停止後のsession利用を確認します。

詳しくは：[AI-002](../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md) ／ [AI-003](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md) ／ [AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md) ／ [作業開始から停止までの設計](development-agent-task-to-stop.md)。

## 23. インシデント対応ランブック

不正な依存の実行が疑われたら、対応責任者を決め、封じ込め・認証情報の失効・証拠保全・影響調査を並行して進めます。順序は、進行中の被害、停止の影響、失われる証拠で決め、全容の判明や保全完了を一律に待ちません。[NIST SP 800-61r3（2025-04）](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf)の対応・証拠保全・復旧を、この判断へ接続する本ガイドの対応方針です。

| 担当する作業 | 初動で決めること・次へ渡すもの |
|---|---|
| 端末・CI・配布の封じ込め | 対象の隔離、疑わしい版の取得・公開停止、継続させる必要がある業務と代替経路 |
| 認証情報への対応 | 読まれ得た値と権限、旧token・派生session・再発行条件の停止。新しい値は信頼できる別環境から扱う |
| 証拠保全と調査 | 観測時刻、対象bytes・digest、必要なログ、実施操作と理由、収集できなかった範囲。秘密そのものは通常の記録へ複製しない |
| 再構築と再開 | 信頼を回復した環境と承認済み入力から再構築し、汚染したrunner・cache等を再利用しない。新成果物の稼働と旧版の非稼働を確認する |

通知は、適用法令、契約、影響を受ける相手、判断責任者で条件を決めます。例えば[EDPBのGDPR 33・34条の説明](https://www.edpb.europa.eu/sme/assess-the-risks/data-breaches_en)では、データ管理者（controller）の監督機関への通知と本人への連絡は条件が異なります。GDPRの対象となる個人データ侵害では、個人の権利・自由へのリスクが生じる可能性が低い場合を除き、不当な遅延なく、可能なら覚知から72時間以内に監督機関へ通知し、遅れる場合は理由を示します。本人への連絡は高リスク等の条件に基づき、不当な遅延なく行うものです。全セキュリティ事案の一律の時間割に転用しません。

**確かめ方。** 全容が未確定でも停止・失効の担当が動けるか、保全に失敗した範囲が残るか、再起動で旧版へ戻らないかを机上で確認します。

詳しくは：[GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md) ／ [GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md) ／ [対応・再開の設計](security-signal-to-response.md)。

## 24. ブラストレイディアス評価

問題の名前・版・取得物から、取得した端末、実行したCI、作られた成果物、配布・稼働先を調べます。実行時期と、その時点で到達できた秘密・公開権限・network・共有状態を確認します。製品に同梱されない開発依存も対象です。結果は「影響候補」「調べた範囲では該当なし」「未調査・調査不能」に分けます。

[Dependency-Track](https://github.com/DependencyTrack/dependency-track)のportfolio検索で調べられるのは登録・解析した対象です。[OSV-Scanner v2](https://google.github.io/osv-scanner/usage/)は渡した入力から部品を抽出し脆弱性へ照合するため、別途全対象の収集が必要です。[対応形式の文書](https://google.github.io/osv-scanner/supported-languages-and-lockfiles/)にも、manifestから推測した版や対象外の依存に限界があります。未信頼projectを調査するために、そのbuildや依存解決を高権限で再実行しません。

[aws-nuke](https://github.com/ekristen/aws-nuke)はAWS resourceの削除を目的とするツールで、認証情報棚卸しの推薦には適しません。[AWS IAM credential report](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html)のような状態の照会を用いる場合も、対象account・user・認証情報の種類と観測時刻を明示し、全sessionや全権限の調査を代替しません。

**確かめ方。** 検索権限不足、未取得ページ、停止中の端末、未登録の成果物、古いSBOM、ログ欠測を結果から消さないか確認します。

詳しくは：[GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md) ／ [GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)。

## 対策一覧と着手順

自分たちが外部コードを使う経路と、他者へコードを公開する経路を分けて対策します。

| 役割 | まず決めること | この対策の後にも残ること |
|---|---|---|
| 利用側の取得・更新（1〜8・11〜12・15・18章） | 取得元、待機条件、承認する差分、実行前の検査、固定した入力 | 正規の取得元から来る不正コード、検査の見逃し、手動取得の迂回 |
| 実行環境（13〜14・16・19〜22章） | 渡す秘密・権限・通信、外側の強制、共有状態の扱い | 必要な権限の悪用、許可先への送信、観測できない経路 |
| 公開側（9〜10・19〜20章） | 公開identity、workflowの変更管理、旧公開経路の停止、配布物の検証材料 | 正規job自体の侵害。利用側の無害性確認を代行するわけではない |
| 発見後の対応（17・23〜24章） | 依存・成果物・稼働先の対応、停止・失効・保全・復旧の担当 | 台帳・記録の欠測、調査対象外。復旧と無影響は別の結論 |

npm利用者は、まず使用版と実効設定を確認し、不要なscriptの停止、待機条件、通常ビルドでのlock照合を適用できるか判断します。その上で、取得先を含む変更審査と、必要な署名・来歴を使用前の条件へ接続します。設定の存在で完了とせず、許可・拒否・判定不能の代表経路を確認します。公開者はこれに加えて、公開権限と復旧経路を見直します。

**確かめ方。** [多層防御ガイド](supply-chain-defense.md)を入口に、対策を通過した後の権限と対応まで確認します。

詳しくは：[多層防御ガイド](supply-chain-defense.md) ／ [分析レンズ](../docs/ANALYSIS_LENSES.md)。
