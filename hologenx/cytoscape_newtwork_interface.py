import csv
import json
from jsondiff import diff
import pandas as pd


def create_nodes_json(csv_filepath):
    nodes_list = []
    with open(csv_filepath, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            node = {}
            data = {
                "id": row["data_id"],
                "shared_name": row["data_shared_name"],
                "diffusion_input": float(row["data_diffusion_input"]),
                "Label": row["data_Label"],
                "name": row["data_name"],
                "SUID": int(row["data_SUID"]),
                "category": row["data_category"],
                "selected": row["data_selected"] == "True"
            }
            node['data'] = data

            position = {
                "x": float(row["position_x"]),
                "y": float(row["position_y"])
            }
            node['position'] = position

            node['selected'] = row["selected"] == "True"

            nodes_list.append(node)
    return nodes_list


def create_edges_json(csv_path):
    edges = []
    with open(csv_path, mode='r', encoding='utf-8-sig') as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            edge = {
                "data": {
                    "id": row["id"],
                    "source": row["source"],
                    "target": row["target"],
                    "shared_name": row["shared_name"],
                    "shared_interaction": row["shared_interaction"],
                    "impact": row["impact"],
                    "name": row["name"],
                    "interaction": row["interaction"],
                    "weight": row["weight"],
                    "SUID": row["SUID"],
                    "selected": False if row.get("selected", "false").lower() == "false" else True
                },
                "selected": False if row.get("selected", "false").lower() == "false" else True
            }
            edges.append(edge)
    return edges


def merge_nodes_and_edges(output_json_path, nodes_csv_path, edges_csv_path):
    nodes_json = create_nodes_json(nodes_csv_path)
    edges_json = create_edges_json(edges_csv_path)

    merged_json = {
        "format_version": "1.0",
        "generated_by": "cytoscape-3.10.1",
        "target_cytoscapejs_version": "~2.1",
        "data": {
            "shared_name": "edges.csv_1",
            "name": "edges.csv_1",
            "SUID": 155,
            "__Annotations": [""],
            "selected": True
        },
        "elements": {
            "nodes": nodes_json,
            "edges": edges_json
        }
    }

    json_str = json.dumps(merged_json, indent=2)

    # Writing to a JSON file
    with open(output_json_path, 'w') as json_file:
        json_file.write(json_str)

    return json_str


def compare_json_files(path1, path2):
    try:
        # Load JSON data from the first file
        with open(path1, 'r') as file1:
            json_data1 = json.load(file1)

        # Load JSON data from the second file
        with open(path2, 'r') as file2:
            json_data2 = json.load(file2)

        # Compare the two JSON data
        differences = diff(json_data1, json_data2)

        # Check if there are any differences
        if differences:
            print("The JSON files are different.")
            print("Differences:", differences)
        else:
            print("The JSON files are equivalent.")

    except Exception as e:
        print(f"An error occurred: {e}")


def json_to_dfs_multi_index(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    nodes_list = json_data['elements']['nodes']
    edges_list = json_data['elements']['edges']

    # Multi-indexed data
    nodes_data = []
    for node in nodes_list:
        node_data = {'data_' + k: v for k, v in node['data'].items()}
        pos_data = {'position_' + k: v for k, v in node.get('position', {}).items()}
        merged_data = {**node_data, **pos_data}
        nodes_data.append(merged_data)

    edges_data = [edge['data'] for edge in edges_list]

    nodes_df = pd.DataFrame(nodes_data)
    nodes_df.columns = pd.MultiIndex.from_tuples(
        [(col.split('_', 1)[0], col.split('_', 1)[1]) for col in nodes_df.columns])

    edges_df = pd.DataFrame(edges_data)

    return nodes_df, edges_df

def save_dfs_to_csv(nodes_df, edges_df, nodes_file_path='nodes2.csv', edges_file_path='edges2.csv'):
    nodes_df.columns = ['_'.join(col).strip() for col in nodes_df.columns.values]
    nodes_df.to_csv(nodes_file_path, index=False)
    edges_df.to_csv(edges_file_path, index=False)


# Example usage:
output_json_path = 'network/merged.json'
nodes_csv_path = 'network/nodes2.csv'
edges_csv_path = 'network/edges2.csv'
merged_json_str = merge_nodes_and_edges(output_json_path, nodes_csv_path, edges_csv_path)

json1 = 'network/merged.json'

json_input = 'network/nw3.cyjs'
nodes_df, edges_df = json_to_dfs_multi_index(json_input)
# Usage example with the previously generated DataFrames
save_dfs_to_csv(nodes_df, edges_df, 'network/nodes.csv', 'network/edges.csv')

# Example usage:
# compare_json_files(json1, json2)



