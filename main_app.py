import streamlit as st
from helpers import load_objects

st.set_page_config(
    page_title="RollForSessions"
)

if "init" not in st.session_state:
    st.session_state.init = False

def init():
    if "player_dict" not in st.session_state:
        st.session_state.player_dict = load_objects("players")

    if "game_dict" not in st.session_state:
        st.session_state.game_dict = load_objects("games")

    if "selected_player" not in st.session_state:
        st.session_state.selected_player = None

    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    if "total_sessions" not in st.session_state:
        st.session_state.total_sessions = 0

    if "total_slots" not in st.session_state:
        st.session_state.total_slots = 0

    st.session_state.init = True

if st.session_state.init == False:
    init()

home_page = st.Page("page_components/home.py", title="Home", icon=":material/home:")
config_page = st.Page("page_components/config.py", title="Konfiguration", icon=":material/settings:")
gamplan_page = st.Page("page_components/gameplan.py", title="Spielplan", icon=":material/empty_dashboard:")
games_page = st.Page("page_components/games.py", title="Games", icon=":material/casino:")
players_page = st.Page("page_components/players.py", title="SpielerInnen", icon=":material/diversity_4:")
debug_page = st.Page("page_components/debug.py", title="Debug", icon=":material/bug_report:")
save_load_page = st.Page("page_components/save_load.py", title="Speichern/Laden", icon=":material/save:")

pg = st.navigation({
    "Home" : [home_page], 
    "Config" : [config_page, save_load_page], 
    "Planning" : [players_page, games_page, gamplan_page], 
    "Dev" : [debug_page]
    })

pg.run()