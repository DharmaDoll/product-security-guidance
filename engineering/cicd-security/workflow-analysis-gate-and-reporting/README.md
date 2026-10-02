# ENG-CICD-007: Workflow analysis gate and reporting

Workflowの変更をmergeしてよいか決める検査と、指摘を画面へ表示する処理を分けます。CIの設計者が、**何を検査し、どの結果でmergeを止め、誰が結果を書き込むか**を選ぶpatternです。

例えば、PRでworkflowが変更され、scannerが指摘をSARIFへ出したとします。Jobは成功し、Security画面にも結果が表示されました。それでも、mergeを止める条件がなければ変更は通ります。検査、表示、受入判断には別々の接続が必要です。

## 検査対象と、検査を決める側を分ける

```text
変更候補のrevision・workflow・Action定義（検査するデータ）
  → 保護された検査定義・scanner・policyで解析
  → 対象、収集範囲、正常完了、指摘、例外を照合
  → 必須の受入条件でmergeを許可・拒否

結果の表示が必要な場合
  → 信頼できるrevisionから別の処理を開始
  → 限定した権限で結果を公開
```

候補のworkflowを解析することと、そのworkflowや呼出先を実行することを分けます。Scanner自体の侵害やparserの欠陥もあり得るため、検査jobには公開用credentialや永続runnerを与えません。[Toolの取得と証拠の扱い](../../detection-verification/scanner-acquisition-and-evidence-boundary/README.md)が共通部分を定めます。

検査対象の変更と同時に、scannerの起動、対象path、設定、重大度のしきい値、ignoreを変更できる経路も確認します。検査を外せるPRが同じcheck名で成功を返せるなら、必須checkの指定だけでは強制できません。検査定義と例外の変更を別途保護し、採用するCIの機能で迂回を拒否できるか確認します。

## 方式を選ぶ

| 方式 | 向く場面 | 確認する代償・失敗経路 |
|---|---|---|
| CLIの検査結果を必須checkへ接続する | Mergeを止めることが目的で、結果の履歴画面は不要 | 採用版・出力modeの終了状態、対象不足、解析失敗をcheckへ反映する。表示用のSARIF出力をそのまま判定に使わない |
| 必須checkと、信頼できるrevisionからの結果公開を分ける | 指摘を止める処理に加え、Security画面や履歴が必要 | 公開側だけに必要な書込権限を渡す。公開の成功・失敗を検査結果と混同せず、公開失敗には別の対応を決める |
| Providerのcode scanning結果を受入条件にする | 対象の契約・機能でtool・しきい値を指定できる | 対象revision、必要tool、解析中・結果不足・障害、bypassを確認する。SARIFをuploadしただけではmerge保護にならない |

二つのjobやSARIFの保存を全repositoryへ要求しません。結果の表示が不要なら、必須checkだけの構成を選べます。PRのartifactを権限付きjobへ渡す場合は[Untrusted PR boundary](../untrusted-pr-boundary/README.md)の検証が必要です。PRが作った結果を無条件に正式な検査結果へ昇格させません。

## GitHub Actionsとzizmorを選ぶ場合

[zizmorの仕様記録](../../../sources/README.md#spec-zizmor-workflow-analysis)は、解析対象、収集、ignore、終了状態の確認先です。SARIF modeでは指摘があっても終了コードが0になり得ます。通常のCLI判定と表示用の出力を区別してください。

対象が一つもない状態と、一部の定義を読み込めなかった状態も別です。`fail-on-no-inputs`だけでは部分的な解析失敗を扱えません。`strict-collection`等の対応、対象一覧との一致、候補内の設定・inline ignoreが検査を弱める経路を、採用版で確認します。旧固定Action v0.6.1はstrict collectionの指定を公開していないため、この要件を満たす導入設定としてそのまま継承しません。

結果公開を選ぶ時は[GitHubの仕様記録](../../../sources/README.md#spec-github-scanning-acceptance)を確認します。`security-events: write`等は公開に必要な処理だけへ与え、`main`という名前だけで保護済みとは判断しません。公開する情報、閲覧者、保持範囲も決めます。一般的な証拠の最小化は[SCAN-5](../../../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)へ接続します。

## 診断で確認する項目（異常時テスト）

これは設計レビュー・脆弱性診断で使うチェックリストです。実GitHubで確認した結果ではありません。

| 確認すること | できてはいけないこと・見る結果 |
|---|---|
| 指摘があるSARIFを出力する経路 | 出力成功だけで必須checkが合格する。指摘の受入条件が別に働くか確認する |
| 対象なし・一部の解析不能・timeout | 正常に検査した対象と漏れた対象を区別せず、問題なしにする |
| PRが検査定義・path・設定・ignoreを変更する | 必須check名を残したまま検査を消す、または承認されていない例外を使う |
| 必須checkの欠落・skip・別revision・別の発行元 | 必要な検査が完了していない変更をmergeできる |
| Fork PRや別イベントから結果公開を起動する | 未信頼のコードや状態が書込権限、secret、保護環境へ届く |
| 公開失敗、未設定tool、解析中の結果 | 結果が届かなかった状態を指摘なしと表示し、受入条件も通る |
| 候補から呼ばれるscriptや動的取得 | 定義の静的検査だけで、呼出先の挙動や実効権限まで確認したと扱う |

## Controlの配置と限界

[DETECT-001](../../../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/README.md)がtool・policy・対象・実行状態・結果・例外の要件を定め、[その教材](../../../controls/records/detection-verification/psb-detect-001-scanner-evidence-trust-boundary/learning.md#workflowの検査が成功したのに変更を止められない)が今回のシナリオを説明します。[CICD-001](../../../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)は外部コードの参照、[CICD-004](../../../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)はjobの権限、[CICD-005](../../../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)は未信頼の状態との分離を担当します。

主なlayerはplatform and infrastructure、直接扱う攻撃段階は5です。段階2の変更保護と段階6の権限を前提に、段階7の実行環境と段階12の検知・調査へ渡します。定義への指摘がないことは、呼出先の完全な解析、実行時の隔離、全体の安全性を証明しません。

今回は既存scannerの仕様と診断項目で判断できるため、独自scanner・SARIF parser・導入workflowは作りません。採用repositoryでの導入・拒否は未確認です。[旧CICD-003の採否](../../../docs/WORKFLOW_ANALYSIS_MIGRATION.md)と[参照資料](../../../sources/README.md#ref-workflow-analysis-001)を参照してください。
