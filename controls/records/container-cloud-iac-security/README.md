# Container / Cloud / IaC Security

実行前の設定と許可、hostの境界、実行後の観測を分けて判断します。

| Control | 問うこと |
|---|---|
| [PSB-CONTAINER-001 Deployment artifact admission](psb-container-001-deployment-artifact-admission/README.md) | 実行する全artifactを現在のconsumer acceptanceへ結び、全経路でfail closedにできるか |
| [PSB-CONTAINER-002 Container registry publication boundary](psb-container-002-container-registry-publication-boundary/README.md) | 公開権限、digest identity、変更防止、audit、withdrawalをregistryで維持できるか |
| [PSB-CONTAINER-004 Runtime threat detection](psb-container-004-runtime-threat-detection/README.md) | どのworkloadの行動を観測し、観測障害と検知を区別して担当者へ渡せるか |

Workload confinement、host、IaCは未移行です。Admissionとregistryは設計移行であり、live platform実装は未確認です。
