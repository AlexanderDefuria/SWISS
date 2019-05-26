
import sqlite3

current_event_key = 'No Event'
current_event_id = 0
current_district_key = '2019ont'


def get_event_id(event_name_arg):
    global current_event_id
    print("Current Event is: " + str(current_event_key) + "   with ID: " + str(get_event(current_event_key)))
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT id FROM entry_event WHERE TBA_key = ?", (event_name_arg,))
    current_event_id = c.fetchone()[0]
    return c.fetchone()[0]


def set_event(event_name_arg):
    global current_event_key
    current_event_key = event_name_arg
    return


