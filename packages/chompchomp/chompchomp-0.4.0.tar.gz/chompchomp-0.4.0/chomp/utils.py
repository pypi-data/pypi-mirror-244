from datetime import datetime
from datetime import timedelta
from time import time

from chomp.config_manager import get_nutritional_targets
from chomp.food import Food


def get_beginning_of_day_timestamp():
    today = datetime.today()
    start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_day.timestamp()


def get_current_time_key():
    return str(int(time()))


def days_since_today(timestamp):
    now = datetime.now()
    point_in_time = datetime.fromtimestamp(int(timestamp))

    return (now - point_in_time) / timedelta(days=1)


def remaining_calories_for_today():
    from chomp.data_manager import (
        get_food_diary,
    )

    food_diary = get_food_diary()
    start_of_day = get_beginning_of_day_timestamp()

    # determine calories eaten today
    combined_intake = None
    for timestamp in food_diary:
        if int(timestamp) < start_of_day:
            continue

        entry = food_diary[timestamp]
        if "food" not in entry:
            print(" missing food diary data for entry.. skipping")
            continue

        time_of_day = datetime.fromtimestamp(int(timestamp))
        food = Food.from_dict(entry["food"])
        calories = round(food.get_nutritional_fact("calories") or 0)

        if combined_intake is None:
            combined_intake = food
        else:
            combined_intake += food

    if combined_intake is None:
        print("No food recorded for today!")
        return

    total_calories = int(combined_intake.get_nutritional_fact("calories"))
    target_calories = int(get_nutritional_targets().get("calories", 0))
    if target_calories == 0:
        return 0

    return target_calories - total_calories
