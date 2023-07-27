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
    5: 'Comment',
}

D_FOREX_INTEREST_FILTER = {
    0: 'Interest',
    1: 'Data'
}

D_FOREX_INTEREST_COLS = {
    3: 'Date/Time',
    5: 'Amount',
    2: 'Currency',
    4: 'Comment',
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
    12: 'Amount',
    4: 'Currency',
    5: 'Symbol',
    7: 'Quantity',
    8: 'T. Price',
    10: 'Proceeds',
    11: 'Comm/Fee'
}




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

# ----------- FOREX -------------

def get_forex_trades(filename_monthly):
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
    df1.columns = ['Date/Time', 'Amount', 'Currency', 'both', 'fx_rate', 'commission']
    df2 = df[['Date/Time', 'value_right', 'right', 'both', 'fx_rate', 'commission']]
    df2.columns = ['Date/Time', 'Amount', 'Currency', 'both', 'fx_rate', 'commission']
    df_appended = df1.append(df2)
    df_appended.sort_values(by=['Date/Time'], inplace=True)
    df_appended.reset_index(inplace=True)
    df_appended.drop(columns=['index'], inplace=True)
    # df_currs = []
    # for curr in ['GBP','USD','EUR','HUF']:
    #     df_temp = df_appended[df_appended['currency']==curr]
    #     df_currs.append(df_temp)
    #     result_filename = filename_monthly.split('.')[0] + '_forex_trades_' + curr + '.csv'
    #     df_temp.to_csv('output/ibkr/' + result_filename, index=False)
    # return df, df_appended, df_currs
    # create description column
    df_appended['Description'] = 'fx trade'
    df_appended['Comment'] = 'fx: ' + df_appended['both'] + ', rate: ' + df_appended['fx_rate'].astype(str) + ', comm: ' + df_appended['commission'].astype(str)
    # time amount, currency, type, descriptions
    df_res = df_appended[['Date/Time', 'Amount', 'Currency', 'Description', 'Comment']]
    return df_res
# get_forex_trades(filename_monthly)

def get_forex_deposits(filename_monthly):
    df = get_given_columns_of_report(filename_monthly, D_FOREX_DEPOSIT_FILTER, D_FOREX_DEPOSIT_COLS)
    df = df[df['Currency']!='Total']
    df['Comment'] = ''
    df = df[['Date/Time', 'Amount', 'Currency', 'Description', 'Comment']]
    return df
# get_forex_deposits(filename_monthly)

def get_forex_fees(filename_monthly):
    df = get_given_columns_of_report(filename_monthly, D_FOREX_FEES_FILTER, D_FOREX_FEES_COLS)
    df['Description'] = 'fee'
    df = df[['Date/Time', 'Amount', 'Currency', 'Description', 'Comment']]
    # df = df[df['Currency']!='Total']
    # export to csv
    # result_filename = filename_monthly.split('.')[0] + '_forex_fees.csv'
    # df.to_csv('output/ibkr/' + result_filename, index=False)
    return df
# get_forex_fees(filename_monthly)

def get_forex_interest(filename_monthly):
    df = get_given_columns_of_report(filename_monthly, D_FOREX_INTEREST_FILTER, D_FOREX_INTEREST_COLS)
    df['Description'] = 'interest'
    df = df[df['Date/Time'].notnull()]
    df = df[['Date/Time', 'Amount', 'Currency', 'Description', 'Comment']]
    # df = df[df['Currency']!='Total']
    # export to csv
    # result_filename = filename_monthly.split('.')[0] + '_forex_fees.csv'
    # df.to_csv('output/ibkr/' + result_filename, index=False)
    return df
# filename_monthly = 'U10557509_202212_202212.csv'
# get_forex_interest(filename_monthly)


def get_stock_trades_report(filename_monthly):
    df = get_given_columns_of_report(filename_monthly, D_STOCK_TRADES_FILTER, D_STOCK_TRADES_COLS)
    df['Description'] = 'stock trade'
    df['Comment'] = 'Symbol: ' + df['Symbol'] + ', Quantity: ' + df['Quantity'] + ', T.Price: ' + df['T. Price'] + ', Proceeds: ' + df['Proceeds'] + ', Comm/Fee: ' + df['Comm/Fee']
    df['Amount'] = -1 * df['Amount'].astype(float)
    df = df[['Date/Time', 'Amount', 'Currency', 'Description', 'Comment']]
    # export to csv
    # result_filename = filename_monthly.split('.')[0] + '_stock_trades.csv'
    # df.to_csv('output/ibkr/' + result_filename, index=False)
    return df
# get_stock_trades_report(filename_monthly)
# sys.exit()


def merged_forex_data(filename_monthly):
    df_fx_trades = get_forex_trades(filename_monthly)
    df_fx_deposits = get_forex_deposits(filename_monthly)
    df_fx_fees = get_forex_fees(filename_monthly)
    df_fx_interest = get_forex_interest(filename_monthly)
    df_stock_trades = get_stock_trades_report(filename_monthly)


    df = df_fx_trades.append(df_fx_deposits)
    df = df.append(df_fx_fees)
    df = df.append(df_fx_interest)
    df = df.append(df_stock_trades)
    df.sort_values(by=['Currency', 'Date/Time'], inplace=True)

    # export to csv
    for curr in ['GBP', 'USD', 'EUR', 'HUF']:
        df_temp = df[df['Currency'] == curr]
        result_filename = filename_monthly.split('.')[0] + '_' + curr + '.csv'
        df_temp.to_csv('output/ibkr/' + result_filename, index=False)

    return df
# merged_forex_data(filename_monthly)


def generate_closing_forex_balance(filename_monthly):
    df = get_given_columns_of_report(filename_monthly, D_FOREX_CLOSING_FILTER, D_FOREX_CLOSING_COLS)
    # export to csv
    result_filename = filename_monthly.split('.')[0] + '_forex_closing_balances.csv'
    df.to_csv('output/ibkr/' + result_filename, index=False)
    return df




def whole_process(filename_monthly):
    merged_forex_data(filename_monthly)
    generate_closing_forex_balance(filename_monthly)

filename_monthly = 'U10557509_202211_202211.csv'
whole_process(filename_monthly)
filename_monthly = 'U10557509_202212_202212.csv'
whole_process(filename_monthly)

