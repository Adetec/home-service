#!/usr/bin/env python3
from application import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, ssl_context=('cert.pem', 'key.pem'))
