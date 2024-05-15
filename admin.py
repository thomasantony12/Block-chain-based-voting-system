from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
	if session.get('lid'):
		return render_template('admin_home.html')
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_manage_district',methods=['get','post'])
def admin_manage_district():
	if session.get('lid'):
		data={}
		
		if 'action' in request.args:
			action=request.args['action']
			ids=request.args['ids']
		else:
			action=None

		if action=='update':
			q="SELECT * FROM `district` WHERE `login_id`='%s'"%(ids)
			res=select(q)
			data['dist_up']=res

		if 'submits' in request.form:
			dname=request.form['dname']
			q="UPDATE `district` SET `district`='%s' WHERE `login_id`='%s'"%(dname,ids)
			update(q)
			flash('Details updated')
			return redirect(url_for('admin.admin_manage_district'))


		if action=='delete':
			q="DELETE FROM `district` WHERE `login_id`='%s'"%(ids)
			delete(q)
			print(q)
			q1="DELETE FROM `login` WHERE `login_id`='%s'"%(ids)
			delete(q1)
			flash('Details deleted')
			return redirect(url_for('admin.admin_manage_district'))

		if 'submit' in request.form:
			dname=request.form['dname']
			uname=request.form['uname']
			password=request.form['password']
			q="SELECT * from `district` WHERE `district`='%s'"%(dname)
			res=select(q)
			q1="SELECT * FROM `login` WHERE `username`='%s'"%(uname)
			res1=select(q1)
			if res:
				flash('DISTRICT ALREADY INSERTED')
			elif res1:
				flash('USER NAME ALREADY TAKEN')	
			else:
				q="INSERT INTO `login`(`username`,`password`,`login_type`) VALUES ('%s','%s','district')"%(uname,password)
				id=insert(q)
				q1="INSERT INTO `district`(`login_id`,`district`) VALUES ('%s','%s')"%(id,dname)
				insert(q1)
				flash('DISTRICT DETAILS SUBMITED')
				return redirect(url_for('admin.admin_manage_district'))

		q="SELECT * FROM `district`"
		res=select(q)
		data['dist']=res
			
		return render_template('admin_manage_district.html',data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_manage_booth',methods=['get','post'])
def admin_manage_booth():
	if session.get('lid'):
		data={}

		if 'action' in request.args:
			action=request.args['action']
			ids=request.args['ids']
		else:
			action=None

		if action=='update':
			q="SELECT * FROM `booth` WHERE `login_id`='%s'"%(ids)
			res=select(q)
			data['booth_up']=res


		if 'submits' in request.form:
			dname=request.form['dname']
			q="UPDATE `booth` SET `booth`='%s' WHERE `login_id`='%s'"%(dname,ids)
			update(q)
			flash('Booth updated')
			return redirect(url_for('admin.admin_manage_booth'))


		q="SELECT * FROM `booth`"
		res=select(q)
		data['booth']=res


		if action=='delete':
			q="DELETE FROM `booth` WHERE `login_id`='%s'"%(ids)
			delete(q)
			q1="DELETE FROM `login` WHERE `login_id`='%s'"%(ids)
			delete(q1)
			flash('Booth deleted')
			return redirect(url_for('admin.admin_manage_booth'))
		


		q="SELECT * FROM `district`"
		res=select(q)
		data['district']=res


		if 'submit' in request.form:
			district_id=request.form['district']
			bname=request.form['bname']
			uname=request.form['uname']
			password=request.form['password']
			q="SELECT * FROM `booth` WHERE `booth`='%s'"%(bname)
			res=select(q)
			q1="SELECT * FROM `login` WHERE `username`='%s'"%(uname)
			res1=select(q1)
			if res:
				flash('BOOTH NAME ALREADY INSERTED')	
			elif res1:
				flash('USERNAME ALREADY TAKEN')
			else:
				q="INSERT INTO `login`(`username`,`password`,`login_type`) VALUES ('%s','%s','booth')"%(uname,password)
				id=insert(q)
				q1="INSERT INTO `booth`(`login_id`,`district_id`,`booth`) VALUES ('%s','%s','%s')"%(id,district_id,bname)
				insert(q1)
				flash('DETAILS SUBMITED')
				return redirect(url_for('admin.admin_manage_booth'))


		return render_template('admin_manage_booth.html',data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_manage_voters',methods=['get','post'])
def admin_manage_voters():
	if session.get('lid'):
		data={}
		

		if 'action' in request.args:
			action=request.args['action']
			ids=request.args['ids']
		else:
			action=None


		if action=='approve':
			q1="UPDATE `login` SET `login_type`='voter' WHERE `login_id`='%s'"%(ids)
			update(q1)
			return redirect(url_for('admin.admin_manage_voters'))

		if action=='reject':
			q1="UPDATE `login` SET `login_type`='reject' WHERE `login_id`='%s'"%(ids)
			update(q1)
			return redirect(url_for('admin.admin_manage_voters'))

		if 'submit' in request.form:
			eno=request.form['eno']

			q="SELECT *,CONCAT (`voter`.`first_name`,' ',`voter`.`last_name`) AS voter,voter.login_id as lids FROM `voter` INNER JOIN `booth` USING(`booth_id`)  INNER JOIN `election` USING(`election_id`) INNER JOIN `login` ON (`voter`.`login_id`=`login`.`login_id`) WHERE `aadhar`='%s'"%(eno)
			res=select(q)
			data['votor']=res	
		else:
			q="SELECT *,CONCAT (`voter`.`first_name`,' ',`voter`.`last_name`) AS voter,voter.login_id as lids FROM `voter` INNER JOIN `booth` USING(`booth_id`)  INNER JOIN `election` USING(`election_id`) INNER JOIN `login` ON (`voter`.`login_id`=`login`.`login_id`) ORDER BY FIELD(`login_type`, 'pending', 'reported', 'voter', 'reject') ASC"
			res=select(q)
			data['votor']=res

		return render_template('admin_manage_voters.html',data=data)
	else:
		return redirect(url_for("public.login"))


@admin.route('/admin_manage_candidate',methods=['get','post'])
def admin_manage_candidate():
	if session.get('lid'):
		data={}

		if 'action' in request.args:
			action=request.args['action']
			ids=request.args['ids']
		else:
			action=None

		if action=='approve':
			q1="UPDATE `login` SET `login_type`='candidate' WHERE `login_id`='%s'"%(ids)
			update(q1)
			q="UPDATE `candidate` SET `candidate_status`='accepted' WHERE `login_id`='%s'"%(ids)
			update(q)
			return redirect(url_for('admin.admin_manage_candidate'))

		if action=='reject':
			q1="UPDATE `login` SET `login_type`='reject' WHERE `login_id`='%s'"%(ids)
			update(q1)
			q="UPDATE `candidate` SET `candidate_status`='reject' WHERE `login_id`='%s'"%(ids)
			update(q)
			return redirect(url_for('admin.admin_manage_candidate'))

		q="SELECT *,CONCAT (`candidate`.`first_name`,' ',`candidate`.`last_name`) AS candidate,candidate.login_id as lids FROM `candidate` INNER JOIN `district` USING(`district_id`)  INNER JOIN `election` USING(`election_id`) INNER JOIN `login` ON (`candidate`.`login_id`=`login`.`login_id`) ORDER BY FIELD(`login_type`, 'pending' , 'candidate' , 'reject') ASC"
		res=select(q)
		data['candidate']=res

		return render_template('admin_manage_candidate.html',data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_manage_election',methods=['get','post'])
def admin_manage_election():
	if session.get('lid'):
		if 'submit' in request.form:
			body=request.form['body']
			edate=request.form['edate']
			ddate=request.form['date']
			q="INSERT INTO `election` (`body`,`election_date`,`declared_on`,`status`) VALUES('%s','%s','%s','pending')"%(body,edate,ddate)
			insert(q)

		data={}
		q="SELECT * FROM `election` "	
		res=select(q)
		data['election']=res

		if 'action' in request.args:
			action=request.args['action']
			eid=request.args['eid']
		else:
			action=None
		if action=='started':
			q="UPDATE `election` SET `status`='started' WHERE `election_id`='%s'"%(eid)
			update(q)
			return redirect(url_for('admin.admin_manage_election'))
		if action=='completed':
			q="UPDATE `election` SET `status`='completed' WHERE `election_id`='%s'"%(eid)
			update(q)
			q="INSERT INTO `result`(candidate_id,total_vote) SELECT candidate_id,COUNT(*) AS total_vote FROM vote  GROUP BY candidate_id ORDER BY total_vote DESC "
			insert(q)	
			return redirect(url_for('admin.admin_manage_election'))

		if 'action' in request.args:
			action=request.args['action']
			eid=request.args['eid']
		else:
			action=None

		if action=='delete':
			q="DELETE FROM `election` WHERE `election_id`='%s'"%(eid)
			delete(q)
			flash('DELETED')
			return redirect(url_for('admin.admin_manage_election'))

		if action=='update':
			q="SELECT * FROM `election` WHERE `election_id`='%s'"%(eid)
			data['election_up']=select(q)
		if 'updatez' in request.form:
			body=request.form['body']
			edate=request.form['edate']
			q="UPDATE `election` SET `election_date`='%s',body='%s' WHERE `election_id`='%s'"%(edate,body,eid)
			update(q)
			flash('UPDATED')
			return redirect(url_for('admin.admin_manage_election'))	


		return render_template('admin_manage_election.html',data=data)
	else:
		return redirect(url_for("public.login"))



@admin.route('/admin_view_result',methods=['get','post'])
def admin_view_result():
	if session.get('lid'):
		data={}
		q="SELECT *,CONCAT (`candidate`.`first_name`,' ',`candidate`.`last_name`) AS candidate FROM `candidate` INNER JOIN `result` USING(`candidate_id`) INNER JOIN district USING(`district_id`) ORDER BY(`district`)"
		res=select(q)
		data['result']=res


		return render_template('admin_view_result.html',data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_realtime_result',methods=['get','post'])
def admin_realtime_result():
	if session.get('lid'):
		data={}
		q="SELECT * FROM `election` WHERE `election_id`='%S'"%(eid)
		res=select(q)
		data['election']=res


		return render_template('admin_realtime_result.html',data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route('/admin_count_vote')
def admin_count_vote():
	if session.get('lid'):
		data={}
		q="SELECT * FROM `election`"
		res=select(q)
		data['election']=res
		if 'action' in request.args:
			action=request.args['action']
			eid=request.args['id']
		else:
			action=None
		if action=='count':
			q="SELECT COUNT(`candidate_id`) AS COUNT,`candidate`.`candidate_id`,`election_id`,`district`,CONCAT (`candidate`.`first_name`,' ',`candidate`.`last_name`) AS candidate FROM `vote` INNER JOIN `candidate` USING (`candidate_id`) INNER JOIN `district` USING(`district_id`) INNER JOIN `election` USING (`election_id`) WHERE `election_id`='%s' GROUP BY `candidate_id` ORDER BY(`district`)"%(eid)
			res1=select(q)
			data['status']=res1
			return render_template('admin_realtime_result.html',data=data)

		return render_template("admin_count_vote.html",data=data)
	else:
		return redirect(url_for("public.login"))


@admin.route('/clear_tables',methods=['get','post'])
def clear_tables():
	data={}
	tables = ['booth','candidate','district','election','login','result','vote','voter']
	for table in tables:
		q="TRUNCATE TABLE %s"%(table)
		update(q)
	q="INSERT INTO `login` VALUES (null,'admin','admin','admin')" 
	insert(q) 
	return redirect(url_for('public.home'))