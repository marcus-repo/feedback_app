import os
import configparser

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from datetime import datetime


app = Flask(__name__)


# switch between dev and production
ENV = 'prod'
if ENV == 'dev':
    
    # debug modus on
    app.debug = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # local config file
    config = configparser.ConfigParser()
    config.read('config.cfg')

    # Database connection
    app.config['SQLALCHEMY_DATABASE_URI'] = config['POSTGRES']['DATABASE_URL']
    
    # Mailtrap user
    login = config['MAILTRAP']['LOGIN']
    password = config['MAILTRAP']['PASSWORD']
    
else:

    # debug modus off
    app.debug = False

    # Database connection from environment
    DATABASE_URL = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

    # Mailtrap user
    login = os.environ.get("MAIL_LOGIN")
    password = os.environ.get("MAIL_PASSWORD")


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# database model
class Feedback(db.Model):
    __tablename__ = 'response'
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(200))
    course_date = db.Column(db.Date(),nullable=False)
    rating = db.Column(db.Integer)
    recommendation = db.Column(db.Integer)
    comments = db.Column(db.Text())
    created_on = db.Column(db.DateTime(), default=datetime.now)
    
    def __init__(self, course, course_date, rating, recommendation, comments):
        self.course = course
        self.course_date = course_date
        self.rating = rating
        self.recommendation = recommendation
        self.comments = comments  



# feedback homepage
@app.route('/')
def index():
	return render_template('index.html')


# post feedback
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        course = request.form['course']
        #course_date = request.form['course_date']
        rating = request.form['rating']
        recommendation = request.form['recommendation']
        comments = request.form['comments']

        course_date = datetime.strptime(request.form['course_date'], '%Y-%m-%d')
        print(course_date)
        
        # trainer and course is requried
        if course == '':
            return render_template('index.html', 
                                   message='Bitte Kurs auswählen')
        
        # insert data
        data = Feedback(course, course_date, rating, recommendation, comments)
        db.session.add(data)
        db.session.commit()
        
        # send email
        send_mail(login, password, course, course_date, rating, recommendation, comments)
        return render_template('success.html')
    

if __name__ == '__main__':
	app.run()
