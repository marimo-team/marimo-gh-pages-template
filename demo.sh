#!/bin/bash

# install uv/uvx
curl -LsSf https://astral.sh/uv/install.sh | sh

# This is interesting as it works without installing
# the dependencies before running this script
uv run build.py \
       --output_dir '_site' \
       --template 'templates/tailwind.html.j2'
