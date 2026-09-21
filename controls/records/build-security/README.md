# Build Security

ビルド対象のコードを実行する権限と、ビルド基盤・公開・deployを管理する権限を分けます。

| Control | 読者が判断すること |
|---|---|
| [PSB-BUILD-001 Build containment](psb-build-001-build-containment/README.md) | 実行中の権限・通信・隔離をどこで強制し、観測の健全性をどう確認するか |

承認builder、一貫した実行、platform側の来歴生成は未移行です。
領域全体の移行完了・組織への導入を意味しません。
