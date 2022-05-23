import pandas as pd
import sqlalchemy
import numpy as np
from django.conf import settings
from urllib.parse import quote
from surprise import SVD,Reader,Dataset

config = getattr(settings, 'CONFIG')

user = config["database"]["DATABASE_USER"]
password = config["database"]["DATABASE_PASSWORD"]
database_name = config["database"]["DATABASE_NAME"]
host = config["database"]["DATABASE_HOST"]

engine = sqlalchemy.create_engine(f'mysql://{user}:%s@{host}/{database_name}' % quote(password))

def hybrid_based_recommendation():

    sql = "SELECT * FROM products_products LIMIT 500"
    new_df = pd.read_sql(sql, engine)

    svd = SVD()
    reader = Reader()

    user_id='A00635603LUUJQPQWSJW1'
    product_id='0000031887'

    data = Dataset.load_from_df(new_df[['user_id', 'product_id', 'ratings']], reader)
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    matrix=pd.pivot_table(data=new_df, values='ratings', index='user_id',columns='product_id')
    # Get the Id of the top five products that are correlated with the ProductId chosen by the user.
    top_five=matrix.corrwith(matrix[product_id]).sort_values(ascending=False).head(5)
    
    # Predict the ratings the user might give to these top 5 most correlated products.
    est_rating=[]
    for x in list(top_five.index):
        if str(top_five[x])!='nan':
            est_rating.append(svd.predict(user_id, iid=x, r_ui=None).est)
           
    return pd.DataFrame({'productId':list(top_five.index)[:len(est_rating)], 'estimated_rating':est_rating}).sort_values(by='estimated_rating', ascending=False).reset_index(drop=True)