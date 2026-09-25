# PSB-IAC-001 Infrastructure change boundary 移行記録

## 結論

旧`PSB-IAC-001 Secure IaC Golden Path`は、標準moduleやCI templateを配る考え方と、plan・apply・provider状態を強制する境界を一つにしていました。移行後は`PSB-IAC-001 Infrastructure change authorization and drift boundary`として、reviewしたsource・依存、resolved plan、policy判断、apply authority、provider上の現在状態を同じ変更として結ぶ8特性へ再編集しました。

Golden Pathは捨てず、[設計pattern](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)の「安全な変更を作りやすくする入口」として位置付けます。標準moduleの利用を、resource固有要件への合格や実環境の安全性と同一視しません。

## 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/control.yaml)
- [ユーザー提供原文](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/container-cloud-iac-security/secure-iac-golden-path/docs/user-supplied-golden-path-guideline-ja.md)

## 旧12項目の扱い

| 旧項目 | 移行先 | 判断 |
|---|---|---|
| `IAC-001` module version／integrity | `IAC-CHANGE-1` | 採用。ただしTerraform provider lockとremote module versionを分け、存在しない共通`sha256` contractを要求しない |
| `IAC-002` multi-cloud compute defaults | `IAC-CHANGE-2`とpattern | 変更して採用。暗号化、network、image等はresource・provider固有controlの入力。AWS／GCP／Azureを一つのfixtureで通すことを要件にしない |
| `IAC-003` private administration／IAM | `IAC-CHANGE-2`と隣接control | 変更して採用。Infrastructure変更経路と、作成するresourceの管理面要件を分ける |
| `IAC-004` resolved plan gate | `IAC-CHANGE-2` | 採用。Source textやmodule名ではなくcreate／update／delete／replaceと値を評価する |
| `IAC-005` fail closed | `IAC-CHANGE-3` | 採用。Unknown、unsupported、error、対象漏れ、人の判断を別状態にする |
| `IAC-006` reusable CI composition | 非継承 | Secret、SCA、SBOM、署名、container scan等をIaC controlの必須一覧に複製していた。各controlとCI patternの責任へ戻す |
| `IAC-007` deploy identity | `IAC-CHANGE-5`とPSB-CICD-006 | 境界だけ採用。OIDC claim、token発行・交換はCICD-006、targetとapply操作の限定はIAC-001が扱う。固定15分を普遍値にしない |
| `IAC-008` provider enforcement | `IAC-CHANGE-6` | 採用。特定hookのcreate／update対応を`all-provisioning-paths`と自己申告する方式は廃止 |
| `IAC-009` runtime drift | `IAC-CHANGE-7` | 採用。固定24時間を外し、provider inventory、実resource、collection health、未管理resourceまで判断する |
| `IAC-010` automatic remediation | `IAC-CHANGE-8` | 採用。安全なaction名の自己申告ではなく、新しいplan、impact、rollback、証拠保全を求める |
| `IAC-011` exceptions | `IAC-CHANGE-8` | 採用。Resource・rule・owner・理由・期限・影響を結ぶ |
| `IAC-012` plan artifact | `IAC-CHANGE-4` | 採用。Hashとretentionだけでなく、review・targetとの結合、read／write、機微値、差替え、廃棄を扱う |

## 旧実装を移さない理由

旧`verify.py`はTerraform、OPA、cloud providerを実行せず、用意した`golden-path-policy.json`と`tfplan.json`のfieldを比較していました。例えば次の内容は、実システムを観測した結果ではなくfixture内の自己申告でした。

- `providers`がAWS／GCP／Azureの三つである。
- `coverage`が`all-provisioning-paths`である。
- Driftを24時間以内に検査した。
- OIDC、provider policy、例外、remediation、plan artifactが期待文字列を持つ。
- Reusable workflowが他controlを`implemented`として列挙する。

これはpolicy metadataのschema testにはできますが、module解決、provider lock、実planのunknown、plan差替え、apply authority、provider側の拒否、actual state、driftを証明しません。`secure` fixtureが12項目を通ることを「実装」と読める構成だったため、script、secure／insecure JSON、固定値、旧Make targetを移植しません。

TerraformとOPAを使うだけのdemoも今回は作りません。Providerとresourceを選ばないplanでは、security invariantとapply後の実効値を確認できず、旧fixtureの表現を変えるだけになるためです。[Patternの開始条件](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md#実装を作る開始条件)を満たす限定実装を今後作ります。

## 参照資料の扱い

2026-07-28のユーザー提供guidanceは正式な組織policyや外部標準ではありません。新しい主題別の参照記録`REF-IAC-CHANGE-BOUNDARY-001`で、Golden Path、resolved plan policy、provider hook、driftという論点の出発点として保持します。

外部資料へのリンクやmulti-cloudの例は、提供文書に記載された事実として扱い、個々の製品挙動を確認済みとはしません。今回、HashiCorp Terraformのplan、dependency lock、refresh-onlyとOPAのTerraform plan limitationを公式文書で2026-09-25に再確認しました。

## 旧framework mapping

旧5関係は移行後の特性へ継承しません。

| 旧関係 | 判断 |
|---|---|
| OpenSSF OSPS `OSPS-QA-03.01` | Primary branchのautomated status checkをpassまたはmanual bypassする要件。Planとapplyの同一性、provider状態は規定しない |
| OpenSSF OSPS `OSPS-QA-04.02` | 複数source repositoryからなるreleaseで同等以上のsecurity requirementを求める要件。IaC resource変更の境界ではない |
| OpenSSF OSPS `OSPS-AC-04.01` | 旧registry titleはCI/CD least privilegeだが、2026.02.19版の詳細関係はCI control側で扱う。Apply targetとplan bindingへの直接要件として重複追加しない |
| NIST SSDF `PW.6.1` | 実行形式の安全性を改善するbuild toolの利用を扱う。Infrastructure plan・apply・driftへの直接要件ではない |
| GitHub Secure use reference `GHSC-SECURE-BUILDS` | Product guidanceとしてCI設計の入力にはなるが、IaC controlのframework requirementではない |

OpenSSF、SSDF、GitHub資料を否定する判断ではありません。意味が一致する別controlで管理し、旧件数を維持するための間接mappingを作らない判断です。

## 完了範囲と残る作業

完了したものは、8特性のcontrol、具体的な失敗から始まる教材、sourceからactual stateまでのpattern、診断観点、参照資料記録、成果物mapping、横断分析です。

未実施なのは、実IaC tool、provider、resource、policy engine、cloud sandbox、identity、plan store、provider guardrail、drift collector、remediationの選定と実行です。実装例を追加する時は、正常系だけでなくplan差替え、unknown／error、別経路の変更、drift、収集失敗、cleanupを実cloud状態で確認します。
