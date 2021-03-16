# ========== Vanessa Navarro 2021-03-17  ==========

import logging
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from utils import graphs_utils as gu, data_utils as du

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
[years_filter, ccaas_filter, families_filter] = du.get_product_filters()
[countries_filter, indicators_filter] = du.get_commerce_filters()
measures_filter = ['TASA DE VARIACIÓN', 'MEDIA']

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
                html.Img(className='logo', src='assets/datagri.png'),
                html.Img(className='logo2', src='assets/Sister-Hack_small.png'),
                dcc.Tabs([
                    dcc.Tab(
                        label='Oferta de Productos 🥕',
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
                            html.Div(
                                className='measure-filter',
                                children=[
                                    html.Label('Medida: '),
                                    dcc.RadioItems(
                                        id='measure-select',
                                        options=[{'label': i, 'value': i} for i in measures_filter],
                                        value=measures_filter[0],
                                        style={'paddingLeft': '10px'}
                                    ),
                                ]),
                            dcc.Graph(
                                'prices-graph',
                                config={'displayModeBar': False}
                            ),
                            # dcc.Graph(
                            #     'spain-map-graph',
                            #     config={'displayModeBar': False}
                            # ),
                            html.Hr(style={'border-top': '3px dotted rosybrown'}),
                            html.H4('🧄 Por Producto 🥝', style={'padding-top': '25px', 'textAlign': 'center'}),
                            dcc.Graph(
                                'offer-graph',
                                config={'displayModeBar': False}
                            ),
                        ]),
                    dcc.Tab(
                        label='Demanda de Productos 👨‍👩‍👧‍👦',
                        children=[
                            html.Div(
                                className='filters',
                                children=[
                                    html.H4('Filtros'),
                                    html.Div(
                                        children=[
                                            html.Label('Año: '),
                                            dcc.Dropdown(
                                                id='year-select2',
                                                options=[{'label': i, 'value': i} for i in years_filter],
                                                value='Todos',
                                                style={'paddingLeft': '10px', 'width': '240px'}
                                            ),
                                        ]),
                                    html.Div(
                                        children=[
                                            html.Label('CCAA: '),
                                            dcc.Checklist(
                                                id='ccaa-select2',
                                                options=[{'label': i, 'value': i} for i in ccaas_filter],
                                                value=[],
                                                style={'paddingLeft': '10px'}
                                            ),
                                        ]),
                                    html.Div(
                                        children=[
                                            html.Label('Familia de productos: '),
                                            dcc.RadioItems(
                                                id='family-select2',
                                                options=[{'label': i, 'value': i} for i in families_filter],
                                                value='F&H',
                                                style={'paddingLeft': '10px'}
                                            ),
                                        ]),
                                ]),
                            html.Div(
                                className='measure-filter',
                                children=[
                                    html.Label('Medida: '),
                                    dcc.RadioItems(
                                        id='measure-select2',
                                        options=[{'label': i, 'value': i} for i in measures_filter],
                                        value=measures_filter[0],
                                        style={'paddingLeft': '10px'}
                                    ),
                                ]),
                            dcc.Graph(
                                'demand-time-graph',
                                config={'displayModeBar': False}
                            ),
                            html.Hr(style={'border-top': '3px dotted rosybrown'}),
                            html.H4('🍆 Por Producto 🍒', style={'padding-top': '25px', 'textAlign': 'center'}),
                            dcc.Graph(
                                'demand-graph',
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
                                            html.Label('Año: '),
                                            dcc.Dropdown(
                                                id='year-select3',
                                                options=[{'label': i, 'value': i} for i in years_filter],
                                                value='Todos',
                                                style={'paddingLeft': '10px', 'width': '240px'}
                                            ),
                                        ]),
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
                            html.Div(
                                className='measure-filter',
                                children=[
                                    html.Label('Medida: '),
                                    dcc.RadioItems(
                                        id='measure-select3',
                                        options=[{'label': i, 'value': i} for i in measures_filter],
                                        value=measures_filter[0],
                                        style={'paddingLeft': '10px'}
                                    ),
                                ]),
                            dcc.Graph(
                                'commerce-time-graph',
                                config={'displayModeBar': False}
                            ),
                            # dcc.Graph(
                            #     'eu-map-graph',
                            #     config={'displayModeBar': False}
                            # ),
                            html.Hr(style={'border-top': '3px dotted rosybrown'}),
                            html.H4('🍅 Por Producto 🍈', style={'padding-top': '25px', 'textAlign': 'center'}),
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
                html.P(
                    children=[
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
                        html.A(
                            html.I(className='fab fa-github fa-lg mt-2'),
                            className='float-right',
                            target='blank',
                            href="https://github.com/VanessaNav/datathon_cajamar_datagri",
                            title="SisterHack GitHub"),
                    ]),
            ])
    ])

