# Use base Makefiles from ska-cicd-makefiles repository
include .make/base.mk
include .make/python.mk

# Define variables
PYTHON_LINT_TARGET := ./src ./main.py
PYTHON_SWITCHES_FOR_PYLINT = --disable=W1203