# Development content injectionの移行判断

旧[`PSB-AI-003`](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/ai-development-security/prompt-document-injection-containment/control.yaml)の対象を、開発agentが読むrepository文書、Issue・PR、Web/API応答、tool出力へ絞りました。移行元の固定revisionは`f42987759218c9b8daf3924320542a1935ef78e0`です。[Security scope](SECURITY_SCOPE.md)に従い、製品のchatbot・RAGは本PJへ戻しません。

読者は開発agentの設計者と診断担当者です。旧パッケージでは「合成run-resultsの構造が正しい」と「実agentが注入を拒否する」が近くに置かれていました。今回の完了条件は、出所・依頼・実行の境界、正当な作業の継続、診断観点を説明できることです。製品別実装の完了や実環境での成功を含めません。

| 旧項目 | 移行先と判断 |
|---|---|
| AII-001〜002 | [DEV-CONTENT-1〜2](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)：入力面ごとの出所と依頼の権限を分ける。6個の固定fixtureとSHA-256一致を普遍要件にしない |
| AII-003〜007 | DEV-CONTENT-3と[設計](../engineering/ai-development-security/untrusted-development-content-boundary/README.md)：注入から保護設定変更、認証情報、通信、依存導入、特権操作への経路を扱う。実際の拒否・隔離は[AI-004](../controls/records/ai-development-security/psb-ai-004-development-agent-runtime-boundary/README.md)の責任 |
| AII-008 | DEV-CONTENT-4と[教材](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/learning.md)：拒否と元の作業の完了を分ける。固定出力digestをあらゆる作業の合格条件にしない |
| AII-009〜010 | DEV-CONTENT-5：最小限の証拠、未実施・判定不能の区別。合成fixtureの`PASS`をlive containmentへ読み替えない |

旧direct-user-prompt scenarioは、資料中の間接注入と異なり、依頼者の権限・管理方針の問題です。管理方針と実行側の拒否はAI-004へ渡し、AI-003の診断件数へ混ぜません。旧packageのWeb/API scenarioは、開発agentが実際に読む場合だけ対象です。旧AISVS C2やAgentic Top 10は製品AI全体の要件・リスク分類を含むため、開発環境の成功証拠として旧8件の`verifies` mappingを継承しません。詳細な出典と採否は[参照資料](../sources/README.md#ref-development-input-trust-001)に保持します。

旧資料ID `REF-AI-001`（Claude Code Hardening Cheatsheet）は製品固有の参考、`REF-AI-002`（OWASP AI Agent Security Cheat Sheet）は開発環境に該当する部分だけを新しい`REF-DEVELOPMENT-INPUT-TRUST-001`へ統合しました。旧IDを新しい成果物の別名として使いません。

旧`secure/`・`insecure/`、`scripts/verify.py`はJSON中の申告値と整合性を検査します。実際のmodel、tool、認証情報パス、通信、実行前の拒否は動かしません。このため本PJの`implementations/`へコピーしません。対象agent・版、入力取得元、toolの強制点、保護対象、使い捨て環境、無効なcanary、元の作業の期待結果を決めたら、その一構成へ限定した実装とsmoke testを作ります。成功、拒否、取得・判断失敗を観測し、旧fixtureとの違いを明示します。

この主題で必要と判断した成果物は[control](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)、control配下の教材、[設計pattern](../engineering/ai-development-security/untrusted-development-content-boundary/README.md)、診断観点です。具体実装は上記の採用先が選ばれるまで保留します。旧52件の件数合わせや、すべてのagentを代表する汎用test runnerは作りません。
