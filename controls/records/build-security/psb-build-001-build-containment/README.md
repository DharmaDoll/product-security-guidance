# PSB-BUILD-001 Build containment

**ビルド中に動くコードから、秘密情報や公開・deploy権限へ届かないか。**

## なぜ必要か

例えば、承認した依存でも準備処理やテスト中にコードが動きます。同じ環境に公開用tokenやhostの管理socketがあれば、そのコードが本来のビルドを超える操作をできます。

## 満たすべきこと

1. **取得と実行の権限を分ける。** 認証が必要な入力は別の境界で用意し、ビルドコードへ秘密情報、token発行能力、管理面の書込権限を渡さない（BUILD-1）。Buildとdeployも分け、固定した成果物を受取側が独立して判断する（BUILD-2）。
2. **外へ出られる経路を絞る。** 通信を既定で拒否し、必要な宛先だけをビルドコードの外側で許可する（BUILD-3）。一時的な非root環境と限定した書込領域を使い、host socketや管理サービスへ届かせない（BUILD-4）。
3. **拒否と観測を確認する。** Process・networkの動きを観測し、sensorとログ配送が動いているかも別に確かめる（BUILD-5）。設定や観測が欠ける、古い、部分的な場合は合格にせず、成果物を公開工程へ進めない（BUILD-6）。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| 取得後に通信を閉じる | 必要入力を事前に用意できる場合。初期化・追加取得の要求を把握する必要がある |
| 限定proxy経由で取得する | 動的取得が必要な場合。直通、DNS、redirect、許可先への送信を別に制限・観測する |
| 非特権containerで実行する | Host mount・socket・共有kernel・networkの境界を確認できる場合。Containerだけで完全隔離とは扱わない |
| VM等の専用世代で実行する | より強いhost分離が必要な場合。生成・image管理・破棄の運用費が増える |

読み取り専用のルートに専用の作業領域と一時領域を組み合わせ、書き込める場所を決めます。
取得用tokenやセンサーのkernel権限はjobへ渡さず、必要な管理権限を外側のサービスへ持たせます。
取得を済ませる前に依存の準備スクリプトを動かすと、取得用tokenをそのコードへ渡す経路が残ります。[Install execution policy](../../dependency-security/psb-deps-002-install-execution-policy/README.md)で、取得とコード実行を分けられる方式を選びます。
利用するrunnerで必要な通信・隔離制御を実現できなければ、方式を変えるか、残るリスクを明示して判断します。

## 何を観測して確認するか

| 境界 | 採用先で行う無害な確認 | 残る限界 |
|---|---|---|
| 権限・ファイル | 管理したdummy secret領域、書込禁止領域、管理socketへのアクセスを拒否できるか | 実secretを試験へ使わない。拒否試験だけで全到達経路を網羅しない |
| 通信 | 管理下の試験宛先を使い、許可・拒否、proxy迂回、redirectを照合する | Metadataから認証情報を取得しない。許可宛先の無害性は保証しない |
| 観測 | 無害なprocess・接続イベントを発生させ、job identityと配送先で照合する | Event取得だけでruleやalert対応の有効性は証明しない |
| Health | 検証用環境でsensor・配送の停止を検出し、出力昇格を止めるか | 本番sensorを無断で停止しない。未対応platformは`NOT_CHECKED` |
| Consumer | Build側から取得・公開・deploy権限へ届かず、未承認出力を受取側が拒否するか | Artifactが正規でもアプリケーション欠陥や悪意は残る |

設定したこと、実際の拒否、イベントの観測、配送、担当者の対応は分けて記録します。
未実施は`NOT_CHECKED`、収集異常は`ERROR`、確認した違反は不合格です。
必要な観測が失われた出力は、正常に生成できても自動で公開へ昇格させません。

## センサーを採用するとき

[REF-BUILD-001](../../../../sources/README.md#ref-build-001)はcicd-sensorの調査候補です。今回も未導入です。
採用前に固定版・integrity、kernel権限、platform対応、収集範囲、redaction・retention、health、通知先を確認します。
CIの短命jobへの組込みと、本番のFalco／Sysdigによる継続監視は別の運用です。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 依存やテストのコードから、取得用認証情報、token発行、公開・deploy権限を利用できないか。
- 非root・読み取り専用の設定でも、host mountやsocketから外側を操作できないか。
- 拒否した宛先へ、直通、DNS、proxy、redirect、metadata経由で到達できないか。
- 許可先への送信を、内容まで承認したものとして扱っていないか。
- Sensor停止、ログ配送失敗、古い観測を「異常なし」として公開を進めないか。
- ビルドが出力した設定やhookを、後続の高権限処理がそのまま実行しないか。

これらは診断項目であり、実環境で拒否を確認した結果ではありません。無害な確認方法は[上の方式説明](#何を観測して確認するか)にあります。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| SLSA Build track v1.2 Build L3「Hardened builds」 | ビルド中のコードを基盤の秘密情報や管理権限から離し、使い捨ての環境で動かす設計が一部を支える。 | Build間の隔離、cache汚染、署名鍵の保護、基盤の実評価は未確認。 |
| OpenSSF OSPS Baseline 2026.02.19 OSPS-BR-01.03 | 未信頼のコードを扱う処理へ特権CI資産を渡さない部分を支える。 | 全pipelineの実際の権限と拒否は未確認。 |

対応範囲は[マッピング](../../../../mappings/frameworks.yaml)に記録しています。このControlだけでSLSA Build L3やOSPSへの準拠を達成したとは言えません。

## このコントロールの範囲

対象はソース、依存、plugin、テストのコードが動くビルド環境です。Runnerの割当・破棄は[CICD-007](../../cicd-security/psb-cicd-007-runner-lifecycle-isolation/README.md)、取得した依存の同一性は[DEPS-003](../../dependency-security/psb-deps-003-dependency-artifact-identity/README.md)、承認したビルド手順は[BUILD-002](../psb-build-002-approved-consistent-build/README.md)、来歴の生成は[BUILD-003](../psb-build-003-platform-provenance-generation/README.md)へ渡します。隔離しても成果物の中身の無害性は示せません。

取得・実行・観測・出力受入をどこで分けるかは、上の方式と確認表で選びます。旧JSON計画検査は実行時の拒否を示さないため移植していません。[教材](learning.md)、特性IDと根拠を残した[control.yaml](control.yaml)、仕様の採否を示す[Sources](../../../../sources/README.md#spec-build-containment)と[sensor候補](../../../../sources/README.md#ref-build-001)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。

工程間の受け渡しは[ビルドした成果物を署名・公開し、使用するまで](../../../../engineering/release-build-to-use.md)で確認できます。
