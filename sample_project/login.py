if not password or not password.strip():
    return {"error": "Password is required"}, 400
        return {"error": result['error']}, 401
