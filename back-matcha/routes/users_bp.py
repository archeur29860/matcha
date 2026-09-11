from flask import Blueprint, request
from models.users_m import Users
import services.users_service as u

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

@users_bp.route("/", methods=["POST"])
# def modify_email():
#     data = request.get_json()

#     if not data:
#         return {"error":"JSON body required"}, 400

#     if "email" not in data:
#         return {"error" : "email is required"}, 400
    
#     email = data["email"].strip()

#     if not email:
#         return {"error": "email cannot be empty"}, 400
    
#     if len(email) > 255:
#         return {"error": "email must be 255 characters or less"}, 400
    
#     result = u.add_email(email)

#     if result is None:
#         return {"error": "email already exists"}, 409

#     return {
#         "email": result["email"]
#         }, 201

# def modify_username():
#     data = request.get_json()

#     if not data:
#         return {"error":"JSON body required"}, 400

#     if "username" not in data:
#         return {"error" : "username is required"}, 400
    
#     username = data["username"].strip()

#     if not username:
#         return {"error": "username cannot be empty"}, 400
    
#     if len(username) > 50:
#         return {"error": "username must be 50 characters or less"}, 400
    
#     result = u.add_username(username)

#     if result is None:
#         return {"error": "username already exists"}, 409

#     return {
#         "id": result["id"],
#         "username": result["username"]
#         }, 201

# def modify_last_name():
#     data = request.get_json()

#     if not data:
#         return {"error":"JSON body required"}, 400

#     if "last_name" not in data:
#         return {"error" : "last_name is required"}, 400
    
#     last_name = data["last_name"].strip()

#     if not last_name:
#         return {"error": "last_name cannot be empty"}, 400
    
#     if len(last_name) > 100:
#         return {"error": "last_name must be 100 characters or less"}, 400
    
#     result = u.add_last_name(last_name)

#     return {
#         "id": result["id"],
#         "last_name": result["last_name"]
#         }, 201

# def modify_first_name():
#     data = request.get_json()

#     if not data:
#         return {"error":"JSON body required"}, 400

#     if "first_name" not in data:
#         return {"error" : "first_name is required"}, 400
    
#     first_name = data["first_name"].strip()

#     if not first_name:
#         return {"error": "first_name cannot be empty"}, 400
    
#     if len(first_name) > 50:
#         return {"error": "first_name must be 50 characters or less"}, 400
    
#     result = u.add_first_name(first_name)

#     return {
#         "id": result["id"],
#         "first_name": result["first_name"]
#         }, 201

# def modify_password():
#     data = request.get_json()

#     if not data:
#         return {"error":"JSON body required"}, 400

#     if "password" not in data:
#         return {"error" : "password is required"}, 400
    
#     password = data["password"].strip()

#     if not password:
#         return {"error": "password cannot be empty"}, 400
    
#     if len(password) > 255:
#         return {"error": "password must be 255 characters or less"}, 400
    
#     result = u.add_password(password)

#     return {
#         "id": result["id"],
#         "password": result["password"]
#         }, 201

# def modify_last_connection():
#     data = request.get_json()

#     if not data:
#         return {"error":"JSON body required"}, 400

#     if "last_co" not in data:
#         return {"error" : "last_co is required"}, 400
    
#     last_co = data["last_co"].strip()

#     result = s.add_tag(last_co)


#     return {
#         "id": result["id"],
#         "last_co": result["last_co"]
#         }, 201

# def modify_is_online():
#     data = request.get_json()

#     if not data:
#         return {"error":"JSON body required"}, 400

#     if "is_online" not in data:
#         return {"error" : "is_online is required"}, 400
        
#     result = u.add_tag(data)


#     return {
#         "id": result["id"],
#         "is_online": result["is_online"]
#         }, 201

# def modify_signaled():
#     data = request.get_json()

#     if not data:
#         return {"error":"JSON body required"}, 400

#     if "signaled" not in data:
#         return {"error" : "signaled is required"}, 400
    
#     result = u.add_signaled(data)

#     return {
#         "id": result["id"],
#         "signaled": result["signaled"]
#         }, 201




def create_user():
    data = request.get_json()
    all_field_content = {}
    if not data:
        return {"error":"JSON body required"}, 400

    required_fields = ["email", "username", "last_name", "first_name", "password"]
    for field in required_fields:
        if field not in data:
          return {"error": f"The field '{field}' is required"}, 400
        field_content = data[field].strip()
        if not field_content:
            return {"error": f"{field} cannot be empty"}, 400
    
        if field == "email" or  field == "password":
            if len(field) > 255:
                return {"error": f"{field} must be 255 characters or less"}, 400
        else:
            if len(field) > 50:
                return {"error": f"{field} must be 50 characters or less"}, 400
        all_field_content[field] = field_content

    
    result = u.add_user(all_field_content)

    if result is None:
        return {"error": "email already exists"}, 409

    return result, 201