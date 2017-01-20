# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
from weibo import APIClient
import requests
import bs4
from urllib import urlretrieve

def getmusic():
	url = 'http://music.163.com/discover'
	header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
	/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
	s = requests.session()

	try:
		print 'Get music now'
		htmllist = s.get(url,headers=header)
		bsObjlist = bs4.BeautifulSoup(htmllist.text,'html.parser')
		ls = bsObjlist.find_all('div',{'class':'u-cover u-cover-1'})
		count = 0
		templist = []
		while(count < 8):
			picurl = ls[count].find('img').attrs['src']
			picurl = picurl.split('param')[0] + 'param=400y400'
			title  = ls[count].find('a',{'class':'msk'}).attrs['title']
			aurl   = 'http://music.163.com' + ls[count].find('a',{'class':'msk'}).attrs['href']
			temp   = [picurl,title,aurl]
			templist.append(temp)
			count += 1

		return templist
	except Exception as e:
		print e
		pass
	
def getTitleList(templist):
	tlist = []
	for item in templist:
		tlist.append(item[1])
	return tlist

def get_access_token(app_key, app_secret, callback_url):  
	client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=callback_url)  

	auth_url = client.get_authorize_url()  
	print auth_url  
	  
	code = raw_input("Input code:")  
	r = client.request_access_token(code)  
	access_token = r.access_token  
	expires_in = r.expires_in  
	print 'access_token:',access_token  
	print 'expires_in:', expires_in  
  
	return access_token, expires_in  


if __name__ == '__main__':
	app_key = '3828611682'  
	app_secret = '905036e24f75c47147da46b0df9e04c0'  
	callback_url = 'https://api.weibo.com/oauth2/default.html'  
	access_token, expires_in = get_access_token(app_key, app_secret, callback_url) 

	client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=callback_url)  
	client.set_access_token(access_token, expires_in) 
	musiclist = []
	print 'start'
	while True:
		try:
			templist = getmusic()
			for item in templist:
				if not item[1] in musiclist:
					print 'try to send ' + item[1]
					try:
						urlretrieve(item[0],'temp.jpg')
						str = item[1] + item[2]
						f = open('temp.jpg', 'rb')  
						r = client.statuses.upload.post(status=str, pic=f)	
						f.close()
						print 'send ' + item[1] + ' successfully!'
						print 'sleep for 30s'
						print ' '
					except Exception as e:
						print e
						pass
					time.sleep(30)
				else:
					print item[1] + '  repeated!'
			musiclist = getTitleList(templist)
			print 'sleep for 200s'
			print ' '
			time.sleep(200)
		except Exception as e:
			print e
			pass

	 