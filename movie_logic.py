"""
movie_logic.py

This module prompts and handle the user input and get
and handle calls from movie.py and movie_storage.py.
"""
import random
import statistics
import matplotlib.pyplot as plt
from rapidfuzz import process, fuzz
from colorama import Fore, Style
import movie_storage_sql as storage

# colors (colorama):
# Title & Goodbye = YELLOW
# Ask for user input = LIGHTGREEN_EX
# Error or info output = RED
# Results = CYAN


def get_movie_list():
    """Iterates through the movie data
    and print out a list of movies with rating and release year"""
    movies = storage.list_movies()
    print(f"{Fore.CYAN}{len(movies)} movies in total")
    for title, details in movies.items():
        rating = details['rating']
        year = details['year']
        print(f"{Fore.CYAN}Title: {title}, "
              f"rating: {rating}, "
              f"year: {year}{Style.RESET_ALL}")
    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue{Style.RESET_ALL}")
    print()


def prompt_add_movie():
    """Prompts the user to add a movie
    and checks if the movie still exists."""
    title = input(f"{Fore.LIGHTGREEN_EX}Enter a new movie name:"
                  f" {Style.RESET_ALL}").strip()
    if not title:
        print(f"{Fore.RED}Invalid input! Cannot be empty."
              f"{Style.RESET_ALL}")
        return

    movies = storage.list_movies()

    for movie in movies:
        if (isinstance(movie, dict)
                and movie.get('title', '').lower() == title.lower()):
            print(f"{Fore.RED}Movie already exists.{Style.RESET_ALL}")
            return

    storage.add_movie(title)
    print(f"{Fore.CYAN}Movie successfully added{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue"
          f"{Style.RESET_ALL}")


def prompt_delete_movie():
    """Prompt the user to delete a movie
    and calls the storage function."""
    title = input(f"{Fore.LIGHTGREEN_EX}Enter movie name to delete: "
                  f"{Style.RESET_ALL}").strip()
    if not title:
        print(f"{Fore.RED}Invalid input! Cannot be empty."
              f"{Style.RESET_ALL}")
        return

    was_deleted = storage.delete_movie(title)

    if was_deleted:
        print(f"{Fore.CYAN}Movie {title} "
              f"successfully deleted{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Movie {title} doesn't exist!"
              f"{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue{Style.RESET_ALL}")


def prompt_update_movie():
    """Prompt the user for movie title to update
    and checks if the movie still exists."""
    title = input(f"{Fore.LIGHTGREEN_EX}Enter movie name: "
                  f"{Style.RESET_ALL}").strip()
    if not title:
        print(f"{Fore.RED}Invalid input! Cannot be empty."
              f"{Style.RESET_ALL}")
        return

    try:
        rating = float(input(f"{Fore.LIGHTGREEN_EX}"
                             f"Enter new movie rating (0-10 float): "
                             f"{Style.RESET_ALL}"))
        if not (0 <= rating <= 10):
            print(f"{Fore.RED}Rating {rating} "
                  f"is invalid! Number must be between 0 and 10.{Style.RESET_ALL}")
            return
    except ValueError:
        print(f"{Fore.RED}Invalid input! "
              f"Please enter a number (0-10){Style.RESET_ALL}")
        return

    was_updated = storage.update_movie(title, rating)

    if was_updated:
        print(f"{Fore.CYAN}Movie {title} "
              f"successfully updated{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Movie {title} doesn't exist!"
              f"{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue{Style.RESET_ALL}")


def calculate_average_rating(movies):
    """Calculate the average rating of movie data."""
    try:
        ratings = [movie['rating'] for movie in movies]
        return statistics.mean(ratings)
    except statistics.StatisticsError:
        print(f"{Fore.RED}No ratings available to calculate average."
              f"{Style.RESET_ALL}")
        return 0


def calculate_median_rating(movies):
    """Calculate the median rating of movie data."""
    try:
        ratings = [movie['rating'] for movie in movies]
        return statistics.median(ratings)
    except statistics.StatisticsError:
        print(f"{Fore.RED}No ratings available to calculate median."
              f"{Style.RESET_ALL}")
        return 0


