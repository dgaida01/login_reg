from flask import Flask
app = Flask(__name__)
app.secret_key = 'the secret key which should be more secret than this for real sessions'