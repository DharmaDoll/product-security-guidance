# PSB-IAC-001 Infrastructure change authorization and drift

**承認したインフラ変更と、実際に適用されて今ある状態は一致しているか。**

## なぜ必要か

例えば、レビューしたplanとは別のplanをapplyすれば、承認していないresourceが作られます。CIを通さずconsoleで変更されたresourceも、planの合格だけでは見つかりません。

## 満たすべきこと

1. **変更の入力を特定する。** Source、module、provider、variable、policy、tool、workspace、targetを一つの変更として記録する（IAC-CHANGE-1）。守る資産に応じたruleを、sourceの文字列だけでなく、解決済みplanの作成・更新・削除と重要な値へ適用する（IAC-CHANGE-2）。
2. **判断できない変更を通さない。** 許可、拒否、人による判断、評価失敗、未対応resource、apply時まで不明な値を分ける。安全性に必要な値が不明ならapply前に止めるか、別の強制点へ渡す（IAC-CHANGE-3）。
3. **承認したplanだけを実行する。** レビューとpolicy判断を保存した実行可能plan・入力・targetへ結び付け、applyで作り直さない。Planには機微値が含まれ得るため保護する（IAC-CHANGE-4）。Apply権限はplan作成から分け、対象と操作を限定する（IAC-CHANGE-5）。
4. **別経路と現在状態を確認する。** Console、API、別tool等の変更経路を列挙し、拒否または独立した観測へつなぐ（IAC-CHANGE-6）。Apply途中失敗を「変更なし」と扱わず、provider上の実resourceと未管理resourceも確認する（IAC-CHANGE-7）。
5. **逸脱を新しい判断へ戻す。** 例外とdriftの対象・owner・期限・影響を記録し、修正は新しいplanとしてレビューする。自動修正は影響・復旧・証跡保全を確認できる範囲に限る（IAC-CHANGE-8）。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- レビュー後にmodule、provider、variable、policy、targetを変えても、古い承認でapplyできないか。
- 表示用planだけをレビューし、apply時に別のplanを作り直していないか。保存planを別targetへ使えないか。
- Unknown値、未対応resource、policy engine障害を「違反なし」としていないか。
- Plan生成jobがapply権限を持つ、またはconsole・API・別toolから禁止状態を作れるままではないか。
- Applyが途中失敗した後の変更や、IaC管理外のresourceを見落とさないか。Provider APIの取得失敗をdriftなしにしていないか。
- 自動修正が影響確認や承認なしにresource削除・network遮断・認証情報変更を行わないか。

これらは診断・設計レビューの確認項目であり、実cloudでの拒否やdrift確認の結果ではありません。

## フレームワークとの関係

レビューしたplan、実際に適用するplan、変更後の実環境を結ぶ問いについて、現行の[フレームワーク・マッピング](../../../../mappings/frameworks.yaml)に個別の関係は登録していません。Terraform等の仕様は具体的な設計入力ですが、planの合格を規格への準拠や実環境の一致とみなしません。

## このコントロールの範囲

対象はIaCのsourceからplan、承認、apply、provider上の現在状態までです。個々のresourceに必要な安全な値は、資産とproviderに応じて別に定めます。CI identityの交換条件は[CICD-006](../../cicd-security/psb-cicd-006-workload-federation-boundary/README.md)、workloadの最終的な許可は[CONTAINER-001](../psb-container-001-deployment-artifact-admission/README.md)や[CONTAINER-005](../psb-container-005-workload-privilege-confinement/README.md)へ渡します。Planの合格だけで実resourceの安全性は示せません。

保存plan、apply権限、provider側の拒否とdrift観測の置き方は[engineering](../../../../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)で選びます。対象providerとresourceを決めるまで合成的な実装例は追加しません。[教材](learning.md)、特性IDを残した[control.yaml](control.yaml)、[参照資料](../../../../sources/README.md#ref-iac-change-boundary-001)、[移行記録](../../../../docs/MIGRATION_CONTAINER_CLOUD_IAC.md#iac-change-boundary-migration)へも辿れます。
