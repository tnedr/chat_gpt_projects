import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Constants for edge weight
STRONG = 5
MODERATE = 3
WEAK = 1

WEIGHT_MAPPING = {'STRONG': STRONG, 'MODERATE': MODERATE, 'WEAK': WEAK}

# Class definitions
class Node:
    def __init__(self, name, category):
        self.name = name
        self.category = category

class Edge:
    def __init__(self, source, target, interaction, impact, weight):
        self.source = source
        self.target = target
        self.interaction = interaction
        self.impact = impact
        self.weight = weight

# Create node objects
# node_objects = [
#     Node("NAD Levels"),
#     Node("Sirtuin Activation"),
#     Node("mTOR Signaling"),
#     Node("Cellular Senescence"),
#     Node("Oxidative Stress"),
#     Node("Inflammation"),
#     Node("DNA Damage"),
#     Node("Mitochondrial Dysfunction"),
#     Node("AMPK Signaling"),
#     Node("CD38 Activity"),
#     Node("Glycation"),
#     Node("AGEs"),
#     Node("Insulin Sensitivity"),
#     Node("Quercetin")
# ]

# Create edge objects with weight
# edge_objects = [
#     Edge("NAD Levels", "Sirtuin Activation", "increase", "good", STRONG),
#     Edge("CD38 Activity", "NAD Levels", "decrease", "bad", MODERATE),
#     Edge("AMPK Signaling", "NAD Levels", "increase", "good", MODERATE),
#     Edge("AMPK Signaling", "mTOR Signaling", "decrease", "good", MODERATE),
#     Edge("mTOR Signaling", "Cellular Senescence", "increase", "bad", STRONG),
#     Edge("Oxidative Stress", "DNA Damage", "cause", "bad", STRONG),
#     Edge("DNA Damage", "Cellular Senescence", "cause", "bad", STRONG),
#     Edge("Mitochondrial Dysfunction", "Oxidative Stress", "cause", "bad", MODERATE),
#     Edge("Inflammation", "Oxidative Stress", "bi-amplify", "bad", MODERATE),
#     Edge("Oxidative Stress", "Inflammation", "bi-amplify", "bad", MODERATE),
#     Edge("Cellular Senescence", "Inflammation", "increase", "bad", MODERATE),
#     Edge("Sirtuin Activation", "DNA Damage", "decrease", "good", MODERATE),
#     Edge("Glycation", "AGEs", "cause", "bad", STRONG),
#     Edge("AGEs", "Inflammation", "increase", "bad", MODERATE),
#     Edge("AGEs", "Oxidative Stress", "increase", "bad", MODERATE),
#     Edge("AGEs", "Cellular Senescence", "increase", "bad", MODERATE),
#     Edge("AGEs", "DNA Damage", "cause", "bad", MODERATE),
#     Edge("Inflammation", "Inflammation", "increase", "bad", WEAK),
#     Edge("Insulin Sensitivity", "mTOR Signaling", "decrease", "good", MODERATE),
#     Edge("AMPK Signaling", "Insulin Sensitivity", "increase", "good", MODERATE),
#     Edge("Inflammation", "Insulin Sensitivity", "decrease", "bad", MODERATE),
#     Edge("AGEs", "Insulin Sensitivity", "decrease", "bad", MODERATE)
#     Edge("Quercetin", "Oxidative Stress", "decrease", "good", STRONG),
#     Edge("Quercetin", "Inflammation", "decrease", "good", STRONG),
#     Edge("Quercetin", "Cellular Senescence", "decrease", "good", MODERATE),
#     Edge("Quercetin", "Sirtuin Activation", "increase", "good", WEAK),
#     Edge("Quercetin", "AMPK Signaling", "increase", "good", MODERATE),
#     Edge("Quercetin", "Insulin Sensitivity", "increase", "good", MODERATE),
#     Edge("Quercetin", "DNA Damage", "decrease", "good", WEAK)
# ]


# Initialize NetworkX graph

def load_nodes_and_edges():
    # Load nodes
    df_nodes = pd.read_csv("network/nodes.csv")
    node_objects = [Node(row['name'], row['category']) for index, row in df_nodes.iterrows()]

    # Load edges
    df_edges = pd.read_csv("network/edges.csv")

    # Replace string constants with numerical weights
    df_edges['weight'] = df_edges['weight'].map(WEIGHT_MAPPING)

    edge_objects = [
        Edge(
            row['source'],
            row['target'],
            row['interaction'],
            row['impact'],
            row['weight']
        ) for index, row in df_edges.iterrows()
    ]

    return node_objects, edge_objects

node_objects, edge_objects = load_nodes_and_edges()




plt.figure(figsize=(15, 6))
G = nx.DiGraph()

# Add nodes to graph
G.add_nodes_from([node.name for node in node_objects])

# Add edges to graph
G.add_edges_from([(edge.source, edge.target,
        {'interaction': edge.interaction, 'impact': edge.impact, 'weight': edge.weight}
                   ) for edge in edge_objects])



level0 = 2
level1 = 1
level2 = 0
level3 = -1
level4 = -2


collll = -2
colll = -1.5
coll = -1
col0 = -0.5
colr = 0
colrr = 0.5
colrrr = 1



# Node positions and attributes
pos = {

    'CD38 Activity': (collll, level0),
    'Mitochondrial Dysfunction': (col0, level0),
    'Glycation': (colrr, level0),
    'AMPK Signaling': (collll, level2),

    'Insulin Sensitivity': (coll, level3),

    'NAD Levels': (colll, level1),
    'Oxidative Stress': (col0, level1),
    'AGEs': (colrr, level1),

    'Quercetin': (colll, level0),

    'Sirtuin Activation': (coll, level2),


    'DNA Damage': (col0, level3),

    'mTOR Signaling': (colll, level4),
    'Cellular Senescence': (colr, level4),
    'Inflammation': (colrr, level3),

}
arrowstyle = "->,head_length=1,head_width=0.5"
# Draw graph
edge_colors = ['green' if G[u][v]['impact'] == 'good' else 'red' for u, v in G.edges()]
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]


nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold',
        node_size=700, font_size=18, edge_color=edge_colors, width=edge_weights,
        arrows=True, connectionstyle='arc3,rad=0.1', arrowstyle=arrowstyle)
labels = nx.get_edge_attributes(G, 'interaction')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show()
