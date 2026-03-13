if not password or not password.strip():
    return {"error": "Password is required"}, 400
