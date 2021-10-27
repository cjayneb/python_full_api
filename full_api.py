import flask
import requests
from Task import Task
from flask import Flask, request, jsonify, url_for, abort, redirect, render_template
from markupsafe import escape

tasks = [
    {
        'id': 1,
        'title': u'Schedule Scrum Meeting',
        'description': u'Call group members to schedule the meeting',
        'done': False
    },
    {
        'id': 2,
        'title': u'Watch TV',
        'description': u'Open TV and relax. Do nothing else',
        'done': True
    },
    {
        'id': 3,
        'title': u'Code DTO and Object Mapper',
        'description': u'Add DTO and Mapper to service, modify methods and tests accordingly',
        'done': False
    }
]

app = flask.Flask("full_api")
app.config["DEBUG"] = True


@app.route('/')
def home():
    return "<h1>Hello Flask. This is my full API</h1>"


@app.route('/tasks/')
def get_all_tasks():
    return jsonify(tasks)


@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    response =[]
    for t in tasks:
        if t['id'] == task_id:
            response.append(t)
    if len(response) == 0:
        abort(404)
    return jsonify(response)


@app.route('/tasks/', methods=['POST'])
def post_task():
    task_id = len(tasks) + 1
    title = request.json.get('title')
    description = request.json.get('description')
    done = request.json.get('done')

    tasks.append({
        'id': task_id,
        'title': title,
        'description': description,
        'done': done
    })
    return jsonify(tasks)


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def put_task(task_id):
    the_task = []
    for idx, task in enumerate(tasks):
        if task['id'] == task_id:
            the_task.append(task)
            the_task.append(idx)
    if len(the_task) == 0:
        abort(404)

    tasks[the_task[1]]['title'] = request.json.get('title')
    tasks[the_task[1]]['description'] = request.json.get('description')
    tasks[the_task[1]]['done'] = request.json.get('done')

    return jsonify(tasks)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404

app.run()
