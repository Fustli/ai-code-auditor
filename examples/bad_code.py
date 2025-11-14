# Example Python code with various issues for testing

import os
import hashlib

class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, username, password):
        # Security issue: storing password in plain text
        user = {
            "username": username,
            "password": password,  # Should be hashed!
            "id": len(self.users) + 1
        }
        self.users.append(user)
        return user
    
    def authenticate(self, username, password):
        # Performance issue: O(n) search
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                return user
        return None
    
    def get_user_by_id(self, user_id):
        # Another O(n) operation that could use a dictionary
        for user in self.users:
            if user["id"] == user_id:
                return user
        return None
    
    # Quality issue: poor function name
    def do_stuff(self, data):
        # Quality issue: no error handling
        result = data * 2
        return result

def unsafe_file_operation(filename):
    # Security issue: path traversal vulnerability
    with open(f"/uploads/{filename}", "r") as f:
        content = f.read()
    return content

def inefficient_fibonacci(n):
    # Performance issue: exponential time complexity
    if n <= 1:
        return n
    return inefficient_fibonacci(n-1) + inefficient_fibonacci(n-2)

# Quality issue: global variable
GLOBAL_COUNTER = 0

def increment_counter():
    global GLOBAL_COUNTER
    GLOBAL_COUNTER += 1
    return GLOBAL_COUNTER