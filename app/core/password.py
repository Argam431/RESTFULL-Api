import hashlib


class Hasher:
    def __init__(self):
        self.secret = None

    def init_app(self, app):
        self.secret = app.secret_key

    def __call__(self, password):
        salt = bytes(self.secret, 'utf-8')

        dk = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), salt, 100000)
            
        return dk.hex()


hash_password = Hasher()
