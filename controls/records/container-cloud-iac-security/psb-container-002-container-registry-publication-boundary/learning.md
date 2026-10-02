# 学習：レジストリに残すことと、使用を止めること

対応するcontrol：[PSB-CONTAINER-002 Container registry publication boundary](README.md) · 設計：[Container registry publication and lifecycle](../../../../engineering/container-cloud-iac-security/container-registry-publication-and-lifecycle/README.md)

## 問題のあるイメージを消すべきか

架空の場面です。公開済みイメージに問題が見つかり、担当者はそのdigestを`quarantined`にしました。調査と切り戻しの判断に必要なため、registry上の内容と公開記録は残します。別の利用者は古いタグや複製先から同じdigestを取得できます。Registryに残すという判断と、新しい実行を許すという判断は同じではありません。

Registryは、誰がどのrepositoryへ公開・変更・削除できるか、公開した内容をどのdigestで識別するかを管理します。Tagは人が見つけやすい名前ですが、付替えられる場合があります。OCIの複数platform向けimageでは、indexと各platformのmanifestにそれぞれdigestがあるため、公開記録にはどれを指すかも残します。

## 状態名だけでは決められない

`active`、`deprecated`、`quarantined`、`removed`は運用上の状態名です。例えば`deprecated`を期限付きの切り戻しに許す設計もあります。一方、使用停止と決めた`quarantined`は、bytesが残っていても[使用直前の許可](../psb-container-001-deployment-artifact-admission/learning.md)で拒否する必要があります。状態と使用可否、対象、期限、判断根拠を別に記録します。

削除だけではcacheや複製先、既に稼働中の環境まで止められません。[GOV-005の復旧判断](../../governance-operations/psb-gov-005-deployed-artifact-recovery/learning.md)には、新digestの公開と旧digestの使用停止を渡し、稼働先で旧digestが残らないかは別に観測します。状態の通知やinventoryが途切れたときも、「もう使われていない」とは結論しません。

採用先で試す項目は[controlの診断観点](README.md#failure-checks)、資料の採否は[Sources](../../../../sources/README.md#ref-container-registry-publication-001)にあります。
