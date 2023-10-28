import networkx as nx
import matplotlib.pyplot as plt


plt.figure(figsize=(15, 6))

# Create a directed graph
G = nx.DiGraph()

# Add nodes
nodes = ['NAD Levels', 'Sirtuin Activation', 'mTOR Signaling', 'Cellular Senescence',
         'Oxidative Stress', 'Inflammation', 'DNA Damage', 'Mitochondrial Dysfunction',
         'AMPK Signaling', 'CD38 Activity']

G.add_nodes_from(nodes)

# Add edges with attributes for interaction and confidence
edges = [
    ('NAD Levels', 'Sirtuin Activation', {'interaction': 'upregulates'}),
    ('CD38 Activity', 'NAD Levels', {'interaction': 'downregulates'}),
    ('AMPK Signaling', 'NAD Levels', {'interaction': 'upregulates'}),
    ('AMPK Signaling', 'mTOR Signaling', {'interaction': 'downregulates'}),
    ('mTOR Signaling', 'Cellular Senescence', {'interaction': 'upregulates'}),
    ('Oxidative Stress', 'DNA Damage', {'interaction': 'causes'}),
    ('DNA Damage', 'Cellular Senescence', {'interaction': 'causes'}),
    ('Mitochondrial Dysfunction', 'Oxidative Stress', {'interaction': 'causes'}),
    ('Inflammation', 'Oxidative Stress', {'interaction': 'upregulates'}),
    ('Cellular Senescence', 'Inflammation', {'interaction': 'upregulates'}),
    ('Sirtuin Activation', 'DNA Damage', {'interaction': 'downregulates'}),
]

G.add_edges_from(edges)

# Define positions directly using a dictionary
pos = {

    'CD38 Activity': (-2, 2),
    'NAD Levels': (-1.5, 0),
    'DNA Damage': (0, 0),
    'Mitochondrial Dysfunction': (1, 2),

    'Sirtuin Activation': (-0.5, 1),
    'mTOR Signaling': (-.5, -2),
    'Cellular Senescence': (1, -2),
    'Oxidative Stress': (0.5, 1.5),
    'Inflammation': (1.5, -1),

    'AMPK Signaling': (-2, -1),
}

# Define color map for edges
edge_colors = ['green' if G[u][v]['interaction'] == 'upregulates' else 'red' if G[u][v]['interaction'] == 'downregulates' else 'blue' for u, v in G.edges()]

# Draw the network
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold',
        node_size=700, font_size=18, edge_color=edge_colors)
labels = nx.get_edge_attributes(G, 'interaction')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show()
