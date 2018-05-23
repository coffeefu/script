import asyncio
import pymongo
import aiohttp
import json
async def find_followers_fans(uid):
	her_follow_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_" + \
        uid+"&since_id="
	client=pymongo.MongoClient()
	db=client.weibo
	tb=db.test_count
	s = aiohttp.ClientSession()
	r = await s.get(her_follow_url+'1')
	test = {}
	a_json = json.loads(await r.text())
	a_page = 1
	if not a_json.__contains__('msg'):    
		followers_info = a_json["data"]["cards"][-1]['card_group']
	else:
		return test
	while not a_json.__contains__('msg'):
	    followers_info = a_json["data"]["cards"][-1]['card_group']
	    for follower in followers_info:
	        show_me = follower["desc1"]
	        name = follower["user"]["screen_name"]
	        uid = follower["user"]["id"]
	        followers_count = follower['user']['followers_count']
	        follow_count = follower['user']['follow_count']
	        print(show_me, name, uid, follow_count, followers_count)
	        test[uid]=1
	        tb.insert_one({'name':name,'uid':uid,'show_me':show_me,'follow_count':follow_count,'followers_count':followers_count})
	    print('现在是第几页',a_page)
	    a_page += 1
	    a_json_url = her_follow_url+str(a_page)
	    r = await s.get(a_json_url)
	    a_json = json.loads(await r.text())
	await s.close()
	client.close()


loop=asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([find_followers_fans('2671109275')]))