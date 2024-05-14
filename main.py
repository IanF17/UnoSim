import random


# def multByRand(num):
#     randMult = random.randint(1, 10)
#     p = randMult * num
#     return p
#
#
# if __name__ == "__main__":
#     x = input("Enter a number: ")
#
#     number = int(x)
#
#     multNum = multByRand(number)
#     print(f"Result is: {multNum}")

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

# IF TOP CARD IS A WILD CARD, LET PLAYER 1 DECIDE WHAT COLOR IT SHOULD BE
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
reversing = False
direction = 1

# THE GAMEPLAY
while playOn:

    for i, hand in enumerate(players):
        pickAndPlay = True
        # IF TOP CARD IS PLUS4, CURRENT PLAYER DRAWS 4 CARDS AND LOSES THEIR TURN
        if topCard.type == "plus4" and drawFour:
            if deck:
                for j in range(4):
                    pick = random.randint(0, len(deck) - 1)
                    players[i].append(deck.pop(pick))
                print(f"Player {i + 1} draws 4 cards. They now have {len(hand)} cards")
                drawFour = False
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
                print(f"Player {i + 1} draws 2 cards. They now have {len(hand)} cards")
                drawTwo = False
                continue
            else:
                print(f"Deck is empty, Player {i + 1}. Game over (for now)")
                break
        # IF TOP CARD IS SKIP, CURRENT PLAYER LOSES THEIR TURN
        if topCard.type == "skip" and skipped:
            print(f"Player {i + 1} is skipped")
            skipped = False
            continue

        # SEE WHAT CARDS IN A PLAYERS HAND ARE PLAYABLE, AND PLAY IT
        for card in hand:
            if card.color == topCard.color or card.type == topCard.type or card.color == "all":
                discard.append(card)
                hand.remove(card)
                topCard = Card(discard[len(discard) - 1].color, discard[len(discard) - 1].type)
                print(
                    f"Player {i + 1} plays: " + discard[len(discard) - 1].color + " " + discard[len(discard) - 1].type)
                if discard[len(discard) - 1].type == "skip":
                    skipped = True
                elif discard[len(discard) - 1].type == "plus2":
                    drawTwo = True
                if discard[len(discard) - 1].color == "all":
                    if discard[len(discard) - 1].type == "plus4":
                        drawFour = True
                    for card2 in hand:
                        if card2.color != "all":
                            topCard.color = card2.color
                            print(f"Player {i + 1} is making the color: {card2.color}")
                            break
                        elif card2 == hand[len(hand) - 1]:
                            topCard.color = "red"
                            print(f"Player {i + 1} is making the color: red")
                            break
                break
            # IF THE LAST CARD IN A PLAYERS HAND CANNOT BE PLAYED, THE PLAYER DRAWS A CARD
            if card == hand[len(hand) - 1] and pickAndPlay:
                if deck:
                    pick = random.randint(0, len(deck) - 1)
                    players[i].append(deck.pop(pick))
                    print(f"Player {i + 1} draws a card. They now have {len(hand)} cards")
                    pickAndPlay = False
                else:
                    print(f"Deck is empty, Player {i + 1}. Game over (for now)")
                    break

        # CHECKS AFTER EACH TURN TO SEE IF THE CURRENT PLAYER IS OUT OF CARDS. IF SO, THE GAME ENDS AND THEY WIN
        if len(hand) < 1:
            print(f"Player {i + 1} is out of cards! They win!")
            playOn = False
            break
