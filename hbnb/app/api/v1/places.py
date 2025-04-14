from flask_restx import Namespace, Resource, fields
from app.services.__init_ import facade
from app.models.place import Place
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db


api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        # Placeholder for the logic to register a new place
        place_data = api.payload

        # Check if place exists
        existing_latitude = facade.get_place_by_latitude(place_data['latitude'])
        existing_longitude = facade.get_place_by_longitude(place_data['longitude'])
        if existing_latitude and existing_longitude:
            return {'error': 'Place already registered'}, 400

        # Check if key names are correct
        key_list = ['id', 'title', 'description', 'price',
                    'latitude', 'longitude', 'owner']
        if not all(name in key_list for name in place_data):
            return {'error': 'Invalid input data'}, 400

        owner_id = facade.get_user(place_data['owner'])
        # print(type(check_owner))
        # print(check_owner.id)
        if not owner_id:
            return {'error': 'Not Owner'}, 404

        # Pass directly to Place Class
        new_place = Place(
                title=place_data['title'],
                description=place_data.get('description'),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner=owner_id.id
            )
        # Convert to dictionary
        place_dict = new_place.to_dict()

        # user authenticate
        current_user = get_jwt_identity()
        if owner_id.id != current_user['id']:
            return {'error': 'Unauthorized User'}, 401

        # Add new place
        add_place = facade.create_place(place_dict)

        if add_place:
            return {
                'id': add_place.id,
                'title': add_place.title,
                'description': add_place.description,
                'price': add_place.price,
                'latitude': add_place.latitude,
                'longitude': add_place.longitude,
                'owner': owner_id.id
            }, 201
        else:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        all_places = facade.get_all_places()
        list_all_places = []
        for place in all_places:
            list_all_places.append({
                'id': str(place.id),
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude,
            })
        return list_all_places, 200

@api.route('/<place_id>')        
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Placeholder for the logic to retrieve a place by ID, including associated owner and amenities
        place = facade.get_place(place_id)
        user = facade.get_user(place.owner)

        if not place:
            return {'error': 'Place not found'}, 404

        # get amenities related to the place
        amenities = place.amenities_r

        if not amenities:
            return {'error': 'Amenities not found'}, 200
        
        for amenity in amenities:
            print(f"Amenity ID: {amenity.id}, Amenity Name: {amenity.name}")

        amenities_list = [{'id': str(amenity.id), 'name': amenity.name} for amenity in amenities]

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': str(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            },
            'amenities': amenities_list
        }, 200

    @api.route('/<place_id>/reviews')
    class PlaceResource(Resource):
        @api.response(200, 'List of reviews for the place retrieved successfully')
        @api.response(404, 'Place not found')
        def get(self, place_id):
            """Get all reviews for a specific place"""
            reviews = facade.get_all_reviews()
            place = facade.get_place(place_id)

            if not place:
                return {'error': 'Place not found'}, 404
            
            place_reviews = []
            for review in reviews:
                
                if review.place_id == place.id:
                    place_reviews.append({
                        'id': str(review.id),
                        'text': review.text,
                        'rating': review.rating
                    })
            return place_reviews, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        place_data = api.payload
        place_exists = facade.get_place(place_id)


        # Check if key names are correct
        # key_list = ['title', 'description', 'price']
        # if not all(name in key_list for name in place_data):
        #     return {'error': 'Invalid input data'}, 400

        # user authenticate
        current_user = get_jwt_identity()

        if place_exists.owner != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        if place_exists:
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

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt_identity()

        place = facade.get_place(place_id)
        
        if place.owner != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        if place:
            facade.delete_place(place_id)

            return {"message": "place deleted successfully"}, 200
        return {'Error': 'place not found'}, 404


    # Many to Many Relationship
    @api.route('/<place_id>/amenities')
    class PlaceAmenityResource(Resource):
        @api.response(200, 'List of amenities for the place retrieved successfully')
        @api.response(404, 'Place not found')
        def get(self, place_id):
            """Get all amenities for a specific place"""
            place = facade.get_place(place_id)

            if not place:
                return {'error': 'Place not found'}, 404
            
             # get amenities related to the place
            amenities = place.amenities_r

            if not amenities:
                return {'error': 'Amenities not found'}, 200
            
            for amenity in amenities:
                print(f"Amenity ID: {amenity.id}, Amenity Name: {amenity.name}")

            amenities_list = [{'id': str(amenity.id), 'name': amenity.name} for amenity in amenities]

            return {'amenities': amenities_list}, 200
        
        @api.expect(amenity_model)
        @api.response(201, 'Amenity successfully added to the place')
        @api.response(404, 'Place not found')
        def post(self, place_id):
            """Add an amenity to a place"""
            place = facade.get_place(place_id)

            if not place:
                return {'error': 'Place not found'}, 404
            
            amenity_data = api.payload
            amenity = facade.get_amenity_by_name(amenity_data['name'])

            if not amenity:
                return {'error': 'Amenity not found'}, 404
            
            # Add the amenity to the place
            place.amenities_r.append(amenity)

            # Commit the changes to the database
            db.session.commit()
            print(place.amenities_r)

            return {"message": f"Amenity {amenity.name} added to {place.title} successfully"}, 201

        ### CURL COMMMANDS TO TEST HHTP REQUESTS ###
#  Register a New Place
#  curl -X POST http://127.0.0.1:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title": "Cozy", "description": "nice", "price": 100.0, "latitude": 37.7749, "longitude": -122.4194, "owner": "<user_id>"}' -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json"

#  Retrieve All Places
#  curl -X GET http://127.0.0.1:5000/api/v1/places/ -H "Content-Type: application/json"

#  Retrieve Place Details
#  curl -X GET http://127.0.0.1:5000/api/v1/places/<place_id> -H "Content-Type: application/json"

#  Update a Place’s Information
#  curl -X PUT http://127.0.0.1:5000/api/v1/places/<place_id> -H "Content-Type: application/json" -d '{"title": "Luxury Condo", "description": "An upscale place to stay", "price": 200.0}' -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json"

#  Retrieve All Reviews for a Specific Place:
#  curl -X GET "http://127.0.0.1:5000/api/v1/places/<place_id>/reviews" -H "Content-Type: application/json"

#  Delete a Place:
#  curl -X DELETE "http://127.0.0.1:5000/api/v1/places/<place_id>" -H "Content-Type: application/json" -H "Authorization: Bearer <your_token>"
