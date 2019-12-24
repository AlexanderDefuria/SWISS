
import sqlite3

current_event_key = '2019onto3'
current_event_id = 11
current_district_key = '2019ont'


def get_event_id(event_name_arg):
    global current_event_id
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT id FROM entry_event WHERE TBA_key = ?", (event_name_arg,))
    current_event_id = c.fetchone()[0]

    print("Current Event is: " + str(current_event_key) + "   with ID: " + str(current_event_id))

    return current_event_id


def set_event(event_name_arg):
    global current_event_key
    current_event_key = event_name_arg
    return


