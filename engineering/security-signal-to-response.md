# 問題の発見から対応・再開まで

設計ID: `ENG-GOV-001`。PSIRT、SOC、開発・基盤・運用担当が、影響調査と実際の処置をつなぐための設計です。Control IDは`PSB-`を省略しています。

公開アプリが内部の管理APIを呼び出したという通知が届いたとします。同時に、そのアプリが使う依存部品の脆弱性情報も見つかりました。部品を含むだけでは侵害されたとは言えず、通知が来ただけでも停止する対象は確定しません。一方、内部操作が続いているなら、全製品の調査完了を待つ間に被害が広がります。

この場面では、**影響する製品を探す作業と、進行中の被害を止める作業を並行し、根拠・対象・未確認範囲を共有する**構成を選びます。通知の重大度だけを広範囲の停止権限へ変えません。

## 二つの入口と、担当者間の受け渡し

```mermaid
flowchart TD
  A["報告・スキャナーの指摘・公開資産の差分<br/>GOV-006・009・010"]
  B["依存から製品・稼働先を調査<br/>REL-003・004 / GOV-001"]
  C["記録と検知から、不正操作の対象を調査<br/>GOV-011・012 / CONTAINER-004"]
  D["製品への影響・優先度・担当・期限<br/>GOV-003"]
  E["事前に決めた条件で封じ込め<br/>GOV-004・012 / CONTAINER-003・006"]
  F["原因の修正と、稼働成果物の置換<br/>GOV-008・005 / BUILD-002・003 / REL-001"]
  G["利用者への案内と訂正<br/>GOV-007"]
  H["再開判断・残る調査・検知の改善<br/>GOV-005・011・012"]
  A -->|依存に関する問題| B
  B --> D
  A -->|自社コード等の脆弱性| D
  C -->|脆弱性への対応も必要| D
  C --> E
  D --> F
  E --> F
  D --> G
  F --> G
  F --> H
  H --> C
```

[GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)は依存に関する影響調査のControlです。アプリへの侵入全般をSBOM検索で調べるものではありません。不正操作から始める場合は、下の[封じ込めと再開](#intrusion-containment)へ進みます。認証情報の漏えいが分かった場合は、[GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)の停止と調査を並行します。

公開資産の差分は、まず管理責任と意図した公開かを確認します。すべてを脆弱性や侵害として扱うのではなく、台帳の更新、公開設定の是正、追加調査へ振り分けます。図は問題に応じて選ぶ経路であり、全案件を全工程へ通す手順ではありません。

| 受け渡し | 次の担当が判断するために渡すもの | 取り違えやすいこと | Control |
|---|---|---|---|
| 発見 → 調査 | 報告・観測元、対象候補、時刻、調査できた範囲と失敗 | 重複という理由で、新しい影響版や移動先を捨てる | [GOV-006](../controls/records/governance-operations/psb-gov-006-vulnerability-report-intake/README.md)・[GOV-009](../controls/records/governance-operations/psb-gov-009-scanner-evidence-trust-boundary/README.md)・[GOV-010](../controls/records/governance-operations/psb-gov-010-external-attack-surface-reconciliation/README.md)・[GOV-012](../controls/records/governance-operations/psb-gov-012-detection-and-response-readiness/README.md) |
| 調査 → 対応担当 | 正確な製品・版・成果物・稼働先、影響根拠、不明点、担当者と期限 | 検索0件を全製品の非該当にする | [GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)・[GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)・[GOV-011](../controls/records/governance-operations/psb-gov-011-security-event-evidence/README.md) |
| 初動 → 復旧担当 | 止めた権限・通信・公開物、残る接続や移動先、通常業務への影響 | 元のアプリを止めただけで、別環境の権限も止まったとする | [GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)・[GOV-012](../controls/records/governance-operations/psb-gov-012-detection-and-response-readiness/README.md) |
| 修正 → 配布・置換 | 確認した悪用条件、対象版、修正を含む成果物のdigest、未確認版 | 主ブランチのテスト成功を、配布版すべての修正とする | [GOV-008](../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md)・[GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md) |
| 対応 → 利用者 | 影響版、回避・更新方法、提供状態、連絡の成功と未到達先 | 修正版の公開を通知完了とする | [GOV-007](../controls/records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/README.md)・[GOV-008](../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md) |
| 再開 → 継続監視 | 再開した範囲、残る調査、必要な記録・検知、次の確認担当 | 成果物の置換完了をインシデント全体の復旧とする | [GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)・[GOV-011](../controls/records/governance-operations/psb-gov-011-security-event-evidence/README.md)・[GOV-012](../controls/records/governance-operations/psb-gov-012-detection-and-response-readiness/README.md) |

調査担当は検索条件と範囲、ビルド担当は成果物との対応、運用担当は実際の稼働、対応責任者は処置の権限と影響を確認します。収集・分析基盤が示す識別子も、元の記録と照合してから使います。

<a id="report-to-remedy-example"></a>

## 運用例：外部からの報告を修正・通知までつなぐ

研究者からサポート窓口へ「他の組織の請求書を閲覧できる」という報告が届いた場面を考えます。製品は自社運用のSaaSと顧客が運用する配布版を持ち、同じAPIを使っています。以下は架空の判断例で、実際の製品・対応実績ではありません。

この例の目的は、受付、開発、運用、顧客対応の間で案件を落とさないことです。既存の非公開ticketと制限された証拠保管先で始められます。受付や通知の専用システムを新しく作ることは前提にしません。

### 最初に担当と引き渡し先を決める

PSIRT担当を案件の調整責任者とし、各工程の担当者が引き受けたことを確認します。小規模な組織では兼任できますが、重要な公開内容や復旧判断を誰が確認したかは残します。

| 工程 | 担当と具体的な判断 | 次へ渡すもの | 関連Control |
|---|---|---|---|
| 受付 | サポートは報告を制限された保管先へ移し、PSIRTへ引き渡す。受領連絡は真偽の確定とは分ける | 到着時刻、返信先、製品候補、報告原本の所在、引受担当。不足情報も残す | [GOV-006](../controls/records/governance-operations/psb-gov-006-vulnerability-report-intake/README.md) |
| 調査 | 開発担当は許可された検証環境で、架空の二組織を使って対象操作を確認する。添付コードを普段の端末で実行しない | 確認した版・構成・操作、再現条件、未確認版、影響するデータ | [GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)、[DESIGN-001](../controls/records/secure-design/psb-design-001-object-access-authorization/README.md) |
| 優先度と初動 | PSIRTと製品担当が公開状況、アクセス可能なデータ、悪用情報を評価。SOC・運用へ履歴の調査を依頼し、必要なら対象機能の制限を選ぶ | 優先度の理由、担当、期限、暫定措置、通常業務への影響。不正利用の有無が不明なら不明のまま残す | [GOV-003](../controls/records/governance-operations/psb-gov-003-vulnerability-priority-decision/README.md)、[GOV-011](../controls/records/governance-operations/psb-gov-011-security-event-evidence/README.md)、[GOV-012](../controls/records/governance-operations/psb-gov-012-detection-and-response-readiness/README.md) |
| 修正と検証 | 開発担当が認可を修正。確認担当が別組織からの操作拒否と、本来許される操作の継続を確認する | 修正対象、検証した版・構成、結果、未確認の派生版、配布成果物との対応 | [GOV-008](../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md) |
| 提供と配備 | Release担当は検証済みの変更を含む成果物を提供。運用担当はSaaSの対象環境を置換する | 提供先、成果物digest、稼働先別の新旧版、失敗・未観測の環境 | [REL-001](../controls/records/release-integrity/psb-rel-001-signature-provenance-verification/README.md)、[GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md) |
| 告知と通知 | PSIRT・顧客対応は影響版、回避策、更新方法、未確認範囲を確認して案内。修正版未提供でも必要な暫定連絡を判断する | 確認済みの原稿、公開先、対象者、配信結果、未到達先と再送担当 | [GOV-007](../controls/records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/README.md) |
| 終了判断 | PSIRTは下の完了条件を工程ごとに確認。残る顧客側更新や調査を担当者へ引き継ぐ | 完了した範囲、継続する作業、次回確認時点、再開する条件 | [GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)、[GOV-007](../controls/records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/README.md)、[GOV-008](../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md) |

この例は自社コードの認可不備なので、依存部品の検索を必須工程にしません。原因が依存部品にあると分かった場合は、GOV-001とREL-003の影響調査へつなぎます。認証情報の持ち出しが疑われる場合は、修正の配備とは別にGOV-004の失効と調査を開始します。

### 一つの案件で共有する記録

ticketの説明欄や既存の案件管理項目に、次を記録します。証拠本文・個人情報・秘密情報を広い閲覧範囲のticketへ複製せず、アクセスを制限した保管先への参照を使います。受信したURLや添付も未信頼として扱います。（[GOV-006](../controls/records/governance-operations/psb-gov-006-vulnerability-report-intake/README.md)、[GOV-011](../controls/records/governance-operations/psb-gov-011-security-event-evidence/README.md)）

| 記録 | この例で記入する内容 |
|---|---|
| 案件と担当 | 社内の案件番号、調整責任者、各作業の引受担当、次回確認時点 |
| 確認できた影響 | SaaSの対象構成では再現。配布版の一部は確認中。未調査版を非該当にしない |
| 根拠と不足 | 検証結果の所在、確認時刻、調べた環境、足りないログや版。ログがないことは悪用なしの証拠にしない |
| 対応判断 | 制限する機能と理由、実行者、業務影響、解除条件。期限は組織の方針と状況から決める |
| 修正と稼働 | 修正の検証結果、提供する版・digest、SaaS環境別の置換結果、顧客側の更新状況は別欄 |
| 連絡と残作業 | 原稿の確認者、公開・配信結果、未到達先、残る調査の担当と期限 |

状態を一つの「対応済み」にまとめません。例えば「修正検証済み／修正版提供済み／SaaS一環境は置換失敗／一部顧客へ未到達」と書けば、次の担当が何をすべきか分かります。

### 完了の判断例

修正版を公開しても、SaaSの一環境だけ古い版が残っていれば、その環境の復旧は未完了です。顧客へメールを送っても配信失敗があれば、対象者への通知は未完了です。顧客が受信しても更新したとは限りません。

- **修正の確認**：報告された条件への対処を対象版・構成で確認し、未検証の版を分ける。（[GOV-008](../controls/records/governance-operations/psb-gov-008-vulnerability-remedy-validation/README.md)）
- **SaaSの復旧**：対象環境の置換、旧版の非稼働、正常な処理を確認する。侵害の疑いがあれば残存アクセスや被害の調査も別に続ける。（[GOV-005](../controls/records/governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)）
- **利用者への対応**：必要な情報の公開と対象者への配信を確認する。顧客管理環境の更新は、確認できた場合だけ更新済みとする。（[GOV-007](../controls/records/governance-operations/psb-gov-007-vulnerability-advisory-and-notification/README.md)）
- **案件の整理**：未確認・未到達・顧客側作業を消さず、継続管理の担当と次回確認を決める。残作業を別案件へ移したことは、製品全体の復旧完了を意味しない。

後から別の影響版が判明したら、調査と通知を再開します。期限付き例外を認める場合も、影響と未修正の事実は残し、GOV-002で対象・理由・期限・取消条件を管理します。

### 自組織へ入れて確かめる

1. 既存の受付、非公開ticket、証拠保管先、配信手段を選び、上の担当と不在時の代替担当を実名で決める。実名や連絡先は組織内で管理し、この公開PJには保存しない。
2. この例を架空の報告として机上演習する。受領連絡だけで止まらず、次の担当が引き受け、修正・配備・通知を別々に判断できるかを確かめる。
3. 「報告の情報不足」「配布版だけ未調査」「一環境で配備失敗」「通知失敗」「後から影響版追加」を途中で提示し、誰が何を確認し直すかを見る。
4. 詰まった引き渡しや連絡経路を修正する。実窓口や配信を試す場合は、承認された検証先と架空データだけを使う。手順を採用したことと実経路の確認結果を分けて記録する。

専用コードや脆弱性診断アプリは追加しません。この運用例の成立は、実際の担当・権限・連絡経路によって確かめます。ここで机上演習や本番対応を実施済みとは扱いません。

この具体例は[Overviewの七つの業務観点](../sources/README.md#ref-portfolio-001)を、担当間の受け渡しへ具体化した本PJの解釈です。PSIRTが調整し、アプリ担当が修正し、基盤担当が提供し、運用担当が稼働を確認し、顧客対応が知らせます。例外判断と振り返り・演習も接続します。七つの新Controlや組織部門を作る要求ではありません。個別要件の根拠は各Controlの参照資料へ進んでください。

## 検索0件を判定する前に（GOV-001 / REL-003・004）

「一致なし」は検索APIの返答です。製品についての「該当なし」に進める前に、次の範囲を同じ調査時点で確認します。

| 確認する範囲 | 欠けている場合 |
|---|---|
| 対象製品・版とSBOMの取得地点、収集対象、除外条件 | ソースSBOMにない部品を、完成物にもないとは言えない |
| 成果物digestとSBOMの対応、分析基盤での取込と必要な分析の完了 | 別成果物や処理途中の結果を使う恐れがある |
| 対象projectへの閲覧権限、全ページ、検索条件と結果時刻 | 見えていない製品・結果が残る |
| 稼働環境の観測範囲、時刻、成果物digestとの対応 | リリース済みと稼働中、未観測と非稼働を区別できない |

各条件が満たされても「該当なし」は示した製品・環境・時点・収集範囲に限ります。一部だけ確認できた場合は、その部分の非該当と残る調査不能を併記します。SBOMの生成と分析状態の確認方法は[REL-003の設計](sbom-to-vulnerability-response.md)、供給者SBOMの訂正・撤回は[REL-004](../controls/records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md)を参照します。

GOV-003へは、影響候補、範囲付き非該当、調査不能のどれかに加え、対象・観測時刻・根拠・不足情報・再確認担当を渡します。GOV-003が露出、深刻度、悪用情報、組織方針を合わせて優先度を決めます。調査不能は担当者を置いて再調査または暫定対応を選ぶ材料であり、自動的な低優先度や最高優先度ではありません。

## 影響調査の方式を選ぶ（GOV-001・009・011）

| 方式 | 向く状況 | 代償・確認事項 |
|---|---|---|
| 手元に保全した台帳を検索 | 管理範囲が限られ、調査時点の台帳を保全できる | 更新漏れ、対象漏れ、異なるパッケージ体系の名前・版の違いを管理する |
| 分析基盤で検索し、元の証拠と照合 | 製品をまたいで部品や脆弱性情報を検索したい | 閲覧権限、全ページの取得、分析完了、情報の鮮度、API仕様を確認する。分析基盤だけを正本にしない |
| 稼働状況の収集結果と照合 | 実際に動いているサービス・環境を特定したい | Cluster・namespace・短命な処理の観測範囲、時点、収集停止を明示する |

Dependency-Trackは二番目の方式の候補であり必須製品ではありません。旧4.14.3向けの模擬データや想定した応答形式を、現行APIの保証として使いません。
検索の読取り権限をSBOM登録や対応操作の権限から分け、秘密情報や取得した本文を共有レポートへ持ち込みません。

## 処置の条件と権限を決める（GOV-004・005・012）

証拠保全、配布停止、認証情報の失効、成果物・cacheの隔離、承認した入力での再ビルド、関係者への連絡について、
対象、担当者、承認、実行条件、通常業務への影響、確認方法を決めます。危険な操作を検索結果から自動実行しません。
緊急封じ込めと保全を並行する条件も事前に決めます。復旧後の監視と再侵入確認は別の手順です。

## 工程の間で確認すること（GOV-001・005・009・011・012）

閲覧権限で製品が欠ける、次ページを取得しない、別のSBOMを使う、tagで同一性を判断する、収集停止を0件とする、承認条件なしで削除する、といった失敗を確認します。
組織での演習では既知の対象を含む非本番調査を行い、独立した資産一覧と照合し、権限不足・収集停止が未解決として担当者へ届くことを確認します。
模擬データでの成功だけで、本番の調査範囲や対応能力を判定しません。実対応の演習は別の承認・範囲で行います。

<a id="intrusion-containment"></a>

## 公開サービスへの侵入から、横展開の封じ込めへ（GOV-004・005・011・012）

ここからは依存部品の検索とは異なり、侵入後の操作を観測した場合の対応設計です。[GOV-012](../controls/records/governance-operations/psb-gov-012-detection-and-response-readiness/README.md)から対象・根拠・未確認範囲を受け取り、SOC、アプリ、基盤、認証基盤の担当者で処置を決めます。既存のSBOM検索で全被害を把握できるとは扱いません。

| 判断 | 処置の選択と代償 | 効果の確認 |
|---|---|---|
| 侵入先が内部へアクセスしている | 対象の通信制限・隔離・停止を選ぶ。停止は通常業務や揮発する証拠に影響する。証拠保全と緊急封じ込めを並行し、全調査を待たない | 設定の受理だけでなく、問題の経路が止まったか、迂回先・既存接続が残らないかを見る |
| 認証情報が悪用された疑いがある | GOV-004へ権限・利用先・時刻を渡す。ネットワーク隔離だけでは別環境から使える権限を止められない | 古い権限と派生セッションの利用拒否、新しい権限で必要な処理が動くかを確認する |
| VMや管理APIへ広がった | 移動先のログ、追加された鍵・アカウント・ロール・定期処理等を調査する。VMなら信頼できる状態からの再構築も選ぶ。管理APIでは実行元の隔離と権限の失効を別々に判断する | 元の侵入先だけでなく移動先と残存アクセス経路の処置結果を確認する |
| 公開物や配備先が変えられた | 公開・配備を制限し、GOV-005へ影響する成果物を渡す | 正しい置換先の稼働、旧版の非稼働、再配布・切り戻し経路を確認する |

処置ごとに対象、判断者、実行者、許可範囲、通常業務への影響、確認方法、解除条件を決めます。既に承認された緊急対応の条件内なら、毎回新たな承認を待つ運用にはしません。逆に対象を特定できない通知だけで、広範囲を自動停止しません。操作権限や連絡先が使えない場合の引き継ぎも決めます。

再開前には、入口の修正、移動先の調査、追加された権限・不正な処理の除去、必要なサービスの正常動作を確認します。データの持ち出し・改変が疑われれば、データ所有者と組織のインシデント対応へ渡します。復旧は漏えいの取消しではありません。未観測の対象は担当者と次の行動を残し、全体を復旧済みにしません。[成果物の復旧設計](deployed-artifact-recovery.md#incident-recovery-boundary)が扱う範囲も区別します。

机上演習では、隔離権限なし、移動先ログの欠落、token失効失敗、一部環境だけ復旧、隔離による監視断を取り上げ、誰が判断を引き継ぐか確認します。実操作を試す場合は許可された非本番対象に限定し、処置の効果と解除を別に確かめます。

根拠は[NISTの封じ込め・除去・復旧のガイダンス](../sources/README.md#ref-security-operations-lifecycle-001)です。上の具体的な分担は本PJの設計判断で、実操作は未確認です。この追記は既存GOV-001を全インシデント対応のControlへ拡張するものではありません。VM・管理APIを含む独立した封じ込めControlは今回追加せず、設計ガイダンスと診断観点で扱います。

## 再開の条件を一つの「完了」へまとめない（GOV-002・005・007・008）

修正の検証、古い成果物の非稼働、残存アクセスの除去、利用者への到達は別の結果です。たとえば修正版を配置しても、移動先の調査が終わっていないなら、成果物の置換状況と未解決の侵入経路を分けて残します。修正がまだでも、利用者に必要な回避策を知らせる判断はできます。

期限付きの例外は[GOV-002](../controls/records/governance-operations/psb-gov-002-security-exception-lifecycle/README.md)で対象と期限を絞ります。例外の承認で元の検査結果や対応期限を消さず、期限切れのときにどの担当が元の拒否・是正へ戻すかを決めます。

[記録の収集・保護・検索](security-event-collection-and-investigation.md)、[検知の検証・配備・改善](detection-engineering-lifecycle.md)、[再ビルドから稼働成果物の置換まで](deployed-artifact-recovery.md)はそれぞれの設計へ進みます。各Controlの条件を重ねて実行しただけで全被害を把握できるとはせず、未確認の対象と次の行動を残します。

## 関連資料と未移植範囲

[Control](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)、
[教材](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/learning.md)、[仕様・採否](../sources/README.md#ref-supply-chain-impact-001)を参照してください。
旧JSON検査・対応手順の生成器は移植しません。文書と診断項目でこの主題の範囲は完了です。分析基盤への実接続、稼働状況の収集、実対応は未検証であり、採用先で導入・確認に役立つ場合だけ具体化します。
