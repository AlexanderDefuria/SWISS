import pandas as pd
import numpy as np
import sqlalchemy as sa
import matplotlib.pyplot as plt

conn = sa.create_engine("sqlite:///db.sqlite3")
conn = conn.connect()

df = pd.read_sql_table("entry_match", conn)
df = df.drop(["team_name", "team_number", "id", "second_start", "first_start", "climb"], axis=1)
df = df.sort_values(by="match_number")
df = df["auto_cargo"]


print(df)


plt.close(fig='all')
df.cumsum()
df.plot()
plt.show()


conn.close()
