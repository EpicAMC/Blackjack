from pygame.sprite import Group
import pygame
import game_functions as gf
from settings import Settings
from card import Cards
from button import Button
from game_state import GameState

pygame.init()


def run_game():
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Blackjack")

    settings = Settings()

    game_state = GameState(settings)
    game_state.shoe = gf.shuffle_deck(settings.deck_amount)

    button_list = []
    active_button_list = []
    play_button = Button(settings, screen, "play_button", "Play")
    keep_playing_button = Button(settings, screen, "keep_playing_button", "Keep Playing")
    quit_button = Button(settings, screen, "quit_button", "Quit")
    hit_button = Button(settings, screen, "hit_button", "Hit")
    stand_button = Button(settings, screen, "stand_button", "Stand")
    double_down_button = Button(settings, screen, "double_down_button", "Double Down")
    split_button = Button(settings, screen, "split_button", "Split")
    insurance_button = Button(settings, screen, "insurance_button", "Insurance")
    even_money_button = Button(settings, screen, "even_money_button", "Even Money")
    surrender_button = Button(settings, screen, "surrender_button", "Surrender")

    button_list.append(play_button)
    button_list.append(keep_playing_button)
    button_list.append(quit_button)
    button_list.append(hit_button)
    button_list.append(stand_button)
    button_list.append(double_down_button)
    button_list.append(split_button)
    button_list.append(insurance_button)
    button_list.append(even_money_button)
    button_list.append(surrender_button)

    cards = Group()

    gf.update_screen(settings, screen, cards, game_state, active_button_list)

    while True:
        gf.decide_active_buttons(settings, game_state, button_list, active_button_list)
        gf.update_screen(settings, screen, cards, game_state, active_button_list)
        gf.check_events(settings, game_state, active_button_list)
        if settings.game_active:
            gf.start_round(settings, screen, cards, game_state, button_list, active_button_list)


def get_bet():
    bet = input("What is your bet? \n --> ")
    try:
        if int(bet) < 0:
            print("Invalid Input. It must be a positive number")
            return get_bet()
        else:
            return int(bet)
    except ValueError:
        print("Invalid Input. It must be a positive number")
        return get_bet()


run_game()
