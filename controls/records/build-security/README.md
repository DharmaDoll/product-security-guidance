# Build Security

ビルド対象のコードを実行する権限と、ビルド基盤・公開・deployを管理する権限を分けます。

| Control | 読者が判断すること |
|---|---|
| [PSB-BUILD-001 Build containment](psb-build-001-build-containment/README.md) | 実行中の権限・通信・隔離をどこで強制し、観測の健全性をどう確認するか |
| [PSB-BUILD-002 Approved and consistent release build](psb-build-002-approved-consistent-build/README.md) | 承認したbuilderと手順で今回の成果物を作り、別経路からの昇格を止められるか |
| [PSB-BUILD-003 Platform provenance generation](psb-build-003-platform-provenance-generation/README.md) | Provenanceの生成権限、field source、artifact binding、認証、失敗時のhandoffをどう分けるか |

承認builderと一貫した実行は設計移行であり、実platformの選定・release gateは未確認です。Platform provenanceも設計移行であり、製品固有のgeneratorや認証serviceは未実装です。
領域全体の移行完了・組織への導入を意味しません。
