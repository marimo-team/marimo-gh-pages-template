# This file contains commands for setting up the environment, formatting code,
# building the book, and other maintenance tasks.

.DEFAULT_GOAL := help

# Install uv and uvx
uv:
	@curl -LsSf https://astral.sh/uv/install.sh | sh

# Display help information about available make targets
.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort

# Install and run Marimo for interactive notebooks
.PHONY: marimo
marimo: uv ## Install Marimo and start server to edit marimo notebooks
	@uvx marimo edit --sandbox notebooks/$(NOTEBOOK).
