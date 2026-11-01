# サプライチェーン攻撃の対策：24章の改訂案

開発者・開発基盤担当者・プロダクトセキュリティ担当者が、依存の取得から実行、公開、侵害後の対応まで、どこで何を止めるか判断するための編集案です。守る対象は端末・CIの秘密と権限、ソース、配布成果物、稼働環境です。依存の公開者や公開アカウントを奪った攻撃者に加え、検査の欠測や設定の迂回も扱います。

[原資料と取得本文の識別情報・採否](../README.md#ref-supply-chain-countermeasures-001)を正本とし、ここでは背景、原資料の1〜24章、末尾の順序を維持します。**「差し替え文」は本PJが書いた修正文であり、原文の引用ではありません。** 製品仕様は各章の一次資料へ接続し、設計上の推奨は本PJの解釈として区別します。章内のコード表記は修正対象の設定や用語を示すもので、新しい導入手順・実装例ではありません。

一次資料の確認日は、別記しない限り**2026-11-01**です。版を固定できた資料はその版、更新される公式文書は確認日を基準にします。後者は`re-review-required`とし、クライアント更新、既定値・設定の優先順位、認証方式、検査対象の変更時に再確認します。最小対応版が確認できない機能を「全バージョンで利用可能」とは扱いません。ここでの確認は文書・公開ソースの読解であり、各章の診断項目を実環境で実施した結果ではありません。

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
- [末尾の対策一覧](#末尾の対策一覧)
- [採用しない記述と再確認の条件](#採用しない記述と再確認の条件)

## 背景

**編集判断。** 依存更新を入口とする侵害の説明は維持します。事件は成立経路の異なる代表例に絞り、被害規模・ダウンロード数と実際の感染数を区別します。Axiosの滞在時間が章により異なる記述、Top.ggの潜在利用者数を被害数と読める表現、Mavenで事件が少ない原因を署名へ帰する説明は削除します。SolarWindsをPyPIの事例に置かず、Log4Shellを悪性パッケージの混入と同一視しません。strong_passwordの実行方式、BirsanのMaven固有の経路など、一次資料で今回裏付けていない細部は未確認として推奨の根拠から外します。

**差し替え文。** 普段使っているパッケージの更新でも、追加された依存や準備処理が端末・CIの権限で動くと、製品を起動する前に秘密が盗まれます。2026年3月31日のAxiosの不正な版（1.14.1、0.30.4）では、追加依存`plain-crypto-js`のインストール処理が実行経路になりました。親パッケージの主要コードだけを見ても判断できない例です。[Microsoftの調査報告（2026-04-01）](https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/)

2025年のShai-Huludの調査では、依存の準備処理から認証情報を盗み、その公開権限で別パッケージへ広がる経路が報告されています。取得時の対策と公開権限の分離をつなぐ必要があります。[Unit 42の調査報告（2025年11月更新を含む）](https://unit42.paloaltonetworks.com/npm-supply-chain-attack/) また、CircleCIの2023年の報告は、端末から盗まれた認証済みセッションや、稼働中に利用できる復号鍵の問題を示します。MFAや保存時暗号化だけで実行環境の侵害を防げるとは限りません。[CircleCIの当事者報告](https://circleci.com/blog/jan-4-2023-incident-report/)

悪性コードの混入と、正規ソフトウェアに元からある脆弱性の悪用は区別します。例えばLog4Shellは後者です。[Apacheの脆弱性情報](https://logging.apache.org/security.html) 名前の取り違え、公開権限の侵害、取得物の差替えは代表的な入口であり、ビルド基盤や開発ツールの侵害も残ります。以下の対策は各経路の成立条件を狭めるもので、組合せだけで全攻撃を防ぐ保証ではありません。

**確かめ方・PJ反映。** 自分たちの端末・CI・公開処理のうち、どこで外部コードが最初に動き、どの権限を持つかを追います。全体の入口は[多層防御ガイド](../../engineering/supply-chain-defense.md)。事件数を新しいControlや効果の数値へ変換しません。

## 1. lifecycleスクリプトの無効化

**編集判断。** 不要な自動実行を止める方針は維持します。npmの設定を一律に「グローバル」と呼ぶ記述、Bunが全依存のスクリプトを既定で止める説明、言語間で同等の停止オプションがあるような表は変更します。Rubyの依存解決省略やlock固定を拡張ビルドの禁止と見なす例は外します。

**差し替え文。** 依存を取得する許可と、依存が用意したコードを実行する許可を分けます。不要な準備処理は止め、必要な処理だけを対象の版・取得物と結び付けて審査します。設定は取得・メタデータ生成が始まる前に適用し、失敗したから全許可へ戻す運用にしません。

| 対象と確認資料 | 修正する説明 | 残る実行経路 |
|---|---|---|
| [npm v11 config](https://docs.npmjs.com/cli/v11/using-npm/config/) | `ignore-scripts=true`の保存先を明示する。`npm config set`の既定はuser設定であり、project設定は`--location=project`で区別する | 明示的な`npm run`・`npm test`の主処理は動く。`allow-git=none`はGit依存の取得制限であり、全実行の禁止ではない |
| [pnpm 10.x settings](https://pnpm.io/10.x/settings) | 依存のbuild許可を確認する。`allowBuilds`は10.26.0で追加。未審査のbuild処理を含む依存で失敗させるなら`strictDepBuilds`も確認する | 許可した名前の将来版、project自身のスクリプト、後続のテストは別に判断する |
| [Bun lifecycle](https://bun.com/docs/pm/lifecycle) | 既定のtrusted listがある。`trustedDependencies`を明示した場合の置換と、空リスト・`--ignore-scripts`の範囲を区別する | 許可済みの処理と後続のアプリ実行は残る |
| [pip Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/)・[Build System Interface](https://pip.pypa.io/en/stable/reference/build-system/)（表示版26.2.2） | 配布wheelに限定する方針とhash照合を別に扱う。sourceのメタデータ生成も実行に含める | build isolationは依存環境の分離であり、OS権限の隔離ではない。wheelを後で読み込む際の実行も残る |

他言語でも実行点を確認します。Rubyは[拡張の準備処理](https://guides.rubygems.org/gems-with-extensions/)、Rustは[Cargoのbuild script](https://doc.rust-lang.org/cargo/reference/build-scripts.html)、.NETは[NuGetから取り込むMSBuildのprops/targets](https://learn.microsoft.com/en-us/nuget/concepts/msbuild-props-and-targets)などが対象です。lockの固定だけを、それらの実行禁止と説明しません。

**確かめ方・PJ反映。** メタデータ取得だけのつもりの操作でも未承認コードが動かないか、設定の上書きと許可済み依存の更新を確認します。[DEPS-002](../../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md)へ検査・情報収集時の実行を補足し、必要な実行の隔離は[BUILD-001](../../controls/records/build-security/psb-build-001-build-containment/README.md)へ渡します。

## 2. クールダウン(最小リリース経過時間)

**編集判断。** 公開直後の採用を待つ方針は維持します。npmの`7d`指定を訂正し、各製品の単位を分けます。一定期間で必ず悪性版が発見される説明と、プロキシ・更新Botなら待機を強制できるという一括説明は削除します。

**差し替え文。** 待機期間は、公開直後の情報不足を補うための時間です。正確な名前・版・取得元の公開時刻で判定し、時刻不明を十分古い版として扱いません。期間は更新の緊急性と組織の判断で決めます。次の7日相当の値は単位の比較例であり、推奨する一律の期間ではありません。

| 確認対象 | 設定と単位の例 |
|---|---|
| [npm CLI v11.10.0の定義](https://github.com/npm/cli/blob/v11.10.0/workspaces/config/lib/definitions/definitions.js) | `min-release-age=7`。数値、単位は日。`7d`ではない |
| [pnpm 10.x（10.16.0で追加）](https://pnpm.io/10.x/settings#minimumreleaseage) | `minimumReleaseAge: 10080`。数値、単位は分 |
| [Bun installの現行文書](https://bun.com/docs/pm/cli/install) | `--minimum-release-age 604800`。数値指定の単位は秒 |
| [Yarnの現行設定文書](https://yarnpkg.com/configuration/yarnrc#npmMinimalAgeGate) | `npmMinimalAgeGate: "7d"`。期間表現。利用版での対応は別途確認する |

[Dependabotのcooldown](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)や[RenovateのminimumReleaseAge](https://docs.renovatebot.com/configuration-options/#minimumreleaseage)は更新作成の制御です。手動install、別クライアント、既存lock、cache、公開時刻を持たない取得先への適用を推測しません。緊急例外は対象版・承認・期限を持たせ、通常条件を満たした結果と分けます。

**確かめ方・PJ反映。** Botが保留した版を手動取得したとき、最初の実行前にも止まるかを確認します。[DEPS-001](../../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)と[DEPS-005](../../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md)に既にある診断項目を使います。

## 3. SemVerレンジの制御とバージョン固定

**編集判断。** 更新を明示的に審査する狙いは維持します。`~`なら安全、開発依存は固定の優先度が低い、直接依存の版だけで全入力が固定される、という読め方を取り除きます。NuGetの単一バージョン表記を完全一致とする例は訂正します。

**差し替え文。** 版の範囲を狭くすると、意図しない更新を減らせますが、範囲内の版が無害になるわけではありません。直接依存の指定に加え、解決した推移依存、取得先、取得物のhashをレビューし、通常ビルドでその入力を使います。開発依存も端末やCIで動くため保護対象です。製品に同梱されないことを、秘密や公開権限へ到達しない根拠にしません。

版の書式は製品ごとに読みます。[NuGetのVersion ranges](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning)では`1.2.3`は最低版の指定で、完全一致の範囲は`[1.2.3]`です。Goの`go.mod`は[Minimal version selection](https://go.dev/ref/mod#minimal-version-selection)に関わる要求を表すため、一つの直接依存を書いただけで全依存が固定されたとは扱いません。npmでもmanifestの範囲と[package-lockに記録する解決結果](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/)を分けます。

**確かめ方・PJ反映。** 直接依存の行を変えず推移依存だけが変わる場合や、開発依存の準備処理が追加される場合をレビュー対象にできるか確認します。固定と照合は[DEPS-003](../../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)、利用範囲による見落としは[DEPS-004](../../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)へ反映します。

## 4. lockfileの厳格な運用

**編集判断。** lockfileの管理と通常ビルドでの書換え禁止は維持します。`npm install`が常にlockを無視する説明、`uv --frozen`と`--locked`の同一視、Goの`go.sum`を完全なlockとする表を変更します。Poetryの`--sync --no-update`など対象版を確認できていないコマンドは推薦例から外します。

**差し替え文。** 依存更新時は解決結果を変更してレビューし、通常ビルドでは承認済みのmanifest・lock・取得物を照合します。lockを作り直して不一致を解消した処理を、通常ビルドの成功にしません。書換え禁止、manifestとの整合、取得物の一致、準備処理の停止は別の条件です。

| 確認対象 | 記述する保証と限界 |
|---|---|
| [npm ci v11](https://docs.npmjs.com/cli/v11/commands/npm-ci/) | manifestとの不一致を拒否しlockを更新しない。script停止は別設定。`npm install`にもlockを参照する動作があり、名称だけで比較しない |
| [uv project sync](https://docs.astral.sh/uv/concepts/projects/sync/) | `--locked`はlockの鮮度を確認し、不一致なら失敗する。`--frozen`はその鮮度確認を省略するため等価ではない |
| [Go modules reference](https://go.dev/ref/mod) | `go.sum`はchecksumの記録。依存の選択は`go.mod`等と合わせて判断する。`-mod=readonly`による更新制限と、`go mod verify`のcache検証は役割が違う |

同じhashでも、承認した内容自体が不正なら通ります。展開済みcache、OS別・optional依存、ローカルやVCSの依存など、選んだ方式で照合できない範囲も明示します。

**確かめ方・PJ反映。** manifestだけの変更、取得物の不一致、古い展開済みcacheで止まるかを確認します。[DEPS-003](../../controls/records/dependency-security/psb-deps-003-dependency-artifact-identity/README.md)の既存項目を使い、取得元とhashの同時変更は次章の採用審査へ渡します。

## 5. lockfileインジェクション対策

**編集判断。** `resolved`などの取得先も審査する提案は維持します。rootの`preinstall`へ検査を置けば依存の実行前に止まる構成、HTTPSやhash一致だけで改ざんを排除できる説明、pnpmなら一般に問題がないという比較は削除します。

**差し替え文。** lockfileの変更者が取得先と期待hashを同時に変更すると、別ファイルでもhash照合は成功します。承認済みの入力から何が変わったかを確認し、名前・版・取得元・hashを一緒にレビューします。許可したregistryの中にある不正なパッケージも残るため、hostの許可と内容の採用判断は分けます。

検査は、対象依存やPR内のスクリプトを動かす前に、独立して用意した信頼できる検査器で行います。npmの[root lifecycleの実行順序](https://docs.npmjs.com/cli/v11/using-npm/scripts/)から、root `preinstall`を依存インストール全体の前段とは見なせません。`ignore-scripts`でその検査自体が省略される構成も避けます。[package-lockのresolved・integrity](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/)を構造として読み、[lockfile-lint](https://github.com/lirantal/lockfile-lint)のhost・方式検査などを判断材料にできますが、同じ未審査の依存から検査器を先にinstallしては順序が逆になります。

Goについては、`GOSUMDB=on`を削除し、[既定の`sum.golang.org`と除外設定`GONOSUMDB`](https://go.dev/ref/mod#authenticating)を説明します。checksum照合は記録された配布物との一致のための材料であり、内容の無害性や社内の取得元方針を証明しません。

**確かめ方・PJ反映。** 無害な別ファイルへ取得先とhashを同時に差し替えた差分が、hashの成功だけで採用されないかを確認します。[DEPS-004](../../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)へ診断項目を追加し、[依存更新ガイド](../../engineering/dependency-update-to-build.md)へ検査器と初回実行の順序を反映します。

## 6. 新規依存+installスクリプトの検知

**編集判断。** 少数の重要な変更へレビューを集中する狙いは維持します。新規の直接依存だけを拾う行単位のgrepと、版を指定しない`npm view`で対象更新を評価する例を外します。新規依存に限らず、既存依存の更新で実行処理が追加される場合も対象にします。

**差し替え文。** 現在のbaseとheadの解決結果を構造として比較し、新しい推移依存、取得元の変更、準備処理の追加・変更をレビュー担当へ示します。名前・版・配布物に結び付いた情報を使い、最新版の情報でPR内の版を代用しません。開発用・optionalの依存も、その環境で実行されるなら対象です。

npmのlockには[`hasInstallScript`](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/)がありますが、フラグがないことだけで実行経路がないとは判断しません。取得できないmetadataや対応外の形式は未評価として残し、必要に応じて対象配布物を実行せず調べます。差分検知は重点レビューへの入口であり、実行の許可を自動で与えるものではありません。

**確かめ方・PJ反映。** manifestの直接依存名が増えない変更で、新規推移依存と既存依存の準備処理追加を拾えるか確認します。[DEPS-004](../../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)と[依存更新ガイド](../../engineering/dependency-update-to-build.md)へ反映します。すべての静的差分を既存GitHub実装例が検出すると主張しません。

## 7. インストール前の事前監査ツール

**編集判断。** インストール前に判断材料を集める提案は維持します。「未知攻撃への強さ」「誤検知コスト」の製品ランキングは、共通の評価条件・測定結果がないため削除します。ツールを各段階へ一つずつ入れることを完了条件にせず、必要な検査と止める場所を先に決めます。

**差し替え文。** ツールは、何を入力し、何を検出し、どこで使用を止めるかで選びます。

| 問い | 判断材料と限界 |
|---|---|
| 既に知られた脆弱性があるか | 名前・版とDBを照合する。未登録の悪意や、検査対象外の依存は分からない |
| 不審なコード・配布情報があるか | 対象配布物の静的解析やmetadataを使う。検出規則の対象と誤判定を確認し、指摘なしを無害と読まない |
| 拒否対象の取得を止められるか | 管理経路で遮断する。対象形式、直接取得の迂回、後日判明した版の追跡を確認する |
| 審査を終えるまで使わないか | 現在の差分に対する承認・拒否・未評価を実行／マージ条件へ接続する。通知だけとは区別する |

検査の前処理も実行経路です。[pip-auditのSecurity Model（mainの確認時点）](https://github.com/pypa/pip-audit#security-model)は、依存解決が`pip install`相当のコード実行を伴い得ると説明しています。`--fix`も入力を変更する操作で、読取りだけの監査ではありません。対象を実行しない照会方法を選ぶか、秘密と高い権限を渡さない環境に置きます。検査器自身の取得元・版・更新経路も管理します。

[GuardDogのv3ブランチのREADME（確認時点）](https://github.com/DataDog/guarddog/tree/v3)では、単一package・配布物等の`scan`と、requirements等に並ぶ依存の`verify`を区別します。原資料の`verify <package>`という例をそのまま使いません。[Takumi Guardの制限](https://shisho.dev/docs/t/guard/limitation/)も、すべての悪性版を事前遮断できる保証とはしません。aliasやラッパーの外からの取得にも同じ制御が届くかは別に確認します。

**確かめ方・PJ反映。** 監査・metadata収集の途中で対象コードが動く場合、検査対象外、DB取得失敗、途中終了を成功へ変えていないか確認します。実行前検査は[依存更新ガイド](../../engineering/dependency-update-to-build.md)、検査の成立条件は[GOV-009](../../controls/records/governance-operations/psb-gov-009-scanner-evidence-trust-boundary/README.md)、取得遮断は[DEPS-005](../../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md)へ接続します。

## 8. Provenanceアテステーションとnpm audit signatures

**編集判断。** 出所と生成条件を確かめる提案は維持します。registry署名、公開者の署名、来歴を同一視する説明、検証コマンドの成功を来歴の必須化やSLSA level達成とする説明を変更します。pipのhashやGoのchecksumを同等の来歴検証に並べません。

**差し替え文。** 署名は「誰のどの主張を、どの成果物について確認したか」で読みます。利用側が期待する公開元・repository・生成経路と、実際に使用する取得物を結び付けます。正しい署名が付く不正コードもあり、出所の正当性と無害性は別です。

[`npm audit signatures`（v11文書）](https://docs.npmjs.com/cli/v11/commands/npm-audit/)は取得済み依存を対象に、registry署名や提供されたattestationを検証します。[v11.10.0の実装](https://github.com/npm/cli/blob/v11.10.0/lib/utils/verify-signatures.js)でも、全packageに来歴があるとは仮定していません。したがって、必要な来歴の欠落を拒否する方針と、期待する生成条件の照合を別に設けます。検査のためのinstallで先にscriptを動かさず、取得時の実行を止めた状態で検証し、使用可否を決めてから必要な処理を実行します。

[pnpm 10.xの`trustPolicy: no-downgrade`](https://pnpm.io/10.x/settings#trustpolicy)は、過去の公開版より信頼の証拠が弱くなる場合を扱う設定です。最初から来歴がないpackageにも来歴を一律要求するものとは区別し、除外設定も確認します。

**確かめ方・PJ反映。** 来歴なし、取得失敗、正しい署名だが別repository、検証後の別取得物という場合に、保護対象の使用が止まるか確認します。[REL-001](../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)の既存診断を使い、[多層防御ガイド](../../engineering/supply-chain-defense.md)には「検証できた証拠」と「必要な証拠が揃ったこと」の区別を補足します。

## 9. OIDC Trusted Publishing(長期トークンの排除)

**編集判断。** 公開用の長期tokenを減らす方針は維持します。これは公開側の対策であり、依存を使う側の安全確認ではありません。OIDC設定だけで旧tokenが無効になる説明、crates.ioの空token、NuGetの認証情報を渡さないpush例は訂正します。各registryの対応開始日を並べた表の未確認箇所は削除します。

**差し替え文。** Registry側で承認するCIのidentityと公開対象を限定し、その実行だけが短命の公開権限を取得できるようにします。workflowの変更・呼出し元・Environmentの審査と、公開前のビルドへの権限非付与も必要です。短命でも、取得したjob内の不正コードからは悪用され得ます。

| 一次資料と確認対象 | 修正する説明 |
|---|---|
| [npm Trusted publishing](https://docs.npmjs.com/trusted-publishers/)（文書の前提はnpm 11.5.1以上・Node 22.14.0以上） | trusted publisherの登録は既存tokenや手動公開の自動廃止ではない。公開アクセスのtoken禁止設定と旧tokenの失効を別に行う |
| [PyPI Trusted publishers](https://docs.pypi.org/trusted-publishers/) | 認めたpublisherのidentityから短命tokenを得る仕組み。登録したworkflow等の条件と、別の公開経路を確認する |
| [crates.ioの公式説明（2025-07-11）](https://blog.rust-lang.org/2025/07/11/crates-io-development-update-2025-07/) | 認証用Actionで取得したtokenを`CARGO_REGISTRY_TOKEN`として渡す説明へ修正。古い記事のprovider対応範囲を現行の網羅表にしない |
| [NuGet Trusted publishing](https://learn.microsoft.com/en-us/nuget/nuget-org/trusted-publishing) | OIDCから一時API keyへ交換し、そのkeyで公開する。`dotnet nuget push`が無条件に自動認証するとは書かない |

**確かめ方・PJ反映。** 別repository・branch・workflowからの交換と、旧token・手動公開の残存を確認します。[CICD-006](../../controls/records/cicd-security/psb-cicd-006-workload-federation-boundary/README.md)の交換条件・旧経路廃止を参照しますが、cloud向け実装例を各registryの実装証拠にはしません。公開物を利用する側の検証は[REL-001](../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)です。

## 10. アカウント保護(2FA / Passkey)

**編集判断。** 公開権限を持つアカウントの保護は維持します。Passkeyをすべてhardware内の持出し不能な鍵と説明する箇所、2FA必須化の状況を全registryに一般化する表は変更します。

**差し替え文。** 公開者・管理者のログインにはフィッシングへの耐性を持つ認証方式を選び、復旧用メール、予備の認証器、連携identity、管理者による復旧も同じ権限への入口として管理します。アカウントを保護しても、既存sessionやAPI tokenが盗まれる経路は残ります。

Passkeyは同期可能なものと、特定の認証器に結び付くものを区別します。[W3C WebAuthn Level 3のbackup eligibility・backup state](https://www.w3.org/TR/webauthn-3/)を根拠に、すべてのPasskeyが同じ鍵保護・復旧特性を持つとは説明しません。サービスごとの必須認証・復旧・tokenの扱いを現在の設定で確認し、端末侵害で認証済みsessionを盗まれる経路には[CircleCIの事例](https://circleci.com/blog/jan-4-2023-incident-report/)のような別対策が必要です。

**確かめ方・PJ反映。** 通常ログインを強化しても、弱い復旧手段や古いsessionで公開権限を取り戻せないか確認します。[SOURCE-004](../../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)と、侵害後の[GOV-004](../../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)へ接続します。

## 11. プライベートレジストリプロキシ(Dependency Confusion対策)

**編集判断。** 社内packageの名前と取得元を結び付ける方針は維持します。proxyを置けば自動的に名前衝突・待機・悪性検知・直接取得のすべてを防げる説明を変更します。TLS検証を緩める`trusted-host`を社内利用の定型手順に含めません。

**差し替え文。** 社内の名前は承認した社内供給元だけから取得し、同名の公開packageへ解決されないようにします。proxy内のremote repositoryへの転送規則と、端末・CIからの直接接続を両方確認します。名前の予約は補助策であり、別名・別クライアント・直接URLの経路を閉じる代わりにはなりません。

[pip install文書](https://pip.pypa.io/en/stable/cli/pip_install/)は、`--extra-index-url`によるprivate package取得にdependency confusionの注意を示しています。社内indexを追加しただけで優先順位が保証されたとは扱いません。[Goのproxy・private module設定](https://go.dev/ref/mod#private-modules)では、`GOPROXY`のfallbackや`GONOPROXY`が別経路を作ります。`GONOSUMDB`はchecksum DBの除外であり、取得元の限定とは別です。原文の`GONOSUMCHECK`は訂正します。npmのscope別設定なども、対象外の名前やクライアントを含む全経路の強制とは分けます。

**確かめ方・PJ反映。** 社内名と同名の公開候補、proxy停止、手動URL、cache利用で方針を迂回しないか確認します。[DEPS-005](../../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md)の既存項目を使い、待機は[DEPS-001](../../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)で別に判断します。

## 12. ad-hoc実行の安全化 (npx / pipx / uvx / go run)

**編集判断。** 一度だけ使うCLIも外部コードとして管理する方針は維持します。`yes=false`を「確認を必ず出す設定」とする説明、venvを端末権限のsandboxとする説明、固定版ならその場で実行してよいという説明を変更します。

**差し替え文。** 一時利用でも、名前・版・取得元と実行権限を確認します。審査済みのツールを用意し、取得・確認・実行の順序を分ける運用を選びます。取得ファイルを確認したら、再ダウンロードした別のbytesへ切り替えず、その対象を限定した権限で実行します。

[npm exec v11](https://docs.npmjs.com/cli/v11/commands/npm-exec/)の`--no`／`yes=false`は不足packageのinstall要求への否定です。既存のローカルCLI等の実行を禁止する機能ではなく、`ignore-scripts`もCLI本体の実行を止めません。[uv toolの環境分離](https://docs.astral.sh/uv/concepts/tools/)や[Python venv](https://docs.python.org/3/library/venv.html)は依存環境の分離です。pipx等で別環境へ入れても、そのプロセスへ渡るファイル・環境変数・通信権限は別に制限します。[版付きの`go run`](https://pkg.go.dev/cmd/go#hdr-Compile_and_run_Go_program)は現在のprojectの`go.mod`を使わずに動くため、projectの審査で承認済みと推測しません。

**確かめ方・PJ反映。** 未導入・cache済み・ローカル導入済みの各経路で、何が取得され何が実行されるか確認します。手動取得は[DEPS-005](../../controls/records/dependency-security/psb-deps-005-dependency-acquisition-gate/README.md)、実行の制限は[DEPS-002](../../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md)と[BUILD-001](../../controls/records/build-security/psb-build-001-build-containment/README.md)へ接続します。

## 13. シークレットの保護(.envファイルの扱い)

**編集判断。** 平文を長期間置かず、用途と権限を絞る方針は維持します。Secret Managerや`op run`を使えば実行中の不正コードから秘密を守れる説明と、`.gitignore`をアクセス制限とする説明を変更します。関係を確認できない事件・packageへの参照は外します。

**差し替え文。** 秘密を安全に保管することと、その値をどのプロセスへ渡すかは別の判断です。参照だけを設定ファイルへ置く方式でも、実行時に環境変数やファイルへ値を展開すれば、受け取ったコードは読めます。[1Passwordの`op run`](https://www.1password.dev/cli/reference/commands/run)も、参照を解決して子プロセスの環境へ渡す方式です。出力のマスクは、受け取ったコードによる読取りや外部送信の禁止ではありません。

依存の取得・検査・ビルドには不要な署名鍵・公開用token・本番秘密を渡しません。必要な操作だけに、対象を限定した短命の権限を渡します。読み出せる秘密、別の秘密を取得できる認証経路、子プロセスへの継承、ログや一時ファイルへのコピーを確認します。`.gitignore`はGitへの追加を避ける補助であり、端末上の読取りを拒否しません。漏えいした値は削除だけでなく失効と利用履歴調査へつなぎます。

**確かめ方・PJ反映。** 実秘密を使わず、環境変数・一時ファイル・読取り専用mountに置いた無害な目印へ実行コードが到達できるか確認します。[SOURCE-007](../../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md)と[BUILD-001](../../controls/records/build-security/psb-build-001-build-containment/README.md)には既にこの境界があるため、本文を複製せず参照します。

## 14. Dev Container / サンドボックス開発

**編集判断。** 実行環境を分ける提案は維持します。`.ssh`の読取り専用mountを秘密保護の例にする構成、非rootやremote環境だけで隔離が完了する説明を削除します。製品名を挙げただけでremote実行・OIDC対応を仮定しません。

**差し替え文。** コンテナの外へ出られなくても、渡した秘密や接続先は使われます。開発用環境へ渡すdirectory、環境変数、SSH agent、Docker等の管理socket、cloud metadata、共有cacheを洗い出し、不要なものを渡しません。[Dockerのread-only bind mount](https://docs.docker.com/engine/storage/bind-mounts/)は書込みを制限するもので、秘密ファイルの読取りを防ぎません。

通信先とhostへのアクセスは、実行されるコード自身が解除できない外側の制御で絞ります。共有cacheや成果物を介して後続jobへ不正な状態が残らないようにし、初期化・セットアップ処理が制限の適用前にhostで動かないかも確認します。OS環境の分離、権限の縮小、通信の制限、実行後の廃棄を、それぞれ確認できる構成を選びます。

**確かめ方・PJ反映。** 秘密の目印、hostのsocket、共有cache、許可外の通信への到達を、準備処理から終了まで確認します。[BUILD-001](../../controls/records/build-security/psb-build-001-build-containment/README.md)と[cache・runnerの設計](../../engineering/ci-state-and-runner-lifecycle.md)を正本とし、[多層防御ガイド](../../engineering/supply-chain-defense.md)から案内します。

## 15. 依存ツリーの削減

**編集判断。** 不要な依存と実行点を減らす提案は維持します。依存数の減少をそのままリスク減少率とする説明、標準APIや自作コードへ置き換えれば同じ機能と安全性を得られる例は変更します。

**差し替え文。** 使っていない依存や機能を外し、実行する公開者のコードと更新の判断を減らします。削減の候補は、利用箇所、実行時点、必要な権限、推移依存、保守状況、代替による互換性と保守負担で選びます。特に暗号・認証などを件数削減のためだけに自作しません。

件数は棚卸しの目安であり、同じ公開者・ビルド基盤に集中する依存や、高権限で動く少数のツールを評価する代わりにはなりません。[OpenSSF ScorecardのREADME（確認時点）](https://github.com/ossf/scorecard)も、検査をheuristicsとして扱い、総合点だけでは個別の状態が分からないと説明しています。点数・人気・更新頻度は調査の入口に留めます。削除後は必要な動作と、別の依存・外部通信で機能が復活していないことを確認します。

**確かめ方・PJ反映。** 不要と判断した依存が対象OSや開発・ビルド工程で再導入されないか、代替が必要以上の権限を増やさないか確認します。[DEPS-004](../../controls/records/dependency-security/psb-deps-004-dependency-change-review/README.md)の変更審査へ接続し、件数に対する新Controlは作りません。

## 16. ネットワーク監視とIOCフィードの運用

**編集判断。** 不審な通信を観測する提案は維持します。監視と遮断を分け、CISA KEVを通信先のIOC feedとする分類を訂正します。社内proxy障害時の公開registryへのfallbackと、pipの`trusted-host`を通信制御の例にする設定は外します。

**差し替え文。** 必要な通信を許す方針と、何が実際に通信したかを記録する仕組みを組み合わせます。パッケージ管理ツールのindex設定だけでは、動き始めたコードの通信先を制限できません。実行環境の外側で制限し、名前解決・redirect・proxy以外の経路と、許可された共有サービスへの情報送信も考慮します。

IOCは発行元、対象となる指標、取得時刻、適用範囲、訂正・失効を管理し、古い指標や取得失敗を「該当なし」にしません。[CISA KEV](https://github.com/cisagov/kev-data)は悪用が確認された脆弱性のcatalogで、C2 domainやpackage hashの一覧とは役割が異なります。EDRや通信ログは、観測できた端末・期間と動作状態を合わせて記録します。通信が見えない場合も、遮断に成功したのか、記録が欠けたのかを分けます。

**確かめ方・PJ反映。** 無害な通信で許可・拒否・記録を確認し、監視停止や対象外の端末を未観測として扱えるか確認します。[CONTAINER-006](../../controls/records/container-cloud-iac-security/psb-container-006-workload-network-segmentation/README.md)と[GOV-011](../../controls/records/governance-operations/psb-gov-011-security-event-evidence/README.md)へ接続します。container用の設定が開発端末にも効くとは扱いません。

## 17. SBOM(ソフトウェア部品表)の生成と管理

**編集判断。** 部品と利用先を調べる目的は維持します。全納入ソフトウェアに一律の提供義務があるという制度の要約は、適用対象・現行調達条件を確認していないため外します。形式の単純な優劣、生成・脆弱性照合の混同、JNDIを使わないという説明だけでLog4Shellを`not_affected`にする例も変更します。

**差し替え文。** SBOMには、何をどの時点で観測したかを示し、source revision、build、成果物digest、稼働先へ結び付けます。配布物に含まれない開発・ビルド依存も、端末・CI侵害の調査には必要です。形式は、受け手が扱える版、識別子、依存関係、必要な証拠の保持で選びます。[CycloneDXのBOM-Link](https://cyclonedx.org/capabilities/bomlink/)のような参照機能があっても、対応する対象の収集と維持は利用者の作業です。

生成器、照合器、集約基盤を役割で分けます。例えば[OSV-Scanner v2の出力文書](https://google.github.io/osv-scanner/output/)にはSPDX・CycloneDX出力もありますが、出力形式の対応と、調査に必要な全依存を収集できたことは別です。[Dependency-Track](https://github.com/DependencyTrack/dependency-track)へ登録しただけで、収集範囲・分析完了・脆弱性情報の鮮度・稼働先の対応まで確認済みとはしません。

[VEX](https://cyclonedx.org/capabilities/vex/)は、特定の製品・版と脆弱性に対する判断を根拠付きで伝えます。発行者、対象、理由、証拠、判断時点を確認して受け入れ、構成や情報が変われば再評価します。抑制した指摘を検査対象外や未調査と混ぜません。Log4Shellの条件は[Apacheの情報](https://logging.apache.org/security.html)に照らし、アプリが明示的にJNDIを呼ばないことだけで除外しません。

**確かめ方・PJ反映。** 同じ名前でも別digestの成果物、開発依存が抜けたSBOM、処理待ちの登録、古いVEXから誤って影響なしにしないか確認します。[REL-003](../../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)と[SBOMから影響調査へ](../../engineering/sbom-to-vulnerability-response.md)に接続し、既存の範囲を再定義しません。

## 18. YARA / 静的解析によるパッケージスキャン

**編集判断。** 実行前に配布物を調べる方針は維持します。公開されたルール数やサンプルへの検出結果を将来の検出率へ一般化する説明は削除します。`pip download --no-deps`をコード実行のない取得とする例、GuardDogの`scan`と`verify`の混同を訂正します。

**差し替え文。** 配布物を実行せず調べ、検査したbytes、検査器・ルールの版、対象形式、未検査の内容を記録します。[GuardDogのv3ブランチの文書](https://github.com/DataDog/guarddog/tree/v3)にあるpackage・archive・directoryのスキャンを使う場合も、読めない形式、難読化、後から取得するコードなどを「指摘なし」へ含めません。指摘は採用保留と調査につなぎ、未検出を無害性の証明にしません。

取得の前処理がコードを動かす場合があります。[pipのbuild system文書](https://pip.pypa.io/en/stable/reference/build-system/)に照らし、推移依存を取得しない指定だけでsourceのmetadata生成まで止まるとは判断しません。検査器自身も未信頼のarchiveやmetadataを処理するため、秘密と高い権限を渡さず、対象を実行する動的解析はさらに独立した環境で行います。

**確かめ方・PJ反映。** 途中で解析できなくなった配布物や、検査規則の対象外が合格へ変わらないか確認します。検査前の実行は[DEPS-002](../../controls/records/dependency-security/psb-deps-002-install-execution-policy/README.md)、検査範囲と完了状態は[GOV-009](../../controls/records/governance-operations/psb-gov-009-scanner-evidence-trust-boundary/README.md)を正本とします。

## 19. CIパイプラインのハードニング

**編集判断。** 外部実行物の固定、権限の縮小、変更審査は維持します。可変tagが使われるだけで全利用者が必ず侵害される説明、tokenの既定権限の一律断定、未確認の他CI製品向け設定例を削除します。Gradle distributionのchecksumとWrapper JARの検証を分けます。

**差し替え文。** CIで読み込むAction・plugin・wrapper・containerを、審査した出所と変更不能な参照へ結び付けます。[GitHub Actionsの公式ガイダンス](https://docs.github.com/en/actions/reference/security/secure-use)ではfull commit SHAでの固定を案内しています。固定したコードの中から取得する別の実行物も確認し、更新時のレビューと、問題が判明した版の利用停止を用意します。

未信頼PRのコードを、公開・署名・配備権限を持つjobで実行しません。`pull_request_target`等のイベント名だけで判断せず、何をcheckout・実行し、どのtoken・secret・cacheを使うかを追います。jobの権限を必要な範囲にし、依存の準備を行うsetup処理より前に実行方針を適用します。runnerを再利用する場合は前の実行が残した状態も境界に含めます。

[Gradle Wrapper文書](https://docs.gradle.org/current/userguide/gradle_wrapper.html)の`distributionSha256Sum`は配布ZIPの照合で、Wrapper JARの正当性確認は別です。[Mavenのoffline指定](https://maven.apache.org/ref/3-LATEST/maven-embedder/cli.html)を「社内Nexusだけへ接続」と説明せず、offline動作と取得先の設定を区別します。どちらも実行したplugin全体に対するOSの通信禁止とは扱いません。

**確かめ方・PJ反映。** 参照先の変更、権限付きjobへの未信頼入力、検査前のsetup実行、共有cache経由の影響を確認します。[CICD-001](../../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)、[CICD-004](../../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)、[CICD-005](../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)と[PRから公開への設計](../../engineering/pull-request-to-release-build.md)へ接続します。

## 20. コンテナイメージのサプライチェーン

**編集判断。** digestによる固定、署名・来歴、最小限の実行環境は維持します。署名検証コマンドを置いただけで利用が強制される説明、shellを除けば悪性コードが活動できない説明を削除します。base間のABI・実行時依存を確認していないmulti-stageのサンプルは完成した実装として残しません。

**差し替え文。** baseと配布imageを審査したdigestへ結び付け、更新時に差分を判断します。[Dockerのdigest固定の説明](https://docs.docker.com/build/building/best-practices/)に沿って、固定後は修正版も意識して更新する必要があると明記します。baseを固定しても、その上のbuild処理が取得・実行する依存は別に管理します。

[Cosignの検証](https://docs.sigstore.dev/cosign/verifying/verify/)では、署名の正当性に加え、信頼するidentityとissuer、対象digestを確認します。期待値を広すぎる正規表現で許可せず、必要な来歴の欠落・検証不能も使用を止める条件へ接続します。検証後に可変tagで取得し直さず、実際に使うdigestとの結び付きを保ちます。複数architectureのimageは、検証対象と実行される対象の関係も確認します。

小さなimageや非rootは攻撃に使える機能・権限を減らしますが、残ったプログラムからのファイル読取り・通信は可能です。実行権限、mount、通信先は別に絞ります。

**確かめ方・PJ反映。** 別identityの有効な署名、来歴欠落、検証後のtag変更で実行を許さないか確認します。[REL-001](../../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)、[CONTAINER-001](../../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)と[コンテナの実行から初動まで](../../engineering/container-deployment-to-response.md)を正本とします。

## 21. IDE拡張機能・開発ツール

**編集判断。** 拡張を実行可能な依存として扱う方針は維持します。`recommendations`／`unwantedRecommendations`を導入禁止の強制とする例、設定一つで全拡張がcontainer内へ移る説明を変更します。JetBrainsのpath設定やEclipseの更新設定を、裏付けなしに更新禁止へ読み替えた例、未確認の事件規模は削除します。

**差し替え文。** 拡張の出所・版・必要性と実行場所を審査し、許可外の導入、更新、手動配布による迂回を確認します。[VS Code 1.96以降の`extensions.allowed`と組織policy](https://code.visualstudio.com/docs/enterprise/extensions)は、導入・有効化を制限する機能です。ただしローカルVSIXの自己申告identityだけでは出所を検証できず、ローカルファイルの改変や実行時権限も別問題です。

[Workspace Trust](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust)は悪意ある拡張そのものの実行を防ぐsandboxではありません。[Extension Host](https://code.visualstudio.com/api/advanced-topics/extension-host)にはlocal・web・remoteの違いがあり、containerを使っていてもすべてがremoteで動くとは推測しません。実行場所ごとのファイル・秘密・socket・通信への到達を確認し、問題の版を無効にして更新・再起動後も読み込まれないことを確かめます。

**確かめ方・PJ反映。** 手動VSIX、許可済み拡張の更新、local host側に残る処理、失効後の再読込みを確認します。端末は[SOURCE-001](../../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md)、秘密の到達は[SOURCE-007](../../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md)、開発agentの拡張に該当する部分は次章のAI-002へ接続します。

## 22. AIコーディング支援・MCPサーバ

**編集判断。** 開発agent・MCP・拡張の依存管理は維持します。承認画面や特定ツールのsandboxを全プロセスの隔離保証とする説明を変更します。モデル・データセットの供給、RAG、AI製品の評価は[本PJの対象範囲](../../docs/SECURITY_SCOPE.md)外として、ai-security-foundryへ委ねます。

**差し替え文。** 開発agentが読み込むskills・plugin・MCP serverも、実行物と操作権限の組として管理します。出所、版またはdigest、起動コマンドと引数、接続先、渡す認証情報を審査し、更新で変われば再確認します。repositoryや外部文書に書かれた命令だけで権限を広げず、実際の読取り・書込み・通信・公開操作を外側で制限します。

例えば[Claude Codeのsandbox文書](https://code.claude.com/docs/en/sandboxing)は、shellとその子プロセスの境界と、外側で動くMCP server・hook・ファイル操作等を区別しています。製品内の一機能を有効にしただけで、すべての経路を制限したとは扱いません。[MCPのSecurity Best Practices（2025-11-25版への参照）](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)にあるtokenの宛先確認やtoken passthroughの禁止も、OSの隔離とは別の境界です。

承認時には実際の操作対象・送信先・権限を示し、停止時にはプロセスだけでなくsession、再起動条件、保存した認証情報、後続処理を確認します。出力されたコードや設定が正しいかのレビューも残します。

**確かめ方・PJ反映。** 拡張の差替え、外部文書からの命令、承認後の引数変更、shell以外の操作、停止後のsession利用を確認します。[AI-002](../../controls/records/ai-development-security/psb-ai-002-agent-extension-dependency-governance/README.md)、[AI-003](../../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)、[AI-004](../../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)と[作業開始から停止までの設計](../../engineering/development-agent-task-to-stop.md)へ接続します。

## 23. インシデント対応ランブック

**編集判断。** 担当と連絡経路を事前に決める提案は維持します。時間帯ごとの一本道を、被害と証拠消失に応じた並行対応へ変更します。鍵の失効を後段まで待つ、再起動・cache削除・手編集だけで復旧する例、全事案で一律72時間の顧客通知とする説明は削除します。

**差し替え文。** 不正な依存の実行が疑われたら、対応責任者を決め、封じ込め・認証情報の失効・証拠保全・影響調査を並行して進めます。順序は、進行中の被害、停止の影響、失われる証拠で決め、全容の判明や保全完了を一律に待ちません。[NIST SP 800-61r3（2025-04）](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf)の対応・証拠保全・復旧を、この判断へ接続する本PJの編集案です。

| 担当する作業 | 初動で決めること・次へ渡すもの |
|---|---|
| 端末・CI・配布の封じ込め | 対象の隔離、疑わしい版の取得・公開停止、継続させる必要がある業務と代替経路 |
| 認証情報への対応 | 読まれ得た値と権限、旧token・派生session・再発行条件の停止。新しい値は信頼できる別環境から扱う |
| 証拠保全と調査 | 観測時刻、対象bytes・digest、必要なログ、実施操作と理由、収集できなかった範囲。秘密そのものは通常の記録へ複製しない |
| 再構築と再開 | 信頼を回復した環境と承認済み入力から再構築し、汚染したrunner・cache等を再利用しない。新成果物の稼働と旧版の非稼働を確認する |

通知は、適用法令、契約、影響を受ける相手、判断責任者で条件を決めます。例えば[EDPBのGDPR 33・34条の説明](https://www.edpb.europa.eu/sme/assess-the-risks/data-breaches_en)では、データ管理者（controller）の監督機関への通知と本人への連絡は条件が異なります。GDPRの対象となる個人データ侵害では、個人の権利・自由へのリスクが生じる可能性が低い場合を除き、不当な遅延なく、可能なら覚知から72時間以内に監督機関へ通知し、遅れる場合は理由を示します。本人への連絡は高リスク等の条件に基づき、不当な遅延なく行うものです。全セキュリティ事案の一律の時間割に転用しません。

**確かめ方・PJ反映。** 全容が未確定でも停止・失効の担当が動けるか、保全に失敗した範囲が残るか、再起動で旧版へ戻らないかを机上で確認します。[GOV-004](../../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)、[GOV-005](../../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)と[対応・再開の設計](../../engineering/security-signal-to-response.md)に既にある判断へ接続します。

## 24. ブラストレイディアス評価

**編集判断。** 依存からサービスへ逆引きし、使えた権限まで調べる方針は維持します。OSV-Scanner単体を全社の利用先台帳とする説明、行検索だけで全lockfileを調査できる例、一律の「10分以内」を完成条件とする表を変更します。`aws-nuke`を認証情報の棚卸しツールに挙げた推薦は削除します。

**差し替え文。** 問題の名前・版・取得物から、取得した端末、実行したCI、作られた成果物、配布・稼働先を調べます。実行時期と、その時点で到達できた秘密・公開権限・network・共有状態を確認します。製品に同梱されない開発依存も対象です。結果は「影響候補」「調べた範囲では該当なし」「未調査・調査不能」に分けます。

[Dependency-Track](https://github.com/DependencyTrack/dependency-track)のportfolio検索で調べられるのは登録・解析した対象です。[OSV-Scanner v2](https://google.github.io/osv-scanner/usage/)は渡した入力から部品を抽出し脆弱性へ照合するため、別途全対象の収集が必要です。[対応形式の文書](https://google.github.io/osv-scanner/supported-languages-and-lockfiles/)にも、manifestから推測した版や対象外の依存に限界があります。未信頼projectを調査するために、そのbuildや依存解決を高権限で再実行しません。

[aws-nuke](https://github.com/ekristen/aws-nuke)はAWS resourceの削除を目的とするツールで、認証情報棚卸しの推薦には適しません。[AWS IAM credential report](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html)のような状態の照会を用いる場合も、対象account・user・認証情報の種類と観測時刻を明示し、全sessionや全権限の調査を代替しません。

**確かめ方・PJ反映。** 検索権限不足、未取得ページ、停止中の端末、未登録の成果物、古いSBOM、ログ欠測を結果から消さないか確認します。記録がないことを秘密への非到達や無影響の証拠にしません。[GOV-001](../../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)へ調査範囲と不足を、[GOV-004](../../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)へ失効対象を渡します。原資料のDependency-Track API例は対象版のOpenAPIと検索範囲を未照合のため、実行手順として採用しません。

## 末尾の対策一覧

**編集判断。** 「対策の層構成」「汎用的原則」「npm特化の即効対策」は、一つの役割表と着手判断へまとめます。全エコシステムで同じ設定が使える説明、全攻撃に有効という断定、環境確認なしの即日導入・完了の宣言は削除します。多数のツール名を上位順に並べず、前提と残る経路を示します。

**差し替え文。** 自分たちが外部コードを使う経路と、他者へコードを公開する経路を分けて対策します。

| 役割 | まず決めること | この対策の後にも残ること |
|---|---|---|
| 利用側の取得・更新（1〜8・11〜12・15・18章） | 取得元、待機条件、承認する差分、実行前の検査、固定した入力 | 正規の取得元から来る不正コード、検査の見逃し、手動取得の迂回 |
| 実行環境（13〜14・16・19〜22章） | 渡す秘密・権限・通信、外側の強制、共有状態の扱い | 必要な権限の悪用、許可先への送信、観測できない経路 |
| 公開側（9〜10・19〜20章） | 公開identity、workflowの変更管理、旧公開経路の停止、配布物の検証材料 | 正規job自体の侵害。利用側の無害性確認を代行するわけではない |
| 発見後の対応（17・23〜24章） | 依存・成果物・稼働先の対応、停止・失効・保全・復旧の担当 | 台帳・記録の欠測、調査対象外。復旧と無影響は別の結論 |

npm利用者は、まず使用版と実効設定を確認し、不要なscriptの停止、待機条件、通常ビルドでのlock照合を適用できるか判断します。その上で、取得先を含む変更審査と、必要な署名・来歴を使用前の条件へ接続します。設定の存在で完了とせず、許可・拒否・判定不能の代表経路を確認します。公開者はこれに加えて、公開権限と復旧経路を見直します。

**確かめ方・PJ反映。** [多層防御ガイド](../../engineering/supply-chain-defense.md)を入口に、対策を通過した後の権限と対応まで確認します。この役割表は原資料の編集用です。本PJの10 domainや[分析レンズ](../../docs/ANALYSIS_LENSES.md)を置き換えず、Controlへの適合・導入状態・全攻撃への対応を宣言しません。

## 採用しない記述と再確認の条件

章中の理由に加え、原資料の製品別コマンド・事例のうち、差し替え文へ残していないものは今回の推奨から外します。削除は常に誤りと断定する意味ではありません。

| 扱い | 該当する記述 | 再び採用するために必要な確認 |
|---|---|---|
| 不採用 | 製品の未知攻撃への強さ・誤検知コストの順位、一定時間後の安全保証、依存数だけの安全判定 | 比較対象・入力・評価方法・限界を備えた再現可能な根拠。順位が読者の判断に必要かも再検討 |
| 訂正して採用 | npmの待機単位、uvのlock確認、NuGetの版指定、GuardDogの操作、OIDC公開、KEV、Wrapper、VS Codeの許可機能、aws-nukeの用途 | 各章の一次資料を使用版へ照合。サービスや既定値が変われば再審査 |
| 未確認のため非採用 | 事件規模・滞在時間・因果の未照合部分、古いPoetry等のCLI、JetBrains/Eclipse等の設定、他registryの網羅的対応表、Dependency-TrackのAPI例 | 当事者報告または公式仕様、対象版、必要な条件・失敗経路を確認。原資料にURLがあるだけでは採用しない |
| 範囲外 | モデル・データセットの供給、AIアプリケーション固有の設計・評価 | ai-security-foundry側で扱い、本PJの開発agent対策へ戻さない |

本PJへの追加は文書と診断項目で完了とします。Sourceの登録と既存成果物との関係、文書検証の結果は[移行台帳](../../docs/MIGRATION.md)に記録します。実装例・テストコード・Controlの新設、Scrapboxの直接編集、外部公開は行いません。
