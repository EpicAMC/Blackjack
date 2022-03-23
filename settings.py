class Settings:
    def __init__(self):
        # Screen
        self.screen_width = 1400
        self.screen_height = 900
        self.bg_color = (50, 100, 50)

        # Game Settings
        self.blackjack_payout = 1.5
        self.deck_amount = 6
        self.starting_amount = 1000

        # Stats
        self.game_active = False
        self.round_active = False
        self.initial_play = True
