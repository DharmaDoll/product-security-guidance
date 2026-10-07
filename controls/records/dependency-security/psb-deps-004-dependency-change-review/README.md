# PSB-DEPS-004 Dependency change review

**今回の変更で入る依存を把握し、採用できない変更をマージ前に止められるか。**

例えば、直接依存を一つ更新しただけでも、その先の依存が増えたり別の版に変わったりします。長いlockfileの差分を見落とすと、採用を判断していない依存が製品へ入ります。

## 満たすべきこと

1. **現在の差分を見せる。** 比較するbaseとheadに対し、直接・推移依存の追加・更新・削除、版、利用範囲、対応するmanifestを確認できるようにする（DEP-REVIEW-1）。Headやbaseが変われば、古い結果で判断しない。
2. **採用方針で判断する。** 何を拒否するかを明示し、拒否対象を警告付きの成功に変えない（DEP-REVIEW-2）。既知の脆弱性だけを判定する場合は、その範囲を明らかにする。
3. **評価が終わるまでマージさせない。** 現在の変更に対する必須判定をマージ条件にする（DEP-REVIEW-3）。データ不足、検査の失敗・取消・省略を「問題なし」と扱わない。検査の成功表示だけから、必要な評価が完了したと推測しない。

<a id="failure-checks"></a>

## 診断で確認する項目（異常時テスト）

- 推移依存だけを追加・更新・削除したとき、現在の差分に現れるか。
- Head更新やbaseの進行後、古い比較結果や承認だけでマージできないか。
- 対応外のmanifestや部分的なデータ取得を、依存変更なしとして扱わないか。
- 拒否対象が警告だけで通る、または利用範囲の誤分類で判定を逃れないか。
- 検査の失敗・取消・省略、判定方針や必須条件の弱体化、同名の別検査によってマージ条件を迂回できないか。

これらは診断・設計レビューの確認項目です。依存の実行や、実際のマージ拒否を確認した結果ではありません。

## このコントロールの範囲

対象は今回の依存変更の採用判断です。既存の必須SCA検査が同じ差分・方針・マージ拒否を満たすなら、別のツールを増やす必要はありません。既知の脆弱性を止めても、未公開の脆弱性や悪意あるpackageをすべて見つけたことにはなりません。承認後に使うファイルの同一性は[DEPS-003](../psb-deps-003-dependency-artifact-identity/README.md)、install時のコード実行は[DEPS-002](../psb-deps-002-install-execution-policy/README.md)へ渡します。未変更の依存の継続監視も別の判断です。

比較、判定、マージ条件のつなぎ方は[engineering](../../../../engineering/dependency-security/reviewed-dependency-intake/README.md)を参照してください。[GitHub実装例](../../../../engineering/dependency-security/reviewed-dependency-intake/implementations/github/README.md)は対象と判定範囲を限定しています。[教材](learning.md)、特性IDと旧項目の対応を残した[control.yaml](control.yaml)、採否を示す[Sources](../../../../sources/README.md#ref-deps-002)、部分的な[framework mapping](../../../../mappings/frameworks.yaml)へも辿れます。
