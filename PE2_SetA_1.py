# PE2_SetA_1.py
# Name: [Your Name]
# Course and Section: [Your Course]
# Assigned Set Letter: A
# Filename: PE2_SetA_1.py
# Programming Task: Display top 10 best-selling artists using Flet & MongoDB

import flet as ft
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ChinookDB"]
invoices_collection = db["Invoices"]
artists_collection = db["Artists"]

# Aggregate sales per artist
pipeline = [
    {
        "$lookup": {
            "from": "Tracks",
            "localField": "_id",
            "foreignField": "AlbumId",
            "as": "tracks"
        }
    },
    {
        "$unwind": "$tracks"
    },
    {
        "$lookup": {
            "from": "Invoices",
            "localField": "tracks.TrackId",
            "foreignField": "TrackId",
            "as": "sales"
        }
    },
    {
        "$group": {
            "_id": "$_id",
            "artist_name": {"$first": "$Name"},
            "total_sales": {"$sum": {"$size": "$sales"}}
        }
    },
    {
        "$sort": {"total_sales": -1}
    },
    {
        "$limit": 10
    }
]

top_artists = list(artists_collection.aggregate(pipeline))

# Flet App
def main(page: ft.Page):
    page.title = "Top 10 Best-Selling Artists"
    page.add(ft.Text("Top 10 Best-Selling Artists", size=20, weight="bold"))

    # DataTable
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Artist")),
            ft.DataColumn(ft.Text("Total Sales"))
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(artist["artist_name"])),
                    ft.DataCell(ft.Text(str(artist["total_sales"])))
                ]
            ) for artist in top_artists
        ]
    )

    page.add(table)

ft.app(target=main)
