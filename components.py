from typing import List, Optional
import random
from numpy import mean

class Player:
    """
    Represents a player in the game planning system.

    Attributes:
        name (str): The player's name.
        id (str): A unique identifier for the player (hashed from name by default).
        slot_availabilities (dict): A dictionary mapping slot numbers to booleans indicating availability.
        game_interests (list): A list of game IDs that the player is interested in.
    """

    def __init__(self, name:str, slot_availabilities:dict = {}, game_interests:list = [], id:Optional[str] = None) -> None:
        """
        Initializes a new Player object.
        """
        self.name = name
        self.id = hash(name) if id is None else id
        self.slot_availabilities = slot_availabilities
        self.game_interests = game_interests

    def set_name(self, name: str) -> None:
        """
        Sets the player's name.

        Args:
            name (str): The new name for the player.
        """
        self.name = name

    def set_availability(self, slot: int, available: bool) -> None:
        """
        Sets the player's availability for a specific slot.

        Args:
            slot (int): The slot number.
            available (bool): True if the player is available for the slot, False otherwise.
        """
        self.slot_availabilities[slot] = available

    def add_game_interest(self, game_id: str) -> None:
        """
        Adds a game ID to the player's list of game interests.

        Args:
            game_id (str): The ID of the game the player is interested in.
        """
        self.game_interests.append(game_id)

    def remove_game_interest(self, game_id: str) -> None:
        """
        Removes a game ID from the player's list of game interests.

        Args:
            game_id (str): The ID of the game to remove from the player's interests.
        """
        self.game_interests.remove(game_id)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the player object.

        Returns:
            dict: A dictionary containing the player's attributes.
        """
        return dict(self.__dict__)

    def __str__(self) -> str:
        """
        Returns a string representation of the player object.

        Returns:
            str: A string in the format "Player(name)".
        """
        return f"Player({self.name})"
    
class Game:
    """
    Represents a game in the game planning system.

    Attributes:
        name (str): The name of the game.
        id (str): A unique identifier for the game (hashed from name by default).
        dm (Player): The game's Dungeon Master (DM).
        max_player_count (int): The maximum number of players allowed in the game.
        min_player_count (int, optional): The minimum number of players required for the game. Defaults to 3.
        slot (int, optional): The slot number in which the game is scheduled to be played. Defaults to None.
        max_repetitions (int, optional): The maximum number of times the game can be repeated in different slots. Defaults to 1.
        fixed_players (List[Player], optional): A list of players who are pre-assigned to the game. Defaults to [].
        players (List[Player]): A list of players currently assigned to the game.
        session (int, optional): The session number within the slot where the game is planned. Defaults to None.
        repetitions (int): The number of times the game has been planned already.
    """
    def __init__(self, name:str, dm:Player, max_player_count:int, min_player_count:int = 3, slot:int = None, max_repetitions:int = 1, fixed_players:Optional[List[Player]] = []):
        """
        Initializes a new Game object.
        """
        self.name = name
        self.id = hash(name)
        self.dm = dm
        self.max_player_count = max_player_count
        self.min_player_count = min_player_count
        self.fixed_player = fixed_players
        self.players = [] + fixed_players
        self.slot = slot
        self.session = None
        self.max_repetitions = max_repetitions
        self.repetitions = 0

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the game object.

        Returns:
            dict: A dictionary containing the game's attributes.
        """
        return dict(self.__dict__)
    
    def __str__(self):
        """
        Returns a string representation of the game object.

        Returns:
            str: A string in the format "Game(name)".
        """
        return f"Game({self.name})"

