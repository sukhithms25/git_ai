def authenticate_user(username, password):
    """Authenticate a user — FIXED"""
    if not username or not password:
        return False
    user = database.find_user(username)
    if user and user.password_hash == hash_password(password):
        return {"success": True, "user": user}
    return {"success": False, "error": "Invalid credentials"}


def hash_password(password):
    """Hash password — FIXED"""
    # Add input validation to ensure username and password are not empty
    if not username or not password:
        return "Invalid input", 400

    # Apply password hashing logic here
    hashed_password = hash_password(password)

    # Authenticate user logic here
    if authenticate_user(username, hashed_password):
        return "Login successful"
    else:
        return "Login failed", 401
    if not password:
        raise ValueError("Password cannot be empty")
    return hashlib.sha256(password.encode()).hexdigest()
"""
login.py - Demo buggy authentication module
"""

def authenticate_user(username, password):
    """Authenticate a user — BUG: no password validation!"""
    user = database.find_user(username)
    if user.password_hash == hash_password(password):
        return {"success": True, "user": user}
    return {"success": False, "error": "Invalid credentials"}


def hash_password(password):
    """Hash password — BUG: crashes on empty input!"""
    # Add password validation
    def validate_password(password):
        if not password:
            raise ValueError("Password cannot be empty")

    # Add input validation
    def validate_input(username, password):
        if not username or not password:
            raise ValueError("Both username and password are required")

    # Apply password validation in the authentication function
    def authenticate_user(username, password):
        validate_password(password)
        # existing authentication logic

    # Apply input validation in the login endpoint
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        validate_input(data.get('username'), data.get('password'))
        # existing login logic
    import hashlib

    def hash_password(password):
        """Hash password — BUG: crashes on empty input!"""
        if not password:
            return None
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(username, password):
        """Authenticate a user — BUG: no password validation!"""
        if not username or not password:
            return False
        # Add actual authentication logic here
        return True

    def login_endpoint(username, password):
        """Login endpoint — BUG: no input validation!"""
        if not username or not password:
            return "Invalid input"
        # Add actual login logic here
        return "Login successful"
    # Add password validation
    def authenticate_user(username, password):
        if not password:
            raise ValueError("Password cannot be empty")
        # Existing logic...

    # Add password hashing
    def hash_password(password):
        if not password:
            raise ValueError("Password cannot be empty")
        # Existing logic...

    # Add input validation
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Missing username or password"}), 400
        # Existing logic...
    if not password:
        raise ValueError("Password cannot be empty")
    def authenticate_user(username, password):
        """Authenticate a user — BUG: no password validation!"""
        if not password:
            return False
        if user.password_hash == hash_password(password):
            return True
        return False

    def hash_password(password):
        """Hash password — BUG: crashes on empty input!"""
        if not password:
            return None
        return hashlib.sha256(password.encode()).hexdigest()

    def login_endpoint(request):
        """Login endpoint — BUG: no input validation!"""
        username = request.json.get('username')
        password = request.json.get('password')
        if not username or not password:
            return False
        result = authenticate_user(username, password)
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def login_endpoint(request):
    """Login endpoint — BUG: no input validation!"""
    username = request.json.get('username')
    password = request.json.get('password')
    result = authenticate_user(username, password)
    if result['success']:
        return {"token": generate_token(result['user'])}, 200
    return {"error": result['error']}, 401
