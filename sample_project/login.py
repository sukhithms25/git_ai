"""
login.py - Sample buggy authentication module
"""

def authenticate_user(username, password):
    """
    Authenticate a user with username and password.
    BUG: No validation for empty password!
    """
    if not password or not password.strip():
        return {"error": "Password is required"}, 400
    # Direct authentication without checking if password is empty
    user = database.find_user(username)
    
    # This will crash if password is None or empty string
    if user.password_hash == hash_password(password):
        return {"success": True, "user": user}
    
    return {"success": False, "error": "Invalid credentials"}


def hash_password(password):
    """Hash the password - but crashes on empty input"""
    import hashlib
    # BUG: This will fail if password is None or empty
    return hashlib.sha256(password.encode()).hexdigest()


def login_endpoint(request):
    """
    Flask/FastAPI login endpoint
    BUG: Doesn't validate password before processing
    """
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Missing validation here!
    result = authenticate_user(username, password)
    
    if result['success']:
        return {"token": generate_token(result['user'])}, 200
    else:
        return {"error": result['error']}, 401
