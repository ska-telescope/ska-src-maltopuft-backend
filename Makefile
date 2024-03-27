# Use base Makefiles from ska-cicd-makefiles repository
include .make/base.mk
include .make/docs.mk
include .make/python.mk

# Define variables
PYTHON_LINT_TARGET := ./src ./main.py
PYTHON_SWITCHES_FOR_PYLINT = --disable=W1203

# Note:
# PYTHON_VARS_AFTER_PYTEST are defined in pyproject.toml
# [tool.pytest.ini_options], addopts

# Doc builds with ska template will fail because core deps
# (not just doc deps) are required for package auto-summary
# documentation. Therefore ensure all deps required for the
# build are installed first.
docs-pre-build:
	poetry install --with docs --no-root

# Run pre-commit checks
pre-commit:
	@python -m mypy src
	make python-format
	make python-lint
	make python-test
	make docs-build html
