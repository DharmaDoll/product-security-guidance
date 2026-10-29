PYTHON ?= python3

.PHONY: check test test-examples test-agent-deadline test-repository-recovery test-workflow-refs
check:
	$(PYTHON) scripts/check_docs.py

test: check
	$(PYTHON) -m unittest discover -s scripts -p 'test_*.py' -v

# Runs local example tests, including pip in a temporary offline environment.
test-examples:
	$(PYTHON) -m unittest discover -s engineering/implementations/pip-install-policy/tests -v
	$(PYTHON) -m unittest discover -s engineering/implementations/cyclonedx-artifact-binding -p 'test_*.py' -v
	$(PYTHON) -m unittest discover -s engineering/implementations/python-unicode-source-review -p 'test_*.py' -v

# Secret-check implementation tests are maintained in agent-control-plane/skills/secret-checks.

# Use the implementation's pinned PyYAML 6.0.3 environment; tests are offline.
test-workflow-refs:
	$(PYTHON) -m unittest discover -s engineering/implementations/python-workflow-refs -p 'test_*.py' -v

# Requires Linux and GNU coreutils 9.7; uses only local disposable processes.
test-agent-deadline:
	$(PYTHON) -m unittest discover -s engineering/implementations/linux-agent-deadline -p 'test_*.py' -v

# Requires Git; restores only local disposable repositories, without network.
test-repository-recovery:
	$(PYTHON) -m unittest discover -s engineering/implementations/git-mirror-recovery -p 'test_*.py' -v
