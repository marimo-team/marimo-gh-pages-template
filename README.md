# marimo WebAssembly + GitHub Pages Template

This template repository demonstrates how to export [marimo](https://marimo.io) notebooks to WebAssembly and deploy them to GitHub Pages.

## 📚 Included Examples

- `apps/charts.py`: Interactive data visualization with Altair
- `notebooks/fibonacci.py`: Interactive Fibonacci sequence calculator
- `notebooks/penguins.py`: Interactive data analysis with Polars and marimo

## 🚀 Usage

1. Fork this repository
2. Add your marimo files to the `notebooks/` or `apps/` directory
3. Push to main branch
4. Go to repository **Settings > Pages** and change the "Source" dropdown to "GitHub Actions"
5. GitHub Actions will automatically build and deploy to Pages

## 📦 Export Types

This template supports three types of exports:

1. **Notebooks** (`notebooks/` directory): Exported in edit mode, allowing users to modify and experiment with the code
2. **WebAssembly Notebooks** (`notebooks/` directory): The same notebooks exported to WebAssembly for fully interactive use in the browser
3. **Apps** (`apps/` directory): Exported in run mode, where code is hidden for a clean user interface

## 📂 Including data or assets

To include data or assets in your notebooks, add them to the `public/` directory.

For example, the `apps/charts.py` notebook loads an image asset from the `public/` directory.

```markdown
<img src="public/logo.png" width="200" />
```

And the `notebooks/penguins.py` notebook loads a CSV dataset from the `public/` directory.

```python
import polars as pl
df = pl.read_csv(mo.notebook_location() / "public" / "penguins.csv")
```

## 🎨 Templates

This repository includes two templates for the generated site:

1. `tailwind.html.j2`: A minimal and lean template using Tailwind CSS

The templates are used by the GitHub Actions workflow to generate the index page. You can specify which template to use by modifying the `template` parameter in the `.github/workflows/deploy.yml` file.

You can also create your own custom templates. See the [templates/README.md](templates/README.md) for more information.

## 🔄 GitHub Actions Workflow

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically builds and deploys the site to GitHub Pages when changes are pushed to the main branch.

The workflow:

1. Checks out the repository code
2. Uses the [marimushka](https://github.com/jebel-quant/marimushka)
action to export notebooks and build the index page
3. Publishes the generated site to GitHub Pages

You can also trigger the workflow manually from the Actions tab in your repository.

## 🧪 Testing Locally

To test the site locally, you can serve the generated `_site/` directory 
using Python's built-in HTTP server:

```bash
python -m http.server -d _site
```

This will serve the site at `http://localhost:8000`.
