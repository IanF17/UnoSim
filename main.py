import random


class Card:
    def __init__(self, color, type):
        self.color = color
        self.type = type


# CREATES AN UNO DECK
deck = []

types = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "skip", "reverse", "plus2"]
colors = ["red", "blue", "yellow", "green"]

for x in colors:
    for y in types:
        deck.append(Card(x, y))

for x in colors:
    for y in range(1, len(types)):
        deck.append(Card(x, types[y]))

for x in range(1, 5):
    deck.append(Card("all", "plus4"))

for x in range(1, 5):
    deck.append(Card("all", "wild"))

# HOW MANY PLAYERS ARE PLAYING
numOfPlayers = int(input("How many players are there (Between 2 and 10): "))

players = [[] for _ in range(numOfPlayers)]

# ADD 7 RANDOM CARDS TO EACH PLAYERS HAND
for x in range(0, numOfPlayers):
    for y in range(7):
        if deck:
            pick = random.randint(0, len(deck) - 1)
            players[x].append(deck.pop(pick))

# PRINT ALL PLAYERS STARTING HAND
for i, hand in enumerate(players):
    print(f"Player {i + 1}'s Hand:")
    for card in hand:
        print(f"{card.color} {card.type}")
    print()

discard = []

draw = random.randint(0, len(deck) - 1)
discard.append(deck.pop(draw))

topCard = Card(discard[len(discard) - 1].color, discard[len(discard) - 1].type)

print("The starting card is: " + discard[len(discard) - 1].color + " " + discard[len(discard) - 1].type)

# IF THE STARTING CARD IS A WILD CARD, LET PLAYER 1 DECIDE WHAT COLOR IT SHOULD BE
if topCard.color == "all":
    for card2 in players[0]:
        if card2.color != "all":
            topCard.color = card2.color
            print(f"Player 1 is making the color: {card2.color}")
            break
        elif card2 == players[0][len(players) - 1]:
            topCard.color = "red"
            print(f"Player 1 is making the color: red")
            break

# CONDITIONS TO DETERMINE IF A PLAYER DRAWS CARDS, IS SKIPPED, ETC.
playOn = True
pickAndPlay = True
drawFour = True
drawTwo = True
skipped = True
# reversing = False
reverse = True
direction = 1

# "i" IS THE INDEX OF THE LIST "PLAYERS" TO KEEP TRACK OF WHICH PLAYER'S TURN IT IS
# "i" WILL INCREASE UNTIL A REVERSE CARD IS PLAYED. THEN IT WILL DECREASE UNTIL ANOTHER REVERSE CARD IS PLAYED
# INCREMENTATION IS DONE THROUGH THE VARIABLE "DIRECTION", WHICH IS ALWAYS EITHER 1 OR -1
i = 0
num_players = len(players)
# THE GAMEPLAY
while playOn:

    i %= num_players

    pickAndPlay = True
    # IF TOP CARD IS PLUS4, CURRENT PLAYER DRAWS 4 CARDS AND LOSES THEIR TURN
    if topCard.type == "plus4" and drawFour:
        if deck:
            for j in range(4):
                pick = random.randint(0, len(deck) - 1)
                players[i].append(deck.pop(pick))
            print(f"Player {i + 1} draws 4 cards. They now have {len(players[i])} cards")
            drawFour = False
            i += direction
            continue
        else:
            print(f"Deck is empty, Player {i + 1}. Game over (for now)")
            break
    # IF TOP CARD IS PLUS2, CURRENT PLAYER DRAWS 2 CARDS AND LOSES THEIR TURN
    if topCard.type == "plus2" and drawTwo:
        if deck:
            for j in range(2):
                pick = random.randint(0, len(deck) - 1)
                players[i].append(deck.pop(pick))
            print(f"Player {i + 1} draws 2 cards. They now have {len(players[i])} cards")
            drawTwo = False
            i += direction
            continue
        else:
            print(f"Deck is empty, Player {i + 1}. Game over (for now)")
            break
    # IF TOP CARD IS SKIP, CURRENT PLAYER LOSES THEIR TURN
    if topCard.type == "skip" and skipped:
        print(f"Player {i + 1} is skipped")
        skipped = False
        i += direction
        continue
    # IF TOP CARD IS REVERSE, SWITCH THE DIRECTION OF THE LOOP TO CHANGE PLAYER TURN DIRECTION
    if topCard.type == "reverse" and reverse:
        direction *= -1
        i += direction * 2
        reverse = False
        continue

    # SEE WHAT CARDS IN A PLAYERS HAND ARE PLAYABLE, AND PLAY IT
    for card in players[i]:
        if card.color == topCard.color or card.type == topCard.type or card.color == "all":
            discard.append(card)
            players[i].remove(card)
            topCard = Card(discard[len(discard) - 1].color, discard[len(discard) - 1].type)
            print(f"Player {i + 1} plays: " + discard[len(discard) - 1].color + " " + discard[len(discard) - 1].type)
            if discard[len(discard) - 1].type == "skip":
                skipped = True
            elif discard[len(discard) - 1].type == "plus2":
                drawTwo = True
            elif discard[len(discard) - 1].type == "reverse":
                reverse = True
            if discard[len(discard) - 1].color == "all":
                if discard[len(discard) - 1].type == "plus4":
                    drawFour = True
                for card2 in players[i]:
                    if card2.color != "all":
                        topCard.color = card2.color
                        print(f"Player {i + 1} is making the color: {card2.color}")
                        break
                    elif card2 == players[i][len(players[i]) - 1]:
                        topCard.color = "red"
                        print(f"Player {i + 1} is making the color: red")
                        break
            break
        # IF THE LAST CARD IN A PLAYERS HAND CANNOT BE PLAYED, THE PLAYER DRAWS A CARD
        if card == players[i][len(players[i]) - 1] and pickAndPlay:
            if deck:
                pick = random.randint(0, len(deck) - 1)
                players[i].append(deck.pop(pick))
                print(f"Player {i + 1} draws a card. They now have {len(players[i])} cards")
                pickAndPlay = False
            else:
                print(f"Deck is empty, Player {i + 1}. Game over (for now)")
                break

    # CHECKS AFTER EACH TURN TO SEE IF THE CURRENT PLAYER IS OUT OF CARDS. IF SO, THE GAME ENDS AND THEY WIN
    if len(players[i]) < 1:
        print(f"Player {i + 1} is out of cards! They win!")
        playOn = False
        break

    i += direction
