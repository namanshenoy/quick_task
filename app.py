from flask import Flask, render_template, jsonify,request
import json
app = Flask(__name__)
app.config['DEBUG'] = True

list = [
	{'priority': 'high', 'name': 'Name 1', 'id':1},
	{'priority': 'medium', 'name': 'Name 2', 'id':2},
	{'priority': 'low', 'name': 'Name 3', 'id':3}
]

current_id = 3

@app.route('/')
def index():
	return render_template('check_get.html')

@app.route('/api/v1/<user_id>/tasks/view')
def api_tasks_view(user_id):
	temp_list = list[:]
	return_list = []
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
	global current_id
	current_id +=1
	add_item = {'priority': request_json[1]['value'], 'name':request_json[0]['value'], 'id':current_id}
	list.append(add_item)
	print('Success')
	print list
	return json.dumps({'success':'True'}), 200, {'ContentType':'application/json'}

@app.route('/api/v1/<user_id>/tasks/delete', methods=['GET', 'DELETE'])
def api_tasks_delete(user_id):
	request_str = request.data.replace('\\','')
	request_json = json.loads(request_str)
	for task in list:
		print (task,request_json)
		print(task['id'])
		if str(task['id']) == str(request_json['id']):
			list.remove(task)
	print('Success: '+ request_json['id'])
	print list
	return json.dumps({'success':'True'}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
	app.run()
