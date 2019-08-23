#!/usr/bin/env python3

# Import modules
from flask import Flask


app = Flask(__name__)

@app.route('/')
def home():
    return 'Home page'



# Run the app in the '__main__' scope
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)