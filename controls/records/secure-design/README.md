# Secure Design

アプリケーションの信頼境界、悪用経路、対象・操作ごとの許可判断を扱います。

| Control | 判断すること |
|---|---|
| [PSB-DESIGN-001 Object access authorization](psb-design-001-object-access-authorization/README.md) | 認証済み利用者による対象・操作・tenant越境を防ぐ |

実装上の入力処理やDB queryはSecure Codingにも関係しますが、誰がどの対象へ何をしてよいかという
許可判断を主題とするため、主なdomainはSecure Designです。
