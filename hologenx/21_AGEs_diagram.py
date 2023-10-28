import networkx as nx
import matplotlib.pyplot as plt

# Create a larger figure size
plt.figure(figsize=(15, 10))

# Create a directed graph
G = nx.DiGraph()

# Add nodes
nodes = ["Sugar Metabolism", "Lipid Peroxidation", "ROS Formation",
         "Reactive Carbonyls", "Protein Modification", "Maillard Reaction",
         "Glycation", "Formation of AGEs", "RAGE", "Cellular Dysfunction",
         "Tissue Damage", "Chronic Diseases"]

G.add_nodes_from(nodes)

# Add edges (arrows)
edges = [("Sugar Metabolism", "Reactive Carbonyls", {"label": "Berberine, Metformin"}),
         ("Lipid Peroxidation", "Reactive Carbonyls", {"label": "NAC, Vitamin E"}),
         ("Lipid Peroxidation", "ROS Formation", {"label": "Vitamin E"}),
         ("ROS Formation", "Reactive Carbonyls", {"label": "ALA, NAC"}),
         ("Reactive Carbonyls", "Protein Modification", {"label": "Pyridoxamine, Aminoguanidine"}),
         ("Reactive Carbonyls", "Maillard Reaction", {"label": "Pyridoxamine, Aminoguanidine"}),
         ("Maillard Reaction", "Glycation", {"label": "Carnosine, Beta-Alanine"}),
         ("Protein Modification", "Formation of AGEs", {"label": "Carnosine, Beta-Alanine"}),
         ("Glycation", "Formation of AGEs", {"label": "Carnosine, Beta-Alanine"}),
         ("Formation of AGEs", "RAGE", {"label": "Thymoquinone"}),
         ("Formation of AGEs", "Cellular Dysfunction", {"label": "Alagebrium"}),
         ("Formation of AGEs", "Tissue Damage", {"label": "Alagebrium"}),
         ("Cellular Dysfunction", "Chronic Diseases", {"label": "Benfotiamine"}),
         ("Tissue Damage", "Chronic Diseases", {"label": "Benfotiamine"}),
            ("RAGE", "Cellular Dysfunction", {"label": "Direct Effect"}),
             ("RAGE", "Tissue Damage", {"label": "Direct Effect"}),
             ("RAGE", "Chronic Diseases", {"label": "Direct Effect"})

         ]

G.add_edges_from([(src, tgt, attr) for src, tgt, attr in edges])

# Draw the graph
# pos = nx.spring_layout(G, seed=42, iterations=100)
pos = nx.planar_layout(G)
# pos = nx.fruchterman_reingold_layout(G)

# pos = nx.circular_layout(G)
# pos = nx.kamada_kawai_layout(G)
# pos = nx.shell_layout(G)
# pos = nx.spectral_layout(G)
# pos = nx.random_layout(G)
# pos = nx.spiral_layout(G)

# Draw the graph
# pos = nx.spring_layout(G, seed=42)  # positions for all nodes

labels = {node: node for node in G.nodes()}
nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', font_size=10,
        font_color='black', font_weight='bold', node_size=1500, arrows=True)
edge_labels = {(src, tgt): attr["label"] for src, tgt, attr in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.title("Elements and Processes Related to AGEs with Inhibiting Compounds")
plt.show()