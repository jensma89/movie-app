"""
movie_api.py

Fetch the data from the OMDB API to handle and store with DB.
"""
import os

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OMDB_API_KEY")


def fetch_movie_by_title(title):
    """Fetch the movies by title from the API."""
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Can not fetch movie title.")
        return None
