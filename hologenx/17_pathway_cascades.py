import networkx as nx
import matplotlib.pyplot as plt

# Create a new directed graph
G = nx.DiGraph()

# Define nodes (aging pathways)
nodes = ["NAD Depletion", "Sirtuin Activation", "Telomere Shortening", "Cellular Senescence",
         "mTOR Signaling", "Mitochondrial Dysfunction", "Oxidative Stress", "DNA Damage",
         "Inflammation", "Hormonal Changes", "Metabolic Dysfunction",
         "Microbiome Alterations", "Nutrient Sensing"]

G.add_nodes_from(nodes)

# Define edges (interactions)
edges = [("NAD Depletion", "Mitochondrial Dysfunction"),
         ("Mitochondrial Dysfunction", "Oxidative Stress"),
         ("Oxidative Stress", "DNA Damage"),
         ("DNA Damage", "Cellular Senescence"),
         ("Cellular Senescence", "Inflammation"),
         ("Inflammation", "Metabolic Dysfunction"),
         ("Metabolic Dysfunction", "Hormonal Changes"),
         ("Hormonal Changes", "Inflammation"),
         ("mTOR Signaling", "Cellular Senescence"),
         ("Nutrient Sensing", "mTOR Signaling"),
         ("Sirtuin Activation", "DNA Damage")]

G.add_edges_from(edges)

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_color="lightblue", font_weight="bold", node_size=1500, font_size=14)
nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="grey")
plt.title("Interconnected Aging Pathways", fontsize=18)
plt.show()
