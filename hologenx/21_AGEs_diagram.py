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


# positions for all nodes
labels = {node: node for node in G.nodes()}

nx.draw(G, pos, with_labels=True, labels=labels,
        node_color='skyblue', font_size=12, font_color='black', font_weight='bold',
        node_size=2000, edgecolors='black',
        arrowsize=20, width=2)

plt.title("Elements and Processes Related to AGEs", fontsize=16)
plt.show()
