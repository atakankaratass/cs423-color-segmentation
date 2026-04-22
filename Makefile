.DEFAULT_GOAL := help

.PHONY: help install-dev format format-check lint test smoke-test validate-pr evaluate-rgb evaluate-hsv run-experiments

help:
	@echo "Available targets:"
	@echo "  make install-dev   - Install Python and Node development dependencies"
	@echo "  make format        - Format Python and supported text files"
	@echo "  make format-check  - Verify formatting"
	@echo "  make lint          - Run Ruff lint checks"
	@echo "  make test          - Run pytest"
	@echo "  make smoke-test    - Run CLI smoke test"
	@echo "  make validate-pr   - Run the full pre-PR validation suite"
	@echo "  make evaluate-rgb  - Evaluate the bundled sample dataset with the RGB profile"
	@echo "  make evaluate-hsv  - Evaluate the bundled sample dataset with the HSV profile"
	@echo "  make run-experiments - Evaluate all bundled profiles and write a summary"

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

evaluate-rgb:
	PYTHONPATH=src python3 -m cs423_segmentation evaluate --metadata data/sample/metadata/dataset.json --profile rgb_red --output results/tables/rgb-sample-results.json

evaluate-hsv:
	PYTHONPATH=src python3 -m cs423_segmentation evaluate --metadata data/sample/metadata/dataset.json --profile hsv_red --output results/tables/hsv-sample-results.json

run-experiments:
	PYTHONPATH=src python3 -m cs423_segmentation run-experiments --metadata data/sample/metadata/dataset.json --output results/tables/experiment-summary.json

validate-pr:
	npm run validate:push
