from general.config import timetable, tables
from datetime import datetime
from general.setup import cursor
from exceptions import *
import mysql.connector.errors


# store today //assume attended all
# store today -rm x=1 //assume attended all then remove


# store custom -d date //pull -h,-a from date
# store custom -a x=1 y=2 -d date //pull -h from date

options = {"today": "today", "custom": "custom"}


def handle(args: list[str]) -> None:
    aquery = None
    hquery = None
    today = datetime.today()
    day_name = today.strftime("%A")

    # for -> store today //assume attended all
    if len(args) == 2 and args[1] == options["today"]:
        if day_name == "Sunday":
            raise InputException("Invalid date.")
        attended = dict(timetable[day_name])
        happened = dict(timetable[day_name])
        aquery = construct_insert_query(tables[0], attended)
        hquery = construct_insert_query(tables[1], happened)

    # for -> store today -rm x=1 //assume attended all then remove
    elif len(args) > 3 and args[1] == options["today"] and args[2] == "-rm":
        attended = dict(timetable[day_name])
        happened = dict(timetable[day_name])
        rm_lectures = args[3:]
        if day_name == "Sunday":
            raise InputException("Invalid date.")
        for lectures in rm_lectures:
            subject, duration = lectures.split("=")
            subject = subject.upper()  # to ignore case
            if subject not in happened:
                raise InputException("Cannot remove a lecture which did not happen.")
            if attended[subject] - int(duration) < 0:
                raise InputException("Cannot remove more total lecture duration.")

            attended[subject] -= int(duration)
        aquery = construct_insert_query(tables[0], attended)
        hquery = construct_insert_query(tables[1], happened)

    # for custom case
    elif len(args) > 2 and args[1] == options["custom"]:
        flag_data = get_flags_data(args[2:])
        if "-d" in flag_data:
            if not is_valid_and_not_sunday(flag_data["-d"][0]):
                raise InputException("Invalid date.")
            today = datetime.strptime(flag_data["-d"][0], "%Y-%m-%d")
            day_name = today.strftime("%A")
            happened = dict(timetable[day_name])
            attended = dict(timetable[day_name])
            # store custom -a x=1 y=2 -d date //pull -h from date
            if "-a" in flag_data:
                attended = {}
                lectures = flag_data["-a"]
                for lecture in lectures:
                    subject, duration = lecture.split("=")
                    subject = subject.upper()
                    if subject not in happened:
                        raise InputException(
                            "Cannot add attendance for a lecture that did not happen."
                        )
                    if int(duration) > happened[subject]:
                        raise InputException(
                            "Cannot add more then total possible duration."
                        )
                    attended[subject] = int(duration)
            aquery = construct_insert_query(tables[0], attended, flag_data["-d"][0])
            hquery = construct_insert_query(tables[1], happened, flag_data["-d"][0])
        else:
            raise InputException("Cannot enter custom day without date.")

    else:
        raise InputException("Invalid syntax.")

    try:
        cursor.execute(aquery)
        cursor.execute(hquery)
    except mysql.connector.Error as e:
        if e.errno == 1062:
            raise InsertException("Entry for that day already exists")
        if e.errno == 1054:
            raise ColumnException(
                "The table is missing columns. Reset the corrupted database"
            )
        else:
            raise e

    cursor.execute(
        f"select * from attended where s_date = '{str(today).split(' ')[0]}'"
    )
    if cursor.fetchone() == None:
        raise InsertException("Data insertion failed")
    cursor.execute(
        f"select * from happened where s_date = '{str(today).split(' ')[0]}'"
    )
    if cursor.fetchone() == None:
        raise InsertException("Data insertion failed")


# Helper Functions
def is_valid_and_not_sunday(date_string: str) -> bool:
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        return date_obj.weekday() != 6  # Sunday is 6
    except ValueError:
        return False


def get_flags_data(
    args: list[str], flags: set = {"-a", "-h", "-d"}
) -> dict[str, list[str]]:

    i = 0
    flag_data = {}
    while i < len(args):
        if args[i] not in flags:
            raise InputException("Invalid flag: " + args[i])
        if args[i] in flag_data:
            raise InputException("Mulitple times same flag.")

        flag = args[i]
        flag_data[flag] = []
        i += 1
        while i < len(args) and args[i][0] != "-":
            flag_data[flag].append(args[i])
            i += 1

    for key in flag_data:
        if len(flag_data[key]) == 0:
            raise InputException("Empty flag entered: " + key)

    return flag_data


def construct_insert_query(
    table: str, lectures: dict[str, int], date: str = None
) -> str:
    query = f"insert into {table}("
    for subject in lectures:
        query += subject + ","
    query += "day,s_date)values("
    for subject in lectures:
        query += str(lectures[subject]) + ","
    if date == None:
        query += "dayname(curdate()),curdate());"
    else:
        query += f"dayname('{date}'),'{date}');"
    return query
