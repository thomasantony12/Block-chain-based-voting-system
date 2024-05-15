from flask import *
from database import *

booth=Blueprint('booth',__name__)

@booth.route('/booth_home')
def booth_home ():
	if session.get('lid'):
		return render_template('booth_home.html')
	else:
		return redirect(url_for("public.login"))

@booth.route('/booth_view_voters',methods=['get','post'])
def booth_view_voters():
	if session.get('lid'):
		data={}
		bid=session['booth_id']
		q="SELECT `booth`.`booth`,`booth`.`district_id`,`booth`.`booth_id`,`election`.`body`,`election`.`election_id`,`election`.`status`,`login`.`login_id`,`login`.`login_type`,`voter`.`aadhar`,`voter`.`age`,`voter`.`booth_id`,`voter`.`city`,`voter`.`dob`,`voter`.`election_id`,`voter`.`email`,CONCAT(`voter`.`first_name`,' ',`voter`.`last_name`) AS voter,`voter`.`login_id`,`voter`.`phone`,`voter`.`place`,`voter`.`state`,`voter`.`voter_id` FROM `voter` INNER JOIN `login` ON `voter`.`login_id`=`login`.`login_id` INNER JOIN `election` ON `voter`.`election_id`=`election`.`election_id` INNER JOIN `booth` ON `voter`.`booth_id`=`booth`.`booth_id` WHERE `booth`.`booth_id`=%s ORDER BY FIELD(`login_type`, 'pending', 'voter' , 'reported', 'reject') ASC"%(bid)
		res=select(q)
		data['voter']=res

		if 'action' in request.args:
			action=request.args['action']
			ids=request.args['ids']
		else:
			action=None


		if action=='report':
			q1="UPDATE `login` SET `login_type`='reported' WHERE `login_id`='%s'"%(ids)
			update(q1)
			return redirect(url_for('booth.booth_view_voters'))

		return render_template("booth_view_voters.html",data=data)
	else:
		return redirect(url_for("public.login"))