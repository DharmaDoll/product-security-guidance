# 学習：同じbuilderでも、別の手順で作れば別のrelease

対応するcontrol：[PSB-BUILD-002 Approved and consistent release build](README.md) · 設計：[Approved release build process](../../../../engineering/build-security/approved-release-build-process/README.md)

製品チームは、ホステッドのビルド基盤で`v3.0`を作ると決めています。担当者はレビュー済みソースを指定しましたが、リリースジョブを手動起動し、通常は無効な`debug=true`を渡しました。ジョブは同じ基盤で成功し、成果物には正しいversion名が付きます。この時、ホステッド基盤で作られたという事実だけでは、レビューしたリリース手順で作られたとは言えません。

ビルド基盤（builder）は「どこがビルドを動かしたか」です。ビルド定義は「何を実行するか」、外部パラメーターと起動条件は「今回どの条件で動かしたか」、ソースのrevisionは「どのコードを入力にしたか」です。これらは異なる問いです。さらに、成果物のdigestは「実際にできたbytes」を指します。名前やversionだけでは、その実行の出力かどうかを判別できません。

直感的な誤りは二つあります。一つは、基盤が承認済みならビルド手順も正しいと思うことです。同じ基盤でも、異なる定義やパラメーターで実行できます。もう一つは、ジョブが`builder.id`や`hosted: true`と書いた記録を基盤の証明とみなすことです。未信頼のジョブはその文字列も作れます。

正規リリースと判断するには、作り手側が承認した基盤と手順を先に定め、今回の成果物digestに結び付いた基盤由来の記録と照合します。ビルド定義を別repositoryで管理するなら、そのrevisionも追跡します。証拠が取得できない時は「問題なし」とせず、公開を止めます。

SLSA Build L2を目標にすると、ホステッド基盤でのビルドと、基盤による認証可能な来歴情報（provenance）が必要です。このcontrolでは、作り手側が選んだ基盤と一貫した手順を確認します。ビルド中の権限・隔離は[BUILD-001](../psb-build-001-build-containment/README.md)、来歴の生成と認証は[BUILD-003](../psb-build-003-platform-provenance-generation/README.md)、利用者側の採否は[REL-001](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)で別に確認します。
