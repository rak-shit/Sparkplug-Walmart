import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

pd.set_option("display.max_rows", None, "display.max_columns", None)

def find_sellers():
    data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
    data = data[(data["cm_name"] == "Wheat") & (data["adm0_name"] == 'India')]
    data_reduced= data[['cm_name','mkt_name', 'mp_month', 'mp_price']]
    items = ['Bread','Wheat','Rice']
    item_sellers = dict()
    i = 0
    for item in items:
        for i in range(len(data_reduced)):
            if data_reduced.iloc[i]['cm_name'] == item:
                if item not in list(item_sellers.keys()):
                    item_sellers[item] = [data_reduced.iloc[i]['mkt_name']]

    print(item_sellers)
    return item_sellers

def map_mkt():
    data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
    data = data[(data["cm_name"] == "Wheat") & (data["adm0_name"] == 'India')]
    data = data[['mkt_name']]
    data = data.drop_duplicates()
    col_mkt_list = data['mkt_name'].tolist()
    mkt_dict = {}
    i = 0
    for x in col_mkt_list:
        mkt_dict[x] = i
        i = i + 1
    
    return mkt_dict

def cluster(mkt_dict):
    data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
    data = data[(data["cm_name"] == "Wheat") & (data["adm0_name"] == 'India')]
    df = data[['cm_name','mkt_name', 'mp_month', 'mp_price']]
    # print(data_reduced)
    print(df)

    for x in df.index:
        df.at[x, 'mkt_name'] = mkt_dict[df.at[x, 'mkt_name']]  

    new_data = df[['mkt_name', 'mp_price']]

    iso_forest = IsolationForest(n_estimators=300, contamination=0.10)
    iso_forest = iso_forest.fit(new_data)



def main():
    mkt_dict = map_mkt()
    cluster(mkt_dict)

if __name__ == "__main__":
    main()
