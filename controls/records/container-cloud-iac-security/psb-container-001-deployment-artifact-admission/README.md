# PSB-CONTAINER-001: Deployment artifact admission

## 問い

実行しようとしている全artifactのexact identityを、consumerが現在受け入れているevidenceへ結び付け、評価不能や未対象の経路を許可へ変えずに使用直前で拒否できるか。

## できてはいけないこと

Mutable tag、別artifact用の署名やprovenance、過去のpass表示、deployerが付けた`verified: true`を根拠にworkloadを実行してはいけません。
Admission evaluator、registry、evidence service、policyの取得に失敗したときや、init・sidecar等の一部artifactを列挙できないときに、通常のallowへfallbackしてはいけません。

## 適用範囲と非適用

Deployment request、そこから実行される全artifactのidentity、[consumer artifact acceptance](../../release-integrity/psb-rel-001-signature-provenance-verification/README.md)の現在の判断、最終的な実行許可、強制点のcoverageと障害時の状態が対象です。

Registryのpublish権限・immutability・retentionは旧`PSB-CONTAINER-002`、non-root・capability・host接続・filesystem・resource・network等のworkload confinementは別主題、host／runtimeの防御と実行後の観測は`PSB-CONTAINER-003`・[PSB-CONTAINER-004](../psb-container-004-runtime-threat-detection/README.md)の責任です。

## 必要なセキュリティ特性

| ID | 成立すべき状態 |
|---|---|
| `ARTIFACT-ADMIT-1` | Main、init、sidecar、ephemeral等、対象workloadが実行し得る全artifactをrepository／package identityと暗号学的digestで列挙し、tagや表示名だけで許可しない |
| `ARTIFACT-ADMIT-2` | Consumer-owned policyが署名・provenance・builder・source・build parameter等の必要な期待値を評価した結果を、実行するexact digestと対象環境へ結び付ける |
| `ARTIFACT-ADMIT-3` | Admission requestからruntimeへ渡る最終状態を評価し、mutation後の差替え、別artifact用decisionの再利用、評価後のtag解決変更を許さない |
| `ARTIFACT-ADMIT-4` | Workloadの作成・更新・rollback・controller経由・直接作成・関連subresource等、artifactを実行または変更できる全経路をinventory化し、同じ強制点か同等の境界を通す |
| `ARTIFACT-ADMIT-5` | Artifact、evidence、policy、evaluatorの欠落・不一致・期限切れ・取得不能・timeout・parse errorを`DENY`または`ERROR`として通常の実行を止め、`ALLOW`と区別する |
| `ARTIFACT-ADMIT-6` | Allow decisionへartifact set、target、policy version、trust profile、decision identity、評価時刻を結び付け、policy変更・失効・再評価と、機微情報を含まないauditを管理する |

## 実装判断の羅針盤

使用境界では、producerの自己申告を再評価しません。`PSB-REL-001`相当のconsumer verifierを直接実行するか、同じconsumer policy serviceが発行した認証済みdecision receiptを検証します。
Receiptを使う場合は、exact digest、target、policy／trust profile、期限を結び、deployerが複製・改変できないことが必要です。

Kubernetesでは、request内だけで完結するfield検査はcontrol plane内のCEL等で処理でき、registryやprovenance serviceへの外部照会はvalidating webhook等が必要になります。
方式名で安全性を判断せず、最終的に実行されるPod state、全API経路、障害時の動作、policy変更権限を確認します。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

採用先では、次の操作や異常があってもdeploymentを許可しないことを確認します。ここにあるのは確認項目であり、
本PJが実際のclusterやdeployment platformで試した結果ではありません。

- Tagだけの参照、digestと取得bytesの不一致、同名の別registry／repositoryを拒否できるか
- 正しい署名・provenanceを別digest、別repository、別targetへ流用できないか
- 失効したidentity、古いpolicy、期限切れreceipt、変更後のtrust profileを許可しないか
- Main imageだけを評価し、init、sidecar、ephemeral、debug、hook等のartifactを見落とさないか
- CREATE後のUPDATE、rollback、controller生成、直接Pod作成、subresource、別API versionで迂回できないか
- Mutating処理が検証後にartifactを差し替えず、validationが最終状態へ適用されるか
- Evaluator、registry、evidence store、DNS、TLS、policy取得のtimeout・部分失敗がallowにならないか
- 除外namespace、selector、break-glassが未承認・期限切れ・対象外へ広がらないか
- Admission policyやwebhook設定を変更できる主体が、artifactをdeployする主体と同じ権限で無効化できないか

## 保証しない範囲

許可したartifactが脆弱性や悪意を含まないこと、workload設定が安全であること、runtimeで同じbytesが必ず実行されたことは、このcontrolだけでは保証しません。
Admission後のnode pull、cache、runtime inventory、driftは別に観測し、allow decisionと実際のdigestを照合する必要があります。

今回はdeployment platformとconsumer verifierの接続方式を選んでいないため、Kubernetes policy、webhook、CLI、cluster testは追加していません。
旧offline JSON verifierはlive API path、mutation order、registry取得、policy availability、runtime digestを証明しないため移植していません。

- [Deployment artifact admission boundary pattern](../../../../engineering/container-cloud-iac-security/deployment-artifact-admission-boundary/README.md)
- [参照資料と採否](../../../../sources/README.md#ref-deployment-artifact-admission-001)
- [Framework mapping](../../../../mappings/frameworks.yaml)
- [移行記録](../../../../docs/DEPLOYMENT_ARTIFACT_ADMISSION_MIGRATION.md)
