# Modules
import matplotlib.pyplot as plt
from matplotlib.image import imread
import pandas as pd
import seaborn as sns
# from sklearn.datasets.samples_generator import (make_blobs,
#                                                 make_circles,
#                                                 make_moons)
# from sklearn.cluster import KMeans, SpectralClustering
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import silhouette_samples, silhouette_score

sns.set_context('notebook')

# Import the data
data = pd.read_csv("data.csv", encoding = "ISO-8859-1")
data = data[data["cm_name"] == "Wheat"]
df = data[['cm_name', 'mkt_name', 'mp_month', 'mp_price']]
print(df)

# Plot the data
plt.scatter(df.iloc[:, 2], df.iloc[:, 3].values.astype(int))
plt.xlabel('Month')
plt.ylabel('CM price')
plt.title('Visualization of raw data')
plt.show()