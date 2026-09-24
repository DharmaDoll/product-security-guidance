# Impact is an evidence chain

[コントロール記録](README.md) · [設計パターン](../../../../engineering/governance-operations/incident-impact-and-response-planning/README.md)

## シナリオ

あるpackageの特定versionに問題が見つかった。分析基盤には製品Aの一致があるが、製品Bは表示されない。
Aは過去のbuildにだけ含まれ、Bは稼働中だが収集対象のproject権限から漏れていた。
「Aは侵害、Bは安全」と判断すると、対応対象を逆にする恐れがあります。

## 一致が意味すること

SBOMはcomponentの記録、artifact digestは成果物bytesの識別、deployment inventoryはある時点の稼働観測です。
この三つは代替できません。Component → SBOM → build → artifact → deploymentという対応を追い、各接続の根拠と観測時刻を確認します。
対応が確認できた製品は影響候補であり、侵害された証拠ではありません。

## 検索結果が空のとき

対象の全projectを閲覧できたか、全pageを取得したか、SBOMの処理が完了しているか、稼働環境の収集が新しいかを先に調べます。
確認できた範囲に一致がなければ「その範囲・時点では該当なし」。権限不足やtimeoutなら「調査不能」です。
Versionが一致しても実行されない開発専用componentと、install時に実行されたcomponentでは調べる資産が違います。

## 初動で決めること

担当者へ渡すのは、候補一覧だけでなく、欠落範囲、保全対象、対応選択肢、承認者です。
Artifact停止、credential失効、cache隔離、clean rebuildはそれぞれ別の権限・可用性影響を持ちます。
計画の生成は実施ではなく、再buildの成功も既存侵害の除去を証明しません。

判断を設計へ落とすには[pattern](../../../../engineering/governance-operations/incident-impact-and-response-planning/README.md)、
保証目標は[コントロール記録](README.md)、根拠と参照版は[Sources](../../../../sources/README.md#ref-supply-chain-impact-001)を参照してください。
