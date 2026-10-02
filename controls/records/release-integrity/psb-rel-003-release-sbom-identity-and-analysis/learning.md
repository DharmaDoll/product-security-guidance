# 学習：そのSBOMは、どこを調べて作ったものか

対応するcontrol：[PSB-REL-003 Release SBOM identity and analysis](README.md) · 設計：[Release SBOM identity and analysis intake](../../../../engineering/release-integrity/release-sbom-identity-and-analysis/README.md)

## PRで作った部品表を、そのまま公開したら

あるチームはPRごとに依存関係の定義ファイルからSBOM（ソフトウェア部品表）を作っていました。リリース時にも同じSBOMを分析基盤へ送り、受付成功を見て作業を終えました。

ところが、完成したコンテナーイメージには、base imageのOSパッケージや、ビルド中に取得したバイナリが加わっていました。PR時の一覧にはありません。後日、そのバイナリに脆弱性が報告されても、部品台帳の検索は0件でした。未収載なのに「影響なし」と判断しそうになったのです。

これは取得地点を考えるための架空の場面です。問題はファイルの有無だけでなく、何を調べた一覧なのかを、利用する判断へ結び付けなかったことにあります。

## 三つの地点で、答えられる問いが変わる

| 取得地点 | 主に分かること | それだけでは分からないこと |
|---|---|---|
| ソース・依存関係定義 | 開発時に採用を意図した依存と変更 | 後のビルドで加わる部品、最終的に配布する内容 |
| 完成物の組立後・公開前 | 配布するファイルやimageに含まれる部品 | ツールが観測できない部品、実際の配置先 |
| 配置時・稼働中 | どの成果物がどこに配置され、何が追加観測されたか | 未観測環境やメモリ上の全構成要素 |

この考え方は[利用者提供のSBOM lifecycle資料](../../../../sources/README.md#ref-release-sbom-lifecycle-001)を設計入力にしています。PRやimage build直後という特定のタイミングを全製品へ固定せず、成果物が生成・変化する場所を確認します。

ソースの観測は早い段階での修正に役立ちます。リリースの一覧は完成物へ結び、稼働環境の観測は配置先の調査に使います。同じ台帳へ集めても、元の記録を上書きせず、commit・成果物digest・配置先の識別子で関係付けます。

共通base imageや供給者から受け取るSBOMも入力の一つです。それを正しく受け入れる判断は[REL-004](../psb-rel-004-supplier-sbom-intake-trust/learning.md)で行い、追加・削除・更新後の最終製品を説明するSBOMとは分けます。

## Hashが一致しても、観測した証明にはならない

Digestは内容から計算する識別値です。成果物とSBOMの対応を保つために使います。一方、ソースだけから作ったSBOMへ完成物のhashを追記しても、部品の見落としはなくなりません。`post-build`という観測段階のラベルだけを追記した場合も同じです。

確認するのは、生成ツールへ実際に何を入力したか、どの成果物を調べたか、対象に含まれる部品のうち何が見えないかです。[既存のhash照合スクリプト](../../../../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)は文書の記述と実ファイルを比較しますが、この生成過程を証明する道具ではありません。

CycloneDXの形式に適合することと部品の網羅性も別です。`compositions`の`complete`・`incomplete`・`unknown`は、記載範囲の完全性についての表明です。生成ツールの対応範囲や除外条件を調べず、`complete`という値だけで完全と判断しません。

## 受付から分析までを一つの成功にしない

分析基盤が受け付けた後にも、形式の検証、部品の取込、脆弱性情報との照合が続きます。どのSBOMをどの製品・版へ送ったかを保持し、今回必要な処理が終わったかを確認します。製品の通知名と各処理の対応は[設計の状態表](../../../../engineering/release-integrity/release-sbom-identity-and-analysis/README.md#6-受付と処理完了を分ける)で扱います。

部品や脆弱性の検索が0件でも、SBOMの不足、処理失敗、古い脆弱性データ、検索結果の取り漏れである可能性があります。未確認の範囲を残したまま、部品から成果物、配置先、担当者へ辿ります。「一覧にない」と「製品に含まれない」を同じ結果にしないことが、この場面の判断基準です。

診断項目は[control](README.md#failure-checks)、生成・公開・分析の構成は[設計パターン](../../../../engineering/release-integrity/release-sbom-identity-and-analysis/README.md)、資料ごとの採否は[参照資料記録](../../../../sources/README.md#ref-release-sbom-lifecycle-001)へ戻れます。
