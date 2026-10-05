# Secure Design

アプリケーションで何を許可・拒否するか、どこでその判断を強制するかを扱います。
[ModelForge](https://github.com/DharmaDoll/ModelForge)が進めるシステムの構造化、DFD、STRIDEなどの脅威候補の生成とは役割を分けます。
このdomainでは個別システムの脅威モデルを作らず、見つかった問題に繰り返し使える設計上の判断を残します。

| Control | 判断すること |
|---|---|
| [PSB-DESIGN-001 Object access authorization](psb-design-001-object-access-authorization/README.md) | 認証済み利用者による対象・操作・tenant越境を防ぐ |

実装上の入力処理やDB queryはSecure Codingにも関係しますが、誰がどの対象へ何をしてよいかという
許可判断を主題とするため、主なdomainはSecure Designです。
