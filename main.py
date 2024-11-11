from components import Player, Game, Gameplan

if __name__ == "__main__":
    slot_availabilities = {
        1: True,
        2: True,
        3: True,
        4: True
    }

    game_interests = [ f"Game_{str(id).zfill(2)}" for id in range(20)]

p1 = Player(name = "Marcel", slot_availabilities = slot_availabilities, game_interests = game_interests)
p2 = Player(name = "Steven", slot_availabilities = {1:True, 2:False, 3:True}, game_interests = game_interests)
p3 = Player(name = "Eric", slot_availabilities = {1:True, 2:True, 3:False}, game_interests = game_interests)
p4 = Player(name = "Rea", slot_availabilities = {1:False, 2:True, 3:True}, game_interests = game_interests)

player_list = [p1, p2, p3, p4]

s1 = Game(name = "Encounter", dm = p1, max_player_count = 2)
s2 = Game(name = "Survival", dm = p2, max_player_count = 2)
s3 = Game(name = "Boardgames V1", dm = None, max_player_count = 2)
s4 = Game(name = "Boardgames V2", dm = p4, max_player_count = 2)

game_list = [s1, s2, s3, s4]

plan = Gameplan(2, 2)

plan.bulk_add_games(game_list=game_list)
plan.bulk_add_players(player_list=player_list)

plan_dict = plan.plan()

print(plan_dict)