import game_functions as gf


class GameState:
    def __init__(self, settings):
        self.settings = settings

        self.player_list = []
        self.player_total = None
        self.player_result = None
        self.dealer_list = []
        self.dealer_total = None
        self.dealer_result = None
        self.split = False
        self.insurance = 0
        self.bet = 10
        self.shoe = None

    def hit_player(self):
        gf.hit(self.shoe, self.player_list, self.settings.deck_amount)

    def hit_dealer(self):
        gf.hit(self.shoe, self.dealer_list, self.settings.deck_amount)

    def dealer_round(self):
        self.dealer_total = gf.check_total(self.dealer_list)

        while self.dealer_total <= 16:
            if self.dealer_total == -1:
                break
            else:
                self.hit_dealer()
                self.dealer_total = gf.check_total(self.dealer_list)

        self.dealer_result = self.dealer_total

    def reset_game_state(self):
        self.player_list = []
        self.player_total = None
        self.player_result = None
        self.dealer_list = []
        self.dealer_total = None
        self.dealer_result = None
        self.split = False
        self.insurance = 0
        self.bet = 10