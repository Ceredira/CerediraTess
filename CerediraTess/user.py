import hashlib
import os


class User:
    def __init__(self, username, salt=None, key=None):
        self.username = username
        self.salt = salt
        self.key = key

    def create_password(self, password):
        salt_binary = os.urandom(32)  # A new salt for this user
        self.salt = salt_binary.hex()
        self.key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_binary, 10000).hex()

    def check_password(self, password):
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(self.salt), 10000).hex()
        if self.key == new_key:
            return True
        else:
            return False
