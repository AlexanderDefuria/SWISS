import sqlite3
import pandas as pd


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


    df = pd.DataFrame(get_data_from_db(data_needed, team_list))

    print("\nDataFrame:\n" + str(df))

    fig = df.plot(kind='bar', rot=-20).get_figure()
    fig.dpi = 288
    fig.savefig('entry/static/entry/images/dynamic_plot.png')


    print("")
    return


def get_data_from_db(data_needed, team_list):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    index = 0

    for x in data_needed:

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

        index += 1

    compiled = []
    compiled_dict = dict.fromkeys(team_list)

    compiled_index = 0



    for team in team_list:

        print("Team LISt:" + str(team))

        compiled.append(dict.fromkeys(data_needed, 0))

        c.execute("SELECT id FROM entry_team WHERE number=?", (int(team),))

        team_id = c.fetchone()[0]

        for data_field in data_needed:

            if 'win' in data_field:
                continue

            c.execute("SELECT %s FROM entry_match WHERE team_id=?" % data_field, (team_id,))

            each_match = c.fetchall()

            print(compiled)

            for item in each_match:
                compiled[compiled_index][data_field] += item[0]

        compiled_dict[team] = compiled[compiled_index]

        compiled_index += 1

    return compiled_dict
