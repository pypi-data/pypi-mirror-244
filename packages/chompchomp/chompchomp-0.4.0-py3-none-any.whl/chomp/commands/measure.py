from chomp.data_manager import (
    add_food_diary_entry,
    get_food,
    FoodNotFoundException,
)
from chomp.utils import remaining_calories_for_today


def measure(food_name, desired_calories=None):
    if desired_calories is None:
        remaining_calories = remaining_calories_for_today()
        desired_calories = 0 if remaining_calories < 0 else remaining_calories
        print(f"You would like to eat {food_name}.")
        print(
            f"Defaulting to using all of your remaining calories for the day: {desired_calories:.0f}"
        )
    else:
        print(f"You would like to eat {desired_calories:.1f} calories of {food_name}.")

    try:
        food = get_food(food_name)
        food_weight = food.get_nutritional_fact("weight")
        cal = food.get_nutritional_fact("calories")
        required_weight = desired_calories * (food_weight / cal)

        print()
        print(f"To do this, you should eat {required_weight:.1f}g.")
    except FoodNotFoundException:
        print(f"Cannot find {food_name}!")
