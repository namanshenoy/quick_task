from flask import Flask, render_template, jsonify,request
import json
from bson.json_util import dumps as bson_dumps
from flask_pymongo import PyMongo
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://admin:Naman123@ds141108.mlab.com:41108/tasks'

mongo = PyMongo(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/api/v1/<user_id>/tasks/view')
def api_tasks_view(user_id):
	return_list = []
	tasks = mongo.db.tasks

	temp_list = json.loads(bson_dumps(tasks.find({'user':user_id})))
	for task in temp_list:
		if task['priority'] == 'high':
			return_list.append(task)
			temp_list.remove(task)


	for task in temp_list:
		if task['priority'] == 'medium':
			return_list.append(task)
			temp_list.remove(task)


	for task in temp_list:
		if task['priority'] == 'low':
			return_list.append(task)
			temp_list.remove(task)


	return jsonify(return_list)

@app.route('/api/v1/<user_id>/tasks/add', methods=['GET', 'POST'])
def api_tasks_add(user_id):
	print(request.json)
	request_json = request.json
	tasks = mongo.db.tasks

	current_id = tasks.find_and_modify({"CURRENT_ID": {"$exists": True}},{"$inc": {"CURRENT_ID": 1}}, True)
	task = {'user':user_id, 'priority': request_json[1]['value'], 'name':request_json[0]['value'], 'id':current_id['CURRENT_ID']}
	task_id = tasks.insert_one(task).inserted_id
	print ('added task: ' +str(task_id))
	print('Add Success')
	return json.dumps({'success':'True'}), 200, {'ContentType':'application/json'}

@app.route('/api/v1/<user_id>/tasks/delete', methods=['GET', 'DELETE'])
def api_tasks_delete(user_id):
	request_str = request.data.replace('\\','')
	request_json = json.loads(request_str)
	tasks = mongo.db.tasks
	print('DELETING')
	tasks.remove({'id': int(request_json['id'])})
	print('Success: '+ request_json['id'])
	return json.dumps({'success':'True'}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
	app.run()
