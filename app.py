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
            "href": "https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;700&display=swap",
            "rel": "stylesheet",
        },
        {
            "href": "https://fonts.googleapis.com/css2?family=Lilita+One&display=swap",
            "rel": "stylesheet",
        }
    ],
    meta_tags=[
        {
            "name": "description",
            "content": "Dashboard desarrollado por el equipo Sister Hack para el reto Agro Analysis de la competición Cajamar UniversityHack 2021."
        },
        {
            "name": "image",
            "content": "assets/Sister-Hack_small.png"
        },
        # {
        #     "name": "viewport",
        #     "content": "width=device-width, initial-scale=1.0"
        # }
    ]
)

server = app.server

# Filtros
[products_filter, df4_products_filter, years_filter, ccaas_filter, families_filter] = du.get_product_filters()
[countries_filter, indicators_filter] = du.get_commerce_filters()
measures_filter = ['Media', 'Tasa de variación']
volume_description = 'La patata, la naraja y el tomate protagonizaron las mejores recolectas de 2020.'
value_description = 'Los productos que mayor valor aportaron a la agricultura de España (en relación a la recolección de 2020) fueron el tomate y la patata.'
consumed_description = 'Aumenta el consumo porque la gente quiere comer mas sano.'
expense_description = 'El gasto de las familias españolas en patatas y naranjas ha aumentado con el paso de la Covid-19.'
offer_description = 'El precio medio del total de frutas y hortalizas en abril de 2020 ha aumentado un 13% con respecto a abril del 2019.'
demand_description = 'El consumo per capita del total de frutas y hortalizas en abril de 2020 ha aumentado un 46% con respecto abril del 2019.'
imports_description = 'Las importaciones a España en mayo de 2020 han disminuido un 7% con respecto a mayo de 2019.'
exports_description = 'Las exportaciones de España en mayo de 2020 han disminuido un 12% con respecto a mayo de 2019.'
product_imports_description = 'En el año 2020 los productos más importados en España son el pimiento y el tomate.'
product_exports_description = 'En el año 2020 los productos más exportados de España son la patata y la manzana.'
commerce_description = 'En 2020, el país donde importamos mayor volumen de frutas y hortalizas fue Finlandia. Así mismo, el país al que más exportamos nuestros productos agrícolas fue Croacia.'
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
                        label='Productos 🍊',
                        children=[
                            html.Div(
                                className='filters',
                                children=[
                                    html.H6('Filtros'),
                                    html.Div(
                                        className='filter',
                                        children=[
                                            html.Label('Año: '),
                                            dcc.Dropdown(
                                                id='year-select4',
                                                options=[{'label': i, 'value': i} for i in years_filter],
                                                value='Todos',
                                            ),
                                        ]),
                                    html.Div(
                                        className='checklist-filter-products',
                                        children=[
                                            html.Label('Productos: '),
                                            dcc.Checklist(
                                                id='product-select',
                                                options=[{'label': i, 'value': i} for i in products_filter],
                                                value=[],
                                            ),
                                        ]),
                                ]),
                            html.Div(
                                className='main-tab-content',
                                children=[
                                    dcc.Tabs([
                                        dcc.Tab(
                                            label='Volumen',
                                            children=[
                                                html.Div(
                                                    className='main-tab-content',
                                                    children=[
                                                        html.Div(
                                                            className='product-graphs',
                                                            children=[
                                                                html.Div(
                                                                    className='percentages',
                                                                    children=[
                                                                        html.Div(
                                                                            className='percentages-item',
                                                                            children=[
                                                                                html.Span(
                                                                                    className="percentage",
                                                                                    children='🥔 14.15k'
                                                                                ),
                                                                                html.Br(),
                                                                                html.Span(
                                                                                    className='year',
                                                                                    children='En 2020'
                                                                                ),
                                                                                html.Span(
                                                                                    className='success',
                                                                                    children='⬆20%'
                                                                                ),
                                                                            ]),
                                                                        html.Div(
                                                                            className='percentages-item',
                                                                            children=[
                                                                                html.Span(
                                                                                    className="percentage",
                                                                                    children='🍊 11.21k'
                                                                                ),
                                                                                html.Br(),
                                                                                html.Span(
                                                                                    className='year',
                                                                                    children='En 2020'
                                                                                ),
                                                                                html.Span(
                                                                                    className='success',
                                                                                    children='⬆62%'
                                                                                ),
                                                                            ]),
                                                                        html.Div(
                                                                            className='percentages-item',
                                                                            children=[
                                                                                html.Span(
                                                                                    className="percentage",
                                                                                    children='🍅 8.52k'
                                                                                ),
                                                                                html.Br(),
                                                                                html.Span(
                                                                                    className='year',
                                                                                    children='En 2020'
                                                                                ),
                                                                                html.Span(
                                                                                    className='success',
                                                                                    children='⬆50%'
                                                                                ),
                                                                            ]),
                                                                        html.Div(
                                                                            className='description',
                                                                            children=[
                                                                                html.P(
                                                                                    volume_description
                                                                                )],
                                                                        ),
                                                                    ]),
                                                                dcc.Graph(
                                                                    'products-volume-graph',
                                                                ),
                                                            ]),
                                                    ]),
                                            ]),
                                        dcc.Tab(
                                            label='Valor',
                                            children=[
                                                html.Div(
                                                    className='main-tab-content',
                                                    children=[
                                                        html.Div(
                                                            className='product-graphs',
                                                            children=[
                                                                html.Div(
                                                                    className='percentages',
                                                                    children=[
                                                                        html.Div(
                                                                            className='percentages-item',
                                                                            children=[
                                                                                html.Span(
                                                                                    className="percentage",
                                                                                    children='🍅 14.92k'
                                                                                ),
                                                                                html.Br(),
                                                                                html.Span(
                                                                                    className='year',
                                                                                    children='En 2020'
                                                                                ),
                                                                                html.Span(
                                                                                    className='success',
                                                                                    children='⬆55%'
                                                                                ),
                                                                            ]),
                                                                        html.Div(
                                                                            className='percentages-item',
                                                                            children=[
                                                                                html.Span(
                                                                                    className="percentage",
                                                                                    children='🥔 13.9k'
                                                                                ),
                                                                                html.Br(),
                                                                                html.Span(
                                                                                    className='year',
                                                                                    children='En 2020'
                                                                                ),
                                                                                html.Span(
                                                                                    className='success',
                                                                                    children='⬆24%'
                                                                                ),
                                                                            ]),
                                                                        html.Div(
                                                                            className='description',
                                                                            children=[
                                                                                html.P(
                                                                                    value_description
                                                                                )],
                                                                        ),
                                                                    ]),
                                                                dcc.Graph(
                                                                    'products-value-graph',
                                                                ),
                                                            ]),
                                                    ]),
                                            ]),
                                        dcc.Tab(
                                            label='Consumo per capita',
                                            children=[
                                                html.Div(
                                                    className='main-tab-content',
                                                    children=[
                                                        html.Div(
                                                            className='product-graphs',
                                                            children=[
                                                                html.Div(
                                                                    className='percentages',
                                                                    children=[
                                                                        html.Div(
                                                                            className='percentages-item',
                                                                            children=[
                                                                                html.Span(
                                                                                    className="percentage",
                                                                                    children='🥔 2.77kg'
                                                                                ),
                                                                                html.Br(),
                                                                                html.Span(
                                                                                    className='year',
                                                                                    children='En 2020'
                                                                                ),
                                                                                html.Span(
                                                                                    className='success',
                                                                                    children='⬆23%'
                                                                                ),
                                                                            ]),
                                                                        html.Div(
                                                                            className='percentages-item',
                                                                            children=[
                                                                                html.Span(
                                                                                    className="percentage",
                                                                                    children='🍊 2.11kg'
                                                                                ),
                                                                                html.Br(),
                                                                                html.Span(
                                                                                    className='year',
                                                                                    children='En 2020'
                                                                                ),
                                                                                html.Span(
                                                                                    className='success',
                                                                                    children='⬆51%'
                                                                                ),
                                                                            ]),
                                                                        html.Div(
                                                                            className='description',
                                                                            children=[
                                                                                html.P(
                                                                                    consumed_description
                                                                                )],
                                                                        ),
                                                                    ]),
                                                                dcc.Graph(
                                                                    'products-consumed-graph',
                                                                ),
                                                            ]),
                                                    ]),
                                            ]),
                                        dcc.Tab(
                                            label='Gasto per capita',
                                            children=[
                                                html.Div(
                                                    className='main-tab-content',
                                                    children=[
                                                        html.Div(
                                                            className='product-graphs',
                                                            children=[
                                                                html.Div(
                                                                    className='percentages',
                                                                    children=[
                                                                        html.Div(
                                                                            className='percentages-item',
                                                                            children=[
                                                                                html.Span(
                                                                                    className="percentage",
                                                                                    children='🥔 2.72€'
                                                                                ),
                                                                                html.Br(),
                                                                                html.Span(
                                                                                    className='year',
                                                                                    children='En 2020'
                                                                                ),
                                                                                html.Span(
                                                                                    className='success',
                                                                                    children='⬆27%'
                                                                                ),
                                                                            ]),
                                                                        html.Div(
                                                                            className='percentages-item',
                                                                            children=[
                                                                                html.Span(
                                                                                    className="percentage",
                                                                                    children='🍊 2.35€'
                                                                                ),
                                                                                html.Br(),
                                                                                html.Span(
                                                                                    className='year',
                                                                                    children='En 2020'
                                                                                ),
                                                                                html.Span(
                                                                                    className='success',
                                                                                    children='⬆74%'
                                                                                ),
                                                                            ]),
                                                                        html.Div(
                                                                            className='description',
                                                                            children=[
                                                                                html.P(
                                                                                    expense_description
                                                                                )],
                                                                        ),
                                                                    ]),
                                                                dcc.Graph(
                                                                    'products-expense-graph',
                                                                ),
                                                            ]),
                                                    ]),
                                            ]),
                                    ]),
                                ]),
                        ]),
                    dcc.Tab(
                        label='Oferta de Productos',
                        children=[
                            html.Div(
                                className='filters',
                                children=[
                                    html.H6('Filtros'),
                                    html.Div(
                                        className='filter',
                                        children=[
                                            html.Label('Año: '),
                                            dcc.Dropdown(
                                                id='year-select',
                                                options=[{'label': i, 'value': i} for i in years_filter],
                                                value='Todos',
                                            ),
                                        ]),
                                    html.Div(
                                        className='filter',
                                        children=[
                                            html.Label('Familia de productos: '),
                                            dcc.RadioItems(
                                                id='family-select',
                                                options=[{'label': i, 'value': i} for i in families_filter],
                                                value='F&H',
                                            ),
                                        ]),
                                    html.Div(
                                        className='checklist-filter-products',
                                        children=[
                                            html.Label('Productos: '),
                                            dcc.Checklist(
                                                id='product-select2',
                                                options=[{'label': i, 'value': i} for i in products_filter],
                                                value=[],
                                            ),
                                        ]),
                                ]),
                            html.Div(
                                className='main-tab-content',
                                children=[
                                    html.Div(
                                        className="measure-filter-container",
                                        children=[
                                            html.Div(
                                                className='measure-filter',
                                                children=[
                                                    html.Label('Medida: '),
                                                    dcc.RadioItems(
                                                        id='measure-select',
                                                        options=[{'label': i, 'value': i} for i in measures_filter],
                                                        value=measures_filter[0],
                                                        style={'display': 'inline-block'}
                                                    ),
                                                ]),
                                        ]),
                                    html.Div(
                                        className='offer-graphs',
                                        children=[
                                            html.Div(
                                                className='description',
                                                children=[
                                                    html.P(
                                                        offer_description
                                                    )],
                                            ),
                                            html.Div(
                                                className='map-graph',
                                                children=[
                                                    html.H6('Precio medio del kg por CCAA'),
                                                    html.Iframe(
                                                        className='spain-map-iframe',
                                                        id='offer-spain-map-iframe',
                                                        width='100%',
                                                        height='350',
                                                        srcDoc=open('maps/spain-offer.html', 'r').read()
                                                    ),
                                                ]),
                                            dcc.Graph(
                                                'prices-graph',
                                            ),
                                        ]),
                                ]),
                        ]),
                    dcc.Tab(
                        label='Demanda de Productos',
                        children=[
                            html.Div(
                                className='filters',
                                children=[
                                    html.H6('Filtros'),
                                    html.Div(
                                        className='filter',
                                        children=[
                                            html.Label('Año: '),
                                            dcc.Dropdown(
                                                id='year-select2',
                                                options=[{'label': i, 'value': i} for i in years_filter],
                                                value='Todos',
                                            ),
                                        ]),
                                    html.Div(
                                        className='filter',
                                        children=[
                                            html.Label('Familia de productos: '),
                                            dcc.RadioItems(
                                                id='family-select2',
                                                options=[{'label': i, 'value': i} for i in families_filter],
                                                value='F&H',
                                            ),
                                        ]),
                                    html.Div(
                                        className='checklist-filter-products',
                                        children=[
                                            html.Label('Productos: '),
                                            dcc.Checklist(
                                                id='product-select3',
                                                options=[{'label': i, 'value': i} for i in products_filter],
                                                value=[],
                                            ),
                                        ]),
                                ]),
                            html.Div(
                                className='main-tab-content',
                                children=[
                                    html.Div(
                                        className='measure-filter-container',
                                        children=[
                                            html.Div(
                                                className='measure-filter',
                                                children=[
                                                    html.Label('Medida: '),
                                                    dcc.RadioItems(
                                                        id='measure-select2',
                                                        options=[{'label': i, 'value': i} for i in measures_filter],
                                                        value=measures_filter[0],
                                                        style={'display': 'inline-block'}
                                                    ),
                                                ]),
                                        ]),
                                    html.Div(
                                        className='demand-graphs',
                                        children=[
                                            html.Div(
                                                className='description',
                                                children=[
                                                    html.P(
                                                        demand_description
                                                    )],
                                            ),
                                            html.Div(
                                                className='map-graph',
                                                children=[
                                                    html.H6('% Penetración por CCAA'),
                                                    html.Iframe(
                                                        className='spain-map-iframe',
                                                        id='demand-spain-map-iframe',
                                                        width='100%',
                                                        height='350',
                                                        srcDoc=open('maps/spain-demand.html', 'r').read()
                                                    ),
                                                ]),
                                            dcc.Graph(
                                                'demand-time-graph',
                                            ),
                                        ]),
                                ]),
                        ]),
                    dcc.Tab(
                        label='Comercio Exterior (UE) 🌍',
                        children=[
                            html.Div(
                                className='filters',
                                children=[
                                    html.H6('Filtros'),
                                    html.Div(
                                        className='filter',
                                        children=[
                                            html.Label('Año: '),
                                            dcc.Dropdown(
                                                id='year-select3',
                                                options=[{'label': i, 'value': i} for i in years_filter],
                                                value='Todos',
                                            ),
                                        ]),
                                    html.Div(
                                        className='filter',
                                        children=[
                                            html.Label('Indicador: '),
                                            dcc.RadioItems(
                                                id='indicators-select',
                                                options=[{'label': i, 'value': i} for i in indicators_filter],
                                                value=indicators_filter[0],
                                            ),
                                        ]),
                                    html.Div(
                                        className='checklist-filter-products',
                                        children=[
                                            html.Label('Productos: '),
                                            dcc.Checklist(
                                                id='product-select4',
                                                options=[{'label': i, 'value': i} for i in df4_products_filter],
                                                value=[],
                                            ),
                                        ]),
                                ]),
                            html.Div(
                                className='main-tab-content',
                                children=[
                                    dcc.Tabs([
                                        dcc.Tab(
                                            label='Evolución en el tiempo',
                                            children=[
                                                html.Div(
                                                    className='measure-filter-container',
                                                    children=[
                                                        html.Div(
                                                            className='measure-filter',
                                                            children=[
                                                                html.Label('Medida: '),
                                                                dcc.RadioItems(
                                                                    id='measure-select3',
                                                                    options=[{'label': i, 'value': i} for i in
                                                                             measures_filter],
                                                                    value=measures_filter[0],
                                                                    style={'display': 'inline-block'}
                                                                ),
                                                            ]),
                                                    ]),
                                                html.Div(
                                                    className='main-tab-content',
                                                    children=[
                                                        html.Div(
                                                            className="commerce-graphs",
                                                            children=[
                                                                html.Div(
                                                                    className='description',
                                                                    children=[
                                                                        html.P(
                                                                            imports_description
                                                                        ),
                                                                        html.P(
                                                                            exports_description
                                                                        )],
                                                                ),
                                                                dcc.Graph(
                                                                    'commerce-time-graph',
                                                                ),
                                                            ]),
                                                    ]),
                                            ]),
                                        dcc.Tab(
                                            label='Por país',
                                            children=[
                                                html.Div(
                                                    className='main-tab-content',
                                                    children=[
                                                        html.Div(
                                                            className="commerce-graphs",
                                                            children=[
                                                                html.Div(
                                                                    className='description',
                                                                    children=[
                                                                        html.P(
                                                                            commerce_description
                                                                        )],
                                                                ),
                                                                html.Div(
                                                                    className='map-graph',
                                                                    children=[
                                                                        html.H6('Importaciones por país (UE)'),
                                                                        html.Iframe(
                                                                            className='eu-map-iframe',
                                                                            id='imports-eu-map-iframe',
                                                                            width='100%',
                                                                            height='350',
                                                                            srcDoc=open('maps/eu-imports.html',
                                                                                        'r').read()
                                                                        ),
                                                                    ]),
                                                                html.Div(
                                                                    className='map-graph',
                                                                    children=[
                                                                        html.H6('Exportaciones por país (UE)'),
                                                                        html.Iframe(
                                                                            className='eu-map-iframe',
                                                                            id='exports-eu-map-iframe',
                                                                            width='100%',
                                                                            height='350',
                                                                            srcDoc=open('maps/eu-exports.html',
                                                                                        'r').read()
                                                                        ),
                                                                    ]),
                                                            ]),
                                                    ]),
                                            ]),
                                        dcc.Tab(
                                            label='Por producto',
                                            children=[
                                                html.Div(
                                                    className='measure-filter-container',
                                                    children=[
                                                        html.Div(
                                                            className='measure-filter',
                                                            children=[
                                                                html.Label('Medida: '),
                                                                dcc.RadioItems(
                                                                    id='measure-select4',
                                                                    options=[{'label': i, 'value': i} for i in
                                                                             measures_filter],
                                                                    value=measures_filter[0],
                                                                    style={'display': 'inline-block'}
                                                                ),
                                                            ]),
                                                    ]),
                                                html.Div(
                                                    className='main-tab-content',
                                                    children=[
                                                        html.Div(
                                                            className="commerce-graphs",
                                                            children=[
                                                                html.Div(
                                                                    className='description',
                                                                    children=[
                                                                        html.P(
                                                                            product_imports_description
                                                                        ),
                                                                        html.P(
                                                                            product_exports_description
                                                                        )],
                                                                ),
                                                                dcc.Graph(
                                                                    'commerce-graph',
                                                                ),
                                                            ]),
                                                    ]),
                                            ]),
                                    ]),
                                ]),
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
                            html.I(className='fab fa-github fa-lg mt-1'),
                            className='float-right',
                            target='blank',
                            href="https://github.com/VanessaNav/datathon_cajamar_datagri",
                            title="SisterHack GitHub"),
                    ]),
            ])
    ])

