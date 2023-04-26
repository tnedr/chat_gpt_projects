import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt



'''
our relevance is the number of shared dna with the user
shared dna as connection
sharing dna means have connections
if we have a, b, ab, bc, c then we have 4 connections: a-ab, b-ab, b-bc, c-bc
in our case the connection mean, to share genetic material
In this way we can separate branches of the family tree

'''

def euclidean_distance(v1, v2):
    return ((v1 - v2) ** 2).sum() ** 0.5


def calculate_genetic_similarity(segment_lengths):
    return 1 / (1 + segment_lengths)


df = pd.read_csv('input/shared_dna.csv')

persons = df['DisplayName'].unique()
user = 'User'
persons = np.append(persons, user)
segments_lengths = []

for p1 in persons:
    p1_segments = df[df['DisplayName'] == p1] if p1 != user else pd.DataFrame()
    p1_lengths = []

    for p2 in persons:
        if p1 == p2:
            p1_lengths.append(0)
        else:
            p2_segments = df[df['DisplayName'] == p2] if p2 != user else pd.DataFrame()
            shared_lengths = 0

            for _, row1 in p1_segments.iterrows():
                for _, row2 in p2_segments.iterrows():
                    if row1['ChromosomeNumber'] == row2['ChromosomeNumber']:
                        shared_start = max(row1['ChromosomeStart'], row2['ChromosomeStart'])
                        shared_end = min(row1['ChromosomeEnd'], row2['ChromosomeEnd'])
                        shared_length = max(0, shared_end - shared_start)
                        shared_lengths += shared_length

            p1_lengths.append(shared_lengths)

    segments_lengths.append(p1_lengths)

genetic_similarity_matrix = calculate_genetic_similarity(np.array(segments_lengths))
print(genetic_similarity_matrix)

clustering = AgglomerativeClustering(distance_threshold=0, n_clusters=None, linkage='average',
                                     affinity='precomputed').fit(genetic_similarity_matrix)

print(clustering.children_)
distance_matrix = 1 - genetic_similarity_matrix
print(distance_matrix)

Z = linkage(distance_matrix, method='average', metric='euclidean')
# Perform hierarchical clustering
# Z = linkage(genetic_similarity_matrix, method='average', metric='precomputed')
# Z = linkage(genetic_similarity_matrix, method='average', metric='precomputed')

# Plot dendrogram
plt.figure(figsize=(10, 5))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Sample Index')
plt.ylabel('Distance')
dendrogram(Z, leaf_rotation=90., leaf_font_size=8.)
plt.show()