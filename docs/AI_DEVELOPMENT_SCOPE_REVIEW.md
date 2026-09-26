# 旧AI-005〜009の移行判断

旧`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`の[AI-005〜009](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security)を、開発者端末・IDE・CLI・repository・CIで使うcoding agentの範囲で読み直した記録です。[Security scope](SECURITY_SCOPE.md)に従い、製品のAI機能、RAG、製品内memory・multi-agent構成、AI製品のTEVVは[ai-security-foundry](https://github.com/DharmaDoll/ai-security-foundry)へ委ねます。委ねることは、別PJでの実装済み状態を意味しません。

読者は開発agentを採用・設計・診断する担当者です。守るのは開発作業の継続、ソースと認証情報、外部サービス、変更・公開・deploy権限です。旧パッケージは合成JSONを検査し、live agent・tool・providerでの強制を確認していません。以下の対応は移行判断であり、実環境の検証結果ではありません。

| 旧control | 開発環境での判断 | 製品AIとの境界 |
|---|---|---|
| [AI-005 Memory / context lifecycle](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-memory-context-lifecycle/README.md) | `deferred`。開発agentが作業をまたいで再利用するcontextを保存・再読込する構成なら、出所を失った指示や秘密情報が次の作業へ入る独立した失敗経路がある。採用する保存・検索経路を選んでから再評価する | 顧客memory、tenant隔離、providerのbackup・vector index・削除保証は対象外 |
| [AI-006 Action integrity / output validation](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-action-integrity-output-validation/README.md) | `split`。開発agentの操作提案、対象・引数、承認、実行、結果不明は既存[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)と[操作認可pattern](../engineering/ai-development-security/development-action-authorization/README.md)へ接続する。別controlは作らない。採用するtool adapterが決まれば、結果が要求に対応するかを製品別実装で確認する | 製品内agentのaction処理・application authorizationは対象外 |
| [AI-007 Resource budget monitoring](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/agent-resource-budget-monitoring/README.md) | `deferred`、次の独立候補。開発agentの一作業がmodel・tool呼出しやretryを重ね、費用、外部負荷、権限保持時間を増やす問題は、単一操作の認可やCI runnerの資源上限と異なる。作業単位の上限と実行前の停止を主題として再編集する | AI製品の推論予算、サービス運用、顧客向け利用制限は対象外 |
| [AI-008 Multi-agent trust / delegation](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/multi-agent-trust-delegation/README.md) | `deferred`。開発agentが別のagentへ作業を渡す構成を採用した時に、親の対象・権限・予算を越える経路を確認する。単なる子processやtool呼出しは[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)の実行境界から始める | 製品のorchestrator、tenant間委譲、汎用multi-agent protocolは対象外 |
| [AI-009 Rogue agent containment / recovery](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/rogue-agent-containment-recovery/README.md) | `deferred`。長時間・自律実行する開発agentを採用した時に、process停止と残存権限の失効、送信済み操作の照合、再開条件を横断して設計する。現行の[AI-002失効の受け渡し](../engineering/ai-development-security/agent-extension-admission/README.md#失効を実行環境へ渡す)とAI-004を、全体の停止・復旧完了と読み替えない | AI製品のincident control plane・fallback・復旧設計は対象外 |

## 旧項目の行き先

表の対応は旧IDを新しい要件IDへ一対一で継承するものではありません。採用先が未定の項目は、適用要否も未確定です。

| 旧項目 | 残す問い・扱い |
|---|---|
| AIM-001〜004 | 再利用する開発contextの出所、保存前の確認、秘密情報、量を問う。未信頼資料の扱いは[AI-003](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)、認証情報の管理は[SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md)と接続する。固定byte上限は継承しない |
| AIM-005〜007 | 作業をまたぐcontextの読込範囲・期限・削除を、実際の保存機能がある場合に評価する。旧user／session／taskの完全一致や5分以内の削除を共通要件にしない |
| AIM-008〜009 | 内容を抑えた証拠とlive未検証の区別を残す。旧tombstone fixtureを削除保証にしない |
| AAI-001〜006 | 構造化した操作、対象と引数、独立した許可、承認と実行の結び付き、再実行防止をAI-004の[DEV-RUNTIME-5〜8](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)と操作認可patternへ渡す。特定のdigest形式や300秒の承認を一律に要求しない |
| AAI-007〜008 | Tool結果の対象・要求への対応と結果不明時の照合。後者はAI-004のDEV-RUNTIME-7に含む。前者は実際のtool adapterと結果schemaを選んだ場合に限定実装で確認する |
| AAI-009〜010 | 記録の最小化と合成fixture／liveの区別をAI-004のDEV-RUNTIME-9と実装時の検証条件に残す |
| ARB-001〜004 | 作業ID、計測元、利用量・費用・経過時間、上限と判定不能をAI-007候補へ残す。旧token数、金額、900秒を移さない |
| ARB-005〜009 | Tool呼出し、retry、子作業の累積上限と、新しい操作を実行する前の停止をAI-007候補へ残す。警告80%、alert 120秒、特定の異常回数は採用先の基準ではない。重要操作の個別許可と結果不明はAI-004へ渡す |
| ARB-010〜011 | 秘密を含まない観測と、fixtureがlive enforcementを示さないことを残す |
| MAD-001〜005 | 実際に開発agent間委譲を使う場合に、依頼元・委譲先・親作業・対象・権限の上限を確認する。Ed25519やtenant分類を共通要件にしない |
| MAD-006〜010 | 子作業の予算・期限・再送・隔離・応答の結び付きを、AI-007候補とAI-004へ接続して採用先で評価する。1 hop、5分、署名付きresponseは旧fixtureの方式 |
| MAD-011 | 証拠不足とlive未検証を区別する |
| RRC-001〜006 | 開発agent自身から独立した停止経路、対象の特定、停止結果、残存する認証情報・承認・外部操作の照合を、長時間実行agentの採用時に設計する。[GOV-004](../controls/records/governance-operations/psb-gov-004-credential-exposure-containment/README.md)は認証情報漏えい時の封じ込めであり、agent停止全体の代替ではない |
| RRC-007〜010 | Agentに依存しない手作業への切替と、新しい権限での段階再開を採用先の運用に合わせて評価する。旧二者署名、60秒停止、15分fallback、5分canaryを移さない |
| RRC-011 | 証拠保全とlive未検証を区別する |

## 次に具体化する条件

AI-007候補では、開発agentが一つの依頼を繰り返すシナリオから始めます。主な問いは「個別のtool呼出しが許可されていても、作業全体の上限を越える前に新たなmodel・tool呼出しを止められるか」です。作業IDと累積量の責任者、上限を決める人、停止を強制する位置、既に送った操作の扱いを明示し、[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)の単一操作認可、[CI runner lifecycle](../controls/records/cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md)、[workload resource bounds](../controls/records/container-cloud-iac-security/psb-container-007-workload-resource-consumption-bounds/README.md)との違いを示します。Control・教材・設計pattern・診断観点を必要な成果物として検討します。製品別の設定・コードは、採用するagentと版、利用量の取得元、実行前に拒否できるhookまたはgateway、使い捨て環境が決まった時に選びます。

AI-005は持続的なcontext保存、AI-008はagent間委譲、AI-009は長時間・自律実行と停止経路が、実際の開発環境で確認できた時に再開します。各主題について固有の失敗経路と強制点が説明できなければ、別controlは作らず既存controlと実装判断へつなぎます。
