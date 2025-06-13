# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15",
#     "polars==1.30.0",
#     "altair==4.2.0",
#     "pandas==2.3.0",
# ]
# ///
import marimo

__generated_with = "0.13.5"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import polars as pl
    import altair as alt
    import pandas as pd

    file = mo.notebook_location() / "public" / "penguins.csv"

@app.cell(hide_code=True)
def _():
    mo.md(
        """
        # Palmer Penguins Analysis

        Analyzing the Palmer Penguins dataset using Polars and marimo.
        """
    )
    return


@app.cell
def _():
    # Read the penguins dataset
    df = pl.read_csv(str(file))
    df.head()
    return (df,)

@app.cell
def _():
    # Try to avoid reading the file with pandas
    _df = pd.read_csv(str(file))
    return

@app.cell
def _(df):
    # Basic statistics
    mo.md(f"""
    ### Dataset Overview

    - Total records: {df.height}
    - Columns: {', '.join(df.columns)}

    ### Summary Statistics

    {mo.as_html(df.describe())}
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""### Species Distribution""")
    return


@app.cell
def _(df):
    # Create species distribution chart
    species_chart = mo.ui.altair_chart(
        alt.Chart(df)
        .mark_bar()
        .encode(x="species", y="count()", color="species")
        .properties(title="Distribution of Penguin Species"),
        chart_selection=None,
    )

    species_chart
    return (species_chart,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""### Bill Dimensions Analysis""")
    return


@app.cell
def _(df):
    # Scatter plot of bill dimensions
    scatter = mo.ui.altair_chart(
        alt.Chart(df)
        .mark_point()
        .encode(
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
            tooltip=["species", "bill_length_mm", "bill_depth_mm"],
        )
        .properties(title="Bill Length vs Depth by Species"),
        chart_selection=None,
    )

    scatter
    return (scatter,)


if __name__ == "__main__":
    app.run()
