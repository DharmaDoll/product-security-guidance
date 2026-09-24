# Zero findings is a scoped observation

[コントロール記録](README.md) · [設計パターン](../../../../engineering/detection-verification/scanner-acquisition-and-evidence-boundary/README.md)

## シナリオ

Pipelineは「脆弱性0件」と表示した。しかしscan jobはDB更新に失敗し、空のresults配列だけを後段へ渡していた。
別の日にはscanは成功したが、IaCだけが対象でcontainer imageは検査されていなかった。どちらも製品全体のclean resultではありません。

## 三つの状態

`CLEAN`は、宣言した対象とカテゴリについて検査が完了し、blocking findingがなかった状態です。
`FINDING`は、policyに該当する観測結果です。`ERROR`は、検査結果を評価できない状態です。空配列はこの区別を持たないため、単独ではclean evidenceになりません。

さらに、cleanは時点と検出能力に限定されます。Databaseに未登録の脆弱性、scannerが扱わないlogic flaw、検査しなかったartifact、本番で後から起きた侵害は含みません。

## Scannerも依存関係である

Scannerはsource、artifact、credentialへ触れる実行コードです。Version文字列だけでなく配布artifact、publisher、実行binaryを確認します。
検出dataとpolicyも結果を変えるため、tool identityとは別に記録します。Scannerを増やすことはcoverage候補を増やす一方、更新経路と攻撃面も増やします。

設計は[Scanner acquisition and evidence boundary](../../../../engineering/detection-verification/scanner-acquisition-and-evidence-boundary/README.md)、保証目標は[コントロール記録](README.md)を参照してください。
