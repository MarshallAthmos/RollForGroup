import streamlit as st
from components import Player, Game
from helpers import format_names, save_object, delete_object
from sidebar import sidebar
import random

st.title("Games")

sidebar()

def edit_game_form(selected_game:Game=None):
    if selected_game is not None:
        checkbox_data = [[True for _ in range(2)] for _ in range(st.session_state.slot_config["duration"])]
        key = "edit_game_form"
        game_name = selected_game.name
        game_id = selected_game.id
        game_dm = selected_game.dm
        game_max_player_count=selected_game.max_player_count
        game_min_player_count=selected_game.min_player_count
        game_fixed_players = selected_game.fixed_players
        game_slot = selected_game.slot
        game_max_reps = selected_game.max_repetitions
        game_pitch = selected_game.pitch
    else:
        checkbox_data = [[True for _ in range(2)] for _ in range(st.session_state.slot_config["duration"])]
        key = "new_game_form"
        game_name = None
        game_id = ""
        game_dm = None
        game_max_player_count=5
        game_min_player_count=3
        game_fixed_players = []
        game_slot = None
        game_max_reps = 1
        game_pitch = ""
    
    # Create a form
    with st.form(key, clear_on_submit=True):
        name = st.text_input("Name", value = game_name)
        pitch = st.text_area("Pitch (Markdown)", value = game_pitch, height = 136)
        disable_id_edit = key == "edit_game_form" 
        id = st.text_input("ID (Optional)", value=game_id, disabled=disable_id_edit)
        form_cols = st.columns(spec=2)
        dm_index = list(st.session_state.player_dict.keys()).index(str(game_dm.id)) if game_dm is not None else None
        dm = form_cols[0].selectbox(label="DM", options=st.session_state.player_dict.values(), format_func=format_names, placeholder="Auswählen", index=dm_index, )
        max_reps = form_cols[0].number_input(label = "Maximale Wiederholungen", value=game_max_reps)
        min_player_count, max_player_count = form_cols[1].slider(label = "Anzahl SpielerInnen", min_value=3, max_value=12, value=(game_min_player_count, game_max_player_count))
        fixed_player_default = [st.session_state.player_dict[player.id] for player in game_fixed_players] if game_fixed_players is not None else None
        fixed_players = st.multiselect(label="Fixe SpielerInnen", options=st.session_state.player_dict.values(), format_func=format_names, default=fixed_player_default)

        # Availability
#          with st.container():
#             cols = st.columns(spec = len(st.session_state.days_list)+1, vertical_alignment="top")
#             cols[0].write("Verfügbarkeit")
#             cols[0].write(st.session_state.slot_config[f"start_time_slot_1"].strftime("%H:%M"))
#             cols[0].write(st.session_state.slot_config[f"start_time_slot_2"].strftime("%H:%M"))
#
#             for day, col in enumerate(cols[1:]):
#                
#                col.write(st.session_state.days_list[day])
#                for time_of_day in range(2):
#                  if (day == 0 and time_of_day == 0 and st.session_state.slot_config["first_slot_afternoon"]) or (day == len(cols[1:])-1 and st.session_state.slot_config["no_slots_on_final_day"]):
#                    col.write("Disabled")
#                    checkbox_data[day][time_of_day] = False
#                  else:
#                    checkbox_data[day][time_of_day] = col.checkbox("", key=f"{key}_slot_{day}_{time_of_day}", value=checkbox_data[day][time_of_day], label_visibility = "collapsed")
#
#          slot_availability = sum(checkbox_data, [])
#          #st.write(slot_availability)
#
#          game_interests_selected = st.multiselect(
#            "Interessiert an:",
#            ["Game1", "Game2", "Game3", "Game4"],
#            game_interests,
#)
#
        submit_button = st.form_submit_button("Speichern")
#          
#
        if submit_button:
        # Create a new Game object with the form data
            new_game = Game(
                name=name if name is not None else f"RandomName{random.randint(0,100)}",
                id=id if id != "" else None,
                dm=dm,
                max_player_count=max_player_count,
                min_player_count=min_player_count,
                max_repetitions=max_reps,
                fixed_players=fixed_players,
                pitch=pitch
            )
            save_object(new_game, "games")
        
            if key == "new_game_form":
                st.session_state.game_dict[new_game.id] = new_game
                st.success("Game added successfully!")
                st.write(st.session_state.game_dict)
            else:
                st.session_state.game_dict[selected_game.id] = new_game
                st.success("Game updated successfully!")
                st.rerun(scope="app")

if "slot_config" not in st.session_state:
    st.write("Bitte zuerst eine Slot Konfiguration einfügen!")
else:
    with st.expander("Games hinzufügen"):
        edit_game_form(selected_game=None)

    with st.expander("Games verwalten"):
        selected_game = st.selectbox(label="Game", options = st.session_state.game_dict.values(), placeholder="Auswählen...", index=None, format_func=format_names)
        delete_game = st.button(label="Löschen")

    if delete_game:
        delete_object(selected_game, "games")
        st.rerun(scope="app")
    
    if selected_game:
        edit_game_form(selected_game=selected_game)
        st.write(selected_game.to_dict())