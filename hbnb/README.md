### PROJECT DESCRIPTION &ensp; ✏️
<hr>
This is part 3 of the HBnB project and the second implemention phase of the HBnB application based on the codebase in part 2.
This phase focuses on extending the backend of the application by adding user authentication, authorization and integration of the database using SQLAlchemy and MySQL.

### PART 2 OBJECTIVES &ensp; ✅
<hr>

* Modify user registration by including the password field and implement password hashing using bcrypt.
* Implement JWT-based user authentication using Flask-JWT-Extended to enable secure login through token generation.
* Secure certain endpoints via JWT token generation to only allow authenticated users to perform certain actions.
* Add administrative priviledges to specific API endpoints to allow administrators to perform certain actions without being restricted by ownership of Places and Reviews.
* Replace the in-memory repository with SQLAlchemy to help integrate persistent storage.
* Map system entities (User, Amenity, Place, Review) to the MySQL database using SQLAlchemy.
* Map the relationships between system entities, including "one-to-many" relationships (User and Places, Place and Reviews and User and Reviews) the "many-to-many" relationship (Place and Amenities and Amenities and Places).

### HOW TO INSTALL IT &ensp; 🔧
<hr>

The requirements needed for part 3 are:
* flask
* flaskrestx
* flask-bcrypt
* flask-jwt-extended
* sqlalchemy
* flask-sqlalchemy

To install the requirements, download the repository, navigate to the part3/hbnb folder and use the following command to install:
<br>

```
pip install -r requirements.txt
```

### HOW TO RUN IT &ensp; 🖥️
<hr>
Once requirments are installed, ensure the MySQL server is running and initialise the database. This can be done in flask shell.
Run the run.py file to launch the application and start up the Flask development server.
This will allow the user to interact with the application locally.
<br>

```
flask shell
>>> from app import db
>>> db.create_all()
```

```
python3 run.py
```

### API ENDPOINTS &ensp; ⚙️

Part 3 includes the same API endpoints from part 2 plus ($${\color{lightgreen}+}$$) admin.py, auth.py and protected.py 
<br>

$${\color{lightgreen}+}$$__Auth__:
<br>
* Initiate a login process and generate token POST /api/v1/auth/login/

$${\color{lightgreen}+}$$ __Protected__:
* Allows user to make authenticated requests to protected endpoints GET /api/v1/protected

$${\color{lightgreen}+}$$ __Admin__:
<br>
The following endpoints are restricted to administrators only.
Administrators can delete any place or review.
* Create a new user POST /api/v1/admin/users/
* Modify a user's details, including email and password PUT /api/v1/admin/users/<user_id>
* Add a new amenity POST /api/v1/admin/amenities/
* Modify the details of an amenity PUT /api/v1/admin/amenities/<amenity_id>
* Delete a Place DELETE /api/v1/admin/places/<place_id>
* Delete a Review DELETE /api/v1/admin/reviews/review_id>

$${\color{lightgreen}+}$$ __Endpoints with JWT Authentication__:
* Create a new place POST /api/v1/places/ 
* Update a place's details. Only the owner of the place can modify its information PUT /api/v1/places/<place_id>: 
* Create a new review. Users can only review places they do not own and can only create one review per place POST /api/v1/reviews/
* Update a review. Users can only modify reviews they created PUT /api/v1/reviews/<review_id>
* Delete a review. Users can only delete reviews they created DELETE /api/v1/reviews/<review_id>: 
* Users can only modify their own details (excluding email and password) PUT /api/v1/users/<user_id>

__Endpoints created in part 2:__
<br>
<br>
__Users__:
* Create a User POST /api/v1/users
* Retrieve a User by ID GET /api/v1/users/<user_id>
* Retrieve a List of Users GET /api/v1/users/
* Update a User PUT /api/v1/users/<user_id>

