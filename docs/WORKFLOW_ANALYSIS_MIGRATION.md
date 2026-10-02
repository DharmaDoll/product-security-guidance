# Workflow analysisの移行判断

旧[PSB-CICD-003](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-static-analysis)の5項目を、既存controlとworkflow固有の設計へ配置しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-27です。旧packageの14 fileと旧`.github/workflows/actions-security.yml`が固定revisionに一致することを確認しました。

## 旧項目の行き先

| 旧項目 | 行き先・判断 |
|---|---|
| SAS-001：scanner固定 | [DETECT-001のSCAN-1・2](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)と[CICD-001](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)。Tool、実行するimage、policyを区別し、旧固定値を現在の推奨値にしない |
| SAS-002：PR gate | SCAN-3・4と[CICD-004](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)・[CICD-005](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)。候補をデータとして解析し、権限を分け、指摘・障害・未検査を受入条件へ接続する |
| SAS-003：信頼できる側でSARIF公開 | [ENG-CICD-007](../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)の方式選択とCICD-004・005。結果公開は必要な場合に選び、`main`へのpush条件を保護の証拠にしない |
| SAS-004：結果の三状態 | SCAN-3・4と[DETECT-001の教材](../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/learning.md)。Scanner・版・出力modeごとの終了状態と、正常完了・対象範囲・指摘を照合する |
| SAS-005：採用workflowの照合 | SCAN-2・4とENG-CICD-007の受入条件。定義の一致に加え、現在のrevision、検査設定の保護、必須check、迂回を確認する。旧ローカルcopyの一致は実GitHubの強制を証明しない |

独立した`PSB-CICD-003`は追加しません。共通要件の正本はDETECT-001、教材もそのcontrol配下です。CI/CDの入口から教材とpatternへ直接たどれます。Scannerの取得やCI権限の説明を、新controlへ複製しない判断です。

## 成果物と具体化判断

必要な成果物は、既存DETECT-001の適用範囲・教材・診断項目の更新、[Workflow analysis gate and reporting](../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)、参照資料、旧項目との対応です。検査、表示、merge可否を分けて選べ、5旧項目と資料の採否を追えることを完了条件とし、この範囲は完了しました。

既存scannerの仕様で検査方法と不足を判断できます。[実効性の基準](ARTIFACT_MODEL.md#主題ごとの具体化判断)に照らし、独自scanner、SARIF parser、固定workflowの再配布は選びません。「実装保留」を残作業にせず、採用対象を選んだ後の実評価と区別します。

DETECT-001の機械可読記録も本文へ揃えました。SCAN-1の特定のchecksum・署名方式、SCAN-3の一律の終了コード`0/1/2`、SCAN-4の全カテゴリfixture要求は、製品非依存の要件へ変更しました。SCAN-7・8のDockSec限定文言も、固有の価値による選定とAI支援の分離へ揃えています。旧DVS参照は移行経緯として保持します。

## 旧成果物の採否

| 旧成果物 | 扱いと理由 |
|---|---|
| README、control | `split`：既存要件、control配下の教材、新pattern、資料記録へ分ける |
| `secure/workflow.yml`、`insecure/workflow.yml`、旧採用workflow | `split`：検査と公開の分離、権限、成立条件を設計へ残す。二つのjob・SARIF公開・全指摘personaを必須構成にしない |
| `scripts/verify.py` | `retired`（移行対象として）：限定的な行検査と独自SARIF契約を、新controlの検証器として継承しない |
| `tests/test.sh`、3 SARIF fixture、5 expected-results | `retired`（移行対象として）：旧検証器への人工入力と出力で、実scannerやproviderの観測ではない |

旧verifierは`uses`等を行単位で読み、公開条件や権限の文字列があることを確認します。該当条件・権限が適切なjobへ結び付いていることをYAML構造全体から確認する方式ではありません。SARIFではdriver名・version、invocationの成功、resultsを要求しますが、これは旧ローカル契約です。実行の真正性やGitHubの全受入条件の証拠にはなりません。

さらに、現在のzizmor仕様ではSARIF modeは指摘による非0終了を無効にします。対象なしの拒否と部分的な解析失敗も別です。旧Action固定版にはstrict collectionを指定する入力がないため、旧profileをSCAN-3・4適合の完成例にしません。版に応じた導入方法と正常・指摘・障害を実対象で確認する必要があります。

`retired`は旧repositoryのファイルを削除したという意味ではありません。旧testは再実行せず、生成済み`PASS`や旧E3を新成果物の証拠へ転用しません。現在のscanner実行、GitHubの必須check・code scanning・権限・拒否・bypassは未確認です。

## 旧framework関係と資料

旧レビュー日は2026-07-27です。以下の2関係は履歴に保持し、新しい配置へ再審査せず継承しません。Framework mappingは116件のままです。

| 旧framework・版 | IDと旧関係 | 旧適用項目 |
|---|---|---|
| GitHub `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24） | GHAS-REF-SECURE-USE：supports / high | SAS-001〜005 |
| OpenSSF OSPS 2026.02.19 | OSPS-VM-06.02：supports / medium | SAS-002・004・005 |

旧`REF-CICD-002`（zizmorの選定）・`REF-CICD-008`（Flatt Securityの比較記事）はこの台帳で旧名を保持します。前者の判断を[REF-WORKFLOW-ANALYSIS-001](../sources/README.md#ref-workflow-analysis-001)へ再編集し、製品挙動は[公式仕様](../sources/README.md#spec-zizmor-workflow-analysis)へ分けました。Actionlint・poutineの旧比較値は新しい実行dependencyや検出能力の証拠にしません。比較記事の選定結論は独立した要件の根拠として採用しません。

固定Actionのコードとversion table、可変のCLI文書、GitHubのSARIF・受入仕様は[Sources](../sources/README.md#spec-zizmor-workflow-analysis)で確認日と限界を区別しています。旧版を現在の推奨版とは扱いません。
