# coding=utf-8
from flask import Flask, request, session, g, redirect, abort, render_template, flash
import pymongo
import json

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY='development key',
))


@app.route('/weibo/pmm',methods=['post'])
def show_pmm():
    client = pymongo.MongoClient()
    db = client.weibo
    collection = db.newpmm
    page=int(request.form.get('page'))
    weibos=[]
    for cur in collection.find().skip(collection.count()-page*5).limit(5):
        weibos.append(cur['a_weibo'])
    return json.dumps({'data':weibos})

@app.route('/weibo/wyj',methods=['post'])
def show_wyj():
    client = pymongo.MongoClient()
    db = client.weibo
    collection = db.wyj
    page=int(request.form.get('page'))
    weibos=[]
    for cur in collection.find().skip(collection.count()-page*5).limit(5):
        weibos.append(cur['a_weibo'])
    return json.dumps({'data':weibos})


@app.route('/', methods=['post'])
def answer():
    client = pymongo.MongoClient
    db = client.moha
    collection = db.test
    do = request.form.get('do')
    question=request.form.get('question')
    answer=request.form.get('answer')
    count=request.form.get('count')
    collection.update_one({'question': question}, {'$set': {'question':
                     question, 'answer': answer, 'count': count+1,'do':do}})


@app.route('/check', methods=['post'])
def check_user_name():
    session['user_name'] = request.args.get('user_name')


@app.route('/login', methods=['post'])
def login():
    user_psw = request.form.get('user_psw')
    email = request.form.get('email')
    return json.dumps({user_psw: email})
# def get_weibo():
#     client = pymongo.MongoClient()
#     db = client.weibo
#     collection = db.pmm
#     weibos = []
#     for aWeibo in collection.find().sort('count'):
#         weibos.append(weibo)

# @app.route('/')
# def hello():
#     if not session.get('keywords'):
#         abort(401)
#     return render_template('mytest.html')


# @app.route('/search', methods=['post'])
# def search_ht():
#     error = None
#     session['logged_in'] = True
#     print(request.args.get('keywords'))
#     return "666"


# @app.route('/posts')
# def sayHelloTwice():
# return render_template('helloTwice.html', posts=[{'index': '1'},
# {'index': '2'}, {'index': '3'}])


# @app.route('/test', methods=['get', 'post'])
# def test():
#     return json.dumps({'test': '666'})


# @app.route('/login', methods=['post'])
# def login():
#     id = request.args.get('id')
#     psw = request.args.get('psw')
#     with pymongo.MongoClient() as client:
#         db = client.info
#         collection = db.student
#         if collection.find_one({'id': id, 'psw': psw}):
#             return 's'
#     return "账号密码错误"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
