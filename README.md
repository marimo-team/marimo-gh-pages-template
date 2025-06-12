# 🚀 marimo WebAssembly + GitHub Pages Template

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Deployed-green?logo=github)](https://pages.github.com/)
[![Marimo](https://img.shields.io/badge/marimo-0.13.15+-orange.svg)](https://marimo.io)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Enabled-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![UV](https://img.shields.io/badge/UV-Package%20Manager-blueviolet)](https://github.com/astral-sh/uv)

This template repository demonstrates how to export [marimo](https://marimo.io) notebooks to WebAssembly and 
deploy them to GitHub Pages. Marimo is an interactive Python notebook that combines the flexibility 
of a notebook with the reproducibility of a script.

## 🧰 Prerequisites

- Python 3.12 or higher
- GitHub account (for deployment)

## 📚 Included Examples

- **`apps/charts.py`**: Interactive data visualization dashboard with Altair charts. This app is exported in "run" mode, which hides the code and presents a clean user interface.
- **`notebooks/fibonacci.py`**: Interactive Fibonacci sequence calculator with a slider to adjust the number of sequence elements. This notebook is exported in "edit" mode, allowing users to modify the code.
- **`notebooks/penguins.py`**: Interactive data analysis of the Palmer Penguins dataset using Polars and marimo. Demonstrates data loading, filtering, and visualization.

## 🚀 Deployment

### Automatic Deployment with GitHub Actions

1. Fork this repository
2. Add your marimo files to the `notebooks/` or `apps/` directory
3. Push to the main branch
4. Go to repository **Settings > Pages** and change the "Source" dropdown to "GitHub Actions"
5. GitHub Actions will automatically build and deploy to Pages

### How the Deployment Works

- Notebooks in the `notebooks/` directory are exported with `--mode edit` (users can modify the code)
- Notebooks in the `apps/` directory are exported with `--mode run --no-show-code` (code is hidden, only UI is shown)
- The GitHub Actions workflow creates an index page and deploys everything to GitHub Pages

## 💻 Local Development

### Setting Up the Environment

This project uses [uv](https://github.com/astral-sh/uv) for package management. The Makefile includes commands to help you get started:

```bash
# Install uv package manager
make uv

# Run a specific notebook in edit mode
make notebook NOTEBOOK=fibonacci

# Run a specific app in edit mode
make app APP=charts

# Build the entire website locally (dry run)
make dryrun
```

The `dryrun` command builds the entire website locally using the same process as the CI/CD pipeline but publishes it to a local `_site` folder instead of deploying to GitHub Pages. This is useful for previewing the complete website before pushing changes.

### Creating New Notebooks

1. Add your Python file to either the `notebooks/` or `apps/` directory
2. Include the necessary dependencies at the top of your file:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.13.15",
#     # Add other dependencies here
# ]
# ///
```

## 📁 Including Data or Assets

To include data or assets in your notebooks, add them to the `public/` directory within either the `notebooks/` or `apps/` directory.

### Examples:

#### Loading an image:

```markdown
<img src="public/logo.png" width="200" />
```

#### Loading a CSV dataset:

```python
import polars as pl
df = pl.read_csv(mo.notebook_location() / "public" / "penguins.csv")
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the terms included in the [LICENSE](LICENSE) file.
