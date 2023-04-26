import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pickle
import json


def get_data_from_row(row):
    name, chromosome, start, end, length =\
        row['Display Name'], row['Chromosome Number'],\
        row['Chromosome Start Point'], row['Chromosome End Point'],\
        row['Chromosome End Point'] - row['Chromosome Start Point']
    return name, chromosome, start, end, length

def create_nodes_and_connections(filename, graph_filename):

    df = pd.read_csv(filename)

    persons = df['Display Name'].unique()
    persons = np.insert(persons, 0, 'User')
    G = nx.Graph()

    # add all persons as nodes to graph
    for person in persons:
        G.add_node(person, name=person)

    # add edges
    for _, row1 in df.iterrows():
        p1, chromosome1, start1, end1, length1 =\
            get_data_from_row(row1)

        p1 = row1['Display Name']
        print(p1)
        # add edge with the user
        # G.add_edge(p1, 'User', segments='11,2')
        G.add_edge(p1, 'User', segments=str([{
            'chromosome': chromosome1,
            'start': start1,
            'end': end1,
            'length': length1
        }]))
        for _, row2 in df[df.index > row1.name].iterrows():
            if row1['Chromosome Number'] == row2['Chromosome Number']:
                p2, chromosome2, start2, end2, length2 = \
                    get_data_from_row(row2)

                shared_start = max(start1, start2)
                shared_end = min(end1, end2)
                shared_length = max(0, shared_end - shared_start)

                if shared_length > 0:
                    new_segment = str({'chromosome': chromosome1,
                                       'start': shared_start,
                                       'end': shared_end,
                                       'length': shared_length})
                    if G.has_edge(p1, p2):
                        G.edges[p1, p2]['segments'] = G.edges[p1, p2]['segments'] + new_segment
                    else:
                        G.add_edge(p1, p2, segments=new_segment)


    nx.write_graphml(G, graph_filename + '.graphml')
    nx.write_gexf(G, graph_filename + '.gexf')
    with open(graph_filename + '.pkl', 'wb') as f:
         pickle.dump(G, f)
    return G



def visualize_graph(graph):
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(10, 10))
    nx.draw(graph, pos, node_color='lightblue', with_labels=True, node_size=3000, font_size=10)
    plt.title('Shared DNA Network')
    plt.show()


def visualize_graph2(G=None, graph_filename=None):

    if G is None:
        with open(graph_filename + '.pkl', 'rb') as f:
            G = pickle.load(f)

        data = nx.node_link_data(G)
        # write the dictionary as a JSON file
        with open('graph222.json', 'w') as f:
            json.dump(data, f, indent=4)



    # convert the graph to a Plotly graph object
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    # set the node color based on the degree of the node
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f'{node}<br># of connections: {len(adjacencies[1])}')
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # create the Plotly figure and add the traces
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='My Network Graph',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    # show the Plotly figure
    fig.show()


# filename = 'input/shared_dna.csv'
filename = 'input/Tamas_Nagy_relatives_download.csv'
graph_filename = '23andme_relative_graph'
G = create_nodes_and_connections(filename, graph_filename)
visualize_graph2(None, graph_filename)