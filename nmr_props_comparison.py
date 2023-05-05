import os
import pandas as pd
import glob

def read_properties(file_path):
    properties = {}
    with open(file_path, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=')
                properties[key] = value
    return properties

def merge_properties(file_paths):
    all_properties = {}
    for file_path in file_paths:
        machine_name = os.path.basename(file_path).split('_')[0]
        properties = read_properties(file_path)
        all_properties[machine_name] = properties

    merged_data = []
    keys = set().union(*(props.keys() for props in all_properties.values()))

    for key in keys:
        row = {'property': key}
        for machine, props in all_properties.items():
            row[machine] = props.get(key)
        merged_data.append(row)

    df = pd.DataFrame(merged_data)
    df['count'] = df.apply(lambda row: row.count() - 2, axis=1)
    df['match'] = df.apply(lambda row: len(set(row[1:-2])) == 1, axis=1)
    df.sort_values(by=['match', 'count', 'property'], ascending=[False, False, True], inplace=True)
    df.drop(columns=['count', 'match'], inplace=True)

    return df

# Replace the folder path with the actual folder containing your text files
folder_path = 'path/to/your/txt_files'
txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

df = merge_properties(txt_files)
print(df)
