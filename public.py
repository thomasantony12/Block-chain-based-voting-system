from flask import *
from database import *
import uuid
from datetime import *
from email.mime.text import MIMEText
from flask_mail import Mail

public=Blueprint('public',__name__)

@public.route('/')
def home():
	session.clear()
	return render_template('home.html')

@public.route('/login',methods=['get','post'])
def login():
	session.clear()
	if 'submit' in request.form:
		uname=request.form['uname']
		passw=request.form['password']

		q="SELECT * FROM `login` WHERE `username`='%s' AND `password`='%s'"%(uname,passw)
		res=select(q)
		if res:
			session['lid']=res[0]['login_id']
			if res[0]['login_type']=='admin':
				flash('WELCOME ADMIN')
				return redirect(url_for('admin.admin_home'))
			elif res[0]['login_type']=='pending':
				flash("YOUR REQUEST IS PENDING")
			elif res[0]['login_type']=='reject':
				flash('YOU WHERE REJECTED!!, CONTACT US')
			elif res[0]['login_type']=='district':
				q="SELECT * FROM `district` WHERE `login_id`='%s'"%(res[0]['login_id'])
				res1=select(q)
				session['district_id']=res1[0]['district_id']
				flash('WELCOME DISTRICT MANAGER')
				return redirect(url_for('district.district_home'))
			elif res[0]['login_type']=='booth':
				q="SELECT * FROM `booth` WHERE `login_id`='%s'"%(res[0]['login_id'])
				res1=select(q)
				session['booth_id']=res1[0]['booth_id']
				return redirect(url_for("booth.booth_home"))
				flash('WELCOME BOOTH MANAGER')
			elif res[0]['login_type']=='candidate':
				q="SELECT * FROM `candidate` WHERE `login_id`='%s'"%(res[0]['login_id'])
				res1=select(q)
				session['cid']=res1[0]['candidate_id']
				flash('WELCOME CANDIDATE')
				return redirect(url_for('candidate.candidate_home'))
			elif res[0]['login_type']=='voter':
				q="SELECT * FROM `voter` WHERE `login_id`='%s'"%(res[0]['login_id'])
				res1=select(q)
				session['voter_id']=res1[0]['voter_id']
				flash('WELCOME VOTER')
				return redirect(url_for('voter.voter_home'))
		else:
			flash('WRONG USERNAME OR PASSWORD')

	return render_template('login.html')


@public.route('/candidate_registration',methods=['get','post'])
def candidate_registration():
	data={}
	q="SELECT * FROM `district`"
	res=select(q)
	data['district']=res
	q="SELECT * FROM `election`"
	res=select(q)
	data['election']=res

	if 'submit' in request.form:
		election=request.form['election']
		district=request.form['district']
		fname=request.form['fname']
		lname=request.form['lname']
		img=request.files['image']
		path="static/"+str(uuid.uuid4())+img.filename
		img.save(path)
		age=request.form['age']
		dob=request.form['dob']
		place=request.form['place']
		city=request.form['city']
		state=request.form['state']
		phone=request.form['phone']
		aadhar=request.form['aadhar']
		email=request.form['email']
		uname=request.form['uname']
		password=request.form['password']
		d=datetime.strptime(dob, '%Y-%m-%d')
		a=datetime.today()
		v=a.year-d.year


		if v<25:
			flash('UNDER AGE')
		else:
			q1="SELECT * FROM `candidate` WHERE `aadhar`='%s'"%(aadhar)
			res1=select(q1)
			q2="SELECT * FROM `candidate` WHERE `phone`='%s'"%(phone)
			res2=select(q2)
			q3="SELECT * FROM `candidate` WHERE `email`='%s'"%(email)
			res3=select(q3)
			q4="SELECT * FROM `login` WHERE `username`='%s'"%(uname)
			res4=select(q4)
			if res2:
				flash('PHONE NUMBER IS ALREADY TAKEN')
			elif res3:
				flash('EMAIL IS ALREADY TAKEN')
			elif res4:
				flash('USERNAME IS ALREADY TAKEN')
			elif res1:
				flash('REGISTRATION FAILD BECAUSE AADHAR NUMBER ALREADY EXIST')
			else:
				q="INSERT INTO `login`(`username`,`password`,`login_type`) VALUES ('%s','%s','pending')"%(uname,password)
				id=insert(q)
				q1="INSERT INTO `candidate`(`login_id`,`election_id`,`district_id`,`first_name`,`last_name`,`image`,`age`,`dob`,`place`,`city`,`state`,`phone`,`email`,`aadhar`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(id,election,district,fname,lname,path,age,dob,place,city,state,phone,email,aadhar)
				insert(q1)
				flash('DETAILS SUBMITED')

	return render_template('candidate_registration.html',data=data)

