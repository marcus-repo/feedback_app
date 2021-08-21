from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from datetime import datetime
import os

app = Flask(__name__)


ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sa@localhost/yoga'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
else:
    app.debug = False
    DATABASE_URL = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL  

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    trainer = db.Column(db.String(200))
    course = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())
    created_on = db.Column(db.DateTime(), default=datetime.now)
    
    def __init__(self, trainer, course, rating, comments):
        self.trainer = trainer
        self.course = course
        self.rating = rating
        self.comments = comments  


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        trainer = request.form['trainer']
        course = request.form['course']
        rating = request.form['rating']
        comments = request.form['comments']
        
        if trainer == '' or course == '':
            return render_template('index.html', 
                                   message='Bitte Trainer und Kurs auswählen')
        
       
        data = Feedback(trainer, course, rating, comments)
        db.session.add(data)
        db.session.commit()
        
        send_mail(trainer, course, rating, comments)
        return render_template('success.html')
    

if __name__ == '__main__':
	app.run()

