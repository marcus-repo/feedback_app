import smtplib
from email.mime.text import MIMEText

#MIMEText allows to send emails in html

def send_mail(login, password, trainer, course, rating, comments):
	port = 2525
	smtp_server = 'smtp.mailtrap.io'
	login = login
	password = password
	message = f"<h3>New Feedback Submission</h3><ul><li>Trainer: {trainer}\
        </li><li>Course: {course} </li><li>Rating: {rating}\
        </li><li>Comments: {comments} </li></ul>"

	sender_email = 'lml-feedback@heroku.com'
	receiver_email = 'lml-feedback@fuerth.com'
	msg = MIMEText(message, 'html')
	msg['Subject'] = 'Feedback'
	msg['From'] = sender_email
	msg['To'] = receiver_email

	# Send email
	with smtplib.SMTP(smtp_server, port) as server:
		server.login(login, password)
		server.sendmail(sender_email, receiver_email, msg.as_string())
	
