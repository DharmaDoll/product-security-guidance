# PSB-CICD-006 Workload federation boundary

**承認したCI jobだけが、必要なクラウド権限を必要な時間だけ取得できるか。**

## なぜ必要か

例えば、本番deploy用のjobだけに権限を渡すつもりでも、同じissuerが発行したtokenなら別repositoryや未承認のbranchからも交換できる設定では、別のjobが本番権限を得ます。正規のtokenであることと、そのjobを許可することは別の判断です。

## 満たすべきこと

1. **交換してよいjobを限定する。** 交換先でissuer、tokenの真正性と期限を確認する（FED-1）。Audienceと安定したworkload identityを結び付け、branch、Environment、workflowなど必要な条件を実際の強制点へ置く（FED-2）。Tokenのclaimに値があるだけでは、その条件を使ったことにならない。
2. **取得経路と操作を絞る。** Token取得・交換は保護されたjobに限り、未信頼PRのコードや成果物をそのjobで実行しない（FED-3）。交換後のaccount・role、許す操作・resource、sessionの長さも必要な範囲にする（FED-4）。短命な認証情報でも有効期間中は悪用できる。
3. **古い経路と実際の設定を確認する。** 移行後の長期keyは保存場所から消すだけでなく、以前の利用者を移し、その権限が使えないことを確かめる（FED-5）。現在の設定、正常な交換、代表的な拒否、旧keyの状態を確認できなければ、導入済みと扱わない（FED-6）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 未承認issuer、期限切れ、真正性を確認できないtokenで権限を得られないか。
- 別audience、別repository・branch・Environment・workflowで発行したtokenが、実際の受入条件を通らないか。
- PR由来のコード、変更可能な呼出先、成果物・cacheを介して交換jobの権限を使えないか。
- 正規jobが交換に成功しても、別account・role、不要な操作・resource、長すぎるsessionを使えないか。
- 移行後も旧keyや既存sessionで同じ操作ができないか。設定や結果を取得できない状態を導入済みとしていないか。

これらは診断・設計レビューの確認項目です。実環境での交換と拒否の結果ではありません。実際に試す場合の無害な操作と証拠の扱いは[GitHub Actions / AWS例](../../../../engineering/cicd-security/workload-federation-boundary/implementations/github-aws/README.md)を参照してください。

## フレームワークとの関係

| 参照先 | このControlとの関係 | 限界 |
| --- | --- | --- |
| GitHub「OIDC reference」 | Audience・subjectを交換先の条件に使う方法と、tokenを求めるjobの権限を示す。 | Claimが存在するだけでは交換先が照合したことにならない。 |
| OpenSSF OSPS Baseline 2026.02.19 OSPS-AC-04.02 | Token取得権限を必要なjobへ限定する部分で関係する。 | OIDCの全claim、交換後のcloud権限、旧鍵の停止は規定しない。 |

この2件は[マッピング](../../../../mappings/frameworks.yaml)上の部分的な設計関係です。実際の交換・拒否や規格への準拠は未確認です。

## このコントロールの範囲

対象はCIのworkloadからクラウド権限への交換、交換後の操作、旧認証経路です。Package registryのTrusted Publishingは別の受入先として判断します。未信頼PRの分離は[CICD-005](../psb-cicd-005-untrusted-pr-boundary/README.md)、job側の発行権限は[CICD-004](../psb-cicd-004-workflow-authority-minimization/README.md)へ渡します。正規job自体の侵害や発行済みsessionの悪用は、この設定だけでは止まりません。

受入条件と権限の分け方は[engineering](../../../../engineering/cicd-security/workload-federation-boundary/README.md)を参照してください。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、仕様の採否を示す[Sources](../../../../sources/README.md#spec-workload-federation)と[補足資料](../../../../sources/README.md#ref-cicd-009)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
