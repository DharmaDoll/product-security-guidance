# PSB-AI-004 Development agent runtime boundary

## このcontrolを一枚で理解する

| 項目 | 内容 |
|---|---|
| セキュリティ上の問題 | 未信頼の指示や拡張が開発者の権限を引き継ぎ、意図しないソース公開、秘密情報の取得、外部変更を実行する。 |
| 誰から、または何から守るか | 悪意あるリポジトリ・tool、承認の偽造や再利用、隔離・認可・監査の障害から守る。 |
| 何が対象か | 開発端末・IDE・CLI・開発用MCP・CIで動くagentの実効権限、拡張、操作許可、通信、監査。 |
| 何をするか | 方針をagentの外側で管理し、到達範囲を制限する。実際の拡張と操作を現在の承認へ照合し、判断・結果・観測障害を分ける。 |
| 成功状態 | 実行できる対象・操作・条件を説明でき、未承認・失効・照合不能な要求を許可しない。必要な監査と通知の欠落も把握できる。 |
| 対象外・残余リスク | 製品自体のAI機能、端末全体の防御、生成コードの正しさ、全prompt injectionの阻止は保証しない。実環境の強制は未検証。 |

## 問いと適用範囲

開発agentが何を提案したかではなく、実際にどの権限で何を実行できるかを管理できるか。
対象はAIを使う開発環境です。[製品自体のAI security](../../../../docs/SECURITY_SCOPE.md)は別PJへ委ねます。

拡張の採用審査は[AI-002](../psb-ai-002-agent-extension-dependency-governance/README.md)、認証情報の発行・失効は[Source credential lifecycle](../../source-protection/psb-source-004-source-access-credential-lifecycle/README.md)の責任です。本controlはそれらを実際の読み込み・操作へ結び付けます。

## 必要なセキュリティ特性

| ID | 満たすべき状態 |
|---|---|
| DEV-RUNTIME-1 | 管理方針をagentの外側に置き、必要な隔離が使えない場合と迂回時は実行を許可しない。 |
| DEV-RUNTIME-2 | 作業対象・保護設定・認証情報を分け、ファイルと認証情報の受け渡し経路を制限する。 |
| DEV-RUNTIME-3 | 通信を必要な経路へ限定し、名前・解決先・実接続先と送信する情報を別に確認する。 |
| DEV-RUNTIME-4 | 実行時の拡張・tool・権限を現在の承認記録へ照合し、欠落・未承認・評価不能は利用可能としない。 |
| DEV-RUNTIME-5 | 操作と引数の効果を独立に分類し、自動変更の対象・量を限定する。未知の間接呼出しは許可しない。 |
| DEV-RUNTIME-6 | 重要操作は、依頼者・実行主体・対象・引数・方針・期限に結び付いた真正な承認を実行前に確認する。 |
| DEV-RUNTIME-7 | 承認の使用を不可分に管理し、外部操作の結果不明を未実行に変換して再送しない。 |
| DEV-RUNTIME-8 | 操作の実行側で要求に一致する許可を確認し、hookの適用漏れ・停止・不正出力を許可へ変換しない。 |
| DEV-RUNTIME-9 | 判断と結果を内容最小限の監査へ結び、対象端末の網羅・収集health・配送・担当者への通知を確認する。 |
| DEV-RUNTIME-10 | 収集結果の出所・内容・方針・鮮度・順序を認証し、古い正常結果の再送を受理しない。 |

これらは保証目標です。設定例の存在や合成データの一致を、導入済みの証拠としません。

## 実装判断の羅針盤

未信頼のテストscriptが公開用tokenを使えるなら、作業フォルダだけの書込制限ではソース公開を止められません。Agentに公開権限を渡さず、独立した実行側が対象と承認を照合する場合、その直接経路は成立しません。
隔離は到達範囲、認可は特定の操作の許可を扱います。一方があるだけで他方を省きません。

最初に自動化する対象と権限を狭め、例外や再試行を含む実行経路を確認します。製品名や確認回数、固定の有効期限を安全性の根拠にしません。
実行前の評価不能は許可しません。実行後の通信障害は結果不明として調べ、承認を戻して自動再送しません。

## 学習・設計・確認

拡張の失効後は、一回の操作承認だけを根拠に実行しません。新規呼出しの拒否、既存処理の停止、認証情報の失効、送信済み操作の結果確認を[別の責任として確認](../../../../engineering/ai-development-security/agent-extension-admission/README.md#失効を実行環境へ渡す)します。AI-004が直接扱うのは現在の資格との照合と利用拒否であり、全端末の復旧完了ではありません。

- [Development runtime isolation](../../../../engineering/ai-development-security/development-runtime-isolation/README.md)：到達範囲、通信先、監査・配送。
- [Development action authorization](../../../../engineering/ai-development-security/development-action-authorization/README.md)：操作分類、承認、並行利用と結果不明。
- [Agent extension admission](../../../../engineering/ai-development-security/agent-extension-admission/README.md)：審査記録と実行時の照合。
- [教材](learning.md)、[参照資料と採否](../../../../sources/README.md#ref-development-runtime-reconciliation-001)、[旧26項目の対応表](../../../../docs/AI_RUNTIME_MIGRATION.md)。

導入時の無害な確認方法は各設計資料に置きます。製品adapter、実通信、拒否・並行消費・配送試験は今回移植していません。
[Framework mapping](../../../../mappings/frameworks.yaml)は旧15関係の版・ID・関係・confidenceを保持した再割当です。旧`verifies`も今回検証したという意味ではありません。特にAISVSの暗号学的結合は方式依存として保留しています。
