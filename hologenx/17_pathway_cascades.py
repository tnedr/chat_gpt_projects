import networkx as nx
import matplotlib.pyplot as plt

# Class definitions
class Node:
    def __init__(self, name):
        self.name = name

class Edge:
    def __init__(self, source, target, interaction):
        self.source = source
        self.target = target
        self.interaction = interaction

# Create node objects
node_objects = [
    Node("NAD Levels"),
    Node("Sirtuin Activation"),
    Node("mTOR Signaling"),
    Node("Cellular Senescence"),
    Node("Oxidative Stress"),
    Node("Inflammation"),
    Node("DNA Damage"),
    Node("Mitochondrial Dysfunction"),
    Node("AMPK Signaling"),
    Node("CD38 Activity"),
    Node("Glycation"),
    Node("AGEs")
]

# Create edge objects
edge_objects = [
    Edge("NAD Levels", "Sirtuin Activation", "increase"),
    Edge("CD38 Activity", "NAD Levels", "decrease"),
    Edge("AMPK Signaling", "NAD Levels", "increase"),
    Edge("AMPK Signaling", "mTOR Signaling", "decrease"),
    Edge("mTOR Signaling", "Cellular Senescence", "increase"),
    Edge("Oxidative Stress", "DNA Damage", "cause"),
    Edge("DNA Damage", "Cellular Senescence", "cause"),
    Edge("Mitochondrial Dysfunction", "Oxidative Stress", "cause"),
    Edge("Inflammation", "Oxidative Stress", "increase"),
    Edge("Cellular Senescence", "Inflammation", "increase"),
    Edge("Sirtuin Activation", "DNA Damage", "decrease"),
    Edge("Glycation", "AGEs", "cause"),  # Glycation leads to the formation of AGEs
    Edge("AGEs", "Inflammation", "increase"),  # AGEs can increase inflammation
    Edge("AGEs", "Oxidative Stress", "increase"),  # AGEs can also increase oxidative stress
    Edge("AGEs", "Cellular Senescence", "increase"),  # AGEs can accelerate cellular senescence
    Edge("AGEs", "DNA Damage", "cause")
]

# Initialize NetworkX graph
plt.figure(figsize=(15, 6))
G = nx.DiGraph()

# Add nodes to graph
G.add_nodes_from([node.name for node in node_objects])

# Add edges to graph
G.add_edges_from([(edge.source, edge.target, {'interaction': edge.interaction}) for edge in edge_objects])

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
    'Glycation': (col0, level0),
    'Mitochondrial Dysfunction': (colrrr, level0),

    'NAD Levels': (colll, level1),
    'AGEs': (col0, level1),
    'Oxidative Stress': (colrr, level1),

    'Sirtuin Activation': (coll, level2),
    'AMPK Signaling': (collll, level2),

    'DNA Damage': (col0, level3),

    'mTOR Signaling': (colll, level4),
    'Cellular Senescence': (1, -2),
    'Inflammation': (1.5, -1),

}

# Draw graph
edge_colors = ['green' if G[u][v]['interaction'] == 'increase' else 'red' for u, v in G.edges()]
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, font_size=18, edge_color=edge_colors)
labels = nx.get_edge_attributes(G, 'interaction')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show()
