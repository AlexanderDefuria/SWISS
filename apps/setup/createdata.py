import random as rand
import sqlite3

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()

index = 0
match = 1
while index < 100:
    if index % 6 == 0:
        match += 1

    c.execute("SELECT id FROM entry_team WHERE event_one_id=230")
    teams = c.fetchall()
    team = rand.choice(teams)

    data = [None, match, rand.randint(0, 4), rand.randint(0, 4), rand.randint(0, 4), rand.randint(0, 8),
            rand.randint(0, 4), rand.randint(0, 4), rand.randint(0, 4), rand.randint(0, 8), rand.randint(0, 4),
            rand.randint(0, 4), rand.randint(0, 3), bool(rand.getrandbits(1)), bool(rand.getrandbits(1)),
            rand.randint(0, 50000), 230, team[0]]

    print(data[17])

    c.executemany("INSERT INTO entry_match VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (data,))

    conn.commit()
    index += 1

conn.close()

################################################################################################################

# Creates a set of realistic test data with random values within the appropriate constraints to
# Test the data visualization phase, can be deleted when there is a real data set.

################################################################################################################
