#!/usr/bin/env python3
"""
Build script for marimo notebooks.

This script exports marimo notebooks to HTML/WebAssembly format and generates
an index.html file that lists all the notebooks. It handles both regular notebooks
(from the notebooks/ directory) and apps (from the apps/ directory).

The script can be run from the command line with optional arguments:
    python .github/scripts/build.py [--output-dir OUTPUT_DIR]

The exported files will be placed in the specified output directory (default: _site).
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "jinja2==3.1.3"
# ]
# ///

import subprocess
import argparse
from typing import List
from pathlib import Path
import jinja2


def export_html_wasm(notebook_path: Path, output_dir: Path, as_app: bool = False) -> bool:
    """Export a single marimo notebook to HTML/WebAssembly format.

    This function takes a marimo notebook (.py file) and exports it to HTML/WebAssembly format.
    If as_app is True, the notebook is exported in "run" mode with code hidden, suitable for
    applications. Otherwise, it's exported in "edit" mode, suitable for interactive notebooks.

    Args:
        notebook_path (Path): Path to the marimo notebook (.py file) to export
        output_dir (Path): Directory where the exported HTML file will be saved
        as_app (bool, optional): Whether to export as an app (run mode) or notebook (edit mode).
                                Defaults to False.

    Returns:
        bool: True if export succeeded, False otherwise
    """
    # Convert .py extension to .html for the output file
    output_path: Path = notebook_path.with_suffix(".html")

    # Base command for marimo export
    cmd: List[str] = ["uvx", "marimo", "export", "html-wasm", "--sandbox"]

    # Configure export mode based on whether it's an app or a notebook
    if as_app:
        print(f"Exporting {notebook_path} to {output_path} as app")
        cmd.extend(["--mode", "run", "--no-show-code"])  # Apps run in "run" mode with hidden code
    else:
        print(f"Exporting {notebook_path} to {output_path} as notebook")
        cmd.extend(["--mode", "edit"])  # Notebooks run in "edit" mode

    try:
        # Create full output path and ensure directory exists
        output_file: Path = output_dir / notebook_path.with_suffix(".html")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Add notebook path and output file to command
        cmd.extend([str(notebook_path), "-o", str(output_file)])

        # Run marimo export command
        print(cmd)
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        # Handle marimo export errors
        print(f"Error exporting {notebook_path}:")
        print(e.stderr)
        return False
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error exporting {notebook_path}: {e}")
        return False


def generate_index(all_notebooks: List[Path], output_dir: Path) -> None:
    """Generate an index.html file that lists all the notebooks.

    This function creates an HTML index page that displays links to all the exported
    notebooks. The index page includes the marimo logo and displays each notebook
    with a formatted title and a link to open it.

    Args:
        all_notebooks (List[Path]): List of paths to all the notebooks
        output_dir (Path): Directory where the index.html file will be saved

    Returns:
        None
    """
    print("Generating index.html")

    # Create the full path for the index.html file
    index_path: Path = output_dir / "index.html"

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    #os.makedirs(output_dir, exist_ok=True)

    try:
        # Set up Jinja2 environment
        template_dir = Path(__file__).parent / "templates"
            #os.path.join(os.path.dirname(__file__), "templates"))
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            autoescape=jinja2.select_autoescape(["html", "xml"])
        )

        # Load the template
        template = env.get_template("index.html.j2")

        # Prepare notebook data for the template
        notebooks_data = []
        for notebook in all_notebooks:
            # Extract the notebook name from the path and remove the .py extension
            notebook_name: str = notebook.stem

            # Format the display name by replacing underscores with spaces and capitalizing
            display_name: str = notebook_name.replace("_", " ").title()

            # Add notebook data to the list
            notebooks_data.append({
                "display_name": display_name,
                "html_path": str(notebook.with_suffix(".html"))
            })

        # Render the template with notebook data
        rendered_html = template.render(notebooks=notebooks_data)

        # Write the rendered HTML to the index.html file
        with open(index_path, "w") as f:
            f.write(rendered_html)

    except IOError as e:
        # Handle file I/O errors
        print(f"Error generating index.html: {e}")
    except jinja2.exceptions.TemplateError as e:
        # Handle template errors
        print(f"Error rendering template: {e}")


def main() -> None:
    """Main function to build marimo notebooks.

    This function:
    1. Parses command line arguments
    2. Finds all marimo notebooks in the 'notebooks' and 'apps' directories
    3. Exports each notebook to HTML/WebAssembly format
    4. Generates an index.html file that lists all the notebooks

    Command line arguments:
        --output-dir: Directory where the exported files will be saved (default: _site)

    Returns:
        None
    """
    # Set up command line argument parsing
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Build marimo notebooks")
    parser.add_argument(
        "--output-dir", default="_site", help="Output directory for built files"
    )
    args: argparse.Namespace = parser.parse_args()

    # Convert output_dir to Path
    output_dir: Path = Path(args.output_dir)

    # Initialize empty list to store all notebook paths
    all_notebooks: List[Path] = []

    # Look for notebooks in both the notebooks/ and apps/ directories
    for directory in ["notebooks", "apps"]:
        dir_path: Path = Path(directory)
        if not dir_path.exists():
            print(f"Warning: Directory not found: {dir_path}")
            continue

        # Find all Python files recursively in the directory
        all_notebooks.extend(path for path in dir_path.rglob("*.py"))

    # Exit if no notebooks were found
    if not all_notebooks:
        print("No notebooks found!")
        return

    # Export each notebook to HTML/WebAssembly format
    # Files in the apps/ directory are exported as apps (run mode)
    # Files in the notebooks/ directory are exported as notebooks (edit mode)
    for nb in all_notebooks:
        export_html_wasm(nb, output_dir, as_app=str(nb).startswith("apps/"))

    # Generate the index.html file that lists all notebooks
    generate_index(all_notebooks, output_dir)


if __name__ == "__main__":
    main()
