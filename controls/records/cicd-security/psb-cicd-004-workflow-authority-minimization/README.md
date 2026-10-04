# PSB-CICD-004: Workflow authority minimization

テストするだけのjobに、releaseの公開権限も付いている。依存やActionが侵害されると、テスト結果を変えるだけでなく、ソースや公開物まで書き換えられます。CIの設計者とレビュー担当者が、**各jobに、その処理で必要な権限だけを渡しているか**を判断するcontrolです。

## 守るものと直接の失敗

守るものは、CIから操作できるソース、package、release、deployment、cloud資源と認証情報です。侵害されたAction・依存、悪意あるコード、権限を広く付ける設定ミスによって、jobの本来の処理に不要な操作が可能になることが直接の失敗です。

対象はjobへの権限付与、追加認証情報の配送、起動できる文脈、再利用workflowへの委譲です。ソース管理の組織方針、認証情報の発行・失効、cloud側の信頼条件、runnerの隔離は隣接するcontrolへ渡します。

## 満たすべきこと

| 特性 | 確認すること |
|---|---|
| JOB-AUTH-1 | Workflowとjobの権限を明示する。未指定時に広い既定権限を受け取らず、追加する権限を見える差分にする |
| JOB-AUTH-2 | 各権限を、実際の操作・対象・必要なアクセスへ対応させる。同じjob内のコードへ共有してよいか確認し、信頼度や用途が違う処理を分離する |
| JOB-AUTH-3 | 標準token以外の認証情報、秘密情報、環境、host・networkへの到達も、そのjobの実効権限として確認する。標準tokenの制限で別の権限を制限したと扱わない |
| JOB-AUTH-4 | OIDC等のtoken発行を、必要な交換処理を行うjobへ限定する。発行の許可と、交換先が受け入れる条件・操作権限を分ける |
| JOB-AUTH-5 | 残した強い権限を使えるrevision・イベント・承認条件を決め、実際の強制点へ接続する。Workflow内の名前や条件だけで保護済みとしない |
| JOB-AUTH-6 | 再利用workflowの呼出元で権限と渡す秘密情報を限定し、呼出先・さらにその先を確認する。委譲先が必要以上の権限を自動で減らすと期待しない |
| JOB-AUTH-7 | 全対象の設定と現在の実行条件を照合し、必要な処理の成功と不要な権限の拒否を区別して確認する。省略・取得障害・古い設定を「最小権限」に変えない |

操作に必要な権限と、jobを開始できる条件の両方で範囲を狭めます。全jobへの同じ承認方式や、全製品への特定のpermission名を要求しません。根拠は[SPEC-GITHUB-WORKFLOW-AUTHORITY](../../../../sources/README.md#spec-github-workflow-authority)と[本PJの解釈](../../../../sources/README.md#ref-workflow-authority-001)へ記録しています。

## 診断で確認する項目（異常時テスト）

以下は診断やレビューで使う確認項目です。記載を実施済みの結果にはしません。

| 試す条件 | できてはいけないこと・確認する扱い |
|---|---|
| 全体の既定権限を広げる、jobの指定を消す | 処理に不要な権限が暗黙に復活する。全jobの設定と実行時の付与を確認する |
| 標準tokenはread-onlyだが、PAT・App・cloud keyも渡す | 標準tokenの結果だけで書込み不能と判断する。追加認証情報の対象・権限も確認する |
| Secretを使うstepより前に未信頼のコードを置く | Stepへの配送指定だけで隔離済みとする。共有状態を介した後続への影響を確認する |
| テストjobへtoken発行を許す | 不要なjobから交換可能なtokenを取得できる。発行条件と交換先の判断を別に確認する |
| 未承認revision・別イベントから権限付き処理を起動する | 名前がmainやreleaseであるだけで通る。保護された変更・開始条件の実値を確認する |
| 保護対象の環境を誤記・削除する、管理者が迂回する | 別の無保護環境へ流れる、または無制限に迂回できる。設定と拒否・待機状態を確認する |
| 再利用workflowへ全secret・広い権限を委譲する | 呼出先の安全性を信じて不要な権限を渡す。必要な値と各呼出しを確認する |
| Workflow一覧や設定取得、検査に失敗する | 確認できない対象を良好な結果へ含める。未確認と障害を残す |

## 隣接する成果物

[CICD-001](../psb-cicd-001-workflow-dependency-identity/README.md)は呼ぶ外部コードの版、[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)は未信頼PRと権限付き処理の境界、[CICD-006](../psb-cicd-006-workload-federation-boundary/README.md)はcloud側の交換条件、[CICD-007](../psb-cicd-007-runner-lifecycle-isolation/README.md)はrunnerに残る状態を扱います。

[CICD-002](../psb-cicd-002-workflow-input-handling/README.md)は題名・入力値が命令へ変わる経路を扱います。Jobの権限を減らすことと、入力から意図しない命令を作らないことを分けます。

[SOURCE-004](../../source-protection/psb-source-004-source-access-credential-lifecycle/README.md)へ追加認証情報の発行・失効を、[SOURCE-006](../../source-protection/psb-source-006-source-organization-security-posture/README.md)へ組織方針の実適用を渡します。静的検査の成功だけで操作上の最小性や導入済み状態は認定しません。

[教材](learning.md)で「read-onlyでも別の権限が残る」例を追い、[設計pattern](../../../../engineering/cicd-security/purpose-bound-job-authority/README.md)で処理を分ける場所を選べます。[GitHub実装例](../../../../engineering/cicd-security/purpose-bound-job-authority/implementations/github/README.md)は設定、最短導入、安全なsmoke test、解除を示します。旧項目の行き先は[移行判断](../../../../docs/MIGRATION_CI_CD.md#workflow-authority-migration)にあります。
