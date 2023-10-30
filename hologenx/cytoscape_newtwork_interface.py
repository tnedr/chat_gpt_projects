import csv
import json


def csv_to_json(csv_filepath):
    nodes_list = []

    # Read the CSV file
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

    output_json = {"nodes": nodes_list}

    # Convert to JSON string
    json_str = json.dumps(output_json, indent=4)

    # Write to JSON file (optional)
    # with open('network/network.json', 'w') as json_file:
    #     json_file.write(json_str)

    return json_str
# Test the function
print(csv_to_json('network/nodes.csv'))
import sys
sys.exit()
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

    edges_json = {"edges": edges}
    return json.dumps(edges_json, indent=4)

# Example usage:
csv_path = "network/edges.csv"
json_output = create_edges_json(csv_path)
print(json_output)
