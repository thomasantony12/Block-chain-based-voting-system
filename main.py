from flask import Flask
from public import public
from admin import admin
from district import district
from booth import booth
from candidate import candidate
from voter import voter
from email.mime.text import MIMEText
from flask_mail import Mail
from api import api

app=Flask(__name__)
app.secret_key='key'

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'projectsriss2020@gmail.com'
app.config['MAIL_PASSWORD'] = 'messageforall'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(district,url_prefix='/district')
app.register_blueprint(booth,url_prefix='/booth')
app.register_blueprint(candidate,url_prefix='/candidate')
app.register_blueprint(voter,url_prefix='/voter')
app.register_blueprint(api,url_prefix="/api")

app.run(debug=True,port=5009,host="192.168.43.65")