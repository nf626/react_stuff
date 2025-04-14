from flask_restx import Namespace, Resource, fields
from app.services.__init_ import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request


api = Namespace('users', description='User operations')


# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
            }, 201

    @api.response(200, 'User list retrieved successfully')
    def get(self):
        """List all users"""
        all_users = facade.get_all_users()
        list_all_users = []
        for user in all_users:
            list_all_users.append({
                'id': str(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            })
        return list_all_users, 200
        
    @api.route('/<user_id>')
    class UserResource(Resource):
        @api.response(200, 'User details retrieved successfully')
        @api.response(404, 'User not found')
        def get(self, user_id):
            """Get user details by ID"""
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password
                }, 200
        
        @api.expect(user_model)
        @api.response(200, 'User details updated successfully')
        @api.response(400, 'User does not exist')
        @jwt_required()
        def put(self, user_id):
            """Update user details by ID"""
            user_data = api.payload
            user_exists = facade.get_user(user_id)

            # If the user is trying to modify another user's data
            current_user = get_jwt_identity()
            if user_exists.id != current_user['id']:
                return {'error': 'Unauthorized User'}, 403

            # Prevent the user from modifying their email and password
            if user_exists.email != user_data['email']:
                # Debug
                print(user_exists.email, user_data['email'])
                return {'error': 'You cannot modify email'}, 400

            if not user_exists.verify_password(user_data['password']):
                # Debug
                print(user_exists.password, user_data['password'])
                print(user_exists.verify_password(user_data['password']))
                return {'error': 'You cannot modify password'}, 400

            if user_exists:
                updated_data = facade.update_user(user_id, user_data)
                return {
                    'message': 'User updated successfully',
                    'id': str(updated_data.id),
                    'first_name': updated_data.first_name,
                    'last_name': updated_data.last_name,
                    'email': updated_data.email
                    }, 200
            else:
                return {'error': 'User does not exist'}, 400
        
        @api.response(200, 'User deleted successfully')
        @api.response(404, 'User not found')
        @api.response(403, 'Unauthorized action')
        @jwt_required()
        def delete(self, user_id):
            """Delete a user"""
            user_exists = facade.get_user(user_id)
            current_user = get_jwt_identity()

            if not user_exists:
                return {'Error': 'User not found'}, 404
        
            # print(current_user['id'])
            if user_exists.id != current_user['id']:
                return {'Error': 'Unauthorized action'}, 403
            else:
                facade.delete_user(user_id)
                return {"message": "User deleted successfully"}, 200


        ### CURL COMMMANDS TO TEST HHTP REQUESTS ###
#  Register new user:
#  curl -X POST http://127.0.0.1:5000/api/v1/users/ -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "123", "is_admin": true}'

# User login
# curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -H "Content-Type: application/json" -d '{"email": "john.doe@example.com", "password": "123"}'

#  Get details by ID:
#  curl -X GET "http://127.0.0.1:5000/api/v1/users/<user_id>" -H "Content-Type: application/json"

#  List all users:
#  curl -X GET "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json"

#  Update user details:
#  curl -X PUT http://127.0.0.1:5000/api/v1/users/<user_id> -H "Content-Type: application/json" -d '{"first_name": "Jane", "last_name": "Do", "email": "jane.do@example.com"}' -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json"
