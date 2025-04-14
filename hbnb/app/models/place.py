from app.models.basemodel import BaseModel
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(60), ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(60), ForeignKey("amenities.id"), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    _title = db.Column("title", db.String(50), nullable=False)
    _description = db.Column("description", db.String(150), nullable=True)
    _price = db.Column("price", db.Float, nullable=False)
    _latitude = db.Column("latitude", db.Float, nullable=False, unique=True)
    _longitude = db.Column("longitude", db.Float, nullable=False, unique=True)
    _owner = db.Column("owner_id", db.String(36), ForeignKey('users.id'), nullable=False)
    owner_r = relationship("User", back_populates="places_r")
    reviews_r = relationship("Review", back_populates="places_r")
    amenities_r = relationship("Amenity", secondary=place_amenity, back_populates="places_r")

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        # self.reviews = []  # List to store related reviews
        # self.amenities = []  # List to store related amenities

    @hybrid_property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if len(value) in range(101):
            self._title = value
        else:
            raise ValueError("title must be a maximum of 100 characters")

    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @hybrid_property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if (isinstance(value, float) or isinstance(value, int)) and value > 0.0:
            self._price = value
        else:
            raise ValueError("Must be a positive value and float")

    @hybrid_property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if isinstance(value, float) and (-90.00 < value < 90.00):
            self._latitude = value
        else:
            raise ValueError("Must be within the range of -90.0 to 90.0 and float")

    @hybrid_property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if isinstance(value, float) and (-180.0 < value < 180.0):
            self._longitude = value
        else:
            raise ValueError("Must be within the range of -90.0 to 90.0 and float")

    @hybrid_property
    def owner(self):
        return self._owner

# User instance of who owns the place. This should be validated to ensure the owner exists.
    @owner.setter
    def owner(self, value):
        self._owner = value
        # else:
        #     raise ValueError("Owner must be validated")

    def to_dict(self):
        """Converty to dictionary method"""
        return {
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner
        }


    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
