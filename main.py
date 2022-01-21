from distutils.command.config import config
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def home():
    return '<h1> Hello World </h1>'

if __name__ == "__main__":
    app.run(host='0.0.0.0')