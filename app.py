from pymongo import MongoClient
import heapq

class PriorityQueue:
    def _init_(self, db_name="trend_analyzer", collection_name="priority_queue"):
        self.client = MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.heap = []  # Initialize heap
        self.counter = 0  # Unique counter to avoid comparison issues

    def insert(self, user):
        heapq.heappush(self.heap, (-user["trend_score"], self.counter, user))  # Max heap by trend score
        self.counter += 1

    def store_in_mongo(self):
        while self.heap:
            _, _, user = heapq.heappop(self.heap)
            self.collection.insert_one(user)  # Insert into MongoDB
        print("Users stored in priority queue.")

    def display_queue(self):
        return list(self.collection.find({}, {"_id": 0}))  # Retrieve all users

# List of 10 users with trend scores and hashtags
users = [
    {"username": "alice", "trend_score": 94, "hashtags": ["#codinglife", "#instagram", "#health", "#investing"]},
    {"username": "bob", "trend_score": 94, "hashtags": ["#motivation", "#powerbi", "#datasciencejobs", "#mysql"]},
    {"username": "charlie", "trend_score": 84, "hashtags": ["#html", "#projects", "#python", "#cloud"]},
    {"username": "david", "trend_score": 71, "hashtags": ["#stress", "#analysis", "#pythondeveloper", "#boxplots"]},
    {"username": "emma", "trend_score": 87, "hashtags": ["#resume", "#timeseries", "#ukraine", "#security"]},
    {"username": "frank", "trend_score": 77, "hashtags": ["#recommendation", "#healthcare", "#statistics", "#datasciencejobs"]},
    {"username": "grace", "trend_score": 79, "hashtags": ["#data", "#datavisualization", "#statistics", "#stockmarket"]},
    {"username": "henry", "trend_score": 71, "hashtags": ["#casestudies", "#jobsearch", "#investing", "#machinelearning"]},
    {"username": "isabella", "trend_score": 77, "hashtags": ["#linux", "#html", "#machinelearningprojects", "#datascienceprojects"]},
    {"username": "jack", "trend_score": 84, "hashtags": ["#stress", "#casestudies", "#timeseriesmalaysia", "#timeseriesanalysis"]}
]

# Initialize and store users in MongoDB priority queue
pq = PriorityQueue()
for user in users:
    pq.insert(user)
pq.store_in_mongo()

# Display stored users
stored_users = pq.display_queue()
for user in stored_users:
    print(user)