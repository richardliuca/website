import secrets
token = secrets.token_hex(16)
print(token)
ENV = 'development'
DEBUG = True
TESTING = True
SECRETE_KEY = token
