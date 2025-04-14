import re
# from app.models.basemodel import BaseModel
from app import db, bcrypt
from .basemodel import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = 'users'

    _first_name = db.Column("first_name", db.String(50), nullable=False)
    _last_name = db.Column("last_name", db.String(50), nullable=False)
    _email = db.Column("email", db.String(120), nullable=False, unique=True)
    _password = db.Column("password", db.String(128), nullable=False)
    _is_admin = db.Column("is_admin", db.Boolean, default=False)
    places_r = relationship("Place", back_populates="owner_r", cascade="all, delete")
    reviews_r = relationship("Review", back_populates="user_r", cascade="all, delete")
    
    # places = db.Column(db.String(128), nullable=True, unique=True)
    # reviews = db.Column(db.String(128), nullable=True, unique=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = password # self.hash_password(password)
        # self.places = []
        # self.reviews = []

    @hybrid_property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if isinstance(value, str) and len(value) in range(51):
            self._first_name = value
        else:
            raise ValueError("First name must be a maximum of 50 characters")

    @hybrid_property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if isinstance(value, str) and len(value) in range(51):
            self._last_name = value
        else:
            raise ValueError("Last name must be a maximum of 50 characters")

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # Email not empty
        if not value:
            raise ValueError("Email is required")
        # check email format
        pattern = (r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9.!#$%&'*+/=?^_{|}~-]+"

                            r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")

        if not re.fullmatch(pattern, value):
            raise ValueError("Required, must be unique,"
                             "and should follow standard email format validation.")
        self._email = value


    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = bcrypt.generate_password_hash(value).decode('utf8')

    @hybrid_property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if isinstance(value, bool):
            self._is_admin = value
        else:
            raise ValueError("Must be boolean value")

    def add_place(self, place):
        """User adds a place to list"""
        self.places.append(place)

    def add_review(self, review):
        """User can add a review"""
        self.reviews.append(review)

    # def hash_password(self, password):
    #     """Hashes the password before storing it."""
    #     self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
