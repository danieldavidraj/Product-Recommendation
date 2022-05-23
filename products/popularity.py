import pandas as pd
import sqlalchemy
from django.conf import settings
from urllib.parse import quote

config = getattr(settings, 'CONFIG')

user = config["database"]["DATABASE_USER"]
password = config["database"]["DATABASE_PASSWORD"]
database_name = config["database"]["DATABASE_NAME"]
host = config["database"]["DATABASE_HOST"]

engine = sqlalchemy.create_engine(f'mysql://{user}:%s@{host}/{database_name}' % quote(password))

# Use popularity based recommender model to make predictions
def recommend(user_id, popularity_recommendations):     
    user_recommendations = popularity_recommendations 
          
    #Add user_id column for which the recommendations are being generated 
    user_recommendations['user_id'] = user_id 
      
    #Bring user_id column to the front 
    cols = user_recommendations.columns.tolist() 
    cols = cols[-1:] + cols[:-1] 
    user_recommendations = user_recommendations[cols] 
          
    return user_recommendations 

def popularity_based_recommendation():
    sql = "SELECT * FROM products_products LIMIT 500"
    df = pd.read_sql(sql, engine)
    
    df = df.groupby("product_id").filter(lambda x:x['ratings'].count() >=50)

    #Count of user_id for each unique product as recommendation score 
    train_data_grouped = df.groupby('product_id').agg({'user_id': 'count'}).reset_index()
    train_data_grouped.rename(columns = {'user_id': 'score'},inplace=True)

    #Sort the products on recommendation score 
    train_data_sort = train_data_grouped.sort_values(['score', 'product_id'], ascending = [0,1]) 
        
    #Generate a recommendation rank based upon score 
    train_data_sort['rank'] = train_data_sort['score'].rank(ascending=0, method='first') 
            
    #Get the top 5 recommendations 
    popularity_recommendations = train_data_sort.head(5) 

    find_recom = 5
    return recommend(find_recom, popularity_recommendations)