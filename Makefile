# Use base Makefiles from ska-cicd-makefiles repository
include .make/base.mk
include .make/python.mk

# Define variables
PYTHON_LINT_TARGET := ./src ./main.py
PYTHON_SWITCHES_FOR_PYLINT = --disable=W1203

# Note:
# PYTHON_VARS_AFTER_PYTEST are defined in pyproject.toml
# [tool.pytest.ini_options], addopts

# Run pre-commit checks
pre-commit:
	@python -m mypy src
	make python-format
	make python-lint
	make python-test
