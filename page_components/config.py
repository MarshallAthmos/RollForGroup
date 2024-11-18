import streamlit as st
from datetime import time, date, timedelta
from sidebar import sidebar

st.title("Konfiguration")

sidebar()

default_start_time_1 = time(hour=11, minute=0)
default_start_time_2 = time(hour=19, minute=0)
default_start_date = date(year=2025, month=2, day=7)
default_end_date = date(year=2025, month=2, day=11)

#def get_settings():
#    settings_to_download = {k: v for k, v in st.session_state.items() if k in ["selected_player", "days_list", "game_dict", "total_slots", "player_dict", "total_sessions", "slot_config"]}
#    return settings_to_download
#
#button_download = st.download_button(label="Download Settings",
#                                      data=pickle.dumps(get_settings()),
#                                      file_name=f"settings.pkl",
#                                      help="Click to Download Current Settings")
#
#button_upload = st.button("Konfiguration importieren")
#
#if button_download:
#   pass
#if button_upload:
#   pass

  
with st.form("new_gameplan_form", clear_on_submit=False):
    st.write("Neue Konfiguration erstellen oder bestehende modifizieren")
    event_start_date = st.date_input("Erster Eventtag", value=default_start_date)
    event_end_date = st.date_input("Letzter Eventtag", value=default_end_date)
    start_time_slot_1 = st.time_input("Startzeit Slot 1", value=default_start_time_1)
    start_time_slot_2 = st.time_input("Startzeit Slot 2", value=default_start_time_2)
    max_concurrent_sessions = st.number_input("Max. parallele Sessions", value=2, min_value=1, max_value=4)
    first_slot_afternoon = st.checkbox("Keine Session am Morgen des ersten Tags?", value=True)
    no_slots_on_final_day = st.checkbox("Keine Sessions am letzten Tag?", value=True)

    submit_button = st.form_submit_button("Konfiguration Speichern")

    if submit_button:
        st.session_state.slot_config = {
            "start_time_slot_1" : start_time_slot_1,
            "start_time_slot_2" : start_time_slot_2,
            "event_start_date" : event_start_date,
            "event_end_date" : event_end_date,
            "first_slot_afternoon" : first_slot_afternoon,
            "no_slots_on_final_day" : no_slots_on_final_day,
            "max_concurrent_sessions" : max_concurrent_sessions,
            "duration" : (event_end_date - event_start_date).days + 1,
        }

        total_slots = ((event_end_date - event_start_date).days + 1) * 2 
        if first_slot_afternoon:
            total_slots -= 1
        if no_slots_on_final_day:
            total_slots -= 2

        total_sessions = total_slots * max_concurrent_sessions
        st.session_state.total_sessions = total_sessions
        st.session_state.total_slots = total_slots
        st.session_state.days_list = [(st.session_state.slot_config["event_start_date"] + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(st.session_state.slot_config["duration"])]
    if "total_slots" in st.session_state:
        st.write(f"Total Sessions available with this configuration: {st.session_state.total_sessions}")