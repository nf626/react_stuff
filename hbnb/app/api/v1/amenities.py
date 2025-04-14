from flask_restx import Namespace, Resource, fields
from app.services.__init_ import facade
from app.models.place import Place
from app.models.amenity import Amenity

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')        
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        # register a new amenity
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

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # return a list of all amenities
        all_amenity = facade.get_all_amenities()
        list_all_amenity = []
        for amenity in all_amenity:
            list_all_amenity.append({
                'id': str(amenity.id),
                'name': amenity.name
            })
        return list_all_amenity, 200

@api.route('/<amenity_id>')         
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # retrieve an amenity by ID
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # update an amenity by ID
        amenity_data = api.payload
        amenity_exists = facade.get_amenity(amenity_id)

        # Check if key names are correct
        # key_list = ['name']
        # if not all(name in key_list for name in amenity_data):
        #     return {'error': 'Invalid input data'}, 400

        if amenity_exists:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'message': 'Amenity updated successfully',
                'id': str(updated_amenity.id),
                'name': updated_amenity.name
                }, 200
        else:
            return {'error': 'Amenity not found'}, 404
        
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete Amenity"""
        amenity = facade.get_amenity(amenity_id)

        if amenity:
            facade.delete_amenity(amenity_id)

            return {"message": "Amenity deleted successfully"}, 200
        return {'Error': 'Amenity not found'}, 404


        ### CURL COMMMANDS TO TEST HHTP REQUESTS ###
#  Register a New Amenity
#  curl -X POST http://127.0.0.1:5000/api/v1/amenities/ -H "Content-Type: application/json" -d '{"name": "Wi-Fi"}'

#  Retrieve All Amenities
#  curl -X GET http://127.0.0.1:5000/api/v1/amenities/ -H "Content-Type: application/json"

#  Retrieve Amenity Details
#  curl -X GET http://127.0.0.1:5000/api/v1/amenities/<amenity_id> -H "Content-Type: application/json"

#  Update a Amenity’s Information
#  curl -X PUT http://127.0.0.1:5000/api/v1/amenities/<amenity_id> -H "Content-Type: application/json" -d '{"name": "Air Conditioning"}'

#  Delete a Amenity:
#  curl -X DELETE "http://127.0.0.1:5000/api/v1/amenities/<amenities_id>" -H "Content-Type: application/json"
