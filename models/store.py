from db import db
from typing import Dict, List
 
class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    """
      When we use lazy=dynamic : self.items is no longer a list of items 
      It is now an object then we must use self.items.all() method
    """
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name: str):
        self.name = name

    def json(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name, 
            'items': [item.json() for item in self.items.all()]
            }

    @classmethod
    def find_by_name(cls, name: str) -> Dict:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
