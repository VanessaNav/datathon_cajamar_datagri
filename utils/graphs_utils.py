import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

colors = ['#2B4162', 'RosyBrown', '#0B6E4F']
line_colors = ['Black', 'Brown', 'Green']

# Prepare maps
spain_coordinates = [40.416775, -3.703790]
eu_coordinates = [48.499998, 23.3833318]
# file name - file is located in the working directory
communities_geo = r'data/spain-communities.geojson'  # geojson file
eu_geo = r'data/europe-filtered.geojson'  # geojson file


def make_bar_chart(data, x_label, y_labels, titles):
    fig = make_subplots(rows=1, cols=len(data), shared_xaxes=True, subplot_titles=titles)

    for d in range(1, len(data) + 1):
        fig.add_trace(
            go.Bar(x=data[d - 1].index, y=data[d - 1].values, name=y_labels[d - 1]),
            row=1, col=d
        )
        fig.update_yaxes(title=y_labels[d - 1], row=1, col=d)
        fig.update_traces(row=1, col=d, marker_color=colors[d - 1], marker_line_color=line_colors[d - 1],
                          marker_line_width=1, opacity=0.8)

    fig.update_xaxes(title=x_label, row=1, col=1)

    return fig


def make_line_chart(data, x_labels, y_labels, names, title, add_vlines=False):
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    text_positions = ['top center', 'bottom center']

    for d in range(1, len(data) + 1):
        texts = np.around(data[d - 1].values, 2)
        if d % 2 != 0:
            text_position = text_positions[0]
        else:
            text_position = text_positions[1]
        fig.add_trace(
            go.Scatter(x=data[d - 1].index, y=data[d - 1].values, mode='lines+markers+text', name=y_labels[d - 1],
                       text=texts, textposition=text_position, textfont_size=8,
                       line={'color': colors[d - 1], 'width': 5},
                       marker={'color': line_colors[d - 1]}),
            row=1, col=1
        )
        fig.update_xaxes(title=x_labels[d - 1], row=1, col=1)
        fig.update_yaxes(title=names[d - 1], row=1, col=1)

    fig.update_layout(title={
        'text': title,
        'font_size': 12
    })
    if add_vlines:
        years = [i[:4] for i in data[0].index]
        for year in set(years):
            fig.add_vline(x=year, line_width=2, line_dash="dash", line_color='#666')

    return fig


def make_scatter_chart(data, y_labels, x_labels, names, title, slice_indexes=False):
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)

    for d in range(1, len(data) + 1):
        sizes = data[d - 1].values * 100 / max(data[d - 1].values)
        fig.add_trace(
            go.Scatter(x=data[d - 1].index, y=data[d - 1].values, mode='markers', name=y_labels[d - 1], marker={
                'size': sizes,
                'color': colors[d - 1],
                'opacity': 0.8,
                'line_color': line_colors[d - 1],
                'line_width': 1,
            }),
            row=1, col=1
        )
        fig.update_yaxes(title=names[d - 1], row=1, col=1)
        if slice_indexes:
            x_ticks = data[d - 1].index.str.slice(stop=30)
            fig.update_xaxes(title=x_labels[d - 1], showticklabels=False,
                             tickmode='array', tickvals=data[d - 1].index, ticktext=x_ticks,
                             row=1, col=1)

    fig.update_layout(height=600, title=title)
    return fig


def generate_spain_map(data, column):
    fig = go.Figure(go.Choroplethmapbox(
        geojson=communities_geo,
        z=data[column],
        locations=data['CCAA'],
        zmin=data[column].min(),
        zmax=data[column].max(),
        colorscale="amp",
        featureidkey='properties.name',
    ))
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=3,
                      mapbox_center={"lat": spain_coordinates[0], "lon": spain_coordinates[1]})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


def generate_eu_map(data, column):
    fig = go.Figure(go.Choroplethmapbox(
        geojson=eu_geo,
        z=data[column],
        locations=data['REPORTER'],
        zmin=data[column].min(),
        zmax=data[column].max(),
        colorscale="amp",
        featureidkey='properties.name',
    ))
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=3,
                      mapbox_center={"lat": eu_coordinates[0], "lon": eu_coordinates[1]})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig
