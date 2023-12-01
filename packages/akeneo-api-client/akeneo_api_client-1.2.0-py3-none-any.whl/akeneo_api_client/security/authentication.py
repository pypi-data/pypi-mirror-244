class Authentication:

    def __init__(self):
        self.username = ''
        self.password = ''
        self.client_id = ''
        self.secret = ''
        self.access_token = ''
        self.refresh_token = ''

    @staticmethod
    def from_password(username, password, client_id, secret):
        auth = Authentication()
        auth.username = username
        auth.password = password
        auth.client_id = client_id
        auth.secret = secret
        return auth
