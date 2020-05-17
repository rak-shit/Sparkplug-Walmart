import json
import statistics
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from helpers import essential_items
import boto3

pd.set_option("display.max_rows", None, "display.max_columns", None)


class Dashboard:
    def __init__(self, commodity, country, year):
        data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
        self.commodity = commodity
        self.country = country
        self.year = year
        self.raw_data = data
        self.data = data[(data["cm_name"] == commodity) & (data["adm0_name"] == country) & (data["mp_year"] == year)] 

    def get_commodities(self):
        return list(set(self.raw_data['cm_name'].tolist())), \
               list(set(self.raw_data['adm0_name'].tolist())), list(set(self.raw_data['mp_year'].tolist()))

    def find_sellers(self, commodity, country):
        # data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
        print(self.data.empty)
        if not self.data.empty:
            data_reduced = self.data[['cm_name','mkt_name', 'mp_month', 'mp_price']]
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
        else:
            return None
    def map_mkt(self, commodity_name, country):
        if not self.data.empty:
            data = self.data[['mkt_name']]
            data = data.drop_duplicates()
            col_mkt_list = data['mkt_name'].tolist()
            mkt_dict = {}
            i = 0
            for x in col_mkt_list:
                mkt_dict[x] = i
                i = i + 1
            
            return mkt_dict
        else:
            return None
    def pull_marketer_data_ses():
        pass

    def threshold(self, commodity, year, country):
        df = self.data[['mp_price']]
        return statistics.median(df['mp_price'].values.tolist()) + 5

    def threshold_all(self, commodity, year, country):
        data = self.data
        all_commodity_data = self.raw_data[(self.raw_data["mp_year"]==year) & (self.raw_data["cm_name"].isin(essential_items())) & (self.raw_data["adm0_name"] == country)]
        all_commodities =  list(set(all_commodity_data['cm_name'].values.tolist()))
        # return all_commodities
        thresholds_dict_cm = dict()
        for cm in all_commodities:
            # print(cm)
            data = all_commodity_data[(all_commodity_data["cm_name"] == cm)]
            df = data[['mp_price']]
            # print(df['mp_price'].values.tolist())
            try:
                threshold = statistics.median(df['mp_price'].values.tolist()) + 5
            except statistics.StatisticsError:
                threshold = 0
            thresholds_dict_cm[cm] = threshold

        lst = []
        for k, v in thresholds_dict_cm.items():
            lst.append([k, v])

        return lst

    def average_rate_change(self, commodity, country):
        df = self.data[['cm_name','mkt_name', 'mp_month', 'mp_price']]
        prices_list =  df['mp_price'].values.tolist()
        avg_rate_increase = 0
        length = len(prices_list)
        for index in range(0, len(prices_list)-1):
            diff = prices_list[index+1] - prices_list[index]
            if not diff * (-1) > 0:
                avg_rate_increase += diff
        return avg_rate_increase/(length-1)


    def anomaly_detection(self, mkt_dict, year, commodity, country):
        """
        Args:
        mkt_dict(dict) : Seller/Marketer to ID mappings
        year(int) : Year to check
        commodity(str) : 
        country(str) : 
        Returns:
        (json_output containing raw_data, outliers & thresholds for a particular field), outlier list
        """
        if not self.data.empty:
            df = self.data[['cm_name','mkt_name', 'mp_month', 'mp_price', 'mkt_id']]
            print("email test", df.values.tolist())

            for x in df.index:
                df.at[x, 'mkt_name'] = mkt_dict[df.at[x, 'mkt_name']]  

            new_data = df[['mkt_name', 'mp_price']]
            out_data = df[['mkt_name', 'mp_price', 'mkt_id']]
            iso_forest = IsolationForest(n_estimators=300, contamination=0.10)
            iso_forest = iso_forest.fit(out_data)
            isof_outliers = iso_forest.predict(out_data)
            isoF_outliers_values = out_data[iso_forest.predict(out_data) == -1]

            isoF_outliers_values = isoF_outliers_values[(isoF_outliers_values["mp_price"] > self.threshold(commodity, year, country))]

            # plt.scatter(isoF_outliers_values.iloc[:, 0], isoF_outliers_values.iloc[:, 1].values.astype(int))
            # plt.xlabel('MKT')
            # plt.ylabel('CM price')
            # plt.title('Visualization of raw data')
            # plt.show()
            print(isoF_outliers_values)
            outliers_list = isoF_outliers_values.values.tolist()


            dict_data = {
                "raw_data": new_data.values.tolist(),
                "outliers": outliers_list,
                "threshold_all": self.threshold_all(commodity, year, country),
                "average_rate_change": self.average_rate_change(commodity, country),
                "list_all": self.get_commodities()
            }

            # convert into JSON:
            json_data = json.dumps(dict_data)
            return json_data, outliers_list
        else:
            dict_data = {
                "errorInput": "No valid data present"
            }
            json_data = json.dumps(dict_data)
            outliers_list = []
            return json_data, outliers_list




    def main():
        mkt_dict = self.map_mkt()
        self.cluster(mkt_dict)

# if __name__ == "__main__":
#     print(cluster('Wheat', 2013, 'India'))

    # threshold('Wheat', 2013, 'Afghanistan')
    # print(average_rate_change())
    # main()
# print(threshold())


#Stuff left out
# pull anomaly marketer data
# Alerts via mail