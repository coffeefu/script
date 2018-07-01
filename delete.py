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

#设定页数->循环->判断中止条件 


def parse_json(uid,dbname):
    	#设置页数
	page=1
	#连接客户端以及服务器
	client=pymongo.MongoClient()
	db=client.weibo
	tb=db[dbname]
	#配置游标
	curs=tb.find().sort('uid',direction=pymongo.DESCENDING)
	#初始化游标为0
	index=0
	isDeUid=False
	#初始化网页
	url='https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode=10000011&type=uid&value={uid}&containerid=107603{uid}'
	while 1:
    	#得到json
		r=requests.get(url.format(uid=uid)+"&page={}".format(page))
		a_json=json.loads(r.text)
		#配置flag
		flag=0
		#这里已经请求完毕了所有page+=1
		page+=1
		#这里是如果数据库的uid<微博的uid的话就会退出

		#如果包含这个msg就退出
		print(page,isDeUid)
		if a_json.__contains__('msg'):
			break
		if isDeUid:
			print('这里越界',page)
			break
		#如果uid小于也退出
		first=True
		#进入循环
		while 1:
    			#如果数据库的cur数量大于index
			if  len(a_json['data']['cards'])<(flag+1):
				print('break')
				break
			elif (tb.count()-1)<index:
				isDeUid=True			
				print('isDeUid',True)
				break
			elif curs[index]['uid']<a_json['data']['cards'][flag]['mblog']['id'] and not first:
				print('break')
				isDeUid=True
				print('isDeUid',True)
				break
			elif curs[index]['uid']!=a_json['data']['cards'][flag]['mblog']['id']:
				print(curs[index]['text'])
				if tb.find_one({'uid':curs[index]['uid']}):
					curs[index]['delete']=1
					temp=curs[index]
					temp['delete']=1
				# tb.update({'uid':curs[index]['uid']},{'$set':temp})
			else:
				first=False
				flag+=1
			print(curs[index]['uid'],)
			index+=1

	client.close()

if __name__=='__main__':

	parse=argparse.ArgumentParser()
	parse.add_argument('-u','--uid',help="input uid")
	parse.add_argument('-n','--name',help="input table name")
	args=parse.parse_args()
	try:
		# a_json=load_weibo(args.url)
		parse_json(args.uid,args.name)
		time.sleep(10)
	except Exception as e:
		print(e)
		time.sleep(600)
