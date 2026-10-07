# Source Protection — 移行判断

この文書は旧成果物の採否・移行時の判断をdomainごとにまとめた履歴です。現在の要件は各control、現在の進捗は[移行計画](MIGRATION_PLAN.md#現在地と次の作業)を確認してください。

## 収録した主題

- [Developer endpoint migration reconciliation](#endpoint-migration)
- [Git hooks migration reconciliation](#git-hooks-migration)
- [SOURCE-003 Public source exposure migration](#public-exposure-migration)
- [Repository recovery independenceの移行判断](#repository-recovery-migration)
- [Source organization security postureの移行判断](#source-organization-posture-migration)
- [Source credential lifecycle framework reconciliation](#source-credential-mapping)

<a id="endpoint-migration"></a>

<a id="endpoint-migration--developer-endpoint-migration-reconciliation"></a>
## Developer endpoint migration reconciliation

対象は旧`PSB-SOURCE-001`、domainは`source-protection`です。2026-09-21に29項目を棚卸しし、
[Managed developer endpoint](../engineering/source-protection/managed-developer-endpoint/README.md)へ端末管理の設計を先行移行しました。
2026-09-22に[Developer endpoint trust](../controls/records/source-protection/psb-source-001-developer-endpoint-trust/README.md)のcontrol記録を追加しました。
旧4件のframework関係は下記で照合し、製品実装と実環境の診断は引き続き未移行です。

<a id="endpoint-migration--根拠と受入条件"></a>
### 根拠と受入条件

移行元はコミット`3bfbeb21246bb2f58c55fa5212068805bca1719b`の
[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/control.yaml)、
[実装ガイド](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/developer-endpoint-hardening/docs/check-implementation-guide.md)です。
提供原文とbaselineの出自・採否は[参照資料記録](../sources/README.md#ref-developer-endpoint-baseline-001)へ保持します。

受入条件は、全29項目の追跡、端末管理と隣接領域の責任分界、状態悪化からアクセス制限への接続、
観測失敗と違反の区別、端末・製品設定を確認していない範囲の明示です。架空の安全／危険設定や検査成功を追加しません。

<a id="endpoint-migration--29項目の配置"></a>
### 29項目の配置

`control-migrated`は旧項目を問いに合わせてcontrolへ再編集したもの、`adjacent`は隣接する成果物への受け渡しです。
`adjacent`は旧項目の完全な移行や実装済みを意味しません。本文全体を複製せず、未対応部分を残します。

| 旧check | 主題 | 扱い | 配置・残る境界 |
|---|---|---|---|
| DEH-001 | 短命な認証情報 | adjacent | [SOURCE-007](../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md)は端末に残る長期の値を減らす選択を扱う。[SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)はソース管理サービス側の権限と期間を扱う。クラウド等の発行・失効の製品別確認は別途必要 |
| DEH-002 | 保護された保管 | adjacent | [SOURCE-007](../controls/records/source-protection/psb-source-007-developer-local-credential-storage/README.md)が開発端末上の保管場所と利用時の受け渡しを扱う。ソース管理サービス側の権限と失効はSOURCE-004 |
| DEH-003 | ハードウェア保護鍵 | adjacent | SOURCE-007は端末にコピー可能な値を残さない選択肢として扱い、SOURCE-004はソース管理サービス側の鍵の権限・失効を扱う。鍵種別・利用者確認・失効の製品別検証は保留 |
| DEH-004 | pre-commit検査 | adjacent | [SOURCE-002](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md)のSECRET-2・3・4と診断で確認する項目へ。製品hooks・導入は未確認 |
| DEH-005 | サーバー側検査 | adjacent | SOURCE-002のSECRET-5へ。送信・受入・mergeを分け、実際のprovider設定と経路は未確認 |
| DEH-006 | install隔離 | adjacent | [Install execution policy](../engineering/dependency-security/install-execution-policy/README.md)と[Build execution boundary](../engineering/build-security/build-execution-boundary/README.md)。開発端末での隔離実装は保留 |
| DEH-007 | cooldownと例外 | adjacent | [DEPS-001](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md)。更新採用は端末の良好状態とは別判断 |
| DEH-008 | 端末の通信制限 | control-migrated | ENDPOINT-5、ENG-SOURCE-002。配布設定と迂回できない通信経路を区別。実通信の検証は保留 |
| DEH-009 | 集中認証・MFA | adjacent | SOURCE-004。全業務サービスへのSSO適用は保証しない |
| DEH-010 | 機密データの公開防止 | control-migrated | [SOURCE-008](../controls/records/source-protection/psb-source-008-sensitive-data-repository-admission/README.md)へ。認証情報以外のデータの所有者・持込み可否・Git受入を扱う。旧hook・宣言fixtureは移植せず、実効的な拒否は未確認 |
| DEH-011 | registry proxyの強制 | adjacent | [Cooldown pattern](../engineering/dependency-security/dependency-release-cooldown/README.md)。全端末・全package managerの迂回防止は未確認 |
| END-001 | ディスク暗号化 | control-migrated | ENDPOINT-2、ENG-SOURCE-002。回復鍵と電源断時の保護を、ログイン後のプロセス権限から分離 |
| END-002 | 画面ロック | control-migrated | ENDPOINT-2、ENG-SOURCE-002。再認証と物理的な不在時の利用防止 |
| END-003 | OS・ツール更新 | control-migrated | ENDPOINT-3、ENG-SOURCE-002。サポート対象、適用期限、再起動、期限付き例外 |
| END-004 | 通常権限・昇格 | control-migrated | ENDPOINT-4、ENG-SOURCE-002。標準ユーザーの権限悪用は残る |
| END-005 | workspaceの秘密情報 | adjacent | SOURCE-007が`.env`など作業領域の平文ファイルと利用時の受け渡しを扱う。[Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md)は開発agentへの到達範囲、SOURCE-004はソース管理サービス側の権限と失効を扱う |
| END-006 | runtime socket | adjacent | Development runtime isolation。AI以外の開発環境への適用・実装検証は保留 |
| END-007 | debugサービス公開 | control-migrated | ENDPOINT-5、ENG-SOURCE-002。待受の制限を残し、未知のポートやトンネルまで検査済みとしない |
| END-008 | AIツールの通信 | adjacent | Development runtime isolation。開発ツールの通信境界のみ。提供先の保持・リージョン・テナントの契約と実効性は別途確認 |
| END-009 | mountの書込み範囲 | adjacent | Development runtime isolation。共有先の限定とcredential除外。汎用開発環境の製品設定は保留 |
| END-010 | バックアップ | control-migrated | ENDPOINT-6、ENG-SOURCE-002。暗号化・復元権限と復旧可能性を分ける |
| END-011 | アプリ・拡張の管理 | control-migrated | ENDPOINT-3、ENG-SOURCE-002。AI拡張の内容審査は[Agent extension admission](../engineering/ai-development-security/agent-extension-admission/README.md)へ |
| END-012 | EDR・XDR | control-migrated | ENDPOINT-7、ENG-SOURCE-002。登録・観測・通知・初動を分離。検知ルールと製品adapterは未移行 |
| END-013 | commit署名 | deferred | 署名者と検証条件、鍵の失効、repository側の拒否を別途整理。署名をコードの安全性・作者本人・端末健全性の保証にしない |
| END-014 | IDEのSAST・SCA | deferred | 開発者へのフィードバックを強制gateと区別。[DETECT-001](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)はIDE連携の導入証明ではない |
| END-015 | 管理された隔離環境 | adjacent | ENG-SOURCE-002で方式を比較し、Development runtime isolationへ接続。接続元端末の保護は残す |
| END-016 | sandbox制限・観測 | adjacent | Development runtime isolationとBuild execution boundary。端末全体のEDRとは別の範囲 |
| END-017 | 集中管理・是正 | control-migrated | ENDPOINT-1 / ENDPOINT-8、ENG-SOURCE-002。登録、現在の観測、資産側のアクセス判断を分離 |
| END-018 | 物理保護・紛失 | control-migrated | ENDPOINT-2 / ENDPOINT-8、ENG-SOURCE-002。保管・輸送、失効、調査、復旧。未到達の消去を完了扱いにしない |

集計は`control-migrated`12項目、`adjacent`15項目、`deferred`2項目です。
SOURCE-001は対象を絞ったcontrol記録として数えます。旧29項目全体の移植・実装・導入完了ではありません。

<a id="endpoint-migration--旧実装とframework-mapping"></a>
### 旧実装とframework mapping

旧`policy.conf`の29宣言を検査するfixtureは移植しません。宣言の整合性が端末への導入証明にならないためです。
読み取り専用Linux assessmentは有用な候補として保留し、観測対象のOS・ホスト、権限、収集失敗の区別をレビューしてから判断します。
旧Linux adapterはworkspaceのblock-device chain、GNOMEの画面ロック設定、既知のdebug portなどを実際に読みます。ただし暗号化を調べるのはworkspaceの参照先、管理権限の判定はrootと一部のgroup、debug待受は固定portに限られ、MDMの状態、資産側の既存セッション、通知・失効は観測しません。ローカルの一部設定の結果を、端末全体の良好状態やアクセス制限の証拠へ昇格させず、今回も移植しません。
今回、ユーザーの実端末を検査・変更していません。

旧4件は、版・ID・関係・confidence・対象check・旧レビューを保持した上で、2026-09-22に適用範囲を照合しました。
[SSDF 1.1公式本文](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)のPO.5.2・PS.3.1・PW.4.1と、
MITREの[T1552.001](https://attack.mitre.org/techniques/T1552/001/)・[T1555](https://attack.mitre.org/techniques/T1555/)の公開本文を確認しました。
MITREの現行ページ確認を旧v19.1全体の再検証とは扱いません。参照時点と採否は[Sources](../sources/README.md#ref-developer-endpoint-baseline-001)に記録します。

| 旧Framework・版 | ID・関係・confidence | 照合結果 |
|---|---|---|
| MITRE ATT&CK v19.1 | T1552.001 / mitigates / medium | DEH-002・END-005は認証情報保管側、DEH-004・005は検査側。新しい端末管理特性へ直接割り当てない |
| MITRE ATT&CK v19.1 | T1555 / mitigates / medium | DEH-002の端末上の保管境界はSOURCE-007へ引き継ぐ。端末管理がpassword storeからの窃取を防ぐ関係として継承しない。SOURCE-007への新たなframework関係は未評価 |
| NIST SSDF 1.1 (SP 800-218, 2022) | PS.3.1 / supports / medium | 原文はreleaseごとのファイルと関連データの保存。旧端末保護全般という根拠は不一致のため、新controlへ継承しない。端末バックアップもrelease archiveの代替ではない |
| NIST SSDF 1.1 (SP 800-218, 2022) | PW.4.1 / supports / medium | DEH-011の依存取得は隣接領域。端末管理全体への対応として継承しない |

旧4件は現在のframework mappingへ追加しません。代わりに、端末保護を直接扱うSSDF PO.5.2と
ENDPOINT-1・2・3・4・7の部分的な設計関係を[framework mapping](../mappings/frameworks.yaml)へ追加しました。
旧IDの機械的な置換ではなく、本文を確認した新しい対応です。要求全体への準拠や実環境での検証を意味しません。

<a id="endpoint-migration--旧framework関係の原記録"></a>
#### 旧framework関係の原記録

以下は移行元から保持した履歴です。新controlの有効なマッピングではありません。

```yaml
legacy_mappings:
- framework: mitre-attack
  version: v19.1
  id: T1552.001
  relationship: mitigates
  confidence: medium
  rationale: Protected credential storage and prohibition of secrets in workspaces reduce exposure to
    credentials in files.
  reviewer: product-security
  review_date: '2026-07-25'
  applies_to:
  - DEH-002
  - DEH-004
  - DEH-005
  - END-005
- framework: mitre-attack
  version: v19.1
  id: T1555
  relationship: mitigates
  confidence: medium
  rationale: System-managed credential storage and endpoint access controls reduce exposure of credentials
    from password stores.
  reviewer: product-security
  review_date: '2026-07-25'
  applies_to:
  - DEH-002
- framework: nist-ssdf
  version: 1.1 (SP 800-218, 2022)
  id: PS.3.1
  relationship: supports
  confidence: medium
  rationale: Least privilege, protected credentials, and endpoint policy checks support protection of
    code and development environments.
  reviewer: product-security
  review_date: '2026-07-25'
  applies_to:
  - DEH-001
  - DEH-002
  - DEH-003
  - DEH-004
  - DEH-005
  - DEH-008
  - DEH-009
  - DEH-010
  - END-001
  - END-002
  - END-003
  - END-004
  - END-005
  - END-006
  - END-007
  - END-008
  - END-009
  - END-010
  - END-011
  - END-012
  - END-013
  - END-014
  - END-015
  - END-016
  - END-017
  - END-018
- framework: nist-ssdf
  version: 1.1 (SP 800-218, 2022)
  id: PW.4.1
  relationship: supports
  confidence: medium
  rationale: Managed proxy-only package acquisition constrains third-party component sources and preserves
    reviewable acquisition evidence.
  reviewer: product-security
  review_date: '2026-07-31'
  applies_to:
  - DEH-011
```

<a id="endpoint-migration--残る範囲"></a>
### 残る範囲

製品設定、Linux収集器、端末と資産側のアクセス制御を結ぶ実環境評価は保留です。
診断で確認する項目はcontrol記録に整理済みであり、実際に診断した結果とは区別します。
2026-09-23にhooksとサーバー側の検査観点をSOURCE-002へ接続しました。公開済み情報の探索・署名・IDE連携は別の境界として残し、SOURCE-001へ再集約しません。

<a id="git-hooks-migration"></a>

<a id="git-hooks-migration--git-hooks-migration-reconciliation"></a>
## Git hooks migration reconciliation

2026-09-23、旧PSB-SOURCE-002を[Secret publication boundary](../controls/records/source-protection/psb-source-002-secret-publication-boundary/README.md)と
[Secret checks before publication](../engineering/source-protection/secret-checks-before-publication/README.md)へ再編集しました。
移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`の
[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/control.yaml)と
[README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/git-hooks-baseline/README.md)です。

<a id="git-hooks-migration--13項目の配置"></a>
### 13項目の配置

旧IDはGHK-001〜012とGHK-014です。欠番を埋めず、元の13項目を追跡します。
以下は設計への移行と隣接責任の整理であり、旧実装の動作検証ではありません。

| 旧check | 主題 | 配置・採否 |
|---|---|---|
| GHK-001 | hookの所有・レビュー | SECRET-3。Repository配置と中央配布を選択肢にし、実際に実行する版を管理 |
| GHK-002 | 外部hookパス | SECRET-3。絶対・共有パスを一律拒否する旧方式は普遍化せず、配布元・変更権限・実効設定を確認 |
| GHK-003 | credential helper・remote内の値 | 隣接：端末上の保管はSOURCE-007、ソース管理側の権限・失効はSOURCE-004。Git製品設定の移植は保留 |
| GHK-004 | safe.directory | 隣接：SOURCE-001の端末権限。Git所有権チェックの製品設定は保留し、hooks管理だけで保証しない |
| GHK-005 | 署名とpush範囲 | 分割：push範囲はSECRET-1。署名・identityの設定は保留し、内容の検査と分離 |
| GHK-006 | 機密形式の拒否 | SECRET-1・2。拡張子だけで機密性を判断せず、内容・検査不能範囲と組み合わせる |
| GHK-007 | 検出と非表示 | SECRET-2・6。旧ルール一覧と検出率を現在の保証には移さない |
| GHK-008 | サイズ上限 | SECRET-1・4。検査の上限を超えた場合の拒否・別経路を定め、旧5 MiBを一律要件にしない |
| GHK-009 | staged内容 | SECRET-2。作業ツリーとの違いを診断で確認する項目へ |
| GHK-010 | commit message | SECRET-2。内容とメタデータを別に検査 |
| GHK-011 | push履歴 | SECRET-1・2。導入履歴を確認。pre-push自体も省略できるためSECRET-5へ接続 |
| GHK-012 | 検査障害 | SECRET-4。失敗・未検査を検出なしにしない |
| GHK-014 | Gitleaks併用 | SECRET-3・4・6の設計へ。製品wrapper・image取得・実行は保留し、複数エンジンを必須にしない |

受信側の独立した判断SECRET-5と限定した除外SECRET-7は、旧READMEの限界と今回確認した仕様から具体化した本PJの設計です。
[端末管理のDEH-004・005](MIGRATION_SOURCE_PROTECTION.md#endpoint-migration)から、このcontrolへローカル検査とサーバー側検査の責任を接続します。
公開済み情報の探索・回収、署名、全機密データの分類は統合しません。

2026-09-30の読み合わせでは、実際の認証情報が共有先へ届いたと分かった場合の受け渡しを明確にしました。非公開リポジトリも共有先であり、受信側でref更新を拒否しても送信前の阻止とは異なります。公開検索による再発見を待たず、値を複製せずに所有者とGOV-004へ到達範囲・失効判断を渡します。SOURCE-003は既知経路外の公開候補を観測する隣接主題です。これはGitの受信境界と両controlの適用範囲から導いた本PJの解釈で、特定providerでの保持や実際の漏えいを推定しません。

<a id="git-hooks-migration--旧4件のframework関係"></a>
### 旧4件のframework関係

| 旧関係 | 今回の扱い |
|---|---|
| ATT&CK v19.1 / T1552.001 / mitigates / medium | ファイル内認証情報の取得と誤公開の接点はあるが、端末からの窃取全体への防御とは異なる。旧関係は履歴に保持し、保管を分離した新特性への割当は保留 |
| SSDF 1.1 / PS.3.1 / supports / medium | releaseの保存に関する原文と、旧source保護全般という根拠が不一致。継承しない。SOURCE-001の[照合結果](MIGRATION_SOURCE_PROTECTION.md#endpoint-migration--旧実装とframework-mapping)を参照 |
| OSPS 2026.02.19 / OSPS-BR-07.01 / supports / high | 2026-09-23に公式本文を確認。SECRET-1・2・4・5への部分的な設計関係として採用。旧highは履歴に残し、現行のconfidenceはmedium。全機密データや迂回経路の防御・適合性を証明しない |
| CISA Version 2 / CISA-PSBP-PP-08 / mitigates / medium | このIDは旧registryによるローカルID。公式PDFを今回取得できず、新特性への割当は保留。旧版・根拠・対象checkを削除しない |

<a id="git-hooks-migration--原記録"></a>
#### 原記録

次の旧記録は現在のマッピングではありません。現行の関係は[frameworks.yaml](../mappings/frameworks.yaml)で管理します。

```yaml
legacy_mappings:
- framework: mitre-attack
  version: v19.1
  id: T1552.001
  relationship: mitigates
  confidence: medium
  rationale: ローカルでのsecretおよび機密ファイル検査はファイル内credentialの誤公開を減らすが、回避可能でpatternにも限界がある。
  reviewer: product-security
  review_date: '2026-07-27'
  applies_to:
  - GHK-003
  - GHK-007
  - GHK-009
  - GHK-010
  - GHK-011
  - GHK-014
- framework: nist-ssdf
  version: 1.1 (SP 800-218, 2022)
  id: PS.3.1
  relationship: supports
  confidence: medium
  rationale: レビューで保護されたrepository-owned hooksとローカルのcredentialおよびidentity保護は、source codeと開発環境の保護を支援する。
  reviewer: product-security
  review_date: '2026-07-27'
  applies_to:
  - GHK-001
  - GHK-002
  - GHK-003
  - GHK-004
  - GHK-005
  - GHK-006
  - GHK-007
  - GHK-008
  - GHK-009
  - GHK-010
  - GHK-011
  - GHK-014
- framework: openssf-osps-baseline
  version: 2026.02.19
  id: OSPS-BR-07.01
  relationship: supports
  confidence: high
  rationale: Repositoryへcommitされる前にsecret patternと機密ファイルを検出・拒否し、unencrypted sensitive dataの意図しない保存防止を支援する。
  reviewer: product-security
  review_date: '2026-07-27'
  applies_to:
  - GHK-006
  - GHK-007
  - GHK-009
  - GHK-010
  - GHK-011
  - GHK-014
- framework: cisa-product-security-bad-practices
  version: 2 (January 2025)
  id: CISA-PSBP-PP-08
  relationship: mitigates
  confidence: medium
  rationale: Commit前にhardcoded credentialとsecret patternを検出・拒否してsource codeへの混入を減らすが、pattern外のsecretやhook
    bypassまでは防止できない。
  reviewer: product-security
  review_date: '2026-07-27'
  applies_to:
  - GHK-007
  - GHK-009
  - GHK-010
  - GHK-011
```

<a id="git-hooks-migration--実装検証の扱い"></a>
### 実装・検証の扱い

旧installer、Docker版Gitleaks wrapper、設定は移植していません。
既存hooksを自動上書きしない判断と切り戻し時の注意は、[新しい代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)の明示的な導入手順へ反映しました。
Gitleaks 8.30.1の組込み検出を採用し、独自PythonはGit objectと拒否判断の接続に限定しました。
旧Gitleaks版・container digest、旧独自ルール、5 MiB等をGitleaks実装の推奨設定として引き継いでいません。
検出・迂回・履歴・検査障害・値の非表示は、controlの診断で確認する項目として整理しました。
一時worktreeとbare repositoryだけで23件の実装テストを実施しました。本PJ自身や実環境のhooks有効化、
外部への検出用文字列の送信、組織の実環境診断は実施していません。
参照版・採否・取得できなかった資料は[Sources](../sources/README.md#ref-secret-publication-001)へ記録します。

2026-09-23追記：具体化判断により、[Git・Gitleaks代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)を追加しました。
旧実装をそのまま復元せず、検出は固定したGitleaksへ、独自コードはGitとの接続へ責任を分けています。
範囲と完了状態の正本は[実装計画](MIGRATION_PLAN.md#source-002の具体実装計画)です。

2026-09-25追記：旧`scan-sensitive.py`の正規表現、機密file名、staged内容、commit message、push履歴、
matched valueを表示しない判定を、[Python pattern scanner](../engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner/README.md)へ再編集しました。
外部toolなしで仕組みを読み、軽い組織固有ruleを試すための第二実装です。新規remote refはremote-tracking refを信頼せず、local tipから到達する履歴を検査するよう変更しました。
ローカルhookだけで受信側のSECRET-5を満たさず、Gitleaksと検出同等でもありません。旧installer、Docker wrapper、巨大なfixture inventoryは移していません。
12 ruleの無効canary、near miss、値の非表示、staged内容、削除後もpush履歴に残る値、Gitによるhook起動を7 testで確認しました。
これは限定したimplementationの挙動であり、本PJや利用者のrepositoryへの導入証拠ではありません。

2026-10-03追記：Python版を使い捨てGitへ導入して正常commit、無効canaryの拒否、scanner欠落時の停止、解除を確認しました。NUL入り・5 MiB超の入力は検出結果ではなく検査不能として`ERROR/2`へ分離し、READMEのsmoke testと既存テストを更新しました。8件のローカルテストは通過しています。Gitleaks版は手元binaryが固定配布物のhashと異なり、今回の実動作試験には含めていません。

<a id="public-exposure-migration"></a>

<a id="public-exposure-migration--source-003-public-source-exposure-migration"></a>
## SOURCE-003 Public source exposure migration

移行元は`product-security-controls@91fdb7661b38723ce6fb38da93cf3c68b701e521`の
[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/91fdb7661b38723ce6fb38da93cf3c68b701e521/controls/source-protection/public-repository-exposure/control.yaml)と
[README](https://github.com/DharmaDoll/product-security-controls/blob/91fdb7661b38723ce6fb38da93cf3c68b701e521/controls/source-protection/public-repository-exposure/README.md)です。

<a id="public-exposure-migration--結論"></a>
### 結論

旧成果物の成果は、組織に関係する公開source surfaceを攻撃者に近い視点で反復観測し、初出・変更・再出現、
期限付き判断、観測障害を区別してresponseへ渡すことです。この成果を
[PSB-SOURCE-003](../controls/records/source-protection/psb-source-003-public-source-exposure-triage/README.md)の6特性と
[ENG-SOURCE-004](../engineering/source-protection/public-exposure-observation-and-triage/README.md)へ再編集しました。

旧PoCが選んだGitHub Actions、Python standard library、public Search API、Gist delta、専用state branch、
sanitized JSONという具体構成は移植しません。この方式は一つの実装候補ですが、採用provider、対象surface、
認証view、state store、通知・case管理によって適切な設計が変わります。Fixture testの成功も実環境のcoverage、
通知、responseを証明しません。

この判断は、具体実装を避ける一般方針ではありません。SOURCE-002ではGit/Gitleaksの技術経路が明確で、
検査対象と拒否境界をcodeで具体化する価値が高いため代表実装を追加しました。SOURCE-003では、providerと運用を
選ぶ前に旧PoCを正本化すると、製品固有の制限と一つのstate方式がcontrolの意味へ逆流するため、旧PoCの移植を保留しました。後に対象をGitHubの公開コード・Issue・PRへ絞り、新しい小さな実装例を追加しています。

<a id="public-exposure-migration--旧checkの配置"></a>
### 旧checkの配置

| 旧check | 旧成果 | 現行配置 | 判断 |
|---|---|---|---|
| `MON-001` | Owned domainにanchorしたreconnaissance query | `PUBLIC-EXPOSURE-1,2` | 所有・許可したindicatorと、query identity・coverageを分けて移行 |
| `MON-002` | Public code・Issue・PR・Gistの収集とsanitization | `PUBLIC-EXPOSURE-2,3,6` | Surface coverage、値の最小化、partial collectionの失敗を分けて移行 |
| `MON-003` | Exact review stateとrecurrence通知 | `PUBLIC-EXPOSURE-4,5` | Occurrence stateとownerのtriage decisionへ抽象化して移行 |
| `MON-004` | Public search identityとstate writerの分離 | `PUBLIC-EXPOSURE-2,3,6` | GitHub workflow要件ではなく、observation view・state integrity・healthの設計へ移行 |
| `MON-005` | Browser-only reconnaissanceのhuman baseline | `PUBLIC-EXPOSURE-2,5` | 自動化できないsurfaceと人の判断をcoverage・triageへ移行。Browser GETを必須方式にしない |
| `MON-006` | Collection・state failureをcleanにしない | `PUBLIC-EXPOSURE-6` | Provider、state、通知、stale observationまで含むhealth propertyへ移行 |

<a id="public-exposure-migration--旧実装の扱い"></a>
### 旧実装の扱い

| 旧成果物 | 扱い | 理由 |
|---|---|---|
| `scripts/monitor-public-exposure.py` | 非移植 | GitHub providerと独自state contractを選んだPoC。現在のAPI挙動・coverage・運用への適合を未確認 |
| `secure/.github/workflows/public-exposure-monitor.yml` | 非移植 | Trusted triggerや権限分離は再利用できる設計入力だが、採用repositoryとnotificationなしでは導入結果にならない |
| `secure/domain-monitor.json`、`secure/state/findings.json` | 非移植 | Synthetic configurationとsample stateを組織のevidenceにしない |
| `insecure/domain-monitor.json` | 非移植 | 問題のある状態を表す比較fixtureをcontrol記録へ置かない。確認項目は現行controlへ移行 |
| `tests/`、`expected-results/` | 非移植 | 旧PoCのbehavior testであり、現行のprovider-neutral propertiesを検証する実装対象がまだない |
| `PUBLIC_EXPOSURE_MONITOR_POC_SPEC.md` | 要点をpatternへ移行 | Coverage、redaction、occurrence、failure semanticsは再利用。GitHub固有interfaceは旧固定commitに保持 |

2026-09-26に利用者がGitHubの公開コード・Issue・PRと、少数の自社ドメイン・メールアドレスに対象を絞ったため、[新しい限定実装](../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)を追加しました。旧fileを復活させず、人の精査後の通知、同じ候補の重複抑制、収集失敗・部分取得の明示だけに集中します。実際のGitHub認証情報、指標、Webhook、対応担当者は導入先が決めます。

2026-09-30のSOURCE-002との読み合わせでは、既知の認証情報が共有先へ届いた事象を、この公開検索の候補発見まで待たせないと整理しました。非公開の共有先や受信側で拒否された送信内容は、この実装の検索対象ではありません。SOURCE-003は既知経路外の公開候補と追加のcopyを見つける役割であり、SOURCE-002から所有者・GOV-004への直接の引き渡しを代替しません。

<a id="public-exposure-migration--旧framework-mapping"></a>
### 旧framework mapping

次は現行mappingではありません。旧版、関係、confidence、対象check、根拠、reviewer、review日を履歴として保持します。

| Framework / ID | 旧relationship／confidence | 旧対象check | 旧review | 旧根拠 |
|---|---|---|---|---|
| MITRE ATT&CK v19.1 / `T1593.003` | `detects / high` | `MON-001,002,005` | `product-security / 2026-08-26` | Owned-domain searchでpublic code repository reconnaissanceを防御側から再現し、攻撃者が発見できる情報を検出する |
| MITRE ATT&CK v19.1 / `T1552.001` | `detects / medium` | `MON-002,005` | `product-security / 2026-08-26` | Domainにanchorしたpublic code・Gist検索でfile内credentialまたは周辺設定の候補を探す |
| NIST SSDF 1.1 / `RV.1.1` | `supports / medium` | `MON-001,002,003,005,006` | `product-security / 2026-08-26` | Public surfaceの反復収集、review state、browser baseline、失敗の明示が潜在的security issueの識別・確認を支援する |
| OpenSSF OSPS 2026.02.19 / `OSPS-BR-07.01` | `supports / low` | `MON-002,003,005` | `product-security / 2026-08-26` | Public fileとcollaboration contentのcredential候補監視がsecret取扱いを補助する |

2026-09-24、固定版の原文と現行6特性を再照合し、`T1593.003`だけを
`PUBLIC-EXPOSURE-1,2,4,5,6 / detects / medium / design-reviewed`として現行mappingへ追加しました。
これはpublic code repositoryから標的情報を探す攻撃経路と、同じ公開面に現れた候補を防御側が観測する設計の
部分的な関係です。攻撃者の検索行動そのものを検知する意味ではなく、旧`high` confidenceは維持しません。

次の3件は非継承です。

- `T1552.001`: Local file systemやremote file shareを含むfile内credentialの探索・取得を扱う。SOURCE-003は
  public surfaceのcandidate triageであり、secret検出を必須方式にせず、domain matchからcredentialの存在や有効性を確認しない。
- `RV.1.1`: Softwareとthird-party componentの潜在的脆弱性について、acquirer、user、public sourceから情報を集め、
  credible reportを調査するtask。SOURCE-003の主対象は、公開source surfaceにある組織情報・credential・設定の露出であり、
  software vulnerability reportの収集ではない。
- `OSPS-BR-07.01`: Version controlへのunencrypted sensitive dataの意図しない保存を防止する要件。
  事後観測とtriageだけではpreventを満たさない。この関係はSOURCE-002の公開前・受入境界に割り当て済み。

<a id="public-exposure-migration--参照資料"></a>
### 参照資料

- [REF-PUBLIC-SOURCE-EXPOSURE-001](../sources/README.md#ref-public-source-exposure-001)に、固定GitHub文書、採用した判断、非採用の実装、限界を記録しました。
- 旧PoCのREADMEが参照したGitHub Search、Gists、Code Search syntaxは、2026-09-24に
  `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`の固定本文で再確認しました。
- Enterprise ATT&CK v19.1の固定STIXで`T1593.003`と`T1552.001`、NIST SP 800-218公式PDFで`RV.1.1`、
  OSPS Baseline 2026.02.19で`OSPS-BR-07.01`を2026-09-24に確認しました。
- 実環境のsearch、credential、public candidate、notification、responseにはアクセスしていません。

<a id="repository-recovery-migration"></a>

<a id="repository-recovery-migration--repository-recovery-independenceの移行判断"></a>
## Repository recovery independenceの移行判断

旧[PSB-SOURCE-005](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/repository-destruction-recovery/control.yaml)を、重要なソースの破壊権限、独立した保管世代、実際の復旧と開発再開へ再編集しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-26です。

| 旧項目 | 行き先・採否 |
|---|---|
| RDR-001 | [RECOVERY-1](../controls/records/source-protection/psb-source-005-repository-recovery-independence/README.md)：製品の必要対象、固定ID、owner、RPO・RTO。GitHubの数値IDと全page取得は製品固有の選択であり、全providerの要件にしない |
| RDR-002 | RECOVERY-2と[設計pattern](../engineering/source-protection/independent-repository-backup-and-restore/README.md)：repository削除・移管とref保護、制限の変更・bypassを分ける。GitHubの設定を全providerへコピーしない |
| RDR-003 | RECOVERY-3〜4：保管世代を破壊できる権限、鍵と復旧用ID、保持、取得の鮮度。別accountやObject Lock COMPLIANCEという製品選択を唯一の実現方法にしない |
| RDR-006 | RECOVERY-5〜6：隔離した実復元、ref・内容・外部データの照合、設定、修正・build、開発再開までの時間。旧四半期を全組織の確認間隔にしない |

旧controlにRDR-004〜005は存在しません。欠番を補完しません。旧[secure runbook](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/repository-destruction-recovery/secure/README.md)の一律checklistは、そのまま正本にせず、選ぶ対象・権限・復元方法・確認結果を説明する設計へ分けました。組織の導入状況は移行しません。

<a id="repository-recovery-migration--具体化判断と旧テストの扱い"></a>
### 具体化判断と旧テストの扱い

必要な成果物はcontrol、control配下の教材、設計pattern、診断観点です。Gitの取得と復元は技術経路が明確なため、[Git mirror実装例](../engineering/source-protection/independent-repository-backup-and-restore/implementations/git-mirror/README.md)も完成条件に含めました。独自のbackupサービスやJSON判定器は作らず、Git標準コマンドによる最短手順、smoke test、解除方法を示します。

旧[tests/test.sh](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/repository-destruction-recovery/tests/test.sh)は実際に使い捨てrepositoryを作り、mirror、元の削除、branches・tagsのpush、ref照合、不完全復元の検出を確認します。合成JSONの自己申告ではなく、この実観測の価値を移しました。

新しい例は、新世代へのmirror取得と新しいbare repositoryへの復元に限定します。ローカル元とのobject共有を避け、annotated tagのobject IDも照合し、元の接続設定を外します。練習用の元repositoryは削除せず別名へ移し、元の場所への依存がないことを確認します。七件の実Gitテストは元の不在、タグ欠落、同名タグの指す先変更、object破損、既存復元先、shallow source、取得中のref変更を観測します。

実装から設計へ戻した判断は、`fsck`成功と必要対象の充足は別、ref名だけでは不足、取得中の変更を成功にしない、更新用mirrorと保持世代を分ける、コピー元との接続を残さない、という点です。取得時のref一覧も取得前から消えた対象を知らないため、製品の必要対象との照合を別に残しました。

2026-09-30の読み合わせでは、攻撃者が内容を書き換えた後に取得した世代も、`fsck`と取得時のref一覧との比較に成功し得ることを明示しました。採用する世代は変更経緯と独立した判断材料から選び、判断できなければ復旧成功にしません。NIST SP 800-61 Rev.3の復旧用資産・復元後の資産を確認する考え方を[Sources](../sources/README.md#ref-repository-recovery-001)へ追加しました。Git例の七テストは整合性と復元経路の確認であり、侵害前の世代を識別する試験ではありません。

この限定例の完了は組織への導入や開発再開の確認ではありません。Live GitHubの拒否、独立したcloud account・鍵・保持lock、LFS、metadata、設定復元、製品の修正・build、RPO・RTO、通知は未確認です。Provider・保管先・必要データ・復元先・許可された確認方法が選べたときに、対応する実装・評価へ戻ります。

<a id="repository-recovery-migration--参照と旧framework関係"></a>
### 参照と旧framework関係

直接の資料は[REF-REPOSITORY-RECOVERY-001](../sources/README.md#ref-repository-recovery-001)、Git実装の仕様は[REF-GIT-MIRROR-RECOVERY-001](../sources/README.md#ref-git-mirror-recovery-001)へ分けました。GitHubのarchive取得とrestore対応を同一視せず、Object Lockの保護対象versionとdelete marker、保持modeの迂回権限を区別します。旧資料の固定確認間隔、保持mode、provider内の削除後復元への依存を共通要件へ移しません。

旧framework mappingはSITF `1.0.0@d1d1536 / T-V009`の`mitigates / high`、MITRE ATT&CK `v19.1 / T1485`の`mitigates / medium`でした。旧日付は2026-08-25で、前者はRDR-001・002・003・006、後者はRDR-002・003・006へ割り当てられていました。攻撃行動との概念上の関係は残りますが、今回その固定版の本文との項目別再照合は行っていないため新しいframework mappingへ継承しません。ローカルGit復元の成功から、組織の大量削除対策や導入済みを主張しません。Framework mappingは116件のままです。

<a id="source-organization-posture-migration"></a>

<a id="source-organization-posture-migration--source-organization-security-postureの移行判断"></a>
## Source organization security postureの移行判断

旧[PSB-SOURCE-006](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/control.yaml)の10項目を、共通方針、必要対象への実適用、grantの照合、状態の変化、確認障害と対応へ分けました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-27です。README、metadata、verifier、二つのrunbookがこの固定revisionと一致することも確認しました。

<a id="source-organization-posture-migration--旧項目の行き先"></a>
### 旧項目の行き先

| 旧項目 | 行き先・採否 |
|---|---|
| GHO-001 | [ORG-POSTURE-1・6](../controls/records/source-protection/psb-source-006-source-organization-security-posture/README.md)：固定組織、方針、必要対象、取得範囲、時点、障害。旧24時間とpolicy SHA-256を全組織の必須形式にしない |
| GHO-002 | ORG-POSTURE-2・4：組織の認証条件とIdP連携の現状。Credentialの発行・失効はSOURCE-004へ渡す。SAML／SCIM／EMUと24時間のoffboardingを一律に要求しない |
| GHO-003 | ORG-POSTURE-2・4：共通設定を変更する管理者の帰属、必要性、回復経路。Ownerを必ず2〜3名とする数値、90日のreviewを共通要件にしない |
| GHO-004 | ORG-POSTURE-4：member・team・外部協力者の実grantを所有者・用途へ照合。外部協力者を必ずpull／triageだけにする旧固定policyは採らない |
| GHO-005 | ORG-POSTURE-2〜3：初期権限、作成・公開・fork、既定値と実適用。Base None、全作成・全private fork禁止という組合せを唯一の正解にしない |
| GHO-006 | ORG-POSTURE-2〜3：組織のActions条件と対象ごとの適用。外部参照は続いて移行した[CICD-001](MIGRATION_CI_CD.md#workflow-dependency-migration)、workflow権限は[CICD-004](MIGRATION_CI_CD.md#workflow-authority-migration)へ渡す |
| GHO-007 | ORG-POSTURE-4：Appのowner・用途・対象・権限の現在値とreview。業務上必要なwriteやadministrationを全Appで一律に不合格にしない |
| GHO-008 | ORG-POSTURE-3：選んだsecurity機能の必要対象と実適用。検査機能の全一律有効化やSOURCE-003への合格を本controlの成功条件へ複製しない |
| GHO-009 | ORG-POSTURE-5〜7：現在状態とaudit、取得・保存・通知のhealth、担当者と再確認。180日保持、30日canary、zero sequence gap、全open driftゼロを普遍条件にしない |
| GHO-010 | ORG-POSTURE-6〜7：方針の承認、未確認と取得障害、秘密情報の持込防止、限定例外、再確認。旧policyの固定floorや例外の全禁止を移さない |

SOURCE-004はID・credential自体の必要範囲と失効、SOURCE-002は公開境界の検査、SOURCE-003は公開候補の観測・精査、SOURCE-005は破壊制限と復旧を扱います。新controlに残す問いは、それらの設定・grantが組織の必要対象へ届き、後の上書き・漏れ・確認障害を見つけられるかです。本文やテストを複製せず、担当成果物へリンクします。

<a id="source-organization-posture-migration--具体化判断"></a>
### 具体化判断

必要な成果物はcontrol、control配下の教材、設計pattern、診断観点です。GitHubを使う場合の確認経路は明確なので、[GitHubの具体手順](../engineering/source-protection/organization-baseline-and-drift-review/implementations/github/README.md)も完成条件に含めました。現在の画面、項目の選択、最短の確認・適用、GETでの補助、使い捨て対象でのsmoke test、解除方法を記載します。

この手順の完成とlive導入を分けます。GitHub CLI 2.95.0のhelpとREST API 2026-03-10の公式仕様は確認しましたが、実organizationの設定変更、API収集、適用・拒否、IdP、監査配送、通知は実行していません。SaaSの設定を架空のテストで成功扱いにせず、実環境の確認は組織側に残します。

旧[verify.py](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/scripts/verify.py)はPython実装です。Normalized JSONの形、時刻、policy digest、固定floor、申告されたgrant・health・alert等を評価します。GitHub・IdPへ接続せず、設定や実際の通知を観測しません。Verifier、policy、snapshot、mutation fixtureは新実装例へコピーしません。Policyを2〜3OwnerやAppのwrite全禁止等へ縛る旧floorも、本PJのcontrolを定義する根拠にはしません。

旧[adoption runbook](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/docs/github-adoption-runbook.md)は画面・GET・変更影響を判断する価値を選別し、固定のMinimum値と不要なendpoint一覧を外しました。旧[automation options](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/source-protection/github-organization-governance/docs/governance-automation-options.md)は、手動、read-only現在状態、auditとの組合せ、第三者Appの選択肢をpatternへ移します。自動収集が必要になる条件と代償を残し、collectorやAllstarを実装済みにはしません。

Collectorの具体化は、必要対象、GitHubの契約とendpoint、IdP、読取り権限、保存先、通知先、取得期限が決まった時に再開します。完了条件は、実取得の必要範囲、pagination・permission denial・rate limit・部分失敗、適用差、通知受領、修正後の実値を観測し、未対応項目を示すことです。Synthetic JSONを増やすことを代替にしません。

実装手順からcontrol・patternへ戻した境界は、新規defaultと移管の違い、configurationの存在と実status、既定tokenとworkflow権限、全page取得とcredentialの可視範囲、2FA fieldとIdP・SSOの違いです。2026-09-30の読み合わせでは、Appの新規申請・インストール制限と既存installation、OAuth制限の再有効化と以前の承認、PAT方針によるブロックとtoken自体の失効も分けました。SOURCE-006は組織側の現在値と方針差を見つけ、不要な認可の失効・拒否確認はSOURCE-004へ渡します。直接資料の確認日・採否は[Sources](../sources/README.md#spec-github-organization-posture)に残します。

<a id="source-organization-posture-migration--旧framework関係と旧資料id"></a>
### 旧framework関係と旧資料ID

旧レビュー日は2026-08-26です。次の11関係は移行履歴として保持します。今回、固定版のexact項目へ新propertyを割り当て直していないため、新しいframework mappingへ継承しません。特に旧`verifies / high`を実organizationの確認結果として使いません。Framework mappingは116件のままです。

| 旧framework・版 | IDと旧関係 | 旧適用項目 |
|---|---|---|
| GitHub guidance `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24） | GH-ADMIN-AUDIT-EVENTS：verifies / high | GHO-001・009・010 |
| 同上 | GH-ADMIN-SAML-IAM：supports / high | GHO-002・003 |
| 同上 | GH-ADMIN-SCIM-ORGANIZATIONS：supports / high | GHO-002・004 |
| 同上 | GHSC-SECURE-ACCOUNTS：supports / high | GHO-002・003・004 |
| 同上 | GH-ADMIN-ACTIONS-ORGANIZATION：verifies / high | GHO-006 |
| 同上 | GH-ADMIN-CREDENTIAL-TYPES：supports / medium | GHO-007 |
| 同上 | GHSC-SECURE-CODE：supports / medium | GHO-005・008 |
| OpenSSF OSPS `2026.02.19` | OSPS-AC-02.01：supports / high | GHO-003・004・007 |
| 同上 | OSPS-AC-04.01：supports / medium | GHO-006 |
| MITRE ATT&CK `v19.1` | T1078：mitigates / medium | GHO-002・003・004 |
| 同上 | T1098：mitigates / medium | GHO-003・004・007 |

SOURCE-004で確認済みの固定GitHub guidanceは、ORG-POSTURE-4の隣接するID判断へ参照します。それでも旧関係全体を再照合したことにはしません。旧`REF-CICD-015`（DS-202）、`REF-CICD-017`（Flatt Security）、`REF-CICD-018`（Allstar）は調査入力の履歴としてここに保持し、今回未再参照の資料を新propertyの直接根拠に追加しません。新しいIDの別名としても残しません。

<a id="source-credential-mapping"></a>

<a id="source-credential-mapping--source-credential-lifecycle-framework-reconciliation"></a>
## Source credential lifecycle framework reconciliation

2026-09-23から24日にかけて、[PSB-SOURCE-004 Source credential lifecycle](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)の
framework対応を、公式本文と旧記録に照らして再評価しました。

移行元は`product-security-controls@91fdb7661b38723ce6fb38da93cf3c68b701e521`の
[control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/91fdb7661b38723ce6fb38da93cf3c68b701e521/controls/source-protection/source-access-credential-lifecycle/control.yaml)です。
旧記録の削除や意味の書換えは行わず、この文書に履歴として保持します。

<a id="source-credential-mapping--ssdfの結論"></a>
### SSDFの結論

旧`PS.3.1`対応は継承しません。NIST SP 800-218の`PS.3.1`は、リリースごとに保持すべきファイル、
完全性検証情報、provenanceを安全にarchiveする要件です。SOURCE-004の認証情報とセッションの
発行・範囲・保管・棚卸し・失効・監査とは、対象資産、目的、強制点が異なります。

SOURCE-004に近い要件は`PS.1.1`です。これはsource、executable、configuration-as-codeを最小権限で保管し、
許可した人・tool・serviceだけにアクセスさせることを扱います。SRC-AUTH-1〜6は、そのアクセス境界を成立・維持する
認証情報ライフサイクルとして`PS.1.1`を部分的に支援します。この関係を`design-reviewed / medium`で新規に記録します。

これは番号の機械的な置換ではありません。`PS.3.1`との旧関係を非継承とし、別の原文との関係を独立して評価した結果です。
SOURCE-004だけでは、すべてのcodeの保管、repositoryの変更保護、code owner review、commit signing、実環境の最小権限を
実現または証明しません。

<a id="source-credential-mapping--残る8件の結論"></a>
### 残る8件の結論

2026-09-24に、GitHubの固定commitにある4文書、Enterprise ATT&CK v19.1の固定STIX、
OSPS Baseline 2026.02.19の版付き本文を確認しました。7件を`design-reviewed`へ移し、意味が広すぎた
property割当とconfidenceを次のように修正しました。残るASI03も2026-10-04に別途照合しています。

| Mapping | 現行の割当 | 判断 |
|---|---|---|
| `GHSC-SECURE-ACCOUNTS` | `SRC-AUTH-2,4,5`／`supports`／`medium` | SSO・2FA、SSH秘密鍵保護・短命証明書、SCIMによる失効を部分的に支援。旧割当のscope、workload ID、auditは本文が直接扱わない |
| `GH-ADMIN-CREDENTIAL-TYPES` | `SRC-AUTH-1,3,5`／`supports`／`medium` | 認証情報とuser・installation・repository・workflowの対応、存続期間、失効手段を選択判断に使う。保管やaudit要件ではないため旧`high`を維持しない |
| `GH-ADMIN-SAML-IAM` | `SRC-AUTH-5`／`supports`／`medium` | SAML identity、session、authorized credentialの表示・失効を支援。SAML自体をphishing-resistant MFAと解釈せず、旧`SRC-AUTH-2`割当を外す |
| `GH-ADMIN-SCIM-ORGANIZATIONS` | `SRC-AUTH-5`／`supports`／`medium` | Organization membershipのprovisioning・deprovisioningを支援。すべてのcredentialとsessionの失効を保証しない |
| `T1078` | `SRC-AUTH-1..5`／`mitigates`／`medium` | 権限の重複、休眠account、盗まれた有効なcredentialの悪用可能性と期間を減らす部分的関係 |
| `T1552.001` | `SRC-AUTH-4`／`mitigates`／`medium` | File内に回収可能なtoken・private keyを残さない境界との直接関係。memory、process、password store全体には拡張しない |
| `OSPS-AC-01.01` | `SRC-AUTH-2`／`supports`／`medium` | OSPSは機微なrepository resourceのreadまたはmodify時のMFAを要求する。SOURCE-004はcredential発行・機微変更だけを扱うため部分対応とし、旧`high`を維持しない |
| `ASI03` | `SRC-AUTH-1,3,4,5`／`mitigates`／`medium` | 開発用agentのソース管理アクセスに限定。権限の範囲、自動処理用ID、認証情報の受け渡し・失効が継承権限の悪用を一部減らす。旧`SRC-AUTH-6`の監査を緩和へ数えない |

2026-09-24の初回レビューでは公式PDFの自動取得がHTTP 403で拒否されていました。2026-10-04に公式PDF公開経路の検索索引でASI03本文を確認し、上の部分的な関係へ変更しました。今回もPDF本体のhashは確認できていません。Agent固有のidentity、委譲先・下流サービスの認可、contextに残る認証情報、実行時のtool操作はSOURCE-004だけでは扱いません。

GitHubの製品文書は、SOURCE-004の製品非依存な特性を定義する根拠ではありません。固定版の製品挙動と
実装選択の対応を示す資料です。ATT&CKとAgentic Top 10は脅威分類であり、合格条件や準拠要件ではありません。
OSPSとの関係も、要件全体への対応やプロジェクトの成熟度を示しません。

<a id="source-credential-mapping--セキュリティ特性ごとの判断"></a>
### セキュリティ特性ごとの判断

| SOURCE-004特性 | PS.3.1 | PS.1.1との関係 | 限界 |
|---|---|---|---|
| SRC-AUTH-1 | 非継承 | 主体・resource・operation・期限への権限結合が、code accessの最小権限を直接支援 | Repository側の権限モデルと実効設定は別に必要 |
| SRC-AUTH-2 | 非継承 | 発行・機微変更時の強固な認証が、許可主体以外による権限取得を減らす | PS.1.1自体が特定の認証方式を要求するとは解釈しない |
| SRC-AUTH-3 | 非継承 | task限定のworkload IDが、許可したtool・serviceだけにaccessを与える設計を支援 | Workload federation条件と実行後の操作認可は別の境界 |
| SRC-AUTH-4 | 非継承 | 認証情報の保護とconsumer限定の受渡しが、repository access境界の迂回を減らす | Code storage自体の完全性・可用性・機密性を保証しない |
| SRC-AUTH-5 | 非継承 | 棚卸しと失効が、現在必要な主体だけにaccessを維持する | 失効処理と関連sessionの実効性は実環境の証拠が必要 |
| SRC-AUTH-6 | 非継承 | 所有者・resourceに結び付く監査が、version controlのaccountabilityを支援 | 変更内容のレビューや全変更の追跡を単独では保証しない |

全特性を`PS.1.1`へ対応させるのは、各特性が同じ強さでSSDFを実装するという意味ではありません。
認証情報ライフサイクルが、許可された主体だけにcode accessを限定する一つの下位設計である、という部分的な関係です。

<a id="source-credential-mapping--ps31を引き継ぐ先"></a>
### PS.3.1を引き継ぐ先

現行ポートフォリオには、release filesと関連するintegrity・provenance dataのarchiveを一体で扱うcontrolはありません。
[PSB-REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)は、consumerが使用前に
artifactと署名・provenanceを照合する境界であり、producerによるrelease保存の要件ではありません。
したがって`PS.3.1`をPSB-REL-001へ移し替えず、release preservationの空白として残します。

<a id="source-credential-mapping--旧記録"></a>
### 旧記録

次は現在のmappingではありません。旧版、関係、confidence、根拠、対象check、reviewer、review日をそのまま保持します。

```yaml
framework: nist-ssdf
version: 1.1 (SP 800-218, 2022)
id: PS.3.1
relationship: supports
confidence: medium
rationale: Controlled development credentials and protected access to repositories
  support protection of code from unauthorized access and modification.
reviewer: product-security
review_date: '2026-08-05'
applies_to:
- SCL-001
- SCL-002
- SCL-003
- SCL-004
- SCL-005
- SCL-006
- SCL-007
- SCL-008
- SCL-009
- SCL-010
- SCL-011
- SCL-012
- SCL-013
- SCL-014
- SCL-015
- SCL-016
- SCL-017
```

残る8件の旧記録は次のとおりです。`SCL-*`は移行元の個別checkであり、現行の`SRC-AUTH-*`と同じ粒度ではありません。
この表は比較用の要約で、文字単位の旧正本は上記の固定commitに残します。旧mappingの`relationship`、`confidence`、
対象check、reviewer、review日と根拠の意味を保持し、現行判断との差を追跡します。

| ID | 旧relationship／confidence | 旧対象check | 旧review | 旧根拠 |
|---|---|---|---|---|
| `GHSC-SECURE-ACCOUNTS` | `supports / medium` | `SCL-001..017` | `product-security / 2026-08-05` | Credential selection、phishing-resistant authentication、protected storage、review、revocationがsecure GitHub account useを支援する |
| `GH-ADMIN-CREDENTIAL-TYPES` | `supports / high` | `SCL-001,002,003,004,005,008,009,010,011,013,014,015` | `product-security / 2026-08-14` | Provider taxonomyによりuser・App・workflow・SSH credentialのidentity、lifetime、SSO authorization、storage、review、revocationを区別する |
| `GH-ADMIN-SAML-IAM` | `supports / medium` | `SCL-007,009,010,013,014` | `product-security / 2026-08-14` | SAML authenticationとcredential authorizationがsource access boundaryを支援する |
| `GH-ADMIN-SCIM-ORGANIZATIONS` | `supports / medium` | `SCL-009,010` | `product-security / 2026-08-14` | SCIM membership removalがoffboardingとaccess reviewを支援する |
| `T1078` | `mitigates / medium` | `SCL-001,002,003,004,005,007,008,009,010,013,014,015,016` | `product-security / 2026-08-05` | Least privilege、bounded lifetime、review、revocationによりstolen valid credentialのpersistとimpactを減らす |
| `T1552.001` | `mitigates / medium` | `SCL-006,008,015` | `product-security / 2026-08-05` | Credential helper、hardware protection、credential-free configurationによりfile内のtoken・private keyを減らす |
| `OSPS-AC-01.01` | `supports / high` | `SCL-007` | `product-security / 2026-08-05` | Phishing-resistant MFAとcentralized authenticationがsensitive project actionへのMFAを支援する |
| `ASI03` | `mitigates / high` | `SCL-013,014,015,016,017` | `product-security / 2026-08-05` | OAuth優先、限定PAT fallback、child-only delivery、read-only tool surfaceによりidentity・delegated privilege abuseを減らす |

<a id="source-credential-mapping--根拠と状態"></a>
### 根拠と状態

- [NIST SP 800-218公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)の`PS.1.1`（PDF p.17、印刷ページ9）と`PS.3.1`（PDF p.18、印刷ページ10）を2026-09-23に確認しました。
- GitHubの4文書は`github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`の本文を2026-09-24に確認しました。Credential types、SAML、SCIMのSHA-256は旧registry記録と一致し、Account securityは今回`5def696244c0bc300adf532acdb4d4a40ae0eabd0c218afbc969a028847c3e1b`を記録しました。
- Enterprise ATT&CK v19.1の公式STIXはSHA-256 `bdf1ce86a4e604214c5076d37ae4dcb322678afc528df8492e6fdc1b554f5da3`が旧registry記録と一致し、`T1078`と`T1552.001`を2026-09-24に確認しました。
- [OSPS Baseline 2026.02.19](https://baseline.openssf.org/versions/2026-02-19#osps-ac-0101)の`OSPS-AC-01.01`本文を2026-09-24に確認しました。
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)はlanding page、公開日、WordPress media ID `52216`、PDF size `1,274,186 bytes`を確認しました。公式PDF本体はHTTP 403で取得できませんでしたが、公式公開経路の検索索引でASI03本文を確認し、SOURCE-004の対象特性と照合しました。PDFのhashや実環境の認可は未確認です。
- 現行mappingは[frameworks.yaml](../mappings/frameworks.yaml)、参照版と採否は[Sources](../sources/README.md#spec-nist-ssdf-1-1)を正本とします。
- この照合は資料とcontrolの意味をレビューしたものです。SSDF準拠、実環境の権限制御、SOURCE-004全体の導入済み状態を示しません。