def get_best_movies(movies):
    """Return the titles of movies with the highest rating."""
    try:
        if not movies:
            return [], None
        max_rating = max(movie['rating'] for movie in movies)
        best = [movie['title'] for movie in movies if movie['rating'] == max_rating]
        return best, max_rating
    except (KeyError, ValueError, TypeError):
        print(f"{Fore.RED}No ratings available to determine best movies."
              f"{Style.RESET_ALL}")
        return [], None


def get_worst_movies(movies):
    """Return the titles of movies with the lowest rating."""
    try:
        if not movies:
            return [], None
        min_rating = min(movie['rating'] for movie in movies)
        worst = [movie['title'] for movie in movies if movie['rating'] == min_rating]
        return worst, min_rating
    except (KeyError, ValueError, TypeError):
        print(f"{Fore.RED}No ratings available to determine worst movies."
              f"{Style.RESET_ALL}")
        return [], None


def print_movie_stats(movies):

    """Call the functions to calculate and display it."""
    average = calculate_average_rating(movies)
    median = calculate_median_rating(movies)
    best_movies, max_rating = get_best_movies(movies)
    worst_movies, min_rating = get_worst_movies(movies)

    print(f"{Fore.CYAN}Average rating: {average:.1f}")
    print(f"Median rating: {median:.1f}")


    for title in best_movies:
        print(f"Best movie(s): {title}, {max_rating}")

    for title in worst_movies:
        print(f"Worst movie(s): {title}, {min_rating}{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue{Style.RESET_ALL}")


def get_movie_stats():
    """Fetch movies and show statistics."""
    movies = get_movies()
    print_movie_stats(movies)


def get_random_movie():
    """Pick a random movie from the movie storage"""
    movies = get_movies()
    movie = random.choice(movies)
    title = movie['title']
    rating = movie['rating']
    year = movie['year']
    print(f"{Fore.CYAN}Your movie tonight: {title}({year}), "
          f"it's rated {rating}{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue{Style.RESET_ALL}")


def search_movie():
    """This function compare the input from user
    with similar results. With the rapidfuzz module
    you can adjust the finding results.
    Print out similar results."""
    movies = get_movies()
    search_input = input(f"{Fore.LIGHTGREEN_EX}Enter a part of a movie name:"
                         f" {Style.RESET_ALL}").strip().lower()
    if not search_input:
        print(f"{Fore.RED}Invalid input! Cannot be empty."
              f"{Style.RESET_ALL}")
        return

    found = False

    for movie in movies: # loop to find movies
        title = movie['title']
        rating = movie['rating']
        year = movie['year']
        if search_input in title.lower():
            print(f"{Fore.CYAN}The movie {title}({year}) "
                  f"with rating {rating}{Style.RESET_ALL}")
            found = True

    if not found:
        print(f"{Fore.RED}\nNo movie found!{Style.RESET_ALL}")

        # Adjusting for sensitivity by finding results
        movie_titles = [movie['title'] for movie in movies]
        matches = process.extract(search_input,
                                  movie_titles,
                                  scorer=fuzz.ratio,
                                  limit=3)
        threshhold_sensitive = 30  # Adjust sensitivity for results
        similar_movies = [match for match, score,_ in matches if score >= threshhold_sensitive]

        if similar_movies:
            for title in similar_movies:
                print(f"{Fore.CYAN}Did you mean: {title}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No similar movies found!{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue{Style.RESET_ALL}")


def sort_movies_by_rank():
    """Sorted the movies by rating,
    reverse it for descending output from storage module"""
    movies = get_movies()
    sorted_movies = sorted(movies, key=lambda movie: movie['rating'],
                           reverse=True)

    for movie in sorted_movies:
        print(f"{Fore.CYAN}{movie['title']}: "
              f"{movie['rating']}{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue{Style.RESET_ALL}")
