"""
movie_storage.py

This module will handle with movie data
from a JSON file.
"""
import json as js


FILENAME = "movie_data.json"


def get_movies():
    """Read the JSON data file and return a list of movies.
    If the file invalid or not found, it will return an empty list."""
    try:
        with open(FILENAME, "r") as fileobject:
            return js.load(fileobject)
    except (FileNotFoundError, js.JSONDecodeError):
        print("Error: invalid JSON file or not found!")
        return []


def save_movies(movies):
    """Save the data to the JSON file."""
    with open(FILENAME, "w", encoding="utf-8") as fileobject:
        js.dump(movies, fileobject, indent=2)


def add_movie(title, rating, year):
    """Check for existence of the input movie,
    if not exist, the function will add a new movie to the list."""
    movies = get_movies()
    new_movie = {
        "title": title,
        "rating": rating,
        "year": year
    }
    movies.append(new_movie)
    save_movies(movies)


def delete_movie(title):
    """Check for valid input of the movie and will delete it."""
    movies = get_movies()
    updated_movies = [movie for movie in movies
                      if movie['title'].lower() != title.lower()]
    if len(movies) != len(updated_movies):
        save_movies(updated_movies)
        return True
    return False


def update_movie(title, rating):
    """If the input fits to the stored movie,
    the function will update the movie
    and save it with function call."""
    movies = get_movies()
    for movie in movies:
        if movie['title'].lower() == title.lower():
            movie['rating'] = rating
            save_movies(movies)
            return True
    return False
