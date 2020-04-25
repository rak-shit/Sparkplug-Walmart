import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)



items = ['Bread','Wheat','Rice']
def find_sellers():
    item_sellers = dict()
    i = 0
    for item in items:
        for i in range(len(data_reduced)):
            if data_reduced.iloc[i]['cm_name'] == item:
                if item not in list(item_sellers.keys()):
                    item_sellers[item] = [data_reduced.iloc[i]['mkt_name']]

    return item_sellers

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