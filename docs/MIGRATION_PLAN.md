# 進め方と移行計画

## 移行の方針

本PJを執筆・移行作業の正本とし、旧product-security-controlsから必要な知識を主題ごとに選別・再編集します。
旧パッケージを保つための空ディレクトリや転送READMEは作りません。独立化の範囲は[Repository cutover](REPOSITORY_CUTOVER.md)に記録しています。

主な成果は、何をすべきか、本質をどこで強制すべきか、何を保証しないかを読者が判断できる知識基盤です。
実装、テスト、導入証拠は、この判断を具体化できる場合だけ別の成果物として作ります。

## 現在地と次の作業

2026-09-26更新。この節を現在地と次作業の正本とし、候補一覧は棚卸し、構造レビューと移行台帳は経緯・判断の記録として使います。

| 状態 | 内容 |
|---|---|
| 現在地 | 41件のcontrol記録・40件の設計パターン。Framework mappingは116件 |
| 直近の成果 | [旧AI-005〜009の範囲を選別](AI_DEVELOPMENT_SCOPE_REVIEW.md)。AI-006はAI-004へ接続し、AI-007を開発agentの作業単位の予算として次の独立候補に選んだ。製品AIの設計・TEVVはai-security-foundryへ委ねる |
| 次の主題 | 旧`PSB-AI-007`から、開発agentの作業単位の上限と新しいmodel・tool呼出しの停止を再編集する。AI-004の操作認可、CI runnerとworkloadの資源上限との境界を確かめる |
| 次回に残す判断 | AI-001のGitHub例は保護branch・レビュー担当・bypassの採用先が未定で、実拒否は未確認。開発agentの効果比較も未実施。AI-003の製品別実装はagent・版・toolの強制点・使い捨て対象を選んだ時に再開する。AI-005・008・009は採用する開発agentの保存・委譲・停止経路が決まるまで保留する。SOURCE-003の実GitHub検索、精査、Webhook受領、対応運用は未確認。DETECT-003の公開サービス台帳照合は、対象環境・収集元とAPI・正本台帳・許可範囲・通知先を選べた時に限定実装へ戻る。CODE-005のreview UIとprotected CI、採用先のpathと例外は未確認。BUILD-002はplatform・provenance形式・publish gateを選べた時に限定実装へ戻る。REL-005はartifact形式・signer・承認の強制点・公開先・consumer条件を選べた時に限定実装へ戻る。REL-004は実供給者・方式・信頼根拠・使い捨て取込先が揃った時に限定実装へ戻る。REL-003のlive storage・Dependency-Track・deployment catalogは未実施。SOURCE-004のASI03は公式PDF本文を取得できた時点で再照合する |
| Secure Codingに残る作業 | ASVS 5.0.0を共通要件の参照先とする方針を記録済み。個別の要件対応は対象主題ごとに確認する。利用者の経験由来の診断チェックリストは後日受領予定で、原本と公開可否の確認前に項目・ASVS対応を作らない |
| SOURCE-002に残る作業 | 実環境への配布・有効化、全書込経路の接続、負荷評価、例外承認、他OS・SaaS構成は未実施。代表実装の完了と組織導入を区別する |
| 継続する未確認事項 | 全旧実装の意味的レビュー、参照仕様の現行性、読みやすさとcontrol・pattern間navigationの継続レビュー、実環境の導入・強制 |

