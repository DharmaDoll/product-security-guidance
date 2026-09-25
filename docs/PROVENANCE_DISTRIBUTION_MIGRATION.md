# PSB-REL-002 Provenance distribution 移行記録

## 結論

旧`PSB-REL-002`を[Provenance distribution and availability boundary](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)へ移行しました。Producerがprovenanceを生成した事実ではなく、intended consumerが取得したexact artifactから対応する一つ以上のprovenanceを発見・取得し続けられることを扱います。

旧成果物の一対一固定、public HTTPS、5分、365日は普遍要件として継承しません。SLSA v1.2のartifact-level binding、一artifactから複数attestationを扱える関係、publish時の同伴、複数配布場所、immutabilityを基に、scope、relation、publication completion、consumer access、immutability、retention、no downgradeの7特性へ再編集しました。

## 移行元

- Repository: `DharmaDoll/product-security-controls`
- Commit: `f42987759218c9b8daf3924320542a1935ef78e0`
- [旧README](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/provenance-publication-distribution/README.md)
- [旧control.yaml](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/provenance-publication-distribution/control.yaml)
- [旧verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/release-integrity/provenance-publication-distribution/scripts/verify.py)

## 旧5項目の扱い

| 旧項目 | 移行先 | 判断 |
|---|---|---|
| `RPD-001` 一artifact・一provenance | `PROV-DIST-1`・`2` | 変更して採用。Artifact digest bindingを保持し、一artifactから一つ以上のattestationへたどれる構造へ変更 |
| `RPD-002` immutable・authenticated・discoverable・accessible | `PROV-DIST-2`・`4`・`5` | 採用。Exact host、public、HTTPS、同一pathという旧fixture固有条件は方式へ移す |
| `RPD-003` 5分以内・365日保持 | `PROV-DIST-3`・`6` | 変更して採用。固定値を外し、release completionとartifactのconsumption・support・investigation windowへ結ぶ |
| `RPD-004` protected family no downgrade | `PROV-DIST-7` | 採用。Policy flagだけでなくartifact／relation inventoryとconsumer retrievalを確認する |
| `RPD-005` verification failureはERROR | `PROV-DIST-7` | 採用。Pagination、scope、stale observation、access、replica、parser等の失敗を分ける |

## 旧実装を移さない理由

旧`verify.py`はnetwork、release API、object storage、registry、TLS、consumer clientへ接続せず、fixture内の次のfieldを比較していました。

- `immutable: true`、`available: true`、`authentication: tls-server-authenticated`
- `access: public`と固定host・path
- Artifact・provenanceのsynthetic digestとtimestamp
- 5分、365日、protected familyのBoolean
- `publication_probe.source: release-api`という自己申告

これはmanifest schemaのtestにはなりますが、object上書き、consumer authorization、registry relation、replication、cache、garbage collection、retention、withdrawal、実取得を確認しません。また一artifactにつきprovenance digestを一つだけ許し、SLSAが推奨するartifactからattestationへの一対多を表せません。

対象ecosystemを選ばないままfield名を変えても同じ問題が残るため、Python verifier、secure／insecure JSON、expected output、固定値を移植しません。[Patternの開始条件](../engineering/release-integrity/provenance-distribution-and-availability/README.md#実装を作る開始条件)を満たす限定実装を今後作ります。

## Framework mapping

SLSA v1.2のproducer `Distribute provenance`は、producerがartifact consumerへprovenanceを配布し、対応できるpackage ecosystemへ委譲できる要件です。`PROV-DIST-1`〜`7`はその配布境界を具体化するため、旧`verifies / high`を`supports / medium / design-reviewed`へ変更します。SLSA Build L1以上の達成やproducer・platform・consumer全体の評価は主張しません。

NIST SSDF `PS.2.1`はsoftware acquirerがsoftware releaseのintegrityを検証できる情報を利用可能にするtaskです。Provenanceのartifact binding、consumer access、retentionは一つの実現方法なので、旧`supports / high`を`supports / medium / design-reviewed`へ変更します。SSDF全体への準拠、signature生成、acquirer側の実検証は別です。

## 完了範囲と残る作業

完了したものは、7特性のcontrol、複数artifactの具体的な教材、artifact digestからconsumer retrievalまでのpattern、診断観点、参照資料、2件のframework mapping、成果物mapping、横断分析です。

未実施なのは、registry／release service、artifact、attestation format、producer／consumer identity、retention policyの選定とlive upload・retrieval・deletion・downgrade確認です。実装時には正常公開だけでなく、artifact追加、複数attestation、部分公開、consumer access拒否、上書き、削除、stale index、probe failureを実serviceで確認します。
