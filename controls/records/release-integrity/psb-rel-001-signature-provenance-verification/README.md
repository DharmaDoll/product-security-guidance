# PSB-REL-001: Signature and provenance verification

学ぶ：[正しい署名でも、使ってよい成果物とは限らない](learning.md) · 設計する：[Consumer artifact acceptance](../../../../engineering/release-integrity/consumer-artifact-acceptance/README.md)

## 問い

使用する成果物のbytesと来歴を結び、利用者が承認した署名者・builder・ソース・ビルド条件に一致するものだけを受け入れられるか。

## できてはいけないこと

別の成果物の有効な来歴、未承認の署名者、正規builderが生成した想定外のソース・条件の成果物を受け入れてはいけません。
配布側が同梱した公開鍵やpolicyを、そのまま利用者の信頼根拠にしてはいけません。
署名や来歴が取れない場合に、検証なしの取得経路へ自動で切り替えてはいけません。

## 適用範囲と非適用

取得した成果物、署名付き来歴、利用者側の信頼根拠と期待値、使用直前の受入判断が対象です。
署名生成、builderの隔離、[証跡の配布](../psb-rel-002-provenance-distribution-availability/README.md)、成果物の脆弱性・悪意の検査は別の保証です。
固定公開鍵とkeyless方式では認証の確認方法が異なるため、方式固有の検証を実装で定めます。

[REL-005](../psb-rel-005-artifact-signing-generation/README.md)の成果物署名は、対象の内容と署名者を結びます。ここで検証する来歴への署名は、ビルド条件などを記した文書を認証します。成果物署名だけで来歴の確認を済ませず、利用者が両方を要求する場合はそれぞれの条件を確認します。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `ACCEPT-1` | 使用するbytesのdigestが、認証した来歴のsubjectに一致する |
| `ACCEPT-2` | 利用者が承認した信頼根拠で来歴の署名を確認する。配布物自身から信頼根拠を自動登録しない |
| `ACCEPT-3` | 採用した来歴の形式・種類を確認し、署名者とbuilderの組合せ、build type、正規ソース、承認revision・ref、外部parameterが利用者の期待値に一致する |
| `ACCEPT-4` | 保護対象の成果物familyで必要な署名・来歴を欠落・低下させない。変更は独立した承認で管理する |
| `ACCEPT-5` | Parser・crypto tool・入力収集の失敗を受入成功にしない。違反と評価不能を区別し、いずれも使用を止める |

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 別の成果物に対する有効な署名・来歴を付けても、使用する内容とのdigest不一致を拒否できるか。
- 未承認の公開鍵や期待値を配布物へ同梱し、それを自動登録させて検証を通せないか。
- 正しい署名でも、想定外のbuilder、forkのソース、未承認revision、外部パラメーターで作った成果物を使用できないか。
- 別の種類の証明や未対応形式を来歴として扱わないか。解釈できない外部パラメーターを黙って無視しないか。
- 必須の署名・来歴が欠けた時や取得が失敗した時に、検証不要の経路へ切り替わらないか。
- 解析・暗号検証ツールの異常終了やタイムアウトを成功へ変換せず、実際の使用を止めるか。
- 検証後にファイル、可変tag、取得先を差し替えても、以前の合格結果で別の内容を使用できないか。
- 古いpolicy版や別digestの合格結果を再利用し、現在の受入条件を迂回できないか。

設計レビューや診断に使う項目です。実際の署名サービスや使用を止める仕組みで確認した結果ではありません。

## 実装判断

期待値は、受け取った来歴の値をコピーして作るのではなく、利用者の承認経路で管理します。
新しいbuilderや鍵への変更と、成果物の通常更新を別の変更としてレビューします。
Build levelをpolicyへ使うなら、builderの自己申告ではなく、利用者が信頼する評価根拠と上限を管理します。

検証したファイルを後で別のtagやpathから再取得すると、照合したbytesを使ったとは限りません。
同じdigestのbytesを使用境界まで維持し、未検証出力を高権限で実行しない構造にします。
Artifact digestの照合を先に行っても、来歴が認証されるまでは受入の根拠にはなりません。

## 保証しない範囲

承認builder・鍵の侵害、正規ソース内の悪意、アプリケーション欠陥は検出できない場合があります。
署名成功は無害性やSLSA level達成の証明ではありません。鍵の失効・rotation、certificate、timestamp、transparency検証は方式固有の実装・運用が必要です。
今回は旧crypto実装を移植せず、実際の署名・拒否・使用gateは未確認です。

- [教材](learning.md)
- [Consumer artifact acceptance pattern](../../../../engineering/release-integrity/consumer-artifact-acceptance/README.md)
- [参照仕様と採否](../../../../sources/README.md#spec-consumer-artifact-verification)
- [Framework mapping](../../../../mappings/frameworks.yaml): 旧版・ID・関係を保持。特性割当はレビュー中
