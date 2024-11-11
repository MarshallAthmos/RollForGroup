from typing import List, Optional
import random

class Player:
    def __init__(self, name:str, slot_availabilities:dict = {}, game_interests:list = []) -> None:
        self.name = name
        self.id = hash(name)
        self.slot_availabilities = slot_availabilities
        self.game_interests = game_interests

    def set_name(self, name:str) -> None:
        self.name = name

    def set_availability(self, slot:int, available:bool) -> None:
        self.slot_availabilities[slot] = available

    def add_game_interest(self, game_id:str) -> None:
        self.game_interests.append(game_id)
    
    def remove_game_interest(self, game_id:str) -> None:
        self.game_interests.remove(game_id)


    def to_dict(self) -> dict:
        return dict(self.__dict__)
    
class Game:
    def __init__(self, name:str, dm:str, max_player_count:int, slot:int = None, max_repetitions:int = 1):
        self.name = name
        self.id = hash(name)
        self.dm = dm
        self.max_player_count = max_player_count
        self.slot = slot
        self.max_repetitions = max_repetitions
        self.repetitions = 0

    def to_dict(self) -> dict:
        return dict(self.__dict__)

class Gameplan:
    def __init__(self, total_slots:int, max_concurrent_sessions:int = 2):
        self.total_slots = total_slots
        self.max_concurrent_sessions = max_concurrent_sessions
        self.sessions = [{session:None for session in range(self.max_concurrent_sessions)} for _ in range(total_slots)]
        self.games = []
        self.fixed_games = []
        self.planned_games = []
        self.players = []

    def add_fixed_session(self, game:Game, slot:Optional[int] = None) -> None:
        if slot is None and game.slot is None:
            raise ValueError("Slot needs to be provided either in function or exist in session to be added as fixed.")
        elif game.slot is None:
            game.slot = slot
        self.fixed_sessions.append(game)

    def add_game(self, game:Game) -> None:
        self.games.append(game)

    def bulk_add_games(self, game_list:List[Game]) -> None:
        for game in game_list:
            self.add_session(game)

    def add_player(self, player:Player) -> None:
        self.players.append(player)

    def bulk_add_players(self, player_list:List[Player]) -> None:
        for player in player_list:
            self.add_player(player)

    def plan(self) -> None:
        for slot_number, slot_sessions in enumerate(self.sessions):
            # get available players
            available_players = [player for player in self.players if player.slot_availabilities[slot_number] == True]
            
            # init sessions
            
            fixed_games = [game for game in self.games if game.slot == slot_number]
            random.shuffle(self.games)

            for session, _ in slot_sessions.items():
                if len(fixed_games) > 0:
                    current_game = fixed_games.pop()
                    slot_sessions[session] = current_game
                    self.planned_games.append(current_game)
                else:
                    not_set = True
                    break_counter = 0
                    while not_set:
                        current_game = self.games[break_counter]
                        if current_game.dm in available_players:
                            slot_sessions[session] = current_game
                            not_set = False
                            available_players.remove(current_game.dm)

                            # Increase Game repeat counter and remove Game from Game List if max repetitions is reached
                            self.games[break_counter].repetitions += 1
                            if self.games[break_counter].repetitions >= self.games[break_counter].max_repetitions:
                                self.games.remove(current_game)
                        
                        break_counter += 1
                        if break_counter >= len(self.games):
                            break


            if len(fixed_games) > 0:
                raise NotImplementedError("More fixed games than available sessions for this slot!")
            
                
            # match players to sessions
            # compare match threshold >> else try again



    def to_dict(self) -> dict:
        return dict(self.__dict__)