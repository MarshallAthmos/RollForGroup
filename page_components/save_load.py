import streamlit as st
from sidebar import sidebar
from helpers import delete_object

sidebar()

st.write("This is empty")

save_button = st.button("Planung Speichern")

if save_button:
    pass

reset_button = st.button(":skull: Power Word: Kill", help="Resets EVERYTHING! Use with caution.")

if reset_button:
    players_to_delete = list(st.session_state.player_dict.values())
    games_to_delete = list(st.session_state.game_dict.values())
    for player in players_to_delete:
        delete_object(player, "players")
    for game in games_to_delete:
        delete_object(game, "games")