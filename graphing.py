import sqlite3
import pandas as pd
from entry import config


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

    try:
        df = pd.DataFrame(get_data_from_db(data_needed, team_list))

        print("\nDataFrame:\n" + str(df))

        fig = df.plot(kind='bar', rot=-20).get_figure()
        fig.dpi = 288
        fig.savefig('entry/static/entry/images/dynamic_plot.png')
    except TypeError:
        print("\n\nEmpty Dataframe  .........  Therefore there is no updated graph")

    print("")
    return


def get_data_from_db(data_needed, team_list):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    compiled = []
    compiled_dict = dict.fromkeys(team_list)
    compiled_index = 0

    for team in team_list:
        compiled.append(dict.fromkeys(data_needed, 0))

        c.execute("SELECT id FROM entry_team WHERE number=?", (int(team),))
        team_id = c.fetchone()[0]

        for data_field in data_needed:
            if 'win' in data_field:
                continue

            if 'total' in data_field:
                if 'Hatch' in data_field:
                    gamepeice = "hatch"
                elif 'Cargo' in data_field:
                    gamepeice = 'cargo'
                else:
                    continue

                c.execute("SELECT %s FROM entry_match WHERE team_id=? AND event_id=?" % ("first_" + gamepeice),
                          (team_id, config.current_event_id))
                totalHatchValue = c.fetchone()[0]
                c.execute("SELECT %s FROM entry_match WHERE team_id=? AND event_id=?" % ("second_" + gamepeice),
                          (team_id, config.current_event_id))
                totalHatchValue += c.fetchone()[0]
                c.execute("SELECT %s FROM entry_match WHERE team_id=? AND event_id=?" % ("third_" + gamepeice),
                          (team_id, config.current_event_id))
                totalHatchValue += c.fetchone()[0]
                c.execute("SELECT %s FROM entry_match WHERE team_id=? AND event_id=?" % ("ship_" + gamepeice),
                          (team_id, config.current_event_id))
                totalHatchValue += c.fetchone()[0]
                compiled[compiled_index][data_field] = totalHatchValue
                continue

            c.execute("SELECT %s FROM entry_match WHERE team_id=? AND event_id=?" % data_field, (team_id, config.current_event_id))
            each_match = c.fetchall()

            for item in each_match:
                compiled[compiled_index][data_field] += item[0]

        compiled_dict[team] = compiled[compiled_index]
        compiled_index += 1

    return compiled_dict
