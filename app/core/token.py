import jwt


class Token:
    def __init__(self):
        self.secret_key = None

    def init_app(self, app):
        self.secret_key = app.secret_key

    def encode(self, payload):
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def decode(self, encoded_token):
        return jwt.decode(encoded_token, self.secret_key, algorithm="HS256")


token = Token()
