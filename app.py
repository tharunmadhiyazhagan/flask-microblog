import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
  app = Flask(__name__)
  try:
      client = MongoClient(os.getenv("MONGODB_URI"))
      app.db = client.microblog2
      print("SUCESSFULL CONNECTION TO MONGODB: DB:",str(app.db))
  except Exception as e:
        print("Error connecting to MongoDB:", str(e))
        app.db = None  # Set app.db to None to indicate a failed connection


  @app.route("/", methods=["GET", "POST"])
  def home():
    if request.method == "GET":
      try:
        # Check if there are any entries in the database
        num_entries = app.db.entries.count_documents({})

        if num_entries > 0:
            # If there are entries, create the list
            entries_with_date = [
                (entry["content"], entry["date"], datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"))
                for entry in app.db.entries.find({})
            ]
        else:
            # If there are no entries, set entries_with_date to an empty list
            entries_with_date = []
      except Exception as e:         
        print("Error connecting to MongoDB:", str(e))
         

    if request.method == "POST":
      entry_content = request.form.get("content")
      formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
      app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

    # entries_with_date = [
    #   (entry["content"], entry["date"], datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"))
    #   for entry in app.db.entries.find({})
    # ]
    return render_template("home.html", entries=entries_with_date)
  return app   

if __name__ == "__main__":
  app = create_app()
  app.run(host="0.0.0.0", port=5000)



