import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()
# cur.execute("select * from entry_match where id is 47;")

df = pd.read_sql_query("select * from entry_match where team_name is 'MaxTech';", conn)


#results = cur.fetchall()


print(df)

plt.close(fig='all')
df.cumsum()
plt.figure()
df.plot()
plt.show()



conn.close()