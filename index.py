from pymongo import MongoClient

class TrendingHashtags:
    def _init_(self, db_name="trend_analyzer", collection_name="trending_hashtags"):
        self.client = MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def store_hashtags(self, hashtags):
        self.collection.delete_many({})  # Clear previous data
        hashtag_data = [{"hashtag": tag, "count": count} for tag, count in hashtags]
        self.collection.insert_many(hashtag_data)
        print("Top 20 trending hashtags stored in MongoDB.")

    def display_hashtags(self):
        return list(self.collection.find({}, {"_id": 0}))  # Retrieve stored hashtags

# Top 20 trending hashtags from your dataset with occurrence counts (in exact order)
top_20_hashtags = [
    ("#amankharwal", 117), ("#thecleverprogrammer", 117), ("#python", 109), ("#machinelearning", 97),
    ("#pythonprogramming", 95), ("#datascience", 94), ("#ai", 91), ("#pythonprojects", 90),
    ("#artificialintelligence", 89), ("#data", 88), ("#dataanalytics", 87), ("#datascientist", 83),
    ("#pythoncode", 78), ("#dataanalysis", 77), ("#deeplearning", 75), ("#machinelearningprojects", 43),
    ("#datascienceprojects", 43), ("#programming", 26), ("#technology", 25), ("#coding", 24)
]

# Store trending hashtags in MongoDB
th = TrendingHashtags()
th.store_hashtags(top_20_hashtags)

# Display stored hashtags
stored_hashtags = th.display_hashtags()
for hashtag in stored_hashtags:
    print(hashtag)