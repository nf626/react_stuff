from app import db
from app.models.basemodel import BaseModel
from app.models.place import Place
from app.models.user import User
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Review(BaseModel):
    __tablename__ = 'reviews'

    _text = db.Column("text", db.String(100), nullable=False)
    _rating = db.Column("rating", db.Integer, nullable=False)
    _place_id = db.Column("place_id", db.String(36), ForeignKey('places.id'), nullable=False)
    _user_id = db.Column("user_id", db.String(36), ForeignKey('users.id'), nullable=False)
    places_r = relationship("Place", back_populates="reviews_r")
    user_r = relationship("User", back_populates="reviews_r")

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @hybrid_property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value:
            self._text = value
        else:
            raise ValueError("Text required")

    @hybrid_property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if isinstance(value, int) and value in range(1, 6):
           self._rating = value
        else:
            raise ValueError("Ratings must be between 1 and 5") 

    @hybrid_property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        from app.services.__init_ import facade

        place_exists = facade.get_place(value)
        if place_exists:
            self._place_id = value
        else:
            raise ValueError("Place does not exist!")
        
    @hybrid_property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        from app.services.__init_ import facade

        user_exists = facade.get_user(value)
        if user_exists:
            self._user_id = value
        else:
            raise ValueError("Owner does not exist!")
   
    def to_dict(self):
        """Converty to dictionary method"""
        return {
            'text': self.text,
            'rating' : self.rating,
            'place_id' : self.place_id,
            'user' : self.user
        }
