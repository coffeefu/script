# coding=utf-8
from flask import Flask, request, session, g, redirect, abort, render_template, flash
import pymongo
import json

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY='development key',
))


@app.route('/weibo',methods=['get'])
def show_weibo():
    client = pymongo.MongoClient()
    db = client.weibo
    
    page=int(request.args.get('page'))
    name=request.args.get('name')
    collection = db[name]
    weibos=[]
    test=[]
    for cur in collection.find().sort('_id',direction=pymongo.DESCENDING).skip((page-1)*5).limit(5):
        cur['a_weibo']['insert_time']=cur['insert_time']
        cur['a_weibo']['comments']=cur['comments']
        weibos.append(cur['a_weibo'])
        print(cur['a_weibo']['text'])
    client.close()
    return json.dumps({'data':weibos})





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
