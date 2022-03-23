import pygame
import sys
import math
import random
import assets
from card import Cards


def check_events(settings, game_state, active_button_list):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            return check_buttons(settings, game_state, active_button_list, mouse_x, mouse_y)


def update_screen(settings, screen, cards, game_state, active_button_list):
    screen.fill(settings.bg_color)

    show_hands(settings, screen, cards, game_state)

    define_button_position(settings, active_button_list)
    show_buttons(active_button_list)

    pygame.display.flip()


def decide_active_buttons(settings, game_state, button_list, active_button_list):
    # play_button:0, keep_playing_button:1, quit_button:2, hit_button:3, stand_button:4, double_down_button:5
    # split_button:6, insurance_button:7, even_money_button:8, surrender_button:9
    del active_button_list[:]

    if settings.initial_play and not settings.game_active:
        active_button_list.append(button_list[0])

    if not settings.initial_play and not settings.game_active:
        active_button_list.append(button_list[1])
        active_button_list.append(button_list[2])

    if settings.round_active:
        active_button_list.append(button_list[3])
        active_button_list.append(button_list[4])

        if len(game_state.player_list) == 2:
            active_button_list.append(button_list[5])

            if game_state.player_list[0][0] == game_state.player_list[1][0] and not game_state.split:
                active_button_list.append(button_list[6])

        if game_state.insurance == 0 and game_state.dealer_list[0][0] == "A":
            active_button_list.append(button_list[7])

        if len(game_state.player_list) == 2 and check_total(game_state.player_list) == 21:
            active_button_list.append(button_list[8])

        active_button_list.append(button_list[9])


def define_button_position(settings, active_button_list):
    count = 1
    length = len(active_button_list)
    screen_width = settings.screen_width
    increment = math.floor(screen_width/(length + 1))

    for button in active_button_list:
        if button.button_id == "play_button" or button.button_id == "keep_playing_button":
            button.rect.center = button.screen_rect.center

        elif button.button_id == "quit_button":
            button.rect.right = button.screen_rect.right - 10
            button.rect.top = button.screen_rect.top + 10

        else:
            button.rect.bottom = button.screen_rect.bottom - 75
            button.rect.centerx = increment * count
            count += 1


def show_buttons(active_button_list):
    for button in active_button_list:
        button.prep_msg()
        button.draw_button()


def check_buttons(settings, game_state, active_button_list, mouse_x, mouse_y):
    for button in active_button_list:
        button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked == 1:
            if button.button_id == "play_button" and not settings.game_active:
                settings.game_active = True
                settings.initial_play = False

            elif button.button_id == "keep_playing_button" and not settings.game_active:
                settings.game_active = True

            elif button.button_id == "quit_button" and settings.game_active:
                sys.exit()

            elif button.button_id == "hit_button" and settings.game_active:
                game_state.hit_player()
                game_state.player_total = check_total(game_state.player_list)
                if game_state.player_total == -1:
                    game_state.player_result = game_state.player_total
                    settings.round_active = False
                    return

            elif button.button_id == "stand_button" and settings.game_active:
                game_state.player_total = check_total(game_state.player_list)
                game_state.player_result = game_state.player_total
                settings.round_active = False
                return

            elif button.button_id == "double_down_button" and settings.game_active:
                if len(game_state.player_list) == 2:
                    game_state.bet *= 2
                    game_state.hit_player()
                    game_state.player_total = check_total(game_state.player_list)
                    game_state.player_result = game_state.player_total
                    settings.round_active = False
                    return

            elif button.button_id == "split_button" and settings.game_active:
                if len(game_state.player_list) == 2 and game_state.player_list[0][0] == game_state.player_list[1][0] and not game_state.split:
                    pass

            elif button.button_id == "insurance_button" and settings.game_active:
                if game_state.dealer_list[0][0] == "A" and game_state.insurance == 0:
                    game_state.insurance = int(input("How much insurance? (Maximum is 1/2 of bet): "))
                    game_state.insurance = check_insurance(game_state.insurance, game_state.bet)
                    print("You paid " + str(game_state.insurance) +
                          ". If the dealer gets a blackjack, you will be paid double of your insurance")
                elif game_state.dealer_list[0][0] == "A" and not game_state.insurance == 0:
                    print("You have already paid an insurance of " + str(game_state.insurance) + "!")
                else:
                    print("Invalid Action\n")

            elif button.button_id == "even_money_button" and settings.game_active:
                if game_state.player_total == 21 and len(game_state.player_list) == 2:
                    game_state.player_result = "Even Money"
                    return

            elif button.button_id == "surrender_button" and settings.game_active:
                game_state.player_result = "Surrendered"
                return


def create_card(settings, screen, cards, card_id, x, y):
    card = Cards(settings, screen, card_id)
    card.rect.centerx = x
    card.rect.centery = y
    cards.add(card)


