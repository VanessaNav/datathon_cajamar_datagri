import pandas as pd
import folium


# Fuentes de datos externas
# http://centrodedescargas.cnig.es/CentroDescargas/catalogo.do?Serie=CAANE
# https://www.kaggle.com/paultimothymooney/latitude-and-longitude-for-every-country-and-state

# def read_datasets():
df1 = pd.read_csv('data/Dataset1.txt', sep='|')
df2 = pd.read_csv('data/Dataset2.txt', sep='|')
df3 = pd.read_csv('data/Dataset3.txt', sep='|')
df4 = pd.read_csv('data/Dataset4.txt', sep='|')
df5 = pd.read_csv('data/Dataset5.txt', sep='|')
# return [df1, df2, df3, df4, df5]
spain_coordinates = [40.416775, -3.703790]

def get_product_filters():
    years_filter = ['Todos'] + df1['Año'].unique().tolist()
    ccaas_filter = df1['CCAA'].unique()
    families_filter = ['F&H', 'Frutas', 'Hortalizas']
    return [years_filter, ccaas_filter, families_filter]


def get_commerce_filters():
    countries_filter = df4['REPORTER'].unique().tolist()
    indicators_filter = df4['INDICATORS'].unique()
    return [countries_filter, indicators_filter]


def get_product_data(column, group_col, year, ccaas, family, measure):
    conditions = filter_product_data(year, ccaas, family)
    if conditions is not None:
        if group_col == 'Fecha' and measure == 'Tasa de variación':
            data = pd.Series.pct_change(df1[conditions].groupby(group_col)[column].mean())
        else:
            data = df1[conditions].groupby(group_col)[column].mean()
    else:
        if group_col == 'Fecha' and measure == 'Tasa de variación':
            data = pd.Series.pct_change(df1.groupby(group_col)[column].mean())
        else:
            data = df1.groupby(group_col)[column].mean()
    return data


def filter_product_data(year, ccaas, family):
    if (len(ccaas) == 0) and (family == 'F&H') and (year == 'Todos'):
        return None
    else:
        if (len(ccaas) > 0) and (family == 'F&H') and (year == 'Todos'):  # 1: CCAA
            conditions = df1['CCAA'].isin(ccaas)
        elif (len(ccaas) == 0) and (family != 'F&H') and (year == 'Todos'):  # 2: Familia
            products = df3[df3['familia'].str.contains(family, na=False, case=False)]['product'].unique()
            conditions = df1['Producto'].isin(products)
        elif (len(ccaas) > 0) and (family != 'F&H') and (year == 'Todos'):  # 3: CCAA y Familia
            products = df3[df3['familia'].str.contains(family, na=False, case=False)]['product'].unique()
            conditions = (df1['CCAA'].isin(ccaas)) & (df1['Producto'].isin(products))
        elif (len(ccaas) == 0) and (family == 'F&H') and (year != 'Todos'):  # 4: Año
            conditions = (df1['Año'] == year)
        elif (len(ccaas) > 0) and (family == 'F&H') and (year != 'Todos'):  # 5: CCAA y Año
            conditions = (df1['CCAA'].isin(ccaas)) & (df1['Año'] == year)
        elif (len(ccaas) == 0) and (family != 'F&H') and (year != 'Todos'):  # 6: Familia y Año
            products = df3[df3['familia'].str.contains(family, na=False, case=False)]['product'].unique()
            conditions = (df1['Producto'].isin(products)) & (df1['Año'] == year)
        else:  # 7: CCAA, Familia y Año
            products = df3[df3['familia'].str.contains(family, na=False, case=False)]['product'].unique()
            conditions = (df1['CCAA'].isin(ccaas)) & (df1['Producto'].isin(products)) & (df1['Año'] == year)

    return conditions


def get_commerce_data(group_col, column, flow, year, countries, indicator, measure):
    conditions = filter_commerce_data(flow, year, countries, indicator)
    if group_col == 'DATE':
        if measure == 'Tasa de variación':
            data = pd.Series.pct_change(df4[conditions].groupby(group_col)[column].mean())
        else:
            data = df4[conditions].groupby(group_col)[column].mean()
    else:
        data = df4[conditions].groupby(group_col)[column].sum()

    return data


def filter_commerce_data(flow, year, countries, indicator):
    if (len(countries) == 0) & (year == 'Todos'):  # 0: sin año ni paises
        conditions = (df4['FLOW'] == flow) & (df4['INDICATORS'] == indicator)
    elif (len(countries) > 0) & (year == 'Todos'):  # 1: paises
        conditions = (df4['FLOW'] == flow) & (df4['INDICATORS'] == indicator) & (df4['REPORTER'].isin(countries))
    elif (len(countries) == 0) & (year != 'Todos'):  # 2: año
        conditions = (df4['FLOW'] == flow) & (df4['INDICATORS'] == indicator) & (df4['Y'] == year)
    else:  # 4: año y paises
        conditions = (df4['FLOW'] == flow) & (df4['INDICATORS'] == indicator) & (df4['REPORTER'].isin(countries)) & \
                     (df4['Y'] == year)
    return conditions


def generate_spain_map(column, map_name, year, ccaas, family):
    conditions = filter_product_data(year, ccaas, family)
    if conditions is not None:
        data = df1[conditions]
    else:
        data = df1
    # file name - file is located in the working directory
    communities_geo = r'data/spain-communities.geojson'  # geojson file
    # create a plain world map
    communities_map = folium.Map(location=spain_coordinates, zoom_start=5, tiles='cartodbpositron')
    # generate choropleth map
    communities_map.choropleth(
        geo_data=communities_geo,
        data=data,
        columns=['CCAA', column],
        key_on='feature.properties.name',
        fill_color="BuPu",
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name=column,
        smooth_factor=0)
    communities_map.save('maps/' + map_name + '.html')
