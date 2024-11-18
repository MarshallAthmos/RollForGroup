# Python Game Planning Application

This document describes a Python application designed to assist with game planning and scheduling. It considers player availability, game preferences, and other constraints to create a schedule of games for each time slot.

## Features:

* Manages players and their availability for different time slots.
* Defines games with attributes like name, Dungeon Master (DM), minimum and maximum player count, and repetition limits.
* Handles fixed games that must be scheduled in specific slots.
* Plans game sessions for each time slot, considering player and game availability, preferences, and constraints.
* Tracks statistics such as the number of planned games, player participation, and slot utilization.

## Structure:

* **Player class:**
  * Represents a player with attributes like name, ID (hashed from name), slot availability, and game interests.
* **Game class:**
  * Represents a game with attributes like name, ID (hashed from name), DM, maximum player count, minimum player count (optional), slot (optional), maximum repetitions (optional), fixed players (optional), assigned players, session (optional), and repetition count.
* **Gameplan class:**
  * Represents the overall game planning system with attributes like total slots, maximum concurrent sessions per slot, sessions (a dictionary mapping session numbers to games), games (list of all potential games), fixed_games (list of games pre-assigned to slots), planned_games (list of successfully scheduled games), game_stats (dictionary storing slot-based statistics), player_stats (dictionary storing player participation statistics), a "No DM" placeholder player, and a dictionary mapping player IDs to player objects.

## Functionality:

* **Add players and games:** Add players and potential games to the system.
* **Add fixed games:** Assign specific games to specific slots.
* **Plan games:** Iterate through time slots and schedule games based on availability and preferences.
* **Access results:** Get planned games and statistics.

## Usage:

1. **Create a `Gameplan` object:** Define the total number of time slots and the maximum number of concurrent sessions per slot.
2. **Add players and games:** Use the `add_player` and `add_game` methods.
3. **Add fixed games (optional):** Use the `add_fixed_session` method.
4. **Plan the games:** Call the `plan` method.
5. **Access results:** The `planned_games` list, `game_stats`, and `player_stats` will contain the results.

**Note:**

This is a basic structure for a game planning application. Further development could involve features like user interface integration, saving and loading plans, and more sophisticated scheduling algorithms.

## Streamlit Commands:
streamlit run frontend.py
./.venv/Scripts/activate