def show_hands(settings, screen, cards, game_state):
    cards.empty()

    screen_width = settings.screen_width
    screen_height = settings.screen_height

    player_length = len(game_state.player_list)
    player_count = 1
    player_increment = math.floor(screen_width / (player_length + 1))
    player_y = math.floor(screen_height * 5/8)
    dealer_length = len(game_state.dealer_list)
    dealer_count = 1
    dealer_increment = math.floor(screen_width / (dealer_length + 1))
    dealer_y = math.floor(screen_height * 1/4)

    if settings.round_active:
        for card in game_state.player_list:
            create_card(settings, screen, cards, card, player_increment * player_count, player_y)
            player_count += 1

        create_card(settings, screen, cards, game_state.dealer_list[0], screen_width / 2, dealer_y)

    else:
        for card in game_state.player_list:
            create_card(settings, screen, cards, card, player_increment * player_count, player_y)
            player_count += 1

        for card in game_state.dealer_list:
            create_card(settings, screen, cards, card, dealer_increment * dealer_count, dealer_y)
            dealer_count += 1

    cards.draw(screen)


def start_round(settings, screen, cards, game_state, button_list, active_button_list):
    settings.round_active = True

    game_state.reset_game_state()

    game_state.hit_dealer()
    game_state.hit_player()
    game_state.hit_dealer()
    game_state.hit_player()

    while settings.round_active:
        decide_active_buttons(settings, game_state, button_list, active_button_list)
        update_screen(settings, screen, cards, game_state, active_button_list)
        check_events(settings, game_state, active_button_list)
        if game_state.player_result:
            settings.round_active = False

    if game_state.player_result == -1:
        print("You busted. You lose your bet to the house.")
        game_state.dealer_list = game_state.dealer_list.pop(0)

    elif game_state.player_result == "Surrendered":
        print("You surrendered. You lose half of your bet to the house.")

    elif game_state.player_result == "Even Money":
        print("You took even money for your blackjack. The house pays you 1/1 of your bet")

    elif game_state.player_result == 21 and len(game_state.player_list) == 2 and not game_state.dealer_list[0][0] == "A":
        print("You got a blackjack! The house pays you 3/2 of your bet.")

    else:
        game_state.dealer_round()
        if game_state.player_result == game_state.dealer_result:
            print("You tied with the house. Nothing happens.")

        elif game_state.player_result > game_state.dealer_result:
            print("You beat the house! The house pays you your bet.")

        else:
            print("The house beat your hand. You lose your bet to the house.")

        print("House's hand:")
        print(game_state.dealer_list)
        print("Score: " + str(check_total(game_state.dealer_list)))
        print("Your hand:")
        print(game_state.player_list)
        print("Score: " + str(check_total(game_state.player_list)))

    settings.game_active = False


# Blackjack Functionality
def shuffle_deck(deck_amount):
    # Return a shuffled deck with the specified amount of decks
    count = 0
    deck = []
    one_deck = ["A.1", "A.2", "A.3", "A.4", "2.1", "2.2", "2.3", "2.4", "3.1", "3.2", "3.3", "3.4", "4.1", "4.2", "4.3",
                "4.4", "5.1", "5.2", "5.3", "5.4", "6.1", "6.2", "6.3", "6.4", "7.1", "7.2", "7.3", "7.4", "8.1", "8.2",
                "8.3", "8.4", "9.1", "9.2", "9.3", "9.4", "T.1", "T.2", "T.3", "T.4", "J.1", "J.2", "J.3", "J.4",
                "Q.1", "Q.2", "Q.3", "Q.4", "K.1", "K.2", "K.3", "K.4"]

    # Get the necessary amount of decks
    while count < deck_amount:
        deck += one_deck
        count += 1

    # Shuffle the deck
    random.shuffle(deck)

    return deck


def hit(deck, hand, deck_amount):
    # If the deck is empty, shuffle another set
    if len(deck) == 0:
        deck = shuffle_deck(deck_amount)
    # Pop the first element of the deck into the hand
    hand.append(deck.pop(0))


def check_total(hand):
    # Check all the possible totals of hand and return the highest possible total or a bust
    aces = 0
    no_ace_hand = hand.copy()
    total = 0

    # Check for Aces
    for card in hand:
        if card[0] == "A":
            aces += 1
            no_ace_hand.remove(card)

    # Take the total without Aces
    for card in no_ace_hand:
        total += assets.card_values[card]

    # Factor in the Aces into the total
    while aces > 1:
        total += 1
        aces -= 1

    if aces == 1:
        if total <= 10:
            total += 11
        else:
            total += 1

    # Final return statements. If it is a bust, the function returns -1. Otherwise, it returns the total
    if total > 21:
        return -1

    else:
        return total


def check_insurance(insurance, bet):
    if insurance > bet / 2 or insurance < 0:
        print("Invalid Insurance")
        return check_insurance(insurance, bet)

    else:
        return insurance
