.DEFAULT_GOAL := help

.PHONY: help install-dev format format-check lint test smoke-test validate-pr

help:
	@echo "Available targets:"
	@echo "  make install-dev   - Install Python and Node development dependencies"
	@echo "  make format        - Format Python and supported text files"
	@echo "  make format-check  - Verify formatting"
	@echo "  make lint          - Run Ruff lint checks"
	@echo "  make test          - Run pytest"
	@echo "  make smoke-test    - Run CLI smoke test"
	@echo "  make validate-pr   - Run the full pre-PR validation suite"

install-dev:
	python3 -m pip install -r requirements-dev.txt
	npm install

format:
	npm run format

format-check:
	npm run format:check

lint:
	npm run lint

test:
	npm run test

smoke-test:
	npm run smoke-test

validate-pr:
	npm run validate:push
