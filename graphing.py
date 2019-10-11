import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_teams_graph(form_data):

    print(pd.Series(form_data))

    team_list = []
    data_needed = []
    to_pop = []
    for x in form_data:
        form_data[x] = form_data[x][0]
        if form_data[x] == 'NaN' or form_data[x] == 'false':
            to_pop.append(x)
        elif 'team' in x:
            team_list.append(form_data[x])
        elif 'type' not in x:
            data_needed.append(x)

    for x in to_pop:
        form_data.pop(x)

    #print(data_needed)

    compiled = get_data_from_db(data_needed, team_list)

    print(compiled)

    dataframe = {'Teams': team_list,}

    #print(dataframe)

    df = pd.DataFrame(dataframe)

    print(df)



    return


def get_data_from_db(data_needed, team_list):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    index = -1
    for x in data_needed:
        index += 1
        if x == 'totalHatches' or x == 'averageHatches':
            data_needed[index] = 'first_hatch'
            data_needed.append('second_hatch')
            data_needed.append('third_hatch')
            data_needed.append('cargo_hatch')
        elif x == 'totalCargo' or x == 'averageCargo':
            data_needed[index] = 'first_cargo'
            data_needed.append('second_cargo')
            data_needed.append('third_cargo')
            data_needed.append('ship_cargo')
        elif x == 'totalDefense' or x == 'averageDefense':
            data_needed[index] = 'defense_time'

    compiled = dict.fromkeys(data_needed, list)

    for team in team_list:

        c.execute("SELECT id FROM entry_team WHERE number=?", (int(team),))

        team_id = c.fetchone()[0]

        for data_field in data_needed:

            #print(team_id)

            if 'win' in data_field:
                continue

            c.execute("SELECT " + data_field + " FROM entry_match WHERE team_id=?", (int(team_id),))

            try:
                for x in c.fetchall()[0]:
                    compiled[data_field] += x
            except IndexError:
                compiled[data_field] += 0

    return compiled
