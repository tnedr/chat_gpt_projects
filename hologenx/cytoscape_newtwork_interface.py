import csv
import json
import pandas as pd
import os
import xlwings as xw
from jsondiff import diff
from openpyxl import load_workbook
import sys

import csv
import json
import pandas as pd
import xlwings as xw
import os
from openpyxl import load_workbook
from jsondiff import diff


class CSVHandler:
    @staticmethod
    def read_csv_to_dict(csv_filepath, encoding='utf-8-sig'):
        with open(csv_filepath, mode='r', encoding=encoding) as csv_file:
            return list(csv.DictReader(csv_file))

    @staticmethod
    def write_dict_to_csv(data, csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


class JSONHandler:
    @staticmethod
    def load_json(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def save_json(data, file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def compare_json_files(file1, file2):
        json_data1 = JSONHandler.load_json(file1)
        json_data2 = JSONHandler.load_json(file2)
        return diff(json_data1, json_data2)


class ExcelHandler:
    @staticmethod
    def create_csv_from_excel(excel_file_path, output_directory):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        wb = xw.Book(excel_file_path)
        for sheet in wb.sheets:
            df = sheet.used_range.options(pd.DataFrame, index=False, header=True).value
            csv_file_path = os.path.join(output_directory, f"{sheet.name}.csv")
            df.to_csv(csv_file_path, index=False)
        wb.close()

    @staticmethod
    def update_excel_with_csv(excel_file_path, csv_data, sheet_name):
        nodes_sheet = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        for index, row in csv_data.iterrows():
            nodes_sheet.loc[nodes_sheet['data_shared_name'] == row['shared_name'], ['position_x', 'position_y']] = \
            row[['x', 'y']].values
        with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            nodes_sheet.to_excel(writer, sheet_name=sheet_name, index=False)


class NetworkDataProcessor:
    def __init__(self):
        self.json_handler = JSONHandler()
        self.csv_handler = CSVHandler()
        self.excel_handler = ExcelHandler()

    def process1_cyjs_file_to_csvs(self, json_path, nodes_csv_path, edges_csv_path):
        json_data = self.json_handler.load_json(json_path)
        nodes_json, edges_json = self._extract_nodes_edges_from_cyjs(json_data)
        nodes_data = self._nodes_json_to_dict(nodes_json)
        edges_data = self._edges_json_to_dict(edges_json)
        self.csv_handler.write_dict_to_csv(nodes_data, nodes_csv_path)
        self.csv_handler.write_dict_to_csv(edges_data, edges_csv_path)

    def process3_cyjs_file_to_csvs(self, json_path, excel_path, nodes_sheet_name='nodes'):
        # Step 1: Convert the CYJS JSON to CSVs (Nodes and Edges)
        self.process1_cyjs_file_to_csvs(json_path, 'temp_nodes.csv', 'temp_edges.csv')

        # Step 2: Load the nodes CSV data
        nodes_df = pd.read_csv('temp_nodes.csv')

        # Step 3: Update the Excel file with the new coordinates
        self.excel_handler.update_excel_with_csv(excel_path, nodes_df, nodes_sheet_name)

        # Cleanup the temporary files
        os.remove('temp_nodes.csv')
        os.remove('temp_edges.csv')

        print(f'Updated the Excel file {excel_path} with coordinates from {json_path}')

    def process4_create_cyjs_from_network_excel(self, excel_path, nodes_csv_path, edges_csv_path, output_json_path):
        # Step 1: Convert the Excel sheets to CSV files
        self.excel_handler.create_csv_from_excel(excel_path, os.path.dirname(nodes_csv_path))

        # Step 2: Create CYJS JSON from the CSVs
        nodes_json = self._create_nodes_json(nodes_csv_path)
        edges_json = self._create_edges_json(edges_csv_path)

        # Step 3: Merge the nodes and edges into a single CYJS JSON structure
        merged_json = self._merge_cyjs(nodes_json, edges_json)

        # Step 4: Save the merged JSON to the output file
        self.json_handler.save_json(merged_json, output_json_path)

        print(f'Created CYJS JSON file at {output_json_path} from Excel data at {excel_path}')

    def _create_nodes_json(self, csv_path):
        nodes_data = CSVHandler.read_csv_to_dict(csv_path)
        nodes_json = []
        for row in nodes_data:
            node = {
                'data': {
                    'id': row["data_id"],
                    'shared_name': row["data_shared_name"],
                    'diffusion_input': float(row["data_diffusion_input"]),
                    'Label': row["data_Label"],
                    'name': row["data_name"],
                    'SUID': int(float(row["data_SUID"])),
                    'category': row["data_category"],
                    'selected': row["data_selected"] == "True",
                },
                'position': {
                    'x': float(row["position_x"]),
                    'y': float(row["position_y"])
                },
                'selected': row["selected"] == "True"
            }
            nodes_json.append(node)
        return nodes_json

    def _create_edges_json(self, csv_path):
        edges_data = CSVHandler.read_csv_to_dict(csv_path)
        edges_json = []
        for row in edges_data:
            edge = {
                'data': {
                    'id': row["id"],
                    'source': row["source"],
                    'target': row["target"],
                    'source_type': row["source_type"],
                    'source_name': row["source_name"],
                    'target_name': row["target_name"],
                    'shared_name': row["shared_name"],
                    'shared_interaction': row["shared_interaction"],
                    'impact': row["impact"],
                    'name': row["name"],
                    'interaction': row["interaction"],
                    'weight': float(row["weight"]),
                    'SUID': int(float(row["SUID"])),
                    'selected': row.get("selected", "false").lower() == "true"
                }
            }
            edges_json.append(edge)
        return edges_json
    def _merge_cyjs(self, nodes_json, edges_json):
        merged_json = {
            "format_version": "1.0",
            "generated_by": "NetworkDataProcessor",
            "target_cytoscapejs_version": "~2.1",
            "data": {
                # ... any additional metadata ...
            },
            "elements": {
                "nodes": nodes_json,
                "edges": edges_json
            }
        }
        return merged_json


    def _extract_nodes_edges_from_cyjs(self, cyjs_data):
        nodes = cyjs_data['elements']['nodes']
        edges = cyjs_data['elements']['edges']
        return nodes, edges

    def _nodes_json_to_dict(self, nodes_json):
        nodes_data = []
        for node in nodes_json:
            node_data = node['data']
            node_data.update(node.get('position', {}))
            node_data['selected'] = node.get('selected', False)
            nodes_data.append(node_data)
        return nodes_data

    def _edges_json_to_dict(self, edges_json):
        edges_data = []
        for edge in edges_json:
            edge_data = edge['data']
            edge_data['selected'] = edge.get('selected', False)
            edges_data.append(edge_data)
        return edges_data


processor = NetworkDataProcessor()
# processor.process1_cyjs_file_to_csvs(
#     'network/nw801b.cyjs',
#     'network/nodes_cyjsb.csv',
#     'network/edges_cyjsb.csv'
# )
# processor.process3_cyjs_file_to_csvs(
#     'network/nw801.cyjs',
#     'network/aging_network.xlsx'
# )
processor.process4_create_cyjs_from_network_excel(
    "network/aging_network.xlsx",
    "network/nodes.csv",
    "network/edges.csv",
    "network/result.json"
)
