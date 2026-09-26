# PSB-CODE-005 Unicode source deceptionの移行

## 何を分けたか

旧[PSB-CODE-005](https://github.com/DharmaDoll/product-security-controls/tree/f42987759218c9b8daf3924320542a1935ef78e0/controls/secure-coding/unicode-source-deception)の6項目を、[control](../controls/records/secure-coding/psb-code-005-unicode-source-review/README.md)、[教材](../controls/records/secure-coding/psb-code-005-unicode-source-review/learning.md)、[pattern](../engineering/secure-coding/unicode-source-review/README.md)、[Python実装](../engineering/secure-coding/unicode-source-review/implementations/python/README.md)へ再編集した。守る資産は、人が承認したソースと処理系が読むソースの対応である。

| 旧項目 | 新しい置き場 | 判断 |
|---|---|---|
| `UNI-001` 双方向制御文字 | `UNICODE-SOURCE-2`、Python実装 | 検出対象として保持。全言語・全contextでの一律拒否は一般要件にしない |
| `UNI-002` 不可視文字・tag | `UNICODE-SOURCE-2`、Python実装 | 位置とcode pointを見せる。旧拒否リストの一部を狭いPython profileへ保持 |
| `UNI-003` ASCII識別子 | `UNICODE-SOURCE-3`、Python実装 | Python例の選択条件。多言語識別子を使うprojectの一般要件にしない |
| `UNI-004` NFKC-stable識別子 | `UNICODE-SOURCE-3`、Python実装 | Python parserの比較規則を踏まえ、元の綴りをtokenで見る |
| `UNI-005` 不正入力・構文・対象漏れ | `UNICODE-SOURCE-1/5`、Python実装 | 評価不能を合格にしない。対象pathと受入revisionの一致は採用先で確かめる |
| `UNI-006` 証拠の最小化 | `UNICODE-SOURCE-5`、Python実装 | 行・列・code point・分類のみ。ソース本文をログに出さない |

## 具体化判断

この主題は実ソースの文字とPythonのtokenを直接読めるため、限定実装に価値がある。旧`scripts/verify.py`とJSON policyをそのままコピーせず、標準ライブラリのみの小さなscannerへ再編集した。UTF-8宣言、対象ゼロ件、symlink、読取不能、構文エラーを評価不能とし、双方向・不可視文字、ASCII識別子、NFKC差分を一時ファイルで確認する。検査対象のコードは実行しない。

旧`materialize_fixture.py`とescaped fixtureは移植しない。新しいtestは一時ファイル内でcode pointを生成し、正常・拒否・評価不能の経路を観測できる。危険な文字を含むソースファイルを恒久的なfixtureとして増やす必要はない。

実装はPython 3.10.4のUTF-8 sourceと、識別子ASCII限定のproject profileに絞る。UTS #55は双方向文字の一律禁止を推奨しておらず、表示環境の改善も重要とするため、旧profileをcontrol全体へ拡大しない。Unicode confusableの網羅検出、review UI、protected CI、言語別の例外は未実装である。実repositoryの採用とmerge拒否も未確認。

## 参照とmapping

- [UTS #55 Version 2](../sources/README.md#spec-unicode-source-handling-2)、[UTS #39 Version 18.0.0](../sources/README.md#spec-unicode-security-mechanisms)、[Python 3.10字句規則](../sources/README.md#spec-python-source-lexical-3-10)を2026-09-26に確認。
- 旧SITF `T-E011`の`mitigates / high`は今回継承しない。SITFは攻撃技法の分類であり、狭いPython検査やcontrol記録が技法全体を高い確度で緩和した証拠にはならない。旧関係は[旧control](https://github.com/DharmaDoll/product-security-controls/blob/f42987759218c9b8daf3924320542a1935ef78e0/controls/secure-coding/unicode-source-deception/control.yaml)に保持する。
- 横断分析では主にApplication layerと、source repositoryの変更受入段階を扱う。CIでの実行とbuildは受け渡しであり、CODE-005がCIやbuildの安全性を証明するわけではない。

Secure Coding domainはこの一例で網羅しない。次の主題を進める場合も、認証・入力処理等の固有の直接失敗から選ぶ。
