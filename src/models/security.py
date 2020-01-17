__author__ = "Fabio Barbieri"

import datetime
import uuid

from src.common.database import Database


class Security(object):
    
    def __init__(self, author, value, prizes, is_winner=False, date=None, _id=None):
        self.author = author
        self.value = value
        self.prizes = prizes
        self.is_winner = is_winner
        self._id = uuid.uuid4().hex if _id is None else _id
        self.date = datetime.datetime.utcnow()
   
    def json(self):
        return {
            '_id': self._id,
            'author': self.author,
            'value': self.value,
            'prizes': self.prizes,
            'is_winner': self.is_winner,
            'date':self.date
        }

    def save_to_mongo(self):
        Database.insert(collection='securities', 
                        data=self.json())

    @classmethod
    def from_mongo(cls, security_id):
        asset = Database.find_one(collection='securities', 
                                query={'_id': security_id}) 
        return cls(**asset)

    def update_mongo(self):
        Database.update(collection='securities',
                        key={'_id': self._id}, 
                        data=self.json())

    @staticmethod
    def get_all():
        assets = Database.find(collection='securities')
        basket = []
        for asset in assets:
            basket.append(asset)
        return basket



