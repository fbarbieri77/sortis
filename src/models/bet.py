__author__ = "Fabio Barbieri"

import datetime
import uuid

from src.common.database import Database
from src.models.security import Security


class Bet(object):
    
    def __init__(self, user_id, security_id, acquisition_date=None, _id=None):
        self.user_id = user_id
        self.security_id = security_id
        self.acquisition_date = datetime.datetime.utcnow() if acquisition_date is None else acquisition_date
        self._id = uuid.uuid4().hex if _id is None else _id
   
    def json(self):
        return {
            '_id': self._id,
            'user_id': self.user_id,
            'security_id': self.security_id,
            'acquisition_date': self.acquisition_date
        }

    def save_to_mongo(self):
        Database.insert(collection='bets', 
                        data=self.json())

    @classmethod
    def bets_by_user(cls, user_id):
        bets = [cls(**bet) for bet in Database.find(collection='bets', query={'user_id': user_id})]
        return [Security.from_mongo(bet.security_id) for bet in bets]

    """
    @classmethod
    def find_security(cls, id):
        post_data = Database.find_one(collection='bets', query={'_id': id}) 
        return cls(**post_data) # same as cls(field = post_data['field'], ...)
    """
    
