import streamlit as st
from components import Player, Game
from helpers import format_names, delete_object, save_object
from sidebar import sidebar
import random

st.title("Player Management")

sidebar()

# diese beiden als nächstes einbauen!
def clean_availabilites_format(slot_availabilities):
    to_delete = []
    if st.session_state.slot_config["first_slot_afternoon"]:
        to_delete.append(1)
    if st.session_state.slot_config["no_slots_on_final_day"]:
        to_delete = to_delete + list(slot_availabilities.keys())[-2:]
    for slot in to_delete:        
        del(slot_availabilities[slot])
        print(slot_availabilities)

    return {i:value for i, (_, value) in enumerate(slot_availabilities.items(), start = 1)}

def restore_availabiliies_format(slot_availabilities):
    updates = {}
    added_slot = 0
    
    if st.session_state.slot_config["first_slot_afternoon"]:
        updates[1] = False
        added_slot = 1
    if st.session_state.slot_config["no_slots_on_final_day"]:
        updates[len(slot_availabilities)+1+added_slot] = False
        updates[len(slot_availabilities)+2+added_slot] = False
    slot_availabilities = {i:value for i, (_, value) in enumerate(slot_availabilities.items(), start = 2)}
    slot_availabilities.update(updates)
    return slot_availabilities

def edit_player_form(selected_player:Player=None):
    if selected_player is not None:
        slot_availabilities = restore_availabiliies_format(selected_player.slot_availabilities)
        slot_availabilities = [slot_availabilities[slot] for slot in range(1, len(slot_availabilities)+1)]
        checkbox_data = [slot_availabilities[i:i+2] for i in range(0, len(slot_availabilities), 2)]
        key = "player_edit_form"
        player_name = selected_player.name
        id = selected_player.id
        game_interests = selected_player.game_interests
    else:
        checkbox_data = [[True for _ in range(2)] for _ in range(st.session_state.slot_config["duration"])]
        key = "new_player_form"
        player_name = None
        id = ""
        game_interests = None

    
    # Player Data Form
    with st.form(key, clear_on_submit=True):
        # General Data
        name = st.text_input("Name", value = player_name)
        disable_id_edit = key == "player_edit_form" 
        player_id = st.text_input("ID (Optional)", value=id, disabled=disable_id_edit) 

        # Availability
        with st.container():
            cols = st.columns(spec = len(st.session_state.days_list)+1, vertical_alignment="top")
            cols[0].write("Verfügbarkeit")
            cols[0].write(st.session_state.slot_config[f"start_time_slot_1"].strftime("%H:%M"))
            cols[0].write(st.session_state.slot_config[f"start_time_slot_2"].strftime("%H:%M"))

            for day, col in enumerate(cols[1:]):
                col.write(st.session_state.days_list[day])
                for time_of_day in range(2):
                    if (day == 0 and time_of_day == 0 and st.session_state.slot_config["first_slot_afternoon"]) or (day == len(cols[1:])-1 and st.session_state.slot_config["no_slots_on_final_day"]):
                        col.write("Disabled")
                        checkbox_data[day][time_of_day] = False
                    else:
                        checkbox_data[day][time_of_day] = col.checkbox(label = f"slot selector {day}_{time_of_day}", key=f"{key}_slot_{day}_{time_of_day}", value=checkbox_data[day][time_of_day], label_visibility = "collapsed")

        slot_availability = sum(checkbox_data, [])

        # Game Interests
        game_interests_selected = st.multiselect(
        label = "Interessiert an:",
        options = st.session_state.game_dict.values(),
        format_func=format_names,
        default = [st.session_state.game_dict[game.id] for game in game_interests] if game_interests is not None else None
)
        submit_button = st.form_submit_button("Speichern")
        

        if submit_button:
            new_player = Player(
                name=name if name is not None else f"RandomName{random.randint(0,100)}",
                id=player_id if player_id != "" else None,
                slot_availabilities=clean_availabilites_format({i+1: available for i, available in enumerate(slot_availability)}),
                game_interests=game_interests_selected
            )

            save_object(new_player, "players")

            if key == "new_player_form":
                st.session_state.player_dict[new_player.id] = new_player
                st.toast('Player added successfully!')
                #st.success("Player added successfully!")
            else:
                st.session_state.player_dict[selected_player.id] = new_player
                st.toast('Player updated successfully!')
                #st.success("Player updated successfully!")
                selected_player = None
                st.rerun(scope="app")

if "slot_config" not in st.session_state:
    st.write("Bitte zuerst eine Slot Konfiguration einfügen!")
else:
    with st.expander("SpielerIn hinzufügen"):
        edit_player_form(selected_player=None)

    #st.write(st.session_state.player_dict)

    with st.expander("SpielerInnen verwalten"):
        selected_player = st.selectbox(label="SpielerIn", options = st.session_state.player_dict.values(), placeholder="Auswählen...", index=None, format_func=format_names)
        delete_player = st.button(label="Löschen")
#
    if delete_player:
        delete_object(selected_player, "players")
        st.rerun(scope="app")
    st.write(st.session_state.player_dict)
        
    if selected_player:
        edit_player_form(selected_player=selected_player)
        st.write(selected_player.to_dict())