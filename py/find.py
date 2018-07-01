#!/usr/bin/python3
import requests
import json
import pymongo
import aiohttp
import math
import time
import asyncio
followers_url="https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{}&type=all&page={}"
fans_url="https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{}&type=all&since_id={}"
s=aiohttp.ClientSession()
client=pymongo.MongoClient()
db=client.find
tb=db.lyy
client.close()
def find_followers(url,uid):
    users=[]
    page=1
    while 1:
        r=requests.get(url.format(uid,page))
        t=json.loads(r.text)
        if t.__contains__('msg'):
            break
        weibo=t['data']['cards'][-1]['card_group']
        page+=1
        if weibo:
            for item in weibo:
                users.append(item['user']['id'])
    return users

async def find_fans(url,uid):
    page=1
    while 1:
        r=await s.get(url.format(uid,page))
        t=json.loads(await r.text())
        if t.__contains__('msg'):
            break
        weibo=t['data']['cards'][-1]['card_group']
        page+=1
        if weibo:
            for item in weibo:
                # print(item['user']['id'])
                tb.insert({'name':item['user']['screen_name'],'uid':item['user']['id']})

# def test(url,uid):
#     page=1
#     while 1:
#         r=requests.get(url.format(uid,page))
#         t=json.loads(r.text)
#         if t.__contains__('msg'):
#             break
#         weibo=t['data']['cards'][-1]['card_group']
#         page+=1
#         if weibo:
#             for item in weibo:
#                 input(item)
#                 input(item['粉丝'])
#                 desc1=''
#                 if item.__contains__('desc1'):
#                     desc1=item['desc1']
#                 # print(item['user']['id'])
#                 tb.insert({'name':item['user']['screen_name'],'uid':item['user']['id'],'desc1':desc1})
if __name__=='__main__':
    client=pymongo.MongoClient()
    db=client.find
    tb=db.lyy
    all={}
    names={}
    for cur in tb.find():
        if cur['uid'] in all:
            all[cur['uid']]=all[cur['uid']]+1
        else:
            names[cur['uid']]=cur['name']
            all[cur['uid']]=1
    max=0
    test=[]
    for i in all.keys():
        if all[i]>max:
            print(i,all[i])
            max=all[i]
        if all[i]>30:
            print(i,all[i],names[i])
    print(test)

    # users=find_followers(followers_url,'2436332372')
    # for i in range(math.ceil(len(users)/3)):
    #     print(i*3/len(users))
    #     if i==math.ceil(len(users)/3)-1 and len(users)%3:
    #         task=[find_fans(fans_url,uid) for uid in users[i*3:i*3+len(users)%3]]
    #         loop=asyncio.get_event_loop()
    #         loop.run_until_complete(asyncio.wait(task))
    #     else:
    #         task=[find_fans(fans_url,uid) for uid in users[i*3:i*3+3]]
    #         loop=asyncio.get_event_loop()
    #         loop.run_until_complete(asyncio.wait(task))
    

    # users=find_followers(followers_url,'6138708048')
    # for i in range(math.ceil(len(users)/2)):
    #     print(i*2/len(users))
    #     task=[find_fans(fans_url,uid) for uid in users[i*2:i*2+2]]
    #     loop=asyncio.get_event_loop()
    #     loop.run_until_complete(asyncio.wait(task))
    #     # time.sleep(2)
    # s.close()
    # client.close()



    # test(fans_url,'2436332372')