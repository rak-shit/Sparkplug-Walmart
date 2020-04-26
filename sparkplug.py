import json
import statistics
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

pd.set_option("display.max_rows", None, "display.max_columns", None)

def find_sellers(commodity, country):
    data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
    data = data[(data["cm_name"] == commodity) & (data["adm0_name"] == country)]
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

def map_mkt(commodity_name, country):
    data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
    data = data[(data["cm_name"] == commodity_name) & (data["adm0_name"] == country)]
    data = data[['mkt_name']]
    data = data.drop_duplicates()
    col_mkt_list = data['mkt_name'].tolist()
    mkt_dict = {}
    i = 0
    for x in col_mkt_list:
        mkt_dict[x] = i
        i = i + 1
    
    return mkt_dict

def threshold(commodity, year, country):
    data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
    data = data[(data["cm_name"] == commodity) & (data["mp_year"]==year) & (data["adm0_name"] == country)]
    df = data[['mp_price']]
    return statistics.median(df['mp_price'].values.tolist()) + 5

def average_rate_change(commodity, country):
    data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
    data = data[(data["cm_name"] == commodity) & (data["adm0_name"] == country)]
    df = data[['cm_name','mkt_name', 'mp_month', 'mp_price']]
    prices_list =  df['mp_price'].values.tolist()
    avg_rate_increase = 0
    length = len(prices_list)
    for index in range(0, len(prices_list)-1):
        diff = prices_list[index+1] - prices_list[index]
        if not diff * (-1) > 0:
            avg_rate_increase += diff
    return avg_rate_increase/(length-1)





def cluster(mkt_dict, year, commodity, country):
    data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
    data = data[(data["cm_name"] == commodity) & (data["adm0_name"] == country)]
    df = data[['cm_name','mkt_name', 'mp_month', 'mp_price']]
    # print(data_reduced)
    # print(df)

    for x in df.index:
        df.at[x, 'mkt_name'] = mkt_dict[df.at[x, 'mkt_name']]  

    new_data = df[['mkt_name', 'mp_price']]

    iso_forest = IsolationForest(n_estimators=300, contamination=0.10)
    iso_forest = iso_forest.fit(new_data)
    isof_outliers = iso_forest.predict(new_data)
    isoF_outliers_values = new_data[iso_forest.predict(new_data) == -1]
    # print(isoF_outliers_values)

    isoF_outliers_values = isoF_outliers_values[(data["mp_price"] > threshold(commodity, year, country))]

    # plt.scatter(isoF_outliers_values.iloc[:, 0], isoF_outliers_values.iloc[:, 1].values.astype(int))
    # plt.xlabel('MKT')
    # plt.ylabel('CM price')
    # plt.title('Visualization of raw data')
    # plt.show()

    x = {
    "raw_data": new_data.values.tolist(),
    "outliers": isoF_outliers_values.values.tolist()
    }

    # convert into JSON:
    y = json.dumps(x)
    return y



def main():
    mkt_dict = map_mkt()
    cluster(mkt_dict)
    print(average_rate_change())

# if __name__ == "__main__":

    # threshold('Wheat', 2013, 'Afghanistan')
    # print(average_rate_change())
    # main()
# print(threshold())


#Stuff left out
# pull anomaly marketer data
# Alerts via mail