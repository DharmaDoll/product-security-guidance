# Workflow input handlingの移行判断

旧[PSB-CICD-002](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/actions-command-injection)を、外部入力が命令へ変わる経路と、呼出先までデータとして扱う判断へ再編集しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-27です。旧packageの14 fileがこのrevisionと一致することを確認しました。

## 旧項目の行き先

| 旧項目 | 行き先・判断 |
|---|---|
| INJ-001 | [CI-INPUT-1・2](../controls/records/cicd-security/psb-cicd-002-workflow-input-handling/README.md)：値を変更できる主体と到達性、命令とデータの分離。全`run:`の直接式を禁止する規則は組織が選ぶprofileへ分ける |
| INJ-002 | CI-INPUT-1〜5：環境変数だけを唯一の方式にせず、引数の保持、再評価、操作・対象の選択、呼出先への受け渡しを分ける。旧本文にあった許可リストと呼出先の限界を明示し、引数注入はOWASP資料で補う |
| INJ-003 | CI-INPUT-6：表示用の式と実行へ流れる値を区別する。宣言的な欄全体を安全と認定しない |
| INJ-004 | CI-INPUT-6：対象不足や未対応構文を問題なしにしない。検査の取得・実行・証拠と変更保護の詳細はDETECT-001や既存の受入設計へ渡す |

旧本文の成立条件と被害差は教材へ残しました。PRコードをすでに同じ権限で実行するjobと、metadataだけを扱うjobでは、この欠陥によって増える実行能力が違います。Read-onlyを無害とせず、欠陥だけで必ずrepositoryやcloudを乗っ取れるとも扱いません。旧外部事例・SITF・CWE・講演等を直接要件の根拠へ一律に追加しません。

## 成果物と具体化判断

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

## 旧framework関係

旧レビュー日は2026-07-27です。次の3関係は履歴として残し、新しい特性へ再審査せず継承しません。Framework mappingは116件のままです。

| 旧framework・版 | IDと旧関係 | 旧適用項目 |
|---|---|---|
| GitHub `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24） | GHAS-CONCEPT-SCRIPT-INJECTIONS：mitigates / high | INJ-001 |
| 同上 | GHAS-REF-SECURE-USE：supports / high | INJ-001・002 |
| OpenSSF OSPS 2026.02.19 | OSPS-BR-01.01：verifies / high | INJ-001・002 |

製品ガイダンスを参照することと、framework項目の検証完了は別です。特に旧`verifies`を、チェックリストの記載だけで引き継ぎません。既存のASVS方針に反して一般的なapplication injection controlを増やす移行でもありません。

一次資料の版・確認日、Bash公式Web本文を取得できなかった範囲、採否は[Sources](../sources/README.md#spec-github-workflow-input)へ記録しました。確認したのは文書・参照本文・ローカルに配布されたBash仕様とリンクです。GitHubでの実行・拒否、全呼出先の挙動、scannerの導入・CI強制は確認していません。
