# Workflow dependency identityの移行判断

旧[PSB-CICD-001](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/action-sha-pinning/control.yaml)を、直接参照の固定、更新レビュー、内側の追加取得、受入経路へ再編集しました。移行元は`product-security-controls@f42987759218c9b8daf3924320542a1935ef78e0`、確認日は2026-09-27です。旧packageの全fileが固定revisionと一致することを確認しました。

## 旧項目の行き先

| 旧項目 | 行き先・判断 |
|---|---|
| ACT-001 | [WORKFLOW-REF-1・3](../controls/records/cicd-security/psb-cicd-001-workflow-dependency-identity/README.md)：外部Actionを確認したcommitへ固定する。40桁の構文はGitHub実装へ分ける |
| ACT-002 | WORKFLOW-REF-1・3：外部reusable workflowの呼出先を固定し、変更をreviewする。GitHubのAction SHA policyだけで済ませない |
| ACT-003 | WORKFLOW-REF-2：直接のcontainer Actionをdigestへ結ぶ。GitのSHA固定とimageの固定を区別する |
| ACT-004 | WORKFLOW-REF-1・2・5：tag、branch、短いSHA、計算式と検査範囲の抜けを受け入れない |
| ACT-005 | WORKFLOW-REF-5：壊れた入力、未検査、tool障害を成功にしない。終了値の数値は実装へ置く |
| ACT-007 | WORKFLOW-REF-3・4：固定commitで読んだsource・実行時取得と未確認を更新reviewへ残す。直接参照の成功から結果を導出しない |

旧項目は6件です。欠番ACT-006を新規に埋めません。旧`NO_OBVIOUS_MUTABILITY`は確認範囲を限定する結果で、依存全体の固定や無害性の証明にはしません。教材では状態名より先に、何を確認したかを日本語で示します。

## 具体化判断と実装の変更

Control、control配下の教材、設計pattern、診断観点を必要な成果物としました。直接参照の形式は低いコストで実検査できるため、[Python / GitHub実装](../engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs/README.md)の導入・smoke test・解除も完了条件へ含めました。技術経路が明確な検査を文書だけへ留めず、組織の導入済み判定を作る合成JSONは追加しません。

旧[Python verifier](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/cicd-security/action-sha-pinning/scripts/verify.py)は標準libraryの正規表現で行ごとの`uses:`を読みます。YAML構造は解析せず、参照以外の文字列と実参照を区別する範囲や、構文不正の扱いに限界があります。そのままcopyせず、PyYAML 6.0.3のnode treeを読み、jobのreusable呼出しとstepのAction呼出しに限定しました。Python objectの構築・workflow実行・通信・書換えは行いません。

この判断にはparser依存の取得・hash管理という代償があります。参照は構造から読み、重複key・merge key・custom tag・循環aliasはerrorにします。Flow形式、引用key、折畳みscalar、普通のaliasを検査します。`run`だけの正当なworkflowは対象を読めた参照数ゼロとして認め、旧「usesなしは一律error」を変更しました。空入力・入力不足と同一視しません。

pinact v4.1.1は任意の修正補助として残し、版・source commit・archive checksumを保持しました。Toolの追加wrapper、自動commit、cooldown、reviewdog、全依存の自動解決は作りません。Docker参照の処理をpinactから外しても、直接参照の検査には含めます。固定後の内部取得は教材とpatternのreviewへ渡します。

今回の実測はLinux x86_64 / Python 3.10.4 / PyYAML 6.0.3のhash付き導入とローカルCLIの12件です。成功・可変参照の拒否・YAML不正等のerror、参照形式、全指定対象、非変更、依存不足を確認しました。採用先へcopyする導入とsmoke testも使い捨てdirectoryで確認しました。PinactのLinux archive SHA-256、binary版・helpを確認しています。実APIによる自動修正、remote SHA・release・出所、実Actionの内容・追加取得、GitHub上のcheck・policy・review・迂回拒否、macOSは未確認です。本PJ自体には`.github/workflows`がなく、その入力はerrorになりました。

実装からcontrol・patternへ戻した境界は、構文と出所の違い、Action policyとreusable呼出しの違い、検査対象内のゼロと入力不足の違い、検査script自身の改変、直接参照と内部取得の違いです。組織への方針適用はSOURCE-006、jobの実効権限は旧CICD-004の次の主題へ渡します。

## 旧framework関係と資料の採否

旧レビュー日は2026-09-01です。以下の3関係を履歴として保持します。今回exact仕様項目へのproperty割当を再審査していないため、新しいframework mappingへ自動継承しません。116件を維持します。

| 旧framework・版 | 旧IDと関係 | 旧適用項目 |
|---|---|---|
| GitHub `github/docs@b17436de8f10c3e7f6a185d6813bf94bc82d22f8`（2026-07-24） | GHAS-REF-SECURE-USE：supports / high | ACT-001・002・004 |
| MITRE ATT&CK v19.1 | T1195.001：mitigates / medium | ACT-001〜004 |
| NIST SSDF 1.1（SP 800-218, 2022） | PW.4.1：supports / medium | ACT-001〜004・007 |

一次資料は現在のGitHub secure use・workflow構文・Actions policy、Docker digest仕様へ置き直し、可変Web文書の確認日と再確認条件を[Sources](../sources/README.md#spec-workflow-dependency-references)へ残します。旧READMEが参照するPalo Alto NetworksのUnpinnable Actionsは内部取得の問題を知る履歴として保持し、調査中の比率や全ecosystemへの一般化を新controlの根拠にしません。旧`REF-CICD-001`（Advisory Database）は版と脆弱性の照合に関する隣接課題、旧`REF-CICD-005`（講演）は既存の調査入力として残し、今回の直接参照検査が脆弱性分析まで行うとはしません。新資料IDは役割に合わせ、旧IDを別名として登録しません。
