# Release Integrity

成果物の同一性、生成・配布した主体、利用者の期待値を、公開・取得・使用の境界で確認します。

| Control | 読者が判断すること |
|---|---|
| [PSB-REL-001 Signature and provenance verification](psb-rel-001-signature-provenance-verification/README.md) | 正しい署名の成果物でも、自分たちの受入条件を満たすか |
| [PSB-REL-002 Provenance distribution and availability](psb-rel-002-provenance-distribution-availability/README.md) | Exact artifactから対応するprovenanceを発見・取得でき、利用期間中に欠落や上書きへdowngradeしないか |
| [PSB-REL-003 Release SBOM identity and analysis](psb-rel-003-release-sbom-identity-and-analysis/README.md) | Final artifact向けSBOMのidentity・coverage・公開・analysis処理・deployment relationを区別できるか |
| [PSB-REL-004 Supplier SBOM intake trust](psb-rel-004-supplier-sbom-intake-trust/README.md) | 供給者のSBOMを期待する製品・成果物・出所へ照合し、通常台帳への受入れを判断できるか |
| [PSB-REL-005 Artifact signing generation](psb-rel-005-artifact-signing-generation/README.md) | 承認した成果物へ限定した権限で署名し、利用者が検証材料を取得できるまでreleaseを止められるか |

署名生成は設計まで移行し、signer・artifact形式・公開先が未選定のため具体実装とlive署名は未確認です。Supplier SBOMは供給者・署名方式・信頼根拠・取込先を選ぶ前提がないため具体実装とlive受入れは未確認です。Provenance distributionは対象ecosystem未選定のためlive配布実装がありません。Release SBOMはCycloneDX artifact bindingだけを限定実装し、generator coverage、live公開・analysis・deployment catalogは未確認です。
