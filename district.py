from flask import *
from database import *

district=Blueprint('district',__name__)

@district.route('/district_home')
def district_home():
	if session.get('lid'):
		return render_template('district_home.html')
	else:
		return redirect(url_for("public.login"))

@district.route('/district_view_booth',methods=['get','post'])
def district_view_booth():
	if session.get('lid'):
		data={}
		did=session['district_id']
		q="SELECT * FROM `booth` INNER JOIN `district` USING (`district_id`) WHERE `district_id`='%s'"%(did)
		res=select(q)
		data['booths']=res
		
		return render_template('district_view_booth.html',data=data)
	else:
		return redirect(url_for("public.login"))

@district.route('/district_view_voters',methods=['get','post'])
def district_view_voters():
	if session.get('lid'):
		data={}
		did=session['district_id']
		q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS NAME FROM `voter` INNER JOIN `booth` USING (`booth_id`) INNER JOIN `district` USING (`district_id`) INNER JOIN `election` USING(`election_id`) INNER JOIN `login` ON(`login`.`login_id`=`voter`.`login_id`) WHERE `district_id`='%s' ORDER BY FIELD(`login_type`, 'pending', 'reported', 'voter', 'reject') ASC"%(did)
		res=select(q)
		data['voters']=res


		if 'action' in request.args:
			action=request.args['action']
			ids=request.args['ids']
		else:
			action=None


		if action=='report':
			q1="UPDATE `login` SET `login_type`='reported' WHERE `login_id`='%s'"%(ids)
			update(q1)
			return redirect(url_for('district.district_view_voters'))

		return render_template('district_view_voters.html',data=data)
	else:
		return redirect(url_for("public.login"))