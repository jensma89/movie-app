"""
movies.py

This module is a Movie App to ask user for input and will handle date
from the movie_storage module.
"""
import sys
import movie_logic as ml
from colorama import Fore, Style
import movie_storage_sql as storage

# colors (colorama):
# Title & Goodbye = YELLOW
# Ask for user input = LIGHTGREEN_EX
# Error or info output = RED
# Results = CYAN


def show_menu():
    """Show the menu in the console"""
    print(f"{Fore.YELLOW}\nMenu:{Style.RESET_ALL}")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Create rating histogram")
    print("0. Exit")


def main():
    """Call the menu function to show it,
    menu handling conditions to call the functions
    from movie storage via the number choose by the user."""
    print(f'{Fore.YELLOW}\n{"*" * 10} My Movies Database '
          f'{"*" * 10}{Style.RESET_ALL}')
    print()


    while True:
        show_menu()
        user_choice = input(f"{Fore.LIGHTGREEN_EX}"
                            f"Enter choice (1-10): {Style.RESET_ALL}")
        print()


        if user_choice == "0":
            print(f"{Fore.YELLOW}\nBye!{Style.RESET_ALL}")
            sys.exit()
        elif user_choice == "1":
            ml.get_movie_list()
        elif user_choice == "2":
            ml.prompt_add_movie()
        elif user_choice == "3":
            ml.prompt_delete_movie()
        elif user_choice == "4":
            ml.prompt_update_movie()
        elif user_choice == "5":
            ml.get_movie_stats()
        elif user_choice == "6":
            ml.get_random_movie()
        elif user_choice == "7":
            ml.search_movie()
        elif user_choice == "8":
            ml.sort_movies_by_rank()
        elif user_choice == "9":
            ml.create_rating_histogram()
        else:
            print(f"{Fore.RED}\nInvalid input, "
                  f"please try again.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
