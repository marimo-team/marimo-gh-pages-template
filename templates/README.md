# Template Documentation

## Overview

This directory contains Jinja2 templates used by the build 
script to generate HTML pages for the marimo WebAssembly + GitHub Pages project. 
Templates define the structure and appearance of the generated pages, 
particularly the index page that lists all notebooks and apps.

## Template Requirements

### Basic Structure

A template should be a valid HTML file with Jinja2 syntax for dynamic content. The template should:

1. Have a `.html.j2` extension
2. Include proper HTML structure (doctype, head, body)
3. Use responsive design principles for good display on various devices

### Expected Variables

Templates receive the following variables from the build script:

- `notebooks`: A list of dictionaries containing information about notebooks
  - Each notebook has:
    - `display_name`: The formatted name of the notebook (e.g., "Penguins" instead of "penguins")
    - `html_path`: The path to the HTML file for the notebook

- `apps`: A list of dictionaries containing information about apps
  - Each app has:
    - `display_name`: The formatted name of the app
    - `html_path`: The path to the HTML file for the app

### Required Sections

A complete template should include:

1. **Conditional Notebook Section**: Only display if notebooks exist

   ```jinja
   {% if notebooks %}
   <h2>Notebooks</h2>
   <div class="notebooks-container">
     {% for notebook in notebooks %}
     <div class="notebook-item">
       <h3>{{ notebook.display_name }}</h3>
       <a href="{{ notebook.html_path }}">Open Notebook</a>
     </div>
     {% endfor %}
   </div>
   {% endif %}
   ```

2. **Conditional App Section**: Only display if apps exist

   ```jinja
   {% if apps %}
   <h2>Apps</h2>
   <div class="apps-container">
     {% for app in apps %}
     <div class="app-item">
       <h3>{{ app.display_name }}</h3>
       <a href="{{ app.html_path }}">Open App</a>
     </div>
     {% endfor %}
   </div>
   {% endif %}
   ```

## Using Custom Templates

To use a custom template with the build script, use the `--template` parameter:

```bash
uv run .github/scripts/build.py --output-dir _site --template templates/your-custom-template.html.j2
```

## Example Templates

This repository includes three example templates:

1. `index.html.j2`: A less lean template with more styling and a footer
2. `tailwind.html.j2`: A minimal and lean template using Tailwind CSS

## Best Practices

1. **Styling**: 
   - Include CSS directly in the template using `<style>` tags for simplicity, or
   - Use Tailwind CSS via CDN for a utility-first approach without custom CSS
2. **Responsive Design**: Ensure the template works well on different screen sizes
3. **Conditional Sections**: Use `{% if %}` blocks to conditionally display sections based on data availability
4. **Comments**: Include comments in your template to explain complex sections
5. **Accessibility**: Use semantic HTML and proper ARIA attributes for accessibility
