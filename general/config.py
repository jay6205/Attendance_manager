name = "attendance"
user = "MYSQL_USER_NAME"
password = "MYSQL_PASSWORD"
host = "MYSQL_HOST"

tables = ("attended","happened")

subject_min = 70 #minimum required per subject in %
overall_min = 75 #minimum required overall in %

subjects = (
    "DBMS",  # 0
    "DE",  # 1
    "DS",  # 2
    "UHV",  # 3
    "HON",  # 4
    "DT_PRAC",  # 5
    "EM",  # 6
    "OE",  # 7
    "DS_PRAC",  # 8
    "DBMS_PRAC",  # 9
    "IPD",  # 10
    "CE",  # 11
)

timetable = {
    "Monday": {
        subjects[0]: 1,
        subjects[1]: 1,
        subjects[2]: 1,
        subjects[3]: 1,
        subjects[4]: 1,
    },
    "Tuesday": {
        subjects[5]: 2,
        subjects[0]: 1,
        subjects[6]: 1,
        subjects[7]: 1,
        subjects[2]: 1,
    },
    "Wednesday": {
        subjects[7]: 1,
        subjects[1]: 1,
        subjects[6]: 1,
        subjects[3]: 1,
    },
    "Thursday": {
        subjects[2]: 1,
        subjects[9]: 2,
        subjects[0]: 1,
        subjects[3]: 1,
    },
    "Friday": {
        subjects[7]: 1,
        subjects[6]: 1,
        subjects[8]: 2,
    },
    "Saturday": {
        subjects[10]: 1,
        subjects[11]: 1,
        subjects[4]: 2,
    },
}
