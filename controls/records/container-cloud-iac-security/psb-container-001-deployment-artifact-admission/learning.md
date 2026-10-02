# 学習：公開されたイメージを、実行してよいか

対応するcontrol：[PSB-CONTAINER-001 Deployment artifact admission](README.md) · 設計：[Deployment artifact admission boundary](../../../../engineering/container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)

## 同じ名前のイメージなのに中身が違う

架空の場面です。チームは`release`タグのイメージを使う設定を承認しました。その後、同じタグが別の内容へ付け替えられました。さらにPodの作成時には補助コンテナーが追加されます。CIで最初のイメージに「合格」と表示されていても、実行される二つのイメージを確認したことにはなりません。

Tagは変えられる名前、digestは特定の内容を指す値です。複数platform向けのimage indexには、index自体のdigestと、実行先が選ぶmanifestのdigestがあります。どの値を受け入れたのか、実行先ではどのmanifestが選ばれるのかを追えないと、別の確認結果を取り違えます。

## 使用直前に問うこと

まず、実行されるmain、init、sidecar、ephemeral等の全artifactを、最終的な設定から列挙します。次に、それぞれのexact identityが利用者側の現在の受入条件を満たすか確かめます。署名の有無だけでなく、対象、builder、source、policy、期限など、受入判断に必要な条件を同じartifactへ結び付けます。

[Registry](../psb-container-002-container-registry-publication-boundary/learning.md)に公開済みでも、まだ使用許可ではありません。過去の受入結果を再利用するなら、別の環境や新しいdigestへ使い回せないこと、使用停止や期限切れを反映できることが必要です。確認先に接続できない場合を「以前は通ったから許可」とは扱いません。

## どこまで確かめたか

作成時だけでなく、更新、切り戻し、直接作成、補助コンテナー追加など、artifactが変わる経路も確認します。許可後に実際どの内容が稼働したかは別の観測です。[GOV-005の復旧判断](../../governance-operations/psb-gov-005-deployed-artifact-recovery/learning.md)では、新digestの公開、使用許可、稼働、旧digestの非稼働を別々に確認します。

採用先で試す項目は[controlの診断観点](README.md#failure-checks)、資料の採否は[Sources](../../../../sources/README.md#ref-deployment-artifact-admission-001)にあります。
