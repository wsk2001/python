# Flask 로 간단한 HTTPS REST API 제공 및 테스트

출처: http://mcchae.egloos.com/v/11143246



예전 [파이썬의 웹 프레임워크](http://mcchae.egloos.com/11064660)를 살펴본 적이 있습니다.

최근에 아주 간단하게 REST API를 꾸미는데 어떤
파이썬 프레임워크가 좋을지 살펴보다가 Flask 로 구성을 해 보기로 하였습니다.

우선 설치는 다음과 같이 간단합니다.

``` sh
sudo pip install Flask
sudo pip install --upgrade --force-reinstall flask_restful
```


실제 작성하는 뼈대도 무척 간단합니다.

``` py
##########################################################################################
from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from flask import request
##########################################################################################
app = Flask(__name__)
api = Api(app)
##########################################################################################
class ZoneInfo(Resource):
    def get(self):
        return { result: [] }
##########################################################################################
api.add_resource(ZoneInfo, '/zoneInfo')
##########################################################################################
if __name__ == '__main__':
    logger.info("Start RestAPI : listen %s:%s" % ('127.0.0.1', 8443))
    app.run(
        host='127.0.0.1',
        port=8443,
    )
```



그런데 만약 UserAuth 라는 기능이 있어, 사용자 인증을 하고 필요에 따라 password를 입력해야 한다고 할 때, HTTPS 프로토콜을 사용하여야 하고, 또, GET이 아니라 Form에 넣어 POST 방식으로 넣어야 URL에도 패러키터 정보도 바로 보이지 않습니다.  우선 위와 같은 경우, HTTPS 통신을 위한 사설 인증서 *.key, *crt 파일이 필요합니다. 다음과 같은 방법으로 인증서(키)를 만듦니다.

``` bash
#!/bin/bash
KCNAME=future
openssl genrsa 2048 > $KCNAME.key
chmod 400 $KCNAME.key
openssl req -new -x509 -nodes -sha1 -days 365 -key $KCNAME.key > $KCNAME.crt
```



이제는 Flask에 SSL을 사용하도록 수정해야 하는데,

``` py
from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('future.key')
context.use_certificate_file('future.crt')

##########################################################################################
if __name__ == '__main__':
    logger.info("Start RestAPI : listen %s:%s" % ('127.0.0.1', 8443))
    app.run(
        host='127.0.0.1',
        port=8443,
        debug = True,
        ssl_context=context,
    )
```

와 같이 주면 됩니다. 이와 같이 하여 [해당 소스 ](https://gist.github.com/mcchae/39febe806c3065064ad7)처럼 작성한 다음 동작시키면 됩니다.

이를 테스트 하기 위해서는 curl 프로그램을 이용해도 되지만, 파이썬 으로 직접 RESTFUL API 를 작성해도 됩니다.

소스는 위의 소스 링크에 rest_test.py 에 있습니다. 이중 주의하여야 할 것은 form에 변수를 넣고 POST 메서드로 호출하는 경우입니다.



``` py
##########################################################################################
def userAuth(host, port, userid, credential):
    params = urllib.urlencode({'userid': userid, 'passwd': credential})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPSConnection(host=host, port=port)
    conn.request("POST", "/userAuth", params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    rdict = json.loads(data)
    return rdict

```

위와 같은 방법으로 호출하면 됩니다.



추가된 사항:

최근 (2015년 3월) 에 

CentOS 5.11에서 작업을 해 보는데 최신 pyOpenSSL 을 설치해서는 다음과 같이  플래스크 테스트를 구축해야 https 환경이 구축되었습니다.

참고하십시오.

``` py
	app = Flask(__name__)
	api = Api(app)
	api.add_resource(Users, '/api/Users')
	api.add_resource(ServerFarms, '/api/ServerFarms')

	from OpenSSL import SSL
	context = SSL.Context(SSL.SSLv3_METHOD)## SSL.Context(SSL.SSLv23_METHOD)
	cert = 'future.crt'
	pkey = 'future.key'
	context.use_privatekey_file(pkey)
	context.use_certificate_file(cert)
	app.run(host=host, port=port, ssl_context=(cert, pkey), threaded=True, debug=True)
```

만약

AttributeError: 'Context' object has no attribute 'wrap_socket'

오류가 발생하면 

``` py
	context = SSL.Context(SSL.SSLv3_METHOD)## SSL.Context(SSL.SSLv23_METHOD)
	cert = 'future.crt'
	pkey = 'future.key'
	context.use_privatekey_file(pkey)
	context.use_certificate_file(cert)
```

대신 

``` py
        context = (cert, pkey)
```

라고 하면 됩니다.

어느 분께는 도움이 되셨기를...



`rest_api.py`

``` py
#!/usr/bin/env python
#coding=utf8
##########################################################################################
import os
import logging
import logging.handlers
import traceback
from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from flask import request

##########################################################################################
def getLogger(logname, logdir, logsize=500*1024, logbackup_count=4):
	if not os.path.exists(logdir):
		os.makedirs(logdir)
	logfile='%s/%s.log' % (logdir, logname)
	loglevel = logging.INFO
	logger = logging.getLogger(logname)
	logger.setLevel(loglevel)
	if logger.handlers is not None and len(logger.handlers) >= 0:
		for handler in logger.handlers:
			logger.removeHandler(handler)
		logger.handlers = []
	loghandler = logging.handlers.RotatingFileHandler(
		logfile, maxBytes=logsize, backupCount=logbackup_count)
	formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
	loghandler.setFormatter(formatter)
	logger.addHandler(loghandler)
	return logger

##########################################################################################
logger = getLogger('restapi', '/tmp/restapi')

##########################################################################################
app = Flask(__name__)
api = Api(app)

from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('future.key')
context.use_certificate_file('future.crt')

##########################################################################################
class ZoneInfo(Resource):
	def get(self):
		logger.info("ZoneInfo.get start...")
		try:
			stmt = "select zone,ou,pool,in_ip,ex_ip FROM tm_zone"
			dlist = [
				{'id':1, 'zone':'서울'},
				{'id':2, 'zone':'대전'},
				{'id':3, 'zone':'부산'},
			]
			rd = {
				'result':dlist
			}
			return rd
		except Exception, e:
			logger.error('ZoneInfo.get: Error: %s: %s' % (e, traceback.format_exc()))
			rd = {
				'result':[]
			}
			return rd
		finally:
			rdstr = str(rd)
			if len(rdstr) > 1024:
				rdstr = rdstr[:1024] + '...'
			logger.info("ZoneInfo.get return: %s" % rdstr)

##########################################################################################
class UserList(Resource):
	def get(self, tm_id):
		logger.info("UserList.get start... tm_id=<%s>" % tm_id)
		try:
			tm_id = tm_id.encode('utf-8')
			dlist = [
				{'id':11, 'userid':'kdkim'},
				{'id':22, 'userid':'kdhong'},
			]
			rd = {
				'result':dlist
			}
			return rd
		except Exception, e:
			logger.error('UserList.get: Error: %s: %s' % (e, traceback.format_exc()))
			rd = {
				'result':[]
			}
			return rd
		finally:
			rdstr = str(rd)
			if len(rdstr) > 1024:
				rdstr = rdstr[:1024] + '...'
			logger.info("UserList.get return: %s" % rdstr)

##########################################################################################
# UserList : get list of TMES master rows which is matching pool_tm_id
class UserAuth(Resource):
	def post(self):
		rd = { 'result': False }
		logger.info("UserAuth.get start...")
		if not (request.form.has_key('userid') and request.form.has_key('passwd')):
			logger.error('UserAuth.get: Error: invalid POST form of request (userid, passwd)')
			return rd
		userid = request.form['userid'].encode('utf-8')
		passwd = request.form['passwd'].encode('utf-8')
		try:
			# authenticate
			authenticated = userid != 'invalid'
			rd = {
				'result': authenticated,
			}
			return rd
		except Exception, e:
			logger.error('UserAuth.get: Error: %s: %s' % (e, traceback.format_exc()))
			rd = { 'result': False }
			return rd
		finally:
			rdstr = str(rd)
			if len(rdstr) > 1024:
				rdstr = rdstr[:1024] + '...'
			logger.info("UserAuth.get return: %s" % rdstr)

##########################################################################################
## Actually setup the Api resource routing here
##########################################################################################
api.add_resource(UserAuth, '/userAuth')
api.add_resource(ZoneInfo, '/zoneInfo')
api.add_resource(UserList, '/userList/<string:tm_id>')

##########################################################################################
if __name__ == '__main__':
	logger.info("Start RestAPI : listen %s:%s" % ('127.0.0.1', 8443))
	app.run(
		host='127.0.0.1',
		port=8443,
		debug = True,
		ssl_context=context,
	)
```



`rest_test.py`

``` py
__author__ = 'future'

##########################################################################################
import sys
import json
import httplib
import urllib

##########################################################################################
def userAuth(host, port, userid, credential):
	params = urllib.urlencode({'userid': userid, 'passwd': credential})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPSConnection(host=host, port=port)
	conn.request("POST", "/userAuth", params, headers)
	response = conn.getresponse()
	# print response.status, response.reason
	data = response.read()
	conn.close()
	rdict = json.loads(data)
	return rdict

##########################################################################################
def zoneInfo(host, port):
	getstr='/zoneInfo'
	import httplib
	conn = httplib.HTTPSConnection(host=host, port=port)
	conn.request("GET", getstr)
	response = conn.getresponse()
	#print response.status, response.reason
	if response.status != 200:
		sys.stderr.write("Error: %s" % response.reason)
		return 0
	data = response.read()
	rdict = json.loads(data)
	return rdict

##########################################################################################
def userList(host, port, tm_id):
	getstr='/userList/%s' % tm_id
	import httplib
	conn = httplib.HTTPSConnection(host=host, port=port)
	conn.request("GET", getstr)
	response = conn.getresponse()
	#print response.status, response.reason
	if response.status != 200:
		sys.stderr.write("Error: %s" % response.reason)
		return 0
	data = response.read()
	rdict = json.loads(data)
	return rdict

##########################################################################################
def test():
	import pprint
	host = '127.0.0.1'
	port = 8443

	# userAuth
	print ">>> Invalid userAuth('invalid', '1234')"
	print userAuth(host, port, 'invalid', '1234')
	print ">>> Valid userAuth('nkkang', '2134')"
	print userAuth(host, port, 'nkkang', '2134')
	print ">>> Valid userAuth('kdhong', '2134')"
	print userAuth(host, port, 'kdhong', '2134')

	# zoneInfo
	print ">>> zoneInfo()"
	pprint.pprint(zoneInfo(host, port))

	# userList
	print ">>> userList('1')"
	print userList(host, port, 1)
	print ">>> userList('2')"

##########################################################################################
if __name__ == '__main__':
	test()

```

