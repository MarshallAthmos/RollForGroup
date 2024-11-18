import streamlit as st
from sidebar import sidebar
from helpers import save_object
from components import Player, Game
import random

sidebar()

def roll_test_objects():
    n_slots = st.session_state.total_slots

    def generate_availability_and_interest(n_slots:int, player_list:list, game_list:list) -> None:
        for player in player_list:
            sample_size = random.randint(8, 15)
            sampled_list = list(set(random.sample(game_list, sample_size)))

            player.slot_availabilities = {slot: random.random() > 0.25 for slot in range(1, n_slots+1)}
            player.game_interests = [game for game in sampled_list]

    def generate_random_text(max_words=4) -> str:
        words = ["hello", "world", "dnd", "boardgames", "fun", "beer", "booze", "tavern", "mystery", "murder", "deeznutz", "goblin", "sneak attack", "smite"]
        text = " ".join(random.sample(words, random.randint(1, max_words)))
        return text

    def generate_games(n_games:int, player_list:list) -> list:
        game_list = []
        mod_player_list = player_list + [None]
        for _ in range(n_games):
            name = generate_random_text()
            dm = random.choice(mod_player_list)
            id = name
            max_player_count = random.randint(4,8)
            game_list.append(Game(name=name, id=id, dm=dm, max_player_count=max_player_count))
        return game_list
        
    player_names = ["Steven", "Rea", "Eric", "Tim", "Marcel", "Matthias", "Jenny", "Maxim", "Nicole", "Lennart", "Marc", "Thea", "Christian", "Lara", "Kalahari", "Aurora", "Hazim", "Antares", "Drex", "Hector", "Draugur", "Tazhazzar"]

    player_list = [Player(name = name, id = name) for name in player_names]
    game_list = generate_games(n_games = 20, player_list = player_list)
    generate_availability_and_interest(n_slots = n_slots, player_list = player_list, game_list = game_list)

    for player in player_list:
        save_object(player, "players")
        st.session_state.player_dict[player.id] = player

    for game in game_list:
        save_object(game, "games")
        st.session_state.game_dict[game.id] = game

test_data_button = st.button("Random Encounter")

if test_data_button:
    roll_test_objects()

st.write(st.session_state)