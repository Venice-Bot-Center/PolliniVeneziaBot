.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Make venv and install requirements
	@mkdir -p .venv
	@uv sync
	@uv run --env-file .env --env-file=.env pre-commit install
	@pre-commit autoupdate

.PHONY: flake8
flake8: ## Flake8
	@uv run --env-file .env flake8

test: flake8 ## Make test

.PHONY: update
update: ## Update requirements
	@uv sync
	@uv update
	@uv run --env-file .env pre-commit autoupdate


patch: ## Increment patch
	@uv version --bump patch

minor: ## Increment minor
	@uv version --bump minor

major: ## Increment major
	@uv version --bump major

alpha: ## Increment alpha
	@uv version --bump alpha

beta: ## Increment beta
	@uv version --bump beta

stable: ## Increment stable
	@uv version --bump stable

dev: ## Increment dev
	@uv version --bump dev

precommit: ## Run pre-commit hooks
	@git add . & uv run --env-file .env pre-commit run --all-files


deploy: ## make the deploy code
	@uv export --no-hashes --format requirements-txt > requirements.txt

run: ## run the script
	@uv run --env-file .env python main.py
