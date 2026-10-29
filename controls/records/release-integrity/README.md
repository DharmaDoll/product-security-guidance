# Release Integrity

成果物の同一性、生成・配布した主体、利用者の期待値を、公開・取得・使用の境界で確認します。

| Control | 読者が判断すること | 教材 |
|---|---|---|
| [PSB-REL-001 Signature and provenance verification](psb-rel-001-signature-provenance-verification/README.md) | 正しい署名の成果物でも、自分たちの受入条件を満たすか | [正しい署名と使用許可の違い](psb-rel-001-signature-provenance-verification/learning.md) |
| [PSB-REL-002 Provenance distribution and availability](psb-rel-002-provenance-distribution-availability/README.md) | 利用者が手元の成果物に対応する来歴を探して取得でき、必要な期間中に失われないか | [来歴を置くだけでは足りない](psb-rel-002-provenance-distribution-availability/learning.md) |
| [PSB-REL-003 Release SBOM identity and analysis](psb-rel-003-release-sbom-identity-and-analysis/README.md) | どこで作ったSBOMか、何を含むかを確認し、公開した成果物・分析結果・稼働先へ辿れるか | [SBOMの取得地点を考える](psb-rel-003-release-sbom-identity-and-analysis/learning.md) |
| [PSB-REL-004 Supplier SBOM intake trust](psb-rel-004-supplier-sbom-intake-trust/README.md) | 供給者のSBOMを期待する製品・成果物・出所へ照合し、通常台帳への受入れを判断できるか | [別製品のSBOMを受け入れない](psb-rel-004-supplier-sbom-intake-trust/learning.md) |
| [PSB-REL-005 Artifact signing generation](psb-rel-005-artifact-signing-generation/README.md) | 承認した成果物へ限定した権限で署名し、利用者が検証材料を取得できるまでreleaseを止められるか | [署名した対象を確認する](psb-rel-005-artifact-signing-generation/learning.md) |

## 工程をつなげて読む

- [ビルドした成果物を署名・公開し、使用するまで](../../../engineering/release-build-to-use.md)：承認した作り方、今回のdigest、署名対象、公開完了、利用者の判断をつなぎます。
- [SBOMから脆弱性の影響調査へ](../../../engineering/sbom-to-vulnerability-response.md)：取得地点、供給者からの受入れ、最終成果物、分析、稼働先をつなぎます。

個別の方式は各Control、シナリオと判断例は各教材を正本とします。

REL-001・002・004・005は文書と診断項目を今回の成果物とし、実環境での署名・公開・取得・受入拒否は未確認です。Release SBOMの限定実装は、実ファイルと記載されたhashの一致などを確認します。生成ツールの収集範囲、実環境での公開・分析・稼働先との対応は未確認です。
