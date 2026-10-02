# Workflow authority minimizationの移行判断

旧[PSB-CICD-004](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-least-privilege/control.yaml)を、jobの用途と実効権限、開始条件、再利用workflowへの委譲、現在の状態確認へ再編集しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-27です。旧packageの全fileがこのrevisionと一致することを確認しました。

## 旧項目の行き先

| 旧項目 | 行き先・判断 |
|---|---|
| PERM-001 | [JOB-AUTH-1](../controls/records/cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)：広い既定権限を暗黙に受け取らず、workflow・jobの権限を明示する。GitHubの`permissions: {}`は製品例へ分ける |
| PERM-002 | JOB-AUTH-2・3：操作・対象と必要な権限を対応させる。旧本文の限界にあった追加PAT・App・host等を、jobの実効権限を読む問いとして明示する。発行・失効やrunner隔離をこのcontrolへ複製しない |
| PERM-003 | JOB-AUTH-4：必要なjobだけへ発行を許可する。Cloudが受け入れる条件と操作はCICD-006へ渡す |
| PERM-004 | JOB-AUTH-5：強い権限を使えるrevision・イベント・承認を実際の強制点へ接続する。全処理に特定ref・Environment・人手承認を一律要求しない |
| PERM-005 | JOB-AUTH-6：呼出元の権限と配送するsecret、呼出先の実jobを確認する。委譲先の権限増加禁止を理由に、呼出元の広い付与を許容しない |
| PERM-006 | JOB-AUTH-7：全対象、実設定、正当な処理、拒否、未確認・取得障害を区別する。静的検査の緑表示を現在の導入証拠にしない |

原則を特定providerのscope名へ縛らず、GitHubでの具体手順へ戻れる構成です。外部コードの版はCICD-001、未信頼側の状態はCICD-005、交換先の権限はCICD-006、runnerはCICD-007、追加認証情報はSOURCE-004、組織方針の実適用はSOURCE-006が所有します。

## 具体化判断

Control、control配下の教材、設計pattern、診断観点を必要な成果物としました。GitHubの設定変更箇所と開始条件は具体化できるため、[GitHub実装](../engineering/cicd-security/purpose-bound-job-authority/implementations/github/README.md)に最短導入、操作からpermissionを選ぶ表、手動の無権限・読取り専用smoke workflow、成功・待機・開始拒否の確認、解除を含めました。

旧例の`make test`を含む一般的なread-only workflowは、未信頼PRの既存実装へリンクします。新しい例は任意のrepositoryで確認できるsourceの取得と、Environment開始条件の確認へ絞り、公開・deploy・cloud交換を実行しません。`permissions: {}`のmarkerへ不要なwrite・OIDCを付けず、実jobに戻す時に必要な操作へ対応させます。

この主題は設定だけから権限の必要性を判定できません。独自のpermission判定器、SaaSの設定を良好とする合成JSON、READMEを確認するだけのテストは追加しません。旧CICD-003のscanner呼出しを移植済みと見せず、静的検査の採否・取得・実行状態は独立した移行候補へ残します。旧危険例も、新しい比較からの判断価値がないためコピーしません。

実装手順から戻した境界は、既定値とjobの最大権限の違い、標準tokenと追加認証情報、stepへの配送と隔離、workflow条件のskipとEnvironmentによる拒否、環境名の誤記・自動作成、呼出元jobで使える設定keyの違いです。「Protected branches only」は保護branchがない時の扱いがあるため、smokeの許可branchは`Selected branches and tags`で明示します。

ローカルではYAMLの読込み、外部Actionの固定参照、shell構文、使い捨てrepositoryへのcopyとGit source確認を検査しました。GitHub CLI 2.95.0のhelpとREST API版2026-03-10の仕様を確認しました。実GitHub設定、tokenの実付与、承認・拒否・bypass、API取得、release・cloud交換は未実行です。SaaSの受入条件は、手順の完成と実導入の完了を分けます。

実評価の再開条件は、許可されたrepository、保護branch・tag、担当者と利用できるEnvironment機能、実jobの用途・scope、追加credential、使い捨て操作対象を選ぶことです。完了条件は、実jobの正常処理と不要な権限・文脈の拒否、設定改変・迂回、現在の対象範囲を観測し、未確認を残すことです。

## 旧framework関係と資料

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
