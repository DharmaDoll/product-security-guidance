# Secure Design

アプリケーションで何を許可・拒否するか、どこでその判断を強制するかを扱います。
[ModelForge](https://github.com/DharmaDoll/ModelForge)が進めるシステムの構造化、DFD、STRIDEなどの脅威候補の生成とは役割を分けます。
このdomainでは個別システムの脅威モデルを作らず、見つかった問題に繰り返し使える設計上の判断を残します。

| Control | 判断すること |
|---|---|
| [PSB-DESIGN-001 Object access authorization](psb-design-001-object-access-authorization/README.md) | 認証済み利用者による対象・操作・tenant越境を防ぐ |

実装上の入力処理やDB queryはSecure Codingにも関係しますが、誰がどの対象へ何をしてよいかという
許可判断を主題とするため、主なdomainはSecure Designです。

## 一つの認可シナリオから読む

利用者Aが請求書APIへ送るIDを、利用者Bの請求書IDへ変えた場合を考えます。ログイン済みでも、AにBの請求書を読む権限はありません。

1. 個別システムの構成やデータの流れから脅威候補を洗い出すなら[ModelForge](https://github.com/DharmaDoll/ModelForge)を使えます。出力はレビュー候補です。この請求書の権限関係を実際に扱うかは、人がシステム情報で確認します。
2. 何を拒否し、どこで許可を判断するかは[DESIGN-001](psb-design-001-object-access-authorization/README.md)と[教材](psb-design-001-object-access-authorization/learning.md)から読みます。対象IDを指定できることと、その対象を読んでよいことを分けます。
3. Webアプリ共通の検証要件は[ASVS 5.0.0のV8認可](../../../sources/README.md#spec-owasp-asvs-5-0-0)へ進みます。この例と部分的に対応するのは、操作ごとの権限を問うV8.2.1と、対象データごとの権限を問うV8.2.2です。対象製品に必要な他の要件は[Secure Codingの入口](../secure-coding/README.md)から選びます。
4. サーバー側の条件をどう置くかは[Object access boundary](../../../engineering/secure-design/object-access-boundary/README.md)で検討します。対象アプリケーションの設計レビューや脆弱性診断では、[診断で確認する項目](psb-design-001-object-access-authorization/README.md#failure-checks)を使えます。

ModelForgeの脅威候補、ASVSの要件、DESIGN-001の設計判断は、対象アプリケーションを確認するための材料です。実際に権限を越えた操作を拒否できるかは、導入先で確認します。
