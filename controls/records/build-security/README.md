# Build Security

ビルド対象のコードを実行する権限と、ビルド基盤・公開・deployを管理する権限を分けます。

| Control | 読者が判断すること | 学ぶ |
|---|---|---|
| [PSB-BUILD-001 Build containment](psb-build-001-build-containment/README.md) | 実行中の権限・通信・隔離をどこで強制し、観測の健全性をどう確認するか | [依存を承認しても、実行権限は別に制限する](psb-build-001-build-containment/learning.md) |
| [PSB-BUILD-002 Approved and consistent release build](psb-build-002-approved-consistent-build/README.md) | 承認したbuilderと手順で今回の成果物を作り、別経路からの昇格を止められるか | [同じbuilderでも、別の手順で作れば別のrelease](psb-build-002-approved-consistent-build/learning.md) |
| [PSB-BUILD-003 Platform provenance generation](psb-build-003-platform-provenance-generation/README.md) | 来歴情報を誰が作り、記録の出所と成果物との対応をどう確かめるか | [署名が正しくても、記録の中身は誰が決めたのか](psb-build-003-platform-provenance-generation/learning.md) |

三つの主題は、文書と診断項目を今回の成果物としています。実行基盤の選定、権限制限、公開を止める仕組み、来歴の生成・認証が採用先で機能するかは別途確認します。
領域全体の移行完了・組織への導入を意味しません。
