# Zero findings is a scoped observation

[コントロール記録](README.md) · [設計パターン](../../../../engineering/detection-verification/scanner-acquisition-and-evidence-boundary/README.md)

## シナリオ

Pipelineは「脆弱性0件」と表示した。しかし検査jobはDB更新に失敗し、空の結果だけを後段へ渡していた。
別の日には検査は成功したが、IaCだけが対象でcontainer imageは調べていなかった。どちらも製品全体が問題なしという結果ではありません。

## 三つの状態

`CLEAN`は、決めた対象とカテゴリについて検査が完了し、受入を止める指摘がなかった状態です。
`FINDING`は、方針に該当する指摘がある状態です。`ERROR`は、検査結果を評価できない状態です。空配列にはこの区別がなく、単独では問題なしの証拠になりません。

例えばIaCから受入を止める指摘が一件出た後、container imageの解析が失敗した場合、全体を`FINDING`だけにするとimageも調べ終えたように見えます。`ERROR`だけにするとIaCの指摘が消えます。検査全体は評価不能として受入を止め、得られた一件の指摘も調査へ残します。

さらに、問題なしという観測は時点と検出能力に限定されます。DBに未登録の脆弱性、scannerが扱わない処理の欠陥、未検査の成果物、本番で後から起きた侵害は含みません。

## Workflowの検査が成功したのに変更を止められない

PRでworkflowが変更され、zizmorが指摘をSARIFへ出しました。SARIFは指摘を別のtoolへ渡す形式です。[現在の公式仕様](../../../../sources/README.md#spec-zizmor-workflow-analysis)では、この出力modeは指摘があっても終了コードが0になり得ます。したがって「job成功＝指摘なし」と考えると、止めるべき変更が通ります。

次に、対象の一部が壊れたYAMLだった場合を考えます。「対象なしを拒否する設定」は、他のfileを読めた状態で起きる解析失敗まで拒否する設定とは限りません。予定した対象、実際に集めた対象、正常に解析できた対象を比べる必要があります。PRが設定やignoreも変更できるなら、指摘0件は除外を増やした結果かもしれません。

判断する順序は、**同じ変更を調べたか、必要な範囲を最後まで調べたか、承認した方針で指摘を判断したか、その判断がmergeの条件か**です。Security画面へのuploadは結果の表示であり、それだけではmergeを止めません。

例えば書込権限を持つPR jobへの指摘がなくても、呼出先scriptの通信やprovider設定まで確認したことにはなりません。静的検査の観測範囲と、[jobの権限](../../cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)・[未信頼PRの分離](../../cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)を別々に読みます。配置と方式は[Workflow analysis gate and reporting](../../../../engineering/cicd-security/workflow-analysis-gate-and-reporting/README.md)へ続きます。

## Scannerも依存関係である

Scannerはsource、成果物、credentialへ触れる実行コードです。Version文字列だけでなく配布物、発行者、実際に使うbinary・imageを確認します。
検出データと方針も結果を変えるため、toolとは別に記録します。Scannerを増やすと検出の候補が増えますが、更新経路と攻撃面も増えます。

設計は[Scanner acquisition and evidence boundary](../../../../engineering/detection-verification/scanner-acquisition-and-evidence-boundary/README.md)、保証目標は[コントロール記録](README.md)を参照してください。
