# This file contains commands for setting up the environment, formatting code,
# building the book, and other maintenance tasks.

.DEFAULT_GOAL := help

# Install uv and uvx
uv:
uv:
	@which uv > /dev/null || (curl -LsSf https://astral.sh/uv/install.sh | sh > /dev/null 2>&1)

# Display help information about available make targets
.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort

# Install and run Marimo for interactive notebooks
.PHONY: notebook
notebook: uv ## Export one notebook with NOTEBOOK=...
	@mkdir -p _site/notebooks/$(NOTEBOOK)
	@uvx marimo export html-wasm --sandbox notebooks/$(NOTEBOOK).py --mode edit -o _site/notebooks/$(NOTEBOOK)

# Export all notebooks to HTML-WASM
.PHONY: all-notebooks
all-notebooks: ## Export all notebooks to HTML-WASM
	@for notebook in notebooks/*.py; do \
		filename=$$(basename "$$notebook" .py); \
		echo "Exporting $$notebook to HTML-WASM..."; \
		echo $$filename; \
		$(MAKE) notebook NOTEBOOK=$$filename; \
	done

# Install and run Marimo for interactive notebooks
.PHONY: app
app: uv ## Export one app with APP=...
	@mkdir -p _site/apps/$(APP)
	@uvx marimo export html-wasm --sandbox apps/$(APP).py --mode run --no-show-code -o _site/apps/$(APP)

# Export all apps to HTML-WASM
.PHONY: all-apps
all-apps: ## Export all apps to HTML-WASM
	@for app in apps/*.py; do \
		filename=$$(basename "$$app" .py); \
		echo "Exporting $$app to HTML-WASM..."; \
		echo $$filename; \
		$(MAKE) app APP=$$filename; \
	done

# Build the website locally (dry run) without deploying to GitHub Pages
.PHONY: dryrun
dryrun: ## Build the website locally using the same process as CI/CD but publish to a local folder
	@echo "Building website locally (dry run)..."
	@mkdir -p _site/assets

	$(MAKE) all-notebooks
	$(MAKE) all-apps

	@echo "Copying assets..."
	@cp -r apps/public/logo.png _site/assets/logo.png

	@echo "Generating index.html..."
	@cp .github/workflows/index_template.html _site/index.html

	@echo "Website built successfully! Open _site/index.html in your browser to view it."
