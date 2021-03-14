# ========== (c) JP Hwang 2020-02-28  ==========

import logging
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from utils import graphs_utils as gu, sql_utils as sqlu

# ===== START LOGGER =====
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)

desired_width = 320
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', desired_width)

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        {
            'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
            'rel': 'stylesheet',
            'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
            'crossorigin': 'anonymous'
        },
        {
            "href": "https://fonts.googleapis.com/css2?family=Gloria+Hallelujah&display=swap",
            "rel": "stylesheet",
        },
        {
            "href": "https://fonts.googleapis.com/css2?family=Lilita+One&display=swap",
            "rel": "stylesheet",
        }
    ]
)

server = app.server

# Filtros
[years_filter, ccaas_filter, families_filter] = sqlu.get_product_filters()
[countries_filter, indicators_filter] = sqlu.get_commerce_filters()

app.title = 'Sister Hack'
app.layout = html.Div(
    className='dash-container',
    children=[
        html.Div(
            className='header',
            children=[
                # html.I(className='fa fa-carrot fa-lg'),
                html.H1('🥑 Agro Analysis Dashboard'),
            ]),
        # graphs
        html.Div(
            className='content',
            children=[
                dcc.Tabs([
                    dcc.Tab(
                        label='Productos 🥕',
                        children=[
                            html.Div(
                                className='filters',
                                children=[
                                    html.H4('Filtros'),
                                    html.Div(
                                        children=[
                                            html.Label('Año: '),
                                            dcc.Dropdown(
                                                id='year-select',
                                                options=[{'label': i, 'value': i} for i in years_filter],
                                                value='Todos',
                                                style={'paddingLeft': '10px', 'width': '240px'}
                                            ),
                                        ]),
                                    html.Div(
                                        children=[
                                            html.Label('CCAA: '),
                                            dcc.Checklist(
                                                id='ccaa-select',
                                                options=[{'label': i, 'value': i} for i in ccaas_filter],
                                                value=[],
                                                style={'paddingLeft': '10px'}
                                            ),
                                        ]),
                                    html.Div(
                                        children=[
                                            html.Label('Familia de productos: '),
                                            dcc.RadioItems(
                                                id='family-select',
                                                options=[{'label': i, 'value': i} for i in families_filter],
                                                value='F&H',
                                                style={'paddingLeft': '10px'}
                                            ),
                                        ]),
                                ]),
                            dcc.Graph(
                                'products-graph',
                                config={'displayModeBar': False}
                            ),
                        ]),
                    dcc.Tab(
                        label='Comercio Exterior (UE) 🌍',
                        children=[
                            html.Div(
                                className='filters',
                                children=[
                                    html.H4('Filtros'),
                                    html.Div(
                                        children=[
                                            html.Label('País: '),
                                            dcc.Checklist(
                                                id='country-select',
                                                options=[{'label': i, 'value': i} for i in countries_filter],
                                                value=[],
                                                style={'paddingLeft': '10px'}
                                            ),
                                        ]),
                                    html.Div(
                                        children=[
                                            html.Label('Indicador: '),
                                            dcc.RadioItems(
                                                id='indicators-select',
                                                options=[{'label': i, 'value': i} for i in indicators_filter],
                                                value=indicators_filter[0],
                                                style={'paddingLeft': '10px'}
                                            ),
                                        ]),
                                ]),
                            dcc.Graph(
                                'commerce-graph',
                                config={'displayModeBar': False}
                            ),
                        ]),
                ])
            ]),
        # footer
        html.Div(
            className='footer',
            children=[
                html.P([
                    html.Small("Desarrollado por "),
                    html.A(html.Small("👩🏻 Vanessa Navarro"), href="https://www.linkedin.com/in/vanessa-nav/",
                           title="Vanessa Navarro"),
                    html.Small(" y "),
                    html.A(html.Small("👩🏼 María Navarro"),
                           href="https://www.linkedin.com/in/mar%C3%ADa-navarro-coronado-22723a206/",
                           title="María Navarro"),
                    html.Small(" para "),
                    html.A(html.Small("Cajamar UniversityHack 2021"),
                           href="https://www.cajamardatalab.com/datathon-cajamar-universityhack-2021/retos/visualizacion/",
                           title="Reto Cajamar Agro Analysis"),
                ]),
            ])
    ])


@app.callback(
    Output('products-graph', 'figure'),
    [Input('year-select', 'value'), Input('ccaa-select', 'value'), Input('family-select', 'value')]
)
def update_product_graphs(year, ccaas, family):
    y_label1 = 'Volumen (miles de kg)'
    y_label2 = 'Valor (miles de €)'
    y_label3 = 'Precio medio kg'
    x_label = 'Producto'
    data1 = sqlu.get_product_data(y_label1, year, ccaas, family)
    data2 = sqlu.get_product_data(y_label2, year, ccaas, family)
    data3 = sqlu.get_product_data(y_label3, year, ccaas, family)
    return gu.make_bar_chart([data1, data2, data3], x_label, [y_label1, y_label2, y_label3])


@app.callback(
    Output('commerce-graph', 'figure'),
    [Input('country-select', 'value'), Input('indicators-select', 'value')]
)
def update_commerce_graphs(countries, indicator):
    title1 = 'Importaciones'
    title2 = 'Exportaciones'
    data1 = sqlu.get_commerce_data('IMPORT', countries, indicator)
    data2 = sqlu.get_commerce_data('EXPORT', countries, indicator)
    return gu.make_scatter_chart([data1, data2], [title1, title2])

# ===== END - PLOT GRAPH =====


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
