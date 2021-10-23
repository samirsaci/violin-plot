import pandas as pd
import json
import numpy as np


ORDERS_PATH = r'static\data\7\df_transactions.xlsx'

def build_dataset(ORDERS_PATH):
    ''' Build Dataset to fit format of json '''
    df_orders = pd.read_excel(ORDERS_PATH)

    # GroupBy
    df_grpby = pd.DataFrame(df_orders.groupby(['SKU', 'BRAND'])['ORDER_NUMBER'].count())
    df_grpby.columns = ['value_2'] # value 2 = Orders Number
    df_grpby['value_1'] = df_orders.groupby(['SKU', 'BRAND'])['PCS'].sum() # value 1 = Pieces

    # Reset Index
    df_grpby.reset_index(inplace = True)

    # Columns
    df_grpby.columns = ['description_1', 'description_2', 'value_2', 'value_1']
    df_grpby = df_grpby.head(500)

    # Sort by highest pcs qty
    df_grpby = df_grpby.sort_values(['value_1'], axis = 0, ascending = False)

    # add value 3
    df_grpby['value_3'] = (100 * df_grpby['value_1']/df_grpby['value_1'].sum(axis=0)).round(2)
    print("{:,} records with {:,} unique brands".format(len(df_grpby), df_grpby['description_2'].nunique()))

    # cumulative sum 
    total_pcs = df_grpby.value_1.sum()
    df_grpby['high_runner'] = np.ceil((df_grpby['value_1'].cumsum()/total_pcs)/0.2).astype(int)

    return df_grpby

def json_violin(df_grpby):
    ''' Create json from dataframes'''
    json_data = []
    for index, row in df_grpby.iterrows():
        dico = {}
        dico['description_1'] = row['description_1']
        dico['description_2'] = row['description_2']
        dico['value_2'] = row['value_2']
        dico['value_1'] = row['value_1']
        dico['value_3'] = row['value_3']
        dico['high_runner'] = row['high_runner']
        json_data.append(dico)

    json_data = {"data": json_data}
    return json_data