from typing import Any, List

import dash
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output
from pydantic import BaseModel, conlist, validator


class Node(BaseModel):
    id: int
    label: str


class Edge(BaseModel):
    source: int
    target: int


class GraphData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

    @validator('edges')
    def validate_edges(cls, edges, values):
        if 'nodes' in values:
            node_ids = {node.id for node in values['nodes']}
            for edge in edges:
                if edge.source not in node_ids or edge.target not in node_ids:
                    raise ValueError('Edge source or target does not exist in nodes')
        return edges


def construct_plot(graph_data: GraphData):
    fig = go.Figure(layout=go.Layout(
        paper_bgcolor='rgb(23, 27, 31)',
        plot_bgcolor='rgb(23, 27, 31)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    ))

    nodes_df = pd.DataFrame([node.dict() for node in graph_data.nodes])
    edges_df = pd.DataFrame([edge.dict() for edge in graph_data.edges])

    for i, edge in edges_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[nodes_df.loc[nodes_df['id'] == edge['source'], 'label'].values[0],
               nodes_df.loc[nodes_df['id'] == edge['target'], 'label'].values[0]],
            y=[0, 0],
            mode='lines',
            line=dict(width=2, color='blue'),
            hoverinfo='none'
        ))

    fig.add_trace(go.Scatter(
        x=nodes_df['label'],
        y=[0]*len(nodes_df),
        mode='markers+text',
        marker=dict(size=20, color='red'),
        text=nodes_df['label'],
        hoverinfo='text',
        textposition='bottom center'
    ))

    return fig

def setup_dash_app(fig):
    app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

    app.layout = html.Div(className="container", style={'backgroundColor': '#1E1E1E'}, children=[
        html.Link(rel='stylesheet', href="styles.css", type='text/css'),
        html.H1("Knowledge Graph with Plotly and Dash", style={'color': 'white'}),
        dcc.Graph(id='knowledge-graph', figure=fig),
        html.P(id='click-data', style={'color': 'white'})
    ])

    @app.callback(
        Output('click-data', 'children'),
        Input('knowledge-graph', 'clickData'))
    def display_click_data(clickData):
        if clickData is not None:
            clicked_point_label = clickData['points'][0]['text']
            return f"You clicked on {clicked_point_label}"
        return "Click on a node to see it here."
    
    return app

def main():
    # Sample data for nodes and edges
    graph_data = GraphData(
        nodes=[
            Node(id=1, label='Node 1'),
            Node(id=2, label='Node 2'),
            Node(id=3, label='Node 3')
        ],
        edges=[
            Edge(source=1, target=2),
            Edge(source=2, target=3)
        ]
    )

    fig = construct_plot(graph_data)
    app = setup_dash_app(fig)
    app.run_server(debug=True)

if __name__ == '__main__':
    main()
