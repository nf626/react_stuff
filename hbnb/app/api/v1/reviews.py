from flask_restx import Namespace, Resource, fields
from app.services.__init_ import facade
from app.models.review import Review
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(required=True, description='ID of the user')
    
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        # Placeholder for the logic to register a new review
        review_data = api.payload

        user = facade.get_user(review_data.get('user_id'))
        if not user:
            return { 'error': "Invalid input data - user does not exist" }, 400
        print(f"User: {user}, Type: {type(user)}")

        place = facade.get_place(review_data.get('place_id'))
        if not place:
            return { 'error': "Invalid input data - place does not exist" }, 400
        print(f"Place: {place}, Type: {type(place)}")
        print(f"Place.owner: {place.owner}, Type: {type(place.owner)}")

        if place.owner == user.id:
            return { 'error': "Invalid input data - review writer is place owner" }, 400
    
        new_review = facade.create_review(review_data)
        if not new_review:
            return {'error': 'Invalid input data'}, 400
        else:
            return {
                'id': str(new_review.id),
                'text': new_review.text,
                'rating': new_review.rating,
                'user': user.id,
                'place': place.id
                }, 201

        # # Check User Class
        # owner_id = facade.get_user(review_data['user_id'])
        # if not owner_id:
        #     return {'error': 'Not Owner'}, 404

        # # user authenticate
        # current_user = get_jwt_identity()
        # if owner_id.id != current_user['id']:
        #     return {'error': 'Unauthorized User'}, 401

        # # Check Place Class
        # new_place = facade.get_place(review_data['place_id'])
        # if not new_place:
        #     return {'error': 'Not Place'}, 404

        # # Owner cannot review own place
        # if owner_id == new_place.owner:
        #     return {'error': 'You cannot review your own place'}, 400

        # # Pass directly to Review Class
        # review_dict = {
        #     'text': review_data['text'],
        #     'rating': review_data['rating'],
        #     'user': owner_id.id,
        #     'place_id': new_place.id
        # }
            
        # # Add new review
        # add_review = facade.create_review(review_dict)
        
        # # Check user has not already reviewed this place
        # if add_review.user == owner_id.id:
        #     return {'error': 'You have already reviewed this place.'}, 400

        # if add_review:
        #     return {
        #         'id': str(add_review.id),
        #         'text': add_review.text,
        #         'rating': add_review.rating,
        #         'user': owner_id.id,
        #         'place': new_place.id
        #         }, 201
        # else:
        #     return {'error': 'Invalid input data'}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        all_reviews = facade.get_all_reviews()
        list_all_reviews = []
        for review in all_reviews:
            list_all_reviews.append({
                'id': str(review.id),
                'text': review.text,
                'rating' : review.rating
            })
        return list_all_reviews, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        review = facade.get_review(review_id)

        if review:
            return {
                'id': str(review.id),
                'text': review.text,
                'rating': review.rating,
                'user_id': str(review.user_id),
                'place_id': str(review.place_id)
            }, 200
        else:
            return {'Error': 'Review not found'}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        review_exist = facade.get_review(review_id)
        
        new_review = {
            'text' : review_data['text'],
            'rating': review_data['rating']
        }

        # user authenticate
        current_user = get_jwt_identity()
        
        if review_exist.user_id != current_user['id']:
            return {'Error': 'Unauthorized action'}, 403

        if review_exist:
            facade.update_review(review_id, new_review)
            return {"message": "Review updated successfully"}, 200
        return {'Error': 'Review not found'}, 404


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        review_exist = facade.get_review(review_id)
        
        # print(review_exist.user_id)
        # print(review_id)
        
        if not review_exist:
            return {'Error': 'Review not found'}, 404
       
        current_user = get_jwt_identity()
       
        # print(current_user['id'])
        if review_exist.user_id != current_user['id']:
            return {'Error': 'Unauthorized action'}, 403
        else:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        
# @api.route('/places/<place_id>/reviews')
# class PlaceReviewList(Resource):
#     @api.response(200, 'List of reviews for the place retrieved successfully')
#     @api.response(404, 'Place not found')
#     def get(self, place_id):
#         """Get all reviews for a specific place"""
#         reviews = facade.get_all_reviews()
#         place = facade.get_place(place_id)
#         place_reviews = []
#         for review in reviews:
#             if review.place_id == place:
#                 place_reviews.append({
#                     'id': str(review.id),
#                     'text': review.text,
#                     'rating': review.rating
#                 })
#         return place_reviews, 200

        ### CURL COMMMANDS TO TEST HHTP REQUESTS ###
#  Register new Review:
#  curl -X POST http://127.0.0.1:5000/api/v1/reviews/ -d '{"text": "Great place to stay!", "rating": 5, "user_id": "<user_id>", "place_id": "<place_id>"}' -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json"

#  Retrieve All Reviews:
#  curl -X GET "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json"

#  Retrieve a Review’s Details:
#  curl -X GET "http://127.0.0.1:5000/api/v1/reviews/<review_id>" -H "Content-Type: application/json"

#  Update a Review’s Information:
#  curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/<review_id>" -d '{"text": "Amazing stay!", "rating": 4}' -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json"

#  Delete a Review:
#  curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/<review_id>" -H "Content-Type: application/json" -H "Authorization: Bearer <your_token>"

#  Retrieve All Reviews for a Specific Place:
#  curl -X GET "http://127.0.0.1:5000/api/v1/places/<place_id>/reviews" -H "Content-Type: application/json"
