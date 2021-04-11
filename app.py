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
            "href": "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap",
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
[products_filter, years_filter, ccaas_filter, families_filter] = du.get_product_filters()
[countries_filter, indicators_filter] = du.get_commerce_filters()
measures_filter = ['Media', 'Tasa de variación']
volume_description = 'En 2020 los productos con mayor volumen de kg recolectados fueron la patata, la naraja y el tomate, con valores de 14.2, 11.2 y 8.5 miles de kg (aprox), respectivamente. Con respecto a 2019, el volumen de patatas recolectadas ha aumentado un 20%.'
value_description = 'Los productos que mayor valor aportaron a la agricultura de España (en relación a la recolección de 2020) fueron el tomate y la patata, con unos valores de 14.9 y 13.9 miles de € (aprox), respectivamente. Con respecto al año anterior, el valor la recolección total del tomate ha aumentado un 55%.'
consumed_description = 'El consumo de kg de patatas y naranjas de los españoles en 2020 ha aumentado un 23% y un 51%, respectivamente.'
expense_description = 'El gasto de patatas y naranjas de las familias en 2020 ha aumentado un 27% y un 74%, respectivamente.'

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
                        label='Productos 🥝',
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
                                        className='checklist-filter',
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
                                                                html.H6('Volumen por CCAA'),
                                                                html.Iframe(
                                                                    className='spain-map-iframe',
                                                                    id='products-volume-spain-map-iframe',
                                                                    width='33%',
                                                                    height='300',
                                                                    srcDoc=open('maps/spain-products-volume.html',
                                                                                'r').read()
                                                                ),
                                                                html.Div(
                                                                    className='description',
                                                                    children=[
                                                                        html.P(
                                                                            volume_description
                                                                        )],
                                                                    style={'width': '67%'}
                                                                ),
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
                                                                html.H6('Valor por CCAA'),
                                                                html.Iframe(
                                                                    className='spain-map-iframe',
                                                                    id='products-value-spain-map-iframe',
                                                                    width='33%',
                                                                    height='300',
                                                                    srcDoc=open('maps/spain-products-value.html',
                                                                                'r').read()
                                                                ),
                                                                html.Div(
                                                                    className='description',
                                                                    children=[
                                                                        html.P(
                                                                            value_description
                                                                        )],
                                                                    style={'width': '67%'}
                                                                ),
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
                                                                html.H6('Consumo per capita por CCAA'),
                                                                html.Iframe(
                                                                    className='spain-map-iframe',
                                                                    id='products-consumed-spain-map-iframe',
                                                                    width='33%',
                                                                    height='300',
                                                                    srcDoc=open('maps/spain-products-consumed.html',
                                                                                'r').read()
                                                                ),
                                                                html.Div(
                                                                    className='description',
                                                                    children=[
                                                                        html.P(
                                                                            consumed_description
                                                                        )],
                                                                    style={'width': '67%'}
                                                                ),
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
                                                                html.H6('Gasto per capita por CCAA'),
                                                                html.Iframe(
                                                                    className='spain-map-iframe',
                                                                    id='products-expense-spain-map-iframe',
                                                                    width='33%',
                                                                    height='300',
                                                                    srcDoc=open('maps/spain-products-expense.html',
                                                                                'r').read()
                                                                ),
                                                                html.Div(
                                                                    className='description',
                                                                    children=[
                                                                        html.P(
                                                                            expense_description
                                                                        )],
                                                                    style={'width': '67%'}
                                                                ),
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
                        label='Oferta de Productos 🥕',
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
                                        className='checklist-filter',
                                        children=[
                                            html.Label('CCAA: '),
                                            dcc.Checklist(
                                                id='ccaa-select',
                                                options=[{'label': i, 'value': i} for i in ccaas_filter],
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
                                            html.H6('Precio medio por CCAA'),
                                            html.Iframe(
                                                className='spain-map-iframe',
                                                id='offer-spain-map-iframe',
                                                width='50%',
                                                height='400',
                                                srcDoc=open('maps/spain-offer.html', 'r').read()
                                            ),
                                            dcc.Graph(
                                                'prices-graph',
                                            ),
                                        ]),
                                ]),
                        ]),
                    dcc.Tab(
                        label='Demanda de Productos 🍇',
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
                                        className='checklist-filter',
                                        children=[
                                            html.Label('CCAA: '),
                                            dcc.Checklist(
                                                id='ccaa-select2',
                                                options=[{'label': i, 'value': i} for i in ccaas_filter],
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
                                            html.H6('Consumo per capita por CCAA'),
                                            html.Iframe(
                                                className='spain-map-iframe',
                                                id='demand-spain-map-iframe',
                                                width='50%',
                                                height='400',
                                                srcDoc=open('maps/spain-demand.html', 'r').read()
                                            ),
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
                                        className="checklist-filter",
                                        children=[
                                            html.Label('País: '),
                                            dcc.Checklist(
                                                id='country-select',
                                                options=[{'label': i, 'value': i} for i in countries_filter],
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
                                                        id='measure-select3',
                                                        options=[{'label': i, 'value': i} for i in measures_filter],
                                                        value=measures_filter[0],
                                                        style={'display': 'inline-block'}
                                                    ),
                                                ]),
                                        ]),
                                    dcc.Graph(
                                        'commerce-time-graph',
                                    ),
                                    # dcc.Graph(
                                    #     'eu-map-graph',
                                    # ),
                                    html.Hr(style={'border-top': '3px dotted rosybrown'}),
                                    html.H4('🍅 Por Producto 🍈', style={'padding-top': '25px', 'textAlign': 'center'}),
                                    dcc.Graph(
                                        'commerce-graph',
                                    ),
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
    data1 = du.get_products_data(y_label1, x_label, year, products)
    du.generate_spain_products_map(y_label1, 'spain-products-volume', year, products)
    data2 = du.get_products_data(y_label2, x_label, year, products)
    du.generate_spain_products_map(y_label2, 'spain-products-value', year, products)
    data3 = du.get_products_data(y_label3, x_label, year, products)
    du.generate_spain_products_map(y_label3, 'spain-products-consumed', year, products)
    data4 = du.get_products_data(y_label4, x_label, year, products)
    du.generate_spain_products_map(y_label4, 'spain-products-expense', year, products)
    return [
        gu.make_bar_chart([data1], x_label, [y_label1]),
        gu.make_bar_chart([data2], x_label, [y_label2]),
        gu.make_bar_chart([data3], x_label, [y_label3]),
        gu.make_bar_chart([data4], x_label, [y_label4]),
    ]


