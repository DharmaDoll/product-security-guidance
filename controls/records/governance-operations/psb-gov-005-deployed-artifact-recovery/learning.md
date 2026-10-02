# 学習：更新後も旧成果物が残るとき

対応するcontrol：[PSB-GOV-005 Deployed artifact recovery](README.md) · 設計：[Deployed artifact rebuild and replacement](../../../../engineering/governance-operations/deployed-artifact-recovery/README.md)

## 新しいイメージを出したのに、終わらない

ある製品で、稼働中のコンテナーイメージに問題が見つかりました。担当者は修正した入力からイメージを作り直し、同じ名前のタグで公開しました。主要な環境は更新され、ビルドと配布のジョブも成功しています。

しかし、別の環境には旧イメージが残り、緊急時の切り戻し設定も旧digestを指していました。タグ名は変わらないため、公開画面だけではどの内容が稼働中か分かりません。これは復旧判断を学ぶための架空の場面です。

## 何を確認したら完了と言えるか

Digestはイメージの内容を識別する値です。[GOV-001の影響調査](../psb-gov-001-supply-chain-impact-assessment/learning.md)で確かめた旧digestと対象環境を、復旧ケースの起点にします。[GOV-003](../psb-gov-003-vulnerability-priority-decision/learning.md)で決めた担当者・対応期限も受け取ります。

まず、新digestが旧digestと異なり、修正を加えたソース、ビルド、来歴、署名、SBOMが同じ新成果物に結び付くか確かめます。次に、対象環境で実際に動くdigestを確認します。新digestの公開や一環境への配布だけでは、旧digestが消えたことになりません。

最後に、元の調査範囲をもう一度観測します。別環境や停止中の作業、観測できない対象があれば、その範囲を未解決として残します。切り戻し経路が旧digestを再投入できるなら、運用上の扱いを決めます。ビルド成功・新digestの稼働・旧digestの非稼働は、それぞれ別の証拠です。
監視アラートが出ていないことやrollout成功表示は、旧digestが動いていない証拠ではありません。停止中のworkloadも旧digestを指定したまま再起動できるなら、対象から消えたとは言えません。
対象の一部を廃止した場合は、新digestの配置を要求する代わりに、その実体が止まり、旧digestを再投入する設定が残らないことを確かめます。検索結果から見えなくなっただけでは廃止の証拠になりません。

## 一時的な許可と復旧完了

別環境の更新が期限に間に合わず、旧digestを一時的に動かす必要がある場合、[GOV-002の例外](../psb-gov-002-security-exception-lifecycle/learning.md)で対象、理由、承認者、失効時刻を限定します。元の対応期限は書き換えません。例外は旧digestの継続使用を一定条件で認める判断であり、修復や復旧の証拠ではありません。

期限切れや取消、台帳を確認できない状態では、その例外を根拠とする利用許可を続けません。旧digestが元の範囲から消えたことを確認できるまで、ケースは開いたままです。どの条件で`REMEDIATED`とするかは[controlの診断項目](README.md#failure-checks)と[設計パターン](../../../../engineering/governance-operations/deployed-artifact-recovery/README.md)へ戻れます。参照資料の採否は[Sources](../../../../sources/README.md#ref-deployed-artifact-recovery-001)に記録しています。
