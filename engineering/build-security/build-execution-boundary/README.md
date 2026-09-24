# ENG-BUILD-001: Build execution boundary

## 利用場面と推奨構造

依存・test・pluginの実行を、ソース管理・公開・deployの権限から切り離す設計です。
開発者と基盤担当者が、取得・実行・観測・出力受入をどこに分けるか選べるようにします。

```text
認証が必要な取得境界 → 固定・照合した入力
                          ↓
            秘密情報なしの一時build環境
            限定した書込領域／通信を外側で制限
                          ↓
              固定した成果物を外側で識別
                          ↓
              別consumerが期待値を照合 → 公開／deploy

外側のsensor・health・配送 → job identityと結合した調査ログ → 担当者
```

Digestは生成したbytesを識別しますが、信頼済みの内容として承認するものではありません。
成果物に含まれるhook・設定・テンプレートをconsumerが高権限で実行する場合も、受入の信頼境界としてレビューします。

## 方式と代償

| 方式 | 選ぶ条件・代償 |
|---|---|
| 取得後に通信を閉じる | 必要入力を事前に用意できる場合。初期化・追加取得の要求を把握する必要がある |
| 限定proxy経由で取得する | 動的取得が必要な場合。直通、DNS、redirect、許可先への送信を別に制限・観測する |
| 非特権containerで実行する | Host mount・socket・共有kernel・networkの境界を確認できる場合。Containerだけで完全隔離とは扱わない |
| VM等の専用世代で実行する | より強いhost分離が必要な場合。生成・image管理・破棄の運用費が増える |

Read-only rootに専用workspaceと一時領域を組み合わせ、書込先を具体化します。
取得用tokenやsensorのkernel権限をjob内へ置かず、必要な管理権限は外側のサービスが持ちます。
Hosted runnerで必要な通信・隔離制御を実現できない場合は、未確認を埋めず、方式を変えるか明示的なrisk判断へ回します。

## 何を観測して確認するか

| 境界 | 採用先で行う無害な確認 | 残る限界 |
|---|---|---|
| 権限・ファイル | 管理したdummy secret領域、書込禁止領域、管理socketへのアクセスを拒否できるか | 実secretを試験へ使わない。拒否試験だけで全到達経路を網羅しない |
| 通信 | 管理下の試験宛先を使い、許可・拒否、proxy迂回、redirectを照合する | Metadataから認証情報を取得しない。許可宛先の無害性は保証しない |
| 観測 | 無害なprocess・接続イベントを発生させ、job identityと配送先で照合する | Event取得だけでruleやalert対応の有効性は証明しない |
| Health | 検証用環境でsensor・配送の停止を検出し、出力昇格を止めるか | 本番sensorを無断で停止しない。未対応platformは`NOT_CHECKED` |
| Consumer | Build側から取得・公開・deploy権限へ届かず、未承認出力を受取側が拒否するか | Artifactが正規でもアプリケーション欠陥や悪意は残る |

結果は設定宣言、実行時の拒否、観測、配送、対応を分けて記録します。
未実施は`NOT_CHECKED`、収集異常は`ERROR`、確認した違反は不合格です。
必要な観測が失われた出力は、正常に生成できても自動で公開へ昇格させません。

## Sensorの採否

[REF-BUILD-001](../../../sources/README.md#ref-build-001)はcicd-sensorの調査候補です。今回も未導入です。
採用前に固定版・integrity、kernel権限、platform対応、収集範囲、redaction・retention、health、通知先を確認します。
CIの短命jobへの組込みと、本番のFalco／Sysdigによる継続監視は別の運用です。

## このpatternの範囲

今回はplatform固有のsandbox・firewall・sensor実装を追加していません。
旧JSON検証器は計画の宣言を調べるだけなので、実際の封じ込めを確認する実装として移植しません。
来歴の生成権限はuser-defined buildから分け、consumer側の期待値照合へ引き継ぎます。
この設計だけでSLSA levelや組織の導入済み状態を主張しません。

- [Control](../../../controls/records/build-security/psb-build-001-build-containment/README.md)、[教材](../../../controls/records/build-security/psb-build-001-build-containment/learning.md)
- [CI state and runner lifecycle](../../cicd-security/ci-state-and-runner-lifecycle/README.md)
- [仕様と採否](../../../sources/README.md#spec-build-containment)
- [Consumer artifact acceptance](../../release-integrity/consumer-artifact-acceptance/README.md): 固定した出力をconsumerの期待値で受け入れる次の境界
