import pandas as pd
import csv
cols = range(17)

def load_ibkr_report(filepath):
    data = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f, quotechar='"')
        for row in reader:
            data.append(row)

    # Convert the list of lists to a DataFrame
    df = pd.DataFrame(data)

    return df


def get_forex(df):
    df = df[df[3]=='Forex']
    df = df[df[1]=='Data']
    df = df[[4,5,6,7,8,10,11,14]]
    cols = ['right', 'both', 'time', 'value_left', 'fx_rate', 'value_right', 'commission', 'mtm']
    df.columns = cols
    df['left'] = df['both'].str.split('.').str[0]
    df = df[['time', 'value_left', 'left',  'value_right', 'right', 'both', 'commission', 'fx_rate', 'mtm']]
    df['time'] = pd.to_datetime(df['time'])
    # delete , from the values
    df['value_left'] = df['value_left'].str.replace(',', '')
    df['value_right'] = df['value_right'].str.replace(',', '')

    df['value_left'] = df['value_left'].astype(float)
    df['value_right'] = df['value_right'].astype(float)
    df['fx_rate'] = df['fx_rate'].astype(float)
    df['commission'] = df['commission'].astype(float)
    # split the left and right values
    df1 = df[['time', 'value_left', 'left', 'both', 'fx_rate', 'commission']]
    df1.columns = ['time', 'value', 'currency', 'both', 'fx_rate', 'commission']
    df2 = df[['time', 'value_right', 'right', 'both', 'fx_rate', 'commission']]
    df2.columns = ['time', 'value', 'currency', 'both', 'fx_rate', 'commission']
    df_appended = df1.append(df2)
    df_appended.sort_values(by=['time'], inplace=True)
    df_appended.reset_index(inplace=True)
    df_appended.drop(columns=['index'], inplace=True)
    return df, df_appended


def get_given_forex(df, currency):
    df, df_appended = get_forex(df)
    df_res = df_appended[df_appended['currency']==currency]
    return df_res

filepath = 'input/' + 'U10557509_202211_202211.csv'
df = load_ibkr_report(filepath)
df = get_given_forex(df, 'GBP')
print(df)