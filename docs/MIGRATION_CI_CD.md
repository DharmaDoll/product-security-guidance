# CI/CD Security — 移行判断

この文書は旧成果物の採否・移行時の判断をdomainごとにまとめた履歴です。現在の要件は各control、現在の進捗は[移行計画](MIGRATION_PLAN.md#現在地と次の作業)を確認してください。

## 収録した主題

- [Workflow analysisの移行判断](#workflow-analysis-migration)
- [Workflow authority minimizationの移行判断](#workflow-authority-migration)
- [Workflow dependency identityの移行判断](#workflow-dependency-migration)
- [Workflow input handlingの移行判断](#workflow-input-migration)

<a id="workflow-analysis-migration"></a>

<a id="workflow-analysis-migration--workflow-analysisの移行判断"></a>
## Workflow analysisの移行判断

旧[PSB-CICD-003](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-static-analysis)の5項目を、既存controlとworkflow固有の設計へ配置しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-27です。旧packageの14 fileと旧`.github/workflows/actions-security.yml`が固定revisionに一致することを確認しました。

<a id="workflow-analysis-migration--旧項目の行き先"></a>
### 旧項目の行き先

| 旧項目 | 行き先・判断 |
|---|---|
| SAS-001：scanner固定 | [DETECT-001のSCAN-1・2](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)と[CICD-001](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)。Tool、実行するimage、policyを区別し、旧固定値を現在の推奨値にしない |
| SAS-002：PR gate | SCAN-3・4と[CICD-004](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)・[CICD-005](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)。候補をデータとして解析し、権限を分け、指摘・障害・未検査を受入条件へ接続する |
| SAS-003：信頼できる側でSARIF公開 | [ENG-CICD-007](../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)の方式選択とCICD-004・005。結果公開は必要な場合に選び、`main`へのpush条件を保護の証拠にしない |
| SAS-004：結果の三状態 | SCAN-3・4と[DETECT-001の教材](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/learning.md)。Scanner・版・出力modeごとの終了状態と、正常完了・対象範囲・指摘を照合する |
| SAS-005：採用workflowの照合 | SCAN-2・4とENG-CICD-007の受入条件。定義の一致に加え、現在のrevision、検査設定の保護、必須check、迂回を確認する。旧ローカルcopyの一致は実GitHubの強制を証明しない |

独立した`PSB-CICD-003`は追加しません。共通要件の正本はDETECT-001、教材もそのcontrol配下です。CI/CDの入口から教材とpatternへ直接たどれます。Scannerの取得やCI権限の説明を、新controlへ複製しない判断です。

<a id="workflow-analysis-migration--成果物と具体化判断"></a>
### 成果物と具体化判断

必要な成果物は、既存DETECT-001の適用範囲・教材・診断項目の更新、[Workflow analysis gate and reporting](../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)、参照資料、旧項目との対応です。検査、表示、merge可否を分けて選べ、5旧項目と資料の採否を追えることを完了条件とし、この範囲は完了しました。

既存scannerの仕様で検査方法と不足を判断できます。[実効性の基準](ARTIFACT_MODEL.md#主題ごとの具体化判断)に照らし、独自scanner、SARIF parser、固定workflowの再配布は選びません。「実装保留」を残作業にせず、採用対象を選んだ後の実評価と区別します。

DETECT-001の機械可読記録も本文へ揃えました。SCAN-1の特定のchecksum・署名方式、SCAN-3の一律の終了コード`0/1/2`、SCAN-4の全カテゴリfixture要求は、製品非依存の要件へ変更しました。SCAN-7・8のDockSec限定文言も、固有の価値による選定とAI支援の分離へ揃えています。旧DVS参照は移行経緯として保持します。

<a id="workflow-analysis-migration--旧成果物の採否"></a>
### 旧成果物の採否

| 旧成果物 | 扱いと理由 |
|---|---|
| README、control | `split`：既存要件、control配下の教材、新pattern、資料記録へ分ける |
| `secure/workflow.yml`、`insecure/workflow.yml`、旧採用workflow | `split`：検査と公開の分離、権限、成立条件を設計へ残す。二つのjob・SARIF公開・全指摘personaを必須構成にしない |
| `scripts/verify.py` | `retired`（移行対象として）：限定的な行検査と独自SARIF契約を、新controlの検証器として継承しない |
| `tests/test.sh`、3 SARIF fixture、5 expected-results | `retired`（移行対象として）：旧検証器への人工入力と出力で、実scannerやproviderの観測ではない |

旧verifierは`uses`等を行単位で読み、公開条件や権限の文字列があることを確認します。該当条件・権限が適切なjobへ結び付いていることをYAML構造全体から確認する方式ではありません。SARIFではdriver名・version、invocationの成功、resultsを要求しますが、これは旧ローカル契約です。実行の真正性やGitHubの全受入条件の証拠にはなりません。

さらに、現在のzizmor仕様ではSARIF modeは指摘による非0終了を無効にします。対象なしの拒否と部分的な解析失敗も別です。旧Action固定版にはstrict collectionを指定する入力がないため、旧profileをSCAN-3・4適合の完成例にしません。版に応じた導入方法と正常・指摘・障害を実対象で確認する必要があります。

`retired`は旧repositoryのファイルを削除したという意味ではありません。旧testは再実行せず、生成済み`PASS`や旧E3を新成果物の証拠へ転用しません。現在のscanner実行、GitHubの必須check・code scanning・権限・拒否・bypassは未確認です。

<a id="workflow-analysis-migration--旧framework関係と資料"></a>
### 旧framework関係と資料

旧レビュー日は2026-07-27です。以下の2関係は履歴に保持し、新しい配置へ再審査せず継承しません。Framework mappingは116件のままです。

| 旧framework・版 | IDと旧関係 | 旧適用項目 |
|---|---|---|
| GitHub `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24） | GHAS-REF-SECURE-USE：supports / high | SAS-001〜005 |
| OpenSSF OSPS 2026.02.19 | OSPS-VM-06.02：supports / medium | SAS-002・004・005 |

旧`REF-CICD-002`（zizmorの選定）・`REF-CICD-008`（Flatt Securityの比較記事）はこの台帳で旧名を保持します。前者の判断を[REF-WORKFLOW-ANALYSIS-001](../sources/README.md#ref-workflow-analysis-001)へ再編集し、製品挙動は[公式仕様](../sources/README.md#spec-zizmor-workflow-analysis)へ分けました。Actionlint・poutineの旧比較値は新しい実行dependencyや検出能力の証拠にしません。比較記事の選定結論は独立した要件の根拠として採用しません。

固定Actionのコードとversion table、可変のCLI文書、GitHubのSARIF・受入仕様は[Sources](../sources/README.md#spec-zizmor-workflow-analysis)で確認日と限界を区別しています。旧版を現在の推奨版とは扱いません。

<a id="workflow-authority-migration"></a>

<a id="workflow-authority-migration--workflow-authority-minimizationの移行判断"></a>
## Workflow authority minimizationの移行判断

旧[PSB-CICD-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-least-privilege/control.yaml)を、jobの用途と実効権限、開始条件、再利用workflowへの委譲、現在の状態確認へ再編集しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-27です。旧packageの全fileがこのrevisionと一致することを確認しました。

<a id="workflow-authority-migration--旧項目の行き先"></a>
### 旧項目の行き先

| 旧項目 | 行き先・判断 |
|---|---|
| PERM-001 | [JOB-AUTH-1](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)：広い既定権限を暗黙に受け取らず、workflow・jobの権限を明示する。GitHubの`permissions: {}`は製品例へ分ける |
| PERM-002 | JOB-AUTH-2・3：操作・対象と必要な権限を対応させる。旧本文の限界にあった追加PAT・App・host等を、jobの実効権限を読む問いとして明示する。発行・失効やrunner隔離をこのcontrolへ複製しない |
| PERM-003 | JOB-AUTH-4：必要なjobだけへ発行を許可する。Cloudが受け入れる条件と操作はCICD-006へ渡す |
| PERM-004 | JOB-AUTH-5：強い権限を使えるrevision・イベント・承認を実際の強制点へ接続する。全処理に特定ref・Environment・人手承認を一律要求しない |
| PERM-005 | JOB-AUTH-6：呼出元の権限と配送するsecret、呼出先の実jobを確認する。委譲先の権限増加禁止を理由に、呼出元の広い付与を許容しない |
| PERM-006 | JOB-AUTH-7：全対象、実設定、正当な処理、拒否、未確認・取得障害を区別する。静的検査の緑表示を現在の導入証拠にしない |

原則を特定providerのscope名へ縛らず、GitHubでの具体手順へ戻れる構成です。外部コードの版はCICD-001、未信頼側の状態はCICD-005、交換先の権限はCICD-006、runnerはCICD-007、追加認証情報はSOURCE-004、組織方針の実適用はSOURCE-006が所有します。

<a id="workflow-authority-migration--具体化判断"></a>
### 具体化判断

Control、control配下の教材、設計pattern、診断観点を必要な成果物としました。GitHubの設定変更箇所と開始条件は具体化できるため、[GitHub実装](../engineering/cicd-security/purpose-bound-job-authority/implementations/github/README.md)に最短導入、操作からpermissionを選ぶ表、手動の無権限・読取り専用smoke workflow、成功・待機・開始拒否の確認、解除を含めました。

旧例の`make test`を含む一般的なread-only workflowは、未信頼PRの既存実装へリンクします。新しい例は任意のrepositoryで確認できるsourceの取得と、Environment開始条件の確認へ絞り、公開・deploy・cloud交換を実行しません。`permissions: {}`のmarkerへ不要なwrite・OIDCを付けず、実jobに戻す時に必要な操作へ対応させます。

この主題は設定だけから権限の必要性を判定できません。独自のpermission判定器、SaaSの設定を良好とする合成JSON、READMEを確認するだけのテストは追加しません。旧CICD-003のscanner呼出しを移植済みと見せず、静的検査の採否・取得・実行状態は独立した移行候補へ残します。旧危険例も、新しい比較からの判断価値がないためコピーしません。

実装手順から戻した境界は、既定値とjobの最大権限の違い、標準tokenと追加認証情報、stepへの配送と隔離、workflow条件のskipとEnvironmentによる拒否、環境名の誤記・自動作成、呼出元jobで使える設定keyの違いです。「Protected branches only」は保護branchがない時の扱いがあるため、smokeの許可branchは`Selected branches and tags`で明示します。

ローカルではYAMLの読込み、外部Actionの固定参照、shell構文、使い捨てrepositoryへのcopyとGit source確認を検査しました。GitHub CLI 2.95.0のhelpとREST API版2026-03-10の仕様を確認しました。実GitHub設定、tokenの実付与、承認・拒否・bypass、API取得、release・cloud交換は未実行です。SaaSの受入条件は、手順の完成と実導入の完了を分けます。

実評価の再開条件は、許可されたrepository、保護branch・tag、担当者と利用できるEnvironment機能、実jobの用途・scope、追加credential、使い捨て操作対象を選ぶことです。完了条件は、実jobの正常処理と不要な権限・文脈の拒否、設定改変・迂回、現在の対象範囲を観測し、未確認を残すことです。

<a id="workflow-authority-migration--旧framework関係と資料"></a>
### 旧framework関係と資料

旧レビュー日は2026-09-02です。次の6関係は履歴として保持します。Exact項目への新property割当を今回再審査していないため、framework mappingへ自動継承せず、116件を維持します。

| 旧framework・版 | IDと旧関係 | 旧適用項目 |
|---|---|---|
| GitHub `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24） | GHAS-CONCEPT-GITHUB-TOKEN：addresses / high | PERM-001〜005 |
| 同上 | GHAS-REF-SECURE-USE：supports / high | PERM-001〜005 |
| 同上 | GH-ADMIN-ACTIONS-REPOSITORY：related-to / medium | PERM-001・004 |
| 同上 | GH-ADMIN-ACTIONS-ORGANIZATION：related-to / medium | PERM-001・004 |
| OpenSSF OSPS 2026.02.19 | OSPS-AC-04.01：supports / high | PERM-001・005 |
| 同上 | OSPS-AC-04.02：addresses / medium | PERM-002〜005 |

現在の一次資料はGITHUB_TOKEN、workflow権限、OIDC発行、reusable workflow、Environment、設定GETへ分け、[Sources](../sources/README.md#spec-github-workflow-authority)へ採否と限界を記録します。旧`REF-CICD-005`（講演）と`REF-CICD-002`（zizmor）は既存の調査・tool候補です。今回の直接根拠へ混ぜず、旧IDを新資料の別名として残しません。

<a id="workflow-dependency-migration"></a>

<a id="workflow-dependency-migration--workflow-dependency-identityの移行判断"></a>
## Workflow dependency identityの移行判断

旧[PSB-CICD-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/action-sha-pinning/control.yaml)を、直接参照の固定、更新レビュー、内側の追加取得、受入経路へ再編集しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-27です。旧packageの全fileが固定revisionと一致することを確認しました。

<a id="workflow-dependency-migration--旧項目の行き先"></a>
### 旧項目の行き先

| 旧項目 | 行き先・判断 |
|---|---|
| ACT-001 | [WORKFLOW-REF-1・3](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)：外部Actionを確認したcommitへ固定する。40桁の構文はGitHub実装へ分ける |
| ACT-002 | WORKFLOW-REF-1・3：外部reusable workflowの呼出先を固定し、変更をreviewする。GitHubのAction SHA policyだけで済ませない |
| ACT-003 | WORKFLOW-REF-2：直接のcontainer Actionをdigestへ結ぶ。GitのSHA固定とimageの固定を区別する |
| ACT-004 | WORKFLOW-REF-1・2・5：tag、branch、短いSHA、計算式と検査範囲の抜けを受け入れない |
| ACT-005 | WORKFLOW-REF-5：壊れた入力、未検査、tool障害を成功にしない。終了値の数値は実装へ置く |
| ACT-007 | WORKFLOW-REF-3・4：固定commitで読んだsource・実行時取得と未確認を更新reviewへ残す。直接参照の成功から結果を導出しない |

旧項目は6件です。欠番ACT-006を新規に埋めません。旧`NO_OBVIOUS_MUTABILITY`は確認範囲を限定する結果で、依存全体の固定や無害性の証明にはしません。教材では状態名より先に、何を確認したかを日本語で示します。

<a id="workflow-dependency-migration--具体化判断と実装の変更"></a>
### 具体化判断と実装の変更

Control、control配下の教材、設計pattern、診断観点を必要な成果物としました。直接参照の形式は低いコストで実検査できるため、[Python / GitHub実装](../engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)の導入・smoke test・解除も完了条件へ含めました。技術経路が明確な検査を文書だけへ留めず、組織の導入済み判定を作る合成JSONは追加しません。

旧[Python verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/action-sha-pinning/scripts/verify.py)は標準libraryの正規表現で行ごとの`uses:`を読みます。YAML構造は解析せず、参照以外の文字列と実参照を区別する範囲や、構文不正の扱いに限界があります。そのままcopyせず、PyYAML 6.0.3のnode treeを読み、jobのreusable呼出しとstepのAction呼出しに限定しました。Python objectの構築・workflow実行・通信・書換えは行いません。

この判断にはparser依存の取得・hash管理という代償があります。参照は構造から読み、重複key・merge key・custom tag・循環aliasはerrorにします。Flow形式、引用key、折畳みscalar、普通のaliasを検査します。`run`だけの正当なworkflowは対象を読めた参照数ゼロとして認め、旧「usesなしは一律error」を変更しました。空入力・入力不足と同一視しません。

pinact v4.1.1は任意の修正補助として残し、版・source commit・archive checksumを保持しました。Toolの追加wrapper、自動commit、cooldown、reviewdog、全依存の自動解決は作りません。Docker参照の処理をpinactから外しても、直接参照の検査には含めます。固定後の内部取得は教材とpatternのreviewへ渡します。

今回の実測はLinux x86_64 / Python 3.10.4 / PyYAML 6.0.3のhash付き導入とローカルCLIの12件です。成功・可変参照の拒否・YAML不正等のerror、参照形式、全指定対象、非変更、依存不足を確認しました。採用先へcopyする導入とsmoke testも使い捨てdirectoryで確認しました。PinactのLinux archive SHA-256、binary版・helpを確認しています。実APIによる自動修正、remote SHA・release・出所、実Actionの内容・追加取得、GitHub上のcheck・policy・review・迂回拒否、macOSは未確認です。本PJ自体には`.github/workflows`がなく、その入力はerrorになりました。

実装からcontrol・patternへ戻した境界は、構文と出所の違い、Action policyとreusable呼出しの違い、検査対象内のゼロと入力不足の違い、検査script自身の改変、直接参照と内部取得の違いです。組織への方針適用はSOURCE-006、jobの実効権限は旧CICD-004の次の主題へ渡します。

<a id="workflow-dependency-migration--旧framework関係と資料の採否"></a>
### 旧framework関係と資料の採否

旧レビュー日は2026-09-01です。以下の3関係を履歴として保持します。今回exact仕様項目へのproperty割当を再審査していないため、新しいframework mappingへ自動継承しません。116件を維持します。

| 旧framework・版 | 旧IDと関係 | 旧適用項目 |
|---|---|---|
| GitHub `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24） | GHAS-REF-SECURE-USE：supports / high | ACT-001・002・004 |
| MITRE ATT&CK v19.1 | T1195.001：mitigates / medium | ACT-001〜004 |
| NIST SSDF 1.1（SP 800-218, 2022） | PW.4.1：supports / medium | ACT-001〜004・007 |

一次資料は現在のGitHub secure use・workflow構文・Actions policy、Docker digest仕様へ置き直し、可変Web文書の確認日と再確認条件を[Sources](../sources/README.md#spec-workflow-dependency-references)へ残します。旧READMEが参照するPalo Alto NetworksのUnpinnable Actionsは内部取得の問題を知る履歴として保持し、調査中の比率や全ecosystemへの一般化を新controlの根拠にしません。旧`REF-CICD-001`（Advisory Database）は版と脆弱性の照合に関する隣接課題、旧`REF-CICD-005`（講演）は既存の調査入力として残し、今回の直接参照検査が脆弱性分析まで行うとはしません。新資料IDは役割に合わせ、旧IDを別名として登録しません。

<a id="workflow-input-migration"></a>

<a id="workflow-input-migration--workflow-input-handlingの移行判断"></a>
## Workflow input handlingの移行判断

旧[PSB-CICD-002](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-command-injection)を、外部入力が命令へ変わる経路と、呼出先までデータとして扱う判断へ再編集しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-27です。旧packageの14 fileがこのrevisionと一致することを確認しました。

<a id="workflow-input-migration--旧項目の行き先"></a>
### 旧項目の行き先

| 旧項目 | 行き先・判断 |
|---|---|
| INJ-001 | [CI-INPUT-1・2](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md)：値を変更できる主体と到達性、命令とデータの分離。全`run:`の直接式を禁止する規則は組織が選ぶprofileへ分ける |
| INJ-002 | CI-INPUT-1〜5：環境変数だけを唯一の方式にせず、引数の保持、再評価、操作・対象の選択、呼出先への受け渡しを分ける。旧本文にあった許可リストと呼出先の限界を明示し、引数注入はOWASP資料で補う |
| INJ-003 | CI-INPUT-6：表示用の式と実行へ流れる値を区別する。宣言的な欄全体を安全と認定しない |
| INJ-004 | CI-INPUT-6：対象不足や未対応構文を問題なしにしない。検査の取得・実行・証拠と変更保護の詳細はDETECT-001や既存の受入設計へ渡す |

旧本文の成立条件と被害差は教材へ残しました。PRコードをすでに同じ権限で実行するjobと、metadataだけを扱うjobでは、この欠陥によって増える実行能力が違います。Read-onlyを無害とせず、欠陥だけで必ずrepositoryやcloudを乗っ取れるとも扱いません。旧外部事例・SITF・CWE・講演等を直接要件の根拠へ一律に追加しません。

<a id="workflow-input-migration--成果物と具体化判断"></a>
### 成果物と具体化判断

[Control](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md)、control配下の教材、[設計pattern](../engineering/cicd-security/workflow-data-and-command-boundary/README.md)、診断チェックリストを必要な成果物としました。教材の短いstep断片で「式の補間」と「固定命令への変数の引数」を比較し、patternで方式と代償を判断できます。

利用者が指定した[実効性の基準](ARTIFACT_MODEL.md#主題ごとの具体化判断)に照らし、今回は独自実装を追加しません。既存のGitHubガイダンスとshell・呼出先の仕様で入力の渡し方を判断でき、独自scannerの維持や中央配布が解消する需要は未指定です。主題は文書と診断項目で完了とし、「実装保留」を残作業にしません。実環境での診断・導入は未実施です。

| 旧成果物 | 扱いと理由 |
|---|---|
| README、control、secure／insecure workflow | `split`：原則、教材の比較、選択条件へ分ける。実行workflowを新設するだけの移植はしない |
| `scripts/verify.py`、`secure/local-gate.yml` | `retired`（移行対象として）：全直接式禁止の限定policyと配布例であり、control全体を検査しない。独自scannerを今回の必須成果にしない |
| `scripts/self-test.sh`、`tests/test.sh`、`expected-results/` | `retired`（移行対象として）：旧scannerの回帰試験と出力で、新構造のcontrolへテストコードや成功結果を持ち込まない |
| `docs/CENTRAL_GATE_POC.md` | `retired`（移行対象として）：同じscannerの配布方式であり、検出能力や組織強制は増えない。多数repositoryへの具体的な導入需要なしに配布機構を作らない |
| 旧`AGENTS.md` | `retired`：旧packageの編集手順であり、新しい読者向け成果物ではない |

ここでの`retired`は旧repositoryのファイルを削除したという意味ではありません。行scannerはYAML構造全体を解析せず、通常の一部の`run`表現だけを読む方式です。構文の限定と評価不能の扱いは旧コードから確認しましたが、旧testの成功や生成済み`PASS`を新成果物の証拠にはしません。

将来、自動確認に具体的な不足が見つかった場合は、既存scannerの対応範囲を先に確認します。独自実装を選ぶには、採用対象と未対応構文、保守責任、既存方式との差、正常・欠陥・検査障害を観測する方法を決めます。全shell解析や中央配布を、この主題の既定の次作業にはしません。

<a id="workflow-input-migration--旧framework関係"></a>
### 旧framework関係

旧レビュー日は2026-07-27です。次の3関係は履歴として残し、新しい特性へ再審査せず継承しません。Framework mappingは116件のままです。

| 旧framework・版 | IDと旧関係 | 旧適用項目 |
|---|---|---|
| GitHub `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24） | GHAS-CONCEPT-SCRIPT-INJECTIONS：mitigates / high | INJ-001 |
| 同上 | GHAS-REF-SECURE-USE：supports / high | INJ-001・002 |
| OpenSSF OSPS 2026.02.19 | OSPS-BR-01.01：verifies / high | INJ-001・002 |

製品ガイダンスを参照することと、framework項目の検証完了は別です。特に旧`verifies`を、チェックリストの記載だけで引き継ぎません。既存のASVS方針に反して一般的なapplication injection controlを増やす移行でもありません。

一次資料の版・確認日、Bash公式Web本文を取得できなかった範囲、採否は[Sources](../sources/README.md#spec-github-workflow-input)へ記録しました。確認したのは文書・参照本文・ローカルに配布されたBash仕様とリンクです。GitHubでの実行・拒否、全呼出先の挙動、scannerの導入・CI強制は確認していません。
