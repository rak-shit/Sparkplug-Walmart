import pandas as pd

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
    data = data[(data["cm_name"] == "Wheat")]
    data = data[['mkt_name']]
    data = data.drop_duplicates()
    col_mkt_list = data['mkt_name'].tolist()
    mkt_dict = {}
    i = 0
    for x in col_mkt_list:
        mkt_dict[x] = i
        i = i + 1
    
    return mkt_dict

def cluster():
    data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
    data = data[(data["cm_name"] == "Wheat") & (data["adm0_name"] == 'India')]
    df = data[['cm_name','mkt_name', 'mp_month', 'mp_price']]
    # print(data_reduced)

    plt.scatter(df.iloc[:, 2], df.iloc[:, 3].values.astype(int))
    plt.xlabel('Month')
    plt.ylabel('CM price')
    plt.title('Visualization of raw data')
    plt.show()

def main():
    print(map_mkt())

main()
