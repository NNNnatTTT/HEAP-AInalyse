from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import jwt
import datetime
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# JWT secret for Kong (should match Kong configuration)
JWT_SECRET = "b18e4adfc5d84177cd8c053e5baaf0913504dafd2f1448ea374614aa0262b312"

def generate_jwt_token(user_id, email):
    """Generate a JWT token that Kong can validate"""
    payload = {
        'sub': user_id,  # Subject (user ID)
        'email': email,
        'iss': 'auth_service',  # Issuer
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    
    # Include 'kid' in header for Kong
    headers = {
        'kid': 'auth_service'
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256', headers=headers)

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('Email')
    password = request.json.get('Password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    try:
        # Create user in Supabase Auth
        result = supabase.auth.sign_up({"email": email, "password": password})
        
        # Handle different response formats
        if hasattr(result, 'model_dump'):
            data = result.model_dump()
            if data.get("error"):
                return jsonify({"msg": data["error"]["message"]}), 400
        elif isinstance(result, dict):
            if result.get("error"):
                return jsonify({"msg": result["error"]["message"]}), 400
        elif hasattr(result, 'error') and result.error:
            return jsonify({"msg": result.error.message}), 400
            
        return jsonify({"message": "Signup successful. Please check your email to verify your account."}), 200
    except Exception as e:
        return jsonify({"msg": f"Error during signup: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('Email')
    password = request.json.get('Password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    try:
        # Authenticate user with Supabase Auth
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        # Handle different response formats and extract user info
        user_id = None
        user_email = None
        
        if hasattr(result, 'model_dump'):
            data = result.model_dump()
            if data.get("error"):
                return jsonify({"msg": data["error"]["message"]}), 401
            user = data.get("user")
            if user:
                user_id = user.get('id')
                user_email = user.get('email')
        elif isinstance(result, dict):
            if result.get("error"):
                return jsonify({"msg": result["error"]["message"]}), 401
            user = result.get("user")
            if user:
                user_id = user.get('id')
                user_email = user.get('email')
        else:
            # Object with attributes
            if hasattr(result, 'error') and result.error:
                return jsonify({"msg": result.error.message}), 401
            user = getattr(result, 'user', None)
            if user:
                user_id = getattr(user, 'id', None)
                user_email = getattr(user, 'email', None)

        if not user_id or not user_email:
            return jsonify({"msg": "Invalid login response"}), 401

        # Generate custom JWT token for Kong
        custom_token = generate_jwt_token(user_id, user_email)

        return jsonify({
            "access_token": custom_token,
            "user": {
                "id": user_id,
                "email": user_email
            }
        }), 200
    except Exception as e:
        return jsonify({"msg": f"Error during login: {str(e)}"}), 500

@app.route('/verify', methods=['GET'])
def verify_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"msg": "Missing or invalid Authorization header"}), 401
    
    token = auth_header.split(' ')[1]

    try:
        # Verify the custom JWT token
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        
        # Extract user info from token
        user_id = payload.get('sub')
        user_email = payload.get('email')
        
        return jsonify({
            "message": "Token is valid.",
            "user": {
                "id": user_id,
                "email": user_email
            }
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"msg": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"msg": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"msg": f"Error during token verification: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
