# Development agent work budgetの移行判断

旧[PSB-AI-007](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-resource-budget-monitoring/control.yaml)を、開発agentの一依頼に属する累積量と次の実行前の停止へ絞りました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-26です。[旧AI-005〜009の選別](AI_DEVELOPMENT_SCOPE_REVIEW.md)からの具体化で、製品の推論サービスや顧客向け予算設計は本PJへ移しません。

| 旧項目 | 移行先・採否 |
|---|---|
| ARB-001 | [DEV-BUDGET-1〜2](../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md)：責任を持つ作業、計測元、必要情報を確認する。旧AI-004の固定digest、二種類のprovider、七scenarioを一律に要求しない |
| ARB-002〜003 | DEV-BUDGET-2〜3：利用量と実行中の予約、次の消費可能量、通貨・単位・価格の不明を分ける。旧20,000／8,000／28,000 token、500,000 USD micro-unitを共通上限にしない |
| ARB-004 | DEV-BUDGET-3〜4：外側の実行期限と実際の停止。旧900秒は移さない。具体例の時間は例として選び、実環境の適正値としない |
| ARB-005〜007 | DEV-BUDGET-1〜3：tool、再試行、子作業の累積量と割当。旧20 tool call、重要操作一回、retry三回、深さ四を共通要件にしない |
| ARB-008 | DEV-BUDGET-5：繰り返す拒否、承認再利用、hook障害を実行方針・調査へ渡す。異常回数の固定閾値は採用先で決める。単一操作の認可はAI-004を再実装しない |
| ARB-009 | DEV-BUDGET-3〜6と[設計](../engineering/ai-development-security/development-work-budget-gate/README.md)：判断と実停止を結ぶ。警告80%とalert 120秒を外し、通知と強制を区別。終了時の要約・読取りも有限の予約に含める |
| ARB-010〜011 | DEV-BUDGET-2・6：証拠不足をゼロへ変換せず、秘密情報を増やさず、合成fixtureと実強制を区別する |

旧verifierは合成session countersから判断し、申告されたbreaker・alert receiptを照合します。Model・toolを起動せず、並列の予約、provider usage、費用請求、実停止、実通知を観測しません。旧JSON、危険なoverlay、verifierは本PJの実装例へコピーしません。

必要な成果物は[control](../controls/records/ai-development-security/psb-ai-007-development-agent-work-budget/README.md)、control配下の教材、設計pattern、診断観点と判断しました。ローカル実行時間の経路は製品を選ばず具体化できるため、GNU coreutils 9.7の[Linux timeout例](../engineering/ai-development-security/development-work-budget-gate/implementations/linux-timeout/README.md)を追加しました。実processの成功・停止・起動失敗を六件で観測しますが、予算control全体の検証や実agentの停止確認ではありません。

実装から戻す境界は、期限後の停止猶予、子processの所属、監視process自身の停止、再起動での予算初期化、外部操作の結果不明です。費用・token・呼び出しの共通予約は、agent・版、利用量と料金の取得元、実行前強制点、使い捨て対象が選ばれた時に限定実装へ進みます。これが必要な採用先では、時間だけの例で完了扱いにしません。

旧frameworkのATLAS `2026.05 / AML.T0034.002・AML.T0029・AML.M0024`、Agentic Top 10 `2026 / ASI08`、AISVS `1.0 / v1.0-C9.1.2・v1.0-C12.2.2`は履歴として保持します。製品AI全体やlive providerへの関係を含むため、旧`verifies / high`などを本PJの実証済み関係へ移しません。今回はframework mappingを追加せず116件のままです。直接の設計入力とその限界は[REF-DEVELOPMENT-WORK-BUDGET-001](../sources/README.md#ref-development-work-budget-001)へ分けます。旧資料ID`REF-AI-002`の汎用agentガイダンスは開発環境に必要な部分だけ再参照し、新しいIDの別名として残しません。
