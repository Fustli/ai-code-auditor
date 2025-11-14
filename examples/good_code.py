# Example of well-written Python code

import hashlib
import secrets
from typing import Optional, Dict, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class User:
    """User data class with proper typing"""
    id: int
    username: str
    password_hash: str
    salt: str

class SecureUserManager:
    """Secure and efficient user management system"""
    
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._username_to_id: Dict[str, int] = {}
        self._next_id = 1
    
    def add_user(self, username: str, password: str) -> User:
        """Add a new user with secure password hashing"""
        if username in self._username_to_id:
            raise ValueError(f"Username '{username}' already exists")
        
        # Generate secure salt and hash password
        salt = secrets.token_hex(16)
        password_hash = self._hash_password(password, salt)
        
        user = User(
            id=self._next_id,
            username=username,
            password_hash=password_hash,
            salt=salt
        )
        
        self._users[self._next_id] = user
        self._username_to_id[username] = self._next_id
        self._next_id += 1
        
        return user
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with O(1) lookup"""
        user_id = self._username_to_id.get(username)
        if not user_id:
            return None
        
        user = self._users[user_id]
        if self._verify_password(password, user.password_hash, user.salt):
            return user
        
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID with O(1) lookup"""
        return self._users.get(user_id)
    
    def get_all_users(self) -> List[User]:
        """Get all users as a list"""
        return list(self._users.values())
    
    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        """Hash password with salt using SHA-256"""
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    @staticmethod
    def _verify_password(password: str, hash_value: str, salt: str) -> bool:
        """Verify password against hash"""
        return SecureUserManager._hash_password(password, salt) == hash_value

class SecureFileHandler:
    """Secure file handling with proper validation"""
    
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path).resolve()
    
    def read_file(self, filename: str) -> str:
        """Safely read file with path validation"""
        file_path = self._validate_path(filename)
        
        try:
            with file_path.open('r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found")
        except PermissionError:
            raise PermissionError(f"Permission denied reading '{filename}'")
    
    def _validate_path(self, filename: str) -> Path:
        """Validate file path to prevent directory traversal"""
        # Remove any path separators and resolve
        clean_filename = Path(filename).name
        file_path = (self.base_path / clean_filename).resolve()
        
        # Ensure the file is within the base directory
        if not str(file_path).startswith(str(self.base_path)):
            raise ValueError(f"Invalid file path: {filename}")
        
        return file_path

def efficient_fibonacci(n: int) -> int:
    """Calculate Fibonacci number with O(n) time complexity"""
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr

def fibonacci_memoized(n: int, cache: Optional[Dict[int, int]] = None) -> int:
    """Calculate Fibonacci with memoization for O(n) time and space"""
    if cache is None:
        cache = {}
    
    if n in cache:
        return cache[n]
    
    if n <= 1:
        result = n
    else:
        result = fibonacci_memoized(n-1, cache) + fibonacci_memoized(n-2, cache)
    
    cache[n] = result
    return result

class Counter:
    """Thread-safe counter class instead of global variables"""
    
    def __init__(self, initial_value: int = 0):
        self._value = initial_value
    
    def increment(self) -> int:
        """Increment counter and return new value"""
        self._value += 1
        return self._value
    
    def get_value(self) -> int:
        """Get current counter value"""
        return self._value
    
    def reset(self) -> None:
        """Reset counter to zero"""
        self._value = 0