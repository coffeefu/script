#!/usr/bin/python3
import json
import requests
import time
import argparse
import pymongo
import time

def load_weibo(url):
	r=requests.get(url)
	return json.loads(r.text)

def parse_json(a_json,dbname):
	client=pymongo.MongoClient()
	db=client.weibo
	tb=db[dbname]
	for a_weibo in a_json['data']['cards']:
		a_weibo=a_weibo['mblog']
		text=a_weibo['text']
		uid=a_weibo['id']
		source=a_weibo['source']
		comments_count=a_weibo['comments_count']
		print(text)
		imgs=[]
		retweeted_status=[]
		comments=[]
		insert_time=time.strftime('%Y-%m-%d %H:%M:%S') 
		if a_weibo.__contains__('pics'):
			for a_img in a_weibo['pics']:
				imgs.append(a_img['large']['url'])
		if a_weibo.__contains__('retweeted_status'):
			retweeted_status.append(a_weibo['retweeted_status'])
		if str(comments_count)!='0':
			comments_url='https://m.weibo.cn/api/comments/show?id={}&page=1'.format(uid)
			comments.append(json.loads(requests.get(comments_url).text))
		item={'a_weibo':a_weibo,'uid':uid,'text':text,'source':source,'comments_count':comments_count,'imgs':imgs,'retweeted_status':retweeted_status,'comments':comments,'insert_time':insert_time}
		if tb.find_one({'uid':uid,'comments_count':{"$lt": comments_count}}):
			tb.update({'uid':uid},{'$set':item})
		elif not tb.find_one({'uid':uid}):
			tb.insert_one(item)
	client.close()

if __name__=='__main__':

	parse=argparse.ArgumentParser()
	parse.add_argument('-u','--url',help="input url")
	parse.add_argument('-n','--name',help="input table name")
	args=parse.parse_args()
	while 1:
		a_json=load_weibo(args.url)
		parse_json(a_json,args.name)
		time.sleep(5)