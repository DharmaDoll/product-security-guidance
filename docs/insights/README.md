# 領域横断のセキュリティ洞察

洞察は、複数のコントロール、パターン、設計レビュー、教育で再利用できる、このリポジトリ独自の考え方です。
規範要件、製品設定、適合性を裏付ける証拠の代替ではありません。
各洞察を攻撃連鎖のどこで使うかは[横断分析の軸](../ANALYSIS_LENSES.md)で確認します。

## パイロットで得た洞察

| 洞察 | 持ち帰る見方 |
|---|---|
| [Security effects live at enforcement points](security-effects-live-at-enforcement-points.md) | 成果物の存在ではなく、実際の操作を変える境界を見る |
| [Credential is delegated authority, not a string](credential-is-delegated-authority.md) | 安全な保管だけでなく、対象リソース、操作、有効期間、利用プロセスを追う |
| [Cooldown buys observation time, not trust](cooldown-buys-time-not-trust.md) | 時間の経過をパッケージの安全性と取り違えない |

## 洞察の条件

- 一つのコントロールを言い換えただけではない。
- 中心となる見方、具体例、設計レビューへの応用、誤用、限界を持つ。
- 関連するコントロール、学習資料、パターン、参照資料へリンクする。
- 参照資料に書かれた事実と、リポジトリでの解釈を区別する。
