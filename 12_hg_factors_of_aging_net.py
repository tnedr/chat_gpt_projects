import networkx as nx
import matplotlib.pyplot as plt

# Create a new directed graph
G = nx.DiGraph()

# Define the nodes and their properties
nodes = [
    "Cellular Energy Production (NAD+)",
    "NAD Depletion Control (CD38)",
    "DNA Repair and Regulation (Sirtuins)",
    "Anti-Glycation Control",
    "Cellular Senescence Control (Senolytics)",
    "Telomere Maintenance (Telomerase)",
    "Oxidative Stress Management (Antioxidants)",
    "Mitochondrial Dysfunction",
    "Hormonal Imbalance",
    "Inflammation Control",
    "Nutrient Sensing and Metabolism (mTOR, AMPK)",
    "Epigenetic Alterations"
]

# Add nodes to the graph
G.add_nodes_from(nodes)

# Define the edges and their properties
edges = [
    ("Cellular Energy Production (NAD+)", "Mitochondrial Dysfunction"),
    ("NAD Depletion Control (CD38)", "Cellular Energy Production (NAD+)"),
    ("DNA Repair and Regulation (Sirtuins)", "Oxidative Stress Management (Antioxidants)"),
    ("Anti-Glycation Control", "Inflammation Control"),
    ("Cellular Senescence Control (Senolytics)", "Telomere Maintenance (Telomerase)"),
    ("Telomere Maintenance (Telomerase)", "DNA Repair and Regulation (Sirtuins)"),
    ("Oxidative Stress Management (Antioxidants)", "Mitochondrial Dysfunction"),
    ("Hormonal Imbalance", "Cellular Energy Production (NAD+)"),
    ("Inflammation Control", "Hormonal Imbalance"),
    ("Nutrient Sensing and Metabolism (mTOR, AMPK)", "Cellular Energy Production (NAD+)"),
    ("Epigenetic Alterations", "DNA Repair and Regulation (Sirtuins)")
]

# Add edges to the graph
G.add_edges_from(edges)

# Draw the graph
plt.figure(figsize=(16, 12))
pos = nx.spring_layout(G, seed=42)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=3000, font_size=10, font_color='black', font_weight='bold', arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Interconnected Web of Molecular Aging Factors")
plt.show()
