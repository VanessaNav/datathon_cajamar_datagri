import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

colors = ['#2B4162', 'RosyBrown', '#0B6E4F']
line_colors = ['Blue', 'Brown', 'Green']


def make_bar_chart(data, x_label, y_labels):
    fig = make_subplots(rows=1, cols=len(data), shared_xaxes=True, subplot_titles=y_labels)

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


def make_scatter_chart(data, titles):
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)

    for d in range(1, len(data) + 1):
        sizes = data[d - 1].values * 100 / max(data[d - 1].values)
        fig.add_trace(
            go.Scatter(x=data[d - 1].index, y=data[d - 1].values, mode='markers', name=titles[d - 1], marker={
                'size': sizes,
                'color': colors[d - 1],
                'opacity': 0.8,
                'line_color': line_colors[d - 1],
                'line_width': 1,
            }),
            row=1, col=1
        )

        x_ticks = data[d - 1].index.str.slice(stop=30)
        fig.update_xaxes(tickmode='array', tickvals=data[d - 1].index, ticktext=x_ticks, row=1, col=1)

    fig.update_layout(height=600)
    return fig


def make_pie_chart(data, x_labels, y_labels):
    pies_data = []
    for d in range(1, len(data) + 1):
        data_pie = {
            "values": data[d - 1].values,
            "labels": data[d - 1].index,
            "texttemplate": "%{value:,s}",
            "hovertemplate": "%{label}: %{value:,s} <br>(%{percent})",
            "domain": {"column": d - 1},
            "name": x_labels[d - 1],
            "hole": .4,
            "type": "pie"
        }
        pies_data.append(data_pie)

    layout = go.Layout({
        "grid": {"rows": 1, "columns": len(pies_data)},
        "paper_bgcolor": 'rgba(0,0,0,0)',
    })
        # "annotations": [
        #     {
        #         "font": {
        #             "size": 16
        #         },
        #         "showarrow": False,
        #         "text": x_labels[d-1],
        #         "x": 0.22,
        #         "y": 0.5
        #     },
        #     {
        #         "font": {
        #             "size": 16
        #         },
        #         "showarrow": False,
        #         "text": x_label2,
        #         "x": 0.8,
        #         "y": 0.5
        #     }
        # ]
    # })
    fig = go.Figure(data=pies_data, layout=layout)

    return fig
