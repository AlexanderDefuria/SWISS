import json
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
from apps import config

# Have to use this method to import from 'FRC-Scouting" cause a module cannot be hyphenated, this is a workaround.
import importlib
settings = importlib.import_module("FRC-Scouting.settings")


def create_teams_graph(form_data):
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

        df.rename(columns={'total_hatch': 'TOTAL'}, inplace=True)

        print("\nDataFrame:\n" + str(df))

        fig = df.plot(kind='bar', rot=-20).get_figure()
        fig.dpi = 400
        fig.savefig(str(settings.BASE_DIR) + "/media/dynamic_plot.png")
    except TypeError:
        print("\nEmpty Dataframe...")
        img = plt.imread(str(settings.BASE_DIR) + "/media/blank_plot.png")
        plt.imsave(str(settings.BASE_DIR) + "/media/dynamic_plot.png", img)

    print("")
    return


def get_data_from_db(data_needed, team_list):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    aliases = {}
    socring_path = str(settings.BASE_DIR) + '/scoring.json'
    with open(socring_path, 'r') as myfile:
        data = myfile.read()
        aliases = json.loads(data)

    compiled = {}
    compiled_dict = dict.fromkeys(team_list)

    for team in team_list:
        c.execute("SELECT id FROM entry_team WHERE number=?", (int(team),))
        team_id = c.fetchone()[0]

        for data_field in data_needed:

            # Skip over wins for now
            if 'win' in data_field:
                continue
            # Combine all the field values for totals
            if 'total' in data_field:
                if 'hatch' in data_field:
                    gamepeice = "hatch"
                elif 'cargo' in data_field:
                    gamepeice = "cargo"
                else:
                    continue

                totalValue = 0

                # Get values from the first_gampeice from each match in record for the team at the event
                c.execute("SELECT %s FROM entry_match WHERE team_id=? AND event_id=?" % ("first_" + gamepeice),
                          (team_id, config.current_event_id))
                result = c.fetchall()
                # by match add the value to the total
                for match in result:
                    totalValue += int(str(match[0]))

                c.execute("SELECT %s FROM entry_match WHERE team_id=? AND event_id=?" % ("second_" + gamepeice),
                          (team_id, config.current_event_id))
                result = c.fetchall()
                for match in result:
                    totalValue += int(str(match[0]))

                c.execute("SELECT %s FROM entry_match WHERE team_id=? AND event_id=?" % ("third_" + gamepeice),
                          (team_id, config.current_event_id))
                result = c.fetchall()
                for match in result:
                    totalValue += int(str(match[0]))

                c.execute("SELECT %s FROM entry_match WHERE team_id=? AND event_id=?" % ("ship_" + gamepeice),
                          (team_id, config.current_event_id))
                result = c.fetchall()
                for match in result:
                    totalValue += int(str(match[0]))

                print(gamepeice + " TOTAL VALUE:  " + str(totalValue))

                compiled[aliases[data_field]["alias"]] = totalValue
                continue

            # Regular fields
            # Data fields for each match
            print("data_field:  " + data_field)
            c.execute("SELECT %s FROM entry_match WHERE team_id=? AND event_id=?" % data_field,
                      (team_id, config.current_event_id))
            each_match = c.fetchall()

            for item in each_match:
                print("Compiled  " + str(compiled))
                try:
                    compiled[aliases[data_field]["alias"]] += item[0]
                except KeyError:
                    compiled[aliases[data_field]["alias"]] = item[0]

        compiled_dict[team] = compiled

    print(compiled_dict)

    return compiled_dict
