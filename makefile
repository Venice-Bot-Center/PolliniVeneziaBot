.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the stuff
	@uv sync
	@uv run pre-commit install
	@uv run pre-commit autoupdate

.PHONY: flake8
flake8: ## Flake8
	@uv run flake8

test: flake8 ## Make test

run: ## Run cron
	@uv run python start.py


.PHONY: update
update: ## Update requirements
	@uv sync
	@uv update
	@uv run pre-commit autoupdate


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
	@git add . & uv run pre-commit run --all-files


deploy: ## make the deploy code
	@uv export --no-hashes --format requirements-txt > requirements.txt