app.title = 'Sister Hack'


@app.callback(
    [Output('products-volume-graph', 'figure'), Output('products-value-graph', 'figure'),
     Output('products-consumed-graph', 'figure'), Output('products-expense-graph', 'figure')],
    [Input('year-select4', 'value'), Input('product-select', 'value')]
)
def update_product_graphs(year, products):
    x_label = 'Producto'
    y_label1 = 'Volumen (miles de kg)'
    y_label2 = 'Valor (miles de €)'
    y_label3 = 'Consumo per capita'
    y_label4 = 'Gasto per capita'
    title1 = 'Volumen de kg recolectados (en miles de kg)'
    title2 = 'Valor de la recolección (en miles de €): Volumen de kg recolectados ✖ Precio medio del kg'
    title3 = 'Consumo per capita: Cantidad de kg consumida por persona'
    title4 = 'Gasto per capita (en €): Cantidad de kg consumida por persona ✖ Precio medio del kg'
    data1 = du.get_products_data(y_label1, x_label, year, products)
    data2 = du.get_products_data(y_label2, x_label, year, products)
    data3 = du.get_products_data(y_label3, x_label, year, products)
    data4 = du.get_products_data(y_label4, x_label, year, products)
    return [
        gu.make_bar_chart([data1], x_label, [y_label1], [title1]),
        gu.make_bar_chart([data2], x_label, [y_label2], [title2]),
        gu.make_bar_chart([data3], x_label, [y_label3], [title3]),
        gu.make_bar_chart([data4], x_label, [y_label4], [title4]),
    ]


