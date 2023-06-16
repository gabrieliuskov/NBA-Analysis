import dash 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
url_theme1 = dbc.themes.SANDSTONE
url_theme2 = dbc.themes.CYBORG
theme1 = "sandstone"
theme2 = "cyborg"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE, font_awesome, dbc_css], title="NBA - Analysis", update_title="", suppress_callback_exceptions=True)

def cria_grafico(template, graph_margin, valor, color):
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        value=round(valor,0),
        mode="number",
        number={"font": {"color": color}, 'valueformat': '.0d'}
    ))
    fig.update_layout(template=template, margin=graph_margin, height=70)

    return fig
