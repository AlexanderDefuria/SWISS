import pandas as pd
import numpy as np
import sqlalchemy as sa
import matplotlib.pyplot as plt

conn = sa.create_engine("sqlite:///db.sqlite3")
conn = conn.connect()

df = pd.read_sql_table("entry_team", conn)


plt.close(fig='all')
fig, ax = plt.subplots()
plt.bar(df['name'], df['matches'])
fig.savefig('./entry/static/entry/images/my_plot.png')

conn.close()
