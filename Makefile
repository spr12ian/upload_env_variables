# Makefile to source setup_development_environment.source

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

SCRIPT := setup_development_environment.source

.PHONY: help source-env

help: ## Show available targets
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS=":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

source-env: ## Source the setup script in a new shell
	@echo "🔧 Sourcing $(SCRIPT)..."
	@bash -c 'source ./$(SCRIPT) && exec $$SHELL'
	@echo "✅ Environment setup complete."
