# PSB-AI-002 Agent extension dependency governance

## このcontrolを一枚で理解する

| 項目 | 内容 |
|---|---|
| セキュリティ上の問題 | 承認後に差し替わった拡張や、有害な指示・過剰な権限を持つ拡張を読み込むと、agent経由でソース、認証情報、接続先の資産に影響が及ぶ。 |
| 誰から、または何から守るか | 悪意ある配布者、侵害されたmarketplace、見た目の似た拡張、自己承認、古い審査結果、失効情報の収集障害から守る。 |
| 何が対象か | Skill、MCP server、plugin、外部promptの出所、内容、所有者、利用条件、要求権限、評価結果、承認期限、失効状態、読み込み先との対応。 |
| 何をするか | 出所と内容を固定し、独立した内容審査と権限審査を行う。同じ内容の評価結果と有効な承認を結び、実行環境へ照合可能な識別情報を渡す。 |
| 成功状態 | 利用可能な拡張を内容・権限・期限で特定でき、変更・失効・証拠不足なら利用を許可せず、実行環境が承認記録と照合できる。 |
| 対象外・残余リスク | 審査は潜在的な悪意をすべて発見できない。Remote serverの稼働内容、操作ごとの認可、端末隔離、実際の停止・失効は別途確認する。 |

## 問いと適用範囲

「その拡張を承認した」から一歩進み、何を審査し、何を読み込み、どの権限で利用するのかを説明できるか。
開発用agentへ追加するコードと指示の両方を扱います。外部文書を検索した際の入力処理や、モデル・学習データの採用審査は別の境界です。

対象は開発者端末・IDE・CLI・repository・CIで使う拡張です。製品のchatbotなどが提供するAI機能のMCP・pluginは[ai-security-foundry](https://github.com/DharmaDoll/ai-security-foundry)へ委ねます。
モデル・学習データも本PJの移行対象外です。詳しい分担は[Security scope](../../../../docs/SECURITY_SCOPE.md)を参照してください。

## 必要なセキュリティ特性

| ID | 満たすべき状態 |
|---|---|
| EXT-1 | 正規の取得元、変更不能なsource commitとversion、実際に取得したartifactのSHA-256を対応付ける |
| EXT-2 | 所有者、承認したlicense、配布者・申請者から独立したreviewer、審査結果、期限を記録する |
| EXT-3 | 指示、コード、tool schema、インストール・更新処理を読み、方針の上書き、認証情報収集、未申告通信や副作用を審査する |
| EXT-4 | ファイルの読み書き、通信先、認証情報、利用可能なtool、直接実行権限を拡張ごとに限定し、審査した要求と一致させる |
| EXT-5 | 同じ拡張ID・commit・digestについて、定めた評価条件と結果を保持する。評価器の失敗や未完了を安全と判定しない |
| EXT-6 | 全対象を含む新しい失効情報で利用可否を確認する。既知の失効は拒否、収集不能や欠落は評価不能として利用を止める |
| EXT-7 | 承認記録と実行時の拡張ID・種類・内容・強制方式を対応付ける。照合できない種類や環境では読み込みを許可しない |

## 実装判断の羅針盤

通常の[Dependency artifact identity](../../dependency-security/psb-deps-003-dependency-artifact-identity/README.md)と同じく、名前やversionだけで内容を特定しません。
Agent拡張ではさらに、文章がagentの判断やtool利用へ与える影響を審査します。署名やhashは、その内容が妥当という判定を代替しません。

Skillが「診断のため」と称して秘密情報の送信を指示すると、agentがその指示を採用し、秘密情報を読めて、外部送信もできる場合に漏えい経路が成立します。
読取権限や送信経路を実行環境で遮断すれば、その経路は成立しません。`direct_tool_authority: false`という申告だけでは遮断した証拠になりません。

Remote MCPのsource commitを固定しても、接続先がそのコードを動かしているとは限りません。稼働版の証拠と承認内容を対応付ける方法を決め、確認できない部分を残したまま「同一性確認済み」としないでください。

## 前後の受け渡し

認証情報の選択・保管・期限は[Source credential lifecycle](../../source-protection/psb-source-004-source-access-credential-lifecycle/README.md)で扱います。
本controlは読み込んでよい拡張を決め、操作ごとの認可と実際の権限制限を実行環境へ引き渡します。
[PSB-AI-001](../psb-ai-001-repository-agent-guidance/README.md)の開発用比較評価は設計まで移行しましたが、旧合成benchmarkや実agentの評価結果は移していません。[PSB-AI-004](../psb-ai-004-development-agent-runtime-boundary/README.md)は保証目標を移行しましたが、実行時強制は未実装です。承認情報の受け渡しは、それらの有効性や導入を証明しません。

## 学習・設計・根拠

- [教材: Reviewing an agent extension](learning.md)
- [設計: Agent extension admission](../../../../engineering/ai-development-security/agent-extension-admission/README.md)
- [参照資料の版と採否](../../../../sources/README.md#ref-agent-extension-admission-001)
- [Framework mapping](../../../../mappings/frameworks.yaml)：旧関係を移行レビュー中として保持。AISVSの`verifies`も今回の実検証を意味しない。
