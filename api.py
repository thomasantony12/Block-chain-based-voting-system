from flask import *
from database import *

import demjson
import uuid
from core import *

api=Blueprint('api',__name__)

@api.route('/login',methods=['get','post'])
def login():
	data={}
	
	username = request.args['username']
	password = request.args['password']
	q="SELECT * from login where username='%s' and password='%s'" % (username,password)
	print(q)
	res = select(q)
	if res :
		data['status']  = 'success'
		data['data'] = res
		data['method']='login'
	else:
		data['status']	= 'failed'
		data['method']='login'
	return  demjson.encode(data)


@api.route('/View_candidate',methods=['get','post'])
def View_candidate():
	data={}

	login_id=request.args['login_id']
	
	q="SELECT *,CONCAT(`candidate`.`first_name`,' ',`candidate`.`last_name`) AS cname FROM `candidate` INNER JOIN `election` USING (`election_id`) WHERE `candidate_status`='accepted' AND district_id=(SELECT `district_id` FROM `voter` INNER JOIN `booth` USING (`booth_id`) WHERE `voter_id`=(SELECT `voter_id` FROM `voter` WHERE `login_id`='%s'))"%(login_id)
	print(q)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
		
	else:
		data['status']	= 'failed'
	data['method']='View_candidate'
	return  demjson.encode(data)


@api.route('/View_district',methods=['get','post'])
def View_district():
	data={}

	q="SELECT * FROM `district`"
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
		
	else:
		data['status']	= 'failed'
	data['method']='View_district'
	return  demjson.encode(data)


@api.route('/View_booth',methods=['get','post'])
def View_booth():
	data={}

	district_ids=request.args['district_ids']

	q="SELECT* FROM `booth` WHERE `district_id`='%s'"%(district_ids)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
		
	else:
		data['status']	= 'failed'
	data['method']='View_booth'
	return  demjson.encode(data)



@api.route('/View_election_status',methods=['get','post'])
def View_election_status():
	data={}

	q="SELECT* FROM `election`"
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
		
	else:
		data['status']	= 'failed'
	data['method']='View_election_status'
	return  demjson.encode(data)



@api.route('/Make_vote_candidate',methods=['get','post'])
def Make_vote_candidate():
	data={}

	login_id=request.args['login_id']
	election_ids=request.args['election_ids']

	q="SELECT *,CONCAT(`candidate`.`first_name`,' ',`candidate`.`last_name`) AS cname FROM `candidate` WHERE `election_id`='%s' and district_id=(SELECT `district_id` FROM `voter` INNER JOIN `booth` USING (`booth_id`) WHERE `voter_id`=(SELECT `voter_id` FROM `voter` WHERE `login_id`='%s'))"%(election_ids,login_id)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
		
	else:
		data['status']	= 'failed'
	data['method']='Make_vote_candidate'
	return  demjson.encode(data)


@api.route('/make_vote',methods=['get','post'])
def make_vote():

	data = {}
	data['method']='make_vote'
	login_id=request.args['login_id']
	candidate_ids=request.args['candidate_ids']
	election_ids=request.args['election_ids']
	q="SELECT `voter_id` FROM `voter` WHERE `login_id`='%s'"%(login_id)
	res=select(q)
	vid=res[0]['voter_id']

	q="SELECT * FROM `vote` INNER JOIN `candidate` USING (`candidate_id`) INNER JOIN `election` USING (`election_id`) WHERE `election_id`='%s' AND `voter_id`=(SELECT `voter_id` FROM `voter` WHERE `login_id`='%s')"%(election_ids,login_id)
	print(q)
	res=select(q)
	if res:
		data['status']='Already Voted'
	else:
		q = "select * from vote order by vote_id desc"
		print(q)
		res = select(q)
		if len(res) > 0 :
			previous_hash = res[0]['hash_value']
		else:
			previous_hash = '0'
		hashing_value = str(vid) + str(election_ids) + str(previous_hash)
		new_hash = get_hashed_value(hashing_value)
		q="INSERT INTO `vote`(`vote_time`,`voter_id`,`candidate_id`,`hash_value`) VALUES(NOW(),(SELECT `voter_id` FROM `voter` WHERE `login_id`='%s'),'%s','%s')"%(login_id,candidate_ids,new_hash)
		print(q)
		insert(q)
		data['status']='success'
		
	
	return demjson.encode(data)



@api.route('/View_result',methods=['get','post'])
def View_result():
	data={}

	q="SELECT *,CONCAT(`candidate`.`first_name`,' ',`candidate`.`last_name`) AS cname FROM `result` INNER JOIN `candidate` USING (`candidate_id`)"
	res=select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
		
	else:
		data['status']	= 'failed'
	data['method']='View_result'
	return  demjson.encode(data)
