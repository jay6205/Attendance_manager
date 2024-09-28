#! python

import mysql.connector
import general.config as db


setup_database = f"create database {db.name};"

setup_attended = (
    "create table attended("
    f"{db.subjects[0]} tinyint default 0,"
    f"{db.subjects[1]} tinyint default 0,"
    f"{db.subjects[2]} tinyint default 0,"
    f"{db.subjects[3]} tinyint default 0,"
    f"{db.subjects[4]} tinyint default 0,"
    f"{db.subjects[5]} tinyint default 0,"
    f"{db.subjects[6]} tinyint default 0,"
    f"{db.subjects[7]} tinyint default 0,"
    f"{db.subjects[8]} tinyint default 0,"
    f"{db.subjects[9]} tinyint default 0,"
    f"{db.subjects[10]} tinyint default 0,"
    f"{db.subjects[11]} tinyint default 0,"
    "day varchar(9) not null,"
    "s_date date not null,"
    "primary key (s_date));"
)

setup_happened = (
    "create table happened("
    f"{db.subjects[0]} tinyint default 0,"
    f"{db.subjects[1]} tinyint default 0,"
    f"{db.subjects[2]} tinyint default 0,"
    f"{db.subjects[3]} tinyint default 0,"
    f"{db.subjects[4]} tinyint default 0,"
    f"{db.subjects[5]} tinyint default 0,"
    f"{db.subjects[6]} tinyint default 0,"
    f"{db.subjects[7]} tinyint default 0,"
    f"{db.subjects[8]} tinyint default 0,"
    f"{db.subjects[9]} tinyint default 0,"
    f"{db.subjects[10]} tinyint default 0,"
    f"{db.subjects[11]} tinyint default 0,"
    "day varchar(9) not null,"
    "s_date date not null,"
    "primary key (s_date));"
)

connection = None
cursor = None

try:
    connection = mysql.connector.connect(
        host=db.host, user=db.user, password=db.password, database=db.name
    )
    cursor = connection.cursor()

except mysql.connector.Error as e:
    if e.errno == 1049:  # no database setup
        cxn = mysql.connector.connect(host=db.host, user=db.user, password=db.password)
        cs = cxn.cursor()
        cs.execute(setup_database)
        connection = mysql.connector.connect(
            host=db.host, user=db.user, password=db.password, database=db.name
        )
        cursor = connection.cursor()

        cursor.execute(setup_attended)
        cursor.execute(setup_happened)
    else:
        print("Unknown Error:", e)
        exit()

try:
    cursor.execute(setup_attended)
except mysql.connector.Error as e:
    if e.errno != 1050:  # table all ready setup
        print("Unknown Error:", e)
        exit()


try:
    cursor.execute(setup_happened)
except mysql.connector.Error as e:
    if e.errno != 1050:  # table all ready setup
        print("Unknown Error:", e)
        exit()
