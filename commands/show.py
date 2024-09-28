from exceptions import InputException
from general.config import overall_min, subject_min, subjects, tables
from general.setup import cursor
from commands.store import get_flags_data
from termcolor import colored
import mysql.connector.errors

# show all
# show -s x y z


def handle(args: list[str]) -> None:
    get_all = False
    to_get = set()
    if len(args) == 2 and args[1] == "all":
        get_all = True
    elif len(args) > 2 and args[1] == "-s":
        flag_data = get_flags_data(args[1:], {"-s"})

        for subject in flag_data["-s"]:
            if subject.upper() in subjects:
                to_get.add(subject.upper())
            else:
                raise InputException("Unknown Subject.")
    else:
        raise InputException("Invalid Syntax")

    attendance_data = get_sum_data(subjects) if get_all else get_sum_data(list(to_get))

    if get_all:
        total_attended = 0
        total_happened = 0
        for subject in attendance_data:
            total_attended += attendance_data[subject][0]
            total_happened += attendance_data[subject][1]
            percentage = attendance_data[subject][0] / attendance_data[subject][1] * 100
            to_print = None
            if percentage >= subject_min:
                to_print = colored(f"{round(percentage,2)}%", "green")
            else:
                to_print = colored(f"{round(percentage,2)}%", "red")
            print(f"{subject} -> Percentage:", to_print)
        percentage = total_attended / total_happened * 100
        if percentage >= overall_min:
            print("\nOverall Percentage:", colored(f"{round(percentage,4)}%", "green"))
        else:
            print("\nOverall Percentage:", colored(f"{round(percentage,4)}%", "red"))

    else:
        for subject in attendance_data:
            percentage = attendance_data[subject][0] / attendance_data[subject][1] * 100
            space_len = len(subject) + 3
            print(subject, "-> Attended:", attendance_data[subject][0])
            print(" " * space_len, "Total:", attendance_data[subject][1])
            color = "green" if percentage >= subject_min else "red"
            print(
                " " * space_len,
                "Percentage:",
                colored(f"{round(percentage,4)}%", color),
            )
            print()


def get_sum_data(subjects: list[str]) -> dict[str, tuple[int, int]]:
    attendance_data = {}
    for subject in subjects:
        try:
            cursor.execute(f"select sum({subject}) from {tables[0]};")
            attended = cursor.fetchone()[0]
            cursor.execute(f"select sum({subject}) from {tables[1]};")
            happened = cursor.fetchone()[0]
            attendance_data[subject] = (attended, happened)
        except mysql.connector.Error as e:
            raise e
    return attendance_data
