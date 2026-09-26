# PSB-DETECT-003 External attack surface reconciliationの移行

## 読者と判断

公開サービスの棚卸しと診断を担当する人が、外から得た候補をどの台帳・担当者へ結び、どこまで調査してよいか判断できるようにした。旧[PSB-DETECT-003](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/detection-verification/external-attack-surface-reconciliation)を[control](../controls/records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md)、[教材](../controls/records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/learning.md)、[pattern](../engineering/detection-verification/external-observation-and-inventory-reconciliation/README.md)へ再編集した。主な対象は段階11の外部公開で、観測結果を段階12の調査・対応へ渡す。

| 旧項目 | 新しい置き場 | 変更点 |
|---|---|---|
| `EASM-001` 所有起点 | `EASM-1/6` | ドメインに限らず採用した起点の責任・許可を確認。旧ID形式と期限の具体値は引き継がない |
| `EASM-002` CT・DNS・HTTPSの完全観測 | `EASM-2`とpattern | 対象に応じて収集元を選ぶ。CT・DNS・HTTPS全三者、各収集元の「完全」を一律要件にしない |
| `EASM-003` 観測の帰属と最小化 | `EASM-3/7` | 候補と出所、委託・共有基盤の区別を残す。IPなどの一律保存禁止はしない |
| `EASM-004` 第三者の共有基盤 | `EASM-3/6` | 自社の名前が指す先と、能動的に調べてよい対象を分ける |
| `EASM-005` 承認台帳 | `EASM-4` | 担当者・期待する公開・見直しを保持。台帳の`COMPLETE`申告だけでは健全性を保証しない |
| `EASM-006` 未知・期待外の公開 | `EASM-4` | 不一致を調査対象にする。脆弱性と自動確定しない |
| `EASM-007` 再出現 | `EASM-5` | 是正後の再観測と再出現を保持。名前だけのhashを唯一の資産identityにしない |
| `EASM-008` 能動的な確認 | `EASM-6` | 許可の境界を保持。DNSとHTTPS 443番だけという旧実装profileは普遍要件にしない |
| `EASM-009` fixtureと実環境 | `EASM-2/5`、移行記録 | 収集・台帳・通知の失敗を正常0件にしない。fixture成功とlive coverageを分ける |

## 具体化判断

旧実装はPythonの`scripts/verify.py`である。`policy.json`、`inventory.json`、`observations.json`、`state.json`を読み、範囲・鮮度・収集元の状態を検査したうえで、未登録、期待外の公開・サービス、委託先の変更、是正後の再出現を照合する。`PASS`／`FINDING`／`ERROR`の終了状態を分ける実際の照合ロジックがあり、単なるJSON形式検査ではない。旧packageの`secure/`・`insecure/`とテストは、用意した入力に対する分岐を確かめる。

一方、旧packageにはCT・DNS・HTTPSのcollectorは含まれず、所有の証明、委託先への確認、台帳の正しさ、通知、liveな再出現を観測しない。採用先が同じschemaの実データを生成すれば照合器として利用する余地はあるが、`status: COMPLETE`、`complete: true`、hash形式を検査できても、収集範囲が完全だった証拠にはならない。旧policyの三つの必須source、HTTPS 443番、固定鮮度と見直し日数、JSON schemaを新実装へそのままコピーしない。

このため、今回は実装例を作らず、[設計pattern](../engineering/detection-verification/external-observation-and-inventory-reconciliation/README.md#実装を作る開始条件)に実装開始条件を残した。対象の使い捨て環境、現実の収集元とAPI、責任を持つ台帳、調査許可、通知先が定まれば、正常な一致、未登録・期待外、部分取得・障害、是正後の再出現を観測できる限定実装を作る。診断観点はcontrolに記載し、試験実施済みとは扱わない。

## 参照とmapping

[NIST CSF 2.0](../sources/README.md#ref-external-surface-001)の資産・サービス台帳と[CISAのFederal向けBOD 23-01](../sources/README.md#ref-external-surface-001)にある資産発見と脆弱性列挙の区別を設計入力にした。BODの対象・周期を一般の組織へ適用していない。

旧ATT&CK v19.1 `T1590.001`、`T1590.002`、`T1596.003`の`detects / high`は継承しない。本controlが見つけるのは外部公開候補であり、攻撃者がそれらの偵察を行ったことを検出するわけではない。旧NIST SSDF 1.1 `RV.1.1`の`supports / medium`も、ソフトウェア脆弱性の識別・確認を直接扱わないため継承しない。旧関係は[旧control](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/detection-verification/external-attack-surface-reconciliation/control.yaml)に保持する。新しいframework mappingは追加しない。

実環境の収集範囲、第三者との契約、所有台帳、能動的確認の許可、担当者の判断、通知、閉鎖証拠は未確認である。
