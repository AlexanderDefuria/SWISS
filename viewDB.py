import pandas as pd
import numpy as np
import sqlalchemy as sa
import matplotlib.pyplot as plt

conn = sa.create_engine("sqlite:///db.sqlite3")
conn = conn.connect()

df = pd.read_sql_query("select * from entry_match where match_number=2", conn)



fig, ax = plt.subplots()

fig.savefig('./entry/static/entry/images/my_plot.png')

conn.close()
