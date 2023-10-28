import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Create a Pandas DataFrame for the effect matrix
data = {
    'Ingredient': ['NR', 'Resveratrol', 'Quercetin'],
    'NAD+ Boosting': ['High', 'Low', 'Medium'],
    'Sirtuin Activation': ['Low', 'High', 'Medium'],
    'Metabolic Health': ['Medium', 'Medium', 'High'],
    'Hormone Regulation': ['Low', 'Low', 'Medium'],
    'Cellular Senescence': ['Low', 'Medium', 'High'],
}

df = pd.DataFrame(data)

# Create an empty graph
G = nx.Graph()

# Add nodes and edges to the graph based on the DataFrame
for idx, row in df.iterrows():
    ingredient = row['Ingredient']
    G.add_node(ingredient, node_type='ingredient')
    for pathway, strength in list(row.items())[1:]:
        G.add_node(pathway, node_type='pathway')
        weight_mapping = {'High': 3, 'Medium': 2, 'Low': 1}
        G.add_edge(ingredient, pathway, weight=weight_mapping.get(strength, 0))
        # G.add_edge(ingredient, pathway, weight=strength)

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # positions for all nodes

# Draw nodes
nx.draw_networkx_nodes(G, pos, nodelist=[n for n, attr in G.nodes(data=True) if attr['node_type'] == 'ingredient'], node_color='r', node_size=700, label='Ingredients')
nx.draw_networkx_nodes(G, pos, nodelist=[n for n, attr in G.nodes(data=True) if attr['node_type'] == 'pathway'], node_color='g', node_size=700, label='Pathways')

# Draw edges with different thickness based on weight
for node1, node2, attr in G.edges(data=True):
    weight = attr['weight']
    if weight == 3:
        nx.draw_networkx_edges(G, pos, edgelist=[(node1, node2)], width=4)
    elif weight == 2:
        nx.draw_networkx_edges(G, pos, edgelist=[(node1, node2)], width=2)
    elif weight == 1:
        nx.draw_networkx_edges(G, pos, edgelist=[(node1, node2)], width=1)

# Labels
nx.draw_networkx_labels(G, pos)

# Legend
plt.legend()

# Show the graph
plt.show()
