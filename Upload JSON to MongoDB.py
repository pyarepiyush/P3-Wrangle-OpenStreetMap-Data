
# #### Load cleaned JSON data into MongoDB instance

# In[16]:


# Load data into MongoDB instance

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")

# Drop database if exists
#db.osm_col.drop()

db = client.osm_col
#osm_col = db.osm_col
db.osm_col.insert_many(data)


print db.osm_col.count()

