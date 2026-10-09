# PSB-BUILD-001 Build containment

**ビルド中に動くコードから、秘密情報や公開・deploy権限へ届かないか。**

## なぜ必要か

例えば、承認した依存でも準備処理やテスト中にコードが動きます。同じ環境に公開用tokenやhostの管理socketがあれば、そのコードが本来のビルドを超える操作をできます。

## 満たすべきこと

1. **取得と実行の権限を分ける。** 認証が必要な入力は別の境界で用意し、ビルドコードへ秘密情報、token発行能力、管理面の書込権限を渡さない（BUILD-1）。Buildとdeployも分け、固定した成果物を受取側が独立して判断する（BUILD-2）。
2. **外へ出られる経路を絞る。** 通信を既定で拒否し、必要な宛先だけをビルドコードの外側で許可する（BUILD-3）。一時的な非root環境と限定した書込領域を使い、host socketや管理サービスへ届かせない（BUILD-4）。
3. **拒否と観測を確認する。** Process・networkの動きを観測し、sensorとログ配送が動いているかも別に確かめる（BUILD-5）。設定や観測が欠ける、古い、部分的な場合は合格にせず、成果物を公開工程へ進めない（BUILD-6）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 依存やテストのコードから、取得用認証情報、token発行、公開・deploy権限を利用できないか。
- 非root・読み取り専用の設定でも、host mountやsocketから外側を操作できないか。
- 拒否した宛先へ、直通、DNS、proxy、redirect、metadata経由で到達できないか。
- 許可先への送信を、内容まで承認したものとして扱っていないか。
- Sensor停止、ログ配送失敗、古い観測を「異常なし」として公開を進めないか。
- ビルドが出力した設定やhookを、後続の高権限処理がそのまま実行しないか。

これらは診断項目であり、実環境で拒否を確認した結果ではありません。無害な確認方法は[engineeringの確認表](../../../../engineering/build-security/build-execution-boundary/README.md#何を観測して確認するか)にあります。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| SLSA Build track v1.2 Build L3「Hardened builds」 | ビルド中のコードを基盤の秘密情報や管理権限から離し、使い捨ての環境で動かす設計が一部を支える。 | Build間の隔離、cache汚染、署名鍵の保護、基盤の実評価は未確認。 |
| OpenSSF OSPS Baseline 2026.02.19 OSPS-BR-01.03 | 未信頼のコードを扱う処理へ特権CI資産を渡さない部分を支える。 | 全pipelineの実際の権限と拒否は未確認。 |

対応範囲は[マッピング](../../../../mappings/frameworks.yaml)に記録しています。このControlだけでSLSA Build L3やOSPSへの準拠を達成したとは言えません。

## このコントロールの範囲

対象はソース、依存、plugin、テストのコードが動くビルド環境です。Runnerの割当・破棄は[CICD-007](../../cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md)、取得した依存の同一性は[DEPS-003](../../dependency-security/psb-deps-003-dependency-artifact-identity/README.md)、承認したビルド手順は[BUILD-002](../psb-build-002-approved-consistent-build/README.md)、来歴の生成は[BUILD-003](../psb-build-003-platform-provenance-generation/README.md)へ渡します。隔離しても成果物の中身の無害性は示せません。

取得・実行・観測・出力受入をどこで分けるかは[engineering](../../../../engineering/build-security/build-execution-boundary/README.md)で選びます。旧JSON計画検査は実行時の拒否を示さないため移植していません。[教材](learning.md)、特性IDと根拠を残した[control.yaml](control.yaml)、仕様の採否を示す[Sources](../../../../sources/README.md#spec-build-containment)と[sensor候補](../../../../sources/README.md#ref-build-001)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
