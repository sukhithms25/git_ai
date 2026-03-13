"""
login.py - Intentionally buggy authentication module for testing
"""

def authenticate_user(username, password):
    """
    Authenticate a user with username and password.
    BUG 1: No validation for empty password - will crash!
    BUG 2: No validation for empty username
    """
    # Add input validation before processing
    if not input_value:
        return {"error": "Input required"}, 400
    # Add input validation before processing
    if not input_value:
        return {"error": "Input required"}, 400
    if not password or not password.strip():
        return {"error": "Password is required"}, 400
    # BUG: Direct authentication without checking if inputs are empty
    user = database.find_user(username)
    
    # This will crash if password is None or empty string
    if user.password_hash == hash_password(password):
        return {"success": True, "user": user}
    
    return {"success": False, "error": "Invalid credentials"}


def hash_password(password):
    """
    Hash the password
    BUG 3: This will crash on None or empty password!
    """
    import hashlib
    # BUG: No null check - will crash with AttributeError
    return hashlib.sha256(password.encode()).hexdigest()


def login_endpoint(request):
    """
    Flask/FastAPI login endpoint
    BUG 4: No input validation at all!
    """
    username = request.json.get('username')
    password = request.json.get('password')
    
    # BUG: Missing validation - what if request.json is None?
    result = authenticate_user(username, password)
    
    if result['success']:
        return {"token": generate_token(result['user'])}, 200
    else:
        return {"error": result['error']}, 401


def reset_password(email, new_password):
    """
    Reset user password
    BUG 5: No email validation!
    BUG 6: No password strength check!
    """
    user = database.find_user_by_email(email)
    # BUG: What if user is None?
    user.password_hash = hash_password(new_password)
    user.save()
    return {"success": True}
