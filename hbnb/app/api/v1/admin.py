from flask_restx import Namespace, Resource, fields
from app.services.__init_ import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request

api = Namespace('admin', description='Admin operations')

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
            }, 201
    
    @api.route('/users/<user_id>')
    class AdminUserResource(Resource):
        @jwt_required()
        def put(self, user_id):

            current_user = get_jwt_identity()
            
            # If 'is_admin' is part of the identity payload
            if not current_user.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403

            data = request.json
            email = data.get('email')

            if email:
                # Check if email is already in use
                existing_user = facade.get_user_by_email(email)
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email is already in use'}, 400
                
            user_exists = facade.get_user(user_id)
            
            if user_exists:
                updated_data = facade.update_user(user_id, data)
                return {
                    'message': 'User updated successfully',
                    'id': str(updated_data.id),
                    'first_name': updated_data.first_name,
                    'last_name': updated_data.last_name,
                    'email': updated_data.email,
                    'password': updated_data.password
                    }, 200
            else:
                return {'error': 'User does not exist'}, 400
            
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload

        # Check if amenity exists
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            return {'error': 'Amenity already registered'}, 400

        new_amenity = facade.create_amenity(amenity_data)

        if new_amenity:
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201
        else:
            return {'error': 'Invalid input data'}, 400
        

@api.route('/amenities/<amenity_id>/')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        # update an amenity by ID
        amenity_data = api.payload
        amenity_exists = facade.get_amenity(amenity_id)

        # Check if key names are correct
        key_list = ['name']
        if not all(name in key_list for name in amenity_data):
            return {'error': 'Invalid input data'}, 400

        if amenity_exists:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'message': 'Amenity updated successfully',
                'id': str(updated_amenity.id),
                'name': updated_amenity.name
                }, 200
        else:
            return {'error': 'Amenity not found'}, 404
        
@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload

        # Check if key names are correct
        key_list = ['title', 'description', 'price']
        if not all(name in key_list for name in place_data):
            return {'error': 'Invalid input data'}, 400

        if place:
            updated_place = facade.update_place(place_id, place_data)
            return {
                "message": "Place updated successfully",
                'id': str(updated_place.id),
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price
                }, 200
        else:
            return {'error': 'Place not found'}, 404
        
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""

        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        
        if not is_admin and place.owner != user_id:
            return {'error': 'Unauthorized action'}, 403

        if place:
            facade.delete_place(place_id)

            return {"message": "place deleted successfully"}, 200
        return {'Error': 'place not found'}, 404
    
@api.route('/reviews/<review_id>')
class AdminModifyReview(Resource):
    @jwt_required()
    def put(self, review_id):

        review_data = api.payload

        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        review_exist = facade.get_review(review_id)

        new_review = {
            'text' : review_data['text'],
            'rating': review_data['rating']
        }

        # user authenticate
        current_user = get_jwt_identity()

        if review_exist:
            facade.update_review(review_id, new_review)
            return {"message": "Review updated successfully"}, 200
        return {'Error': 'Review not found'}, 404



    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        review_exist = facade.get_review(review_id)
        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # user authenticate
        current_user = get_jwt_identity()
        if review_exist.user.id != current_user['id']:
            return {'Error': 'Unauthorized action'}, 403

        if review_exist:
            facade.delete_review(review_id)

            return {"message": "Review deleted successfully"}, 200
        return {'Error': 'Review not found'}, 404
    


