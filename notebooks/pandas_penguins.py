import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import polars as pl
    return mo, pd, pl


@app.cell
def _(mo):
    _file = mo.notebook_location() / "public" / "penguins.csv"
    file_str = str(_file)
    return (file_str,)


@app.cell
def _(file_str, pd):
    pd.read_csv(file_str)
    return


@app.cell
def _(file_str, pl):
    pl.read_csv(file_str)
    return


if __name__ == "__main__":
    app.run()
