# Release Integrity

成果物の同一性、生成・配布した主体、利用者の期待値を、公開・取得・使用の境界で確認します。

| Control | 読者が判断すること |
|---|---|
| [PSB-REL-001 Signature and provenance verification](psb-rel-001-signature-provenance-verification/README.md) | 正しい署名の成果物でも、自分たちの受入条件を満たすか |
| [PSB-REL-002 Provenance distribution and availability](psb-rel-002-provenance-distribution-availability/README.md) | Exact artifactから対応するprovenanceを発見・取得でき、利用期間中に欠落や上書きへdowngradeしないか |

SBOM、供給者SBOM、署名生成は未移行です。Provenance distributionは対象ecosystem未選定のためcontrol・教材・patternまでを移行し、live配布実装はありません。
