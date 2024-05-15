from flask import *
from database import*
from core import *

voter=Blueprint('voter',__name__)

@voter.route('/voter_home')
def voter_home():
	if session.get('lid'):
		return render_template("voter_home.html")
	else:
		return redirect(url_for("public.login"))

@voter.route('/voter_view_district_details')
def voter_view_district_details():
	if session.get('lid'):
		data={}

		vid=session['voter_id']
		q="SELECT * FROM `district`"
		res=select(q)
		data['result']=res

		return render_template("voter_view_district_details.html",data=data)
	else:
		return redirect(url_for("public.login"))

@voter.route('/voters_view_booth')
def voters_view_booth():
	if session.get('lid'):
		data={}
		vid=session['voter_id']
		ids=request.args['ids']

		q="SELECT* FROM `booth` WHERE `district_id`='%s'"%(ids)
		res=select(q)
		data['result']=res

		return render_template("voters_view_booth.html",data=data)
	else:
		return redirect(url_for("public.login"))

@voter.route('/voter_view_candidate')
def voter_view_candidate():
	if session.get('lid'):
		data={}
		vid=session['voter_id']
		
		q="SELECT *,CONCAT (`candidate`.`first_name`,' ',`candidate`.`last_name`) AS candidate FROM `candidate`  INNER JOIN `election` USING (`election_id`) INNER JOIN `login` USING (`login_id`) WHERE `login_type`='candidate' and district_id=(SELECT `district_id` FROM `voter` INNER JOIN `booth` USING (`booth_id`) WHERE `voter_id`='%s')"%(session['voter_id'])
		res=select(q)
		data['voters']=res
		return render_template("voter_view_candidate.html",data=data)
	else:
		return redirect(url_for("public.login"))

@voter.route('/voter_view_election_status')
def voter_view_election_status():
	if session.get('lid'):
		data={}
		vid=session['voter_id']
		
		q="SELECT* FROM `election`"
		res=select(q)
		data['status']=res
		return render_template("voter_view_election_status.html",data=data)
	else:
		return redirect(url_for("public.login"))

@voter.route('/voter_make_vote')
def voter_make_vote():
	if session.get('lid'):
		data={}
		vid=session['voter_id']
		ids=request.args['ids']
		data['ids']=ids
		q="SELECT * FROM `vote` INNER JOIN `candidate` USING (`candidate_id`) INNER JOIN `election` USING (`election_id`) WHERE `election_id`='%s' AND `voter_id`='%s'"%(ids,vid)
		print(q)
		res=select(q)
		if res:
			flash('ALREADY VOTED')
			return redirect(url_for('voter.voter_view_election_status'))
		else:

			q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS NAME FROM `candidate` WHERE `election_id`='%s' and district_id=(SELECT `district_id` FROM `voter` INNER JOIN `booth` USING (`booth_id`) WHERE `voter_id`='%s')"%(ids,session['voter_id'])
			res=select(q)
			data['candidates']=res

		if 'action'in request.args:
			action=request.args['action']
			cids=request.args['cids']

		else:
			action=None

		if action=='vote':
			cid=request.args['cids']
			q = "select * from vote order by vote_id desc"
			res = select(q)
			if len(res) > 0 :
				previous_hash = res[0]['hash_value']
			else:
				previous_hash = '0'
			hashing_value = str(vid) + str(ids) + str(previous_hash)
			new_hash = get_hashed_value(hashing_value)
			q="INSERT INTO `vote`(`vote_time`,`voter_id`,`candidate_id`,`hash_value`) VALUES(NOW(),'%s','%s','%s')"%(vid,cid,new_hash)
			insert(q)
			# q="INSERT INTO `vote` (`vote_time`,`voter_id`,`candidate_id`) VALUES (NOW(),'%s','%s')"%(vid,cids)
			# insert(q)
			return redirect(url_for('voter.voter_view_election_status'))

		return render_template("voter_make_vote.html",data=data)
	else:
		return redirect(url_for("public.login"))

@voter.route('/voter_view_result')
def voter_view_result():
	if session.get('lid'):
		data={}
		vid=session['voter_id']
		# eid=request.args['eid']
		q="SELECT *, CONCAT (`candidate`.`first_name`,' ',`candidate`.`last_name`)AS NAME FROM `result` INNER JOIN `candidate` USING (`candidate_id`) INNER JOIN `district` USING (`district_id`) ORDER BY (`district`)"
		res=select(q)
		data['result']=res
		return render_template("voter_view_result.html",data=data)
	else:
		return redirect(url_for("public.login"))