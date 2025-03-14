import random
import curses

colors = ['RED', 'BLU', 'YEL', 'GRN']
players = [0, 1]
play_stack = []

def create_deck():
    deck = [color + str(i) for color in colors for i in range(10)]
    random.shuffle(deck)
    return deck

def deal_cards(deck, players):
    hands = {player: [deck.pop() for _ in range(7)] for player in players}
    return hands

def next_player(player):
    return (player + 1) % len(players)

def play_card(player, selected_index, play_stack, deck, hands):
    if selected_index >= len(hands[player]):
        return False  # Ignore if trying to select Draw, Pass, or Quit
    
    card = hands[player][selected_index]
    top_card = play_stack[-1]
    
    if card[:3] != top_card[:3] and card[3:] != top_card[3:]:
        return False  # Invalid move

    play_stack.append(card)
    hands[player].pop(selected_index)
    deck.append(play_stack.pop(0))
    random.shuffle(deck)
    return True

def draw_card(player, deck, hands):
    if deck:
        hands[player].append(deck.pop())
        return True
    return False

def get_color_pair(color):
    mapping = {"RED": 1, "BLU": 2, "YEL": 3, "GRN": 4}
    return curses.color_pair(mapping.get(color, 0))

def game_loop(stdscr):
    curses.curs_set(0)
    stdscr.keypad(1)
    curses.start_color()
    
    for i, color in enumerate([curses.COLOR_RED, curses.COLOR_BLUE, curses.COLOR_YELLOW, curses.COLOR_GREEN], start=1):
        curses.init_pair(i, color, curses.COLOR_BLACK)
    
    deck = create_deck()
    hands = deal_cards(deck, players)
    play_stack.append(deck.pop())
    
    player, drawFlag, selected_index = 0, False, 0
    
    while True:
        stdscr.clear()
        stdscr.addstr(1, 0, f"Current player: {player}")
        stdscr.addstr(2, 0, "Top of Play Stack: ", curses.A_BOLD)
        stdscr.addstr(2, 18, f"[ {play_stack[-1][3:]} ]", get_color_pair(play_stack[-1][:3]))
        
        stdscr.addstr(4, 0, "Your cards:")
        total_options = len(hands[player]) + 3  # Cards + Draw + Pass + Quit buttons
        
        for idx, card in enumerate(hands[player]):
            color = get_color_pair(card[:3])
            text = f"[ {card[3:]} ]"
            attr = color | curses.A_REVERSE if idx == selected_index else color
            stdscr.addstr(5, idx * 6, text, attr)
        
        draw_attr = curses.A_REVERSE if selected_index == len(hands[player]) else curses.A_NORMAL
        pass_attr = curses.A_REVERSE if selected_index == len(hands[player]) + 1 else curses.A_NORMAL
        quit_attr = curses.A_REVERSE if selected_index == len(hands[player]) + 2 else curses.A_NORMAL
        
        stdscr.addstr(5, len(hands[player]) * 6 + 4, "[ Draw ]", draw_attr)
        stdscr.addstr(5, len(hands[player]) * 6 + 12, "[ Pass ]", pass_attr)
        stdscr.addstr(5, len(hands[player]) * 6 + 20, "[ Quit ]", quit_attr)
        stdscr.addstr(7, 0, "Use ← → to select, Enter to confirm.")
        
        key = stdscr.getch()
        
        if key == curses.KEY_LEFT and selected_index > 0:
            selected_index -= 1
        elif key == curses.KEY_RIGHT and selected_index < total_options - 1:
            selected_index += 1
        elif key == 10:  # Enter key
            if selected_index == len(hands[player]):  # Draw button
                if draw_card(player, deck, hands):
                    drawFlag, selected_index = True, len(hands[player]) - 1
            elif selected_index == len(hands[player]) + 1:  # Pass button
                if drawFlag:
                    player, drawFlag, selected_index = next_player(player), False, 0
                else:
                    stdscr.addstr(9, 0, "You must draw a card first!", curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(1000)
            elif selected_index == len(hands[player]) + 2:  # Quit button
                return  # Exit game loop
            elif play_card(player, selected_index, play_stack, deck, hands):
                drawFlag, selected_index = False, 0
                if not hands[player]:
                    stdscr.clear()
                    stdscr.addstr(10, 0, f"Player {player} wins!", curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(2000)
                    break
                player = next_player(player)
            else:
                stdscr.addstr(9, 0, "Invalid move!", curses.A_BOLD)
                stdscr.refresh()
                curses.napms(1000)

if __name__ == "__main__":
    curses.wrapper(game_loop)