@app.callback(
    [Output('prices-graph', 'figure')],
    [Input('year-select', 'value'), Input('ccaa-select', 'value'), Input('family-select', 'value'),
     Input('measure-select', 'value')]
)
def update_offer_graphs(year, ccaas, family, measure):
    y_label3 = 'Precio medio kg'
    name = 'Precio medio kg (' + measure + ')'
    x_label4 = 'Fecha'
    title = 'Volatilidad de los precios 📈: Evolución del precio medio por kg'
    data4 = du.get_generic_product_data(y_label3, x_label4, year, ccaas, family, measure)
    du.generate_spain_map(y_label3, 'spain-offer', year, ccaas, family)
    return [
        gu.make_line_chart([data4], [x_label4], [y_label3], [name], title),
    ]


@app.callback(
    [Output('demand-time-graph', 'figure')],
    [Input('year-select2', 'value'), Input('ccaa-select2', 'value'), Input('family-select2', 'value'),
     Input('measure-select2', 'value')]
)
def update_demand_graphs(year, ccaas, family, measure):
    y_label1 = 'Consumo per capita'
    y_label2 = 'Gasto per capita'
    x_label3 = 'Fecha'
    title = 'Evolución del gasto y del consumo per capita'
    data3 = du.get_generic_product_data(y_label1, x_label3, year, ccaas, family, measure)
    data4 = du.get_generic_product_data(y_label2, x_label3, year, ccaas, family, measure)
    du.generate_spain_map(y_label1, 'spain-demand', year, ccaas, family)
    return [
        gu.make_line_chart([data3, data4], [x_label3, x_label3], [y_label1, y_label2], [measure, measure], title)
    ]


@app.callback(
    [Output('commerce-time-graph', 'figure'), Output('commerce-graph', 'figure')],
    [Input('year-select3', 'value'), Input('country-select', 'value'), Input('indicators-select', 'value'),
     Input('measure-select3', 'value')]
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
    return [
        gu.make_line_chart([data1, data2], [x_label, x_label], [y_label1, y_label2], [name, name], title1),
        gu.make_scatter_chart([data3, data4], [y_label1, y_label2], [name, name], title2, True)
    ]


# ===== END - PLOT GRAPH =====


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
