import random


# ---------- CREATE DECK ----------
def create_deck():
    deck = []

    deck.append("0")
    deck.append("1")

    for number in range(2, 13):
        for i in range(number):
            deck.append(str(number))

    deck.extend(["+2", "+4", "+6", "+8", "x2"])

    power_cards = ["Freeze", "Second Chance", "Flip Three"]

    for card in power_cards:
        deck.append(card)
        deck.append(card)

    return deck


# ---------- DRAW CARD ----------
def draw_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card


# ---------- CHECK NUMBER ----------
def is_number(card):
    return card.isdigit()


# ---------- COUNT NUMBER CARDS ----------
def count_numbers(player):
    count = 0
    for card in player["cards"]:
        if is_number(card):
            count += 1
    return count


# ---------- CHECK DUPLICATE ----------
def has_duplicate(player, card):

    if not is_number(card):
        return False

    return card in player["cards"]


# ---------- BOT DECISION ----------
def bot_decision(player):

    numbers = count_numbers(player)

    if numbers < 4:
        return "flip"

    return random.choice(["flip", "stop"])


# ---------- DISPLAY CARDS ----------
def display_cards(player):

    card_line = ""

    for card in player["cards"]:
        card_line += f"[ {card} ] "

    return card_line


# ---------- PLAYER DISPLAY ----------
def show_players(players):

    print("\n================ PLAYERS =================")

    for p in players:
        status = ""

        if p["lost"]:
            status = " (LOST)"
        elif p["frozen"]:
            status = " (FROZEN)"
        elif p["stopped"]:
            status = " (STOPPED)"

        print(f"{p['name']:<10}: {display_cards(p)}{status}")

    print("==========================================\n")


# ---------- GET NUMBER OF PLAYERS ----------
while True:

    num_players = int(input("How many players? (minimum 2): "))

    if num_players >= 2:
        break

    print("You need at least 2 players.")


# ---------- CREATE PLAYERS ----------
players = []

for i in range(num_players):

    name = input(f"Enter name for Player {i+1}: ")

    while True:
        player_type = input("Human or Bot? ").lower()

        if player_type in ["human", "bot"]:
            break

        print("Type 'human' or 'bot'.")

    player = {
        "name": name,
        "type": player_type,
        "cards": [],
        "lost": False,
        "stopped": False,
        "frozen": False,
        "second_chance": False,
        "booster_add": 0,
        "booster_mult": 1,
        "total_score": 0
    }

    players.append(player)


# ---------- PLAY 3 GAMES ----------
for game in range(1, 4):

    print("\n\n====================================")
    print(f"            GAME {game}")
    print("====================================")

    deck = create_deck()

    for player in players:
        player["cards"] = []
        player["lost"] = False
        player["stopped"] = False
        player["frozen"] = False
        player["second_chance"] = False
        player["booster_add"] = 0
        player["booster_mult"] = 1

    print("\nFirst card draw:\n")

    for player in players:

        card = draw_card(deck)
        player["cards"].append(card)

        print(f">>> {player['name']} drew: [ {card} ]")

    game_over = False

    # ---------- GAME LOOP ----------
    while not game_over:

        show_players(players)

        for player in players:

            if player["lost"] or player["stopped"] or player["frozen"]:
                continue

            print("\n------------------------------------")
            print(f"{player['name']}'s Turn")
            print("------------------------------------")

            print("Your Cards:")
            print(display_cards(player))

            # ---------- HUMAN ----------
            if player["type"] == "human":

                while True:
                    choice = input("\nFlip or Stop? ").lower()

                    if choice in ["flip", "stop"]:
                        break

                    print("Invalid choice.")

            # ---------- BOT ----------
            else:

                choice = bot_decision(player)
                print(f"\nBot chooses: {choice}")

            # ---------- STOP ----------
            if choice == "stop":

                total = 0

                for card in player["cards"]:
                    if is_number(card):
                        total += int(card)

                total = (total + player["booster_add"]) * player["booster_mult"]

                player["total_score"] += total
                player["stopped"] = True

                print("\nScore added:", total)

            # ---------- FLIP ----------
            if choice == "flip":

                if len(deck) == 0:
                    print("Deck empty!")
                    game_over = True
                    break

                card = draw_card(deck)

                print(f"\n>>> {player['name']} drew: [ {card} ]")

                # ---------- NUMBER ----------
                if is_number(card):

                    if has_duplicate(player, card):

                        if player["second_chance"]:
                            print("Second chance used!")
                            player["second_chance"] = False
                        else:
                            print("Duplicate! You lose this game.")
                            player["lost"] = True
                            continue

                    player["cards"].append(card)

                # ---------- SECOND CHANCE ----------
                elif card == "Second Chance":

                    print("Second Chance gained!")
                    player["second_chance"] = True

                # ---------- BOOSTER + ----------
                elif card.startswith("+"):

                    value = int(card[1])
                    player["booster_add"] += value

                    print(f"Booster collected: +{value}")

                # ---------- BOOSTER x ----------
                elif card.startswith("x"):

                    multiplier = int(card[1])
                    player["booster_mult"] *= multiplier

                    print(f"Multiplier collected: x{multiplier}")

                # ---------- FREEZE ----------
                elif card == "Freeze":

                    print("\nFREEZE CARD!")

                    while True:
                        target = input("Choose player to freeze: ")

                        for p in players:
                            if p["name"].lower() == target.lower():
                                p["frozen"] = True
                                print(p["name"], "is frozen for the rest of the game!")
                                break
                        else:
                            print("Invalid player.")
                            continue

                        break

                # ---------- FLIP THREE ----------
                elif card == "Flip Three":

                    print("\nFLIP THREE CARD!")

                    while True:
                        target = input("Choose player to flip three cards: ")

                        for p in players:
                            if p["name"].lower() == target.lower():

                                print(p["name"], "must flip 3 cards!")

                                for i in range(3):

                                    if len(deck) == 0:
                                        break

                                    new_card = draw_card(deck)

                                    print(f">>> {p['name']} drew: [ {new_card} ]")

                                    if is_number(new_card):

                                        if has_duplicate(p, new_card):

                                            if p["second_chance"]:
                                                print("Second chance used!")
                                                p["second_chance"] = False
                                            else:
                                                print(p["name"], "lost due to duplicate!")
                                                p["lost"] = True
                                                break

                                        p["cards"].append(new_card)

                                break
                        else:
                            print("Invalid player.")
                            continue

                        break

                # ---------- WIN CHECK ----------
                if count_numbers(player) >= 7:

                    print("\n", player["name"], "wins this game!")

                    total = 0

                    for c in player["cards"]:
                        if is_number(c):
                            total += int(c)

                    total = (total + player["booster_add"]) * player["booster_mult"]
                    total += 10

                    player["total_score"] += total

                    print("Points gained:", total)

                    game_over = True

                    for p in players:

                        if p["name"] != player["name"] and not p["lost"]:

                            total = 0

                            for c in p["cards"]:
                                if is_number(c):
                                    total += int(c)

                            total = (total + p["booster_add"]) * p["booster_mult"]

                            p["total_score"] += total

                            print(p["name"], "survives and gains", total)

                    break

        active = False

        for p in players:
            if not p["lost"] and not p["stopped"] and not p["frozen"]:
                active = True

        if not active:
            game_over = True


# ---------- FINAL SCORES ----------
print("\n\n=========== FINAL SCORES ===========")

for player in players:
    print(player["name"], ":", player["total_score"])

winner = max(players, key=lambda p: p["total_score"])

print("\nWinner:", winner["name"])