__author__ = "Fabio Barbieri"

from src.models.bet import Bet
from src.models.security import Security

class Dashboard(object):
    def __init__(self, user_id):
        self.user_id = user_id


    def new_bet(self, security_id):
        bet = Bet(self.user_id, security_id)
        bet.save_to_mongo()

    def get_bets(self):
        return Bet.bets_by_user(self.user_id)

    def withdraw_bet(self):
        pass

    def check_prizes(self):
        pass