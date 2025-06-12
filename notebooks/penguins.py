import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl
    import marimo as mo
    import altair as alt
    return alt, mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # Palmer Penguins Analysis

        Analyzing the Palmer Penguins dataset using Polars and marimo.
        """
    )
    return


@app.cell
def _(mo, pl):
    # Read the penguins dataset
    df = pl.read_csv(str(mo.notebook_location() / "public" / "penguins.csv"))
    df.head()
    return (df,)


@app.cell
def _(df, mo):
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
def _(mo):
    mo.md(r"""### Species Distribution""")
    return


@app.cell
def _(alt, df, mo):
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
def _(mo):
    mo.md(r"""### Bill Dimensions Analysis""")
    return


@app.cell
def _(alt, df, mo):
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
