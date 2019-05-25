
import sqlite3

current_event = "Ryerson"


def get_event(event_name_arg):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT id FROM entry_event WHERE name = ?", (event_name_arg,))
    return c.fetchone()[0]


def set_event(event_name_arg):
    current_event = event_name_arg
    return


print("Current Event is: " + str(current_event) + "   with ID: " + str(get_event(current_event)))