@public.route('/voter_registration',methods=['get','post'])
def voter_registration():

	data={}
	q="SELECT * FROM `district`"
	res=select(q)
	data['disup']=res

	if 'submitz' in request.form:
		disid=request.form['disup']
		q="SELECT * FROM `booth` WHERE district_id='%s'"%disid
		res=select(q)
		data['booth']=res
		q=""
		res=q
		data['disup']=res



	q="SELECT * FROM `election`"
	res=select(q)
	data['election']=res

	if 'submit' in request.form:
		booth=request.form['booth']
		election=request.form['election']
		fname=request.form['fname']
		lname=request.form['lname']
		dob=request.form['dob']
		age=request.form['age']
		place=request.form['place']
		city=request.form['city']
		state=request.form['state']
		phone=request.form['num']
		email=request.form['email']
		uname=request.form['uname']
		passs=request.form['psw']
		aadhar=request.form['aadhar']
		d= datetime.strptime(dob, '%Y-%m-%d')
		a=datetime.today()
		v=a.year-d.year
		print(v,"...")
		print(d)
		
		
		
		if v<18:
			flash('UNDER AGE')
		else:
			q1="SELECT * FROM `voter` WHERE `aadhar`='%s'"%(aadhar)
			res1=select(q1)
			q2="SELECT * FROM `voter` WHERE `phone`='%s'"%(phone)
			res2=select(q2)
			q3="SELECT * FROM `voter` WHERE `email`='%s'"%(email)
			res3=select(q3)
			q4="SELECT * FROM `login` WHERE `username`='%s'"%(uname)
			res4=select(q4)
			if res2:
				flash('PHONE NUMBER IS ALREADY TAKEN')
			elif res3:
				flash('EMAIL IS ALREADY TAKEN')
			elif res4:
				flash('USERNAME IS ALREADY TAKEN')
			elif res1:
				flash('REGISTRATION FAILD BECAUSE AADHAR NUMBER ALREADY EXIST')
			else:
				q="INSERT INTO `login`(`username`,`password`,`login_type`) VALUES ('%s','%s','pending')"%(uname,passs)	
				login_id=insert(q)

				q="INSERT INTO `voter`(`login_id`,`booth_id`,`election_id`,`first_name`,`last_name`,`age`,`dob`,`place`,`city`,`state`,`phone`,`email`,`aadhar`)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(login_id,booth,election,fname,lname,age,dob,place,city,state,phone,email,aadhar)
				insert(q)
				flash('REGISTERED')

				try:
					gmail = smtplib.SMTP('smtp.gmail.com', 587)

					gmail.ehlo()

					gmail.starttls()

					gmail.login('projectsriss2020@gmail.com','messageforall')

				except Exception as e:
					print("Couldn't setup email!!"+str(e))

				msg = MIMEText("Your Username is " + uname +" and password is " + passs  )
				# msg = MIMEText("Your password is Haii")

				msg['Subject'] = 'Your Username and Password'

				msg['To'] = email

				msg['From'] = 'projectsriss2020@gmail.com'

				try:

					gmail.send_message(msg)
					print(msg)
					print(email)

				except Exception as e:

					print("COULDN'T SEND EMAIL", str(e))

					# For Message Close

			    # return jsonify({'tasks':"success"})
				return redirect(url_for('public.voter_registration'))
		
	return render_template("voter_registration.html",data=data)