class Gameplan:
    """
    Represents the overall game planning system.

    Attributes:
        total_slots (int): The total number of time slots available for game sessions.
        max_concurrent_sessions (int, optional): The maximum number of concurrent game sessions per slot. Defaults to 2.
        sessions (list): A list of dictionaries, where each dictionary represents a slot and maps session numbers to Game objects.
        games (list): A list of all games that can be potentially scheduled.
        fixed_games (list): A list of games that must be scheduled in specific slots.
        planned_games (list): A list of games that have been successfully scheduled.
        game_stats (dict): A dictionary to store statistics about game planning for each slot.
        player_stats (dict): A dictionary to store statistics about player participation.
        no_dm_placeholder (Player): A placeholder Player object representing a game without a DM.
        players (dict): A dictionary mapping player IDs to Player objects.
    """

    def __init__(self, total_slots:int, max_concurrent_sessions:int = 2):
        """
        Initializes a new Gameplan object.
        """
        self.total_slots = total_slots
        self.max_concurrent_sessions = max_concurrent_sessions
        self.sessions = [{session:None for session in range(self.max_concurrent_sessions)} for _ in range(1, total_slots+1)]
        self.games = []
        self.fixed_games = []
        self.planned_games = []
        self.game_stats = {}
        self.player_stats = {}
        
        self.no_dm_placeholder = Player(name = "No DM", slot_availabilities = {slot:True for slot in range(1, total_slots+1)}, id = "no_dm")
        self.players = {}

    def add_fixed_session(self, game:Game, slot:Optional[int] = None) -> None:
        """
        Adds a fixed game to the game plan.

        Args:
            game (Game): The game to be added as a fixed session.
            slot (int, optional): The slot number for the fixed game. If not provided, the game's `slot` attribute must be set.
        """
        if slot is None and game.slot is None:
            raise ValueError("Slot needs to be provided either in function or exist in session to be added as fixed.")
        elif game.slot is None:
            game.slot = slot
        self.fixed_sessions.append(game)

    def add_game(self, game:Game) -> None:
        """
        Adds a game to the list of potential games to be scheduled.
        If the game doesn't have a Dungeon Master (DM) assigned, it will be assigned a placeholder "No DM" player before being added.

        Args:
            game (Game): The game to be added.
        """
        if game.dm is None:
            game.dm = self.no_dm_placeholder
        self.games.append(game)

    def bulk_add_games(self, game_list:List[Game]) -> None:
        """
        Adds a list of games to the list of potential games to be scheduled.
        This method calls `add_game` for each game in the provided list.

        Args:
            game_list (List[Game]): A list of games to be added.
        """
        for game in game_list:
            self.add_game(game)

    def add_player(self, player:Player) -> None:
        """
        Adds a player to the game plan by storing them in a dictionary with their ID as the key.

        Args:
            player (Player): The player to be added.
        """
        self.players.update({player.id:player})

    def bulk_add_players(self, player_list:List[Player]) -> None:
        """
        Adds a list of players to the game plan.

        This method calls `add_player` for each player in the provided list.

        Args:
            player_list (List[Player]): A list of players to be added.
        """
        for player in player_list:
            self.add_player(player)

    def plan(self) -> None:
        """
        Plans game sessions for each slot, considering player availability, game preferences, and other constraints.

        This method iterates over each slot, selects available games, assigns players to games based on their availability and preferences, and updates the game plan accordingly.

        Steps:
            1. **Identify available players:** Determine which players are available for the current slot.
            2. **Select games:** Randomly select games from the list of available games, prioritizing games with available DMs and considering their maximum repetition limits.
            3. **Assign players to games:** Assign available players to selected games based on their game preferences and the game's maximum player count.
            4. **Update game and player information:** Update the game's player list, session number, and repetition count. Update the player's slot availability.
            5. **Calculate and store statistics:** Calculate statistics for each slot, such as the number of unmatched players, the number of planned sessions, and the utilization of player slots and game seats.
            6. **Calculate and store player statistics:** Calculate statistics for each player, such as the number of games they are interested in, the number of slots they are available for, and the number of slots they are booked in.
        """

        import copy

        for slot_number, slot_sessions in enumerate(self.sessions, start=1):
            slot_index = slot_number - 1
            # get available players
            available_players = {player_id:player for player_id, player in self.players.items() if player.slot_availabilities[slot_number] == True}
            self.game_stats[slot_number] = {"total_players_available" : len(available_players)}

            print(f"""Planning slot {slot_number}. \nAvailable Players: \n{[player.name for _, player in available_players.items()]}""")
            
            # init sessions
            
            fixed_games = [game for game in self.games if game.slot == slot_number]
            random.shuffle(self.games)

            for session, _ in slot_sessions.items():
                print(f"Planning Session: {session}")

                # Handle fixed games for the session (if any)
                if len(fixed_games) > 0:
                    current_game = fixed_games.pop()

                else:
                 # Loop until a game is successfully planned (or limit is reached)
                    planned = False
                    break_counter = 0
                    while not planned:
                        current_game = random.choice(self.games)
                        print(f"Trying: {current_game.name} by {current_game.dm.name}")
                         # Check if the DM is available for the chosen game
                        if current_game.dm.id in available_players.keys() or current_game.dm.id == "no_dm":
                            planned = True
                        else:
                            print("DM not available!")
                        
                        break_counter += 1
                        if break_counter >= len(self.games)*2:
                            break
                     # If no game could be planned after retries, continue to the next session
                    if break_counter >= len(self.games)*2:
                        continue

                modified_game = copy.deepcopy(current_game)
                
                modified_game.slot = slot_number
                modified_game.session = session

                # Remove the DM (if applicable) from the available players pool
                if modified_game.dm.id != "no_dm":
                    print(f"Deleting: {modified_game.dm.name} from {[player.name for player in available_players.values()]}")
                    del(available_players[modified_game.dm.id]) 

                # Find players interested in the chosen game (excluding the DM)
                # Randomly select players from the matched players (up to the game's max player count)
                # Add the selected players to the modified game object
                matching_players = [player for player in available_players.values() if modified_game.name in player.game_interests and player != modified_game.dm]
                print(f"Matched: {[player.name for player in matching_players]}")
                added_players = random.sample(population = matching_players, k = min(modified_game.max_player_count, len(matching_players)))
                print(f"Adding Players:  {[player.name for player in added_players]}")
                modified_game.players = modified_game.players + added_players

                 # Check if minimum player count is met, otherwise add the DM back to available players
                if len(modified_game.players) < modified_game.min_player_count:
                    available_players[modified_game.dm.id] = modified_game.dm
                    del(modified_game)
                else:
                    # Remove players from the available pool for this session
                    for player in modified_game.players:
                        print(f"Deleting: {player.name} from {[player.name for player in available_players.values()]}")
                        del(available_players[player.id])
                    
                    self.games[self.games.index(current_game)] = modified_game
                    slot_sessions[session] = modified_game
                    self.planned_games.append(modified_game)

                    # Increase Game repeat counter and remove Game from Game List if max repetitions is reached
                    modified_game.repetitions += 1
                    if modified_game.repetitions >= modified_game.max_repetitions:
                        self.games.remove(modified_game)
                    
            if len(fixed_games) > 0:
                raise NotImplementedError("More fixed games than available sessions for this slot!")
            

            # Calculate metrics for plan quality comparison
            self.game_stats[slot_number]["total_unmatched_players"] = len(available_players)
            self.game_stats[slot_number]["sessions_planned"] = sum([1 if value is not None else 0 for value in self.sessions[slot_index].values()])
            self.game_stats[slot_number]["sessions_planned_ratio"] = self.game_stats[slot_number]["sessions_planned"] / self.max_concurrent_sessions
            self.game_stats[slot_number]["players_planned_ratio"] = 1 - self.game_stats[slot_number]["total_unmatched_players"] / self.game_stats[slot_number]["total_players_available"]
            self.game_stats[slot_number]["seats_available"] = sum([game.max_player_count for game in self.sessions[slot_index].values() if game is not None])
            self.game_stats[slot_number]["seats_planned_ratio"] = 1 - self.game_stats[slot_number]["total_unmatched_players"] / self.game_stats[slot_number]["seats_available"] if self.game_stats[slot_number]["seats_available"] else 0

        for player in self.players.values():
            player_in_game = []
            for game in self.planned_games:
                player_in_game.append(player.id in [player.id for player in game.players]) 

            self.player_stats[player.name] = {
                "games_interested" : len(player.game_interests),
                "slots_available" : sum([int(value) for value in player.slot_availabilities.values()]),
                "slots_booked" : sum(player_in_game),
            }

            self.player_stats[player.name]["slots_booked_ratio"] = self.player_stats[player.name]["slots_booked"] / self.player_stats[player.name]["slots_available"]
            self.player_stats[player.name]["games_interested_ratio"] = self.player_stats[player.name]["slots_booked"] / self.player_stats[player.name]["games_interested"]

        return slot_sessions

    def to_dict(self) -> dict:
        return dict(self.__dict__)