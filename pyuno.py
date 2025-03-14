import random
import os
import time
from colorama import init, Fore, Back, Style

colors = ['RED', 'BLU', 'YEL', 'GRN']
players = [0, 1]
play_stack = []

def create_deck():
    deck = []
    for color in colors:
        for i in range(0, 10):
            deck.append(color + str(i))
    return deck

def shuffle(cards):
    random.shuffle(cards)
    return cards

def deal_cards(deck, players):
    hands = {}
    for player in players:
        hands[player] = []
    for i in range(0, 7):
        for player in players:
            hands[player].append(deck.pop())
    return hands

def next_player(player):
    return (player + 1) % len(players)

def play_card(player, card, play_stack, deck, hands):
    if card in hands[player]:
        selectedCardColor = card[:3]
        selectedCardNumber = card[3:]

        topCard = play_stack[-1]
        topCardColor = topCard[:3]
        topCardNumber = topCard[3:]

        if selectedCardColor != topCardColor and selectedCardNumber != topCardNumber:
            return False

        play_stack.append(card)
        hands[player].remove(card)
        deck.append(play_stack[0])
        play_stack.pop(0)
        random.shuffle(deck)
        # time.sleep(1)
        return True
    else:
        return False
    
def draw_card(player, deck, hands):
    card = random.choice(deck)
    deck.remove(card)
    hands[player].append(card)
    return True

if __name__ == '__main__':
    init()
    deck = create_deck()
    deck = shuffle(deck)
    hands = deal_cards(deck, players)

    # Add a random card from the deck to the play stack
    start_card = random.choice(deck)
    play_stack.append(start_card)
    deck.remove(start_card)

    player = players[0]
    drawFlag = False
    while True:
        # time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Current player: ", player)
        print()
        print("Top of the Play Stack: ", play_stack[-1])
        print()
        for card in hands[player]:
            color = card[:3]
            number = " " + card[3:] + " "
            if color == 'RED':
                print(Back.RED + Fore.WHITE + number + Style.RESET_ALL)
            elif color == 'BLU':
                print(Back.BLUE + Fore.WHITE + number + Style.RESET_ALL)
            elif color == 'YEL':
                print(Back.YELLOW + Fore.WHITE + number + Style.RESET_ALL)
            elif color == 'GRN':
                print(Back.GREEN + Fore.WHITE + number + Style.RESET_ALL)
        print()
        choice = input("Enter the card you want to play (enter DRAW to draw a card, and enter PASS to skip turn): ")
        choice = choice.upper()
        if choice == "DRAW":
            if draw_card(player, deck, hands):
                drawFlag = True
                continue
            else:
                print("Deck is empty.")
        
        if choice == "PASS":
            if drawFlag:
                player = next_player(player)
                drawFlag = False
                continue
            else:
                print("You must draw a card first!")
                time.sleep(1)
                continue

        if play_card(player, choice, play_stack, deck, hands):
            drawFlag = False
            if len(hands[player]) == 0:
                print("Player ", player, " wins!")
                break
            player = next_player(player)
        else:
            print("Invalid card. Try again.")
            time.sleep(1)

        # break
