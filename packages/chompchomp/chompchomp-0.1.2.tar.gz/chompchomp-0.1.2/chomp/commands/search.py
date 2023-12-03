from chomp.data_manager import get_food_list


def search(search_string):
    food_names = get_food_list()

    print(f"Searching for '{search_string}'.")

    match_found = False
    for name in food_names:
        if search_string in name:
            if not match_found:
                print("\nMatches:")
                match_found = True
            print(f"- {name}")
    if not match_found:
        print("No matches found!")
