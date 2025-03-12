import matplotlib.pyplot as plt
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ChinookDB"]

# Access collections
tracks_collection = db["Tracks"]
genre_collection = db["Genre"]

# Count tracks per genre
genre_counts = {}
for genre in genre_collection.find():
    genre_id = genre["GenreId"]
    genre_name = genre["Name"]
    track_count = tracks_collection.count_documents({"GenreId": genre_id})
    if track_count > 0:
        genre_counts[genre_name] = track_count

# Sort genres by track count (descending order)
sorted_genres = dict(sorted(genre_counts.items(), key=lambda item: item[1], reverse=True))

# Prepare data for the pie chart
labels = list(sorted_genres.keys())
sizes = list(sorted_genres.values())

# Create the pie chart
plt.figure(figsize=(10, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'})
plt.title("Genre Distribution of Tracks in Chinook Database")
plt.axis("equal")  # Ensures the pie chart is circular

# Show the chart
plt.show()
