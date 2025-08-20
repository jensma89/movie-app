"""
movie_storage_sql.py
This file is handling the database options.
"""

from colorama import Fore, Style
from core.movie_api import fetch_movie_by_title as fetch_movie
from requests.exceptions import RequestException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.begin() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT
        )
    """))


def list_movies():
    """Retrieve all movies from the database."""
    with engine.begin() as connection:
        result = connection.execute(
            text("SELECT title, "
                 "year, "
                 "rating,"
                 "poster "
                 "FROM movies"))
        movies = result.mappings().all()

    return {row['title']:
                {'year': row['year'],
                 'rating': row['rating'],
                 'poster': row['poster']}
            for row in movies}


def add_movie(title):
    """Add a new movie from API to the database."""
    try:
        data = fetch_movie(title)
    except RequestException as e:
        print(f"{Fore.RED}Network error "
              f"while fetching movie: {e}{Style.RESET_ALL}")
        return

    if not data:    # Error movie not found
        print(f"{Fore.RED}Movie '{title}' "
              f"not found in the database.{Style.RESET_ALL}")
        return

    year = data.get("Year", "Unknown")
    rating_raw = data.get("imdbRating", "N/A")
    try:
        rating = float(rating_raw) \
            if rating_raw != "N/A" \
            else None
    except ValueError:
        rating = None
    poster = data.get("Poster")

    with engine.begin() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies "
                     "(title, year, rating, poster) "
                     "VALUES (:title, :year, :rating, :poster)"),
                {"title": data.get("Title"),
                 "year": year,
                 "rating": rating,
                 "poster": poster})
            print(f"Movie '{data.get("Title")}' added successfully.")
        except IntegrityError:
            print(f"Movie '{title}' already exists.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.begin() as connection:
        result = connection.execute(
            text("DELETE FROM movies "
                 "WHERE LOWER(title) = LOWER(:title)"),
            {"title": title}
        )

        if result.rowcount > 0:
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")

        return result.rowcount > 0


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.begin() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating "
                 "WHERE LOWER(title) = LOWER(:title)"),
            {"title": title, "rating": rating}
        )

        if result.rowcount > 0:
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")
