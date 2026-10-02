# タグが動くと、CIで何が変わるか

対象は[PSB-CICD-001 Workflow dependency identity](README.md)、設計の行き先は[Reviewed workflow dependency binding](../../../../engineering/cicd-security/reviewed-workflow-dependency-binding/README.md)です。

## 昨日と同じworkflowなのに

あるチームは外部Actionを`vendor/build@v1`で呼び、生成したpackageをreleaseへ渡しています。レビューした日に`v1`が指していたコードは正常でした。後日、配布元のアカウントを奪った攻撃者が`v1`を別commitへ動かします。チームのworkflowには差分がありませんが、次の実行では別のコードが動きます。

そのjobが公開済みsourceを読むだけなら、非公開情報の持ち出し経路は限られます。それでも結果をrelease判断に使えば、検査の偽装が後続へ届く可能性があります。非公開source、secret、書込みtoken、OIDCや公開権限を利用できれば、持ち出しや成果物改ざんへつながります。参照方法と、そのjobが何へ触れられるかを一緒に見ます。

## 名前、内容、出所は別の問い

タグやbranchはcommitに付けた名前で、後から指す先を変えられます。完全なcommit SHAは特定のGit objectを選びます。Containerのdigestはimageの内容を選びます。固定すると新しい内容を取り込むために利用側の差分が必要になり、変更をレビューへ戻せます。

しかし、40桁の文字列が書かれていることと、正規の配布元の意図したcommitであることは別です。検査scriptが外部へ問い合わせないなら、存在・出所・releaseとの関係を確認していません。SHA横の`# v1.2.3`も説明用のコメントで、実行する内容を決めるのは参照そのものです。

## 固定したのに、内側で変わる例

固定commitのActionが、実行時に`https://.../latest/tool.sh`を取得して実行するとします。外側のSHAは変わりませんが、取得したscriptの内容は変わり得ます。タグ付きbase image、lockなしのpackage取得、内部のタグ付きActionにも同じ問いがあります。このように、依存先のさらに先を**推移的依存**と呼びます。

見るべきものは固定commitの`action.yml`、呼出workflow、実行するscript・Dockerfile、そこから取得する実行物です。読んだファイルと取得経路を更新PRへ残し、「見た範囲では可変取得なし」「可変取得あり」「未確認」「取得・確認に失敗」を区別します。静的なsourceだけで外部serviceや実行時の全経路を確認できたとは言いません。

可変取得があり、jobに強い権限が必要なら、取得物の検証、小さな自社scriptへの置換、レビューしたfork、権限の分離、期限付き例外を比較します。確認範囲の外に経路が残ること自体を隠さないのが判断基準です。

## 誤解をほどく

| よくある判断 | 確認し直すこと |
|---|---|
| 固定したので更新は不要 | 固定した版の脆弱性は残る。更新の差分・内容と期限を確認する |
| 公式Actionなら固定不要 | 信頼する配布元でも、名前が指す内容を後から変更できる |
| GitHubのSHA policyで全て済む | Actionとreusable workflowで適用範囲が違う。対象ごとに確認する |
| ローカルActionは安全 | `./`はcheckoutしたコードを使う。そのコードを誰が変更できたかを確認する |
| 検査jobが緑ならmerge保護も有効 | required check、review担当、迂回権限を別に確認する |

自分のworkflowを読む時は、最初に「外部コードの内容を何で選ぶか」、次に「その内側で何を取得するか」、最後に「その実行が持つ権限と後続への影響」を追ってください。具体的な参照構文と安全なローカル確認は[実装README](../../../../engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)にあります。仕様・確認日・採否は[Sources](../../../../sources/README.md#spec-workflow-dependency-references)へたどれます。
