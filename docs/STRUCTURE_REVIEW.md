# Structure review

この文書は構造レビューの結果と、その後の補修の記録です。現在地と次作業は[進め方と移行計画](MIGRATION_PLAN.md#現在地と次の作業)を参照してください。

## 2026-10-03：GOV-001のframework関係

SSDF RV.1.1の報告後の製品影響調査とRV.2.1の対応計画に必要な適用性情報を、GOV-001の部分的な設計関係として残しました。旧ATT&CK T1195.001の`detects`は、既知版の利用先特定を攻撃行動の検知と取り違えるため非継承です。[資料記録](../sources/README.md#ref-supply-chain-impact-001)、[現行mapping](../mappings/frameworks.yaml)、[移行台帳](MIGRATION.md)に範囲と理由を記録しました。全108関係のうち60件が設計関係のレビュー済み、48件が再レビュー待ちです。実inventory・稼働先の網羅性と対応実施は未確認で、新しい実装やテストコードは追加しません。

## 2026-10-03：DETECT-001のframework関係

NIST SP 800-190 §4.1.1のイメージ脆弱性検査に必要な証拠の範囲と状態だけを、DETECT-001の`SCAN-2・3・4`に対する`design-reviewed`の部分関係として残しました。旧SSDF RV.1.1・PW.4.1、OSPS VM-06.02、NIST SP 800-190 §4.4.1は、継続収集・調査、第三者部品の採用、全変更の自動拒否、稼働中ランタイムの監視をDETECT-001自身が要求しないため非継承です。[資料記録](../sources/README.md#ref-scanner-evidence-001)と[移行台帳](MIGRATION.md)に理由を記録しました。全109関係のうち58件が設計関係のレビュー済み、51件が再レビュー待ちです。実scannerと受入gateは未確認で、新しい実装やテストコードは追加しません。

## 2026-10-03：DEPS-004のframework関係

OSPS VM-05.03のうち変更依存の既知脆弱性gateと、SSDF PW.4.1の採用レビューへ絞った二関係を`design-reviewed`にしました。OSPS VM-05.01のライセンスを含む是正閾値、VM-05.02のrelease前対応、ATT&CK T1195.001の悪意ある依存・開発ツール改変は、現行DEPS-004の必須特性からは説明できず非継承です。[資料記録](../sources/README.md#ref-deps-002)、[mapping](../mappings/frameworks.yaml)、[移行台帳](MIGRATION.md)に採否と限界を記録しました。全113関係のうち57件が設計関係のレビュー済み、56件が再レビュー待ちです。実環境のmerge拒否、悪意ある依存の検知、準拠は未確認です。必要な成果物は既存文書の補修で、新しい実装やテストコードは追加しません。

## 2026-10-03：DEPS-003のframework関係

旧ATT&CK T1195.001の`high`は、承認済み依存から未レビューの内容へずれる経路に限る`medium`の部分関係へ改めました。NIST SSDFの旧PW.4.1は継承せず、取得した部品の完全性確認を例示するPW.4.4の一部へ新しく対応付けました。OSPS BR-05.01の標準ツール使用はDEPS-003の特性が要求しないため、旧関係を外しました。根拠と限界は[資料記録](../sources/README.md#spec-dependency-lock-identity)と[現行mapping](../mappings/frameworks.yaml)、非継承理由は[移行台帳](MIGRATION.md)へ記録しています。全116関係のうち55件が設計関係のレビュー済み、61件が再レビュー待ちです。実際の通常build・取得物照合は確認していません。必要な成果物は既存mapping・control案内・資料記録の補修で、新しい実装やテストコードは追加しません。

## 2026-10-02：DEPS-002のframework関係

ATT&CK T1195.001のうち、悪意ある依存の準備時コードを実行する経路に対して、DEPS-002の既定拒否・対象を絞った承認・迂回と評価失敗の扱いを照合しました。脅威技法全体の緩和ではないため旧`high`を`medium`へ下げ、部分的な設計関係としました。NIST SSDF PW.4.1は部品の取得・評価・維持を求め、準備処理の実行可否そのものを示す要件ではありません。旧関係は現行mappingから外し、理由を[移行台帳](MIGRATION.md)へ記録しました。実際のinstall拒否や組織導入の確認は行っていません。必要な成果物は既存mapping・control案内・資料記録の補修だけで、新しい実装やテストコードは追加しません。

## 2026-10-01：DEPS-001のframework関係

MITRE ATT&CK v19のT1195.001とNIST SP 800-218最終版のPW.4.1を、DEPS-001の特性へ照合しました。待機期間が扱うのは新しく公開された依存版の早期採用であり、ATT&CKの開発ツール侵害や古い悪意ある版には対応しません。SSDFは第三者部品の取得・維持を求めますが、公開後の待機時間は指定しません。両者とも部分的な設計関係として`design-reviewed`へ進め、例外管理のDEP-AGE-6を対象propertyから外しました。残るreview待ちは66件です。実際の依存解決、インストール前の拒否、SSDF準拠は未確認です。必要な成果物は既存mapping・control案内・資料記録の補修であり、新たな実装やテストコードは追加しません。

根拠の版と採否は[資料記録](../sources/README.md#ref-deps-004)へ、propertyごとの範囲は[framework mapping](../mappings/frameworks.yaml)へ記録しています。

<a id="framework-mapping-review"></a>

## 2026-10-01：Framework mappingの状態と実証表現

`frameworks.yaml`の118関係は、資料と現在のcontrol特性を照合した`design-reviewed`が50件、旧関係の再レビュー待ちが68件でした。後者の`relationship: verifies`や`confidence: high`は過去の判断を保持した値で、現在の要件検証や導入結果ではありません。その読み方を機械可読のpolicyとmappingの入口へ明記しました。

旧`verifies/high`の14件を確認し、Release・Buildの説明に残る「直接実装」「policy testで検証」を設計の説明へ直しました。AI拡張の二行も、出所・完全性・実行時許可を確認済みとする語を外しました。14件すべてに未確認範囲が分かる`limitation`があります。`design-reviewed`のCONTAINER-004は、既存のNIST SP 800-190 §4.4.4照合記録に沿って部分関係の範囲・限界を追記しました。今回の補修は新たな規範資料のレビュー、準拠判定、実環境のテストではありません。

確認結果：118件のproperty参照はすべて現行controlに解決し、50件の`design-reviewed`にはレビュー範囲・限界、14件の旧`verifies/high`には限界があります。`make test`で2698件のローカルリンク、47 control ID、文書検査4件はエラー0件。`git diff --check`も成功しました。

## 2026-10-01：成果物間mappingと限定実装の境界

`pilot.yaml`のpattern→controlと実装例→patternの関係を点検しました。既存の19実装例のscope・rationaleには、未導入を明記したものが多い一方、SOURCE-002のGitleaks版とPython版は設計から辿る関係がありませんでした。両例を別々に結び、受信側を含むGit経路とローカルhookのみの経路、検出・書込み経路・例外の残る範囲を記録しました。

KubernetesのResourceQuota＋CEL例は`RESOURCE-1〜4・7`の全特性を満たすように読めるscopeと、live API拒否を確認済みと読める説明を持っていました。各特性のうちnamespace quota・admissionで示せる部分に限定し、live clusterでは未実行としました。Mappingの入口でも`implements`は設計上の関係、`realizes`は具体化した部分との関係であり、controlの合格や導入証拠ではないと明記しました。必要な成果物はmappingと読み方の補修で、新しい実装・テストコードは追加しません。

確認結果：`pilot.yaml`の72関係（設計51、実装例21）の参照先・重複・control特性IDを確認。`make test`で2698件のローカルリンク、47 control ID、文書検査4件はエラー0件。`git diff --check`も成功しました。

## 2026-10-01：設計patternと実装例の横断mapping

横断mappingに収録した33設計patternと6実装例の関係一覧・制限を点検しました。Build、Release、IaC、AI Developmentの設計で、前段からsource・artifact・権限条件を受け取るだけの関係を`handoff`としていた12箇所を`adjacent`へ直しました。対応・復旧からclean buildや権限の停止を前段の実行系へ戻す関係は、実際に判断を渡すため`handoff`のままです。六つの実装例は対象と未確認事項を本文と照合し、対応範囲を広げる変更はしませんでした。

関係の意味を横断分析とmappingの入口に明記しました。これらは導入・強制の証拠ではありません。全pattern本文の詳細な妥当性、実装例のlive動作、収録していないpatternの追加要否は未確認です。必要な成果物はmappingとその読み方の補修で、新しい実装・テストコードは追加しません。

確認結果：`make test`で2698件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。YAMLの86成果物のID重複・参照先欠落・横断資料IDの混入はなく、`git diff --check`も成功しました。

## 2026-10-01：横断mappingとcontrolの対応

横断mappingの86成果物と47 control記録を読み込み、各controlに明記された主レイヤー・直接段階・引き渡し段階を照合しました。SOURCE-003は公開候補を探し所有者が判断するところまでが直接の責任で、インシデント対応は引き渡しです。CICD-007のrelease段階とCICD-009の対応段階には、本文に独立した受け渡しを定義していなかったため、control記録から外しました。十二段階の表は代表的な直接対応を補い、CONTAINER-005の稼働時観測への引き渡しを明示しました。

`REF-PORTFOLIO-001`と`LOCAL-SUPPLY-CHAIN-ATTACK-STAGES`はmappingの分析軸にのみ置かれ、成果物別の`source_refs`には混在していません。構造的な照合で明示された段階関係の食い違いは0件です。残るpattern・実装例の関係を含めた意味的妥当性、組織導入、実環境の強制は確認していません。必要な成果物はcontrol記録と横断分析の補修であり、新しい実装例・テストコードは追加しません。

確認結果：`make test`で2698件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

## 2026-10-01：横断分析と入口の状態表記

READMEとcontrol・engineeringの入口を、Sourceから復旧までの横断分析と照合しました。READMEに残っていた初期pilot中心の対象・制限事項を現在の使い方と移行記録への案内にまとめました。横断分析では、署名境界の完了をrelease全体の完了と誤読させる表現、CONTAINER-002移行後もregistry publicationが未実装と読める表現、移行済みのworkflow権限を「次の主題」とする表現を補修しました。十二段階の表でもSOURCE-006、CODE-005、CICD-004などの既存成果物と、GOV-002の隣接関係を見えるようにしました。

必要な成果物は入口と横断分析の補修です。新しいcontrol、実装例、テストコードは追加しません。組織への導入、実環境での強制・復旧、機械可読mapping全件と本文の意味的な一致は未確認です。次はそのmappingを確認します。

確認結果：`make test`で2698件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

## 2026-10-01：稼働観測から復旧完了への受け渡し

GOV-001からGOV-005へ渡す元の調査範囲、CONTAINER-001の使用許可、CONTAINER-004のruntime検知を読み合わせました。検知アラートの不在、rollout成功、desired stateの新digestは旧digestの非稼働を示しません。GOV-005のcontrol・機械可読記録・教材・patternに、元のtargetごとの実稼働digest、観測時刻・収集範囲、停止・切り戻し経路の確認を明記しました。対象の一部を廃止する場合は、新digestを配置したとみなさず、実体の停止・削除と再起動経路を確認します。

必要な成果物は既存文書の補修と診断項目です。新しいcollector、verifier、テストコードは追加しません。判断の根拠と旧成果物との関係は[資料記録](../sources/README.md#ref-deployed-artifact-recovery-001)と[移行記録](DEPLOYED_ARTIFACT_RECOVERY_MIGRATION.md#2026-10-01の横断レビュー)へ残しました。Live inventory、再投入拒否、復旧完了は未確認です。

確認結果：`make test`で2707件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。GOV-005の機械可読記録の読取りと`git diff --check`も成功しました。

## 2026-10-01：Releaseから使用許可・稼働観測への受け渡し

Release IntegrityとCONTAINER-001・002の既存control・教材・設計を読み合わせました。個別の本文では区別できていた「registryに公開・保持した」「admissionで使用を許した」「runtimeで実際に稼働した」を、両分野の入口から順に辿れるようにしました。Admission patternでも`ALLOW`を稼働証拠へ置き換えず、後段のdigest観測へ渡すと明記しました。旧digestの非稼働と復旧完了はGOV-005の判断です。

必要な成果物は既存の入口とpatternの補修です。採用するregistry・cluster・runtime collectorが未定のため新しい実装例やテストコードは追加しません。実registryの公開・状態、admissionの拒否、runtimeのdigest対応、旧digestの非稼働は未確認です。

確認結果：`make test`で2701件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

## 2026-10-01：CI/CDからRelease Integrityへの受け渡し

CIのPR境界・job権限・cloud交換から、BUILD-002・003とRelease Integrity五controlへ渡す内容を読み合わせました。CIの検査成功や権限取得だけでは公開対象のbytesや承認内容が決まらないこと、署名・来歴配布・SBOM公開は必要な条件ごとに確認し、一つの成功をrelease全体の完了へ変換しないことをRelease分野の入口へ示しました。五controlから教材と設計patternへ直接辿れるようにもしました。

署名patternの図と説明では、`SIGNED_AND_AVAILABLE`を署名境界の結果として明示しました。今回の成果物は既存文書の補修で、新しい実装例・テストコードは作りません。実公開・配布、利用者側の検証・使用拒否、稼働中のdigestとの対応は未確認です。

確認結果：`make test`で2694件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

## 2026-09-30：CICD-006の診断項目

CI/CD Securityの検査結果、job権限、PR境界、runner・cacheと、cloudへの権限交換の役割を読み合わせました。CICD-006は要件・教材・設計に交換条件と操作権限の違いがありましたが、control本文から直接使える診断項目がありませんでした。そこで、別issuer・audience・workload文脈の拒否、未信頼状態からのtoken取得、交換後の不要操作、旧key・派生session、確認不足を分けて列挙しました。

必要な成果物は既存control・pattern・資料記録の補修です。製品共通の診断チェックリストで判断できるため、新しい実装例・テストコードは追加しません。[GitHubとAWSの公式資料](../sources/README.md#spec-workload-federation)でtokenのclaimと受け入れ先の実際の条件を区別しました。実trust、交換、操作拒否、旧keyの失効は未確認です。

確認結果：`make test`で2684件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

## 2026-09-30：CI/CD Securityの横断レビュー

七つのcontrolの入口と設計への導線を照合し、各controlから対応するpatternをたどれるようにしました。特にCICD-005のGitHub例では、`main`へのpushで新しいrunを始め、SHAを照合しても、その変更がレビュー済みとは言えません。そこでworkflowの名称・marker、controlの診断項目と判定例、patternと導入手順に、branch保護・rulesetの対象、直接push、bypassを確かめる判断を加えました。[GitHub公式資料](../sources/README.md#spec-github-security-guidance)の可変Web版を2026-09-30に確認しています。

必要な成果物は既存文書とGitHub例の補修です。新しい実装例やテストコードは作りません。Review経路とbypassの実効設定、直接push拒否、実runは未確認です。設定例のmarkerは権限操作をしないため、実環境での権限処理の安全性も未確認です。

確認結果：`make test`で2681件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。GitHub例のYAML読取りと`git diff --check`も成功しました。

## 2026-09-30：Source Protectionの横断レビュー

六つのcontrolの入口、各教材、設計pattern、限定実装への導線を照合しました。分野READMEは六つの教材を列挙しながら「読み進め方」がSOURCE-004だけの順路だったため、各controlに設計への直接リンクを置き、端末・権限、公開前検査・公開後の観測、復旧の三つの読み筋へ整理しました。Engineering索引でも六つのpatternを一箇所にまとめ、一覧名を現在の収録範囲へ揃えました。

横断分析に残っていた「SOURCE-003にはprovider実装がない」「SOURCE-002はガイダンスのみ」という古い制限表記を、限定実装の存在とlive導入未確認の区別へ直しました。新しいcontrol・実装・テストコードは追加していません。これは導線と状態表記の執筆者レビューであり、実組織への導入や利用者による読書評価ではありません。

確認結果：`make test`で2674件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。横断分析YAMLの読取りと`git diff --check`も成功しました。

## 2026-09-30：SOURCE-002・003の読み合わせ

既存control・教材・pattern、GitHubの公開情報監視例を照合しました。実際の認証情報が共有先へ届いたと分かっている事象は、非公開リポジトリでも所有者に渡し、到達範囲・失効・利用履歴を判断します。受信側の拒否は送信前の拒否と異なります。SOURCE-003の公開検索は既知経路外の候補や追加のcopyを探すもので、再発見まで対応を待たせないよう文書を補修しました。[Gitの受信側仕様とGitHub資料](../sources/README.md#ref-secret-publication-001)を再確認し、この受け渡しは本PJの解釈として記録しています。

新しい実装・テストコードは追加していません。実GitHubの受信・検索、認証情報の失効、通知と対応は未確認です。具体化と導入の残りは[計画](MIGRATION_PLAN.md#source-002003の読み合わせと具体化判断)を参照してください。

確認結果：`make test`で2677件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。

## 2026-09-30：SOURCE-005の読み合わせ

既存control・教材・pattern・Git mirror例を照合しました。取得前に不正変更された世代は、Git objectの整合性と取得時のref一覧との比較に成功し得ます。そこで、復旧する世代の選択をGitの復元成否から分け、変更の経緯、承認済みの変更記録、以前の世代で判断する流れを診断項目・教材・設計・実装説明へ補いました。判断できない場合は復旧完了にしません。[NIST SP 800-61 Rev.3](../sources/README.md#ref-repository-recovery-001)の復旧用資産と復元後の資産を確認する考え方を参照しました。具体的なGitの選び方は本PJの解釈です。

新しい実装・テストコードは追加していません。七つのローカルGit試験は整合性と復元経路の確認で、侵害前の世代選択や実組織での開発再開の証拠ではありません。残る実評価は[具体化判断](MIGRATION_PLAN.md#source-005の具体化判断)を参照してください。

確認結果：`make test`で2668件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`make test-repository-recovery`の実Git試験7件、SOURCE-005の機械可読記録のJSON読取り、`git diff --check`も成功しました。

## 2026-09-30：SOURCE-006の読み合わせ

既存control・教材・pattern・GitHub手順を照合しました。組織のApp申請・インストール制限、OAuth Appの承認、PATの有効期間方針は、既存の認可を同じ方法で失効させません。方針変更後の現在のgrantと実効アクセスを確認し、不要なものはSOURCE-004の失効判断へ渡すよう、診断項目・教材・設計・GitHub手順を補修しました。GitHub公式のApp、OAuth、organizationのPAT方針の現行Web本文を[Sources](../sources/README.md#spec-github-organization-posture)へ追記しました。

新しいcontrol・教材・実装・テストコードは増やしていません。実組織での方針変更、既存token・App、拒否、通知は未確認です。実導入と確認の残りは[具体化判断](MIGRATION_PLAN.md#source-006の具体化判断)を参照してください。

確認結果：`make test`で2665件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。GitHubの実組織は操作していません。

## 2026-09-30：SOURCE-004の読み合わせ

端末状態の悪化から失効を求めるとき、元のトークンを止めるだけでは、既存セッションや別に発行した鍵・アプリ権限が残り得ます。Controlに診断項目を設け、教材・pattern・GitHub実装案へ失効単位と拒否確認を戻しました。[GitHub Enterprise CloudのSAML管理](https://docs.github.com/en/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization)、[fine-grained PATの失効](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-programmatic-access-to-your-organization/reviewing-and-revoking-personal-access-tokens-in-your-organization)、[認可取消と認証情報削除](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/respond-to-incidents/revoke-authorizations-or-tokens)の可変文書を照合しています。

これらは製品固有の失効範囲を示す資料であり、組織への導入や実際の拒否を示しません。今回の成果物は文書と診断項目で、追加のコードやテストはありません。旧framework mappingは再割当せず、[具体化判断](MIGRATION_PLAN.md#source-004の読み合わせと具体化判断)に限界を記録します。

確認結果：`make test`で2661件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。SOURCE-004のYAML読取りと`git diff --check`も成功しました。GitHubの実組織やテスト用認証情報は操作していません。

## 2026-09-30：SOURCE-001の読み合わせ

登録と現在の観測が分かれていても、端末状態の悪化を資産側の既存セッションへ反映できなければアクセス制限になりません。既存control・教材・patternへ、新規ログインと継続中の接続で再評価時点を分け、反映までの時間と残る権限を確認する判断を補いました。旧Linux adapterはローカル設定の一部を読むものの、MDM・通知・資産側の失効は観測しません。

[NIST SP 800-207 §3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf)の端末状態を用いたアクセス判断と接続終了の役割を設計入力にしました。資産別の再評価時点と許容時間は本PJの解釈です。新しい実装例・テストコードは追加せず、実MDM・端末・ソース管理・遠隔開発環境の連携は未確認です。[具体化判断](MIGRATION_PLAN.md#source-001の読み合わせと具体化判断)に範囲を記録します。

確認結果：`make test`で2654件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。SOURCE-001のYAML読取りと`git diff --check`も成功しました。実端末・実セッションは操作していません。

## 2026-09-29：DETECT-001の読み合わせ

既存control・機械可読記録・教材・patternを照合しました。予定した対象の一部で指摘が出て別の対象が解析不能な場合、`FINDING`だけでは完了を誤認させ、`ERROR`だけでは既知の指摘を失います。全体は`ERROR`として受入を止め、指摘を別に保持して調査へ渡す判断を補いました。`CLEAN`／`FINDING`の集約も対象と検出カテゴリが完了した範囲に限定します。

[zizmor公式Usage](https://docs.zizmor.sh/usage/)でSARIF時の終了状態と部分的な解析失敗の説明を再確認しました。この集約判断は本PJの解釈であり、旧製品版やTrivy・DockSecの現行挙動を確認した意味ではありません。新しい実装例・テストコードは追加していません。完了条件と未確認範囲は[具体化判断](MIGRATION_PLAN.md#detect-001の読み合わせと具体化判断)に記録します。

確認結果：`make test`で2649件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。実scannerとCI受入は未確認です。

## 2026-09-29：DETECT-003の読み合わせ

旧Python verifierは入力済みの候補と台帳を照合し、是正済み候補の再出現を判定しますが、外部collector、台帳の正しさ、通知先の受領を観測しません。既存control・教材・patternに、部分取得で新たに見えた候補は調査し、見えなかった既存候補は保持する判断を補いました。台帳や収集pageの取得不足を全件一致や是正完了へ変換しません。

[NIST CSF 2.0](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final)の公開ページと[CISA BOD 23-01](https://www.cisa.gov/news-events/directives/bod-23-01-improving-asset-visibility-and-vulnerability-detection-federal-networks)の公開検索本文を確認しました。後者の直接取得は403でした。状態遷移は資料からの引用要件ではなく、本PJの設計判断です。新規実装・テストコードは追加していません。完了条件と未確認の実環境は[具体化判断](MIGRATION_PLAN.md#detect-003の読み合わせと具体化判断)に記録します。

確認結果：`make test`で2643件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。実APIと台帳の照合は行っていません。

## 2026-09-29：DESIGN-001の読み合わせ

請求書の単体read／updateを起点に、認証された主体と対象データへの権限を分けました。Python／SQLite実装はowner・tenant付きqueryを行いますが、`Principal`の生成元、HTTP、全endpoint、並行処理は実装外です。実装READMEの古い`experiments/next-repository` pathを直し、手元の使い捨てrepositoryへコピーして試す手順と解除を追加しました。

ASVS 5.0.0固定版V8.2.1・V8.2.2とcontrol特性を照合し、二件の部分的な設計関係を追加しました。Field別権限、信頼できるservice層、全tenant操作の要件にまで拡張しません。完了条件と未確認範囲は[具体化判断](MIGRATION_PLAN.md#design-001の読み合わせと具体化判断)に記録しています。

確認結果：Python 3.10.4で既存7件の実装testと、使い捨てrepositoryへのコピー後の同じ7件を確認しました。`make test`で2637件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。Framework mappingはYAMLとして読め、118件です。`git diff --check`も成功しました。

## 2026-09-29：CODE-005の読み合わせ

UTS #55固定版のline break spoofingとPython 3.10の物理行・コメントの字句規則を照合しました。既存Python例は、U+000B、U+000C、U+0085、U+2028、U+2029を含むコメントを`PASS`にしていたため、`display-line-break`として報告するよう修正しました。Control・教材・pattern・参照記録にも表示と処理系の改行差を戻し、Python限定profileを一般要件にはしません。

Review UIとprotected CIの採用先は未選定です。必要な成果物と完了条件は[具体化判断](MIGRATION_PLAN.md#code-005の読み合わせと具体化判断)に記録しました。

確認結果：Python 3.10.4と手元のPythonで実装test各13件が成功しました。`make test`で2632件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。YAMLの読取りと`git diff --check`も成功しました。実repositoryのmerge拒否は未確認です。

## 2026-09-29：IAC-001の読み合わせ

利用者提供のGolden Path原文、既存control・教材・patternと、Terraformのplan／apply・依存lock・refresh、OPAの公開資料を照合しました。Golden Pathを作業の入口、保存planに結び付いた承認を実行前の判断、apply結果とprovider inventoryを実状態の確認として分けています。保存planの指定だけでTerraform側の対話承認が不要になること、途中失敗も自動で元に戻らないことを補いました。

文書と診断項目を今回の成果物とし、実装例・テストコードは追加していません。対象provider・resource・plan store・cloud identityが未選定で、live apply、provider側の迂回拒否、driftは未確認です。[具体化判断](MIGRATION_PLAN.md#iac-001の読み合わせと具体化判断)に記録しました。

確認結果：`make test`で2626件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。`git diff --check`も成功しました。実cloud操作は行っていません。

## 2026-09-29：CONTAINER-005〜007の読み合わせ

Workload権限、通信、資源のcontrol・教材・patternと既存Kubernetes例を照合しました。CONTAINER-005の受付時policyを既存Podのruntime強制と混同せず、CONTAINER-006では拒否probeの宛先listenerも確認し、CONTAINER-007はcontainer単位budgetを選ぶtest profileと明記しました。Kubernetes 1.37で利用できるPod-level CPU・memory予算を、共通要件から除外したわけではありません。

三つの`verify.sh`で使い捨て対象の事前確認を揃え、既存のnamespace・cluster-scoped policy・binding、またはAPI errorによる確認不能を変更前に停止する条件にしました。新しい実装例・テストコードは追加していません。必要な成果物とlive clusterで未確認の範囲は[具体化判断](MIGRATION_PLAN.md#container-005007の読み合わせと具体化判断)に記録しています。

確認結果：`make test`で2621件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。三つのshell構文と`git diff --check`も成功しました。使い捨ての`kubectl` mockでは、三つのscriptすべてで既存対象・API errorのどちらも変更前に終了することを確認しました。Live clusterの受付拒否、通信、資源制限は未確認です。

## 2026-09-28：CONTAINER-003・004の読み合わせ

CONTAINER-003のhost・node管理面とCONTAINER-004のruntime検知を照合しました。侵害が疑われるnode上のsensorによる「異常なし」は独立した健全性証拠にせず、node外の受信記録や管理面の状態と照合する条件を加えました。CONTAINER-004には診断項目を追加し、eventの対象ID欠落、sensor・配送障害、担当者の受領、無承認の破壊的対応を確認できるようにしました。

機械可読記録の製品横断の過剰な前提を本文へ揃え、NIST SP 800-190 §4.4.4のmappingを部分関係へ縮小しました。Falco・Sysdigの現行公開資料で、event fieldと転送方式が設定・製品によって異なることを確認しています。必要な成果物と実環境で未確認の範囲は[具体化判断](MIGRATION_PLAN.md#container-003004の読み合わせと具体化判断)に記録しました。新規実装・テストコードはありません。

確認結果：`make test`で2612件のローカルリンク、47 control ID、文書検査4件を確認し、エラー0件。Framework mappingはYAMLとして読み取れ、116件を保持しました。`git diff --check`も成功しました。Live node、sensor、配送、担当者の対応は未確認です。

## 2026-09-28：CONTAINER-001・002の読み合わせ

両control・設計・旧移行記録を照合し、registryの公開・保持とadmissionの使用許可を分けました。`deprecated`を一律の拒否と読める箇所を修正し、使用停止を決めたartifactの状態をconsumerへ渡す条件を補いました。OCI image indexと選択manifestのdigestが別であることを[OCI Image Index v1.1.1](https://github.com/opencontainers/image-spec/blob/v1.1.1/image-index.md)で確認し、使用先との照合を明示しました。

[CONTAINER-001](../controls/records/container-cloud-iac-security/psb-container-001-deployment-artifact-admission/learning.md)と[CONTAINER-002](../controls/records/container-cloud-iac-security/psb-container-002-container-registry-publication-boundary/learning.md)の教材をそれぞれの問いに分けて追加しました。GOV-005へ渡す新digestの公開、使用許可、稼働、旧digestの非稼働を区別しています。製品未選定の実装は追加していません。必要な成果物と未確認の範囲は[具体化判断](MIGRATION_PLAN.md#container-001002の読み合わせと具体化判断)に記録しています。

確認結果：`make check`で2594件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。Live registry、admission、runtimeは未確認です。

## 2026-09-28：GOV-002・005の読み合わせ

GOV-002のcontrol・機械可読記録・教材・設計と、GOV-005のcontrol・機械可読記録・設計を照合しました。旧YAML形式の必須化を外し、例外の対象・承認・期限・取消・評価不能という判断を残しています。GOV-005には別環境と切り戻し経路に旧digestが残る具体的な教材を追加し、GOV-003の元の期限、GOV-002の一時使用許可、GOV-005の復旧完了を区別しました。

GOV-003とGOV-005の例外consumer mappingを追加し、承認された例外でもfindingと旧digestの残存を消さない条件を明示しています。NIST SSDF 1.1・SP 800-61 Rev.3とOpenSSF Baseline 2026.02.19の公開ページを再確認しました。必要な成果物と実環境で未確認の範囲は[具体化判断](MIGRATION_PLAN.md#gov-002005の読み合わせと具体化判断)に記録しています。新規実装・テストコードはありません。

確認結果：`make check`で2563件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。例外の承認・取消、実際の使用拒否、置換後の旧digest非稼働は実環境で確認していません。

## 2026-09-28：GOV-001・003の読み合わせ

両control・設計とGOV-001の教材を照合し、GOV-003配下に具体的な場面から学ぶ教材を追加しました。問題の部品が見つかった製品と、閲覧権限や完成物の収集が不足する製品を分け、検索0件・取込通知・悪用情報の取得失敗を非該当や低優先度へ変換しない判断を示しました。GOV-001には診断項目を、GOV-003には再調査の担当・期限と暫定判断の条件を補いました。

GOV-001からGOV-003へ渡す対象・時点・根拠・不足情報を設計で明確にしました。FIRST CVSS v4.0仕様、NIST SSDF 1.1公開ページ、CISA管理のKEV配布mirrorを確認し、CISA本体catalogの内容・live取得は今回確認していません。必要な成果物と未確認の範囲は[具体化判断](MIGRATION_PLAN.md#gov-001003の読み合わせと具体化判断)に記録しています。新規実装・テストコードは追加していません。

確認結果：`make check`で2525件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。実環境での影響調査や優先度判断は行っていません。

## 2026-09-28：REL-003・004の読み合わせ

両control・既存教材・設計とCycloneDX限定実装を照合しました。REL-003の教材を「どこを調べて作ったSBOMか」から辿る説明へ改め、供給者や共通base imageのSBOMと最終製品の一覧の違いを補いました。利用者提供資料の固定原文、CycloneDXの生成段階、Dependency-Track 4.14.3の通知順を確認し、取込完了を脆弱性分析完了と扱わない設計へ修正しました。

実装READMEに最短導入手順、phaseの申告と実際の生成経路の違い、root・最上位componentに限る検査範囲を明記しました。既存9テストがPython 3.13.5で成功し、空白を含むパスへのコピー・正常例・上書き防止・配置先制限・成果物変更・入力不足を使い捨てrepositoryで確認しました。実装・テストコードは増やしていません。

旧check・framework関係は保持します。必要な成果物と実環境で未確認の範囲は[具体化判断](MIGRATION_PLAN.md#rel-003004の読み合わせと具体化判断)、資料の版と採否は[Sources](../sources/README.md#ref-release-sbom-lifecycle-001)に記録しています。

確認結果：`make check`で2493件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。実生成・公開・分析・供給者からの受入れは未確認です。

## 2026-09-28：REL-001・002・005の読み合わせ

三つのcontrol・既存教材・設計を照合しました。REL-001に診断項目を追加し、機械可読記録へ本文の外部パラメーター照合、取得・検証不能時の使用停止を反映。来歴の種類の確認と、検証後も同じ内容を使用する判断を補いました。

REL-002の教材はWindows版の利用者から配布経路を辿る説明へ書き直し、用語の列挙と本文の重複を減らしました。公開準備中の表示と実際の取得・使用制限を分けています。REL-005からは成果物署名、来歴の認証、利用者の期待値の違いを辿れるようにしました。一次資料はSLSA v1.2の検証・配布と、Sigstoreの公式署名・検証文書を確認しました。

旧check・参照資料・framework関係は保持し、文書と診断項目で完了としました。必要な成果物と実環境で未確認の範囲は[具体化判断](MIGRATION_PLAN.md#rel-001002005の読み合わせと具体化判断)に記録しています。

確認結果：`make check`で2466件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。実signer・配布先・使用経路での拒否試験は行っていません。

## 2026-09-28：BUILD-001〜003の読み合わせ

三つのcontrolと設計、既存二教材を照合しました。BUILD-001へ診断項目を追加し、機械可読記録のHTTPS固定・短い観測宣言を本文の特性へ揃えています。実行権限、承認手順、来歴情報の出所を分け、取得時に準備コードが動く境界も既存の依存実行設計へ接続しました。

BUILD-003には、正しい署名が付いていても記録の内容を誰が決めたか確認する教材を追加しました。基盤が入力を正確に記録することと、その入力での公開承認を区別し、domain入口・control・教材・設計を往復できるようにしています。SLSA v1.2の一次資料でL3のfield例外への参照を再照合し、以前の説明を補修しました。

今回は文書と診断項目を成果物に選び、製品未選定の実装や合成検証器は増やしていません。旧check・framework関係は保持します。必要な成果物と実環境で未確認の範囲は[具体化判断](MIGRATION_PLAN.md#build-001003の読み合わせと具体化判断)を参照してください。

確認結果：`make check`で2442件のローカルリンク、47 control IDを検査し、エラー0件。`git diff --check`も成功しました。文書・記録の整合性検査であり、実基盤での生成・隔離・拒否試験は実行していません。

## 2026-09-27：CICD-005・009・007の読み合わせ

三つのcontrol・既存教材、Untrusted PR boundaryとCI state and runner lifecycle、既存GitHub例を読みました。未信頼の内容を権限処理へ渡す経路、外部cache、同じrunnerに残る状態を分け、controlへ診断項目、教材と設計へ隣接する問いへのリンクを追加しました。Cacheとrunnerの機械可読記録に残った製品固有の条件も本文へ揃えています。

Cacheの取得範囲・key一致・job成功は内容の正しさとは別であり、runner名・登録解除・破棄記録は実体の破棄とは別だと説明しました。登録・破棄・外部ログを世代で追い、取消・破棄失敗・ログ不足を成功へ丸めない設計へ戻しています。データの形式・出所が正しくても、PR runの自己申告を独立した検査や公開承認へ置き換えません。

既存GitHub例にはcacheを使わない設定、push SHAのcheckoutと一致確認、最短copy・smoke test・解除を補いました。文書・ローカルcopy・構文・実Gitのrevision照合と、実GitHubの拒否・実runnerの世代別破棄を区別します。新しいcontrol・教材・実装は増やしていません。必要な成果物と確認範囲は[具体化判断](MIGRATION_PLAN.md#cicd-005009007の読み合わせと具体化判断)、一次資料は[cache資料](../sources/README.md#spec-ci-cache-boundary)と[runner資料](../sources/README.md#ref-cicd-014)へ記録しました。

## 2026-09-27：DEPS-002〜004の読み合わせ

三つのcontrol・既存教材、Install execution policyとReviewed dependency intake、既存pip・GitHub例を読みました。更新の採用、依存内容の照合、準備コードの実行許可を別の問いとして渡す構成へ補修し、各controlへ製品非依存の診断項目を追加しています。新しいcontrol・教材・実装は増やしていません。

Lockを書き換えないこととmanifestとの一致、取得時のhash照合と既存の展開済み環境、Actionの成功と必要な評価の完了を教材で区別しました。pipは新しい専用環境を使う導入と解除、GitHubは配置・必須検査への接続・データ不足・smoke test・解除を整理しました。固定Actionのsnapshot警告が期限後も判定を止めないことを、sourceと配布コードで照合しています。

確認した一次資料と観測版は[Sources](../sources/README.md#spec-install-execution-policy)、必要な成果物とローカル確認・実導入の境界は[具体化判断](MIGRATION_PLAN.md#deps-002004の読み合わせと具体化判断)へ記録しました。npm・uvの実行、実GitHubの取得・必須判定・merge拒否、採用先の全依存・platform・CI配線は今回の確認に含みません。

## 2026-09-27：SOURCE-002・003の読み合わせ

両control・patternと、Git / Gitleaks、Python pattern scanner、GitHub indicator watchの既存コード・READMEを読みました。検査場所の違いと検索後の判断を説明する教材を各controlへ置き、入口、機械可読記録、設計と実装から相互にたどれるようにしました。

SOURCE-002の未検証という表記を、ローカルの代表実装と実導入へ分けました。SOURCE-003は候補0件だけで完了と判断しない説明、診断項目の問い、投稿単位の重複抑制の限界を明確にしています。既存Python版のmerge時の検査漏れは修正前に再現し、修正後8件、監視は模擬HTTPで6件の既存テストを確認しました。Git / Gitleaksの再実行、実GitHubと組織での導入・対応は含みません。必要な成果物と残る判断は[計画](MIGRATION_PLAN.md#source-002003の読み合わせと具体化判断)へ記録しました。

## 2026-09-27：移行状況と教材への導線

[三領域の索引](MIGRATION_CANDIDATES.md)を現在の成果物へ照合しました。SOURCE-001・002、DEPS-002〜004、CICD-006・007・009の古い「候補・保留」を補修し、SOURCE-003の限定実装とCICD-003の既存controlへの配置も反映しています。旧19件のうち対象内18件は主な問いの行き先があり、DEPS-005は別PJの範囲です。旧実装全体の移植・導入完了という判定にはしません。

全47 controlについて、全体一覧・domainの入口・設計へのリンクを照合しました。全体一覧から漏れていたIAC-001を追加し、Domain一覧と同じ分野順・ID順へ揃えています。Detection / Verificationの概要へDETECT-003も反映しました。

既存39教材はcontrolから読め、教材から元のcontrolと設計へ戻れます。三領域では既存15教材への直接リンクを一覧に追加しました。SOURCE-002・003は独立教材がないため、その状態を示し、controlと設計を入口にしています。教材の数を揃えるための新設はしません。

次作業への案内を移行計画へ揃え、現在件数の重複記載と「将来実装する」とだけ記した古い案内を補修しました。以下の初回レビューや日付付きの記録は経緯として保持します。今回の確認は索引・配置・リンクと、状態表記に関する執筆者のレビューです。全教材・実装の意味的レビュー、利用者による読書評価、製品の現行性、実環境への導入は含みません。

## 結論と範囲

2026-09-17時点で、Build、consumer、Application、Operationsの四種類について、
control・教材・pattern・実装を別の更新単位へ分ける構造を維持します。
ただし、これは執筆者による読み通し・構造検査であり、独立した利用者テストやセキュリティ監査ではありません。

初回レビューではcontrolを追加せず、12件の記録と11patternを入口で整理しました。その後GOV-001、GOV-002、DETECT-001、AI-002を追加しました。2026-09-20にAI-004の設計部分を先行移行し、その時点で17件の記録と17patternになりました。AI-004のcontrol記録を追加しました。操作認可に続き、開発用実行環境の隔離を設計資料へ分離しました。

## 四種類で確認した境界

| 主題 | 判断の正本 | 実装・検証の状態 | 残る境界 |
|---|---|---|---|
| [Build](../engineering/build-security/build-execution-boundary/README.md) | 実行コードへ渡す権限、外側の通信・隔離、観測 | ガイダンス。旧JSON計画検査は保留 | 実sandbox・通信拒否・sensorは未確認 |
| [Consumer](../engineering/release-integrity/consumer-artifact-acceptance/README.md) | 同一性・認証・利用者の期待値・使用gate | ガイダンス。旧crypto fixtureは公開鍵欠落等で保留 | 実署名・失効・使用gateは未確認 |
| [Application](../engineering/secure-design/object-access-boundary/README.md) | 主体・対象・操作・tenantを使う認可設計 | PSB-DESIGN-001、SQLite限定実装、7テスト | HTTP認証、全endpoint、並行処理、組織導入は未確認 |
| [Operations](../engineering/container-cloud-iac-security/runtime-detection-to-triage/README.md) | 検知・観測障害・配送・対象・担当者・独立承認 | ガイダンス。旧synthetic adapterは保留 | Live sensor、通知、対応、PSIRT能力は未確認 |

教材は具体的なシナリオから誤解を解き、patternは方式・責任・代償を選ぶ材料とします。
同じ概念が現れても全文を統合せず、この役割分担と正本へのリンクを維持します。
「検証成功だけで安全とは言えない」のような一般論を別ファイルへ切り出さず、具体的なシナリオと問いがある教材の中で扱います。

## 修正した不一致

- ファイルリンクが存在していてもSources内の短いID anchorが欠けていた6リンクを修正。
- Application・Operations・攻撃段階9／11の集約を最新成果物と一致させた。直接対応は文書が保証目標を扱う意味で、導入済みではない。
- Control・engineering索引を一つの一覧へ整理。CacheとRunner、Buildとconsumer、CI観測と本番監視を別の境界として維持。
- 初期三件のpilotと追加の構造検証を区別し、過去の「次に作業する」という案内を最新状態へ更新。

## 引き続き残す制限

初回検査: YAML parse、当時12件のID一意性とcontrol索引、ローカルMarkdownのファイル・見出しanchor、
`git diff --check`を確認。SQLiteの7テストも再実行して成功しました。
これらは構造と限定実装の確認であり、全本文の正確さや本番導入を保証する検査ではありません。

Sourcesに保留・取得失敗・mutable版の記録がある資料は、現在の仕様へ再確認済みと読み替えません。
Framework mappingは旧版・ID・関係を保持した移行レビュー中の関係です。PSB-DESIGN-001のexact ASVS mappingは未追加です。
初回レビュー時は旧ツリーへの相対参照が独立化を妨げていました。2026-09-21に固定コミットへの外部参照へ変更し、[単独検査](REPOSITORY_CUTOVER.md)を追加しました。2026-09-22には本PJを正本とする公開先が確定しました。独立化の範囲と残る運用判断は[Repository cutover](REPOSITORY_CUTOVER.md)を参照してください。
全legacy実装の意味的レビュー、全参照仕様の現在の有効性、独立した読者による理解度確認は未完了です。

## 2026-09-20の横断補修

- DETECT-001の旧fixtureに関する根拠を`legacy_rationale`へ分け、現在のガイダンスとの関係と未検証範囲を記載。
- 候補一覧・横断分析の移行済み／未移行を更新。過去の作業順序は履歴と明記。
- GOV-002の設計上の接続先をDependencyの2件とDETECT-001の計3件へ統一。
- Scanner設計本文の日英混在を補修。これは全資料の文章校正完了を意味しない。
- [Development action authorization](../engineering/ai-development-security/development-action-authorization/README.md)と教材を追加。AI-004の認可部分のみの再編集で、control全体・製品実装・framework mappingは未移行。

レビューは内部整合性を対象とし、外部仕様全体の現行性や実環境の導入は検証していません。新規資料で確認した外部資料の範囲はSourcesに記載します。

補修後の確認：YAML 20件の構文、control ID 16件の一意性、設計パターン16件、framework mapping 62件の旧版・ID・関係・confidenceの保持、property参照、ローカルMarkdownリンク761件のファイルと見出し、`git diff --check`を確認しました。コード・製品設定は変更していないため、実装テストや実環境の認可試験は実行していません。

## 追加移行と受け渡しのレビュー記録

[Security scope](SECURITY_SCOPE.md)により、AI-004は開発環境に限定します。製品自体のAI securityはai-security-foundryの担当であり、移行待ちとして補完しません。

追加batchで[PSB-GOV-001](../controls/records/governance-operations/psb-gov-001-supply-chain-impact-assessment/README.md)をガイダンス移行しました。
Runtimeの対象identityから、SBOM・build・artifact・稼働deploymentへ影響調査を渡す境界を再編集しました。
「該当なし」と「inventory不完全」、対応計画と実対応、PSIRTの組織能力を分けることが受入条件です。

端末隔離・認証情報・通信制限は[Development runtime isolation](../engineering/ai-development-security/development-runtime-isolation/README.md)へ移行し、Source Protection・Build・runner・操作認可との責任分界を示しました。AI-004は[全26項目の対応表](AI_RUNTIME_MIGRATION.md)、10特性のcontrol記録、旧15件のframework関係を整理し、2026-09-21にAI-002との失効時の受け渡しを補修しました。

続いてSOURCE-001を[29項目の対応表](ENDPOINT_MIGRATION.md)へ棚卸しし、[Managed developer endpoint](../engineering/source-protection/managed-developer-endpoint/README.md)を追加しました。登録・現在の観測・業務アクセスを分け、11項目の設計を先行移行しています。端末管理範囲のcontrol記録と旧4件のframework関係の照合は、このレビュー時点で残っています。認証情報・実行隔離・公開防止を一つへ再集約しません。製品設定を移す場合のみ現行仕様と実際の拒否挙動を確認します。Domainを一つずつ全件移す方式へ戻しません。
この記録は追加の依存や実環境での操作を承認するものではありません。次作業の優先順位は移行計画で管理します。
