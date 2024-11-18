import streamlit as st
from sidebar import sidebar
from components import Gameplan
import matplotlib.pyplot as plt
import pandas as pd
import copy
import pprint
from tabulate import tabulate

sidebar()

st.title(":dragon: Gamplan Roller")

n_plans = st.number_input(label="N Plans", min_value=1, max_value=10000, value=1000, step=10, help="Anzahl der zu generierenden Pläne.")

generate_button = st.button("Roll")

if generate_button:
    plans = {}
    for plan_id in range(n_plans):
        gameplan = Gameplan(total_slots=st.session_state.total_slots, max_concurrent_sessions=st.session_state.slot_config["max_concurrent_sessions"])
        gameplan.bulk_add_players(player_list=st.session_state.player_dict.values())
        gameplan.bulk_add_games(game_list=st.session_state.game_dict.values())
        gameplan.plan()

        game_stats = pd.DataFrame(gameplan.game_stats).transpose().median()[["sessions_planned_ratio", "seats_planned_ratio", "players_planned_ratio"]].to_dict()
        player_stats = pd.DataFrame(gameplan.player_stats).transpose().median()[["slots_booked_ratio", "games_interested_ratio"]].to_dict()

        plans[plan_id] = dict(gameplan = gameplan, game_stats = game_stats, player_stats = player_stats)

    st.write(f"{len(plans)} Pläne generiert!")

    game_stats = pd.DataFrame(pd.DataFrame(plans).transpose()["game_stats"].to_dict()).transpose()[["seats_planned_ratio", "players_planned_ratio"]]
    player_stats = pd.DataFrame(pd.DataFrame(plans).transpose()["player_stats"].to_dict()).transpose()
    
    fig = plt.figure()
    ax = plt.subplot()
    game_stats.plot(ax=ax)
    player_stats.plot(ax=ax)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    ax.set_xlabel("Plan ID")
    ax.set_ylabel("Score")
    st.write(fig)

    #st.write(gameplan.to_dict())
    st.write(plans)
    st.write(game_stats)
    st.write(player_stats)

    session_plan = []
    st.write(gameplan.sessions)
    for slot in gameplan.sessions:
        current_slot_games = {}
        for session, game in slot.items():
            if game is not None:
                print(session, game)
                current_slot_games[session] = game.to_dict(mode="deep")
            else:
                current_slot_games[session] = {}
        session_plan.append(current_slot_games)


    #session_plan_df = pd.DataFrame(
    #    columns=[f"Session {n}" for n in range(1, st.session_state.slot_config['max_concurrent_sessions']+1)],
    #    index = [n for n in range(1, st.session_state.total_slots+1)]
    #    )
    
    friendly_session_plan = copy.deepcopy(session_plan)
    
    for slot_idx, slot in enumerate(friendly_session_plan):
        for session_id, session in slot.items():
            pprint.pprint(session)
            if len(session) > 0:
                print("----------------------")
                print(session_id)
                player_list = ',\n'.join(session['players'])
                friendly_session_plan[slot_idx][session_id] = f"""{session['name']} \n\nDM: {session['dm']} \n\n{session['pitch'] if session['pitch'] is not None else ''} \n\nPlayers: {player_list}"""
            else:
                friendly_session_plan[slot_idx][session_id] = "KEINE GEPLANTE SESSION"
    index_names = []
    for i, day in enumerate(st.session_state.days_list):
        for timeslot in [1,2]:
            if i == 0 and timeslot == 1 and st.session_state.slot_config["first_slot_afternoon"]:
                continue
            elif i == len(st.session_state.days_list)-1 and st.session_state.slot_config["no_slots_on_final_day"]:
                continue
            else:
                index_names.append((day, st.session_state.slot_config[f"start_time_slot_{timeslot}"].strftime(("%H:%M"))))
    column_names =[f"Session {n}" for n in range(1, st.session_state.slot_config['max_concurrent_sessions']+1)]
    pprint.pprint(friendly_session_plan)
    print(index_names)
    print(column_names)
    session_plan_df = pd.DataFrame(data = friendly_session_plan)
    session_plan_df.columns=column_names
    session_plan_df.index = pd.MultiIndex.from_tuples(index_names, names=["Tag", "Uhrzeit"])
    session_plan_df.reset_index(inplace=True)
    
    tabulated_df = tabulate(session_plan_df, headers="keys", tablefmt="html", showindex=False)
    #print(tabulated_df)
    st.write(tabulated_df, unsafe_allow_html=True)