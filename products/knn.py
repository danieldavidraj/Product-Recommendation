import pandas as pd
import sqlalchemy
import math
import numpy as np
from django.conf import settings
from urllib.parse import quote
from sklearn.neighbors import NearestNeighbors

config = getattr(settings, 'CONFIG')

user = config["database"]["DATABASE_USER"]
password = config["database"]["DATABASE_PASSWORD"]
database_name = config["database"]["DATABASE_NAME"]
host = config["database"]["DATABASE_HOST"]

engine = sqlalchemy.create_engine(f'mysql://{user}:%s@{host}/{database_name}' % quote(password))

def knn_based_recommendation():
    sql = "SELECT * FROM products_products LIMIT 5000"
    df = pd.read_sql(sql, engine)
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    pivot_df = df.pivot(index = 'user_id', columns ='product_id', values = 'ratings').fillna(0)
    model_knn.fit(pivot_df)
    pivot_df=pivot_df.iloc[:10000]
    query_index = np.random.choice(pivot_df.shape[0])
    distances, indices = model_knn.kneighbors(pivot_df, n_neighbors = 1)
    try:
        df = pd.DataFrame(columns=['rank','product_id','distance'])
        for i in range(0, len(distances.flatten())):
            if distances.flatten()[i] != 0:
                if i == 0:
                    print('Recommendations for {0}:\n'.format(pivot_df.index[query_index]))
                else:
                    df.loc[-1] = [i, pivot_df.index[indices.flatten()[i]], distances.flatten()[i]]
                    df.index = df.index + 1
        print(df)
        return df
    except IndexError:
        print('Reduced Recommendations')