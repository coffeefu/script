from PIL import Image,ImageDraw,ImageFont
from random import choice
import win32api,win32con,win32gui
import os,pymongo
import servicemanager
import sys
def add_text(texts,nums):
	cgs=os.listdir('white')
	if 'desktop.png' in cgs:
		cgs.remove('desktop.png')
	a_url=os.getcwd()+'/white/'+choice(cgs)
	ttfont = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf",35) 
	im = Image.open(a_url)  
	draw = ImageDraw.Draw(im)  
	for index,text in enumerate(texts):
		draw.text((200, 115+index*45), text+str(nums[index]), (28, 28, 28), font=ttfont)
	im.save(os.getcwd()+'/white/'+'desktop.png')

def change_desktop_img():
	bmp_path=os.getcwd()+'/white/'+'desktop.png'
	reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
	win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "10")
	win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
	win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmp_path, win32con.SPIF_SENDWININICHANGE)


def get_text():
	client=pymongo.MongoClient()
	db=client.weibo
	tb=db.pmm
	count=tb.find().count()
	skip_count=count-8
	texts=[]
	nums=[]
	for cur in tb.find().skip(skip_count).limit(8):
		texts.append(cur['text'])
		nums.append(cur['comments_count'])
	client.close()
	return texts,nums



texts,nums=get_text()
add_text(texts,nums)
change_desktop_img()