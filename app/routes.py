import json

from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request

from requests import post

from app import app
from app.notebook import decode
from app.notebook import encode


@app.before_first_request
def before_first_request_func():
    data = {
        'messages': []
    }
    with open(f'{request.host[-4:]}.json', "w") as write_file:
        json.dump(data, write_file)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        json_obj = {
            'key': encode(
                request.form.get('key'), 
                app.config.get('SECRET_KEY')
            ),
            'msg': encode(
                request.form.get('msg'), 
                request.form.get('key')
            )
        }

        try:
            if request.host[-4:] == '5000':
                resp = post('http://127.0.0.1:3000/exchange', json=json_obj)
            else:
                resp = post('http://127.0.0.1:5000/exchange', json=json_obj)
            flash('Сообщение зашифровано и отправлено', category='success')
        except:
            flash('Второе приложение отключено', category='danger')
    return render_template('index.html')


@app.route('/exchange', methods=['POST'])
def exchange():
    with open(f'{request.host[-4:]}.json', 'r') as read_file:
        data = json.load(read_file)
    
    data['messages'].append({
        'key': request.json.get('key'),
        'msg': request.json.get('msg')
    })
    
    with open(f'{request.host[-4:]}.json', "w") as write_file:
        json.dump(data, write_file)

    return jsonify({
        'result': 'Зашифровано и сохранено'
    })


@app.route('/posts', methods=['GET'])
def posts():
    with open(f'{request.host[-4:]}.json', 'r') as read_file:
        data = json.load(read_file)['messages']
    
    posts = [
        decode(
            d['msg'],
            decode(d['key'], app.config['SECRET_KEY'])
        ) for d in data
    ]

    return render_template('posts.html', posts=posts)
