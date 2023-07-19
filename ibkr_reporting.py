import pandas as pd
import csv
import sys


D_FOREX_TRADES_FILTER = {
    0: 'Trades',
    1: 'Data',
    3: 'Forex'
}

D_FOREX_TRADES_COLS = {
    6: 'Date/Time',
    7: 'value_left',
    10: 'value_right',
    4: 'right',
    5: 'both',
    11: 'commission',
    8: 'fx_rate',
    14: 'mtm'
}

D_FOREX_DEPOSIT_FILTER = {
    0: 'Deposits & Withdrawals',
    1: 'Data'
}

D_FOREX_DEPOSIT_COLS = {
    3: 'Date/Time',
    5: 'Amount',
    2: 'Currency',
    4: 'Description',
}

D_FOREX_FEES_FILTER = {
    0: 'Fees',
    1: 'Data',
    2: 'Other Fees'

}

D_FOREX_FEES_COLS = {
    4: 'Date/Time',
    6: 'Amount',
    3: 'Currency',
    5: 'Description',
}

D_FOREX_CLOSING_FILTER = {
    0: 'Mark-to-Market Performance Summary',
    1: 'Data',
    2: 'Forex'
}
D_FOREX_CLOSING_COLS = {
    3: 'currency',
    5: 'ending_cash_balance'
}
D_STOCK_TRADES_FILTER = {
    0: 'Trades',
    1: 'Data',
    2: 'Order',
    3: 'Stocks'
}

D_STOCK_TRADES_COLS = {
    6: 'Date/Time',
    5: 'Symbol',
    4: 'Currency',
    7: 'Quantity',
    8: 'T. Price',
    10: 'Proceeds',
    11: 'Comm/Fee',
    12: 'Basis'
}


filename_monthly = 'U10557509_202211_202211.csv'

def load_ibkr_report(filepath):
    data = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f, quotechar='"')
        for row in reader:
            data.append(row)

    # Convert the list of lists to a DataFrame
    df = pd.DataFrame(data)

    return df


def get_given_columns_of_report(filename_monthly, d_filter, d_cols):
    filepath = 'input/' + filename_monthly
    df = load_ibkr_report(filepath)
    for key, value in d_filter.items():
        df = df[df[key] == value]
    df = df[d_cols.keys()]
    df.columns = d_cols.values()
    if 'Date/Time' in df.columns:
        df['Date/Time'] = pd.to_datetime(df['Date/Time'])
        df.sort_values(by=['Date/Time'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def generate_stock_trades_report(filename_monthly):
    df = get_given_columns_of_report(filename_monthly, D_STOCK_TRADES_FILTER, D_STOCK_TRADES_COLS)
    # export to csv
    result_filename = filename_monthly.split('.')[0] + '_stock_trades.csv'
    df.to_csv('output/ibkr/' + result_filename, index=False)
    return df
# df = generate_stock_trades_report(filename_monthly)
# sys.exit()


def generate_closing_forex_balance(filename_monthly):
    df = get_given_columns_of_report(filename_monthly, D_FOREX_CLOSING_FILTER, D_FOREX_CLOSING_COLS)
    # export to csv
    result_filename = filename_monthly.split('.')[0] + '_forex_closing_balances.csv'
    df.to_csv('output/ibkr/' + result_filename, index=False)
    return df
# generate_closing_forex_balance(filename_monthly)
# sys.exit()


def generate_forex_trades(filename_monthly):
    df = get_given_columns_of_report(filename_monthly, D_FOREX_TRADES_FILTER, D_FOREX_TRADES_COLS)
    df['left'] = df['both'].str.split('.').str[0]
    # delete , from the values
    df['value_left'] = df['value_left'].str.replace(',', '')
    df['value_right'] = df['value_right'].str.replace(',', '')
    df['value_left'] = df['value_left'].astype(float)
    df['value_right'] = df['value_right'].astype(float)
    df['fx_rate'] = df['fx_rate'].astype(float)
    df['commission'] = df['commission'].astype(float)
    # split the left and right values
    df1 = df[['Date/Time', 'value_left', 'left', 'both', 'fx_rate', 'commission']]
    df1.columns = ['Date/Time', 'value', 'currency', 'both', 'fx_rate', 'commission']
    df2 = df[['Date/Time', 'value_right', 'right', 'both', 'fx_rate', 'commission']]
    df2.columns = ['Date/Time', 'value', 'currency', 'both', 'fx_rate', 'commission']
    df_appended = df1.append(df2)
    df_appended.sort_values(by=['Date/Time'], inplace=True)
    df_appended.reset_index(inplace=True)
    df_appended.drop(columns=['index'], inplace=True)
    df_currs = []
    for curr in ['GBP','USD','EUR','HUF']:
        df_temp = df_appended[df_appended['currency']==curr]
        df_currs.append(df_temp)
        result_filename = filename_monthly.split('.')[0] + '_forex_trades_' + curr + '.csv'
        df_temp.to_csv('output/ibkr/' + result_filename, index=False)
    return df, df_appended, df_currs
# generate_forex_trades(filename_monthly)


def whole_process(filename_monthly):
    generate_stock_trades_report(filename_monthly)
    generate_closing_forex_balance(filename_monthly)
    generate_forex_trades(filename_monthly)



def generate_forex_deposits(filename_monthly):
    df = get_given_columns_of_report(filename_monthly, D_FOREX_DEPOSIT_FILTER, D_FOREX_DEPOSIT_COLS)
    df = df[df['Currency']!='Total']
    # export to csv
    result_filename = filename_monthly.split('.')[0] + '_forex_deposits.csv'
    df.to_csv('output/ibkr/' + result_filename, index=False)
    return df
# generate_forex_deposits(filename_monthly)
# sys.exit()

def generate_forex_deposits(filename_monthly):
    df = get_given_columns_of_report(filename_monthly, D_FOREX_FEES_FILTER, D_FOREX_FEES_COLS)
    # df = df[df['Currency']!='Total']
    # export to csv
    result_filename = filename_monthly.split('.')[0] + '_forex_fees.csv'
    df.to_csv('output/ibkr/' + result_filename, index=False)
    return df
generate_forex_deposits(filename_monthly)

# whole_process(filename_monthly)
# sys.exit()
# todo
# deposits
# fees
# merge
# comments

#time amount, currency, type, descriptions
