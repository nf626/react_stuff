from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.services.user_repository import UserRepository
from app.services.amenity_repository import AmenityRepository
from app.services.place_repository import PlaceRepository
from app.services.review_repository import ReviewRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

#---------- User Methods ------------# 
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)


#---------- Place Methods ------------#
    def create_place(self, place_data):
    # Create a place, including validation for price, latitude, and longitude
        place = Place(**place_data)
        # Round the price to two decimal places
        place.price = round(place.price, 2)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        return self.place_repo.update(place_id, place_data)

    def get_place_by_latitude(self, latitude):
        return self.place_repo.get_by_attribute('latitude', latitude)

    def get_place_by_longitude(self, longitude):
        return self.place_repo.get_by_attribute('longitude', longitude)
    
    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)


#---------- Amenity Methods ------------#
    def create_amenity(self, amenity_data):
    # Create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
    # Retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
    # Retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
    # Update an amenity
        return self.amenity_repo.update(amenity_id, amenity_data)

    def get_amenity_by_name(self, name):
    # Get amenity name attribute
        return self.amenity_repo.get_by_attribute('name', name)

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

#---------- Review Methods ------------#
    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        return self.review_repo.delete(review_id)
