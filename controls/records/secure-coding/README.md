# Secure Coding

WebアプリケーションとWebサービスの共通の検証要件は、[OWASP ASVS 5.0.0](../../../sources/README.md#spec-owasp-asvs-5-0-0)から探します。このPJはASVSの各要件を独自controlへ複製しません。個別の失敗経路や実装判断を深める必要がある主題だけを教材や設計パターンにします。実装例は導入・確認に役立つ場合だけ作ります。[領域の方針](../../../docs/REPOSITORY_DESIGN.md#secure-codingとasvs)を参照してください。

## ASVSから探す

| 確認したいこと | 固定版の入口 |
|---|---|
| SQLなどへの注入や、出力先に合わせた符号化 | [V1 Encoding and Sanitization](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x10-V1-Encoding-and-Sanitization.md) |
| 入力値が業務上妥当か、処理順や回数を悪用できないか | [V2 Validation and Business Logic](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x11-V2-Validation-and-Business-Logic.md) |
| ブラウザ側の処理、APIやWebサービスの入口 | [V3 Web Frontend](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x12-V3-Web-Frontend-Security.md)、[V4 API and Web Service](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x13-V4-API-and-Web-Service.md) |
| ログイン、セッション、利用者が操作できる対象 | [V6 Authentication](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x15-V6-Authentication.md)、[V7 Session Management](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x16-V7-Session-Management.md)、[V8 Authorization](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x17-V8-Authorization.md) |
| アプリケーションのトークン、OAuth・OIDC | [V9 Self-contained Tokens](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x18-V9-Self-contained-Tokens.md)、[V10 OAuth and OIDC](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x19-V10-OAuth-and-OIDC.md) |
| 暗号、アプリケーションが使う秘密情報 | [V11 Cryptography](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x20-V11-Cryptography.md)、[V13.3 Secret Management](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x22-V13-Configuration.md) |
| 安全な設計、言語固有の問題、並行処理 | [V15 Secure Coding and Architecture](https://github.com/OWASP/ASVS/blob/v5.0.0_release/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md) |

これは探すための入口です。対象製品に適用する要件は、リンク先の本文と要件IDを確認して選びます。アプリケーションが使う秘密情報と、開発者が端末で使う認証情報は別の問題です。後者は[開発端末上の認証情報](../source-protection/psb-source-007-developer-local-credential-storage/README.md)で扱います。

現在の独立controlは[PSB-CODE-005 Unicode source review](psb-code-005-unicode-source-review/README.md)です。レビュー画面に見えるコードと処理系が読むコードの食い違いを扱い、主な根拠は[Unicodeの仕様](../../../sources/README.md#spec-unicode-source-handling-2)です。ASVS V15の要件を満たした証拠として扱いません。

利用者が後日提供する経験由来の脆弱性診断チェックリストは、[受領後の扱い](../../../docs/MIGRATION_PLAN.md#secure-codingの進め方)を定めています。原本を受け取ってからASVSと重なる点や補う点を確認します。項目はまだ受け取っていません。

認可を具体例から読むなら、[請求書IDを変えるシナリオ](../secure-design/README.md#一つの認可シナリオから読む)へ進んでください。そこから[DESIGN-001](../secure-design/psb-design-001-object-access-authorization/README.md)の拒否条件と診断項目、ASVS V8.2.1・V8.2.2、設計パターンをたどれます。この例が扱うread・updateとowner・tenant条件を、Webアプリ全体の認可要件へ広げて扱いません。
