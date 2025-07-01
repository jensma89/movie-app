"""
movie_storage_sql.py
This file is handling the database options.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.begin() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """))


def list_movies():
    """Retrieve all movies from the database."""
    with engine.begin() as connection:
        result = connection.execute(
            text("SELECT title, "
                 "year, "
                 "rating "
                 "FROM movies"))
        movies = result.mappings().all()

    return {row['title']:
                {'year': row['year'],
                 'rating': row['rating']}
            for row in movies}


def add_movie(title, year, rating):
    """Add a new movie to the database."""
    with engine.begin() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies "
                     "(title, year, rating) "
                     "VALUES (:title, :year, :rating)"),
                {"title": title,
                 "year": year,
                 "rating": rating})
            print(f"Movie '{title}' added successfully.")
        except IntegrityError:
            print(f"Movie '{title}' already exists.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.begin() as connection:
        result = connection.execute(
            text("DELETE FROM movies "
                 "WHERE title = :title"),
            {"title": title}
        )

        if result.rowcount > 0:
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.begin() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating "
                 "WHERE title = :title"),
            {"title": title, "rating": rating}
        )

        if result.rowcount > 0:
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")
