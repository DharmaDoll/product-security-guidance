# Release Integrity

成果物の同一性、生成・配布した主体、利用者の期待値を、公開・取得・使用の境界で確認します。

| Control | 読者が判断すること | 教材 | 設計pattern |
|---|---|---|---|
| [PSB-REL-001 Signature and provenance verification](psb-rel-001-signature-provenance-verification/README.md) | 正しい署名の成果物でも、自分たちの受入条件を満たすか | [正しい署名と使用許可の違い](psb-rel-001-signature-provenance-verification/learning.md) | [Consumer artifact acceptance](../../../engineering/release-integrity/consumer-artifact-acceptance/README.md) |
| [PSB-REL-002 Provenance distribution and availability](psb-rel-002-provenance-distribution-availability/README.md) | 利用者が手元の成果物に対応する来歴を探して取得でき、必要な期間中に失われないか | [来歴を置くだけでは足りない](psb-rel-002-provenance-distribution-availability/learning.md) | [Provenance distribution and availability](../../../engineering/release-integrity/provenance-distribution-and-availability/README.md) |
| [PSB-REL-003 Release SBOM identity and analysis](psb-rel-003-release-sbom-identity-and-analysis/README.md) | どこで作ったSBOMか、何を含むかを確認し、公開した成果物・分析結果・稼働先へ辿れるか | [SBOMの取得地点を考える](psb-rel-003-release-sbom-identity-and-analysis/learning.md) | [Release SBOM identity and analysis](../../../engineering/release-integrity/release-sbom-identity-and-analysis/README.md) |
| [PSB-REL-004 Supplier SBOM intake trust](psb-rel-004-supplier-sbom-intake-trust/README.md) | 供給者のSBOMを期待する製品・成果物・出所へ照合し、通常台帳への受入れを判断できるか | [別製品のSBOMを受け入れない](psb-rel-004-supplier-sbom-intake-trust/learning.md) | [Supplier SBOM intake boundary](../../../engineering/release-integrity/supplier-sbom-intake-boundary/README.md) |
| [PSB-REL-005 Artifact signing generation](psb-rel-005-artifact-signing-generation/README.md) | 承認した成果物へ限定した権限で署名し、利用者が検証材料を取得できるまでreleaseを止められるか | [署名した対象を確認する](psb-rel-005-artifact-signing-generation/learning.md) | [Artifact signing boundary](../../../engineering/release-integrity/artifact-signing-boundary/README.md) |

## CI/CDから受け取り、利用者へ渡すもの

[CICD-005](../cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md)はPR由来の状態を権限処理へ持ち込まない境界、[CICD-004](../cicd-security/psb-cicd-004-workflow-authority-minimization/README.md)と[CICD-006](../cicd-security/psb-cicd-006-workload-federation-boundary/README.md)はjobと交換先の権限を絞る境界です。CIの検査成功や権限取得だけでは、公開する成果物のbytesと承認内容は決まりません。[BUILD-002](../build-security/psb-build-002-approved-consistent-build/README.md)で正規のbuildを定め、来歴を要求する場合は[BUILD-003](../build-security/psb-build-003-platform-provenance-generation/README.md)から完成した成果物のdigestに結び付く生成結果を受け取ります。

完成した成果物のdigestを起点に、必要な署名と検証材料はREL-005、必要な来歴の発見・取得はREL-002、release SBOMの取得地点と対象の結合はREL-003で確認します。どれか一つの成功をリリース全体の完了へ置き換えません。供給者から受け取るSBOMはREL-004で別に受け入れます。公開側の完了後も、利用者はREL-001で自分たちの期待値と使用するbytesを照合します。

Container imageを使う場合は、[registryの公開・保持](../container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/README.md)と[deployment時の使用許可](../container-cloud-iac-security/psb-container-001-deployment-artifact-admission/README.md)を分けます。許可された後に何が実際に稼働したかは別に観測し、問題のある旧digestの非稼働確認は[GOV-005](../governance-operations/psb-gov-005-deployed-artifact-recovery/README.md)へ渡します。

成果物への署名と来歴情報への署名は対象が異なります。各controlの教材から具体的な攻撃経路を読み、必要な箇所だけ設計patternへ進めます。

REL-001・002・004・005は文書と診断項目を今回の成果物とし、実環境での署名・公開・取得・受入拒否は未確認です。Release SBOMの限定実装は、実ファイルと記載されたhashの一致などを確認します。生成ツールの収集範囲、実環境での公開・分析・稼働先との対応は未確認です。
