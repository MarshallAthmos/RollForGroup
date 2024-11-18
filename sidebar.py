import streamlit as st
from helpers import render_svg_and_title
import pandas as pd

def sidebar():

  st.sidebar.write(f"SpielerInnen: {len(st.session_state.player_dict)}")
  st.sidebar.write(f"Games: {len(st.session_state.game_dict)}")

  st.sidebar.title("Aktuelle Konfiguration")
  if "slot_config" not in st.session_state:
    st.sidebar.write("Noch keine Konfiguration gesetzt!")
  if "slot_config" in st.session_state:
    st.session_state.slot_config["total_slots"] = st.session_state.total_slots
    st.session_state.slot_config["total_sessions"] = st.session_state.total_sessions
    config_data = pd.DataFrame.from_dict(st.session_state.slot_config, orient='index', columns=['Wert'])
    config_data = config_data.astype("str")
    config_data.index = config_data.index.map({
        "start_time_slot_1" : "Erster Zeitslot",
        "start_time_slot_2" : "Zweiter Zeitslot",	
        "event_start_date" : " Beginndatum",
        "event_end_date" : "Enddatum",	
        "first_slot_afternoon" : "Beginn Nachmittags?",	
        "no_slots_on_final_day" : "Keine Session letzter Tag?",	
        "max_concurrent_sessions" : "Max. parallele Sessions",
        "total_slots" : "Zeitslots gesamt",
        "total_sessions" : "Mögliche Sessions",
        "duration": "Dauer in Tagen"
    })
    st.sidebar.table(config_data)

  if "svg_string" not in st.session_state:
    with open("VibeCheck-Logo_Farbe.svg", "rb") as f:
      svg_string = f.read().decode("utf-8")
    rendered_svg = render_svg_and_title(svg_string = svg_string)
  st.sidebar.write(rendered_svg, unsafe_allow_html=True)