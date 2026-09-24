PYTHON ?= python3

.PHONY: check test test-examples test-secret-hooks
check:
	$(PYTHON) scripts/check_docs.py

test: check
	$(PYTHON) -m unittest discover -s scripts -p 'test_*.py' -v

# Runs local example tests, including pip in a temporary offline environment.
test-examples:
	$(PYTHON) -m unittest discover -s engineering/secure-design/object-access-boundary/implementations/python-sqlite -v
	$(PYTHON) -m unittest discover -s engineering/dependency-security/install-execution-policy/implementations/pip/tests -v

# Requires a separately verified Gitleaks binary; creates only temporary repositories.
test-secret-hooks:
	$(PYTHON) -m unittest discover -s engineering/source-protection/secret-checks-before-publication/implementations/git-gitleaks -v
