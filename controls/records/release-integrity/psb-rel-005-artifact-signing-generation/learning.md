# 学習：署名が正しくても、署名した対象が違う

対応するcontrol：[PSB-REL-005 Artifact signing generation](README.md) · 設計：[Artifact signing boundary](../../../../engineering/release-integrity/artifact-signing-boundary/README.md)

リリース担当者が`v2.0`を承認しました。署名jobは`app:latest`を取得して正規の署名鍵で署名します。その間に別のjobが`latest`を更新すると、暗号検証が成功しても、承認した`v2.0`のbytesへ署名したとは言えません。

ここで守るのは「署名がある」という表示ではなく、「承認した一つの成果物のbytesに、許可した主体が署名し、利用者がその関係を確かめられること」です。可変の名前を使う場合は、その時点で解決したdigestを固定し、承認時・署名時・公開時の対象を照合します。ファイルなら実際のbytes、OCI imageなら採用形式が署名するmanifest digestなど、何を署名するのかを明記します。

もう一つの落とし穴は、署名鍵を安全に保管すれば署名対象も安全になるという思い込みです。鍵を持ち出せないKMSでも、権限のあるjobが別のartifact digestを渡せるなら不正な成果物に正規の署名を付けられます。署名操作の認可と、署名する対象の承認は別に確認します。

署名結果を作った後も、利用者が対応する署名と信頼根拠を取得できなければ意味がありません。発行時刻や透明性ログの証拠は採用した方式で必要なときに揃えます。単にJSONへ`included: true`と書いても証拠にはなりません。署名器や公開先が止まった場合は、リリースを止めて原因を確認します。

判断するときは次を順に問います。誰がその成果物を承認したか。署名器へ渡した実際のbytesまたはdigestは何か。誰にどの範囲の署名権限があったか。署名結果を想定する利用者の条件で検証できるか。正確な成果物から署名を取得できるか。この問いのどれかが未確認なら、暗号署名が一つ存在してもリリース完了とはしません。

この例で署名するのは成果物です。ビルド条件を記した来歴情報への署名とは対象が異なります。成果物署名が成功しても来歴が生成・配布されたとは判断せず、必要な証明をそれぞれ取得します。

利用者自身の受入条件は[REL-001の教材](../psb-rel-001-signature-provenance-verification/learning.md)、来歴が取得できるかは[REL-002の教材](../psb-rel-002-provenance-distribution-availability/learning.md)、来歴の内容を誰が決めるかは[BUILD-003の教材](../../build-security/psb-build-003-platform-provenance-generation/learning.md)で続けて学べます。参照資料と採否は[REF-ARTIFACT-SIGNING-BOUNDARY-001](../../../../sources/README.md#ref-artifact-signing-boundary-001)を参照してください。
