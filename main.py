from components import Player, Session, Gameplan

if __name__ == "__main__":
    slot_availabilities = {
        1: True,
        2: True,
        3: True,
        4: True
    }

    session_interests = [
        "Encounter",
        "Survival",
        "Boardgames V1",
        "Boardgames V2",
    ]

p1 = Player(name = "Marcel", slot_availabilities = slot_availabilities, session_interests = session_interests)
p2 = Player(name = "Steven", slot_availabilities = {1:True, 2:False, 3:True}, session_interests = session_interests)
p3 = Player(name = "Eric", slot_availabilities = {1:True, 2:True, 3:False}, session_interests = session_interests)
p4 = Player(name = "Rea", slot_availabilities = {1:False, 2:True, 3:True}, session_interests = session_interests)

player_list = [p1, p2, p3, p4]

s1 = Session(name = "Encounter", dm = "Marcel", max_player_count = 2)
s2 = Session(name = "Survival", dm = "Steven", max_player_count = 2)
s3 = Session(name = "Boardgames V1", dm = None, max_player_count = 2)
s4 = Session(name = "Boardgames V2", dm = "Rea", max_player_count = 2)

session_list = [s1, s2, s3, s4]

