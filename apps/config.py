import sqlite3

current_event_key = 'ONBAR'
current_event_id = 0
current_district_key = 'ONT'


def get_event_id(event_name_arg):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    return c.execute("SELECT id FROM entry_event WHERE TBA_key = ?", (event_name_arg,))


def get_current_event_id():
    return current_event_id


def set_event(event_name_arg):
    global current_event_key
    current_event_key = event_name_arg
    return