各主題は、読者が問い・直接の失敗・適用範囲・セキュリティ特性・隣接境界を判断でき、
参照資料と旧項目との関係を追跡できるところまで整理します。文書の完成に加え、
[主題ごとの具体化判断](ARTIFACT_MODEL.md#主題ごとの具体化判断)で選んだ成果物を完了条件に含めます。
必要な具体実装が残る主題は、文書作成済み・実装未完了として記録します。実環境への導入・診断は別に扱います。
[診断で確認する項目](CONTENT_QUALITY.md#failure-checks)は、チェックリストだけでも成立し、実際に試した結果とは区別します。

Git hooksの主題は利用者の指定により先に整理し、代表実装まで追加しました。SOURCE-004は8件中7件の追加照合も完了し、
OWASP ASI03だけを資料取得待ちとして残しました。
その後の主題は、次回のレビュー結果、読者の需要、実装予定、攻撃経路の受け渡しの欠落から選びます。
一つのdomainを全件移してから次へ進む方式や、旧52件を一対一で移す方式にはしません。
候補は[三領域の棚卸し](MIGRATION_CANDIDATES.md)と[残る八domainの棚卸し](PORTFOLIO_MIGRATION_REVIEW.md)に保持します。

## 旧AI-005〜009の具体化判断

2026-09-26、[範囲と旧項目の行き先](AI_DEVELOPMENT_SCOPE_REVIEW.md)を確認しました。旧5件を件数どおりに移すのではなく、AI-006の開発agent操作は既存AI-004へ接続します。AI-007には作業全体の呼出し回数・時間・費用と、上限前の停止という独立した問題が残ります。まず開発agentに絞ったcontrol・教材・設計pattern・診断観点を検討します。実装例は採用するagent、利用量の取得元、実行前強制点、使い捨て対象を選べた時に判断します。AI-005・008・009はそれぞれ持続的context、agent間委譲、長時間・自律実行の採用条件が確定するまで保留します。製品AIの機能をこの移行へ戻しません。

## AI-001の具体化判断

2026-09-26、旧[AI-001](REPOSITORY_AGENT_GUIDANCE_MIGRATION.md)を開発agentが実際に読むrepository指示の変更レビューと、開発作業への効果比較へ選別しました。[Control](../controls/records/ai-development-security/psb-ai-001-repository-agent-guidance/README.md)、教材、[設計pattern](../engineering/ai-development-security/repository-agent-guidance-review/README.md)、診断観点を必要な成果物としました。GitHubでの受入れ経路は技術的に具体化できるため、[CODEOWNERS・branch保護の例](../engineering/ai-development-security/repository-agent-guidance-review/implementations/github-codeowners/README.md)に変更箇所、使い捨てrepositoryでの確認方法、解除方法を示しました。

例の設定には実在するレビュー担当者と保護branchが必要です。本PJはGitHub上のルール設定や拒否をまだ観測しておらず、導入・実効性の完了とはしません。比較評価の実装もagent・版・課題・実行権限・独立した採点元が定まるまで保留します。旧合成JSONの62.50%→93.75%や固定閾値は採用しません。この主題は開発環境だけを扱い、製品のAI機能の設計やTEVVを含めません。Framework mappingは旧関係を継承せず、116件のままです。

## AI-003の具体化判断

2026-09-26、[旧AI-003](DEVELOPMENT_CONTENT_INJECTION_MIGRATION.md)を開発agentが読む未信頼資料の主題へ絞りました。読者は、Issue・文書・tool出力の出所と指示権限を区別し、agentの提案から実行までの強制点を選ぶ必要があります。このため[control](../controls/records/ai-development-security/psb-ai-003-development-content-injection-boundary/README.md)、control配下の教材、[設計pattern](../engineering/ai-development-security/untrusted-development-content-boundary/README.md)、診断観点を必要な成果物とし、本文と旧項目の対応まで完了しました。Framework mappingは旧`verifies`関係を継承せず、116件のままです。

実装例は採用するagent・版、入力取得元、toolの実行前強制点、保護対象、使い捨て環境を選べば限定して作れます。現時点ではこれらが未指定で、旧verifierも合成JSONの自己申告を検査するだけなので保留します。実装再開時の完了条件は、無害なcanaryで元の作業の成功、不要操作の拒否、取得・判定障害を実際に観測し、解除方法と未対応経路を示すことです。診断項目を記載したことを試験済みとしません。

## Secure Codingの進め方

Web application／web serviceに共通するSecure Codingの要件観点は、固定した[OWASP ASVS 5.0.0](../sources/README.md#spec-owasp-asvs-5-0-0)を参照先とします。旧計画の`PSB-CODE-001〜004`（アプリケーションsecret、認証・session、認可、injection）は、番号や計画があることだけを理由に独自controlへ一対一で移行しません。対象製品に適用する要件を選ぶ際は、ASVSの版・exact要件ID・原文・適用条件を確認します。ASVSのlevel達成や領域全体のcoverageは、この索引やmappingから推定しません。

利用者は経験由来の独自の脆弱性診断チェックリストを後日提供する予定です。これはASVSを置き換える資料でも、ASVSから復元する資料でもありません。受領時には次の順で扱います。

1. 題名、作成者または管理者、版・更新日、項目IDと原文、適用対象、公開可能な範囲を確認する。非公開項目や実案件の証拠を公開repositoryへ転記しない。旧`REF-USER-004`と同じ資料かどうかも、この時点で確認する。
2. 原文と由来を保持したまま、各項目が何を診断するかを整理する。ASVS 5.0.0のexact要件と重なる、補足する、ASVSの対象外、判断保留のどれかを理由付きで記録する。重ならない実務観点も捨てず、ASVSの語彙へ無理に言い換えない。
3. 読者の判断に役立つシナリオ・診断観点は関連する教材やcontrolへ結び付ける。独立control・pattern・実装例は、固有の失敗経路と強制点を説明でき、実装判断に価値がある場合だけ作る。チェックリスト項目をテストコードへ一律に変換しない。

原本はまだ受領していません。項目、適用範囲、ASVSとの対応、公開可能性は未確認です。[Secure Codingの入口](../controls/records/secure-coding/README.md)には、この状態を明示します。

## SOURCE-003の限定実装

2026-09-26、利用者が公開GitHubのコード・Issue・PRを対象に、少数の自社ドメイン名・メールアドレスから候補を探す経路を選んだため、[GitHub indicator watch](../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)を具体実装として追加した。完了条件は、使い捨てのHTTP環境で候補発見、人の精査前の非通知、同じ候補の重複抑制、Webhookへの一度の通知、不完全結果と壊れたstateの失敗を観測すること。旧1300行超のPoCをコピーせず、第一ページの少数クエリ、ローカルstate、人が選んだ候補だけの通知に絞る。

この実装はSOURCE-003の公開ソース情報の観測を具体化し、DETECT-003の公開サービス・台帳照合は実装しない。実GitHub検索、組織の認証情報と指標、通知先、精査と対応運用は未確認。詳細は[実装README](../engineering/source-protection/public-exposure-observation-and-triage/implementations/github-indicator-watch/README.md)と[旧PoCの扱い](PUBLIC_EXPOSURE_MIGRATION.md)を参照してください。

## DETECT-003の具体化判断

2026-09-26に旧`PSB-DETECT-003`を[External attack surface reconciliation](../controls/records/detection-verification/psb-detect-003-external-attack-surface-reconciliation/README.md)へ移した。外部公開候補の所有・台帳照合・再出現・収集障害・調査許可は、control、教材、pattern、診断観点として整理した。旧Python verifierには実際の台帳照合・再出現判定があるが、旧packageにはCT・DNS・HTTPSのcollectorがなく、台帳の正しさも観測しない。限定profileをそのまま移植せず、CT・DNS・HTTPSを全対象に必須とはしない。HTTPS 443番や固定期限も製品非依存の要件にしない。

実装例の開始条件は、使い捨てまたは明示的に許可された対象、採用する収集元とAPI、正本台帳、能動的確認の許可範囲、通知先を決めること。正常な一致、未登録・期待外、収集の部分取得・失敗、再出現を実際に観測できる形にする。旧ATT&CKの`detects`とSSDF `RV.1.1`は直接性が不足するため非継承とした。詳細は[移行記録](EXTERNAL_ATTACK_SURFACE_MIGRATION.md)を参照してください。

## CODE-005の具体化判断

2026-09-26に旧`PSB-CODE-005`を[Unicode source review](../controls/records/secure-coding/psb-code-005-unicode-source-review/README.md)へ移しました。文字と識別子を実ソースから読めるため、control、教材、pattern、診断観点に加え[Python 3.10限定scanner](../engineering/secure-coding/unicode-source-review/implementations/python/README.md)を必要な成果物としました。導入・smoke test・解除、正常・検出・評価不能の観測を含みます。

旧ASCII識別子と文字拒否リストはPython向けの狭いprofileとして保持し、全言語の普遍要件にしません。UTS #55／#39に照らし、多言語テキストと表示支援を設計上の選択肢として残します。Protected CI、レビュー画面、採用先path・例外、別言語の実装は未確認です。詳細は[移行記録](UNICODE_SOURCE_MIGRATION.md)を参照してください。

## CONTAINER-005の具体化判断

2026-09-25の選別では、旧`CNT-003..006`を一つのWorkload privilege confinementへまとめました。Application processの侵害からroot、kernel機能、host attachment、writable root filesystem、control-plane credentialへ進む経路は、全containerを同じ実効runtime profileで扱う必要があるためです。

`CNT-007`のresource availabilityはquota、scheduling、eviction、node capacity、runtime PIDを、`CNT-008`のnetwork segmentationはCNI、identity、ingress／egress、DNS、外部境界を扱うため分離しました。その後、resourceはCONTAINER-007、networkはCONTAINER-006へ移行しました。IaC／CI検査は早いfeedback、live admissionはcontroller生成後を含む最終強制点とし、同じ成果として扱いません。項目ごとの判断は[Workload confinement移行記録](WORKLOAD_CONFINEMENT_MIGRATION.md)に保持します。

この主題はKubernetesの技術経路が明確なので、文書に加えて[Kubernetes 1.37 Pod Security Admission + CEL実装](../engineering/container-cloud-iac-security/workload-privilege-and-host-boundary/implementations/kubernetes-psa-cel/README.md)を必要な成果物に選びました。対象版、変更箇所、使い捨てclusterでの確認、解除、制限を記載し、YAMLとscriptをrepositoryで検査します。Live clusterの拒否とruntimeの実効状態は導入証拠として別に残します。

## CONTAINER-006の具体化判断

2026-09-25の選別では、旧`CNT-008`をWorkload network segmentationとして独立させました。Process権限を絞っても、侵害されたworkloadにneighbor、管理service、外部宛ての通信が残ればlateral movementやexfiltrationが成立するため、CONTAINER-005へ統合しません。

この主題ではKubernetes core NetworkPolicyの技術経路が明確であり、policy objectを受理するだけでdata planeの強制を証明できない失敗も具体的です。そのため[Kubernetes 1.37 NetworkPolicy実装](../engineering/container-cloud-iac-security/workload-network-allow-boundary/implementations/kubernetes-networkpolicy/README.md)を必要な成果物に選びました。三つの使い捨てnamespaceでdefault denyを先に配置し、source egressとdestination ingressの片側allowを個別に追加・削除して実通信の成功・拒否を確認します。

DNS、external destination、IPv6、hostNetwork、node traffic、NAT、L7 identityには共通の安全な固定値がありません。代表実装へ架空のallowを足さず、flow contractと採用CNI・gateway・proxyに応じて具体化する項目としてpatternへ残しました。RepositoryではYAMLとshellを静的に検査します。Live CNI enforcementは未実行であり、導入証拠にはしません。項目ごとの判断は[Network segmentation移行記録](NETWORK_SEGMENTATION_MIGRATION.md)に保持します。

## CONTAINER-007の具体化判断

2026-09-25の選別では、旧`CNT-007`をWorkload resource consumption boundsとして独立させました。Process privilegeとnetwork reachabilityを制限しても、loop、fork、log、replica増加が共有nodeや別tenantのCPU、memory、PID、local storage、object capacityを枯渇させるためです。

Workloadのrequest／limit、namespaceのaggregate quota、node allocatable・reservation・pressureは別の強制点ですが、直接の失敗は「一workloadの消費が共有capacityへ広がること」です。一つのcontrolの別特性として保持し、[Kubernetes 1.37 ResourceQuota + CEL実装](../engineering/container-cloud-iac-security/workload-resource-budget-and-pressure-boundary/implementations/kubernetes-resourcequota-cel/README.md)はnamespace admissionとquotaだけを具体化しました。

旧固定値を普遍的な安全値として移さず、test profileに限定しました。Live APIでは必須値不足、aggregate quota超過、正常PodのQoSとquota usageを確認する構成です。PID、node reservation、pressure／eviction、cgroup、capacityはproviderとnode構成に依存するため、架空のplatform evidenceで完了させません。RepositoryではYAMLとshellを静的に検査し、live clusterでは未実行です。項目ごとの判断は[Resource consumption移行記録](RESOURCE_CONSUMPTION_MIGRATION.md)に保持します。

## CONTAINER-003の具体化判断

2026-09-25の選別では、旧`PSB-CONTAINER-003`をContainer host and daemon boundaryとして再編集しました。Workload specのnon-root、capability、hostPath、seccomp等はCONTAINER-005へ残し、CONTAINER-003はruntime socket、kubelet・補助endpoint、host上のprotected state、node identity、host側isolation、管理操作、更新・隔離・再登録を扱います。

Provider-neutralなcontrol、教材、[Node runtime and management boundary](../engineering/container-cloud-iac-security/node-runtime-management-boundary/README.md)は必要な成果物に選びました。一方、具体実装は対象OS distribution、runtime、Kubernetes distribution、managed／self-managed provider、node image build、identity、network、attestationで変更箇所と確認方法が変わるため追加していません。

旧synthetic `policy.json`、`host-evidence.json`、exception fixture、Python verifierはlive hostを観測せず、自己申告値の比較を実効的なhost implementationに見せるため非移植です。対象platform、変更箇所、使い捨てnode pool、更新・隔離・rollback、取得可能なlive evidenceを一組で選べた時に限定名のimplementationを作ります。詳細は[Container host and daemon移行記録](CONTAINER_HOST_DAEMON_MIGRATION.md)に保持します。

## IAC-001の具体化判断

2026-09-25の選別では、旧Secure IaC Golden Pathを[Infrastructure change authorization and drift boundary](../controls/records/container-cloud-iac-security/psb-iac-001-infrastructure-change-authorization-and-drift/README.md)へ再編集しました。Golden Pathは標準moduleとworkflowによって安全な変更を作りやすくする入口です。Controlの合格は、reviewしたsource・module／provider・入力・policy・targetがresolved plan、policy decision、保存plan、apply authority、provider上の実resourceへ結ばれることで判断します。

Provider-neutralなcontrol、教材、[Infrastructure plan, apply, and drift boundary](../engineering/container-cloud-iac-security/infrastructure-plan-apply-and-drift-boundary/README.md)は必要な成果物に選びました。旧Python verifierとJSON fixtureはTerraform、OPA、provider APIを実行せず、全変更経路、drift、identity、remediation等を自己申告fieldで表していたため非移植です。

具体実装は、exact IaC tool・policy engine、一provider、一resource、一つのsecurity invariant、使い捨てcloud環境、protected apply、provider-side bypass test、drift・cleanupを一組で選べる時に作ります。Localだけのsynthetic planやmulti-cloud共通fieldを実効的なimplementationとして追加しません。詳細は[IaC移行記録](IAC_CHANGE_BOUNDARY_MIGRATION.md)に保持します。

## REL-002の具体化判断

2026-09-25の選別では、旧`PSB-REL-002`を[Provenance distribution and availability boundary](../controls/records/release-integrity/psb-rel-002-provenance-distribution-availability/README.md)へ再編集しました。一releaseに複数artifact、一artifactに複数attestationが存在できる前提で、artifact digestからprovenance identityを発見し、intended consumerが取得できる関係を扱います。

Provider-neutralなcontrol、教材、[Provenance distribution and availability](../engineering/release-integrity/provenance-distribution-and-availability/README.md)は必要な成果物に選びました。旧Python verifierとJSON fixtureはnetwork、registry、release API、storage、consumer clientを実行せず、`immutable`・`available`・`public`等の自己申告fieldを比較していたため非移植です。

具体実装は、artifact ecosystemと対象版、artifact・attestation形式、producer／consumer identity、使い捨てrepository、immutability・retention・garbage collectionを一組で選べる時に作ります。固定5分・365日を普遍値として移さず、artifactのconsumption・support・investigation windowへ合わせます。詳細は[Provenance distribution移行記録](PROVENANCE_DISTRIBUTION_MIGRATION.md)に保持します。

## BUILD-002の具体化判断

2026-09-26の選別では、旧Hosted consistent buildを[Approved and consistent release build](../controls/records/build-security/psb-build-002-approved-consistent-build/README.md)へ再編集しました。SLSA v1.2のproducer責任に合わせ、目標profileに合うbuilder選定と、verifierが期待値を作れる一貫した手順を分けます。Hosted実行はBuild L2以上の選択時に必要です。

Provider-neutralなcontrol、教材、[Approved release build process](../engineering/build-security/approved-release-build-process/README.md)、診断観点を必要な成果物とし、実装例は保留します。旧verifierは`hosted`・`assessed_slsa_build_level`等のJSON値を読み、実platformやartifactを観測していません。再開時は一つのplatform、artifact family、provenance形式、protected publish gateを選び、正常、別builder・定義・parameter・local uploadの拒否、証拠障害の停止を使い捨てreleaseで確認します。詳細は[移行記録](CONSISTENT_BUILD_MIGRATION.md)に保持します。

## REL-005の具体化判断

2026-09-26の選別では、旧`PSB-REL-005`を[Artifact signing generation](../controls/records/release-integrity/psb-rel-005-artifact-signing-generation/README.md)へ再編集しました。承認したexact artifactと、署名サービスへ接続できる権限を別の条件として扱い、鍵の管理、署名結果のconsumer条件での検証、公開完了をrelease gateへつなげます。

Provider-neutralなcontrol、教材、[Artifact signing boundary](../engineering/release-integrity/artifact-signing-boundary/README.md)、診断観点を必要な成果物に選びました。旧OpenSSL verifierは暗号計算とbytes照合を実行しますが、KMS/HSM、鍵状態、透明性ログ、公開先、release gateは合成JSONの自己申告です。Artifact形式、signer、承認の強制点、公開先、consumer条件が未選定のため、旧envelopeを実装例へ移しません。再開時は使い捨てのrelease先で正常署名、別digest・別identity・signer障害・公開失敗・取得不能の拒否を観測します。詳細は[Artifact signing移行記録](ARTIFACT_SIGNING_MIGRATION.md)に保持します。

## REL-004の具体化判断

2026-09-25の選別では、旧`PSB-REL-004`を[Supplier SBOM intake trust](../controls/records/release-integrity/psb-rel-004-supplier-sbom-intake-trust/README.md)へ再編集しました。Provider-neutralなcontrol、教材、[Supplier SBOM intake boundary](../engineering/release-integrity/supplier-sbom-intake-boundary/README.md)、診断観点を必要な成果物とし、供給者の認証と成果物への結合を台帳取込の前に置きます。

旧verifierのEd25519署名計算は実値を確認しますが、独自envelope、手書き状態snapshot、自己申告の台帳権限をそのまま移すと、実供給者の失効・隔離・権限が確認できたように見えます。具体実装は、供給者と製品・成果物、署名または配送方式、利用者側の信頼根拠、時刻・失効・訂正のsource、使い捨ての取込先を選んでから作ります。正常、別製品・改変・未知署名者の拒否、状態取得不能、隔離の迂回を観測できることを完了条件にします。詳細は[Supplier SBOM移行記録](SUPPLIER_SBOM_MIGRATION.md)に保持します。

## REL-003の具体化判断

2026-09-25の選別では、旧`PSB-REL-003`を[Release SBOM identity and analysis boundary](../controls/records/release-integrity/psb-rel-003-release-sbom-identity-and-analysis/README.md)へ再編集しました。Source、build、deployment／operationsのSBOMを同じserialへ上書きせず、final artifactを観測したbuild／post-build SBOMをrelease authorityとしてexact artifact digestへ結びます。

Provider-neutralなcontrol、教材、[Release SBOM identity and analysis intake](../engineering/release-integrity/release-sbom-identity-and-analysis/README.md)に加え、[CycloneDX 1.7 artifact binding実装](../engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding/README.md)を必要な成果物に選びました。実artifact SHA-256、SBOM digest・serial・version、build／post-build phase、version付きPURL、`bom-ref`、dependency・composition参照、composition stateを実値で確認できるためです。9 testで正常、artifact変更、phase違い、dangling reference、型の不一致、JSON key重複、unknown composition、malformed inputを確認しました。

旧verifierのstorage、permission、processing receipt、analyzer healthはJSON内の自己申告を比較していたため非移植です。限定実装もCycloneDX schema全体や`complete`の正当性を証明しません。Productionでは固定schema validator、実generator coverage、release storage、intended-consumer retrieval、採用Dependency-Track版、data source health、deployment catalogを別に接続します。詳細は[Release SBOM移行記録](RELEASE_SBOM_MIGRATION.md)に保持します。

## SOURCE-002の具体実装計画

2026-09-23の具体化判断：Git hooksとsecret scannerを接続する技術経路を絞れ、検査対象の取り出し方、拒否への接続、
障害・出力の扱いを具体化すると読者が導入判断をできるため、実装例を必要な成果物に選びます。
文書と診断で確認する項目に加え、2026-09-23に[Git・Gitleaks代表実装](../engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks/README.md)を追加しました。
2026-09-25には、旧scannerを読みやすいローカル用の[Python pattern scanner](../engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner/README.md)として追加しました。
実装例としての完了条件は満たしました。組織の導入、実環境診断、全経路の強制は別の未実施事項です。

- **配置・範囲**：[Secret checks before publication](../engineering/source-protection/secret-checks-before-publication/README.md)配下の`implementations/`に、一つの代表構成を作る。対象OS・Git・scannerの版を確定し、staged内容・commit message・pushで導入する履歴を検査するローカルhooksとの接続を示す。
- **実装選択**：境界を厳しく扱う実装はGitleaks 8.30.1の組込み検出を採用し、独自scriptをGit objectの取得、上限・未対応形式の拒否、結果の整合確認へ限定した。別に、正規表現とhookの接続を読めるPython標準ライブラリ版を移行した。旧Docker wrapperとinstallerは非移植で、両実装の検出同等性は主張しない。
- **境界**：ローカル実装が担うSECRET-1〜4・6・7の範囲を明示する。SECRET-5は独立した受信側検査の具体設定・確認手順を一構成で示す。受信側が未完なら残作業として記録し、ローカルhooksや送信後のCIで達成した扱いにしない。組織全体の例外承認や全経路の導入済み状態は主張しない。
- **導入と更新**：既存hooks・設定への影響、明示的な導入方法、版の更新、解除・切り戻しを示す。未レビューのhookを自動実行しない。本PJ自身へのhooks有効化は実装例の追加と別の作業とする。
- **確認**：Gitleaks版は隔離した一時worktreeとbare repository、未発行で無効な検出用文字列により23件を確認した。正常入力、indexと作業ツリーの不一致、履歴・メッセージ・タグ・複数ref・force push・merge、ローカル省略時の受信拒否、設定弱体化、未対応形式、障害、非表示を含む。Python版は12 rule、near miss、値の非表示、staged内容、削除後も残るpush履歴、Gitによるhook起動を7件で確認した。
- **完了状態**：二つの実装について、設定・コード、前提、確認方法、未検証範囲を追跡できる。Gitleaks版では対象版と取得物digest、導入・解除手順、23件の確認も保持する。全確認項目の自動化、全OS、SaaS、旧installer・Docker wrapperの移植、実環境への適用は範囲外。

## 基本分類と横断分析

[Security scope](SECURITY_SCOPE.md)に従い、AI Development SecurityはAIを使う開発環境へ限定します。
製品自体のAI securityはai-security-foundryの担当です。旧AI-010・AI-011・DEPS-005・DETECT-002は`out-of-scope`です。旧AI-005〜009は[選別済み](AI_DEVELOPMENT_SCOPE_REVIEW.md)で、開発環境の一部だけを継続候補とします。旧52件との差をそのまま未移行の残件数として扱いません。

現行の11 domainを移行先の基本分類として維持します。[Domain一覧](../controls/README.md#domain一覧)を
読者の入口にし、未移行領域も明示します。成果物がない領域の空ディレクトリは作りません。
七つのレイヤーは偏り・空白、十二の攻撃段階は脅威・受け渡しを分析するために使います。
これらをdomainの置換や、領域ごとの全control移行の義務にしません。

一つの主題を移すたびに主なdomain、隣接domain、前後の受け渡しを確認し、Domain一覧と移行台帳を更新します。
初期三領域に加え、残る八domainの初回棚卸しも完了しています。今後は棚卸し結果と七つのレイヤーで優先主題を選びます。
PSIRTはGovernance / Operations、runner内の検知はCI/CD・Buildとの境界、本番runtimeは
Container / Cloud / IaCとの境界を検討します。教材は主なcontrolの`learning.md`に置き、隣接controlからリンクします。
講義や再学習で育つ問いを、独立した洞察ファイルへ先回りして分離しません。
基本分類の変更はADRに記録します。境界の詳細は[リポジトリ設計](REPOSITORY_DESIGN.md)を参照してください。

## 初期パイロットで確認した構造

| パイロット | 検証する情報設計 | 残す実装価値 |
|---|---|---|
| [PSB-SOURCE-004](../controls/records/source-protection/psb-source-004-source-access-credential-lifecycle/README.md) | ガイダンス中心の主題を、成果、教材、設計、製品手順へ分ける | GitHubとIdPの導入判断。架空のJSON検査による導入済み判定は移さない |
| [PSB-DEPS-001](../controls/records/dependency-security/psb-deps-001-dependency-release-cooldown/README.md) | 抽象的な観測期間とresolver／proxy固有の挙動を分ける | 小さなnpm設定例。汎用検証器とproxy clientの一括移植は行わない |
| [PSB-CICD-005](../controls/records/cicd-security/psb-cicd-005-untrusted-pr-boundary/README.md) | 信頼境界、攻撃教材、設計パターン、実行可能な設定を分ける | 無権限PR検証とmerge後のfresh run。危険な比較例は隔離する |

初期三件と、その後のBuild・consumer・Application・Operationsで、成果物を分ける構造をレビューしました。
詳細は[構造レビュー](STRUCTURE_REVIEW.md)に保持します。教材はcontrol・patternへ辿れるnavigationを維持し、受講者個人の理解度や受講記録は本PJで管理しません。

## 参照資料の名称と構造を見直す

参照資料の影響を強めるとは、参考文献を増やすことではありません。資料の役割、採否、変更した判断、
残余境界を、各成果物の設計に反映することです。

移行する資料ごとに次を行います。

1. 主な役割を、規範仕様、脅威、製品仕様、実装候補、ポートフォリオ分析、統合資料に分ける。
2. その役割を誤解させるIDと見出しを見直す。AI、GitHub、toolなどの目立つ語だけで命名しない。
3. 参照版、確認日、ライセンス、採用／変更して採用／不採用、利用先、限界を記録する。
4. 直接の特性根拠と、横断分析だけに使う資料を別の関係として記録する。
5. 廃止したIDは[移行台帳](MIGRATION.md)にだけ残し、新しいツリーや索引へ別名を持ち込まない。

この見直しの最初の対象は`REF-PORTFOLIO-001`でした。七つのレイヤーによる全体分析と、個別のAI境界の
解釈を区別します。他のIDも自動的には継承せず、対応する主題を移す時に資料単位で判断します。

## 一つの主題を移す手順

三領域の初回棚卸しは[Migration candidates](MIGRATION_CANDIDATES.md)を参照してください。
残る8 domainの初回棚卸しは[Portfolio migration review](PORTFOLIO_MIGRATION_REVIEW.md)を参照してください。
個別実装の詳細レビューは未完了です。

```text
旧成果物と参照資料を読む
  -> 直接の失敗、信頼境界、読者の問いを再定義
  -> 主題の具体化判断を行い、必要な成果物・理由・範囲・完了条件を決める
  -> control／教材／pattern／実装／評価へ必要な内容だけ分ける
  -> 参照資料の役割・ID・採否を見直す
  -> 隣接境界と前後の受け渡し、診断で確認する項目を整理
  -> リンク、版、マッピングを検査。実装を変更した場合は必要な挙動を検証
  -> 読み通しレビュー
  -> 移行台帳と横断索引、この計画の現在地・次作業を更新
```

一回の移行は一つの主題を単独でレビューできる大きさにします。旧52件を一対一変換することや、
旧READMEの全項目を移行先のどこかへ必ず残すことは目標にしません。ただし参照仕様と重要な除外判断は省略しません。

## 独立化後に残る運用判断

公開先と初版の範囲は[Repository cutover](REPOSITORY_CUTOVER.md)で確定しています。
ライセンスは未指定です。旧版READMEからの案内の反映状況と、旧版の維持期間・アーカイブ化は別途確認・判断します。
これらをcontrolの移行完了や実環境の導入済み状態と混同しません。

## 分析の正本

- [参照資料の方針](SOURCE_POLICY.md)
- [参照資料と仕様](../sources/README.md)
- [横断分析の軸](ANALYSIS_LENSES.md)
- [移行台帳](MIGRATION.md)
