# Pro Handy service
## One million Arab Coder Challenge Sept-2019
### Overview
This app provides a list of home services within a variety of categories as well as provides a user registration and authentication system (for client or handyman, company ..etc). Registered users will have the ability to post, edit and delete their services or requests.

Every one can register and get benefit of the app service
#### For the client:
User can reach out every neiberhood handyman, company or entreprener and get contact with him by requesting him from services he / it provides, making disscution ...etc

#### For services poster
Service owner can post his work for everyone and make offers for interested client, he also can react with him by sending messages to each other

### Features
Progressive web App
Neiberhood location services offers for clients 
Authentication & Authorization




### Techs used:
#### Backend
* [Python 3](https://www.python.org/download/releases/3.0/)
* [Flask](https://flask.palletsprojects.com/en/1.0.x/): is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.
* [SQLAlchemy](https://www.sqlalchemy.org/): Is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.
* [Jinja2](https://jinja.palletsprojects.com/en/2.10.x/): is a modern and designer-friendly templating language for Python, modelled after Django’s templates. It is fast, widely used and secure with the optional sandboxed template execution environment
* [Flask moment](https://github.com/miguelgrinberg/Flask-Moment): Formatting of dates and times in Flask templates using moment.js.
* [FTW](https://flask-wtf.readthedocs.io/en/stable/): Simple integration of Flask and WTForms, including CSRF, file upload, and reCAPTCHA.
* [Mail Message](https://pythonhosted.org/Flask-Mail/): One of the most basic functions in a web application is the ability to send emails to your users
* Flask RestAPI
* 
#### Front-end
* Html
* Css
* Vanilla Javascript (ES6)
* [Mapbox Api](https://mapbox.com): let developers build a new world powered by location data. Real-time updates. Total customization. Developers first.
* [Bootstrap4](https://getbootstrap.com/): is an open source toolkit for developing with HTML, CSS, and JS. Quickly prototype ideas or build  entire app with Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful plugins built on jQuery
* [JQuery](https://jquery.com): is a fast, small, and feature-rich JavaScript library. It makes things like HTML document traversal and manipulation, event handling, animation, and Ajax much simpler with an easy-to-use API that works across a multitude of browsers. With a combination of versatility and extensibility, jQuery has changed the way that millions of people write JavaScript.
* [Ajax](https://www.tutorialrepublic.com/javascript-tutorial/javascript-ajax.php): stands for Asynchronous Javascript And Xml. Ajax is just a means of loading data from the server and selectively updating parts of a web page without reloading the whole page.
* [Aos js](https://github.com/michalsnik/aos): Animate on scroll library
* [BX-Slider Js](https://bxslider.com/): Responsive jQuery content slider
* [Google fonts](https://fonts.google.com)
* [Materialise icons](https://material.io/resources/icons)
* [Font Awsome](https://fontawesome.com/)


### How to run
* First clone [ProHandy](https://github.com/Adetec/home-service) webapp onto your local machine
* CD into the app directory
* Python and pip should be installed
* Packages should  be installed
```
1 python-secrets
2 Flask_Login
3 Flask_Bcrypt
4 Flask_WTF
5 Flask_Moment
6 Flask_Cors
7 Flask_SQLAlchemy
8 Flask_Mail
9 itsdangerous
10 WTForms
11 Flask
12 Pillow
```

* Open your terminal and run ```pip3 freeze > reuirements.txt```
* Open `application/__init__.py`
* Create a google mail or if you want to set your own Email and password

```
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# change this lines below
app.config['MAIL_USERNAME'] = os.environ.get('HS_DB_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('HS_DB_PASS')
# by following
app.config['MAIL_USERNAME'] = 'youremail@gmail.com'
app.config['MAIL_PASSWORD'] = 'dummypassword'
```

* Make shure you're on the app root directory
* Run 'python3 run.py'
Open the app on your browser at `http://localhost:5000` and have fun

**ps**: If doesn't work, try to uncomment one of options in `run.py` file


### Thanks to:
* My wife for her huge patience and help :rose:
* His Highness **Sheikh Mohammed bin Rashid Al Maktoum**, UAE Vice President, Prime Minister and Ruler of Dubai
* [The 1 Million Arab Coders](/http://www.arabcoders.ae) initiative
* [Udacity](https://udacity.com)
* [Stackoverflow](https://stackoverflow.com)
* [Google](https://google.com)


## Images credits to:
[FreePix](freepik.com) image web library