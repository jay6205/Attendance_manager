#! python

from mysql.connector import Error as MySQLError
from sys import argv
from commands import store, show
from general.setup import connection
from exceptions import *

args = argv[1:]

commands = {"store": store.handle, "show": show.handle}

if len(args) == 0:
    print("Error:", "No such usage.")
    connection.close()
    exit()

if args[0] not in commands:
    print("Error:", "No such command.")
    connection.close()
    exit()

try:
    commands[args[0]](args)
except ValueError as e:
    print("Error:", "Invalid values entered.")
except InputException as e:
    print("Error:", e.message)
except InsertException as e:
    print("Error:", e.message)
except ColumnException as e:
    print("Error:", e.message)
except MySQLError as e:
    print(e)
except Exception as e:
    print("Unknown Error:", e)
finally:
    connection.commit()
    connection.close()
