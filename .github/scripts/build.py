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

import os
import subprocess
import argparse
from typing import List, Optional, Dict, Any, Union
from pathlib import Path


def export_html_wasm(notebook_path: str, output_dir: str, as_app: bool = False) -> bool:
    """Export a single marimo notebook to HTML/WebAssembly format.

    This function takes a marimo notebook (.py file) and exports it to HTML/WebAssembly format.
    If as_app is True, the notebook is exported in "run" mode with code hidden, suitable for
    applications. Otherwise, it's exported in "edit" mode, suitable for interactive notebooks.

    Args:
        notebook_path (str): Path to the marimo notebook (.py file) to export
        output_dir (str): Directory where the exported HTML file will be saved
        as_app (bool, optional): Whether to export as an app (run mode) or notebook (edit mode).
                                Defaults to False.

    Returns:
        bool: True if export succeeded, False otherwise
    """
    # Convert .py extension to .html for the output file
    output_path: str = notebook_path.replace(".py", ".html")

    # Base command for marimo export
    cmd: List[str] = ["marimo", "export", "html-wasm"]

    # Configure export mode based on whether it's an app or a notebook
    if as_app:
        print(f"Exporting {notebook_path} to {output_path} as app")
        cmd.extend(["--mode", "run", "--no-show-code"])  # Apps run in "run" mode with hidden code
    else:
        print(f"Exporting {notebook_path} to {output_path} as notebook")
        cmd.extend(["--mode", "edit"])  # Notebooks run in "edit" mode

    try:
        # Create full output path and ensure directory exists
        output_file: str = os.path.join(output_dir, output_path)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Add notebook path and output file to command
        cmd.extend([notebook_path, "-o", output_file])

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


def generate_index(all_notebooks: List[str], output_dir: str) -> None:
    """Generate an index.html file that lists all the notebooks.

    This function creates an HTML index page that displays links to all the exported
    notebooks. The index page includes the marimo logo and displays each notebook
    with a formatted title and a link to open it.

    Args:
        all_notebooks (List[str]): List of paths to all the notebooks
        output_dir (str): Directory where the index.html file will be saved

    Returns:
        None
    """
    print("Generating index.html")

    # Create the full path for the index.html file
    index_path: str = os.path.join(output_dir, "index.html")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Open the index.html file for writing
        with open(index_path, "w") as f:
            # Write the HTML header and page structure
            f.write(
                """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>marimo</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  </head>
  <body class="font-sans max-w-2xl mx-auto p-8 leading-relaxed">
    <div class="mb-8">
      <img src="https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/marimo-logotype-thick.svg" alt="marimo" class="h-20" />
    </div>
    <div class="grid gap-4">
"""
            )
            # Process each notebook and create a card for it
            for notebook in all_notebooks:
                # Extract the notebook name from the path and remove the .py extension
                notebook_name: str = notebook.split("/")[-1].replace(".py", "")

                # Format the display name by replacing underscores with spaces and capitalizing
                display_name: str = notebook_name.replace("_", " ").title()

                # Write the HTML for the notebook card
                f.write(
                    f'      <div class="p-4 border border-gray-200 rounded">\n'
                    f'        <h3 class="text-lg font-semibold mb-2">{display_name}</h3>\n'
                    f'        <div class="flex gap-2">\n'
                    f'          <a href="{notebook.replace(".py", ".html")}" class="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded">Open Notebook</a>\n'
                    f"        </div>\n"
                    f"      </div>\n"
                )
            # Write the HTML footer
            f.write(
                """    </div>
  </body>
</html>"""
            )
    except IOError as e:
        # Handle file I/O errors
        print(f"Error generating index.html: {e}")


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

    # Initialize empty list to store all notebook paths
    all_notebooks: List[str] = []

    # Look for notebooks in both the notebooks/ and apps/ directories
    for directory in ["notebooks", "apps"]:
        dir_path: Path = Path(directory)
        if not dir_path.exists():
            print(f"Warning: Directory not found: {dir_path}")
            continue

        # Find all Python files recursively in the directory
        all_notebooks.extend(str(path) for path in dir_path.rglob("*.py"))

    # Exit if no notebooks were found
    if not all_notebooks:
        print("No notebooks found!")
        return

    # Export each notebook to HTML/WebAssembly format
    # Files in the apps/ directory are exported as apps (run mode)
    # Files in the notebooks/ directory are exported as notebooks (edit mode)
    for nb in all_notebooks:
        export_html_wasm(nb, args.output_dir, as_app=nb.startswith("apps/"))

    # Generate the index.html file that lists all notebooks
    generate_index(all_notebooks, args.output_dir)


if __name__ == "__main__":
    main()
