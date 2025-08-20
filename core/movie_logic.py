"""
movie_logic.py

This module prompts and handle the user input and get
and handle calls from movie.py and movie_storage.py.
"""
import random
import statistics

from colorama import Fore, Style
from movie_storage import movie_storage_sql as storage
from rapidfuzz import process, fuzz


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
    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue"
          f"{Style.RESET_ALL}")
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
            print(f"{Fore.RED}Movie already exists."
                  f"{Style.RESET_ALL}")
            return

    storage.add_movie(title)
    print(f"{Fore.CYAN}Movie successfully added"
          f"{Style.RESET_ALL}")

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

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue"
          f"{Style.RESET_ALL}")


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
                  f"is invalid! Number must be between 0 and 10."
                  f"{Style.RESET_ALL}")
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

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue"
          f"{Style.RESET_ALL}")


def calculate_average_rating(movies):
    """Calculate the average rating of movie data."""
    try:
        ratings = [details['rating']
                   for _, details in movies.items()]
        return statistics.mean(ratings)
    except statistics.StatisticsError:
        print(f"{Fore.RED}No ratings available to calculate average."
              f"{Style.RESET_ALL}")
        return 0


def calculate_median_rating(movies):
    """Calculate the median rating of movie data."""
    try:
        ratings = [details['rating']
                   for _, details in movies.items()]
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
        max_rating = max(details['rating']
                         for details in movies.values())
        best = [title for title, details in movies.items()
                if details['rating'] == max_rating]
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
        min_rating = min(details['rating']
                         for details in movies.values())
        worst = [title for title, details in movies.items()
                 if details['rating'] == min_rating]
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
        print(f"Worst movie(s): {title}, {min_rating}"
              f"{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue"
          f"{Style.RESET_ALL}")


def get_movie_stats():
    """Fetch movies and show statistics."""
    movies = storage.list_movies()
    print_movie_stats(movies)


def get_random_movie():
    """Pick a random movie from the movie storage."""
    movies = storage.list_movies()
    if not movies:
        print(f"{Fore.RED}No movies available.{Style.RESET_ALL}")
        return

    title, details = random.choice(list(movies.items()))
    rating = details['rating']
    year = details['year']

    print(f"{Fore.CYAN}Your movie tonight: {title} ({year}), "
          f"it's rated {rating}{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue"
          f"{Style.RESET_ALL}")


def search_movie():
    """Search movies by partial title, include fuzzy matching."""
    movies = storage.list_movies()
    search_input = input(f"{Fore.LIGHTGREEN_EX}Enter a part of a movie name:"
                         f" {Style.RESET_ALL}").strip().lower()
    if not search_input:
        print(f"{Fore.RED}Invalid input! Cannot be empty."
              f"{Style.RESET_ALL}")
        return

    found = False

    for title, details in movies.items():
        rating = details['rating']
        year = details['year']
        if search_input in title.lower():
            print(f"{Fore.CYAN}The movie {title} ({year}) "
                  f"with rating {rating}{Style.RESET_ALL}")
            found = True

    if not found:
        print(f"{Fore.RED}\nNo movie found!{Style.RESET_ALL}")

        # Fuzzy matching fallback
        movie_titles = list(movies.keys())
        matches = process.extract(search_input, movie_titles,
                                  scorer=fuzz.ratio, limit=3)
        threshold_sensitive = 30
        similar_movies = [match for match, score, _ in matches
                          if score >= threshold_sensitive]

        if similar_movies:
            for title in similar_movies:
                print(f"{Fore.CYAN}Did you mean: {title}?"
                      f"{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No similar movies found!"
                  f"{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue"
          f"{Style.RESET_ALL}")


def sort_movies_by_rank():
    """Sorted the movies by rating,
    reverse it for descending output from storage module"""
    movies = storage.list_movies()
    sorted_movies = sorted(
        movies.items(),
        key=lambda item: item[1]['rating'],
        reverse=True
    )

    for title, details in sorted_movies:
        print(f"{Fore.CYAN}{title}: "
              f"{details['rating']}{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue"
          f"{Style.RESET_ALL}")


def generate_website():
    """Generate a website template."""
    movies = storage.list_movies()

    # Read template file
    try:
        with (open("../_static/index_template.html", "r", encoding="utf-8")
              as template_file):
            html_template = template_file.read()
    except FileNotFoundError:
        print(f"{Fore.RED}Template file not found! "
              f"{Style.RESET_ALL}")
        return

    # Create movie-grid
    movie_grid_html = ""
    for title, info in movies.items():
        poster_url = (info.get('poster', '')
                      or "https://via.placeholder.com/150")

        movie_html = f"""
        <li>
            <div class="movie">
                <div class="movie-poster">
                    <img src="{poster_url}" alt="{title} poster">
                </div>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{info['year']}</div>
            </div>
        </li>
        """
        movie_grid_html += movie_html

    # Replace placeholder
    final_html = html_template.replace("__TEMPLATE_TITLE__",
                                       "My movie collection")
    final_html = final_html.replace("__TEMPLATE_MOVIE_GRID__",
                                    movie_grid_html)

    # Save as index.html
    try:
        with (open("../_static/index.html", "w", encoding="utf-8")
              as output_file):
            output_file.write(final_html)
        print(f"{Fore.CYAN}Website was generated successfully."
              f"{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Failed to write index.html: {e}"
              f"{Style.RESET_ALL}")

    input(f"{Fore.LIGHTGREEN_EX}\nPress Enter to continue"
          f"{Style.RESET_ALL}")
