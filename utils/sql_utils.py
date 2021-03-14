import pandas as pd


# def read_datasets():
df1 = pd.read_csv('data/Dataset1.txt', sep='|')
df2 = pd.read_csv('data/Dataset2.txt', sep='|')
df3 = pd.read_csv('data/Dataset3.txt', sep='|')
df4 = pd.read_csv('data/Dataset4.txt', sep='|')
df5 = pd.read_csv('data/Dataset5.txt', sep='|')
# return [df1, df2, df3, df4, df5]


def get_product_filters():
    years_filter = ['Todos'] + df1['Año'].unique().tolist()
    ccaas_filter = df1['CCAA'].unique()
    families_filter = ['F&H', 'Frutas', 'Hortalizas']
    return [years_filter, ccaas_filter, families_filter]


def get_commerce_filters():
    countries_filter = df4['REPORTER'].unique().tolist()
    indicators_filter = df4['INDICATORS'].unique()
    return [countries_filter, indicators_filter]


def get_product_data(column, year, ccaas, family):
    conditions = filter_product_data(year, ccaas, family)
    if conditions is not None:
        data = df1[conditions].groupby('Producto')[column].sum()
    else:
        data = df1.groupby('Producto')[column].sum()
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


def get_commerce_data(flow, countries, indicator):
    conditions = filter_commerce_data(flow, countries, indicator)
    data = df4[conditions].groupby('PRODUCT')['Value'].sum()

    return data


def filter_commerce_data(flow, countries, indicator):
    if len(countries) == 0:
        conditions = (df4['FLOW'] == flow) & (df4['INDICATORS'] == indicator)
    else:
        conditions = (df4['FLOW'] == flow) & (df4['REPORTER'].isin(countries)) & (df4['INDICATORS'] == indicator)
    return conditions
