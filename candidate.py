from flask import *
from database import *

candidate=Blueprint('candidate',__name__)

@candidate.route('/candidate_home')
def candidate_home():
	if session.get('lid'):
		return render_template('candidate_home.html')
	else:
		return redirect(url_for("public.login"))
	
@candidate.route('/candidate_view_voting_status',methods=['get','post'])
def candidate_view_voting_status():
	if session.get('lid'):
		data={}
		id=session['cid']
		q1="SELECT `district_id` FROM candidate WHERE `candidate_id`='%s'"%(id)
		disid=select(q1)
		session['disid']=disid[0]['district_id']
		disidd=session['disid']
		q="SELECT `status` FROM `election` WHERE `status`='started'"
		res=select(q)
		if res:
			q="SELECT COUNT(`candidate_id`) AS COUNT FROM `vote`"
			res1=select(q)
			data['status']=res1
		else:
			q="SELECT *,CONCAT (`candidate`.`first_name`,' ',`candidate`.`last_name`) AS candidate_name FROM `result` INNER JOIN `candidate` USING (`candidate_id`) INNER JOIN `district` USING (`district_id`) WHERE `district_id`='%s' ORDER BY (`district`)"%(disidd)
			res=select(q)
			data['result']=res

		return render_template("candidate_view_voting_status.html",data=data)
	else:
		return redirect(url_for("public.login"))


@candidate.route('/candidate_view_boothwise')
def candidate_view_boothwise():
	if session.get('lid'):
		data={}
		id=session['cid']
		q="SELECT * FROM `booth`"
		data['booth']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			bid=request.args['id']
		else:
			action=None
			
		if action=='result':
			q="SELECT COUNT(`vote_id`) AS vote,`candidate_id`,`voter_id`,CONCAT (`candidate`.`first_name`,' ',`candidate`.`last_name`) AS cand_name FROM `vote` INNER JOIN `voter` USING(`voter_id`) INNER JOIN `candidate` USING (`candidate_id`) WHERE `booth_id`='%s' GROUP BY `candidate_id`"%(bid)
			res=select(q)
			data['booth_result']=res
		
		return render_template("candidate_view_boothwise.html",data=data)

	else:
		return redirect(url_for("public.login"))


@candidate.route('/candidate_view_districtwise')
def candidate_view_districtwise():
	if session.get('lid'):		
		data={}
		id=session['cid']
		q="SELECT * FROM `district`"
		data['district']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			did=request.args['id']
		else:
			action=None
		if action=='result':
			q="SELECT COUNT(`vote_id`)  AS vote,`candidate_id`,`voter_id`,CONCAT (`candidate`.`first_name`,' ',`candidate`.`last_name`) AS cand_name FROM `vote` INNER JOIN `voter` USING(`voter_id`) INNER JOIN `candidate` USING (`candidate_id`) WHERE `district_id`='%s' GROUP BY `candidate`.`candidate_id`"%(did)
			res=select(q)
			data['dis_result']=res
		return render_template("candidate_view_districtwise.html",data=data)
	else:
		return redirect(url_for("public.login"))