if not password or not password.strip():
    return {"error": "Password is required"}, 400
        return {"token": generate_token(result['user'])}, 200
    else:
        return {"error": result['error']}, 401
