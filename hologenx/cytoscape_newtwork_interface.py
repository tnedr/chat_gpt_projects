import csv
import json
from jsondiff import diff
import pandas as pd
import os
import sys
from openpyxl import load_workbook
import xlwings as xw

# use case:
# - cytoscape export the file into cyjs format
# - we should create csvs
# - we can add records to csvs (manually or programmatically), we should set x and y position manually
# - we can create a new cyjs file from csvs
# - we can upload the modified cyjs file to cytoscape

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
                "SUID": int(float(row["data_SUID"])),
                "category": row["data_category"],
                "selected": row["data_selected"] == "True",
                "show": row["show"]
            }
            node['data'] = data

            position = {
                "x": float(row["position_x"]),
                "y": float(row["position_y"])
            }
            node['position'] = position

            node['selected'] = row["selected"] == "True"
            # node['selected'] = row["selected"] == "True"

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
                    "source_type": row["source_type"],
                    "source_name": row["source_name"],
                    "target_name": row["target_name"],
                    "shared_name": row["shared_name"],
                    "shared_interaction": row["shared_interaction"],
                    "impact": row["impact"],
                    "name": row["name"],
                    "interaction": row["interaction"],
                    "weight": row["weight"],
                    "SUID": int(float(row["SUID"])),
                    "selected": False if row.get("selected", "false").lower() == "false" else True
                },
                "selected": False if row.get("selected", "false").lower() == "false" else True
            }
            edges.append(edge)
    return edges


def save_new_network_json_from_nodes_and_edges(output_json_path, nodes_csv_path, edges_csv_path):
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
        # merged_data = {**node_data, **pos_data}
        merged_data = {**node_data, **pos_data, 'selected': node.get('selected', False)}
        nodes_data.append(merged_data)

    edges_data = [edge['data'] for edge in edges_list]

    nodes_df = pd.DataFrame(nodes_data)
    # nodes_df.columns = pd.MultiIndex.from_tuples(
    #     [(col.split('_', 1)[0], col.split('_', 1)[1]) for col in nodes_df.columns])
    nodes_df.columns = pd.MultiIndex.from_tuples(
        [(col.split('_', 1)[0], col.split('_', 1)[1]) if '_' in col else (col, '') for col in nodes_df.columns])

    edges_df = pd.DataFrame(edges_data)

    return nodes_df, edges_df


def save_dfs_to_csv(nodes_df, edges_df, nodes_file_path='nodes2.csv', edges_file_path='edges2.csv'):
    # nodes_df.columns = ['_'.join(col).strip() for col in nodes_df.columns.values]
    nodes_df.columns = ['_'.join(filter(None, col)).strip() for col in nodes_df.columns.values]
    nodes_df.to_csv(nodes_file_path, index=False)
    edges_df.to_csv(edges_file_path, index=False)


def save_excel_sheets_to_csv(excel_file_path, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Open the workbook with xlwings
    wb = xw.Book(excel_file_path)

    # Loop through each sheet in the Excel workbook
    for sheet in wb.sheets:
        # Convert the sheet to a DataFrame
        df = sheet.used_range.options(pd.DataFrame, index=False, header=True).value

        # Create the CSV file path
        csv_file_path = os.path.join(output_directory, f"{sheet.name}.csv")

        # Save the DataFrame to CSV
        df.to_csv(csv_file_path, index=False)

    # Close the workbook
    wb.close()


# save_excel_sheets_to_csv("network/aging_network.xlsx", "network")
# sys.exit()

def modify_edges_csv(file_path):
    # 1. Open the CSV as a DataFrame
    df = pd.read_csv(file_path)

    # 2. Add the new columns, initializing with empty strings
    df['source_name'] = ''
    df['target_name'] = ''

    # 3. Fill up the columns by splitting 'shared_name'
    for index, row in df.iterrows():
        shared_name = row['shared_name']
        source_name, _, target_name = shared_name.partition(' (')
        target_name = target_name.rpartition(') ')[2]

        df.at[index, 'source_name'] = source_name
        df.at[index, 'target_name'] = target_name

    # Reorder columns to place 'source_name' and 'target_name' after 'target'
    if False:
        cols = df.columns.tolist()
        source_name_index = cols.index('source_name')
        target_name_index = cols.index('target_name')
        target_index = cols.index('target')

        reordered_cols = cols[:target_index + 1] + [cols[source_name_index], cols[target_name_index]] + cols[
                                                                                                        target_index + 1:source_name_index] + cols[
                                                                                                                                              source_name_index + 1:target_name_index] + cols[
                                                                                                                                                                                         target_name_index + 1:]

        df = df[reordered_cols]

    # 4. Save the DataFrame back to the original CSV file
    df.to_csv(file_path, index=False)
# modify_edges_csv('network/edges.csv')
# import sys
# sys.exit()

# Example usage:

def update_coordinates_in_excel_file(excel_file_path, node_csv_file_path):

    nodes_sheet = pd.read_excel(excel_file_path, sheet_name='nodes')
    csv_data = pd.read_csv(node_csv_file_path)

    for index, row in csv_data.iterrows():
        node_name = row['data_shared_name']
        position_x_csv = row['position_x']
        position_y_csv = row['position_y']

        # Update the corresponding row in the 'nodes' sheet
        nodes_sheet.loc[nodes_sheet['data_shared_name'] == node_name, 'position_x'] = position_x_csv
        nodes_sheet.loc[nodes_sheet['data_shared_name'] == node_name, 'position_y'] = position_y_csv

    # Save the modified 'nodes' sheet back to the Excel file
    with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        nodes_sheet.to_excel(writer, sheet_name='nodes', index=False)

    print('Excel file updated successfully!')
# update_coordinates_in_excel_file('network/aging_network.xlsx', 'network/nodes_cyjs.csv')



def create_cyjs():
    # step 5: create nodes and edges csvs from excel
    save_excel_sheets_to_csv("network/aging_network.xlsx", "network")
    # step 6: create cyjs from csvs
    nodes_csv_path = 'network/nodes.csv'
    edges_csv_path = 'network/edges.csv'
    output_json_path = 'network/result.json'
    merged_json_str = save_new_network_json_from_nodes_and_edges(output_json_path, nodes_csv_path, edges_csv_path)


def refresh_coordinates_in_result_json(json_cyjs, excel_file_path):
    # get the new coordinates from json cyjs
    nodes_df, edges_df = json_to_dfs_multi_index(json_cyjs)
    # save the results to cyjs nodes
    save_dfs_to_csv(nodes_df, edges_df, 'network/nodes_cyjs.csv', 'network/edges_cyjs.csv')
    # update the
    update_coordinates_in_excel_file(excel_file_path, 'network/nodes_cyjs.csv')
    create_cyjs()
refresh_coordinates_in_result_json('network/nw501.cyjs', 'network/aging_network.xlsx')
sys.exit()



#step 7: upload the cyjs to cytoscape

# compare cyjs with json
# compare_json_files(output_json_path, json_cyjs)