__Amenities__:
* Register a new amenity POST /api/v1/amenities/
* Retrieve a list of all amenities GET /api/v1/amenities/
* Get amenity details by ID GET /api/v1/amenities/<amenity_id>
* Update an amenity's information PUT /api/v1/amenities/<amenity_id>

__Places__:
* Register a new place POST /api/v1/places/
* Return a list of all places GET /api/v1/places/
* Retrieve details of a specific place, including its associated owner and amenities GET /api/v1/places/<place_id>
* Update place information PUT /api/v1/places/<place_id>

__Reviews__:
* Register a new review POST /api/v1/reviews/
* Return a list of all reviews GET /api/v1/reviews/
* Retrieve details of a specific review GET /api/v1/reviews/<review_id>
* Retrieve all reviews for a specific place GET /api/v1/places/<place_id>/reviews
* Update a review’s information PUT /api/v1/reviews/<review_id>
* Delete a review DELETE /api/v1/reviews/<review_id>

### HOW TO USE IT &ensp; 🧑‍💻
<hr>
Use the following commands to test different endpoints using cURL:

### Login and Get JWT
Possible status codes:
* 200: Success
* 401: Invalid credentials
```
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -H "Content-Type: application/json" -d
'{
  "email": "john.doe@example.com",
  "password": "your_password"
}'
```

### Expected Response
```
{
    "access_token": "your_generated_jwt_token"
}
```

### Test Authenticated Endpoint for Place creation
Possible status codes:
* 201: Place successfully created
* 400: Invalid input data
* 401: Unauthorized User
```
#  curl -X POST http://127.0.0.1:5000/api/v1/places/ -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d
'{
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner": "<user_id>"
}'
```

### Expected Response
```
{
  "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
### Test Unauthorized Place Update
Possible status codes:
* 200: Place updated successfully
* 404: Place not found
* 400: Invalid input data
* 403: Unauthorized action
```
curl -X PUT "http://127.0.0.1:5000/api/v1/places/<place_id>" -H "Authorization: Bearer <wrong/invalid_token>" -H "Content-Type: application/json -d
{
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 150.0
}
```

### Expected Response
```
{
    "error": "Unauthorized action"
}
```

### Test admin priviledges by modifying another User's data
Possible status codes:
* 200: Success
* 400: User does not exist
* 400: Email is already in use
* 400: Invalid input data
* 403: Admin privileges required

```
curl -X PUT "http://127.0.0.1:5000/api/v1/users/<user_id>" -H "Authorization: Bearer <admin_token>" -H "Content-Type: application/json" -d
'{
    "email": "JaneMDoe@example.com"
}' 
```
### Expected response
```
'{
  'message': 'User updated successfully',
  'id': '<user_id>',
  'first_name': 'Jane',
  'last_name': Doe,
  'email': JaneMDoe@example.com,
  'password': <hashed_password>
}'
```
### Test Place-Amenity (many-to-many) Relationship
First add an amenity to a place (POST api/v1/places/<place_id>/amenities)
<br>
Possible status codes:
* 200: Amenity successfully added to the place
* 404: Place not found
```
curl -X POST "http://127.0.0.1:5000/api/v1/places/<place_id>" -H "Content-Type: application/json" -d
'{
  "name": "Wi-Fi",
}'
```
### Expected Response
```
'{
  "message": "Wi-Fi added to <place_title> successfully"
}'
```
### Test retrieval of amenities associated with a specific Place
Possible status codes:
* 200: Success
* 404: Place not found
* 404: Amenities not found
```
curl -X GET "http://127.0.0.1:5000/api/v1/places/<place_id>/amenities" -H "Content-Type: application/json" -d
```

### Expected Response
```
{
    "amenities": [
        {
            "id": "<place_id>",
            "name": "Wi-Fi"
        }
    ]
}
```

### CONTRIBUTORS 🧑‍💻👩‍💻🧑‍💻
Nigel Feng
<br>
Maxine Janka
<br>
Dieu Doan


