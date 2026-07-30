# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "gcloud==0.18.3",
#     "gspread==6.2.1",
#     "oauth2client==4.1.3",
# ]
# ///

import marimo

__generated_with = "0.23.15"
app = marimo.App(width="full", auto_download=["html"])


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import io
    import plotly.express as px
    import plotly.graph_objects as go
    app = mo.App(width="full")
    return go, io, mo, pd, px


@app.cell
def _():
    # Upload file locally
    # file = mo.ui.file()
    # file
    return


@app.cell
def _(mo):
    from gdrive_fsspec import GoogleDriveFileSystem

    fs = GoogleDriveFileSystem(use_listings_cache=False, skip_instance_cache=True, auth_kwargs={"use_local_webserver": False})
    mo.output.clear_console()
    return (fs,)


@app.cell
def _(fs, io, pd):
    data = fs.cat_file("Paineiras/arrecadacao_bolsas_paineiras.csv")
    df = pd.read_csv(io.BytesIO(data))
    # remove valor das mensalidades
    df = df.iloc[:-1]
    df['mensalidade_aluno'] = df['total_mensalidades']/(df['total_alunos'] - df['funcionarios_(100%)'])
    df['desconto_aluno'] = df['total_isencoes']/(df['total_alunos'] - df['funcionarios_(100%)'])
    # df.columns
    lista = ['total_alunos', 'mensalidade_aluno','desconto_aluno',
           'total_bolsas', 'bolsas_perc_alunos', 'total_bolsa_edital',
           'bolsa_edital_div_total_bolsas_perc','total_isencoes',
           'isencao_bolsa_edital','mensalidade_integral', 'mensalidade_bolsistas',
           'total_mensalidades', 'desconto_bolsa_social']
    return df, lista


@app.cell
def _(lista, mo):
    dd1 = mo.ui.dropdown(value='total_alunos',options=lista,full_width=True)

    dd2 = mo.ui.dropdown(value='total_mensalidades',options=lista,full_width=True)

    dd3 = mo.ui.dropdown(value='mensalidade_aluno',options=lista,full_width=True)

    dd4 = mo.ui.dropdown(value='total_isencoes',options=lista,full_width=True)

    dd5 = mo.ui.dropdown(value='desconto_aluno',options=lista,full_width=True)

    mo.sidebar(mo.md(f'''
        Tab1
        {dd1}
        Tab2
        {dd2}
        Tab3
        {dd3}
        Tab4
        {dd4}
        Tab5
        {dd5}
    '''))
    return dd1, dd2, dd3, dd4, dd5


@app.cell
def _(df, go, mo, px):
    # Distribuição dos alunos
    def fn_plots(dado):
        fig0 = px.sunburst(df,values=dado,path=['ciclo','turma'],hover_data=dado,title=dado).update_layout(width=1000, height=500)

        fig1 = px.bar(df, x='turma', y=dado, color='turma').add_annotation(
            text=f"""Total = {df[dado].sum()}""",
            font_size=16, xref="paper", yref="paper", y=0.99, x=0.99).update_layout(width=1000, height=500)

        fig2 = px.box(df,y=dado, color='ciclo', points='all', hover_name='turma').add_trace(go.Box(y=df[dado], name='Paineiras', marker_color='gray')).update_layout(width=1000, height=500)

        t0 = mo.ui.table(df[dado].describe().round(0).to_frame())

        tab1 = [fig0,fig1,fig2,t0]
        return tab1

    return (fn_plots,)


@app.cell
def _(dd1, dd2, dd3, dd4, dd5, fn_plots, mo):
    dado1 = dd1.value
    dado2 = dd2.value
    dado3 = dd3.value
    dado4 = dd4.value
    dado5 = dd5.value

    tab1 = fn_plots(dado1)
    tab2 = fn_plots(dado2)
    tab3 = fn_plots(dado3)
    tab4 = fn_plots(dado4)
    tab5 = fn_plots(dado5)

    tabs = mo.ui.tabs({
        dado1: tab1,
        dado2: tab2,
        dado3: tab3,
        dado4: tab4,
        dado5: tab5
    })
    tabs
    return


@app.cell
def _():
    # # Distribuição das isenções médias por aluno
    # df['desconta'] = df['total_isencoes']/(df['total_alunos']-df['funcionarios_(100%)'])
    return


if __name__ == "__main__":
    app.run()
