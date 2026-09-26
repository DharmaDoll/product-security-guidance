# Secure Coding

WebアプリケーションとWebサービスの認証、認可、入力処理など、共通の検証要件を探すときは[OWASP ASVS 5.0.0](../../../sources/README.md#spec-owasp-asvs-5-0-0)から始めてください。このPJはASVSの各要件を独自controlへ複製しません。個別の失敗経路や実装判断を掘り下げる必要がある主題だけを、教材・pattern・実装例へつなぎます。[領域の方針](../../../docs/REPOSITORY_DESIGN.md#secure-codingとasvs)を参照してください。

探す入口は、入力・出力とinjectionならASVS第1章、入力検証とbusiness logicなら第2章、認証・session・認可なら第6〜8章、暗号なら第11章、secret管理なら第13章です。実際の判断には章名だけでなく[固定版の要件本文](https://github.com/OWASP/ASVS/releases/tag/v5.0.0_release)を確認し、対象製品に適用する要件を選んでください。この案内はASVSの網羅的な対応表ではありません。

現在の独立controlは[PSB-CODE-005 Unicode source review](psb-code-005-unicode-source-review/README.md)です。Source codeの表示と解釈の食い違いを扱い、ASVS全体の代わりにはなりません。

利用者が後日提供する経験由来の脆弱性診断チェックリストも、この領域の重要な入力として[受領後の扱い](../../../docs/MIGRATION_PLAN.md#secure-codingの進め方)を定めています。まだ原本はないため、項目やASVSとの対応を作っていません。

認可の具体的な失敗経路と実装例は、隣接する[Object access boundary](../../../engineering/secure-design/object-access-boundary/README.md)からたどれます。
