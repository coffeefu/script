#!/usr/bin/env python3
import json
import requests
import time
import argparse
import pymongo
import time


#https://m.weibo.cn/api/container/getIndex?uid=3212105147&luicode=20000174&type=uid&value=3212105147&containerid=1076033212105147
																												# 005053212105147
#https://m.weibo.cn/api/container/getIndex?uid=6138708048&luicode=10000011&type=uid&value=6138708048&containerid=1076036138708048
#https://m.weibo.cn/api/container/getIndex?uid=3212105147&luicode=10000011&type=uid&value=3212105147&containerid=1076036138708048

# def load_weibo(url):
# 	r=requests.get(url)
# 	return json.loads(r.text)

def parse_json(uid,dbname):
	url='https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode=10000011&type=uid&value={uid}&containerid=107603{uid}'
	r=requests.get(url.format(uid=uid))
	a_json=json.loads(r.text)
	# print(url.format(uid=uid))
	client=pymongo.MongoClient()
	db=client.weibo
	tb=db[dbname]
	for a_weibo in a_json['data']['cards'][::-1]:
		a_weibo=a_weibo['mblog']
		text=a_weibo['text']
		uid=a_weibo['id']
		source=a_weibo['source']
		comments_count=a_weibo['comments_count']
		# print(text,uid)
		imgs=[]
		retweeted_status=[]
		comments=[]
		insert_time=time.strftime('%Y-%m-%d %H:%M:%S') 
		if a_weibo.__contains__('pics'):
			# print(a_weibo['mblog']['pics'])
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
		curs=tb.find().sort('_id',direction=pymongo.DESCENDING)
		#记录删除的
	flag=0
	for index in range(tb.count()):
		if  tb.count() >index and len(a_json['data']['cards'])<(flag+1)  :
			break
		elif curs[index]['uid']<a_json['data']['cards'][flag]['mblog']['id']:
			break
		elif curs[index]['uid']!=a_json['data']['cards'][flag]['mblog']['id']:
			print(curs[index]['text'])
			if tb.find_one({'uid':curs[index]['uid']}):
					curs[index]['delete']=1
					temp=curs[index]
					temp['delete']=1
			tb.update({'uid':curs[index]['uid']},{'$set':temp})
		else:
			flag+=1

	client.close()

if __name__=='__main__':

	parse=argparse.ArgumentParser()
	parse.add_argument('-u','--uid',help="input uid")
	parse.add_argument('-n','--name',help="input table name")
	args=parse.parse_args()
	while 1:
		try:
		    # a_json=load_weibo(args.url)
		    parse_json(args.uid,args.name)
		    time.sleep(10)
		except Exception as e:
			print(e)
			time.sleep(600)
