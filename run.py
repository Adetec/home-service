from application import app



# Run the app in the '__main__' scope
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)