@app.callback(
    [Output('prices-graph', 'figure')],
    [Input('year-select', 'value'), Input('product-select2', 'value'), Input('family-select', 'value'),
     Input('measure-select', 'value')]
)
def update_offer_graphs(year, products, family, measure):
    y_label1 = 'Precio medio kg'
    name1 = 'Precio medio kg (' + measure + ')'
    x_label = 'Fecha'
    title = 'Volatilidad de los precios 📈: Evolución del precio medio por kg'
    data1 = du.get_generic_product_data(y_label1, x_label, year, products, family, measure)
    du.generate_spain_map(y_label1, 'spain-offer', year, products, family)
    return [
        gu.make_line_chart([data1], [x_label], [y_label1], [name1], title, True),
    ]


@app.callback(
    [Output('demand-time-graph', 'figure')],
    [Input('year-select2', 'value'), Input('product-select3', 'value'), Input('family-select2', 'value'),
     Input('measure-select2', 'value')]
)
def update_demand_graphs(year, products, family, measure):
    y_label1 = 'Consumo per capita'
    y_label2 = 'Gasto per capita'
    y_label3 = 'Penetración (%)'
    x_label = 'Fecha'
    title = 'Evolución del gasto y del consumo per capita'
    data3 = du.get_generic_product_data(y_label1, x_label, year, products, family, measure)
    data4 = du.get_generic_product_data(y_label2, x_label, year, products, family, measure)
    du.generate_spain_map(y_label3, 'spain-demand', year, products, family)
    return [
        gu.make_line_chart([data3, data4], [x_label, x_label], [y_label1, y_label2], [measure, measure], title, True)
    ]


