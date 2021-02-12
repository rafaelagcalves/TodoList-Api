"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user/<name>', methods=['GET'])
def get_user_information(name):
    user = User.get_by_name(name)
    if user:
        return jsonify(user.serialize()), 200
    else: "User nor found", 404

@app.route('/user', methods=['POST'])
def create_user():
    name = request.get_json().get("name", None)
    if name:
        user = User(name=name, is_active=True)
        user.add()
        return "Created user", 201
    return "Missing new user name", 400

@app.route('/user/<name>', methods=['PUT'])
def update_user(name):
    user = User.get_by_name(name)
    new_name = request.get_json().get("name", None)
    
    if new_name and User.get_by_name(new_name) is None:
        updated_user = user.update_name(new_name)
        return updated_user.serialize(), 200
    
    return "Another user with this username already exists. Maybe it's your evil twin. Spooky!", 400

@app.route('/user/<name>', methods=['DELETE'])
def delete_user(name):
    user = User.get_by_name(name)
    if user:
        delete_user = User.delete_user(user)
        return f'Your account has been deleted: {user}', 200
    else:
        return 'That username does not exists', 404
    
@app.route('/user/<name>/tasks', methods=['GET'])
def get_user_tasks(name):
    user = User.get_by_name(name)
    tasks = Task.get_by_user(user.id)
    tasks = [task.serialize() for task in tasks if task is not None]
    return jsonify(tasks), 200

@app.route('/user/<name>/tasks', methods=['POST'])
def add_user_new_task(name):
    user = User.get_by_name(name)
    new_tasks = request.get_json()

    for new_task in new_tasks:
        task = Task(
            label= new_task.get('label'),
            is_done= new_task.get('is_done'),
            user_id=user.id
        )
        task.add(name)

    return "Added tasks",200

@app.route('/user/<name>/tasks/<id>', methods=['PUT'])
def update_task(name, id):
    body = request.get_json()
    id = int(id)
    task = Task.get_by_id(id)
    task.update_task(body['label'], body['is_done'], )

    return "Task Updated Successfully", 200

@app.route('/user/<name>/tasks/<id_tasks>', methods=['DELETE'])
def delete_tasks(name, id_tasks):
    task = Task.get_task(id_tasks)
    task.delete()
    return f'Your task has been deleted', 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
