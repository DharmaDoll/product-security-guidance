# 学習：署名が正しくても、記録の中身は誰が決めたのか

対応するcontrol：[PSB-BUILD-003 Platform provenance generation](README.md) · 設計：[Platform-owned provenance generation](../../../../engineering/build-security/platform-owned-provenance-generation/README.md)

## 署名検証が成功したリリース候補

担当者が、通常リリースでは認めていない`debug=true`でビルドを起動しました。ビルドスクリプトは成果物とJSONを出力します。JSONには成果物の正しいdigestと、実際とは異なる`debug=false`を書きました。署名サービスは、そのJSONを受け取って内容を確認せずに署名します。

利用者が署名と成果物のdigestを確認すると、どちらも一致します。しかし、「通常の設定で作った」という記述まで正しいとは言えません。ビルドを動かす側が記録の中身も決められ、署名サービスの信用を借りて自己申告を通せたからです。この場面は説明用であり、特定製品の不具合報告ではありません。

## 来歴情報で確かめたいこと

来歴情報（provenance）は、どの基盤がどの手順・入力から成果物を作ったかを記録します。`subject`は対象成果物、digestはそのbytesを識別する値、`builder.id`は信頼する基盤の境界、`externalParameters`は基盤へ外から渡した入力です。

署名で確認するのは、誰が認証した記録で、認証後に改変されていないかです。認証前に書かれた嘘を署名だけで見抜くことはできません。そこで、ジョブの起動や管理を担う部分（control plane）が受け取った入力を記録し、ジョブにその記録の書き換えや任意の内容への署名を許さない構造を選びます。

上の例なら、基盤が受理した`debug=true`を記録へ残します。そのうえで、公開を判断する側が「通常リリースは`debug=false`」という期待値と比べます。正確な記録を作ることと、その記録から公開を許すことは別の判断です。

## Fieldごとの出所を読む

すべての値が同じ方法で作られるとは限りません。例えば、基盤が起動時の入力を記録し、成果物digestはジョブから受け取る方式もあります。どこを基盤が観測し、どこをジョブが申告し、何を追加照合するかを確認します。SLSAのlevelに応じた例外は[controlの実装判断](README.md#実装判断)を参照してください。

レビューでは、`builder.id`と署名の確認に加えて、公開判断に必要な値の出所をたどります。必要な値を基盤から取得できない場合は、ジョブの申告で埋めて確認済みにしません。採用方式を見直すか、保証できない範囲を残して公開方針を判断します。

## 前後の判断へ戻る

この記録が正しくても、ビルド中に秘密情報を持ち出していないかは[BUILD-001の教材](../psb-build-001-build-containment/learning.md)で考えます。作り手が承認した手順との照合は[BUILD-002の教材](../psb-build-002-approved-consistent-build/learning.md)、配布された成果物を使ってよいかは[REL-001](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)へ進みます。来歴情報の依存一覧だけで、製品に含まれる全構成要素が分かるとも判断しません。

生成側の構成と方式の選択は[設計パターン](../../../../engineering/build-security/platform-owned-provenance-generation/README.md)、仕様と本PJでの解釈の区別は[SPEC-PLATFORM-PROVENANCE-GENERATION](../../../../sources/README.md#spec-platform-provenance-generation)が正本です。
