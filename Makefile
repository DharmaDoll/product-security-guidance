PYTHON ?= python3

.PHONY: check test test-examples test-secret-hooks test-python-secret-hooks test-agent-deadline test-repository-recovery test-workflow-refs
check:
	$(PYTHON) scripts/check_docs.py

test: check
	$(PYTHON) -m unittest discover -s scripts -p 'test_*.py' -v

# Runs local example tests, including pip in a temporary offline environment.
test-examples:
	$(PYTHON) -m unittest discover -s engineering/dependency-security/install-execution-policy/implementations/pip/tests -v
	$(PYTHON) -m unittest discover -s engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner -v
	$(PYTHON) -m unittest discover -s engineering/release-integrity/release-sbom-identity-and-analysis/implementations/cyclonedx-artifact-binding -p 'test_*.py' -v
	$(PYTHON) -m unittest discover -s engineering/secure-coding/unicode-source-review/implementations/python -p 'test_*.py' -v

# Requires a separately verified Gitleaks binary; creates only temporary repositories.
test-secret-hooks:
	$(PYTHON) -m unittest discover -s engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks -v

test-python-secret-hooks:
	$(PYTHON) -m unittest discover -s engineering/source-protection/secret-checks-before-publication/implementations/python-pattern-scanner -v

# Use the implementation's pinned PyYAML 6.0.3 environment; tests are offline.
test-workflow-refs:
	$(PYTHON) -m unittest discover -s engineering/cicd-security/reviewed-workflow-dependency-binding/implementations/python-workflow-refs -p 'test_*.py' -v

# Requires Linux and GNU coreutils 9.7; uses only local disposable processes.
test-agent-deadline:
	$(PYTHON) -m unittest discover -s engineering/ai-development-security/development-work-budget-gate/implementations/linux-timeout -p 'test_*.py' -v

# Requires Git; restores only local disposable repositories, without network.
test-repository-recovery:
	$(PYTHON) -m unittest discover -s engineering/source-protection/independent-repository-backup-and-restore/implementations/git-mirror -p 'test_*.py' -v
