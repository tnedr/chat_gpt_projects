import networkx as nx
import matplotlib.pyplot as plt

# Create a larger figure size
plt.figure(figsize=(15, 10))

# Create a directed graph
G = nx.DiGraph()

# Add nodes
nodes = ["Sugar Metabolism", "Lipid Peroxidation", "ROS Formation",
         "Maillard Reaction", "Reactive Carbonyls", "Protein Modification",
         "Glycation", "Formation of AGEs", "Cellular Dysfunction",
         "Tissue Damage", "Chronic Diseases"]

G.add_nodes_from(nodes)

# Add edges (arrows)
edges = [("Sugar Metabolism", "Maillard Reaction"),
         ("Sugar Metabolism", "Reactive Carbonyls"),
         ("Lipid Peroxidation", "Reactive Carbonyls"),
         ("Lipid Peroxidation", "ROS Formation"),
         ("ROS Formation", "Lipid Peroxidation"),
         ("ROS Formation", "Protein Modification"),
         ("Maillard Reaction", "Glycation"),
         ("Reactive Carbonyls", "Protein Modification"),
         ("Protein Modification", "Formation of AGEs"),
         ("Glycation", "Formation of AGEs"),
         ("Formation of AGEs", "Cellular Dysfunction"),
         ("Formation of AGEs", "Tissue Damage"),
         ("Cellular Dysfunction", "Chronic Diseases"),
         ("Tissue Damage", "Chronic Diseases")]

edge_labels = {
    ("Sugar Metabolism", "Maillard Reaction"): 'ALA',
    ("Sugar Metabolism", "Reactive Carbonyls"): 'ALA',
    ("Lipid Peroxidation", "Reactive Carbonyls"): 'Vitamin E',
    ("Lipid Peroxidation", "ROS Formation"): 'Vitamin E',
    ("ROS Formation", "Lipid Peroxidation"): 'Vitamin E',
    ("ROS Formation", "Protein Modification"): 'ALA',
    ("Maillard Reaction", "Glycation"): 'Pyridoxamine',
    ("Reactive Carbonyls", "Protein Modification"): 'Pyridoxamine',
    ("Protein Modification", "Formation of AGEs"): '',
    ("Glycation", "Formation of AGEs"): '',
    ("Formation of AGEs", "Cellular Dysfunction"): 'Carnosine',
    ("Formation of AGEs", "Tissue Damage"): 'Carnosine',
    ("Cellular Dysfunction", "Chronic Diseases"): '',
    ("Tissue Damage", "Chronic Diseases"): ''
}


G.add_edges_from(edges)

# Draw the graph
# pos = nx.spring_layout(G, seed=42, iterations=100)
# pos = nx.planar_layout(G)
pos = nx.fruchterman_reingold_layout(G)

# pos = nx.circular_layout(G)
# pos = nx.kamada_kawai_layout(G)
# pos = nx.shell_layout(G)
# pos = nx.spectral_layout(G)
# pos = nx.random_layout(G)
# pos = nx.spiral_layout(G)

# Draw the graph
# pos = nx.spring_layout(G, seed=42)  # positions for all nodes
labels = {node: node for node in G.nodes()}

nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', font_size=10, font_color='black',
        font_weight='bold', node_size=1500, arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
plt.title("Elements and Processes Related to AGEs")
plt.show()