app.title = 'Sister Hack'


@app.callback(
    [Output('prices-graph', 'figure'), Output('offer-graph', 'figure')],
    # [Output('prices-graph', 'figure'), Output('spain-map-graph', 'figure'), Output('offer-graph', 'figure')],
    [Input('year-select', 'value'), Input('ccaa-select', 'value'), Input('family-select', 'value'), Input('measure-select', 'value')]
)
def update_offer_graphs(year, ccaas, family, measure):
    y_label1 = 'Volumen (miles de kg)'
    y_label2 = 'Valor (miles de €)'
    y_label3 = 'Precio medio kg'
    name = 'Precio medio kg (' + measure + ')'
    x_label123 = 'Producto'
    x_label4 = 'Fecha'
    title = 'Volatilidad de los precios 📈: Evolución del precio medio por kg'
    data1 = du.get_product_data(y_label1, x_label123, year, ccaas, family, measure)
    data2 = du.get_product_data(y_label2, x_label123, year, ccaas, family, measure)
    data3 = du.get_product_data(y_label3, x_label123, year, ccaas, family, measure)
    data4 = du.get_product_data(y_label3, x_label4, year, ccaas, family, measure)
    # [data5, geometry] = du.get_map_data(year, ccaas, family)
    return [
        gu.make_line_chart([data4], [x_label4], [y_label3], [name], title),
        # gu.make_map_chart(data5, geometry, y_label3, 'CCAA', title),
        gu.make_bar_chart([data1, data2, data3], x_label123, [y_label1, y_label2, y_label3]),
    ]


@app.callback(
    [Output('demand-time-graph', 'figure'), Output('demand-graph', 'figure')],
    [Input('year-select2', 'value'), Input('ccaa-select2', 'value'), Input('family-select2', 'value'), Input('measure-select2', 'value')]
)
def update_demand_graphs(year, ccaas, family, measure):
    y_label1 = 'Consumo per capita'
    y_label2 = 'Gasto per capita'
    x_label12 = 'Producto'
    x_label3 = 'Fecha'
    title = 'Evolución del gasto y del consumo per capita'
    data1 = du.get_product_data(y_label1, x_label12, year, ccaas, family, measure)
    data2 = du.get_product_data(y_label2, x_label12, year, ccaas, family, measure)
    data3 = du.get_product_data(y_label1, x_label3, year, ccaas, family, measure)
    data4 = du.get_product_data(y_label2, x_label3, year, ccaas, family, measure)
    return [
        gu.make_line_chart([data3, data4], [x_label3, x_label3], [y_label1, y_label2], [measure, measure], title),
        gu.make_bar_chart([data1, data2], x_label12, [y_label1, y_label2]),
    ]


@app.callback(
    [Output('commerce-time-graph', 'figure'), Output('commerce-graph', 'figure')],
    # [Output('commerce-time-graph', 'figure'), Output('eu-map-graph', 'figure'), Output('commerce-graph', 'figure')],
    [Input('year-select3', 'value'), Input('country-select', 'value'), Input('indicators-select', 'value'), Input('measure-select3', 'value')]
)
def update_commerce_graphs(year, countries, indicator, measure):
    y_label1 = 'Importaciones'
    y_label2 = 'Exportaciones'
    x_label = 'Fecha'
    name = 'Value'
    title1 = 'Evolución del comercio exterior'
    title2 = 'Comercio exterior por producto'
    data1 = du.get_commerce_data('DATE', name, 'IMPORT', year, countries, indicator, measure)
    data2 = du.get_commerce_data('DATE', name, 'EXPORT', year, countries, indicator, measure)
    data3 = du.get_commerce_data('PRODUCT', name, 'IMPORT', year, countries, indicator, measure)
    data4 = du.get_commerce_data('PRODUCT', name, 'EXPORT', year, countries, indicator, measure)
    # [data5, geometry] = du.get_eu_map_data('EXPORT', year, countries, indicator)
    return [
        gu.make_line_chart([data1, data2], [x_label, x_label], [y_label1, y_label2], [name, name], title1),
        # gu.make_map_chart(data5, geometry, 'Value', 'country', title1),
        gu.make_scatter_chart([data3, data4], [y_label1, y_label2], [name, name], title2, True)
    ]

# ===== END - PLOT GRAPH =====


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