@app.callback(
    [Output('commerce-time-graph', 'figure'), Output('commerce-graph', 'figure')],
    [Input('year-select3', 'value'), Input('product-select4', 'value'), Input('indicators-select', 'value'),
     Input('measure-select3', 'value'), Input('measure-select4', 'value')]
)
def update_commerce_graphs(year, df4_products, indicator, measure1, measure2):
    y_label1 = 'Importaciones'
    y_label2 = 'Exportaciones'
    x_label = 'Fecha'
    name = 'Value'
    title1 = 'Evolución del comercio exterior de España con la UE: Importaciones y Exportaciones por valor monetario (precio del total de kg) o por cantidad (volumen de producto en 100kg)'
    title2 = 'Comercio exterior por producto: Importaciones y Exportaciones de España con el resto de la UE'
    data1 = du.get_commerce_data('DATE', name, 'IMPORT', year, df4_products, indicator, measure1)
    data2 = du.get_commerce_data('DATE', name, 'EXPORT', year, df4_products, indicator, measure1)
    data3 = du.get_commerce_data('PRODUCT', name, 'IMPORT', year, df4_products, indicator, measure2)
    data4 = du.get_commerce_data('PRODUCT', name, 'EXPORT', year, df4_products, indicator, measure2)
    du.generate_eu_map(name, 'eu-imports', 'IMPORT', year, indicator)
    du.generate_eu_map(name, 'eu-exports', 'EXPORT', year, indicator)
    return [
        gu.make_line_chart([data1, data2], [x_label, x_label], [y_label1, y_label2], [name, name], title1, True),
        gu.make_scatter_chart([data3, data4], [y_label1, y_label2], [name, name], title2, True)
    ]


# ===== END - PLOT GRAPH =====


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
