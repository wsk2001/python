# 파이썬 Web Scraping

​	출처: http://pythonstudy.xyz/python/article/403-%ED%8C%8C%EC%9D%B4%EC%8D%AC-Web-Scraping

#### 1. 파이썬 Web Scraping

웹사이트에서 HTML을 읽어와 필요한 데이타를 긁어오는 것을 Web Scraping이라 한다. 이 과정은 크게 웹페이지를 읽어오는 과정과 읽어온 HTML 문서에서 필요한 데이타를 뽑아내는 과정으로 나뉠 수 있다.

웹페이지를 읽어오는 일은 여러 모듈을 사용할 수 있는데, 파이썬에서 기본적으로 제공하는 urllib, urllib2 을 사용하거나 편리한 HTTP 라이브러리로 많이 쓰이고 있는 [requests](http://docs.python-requests.org/en/latest/index.html) 를 설치해 사용할 수 있다. 만약 기존 코드를 유지보수하는 일이 아니라면 requests 를 사용할 것을 권장한다.

#### 2. requests - 웹페이지 읽어오기

HTTP 라이브러리인 requests를 사용하기 위해서는 먼저 아래와 같이 pip을 이용하여 requests 패키지를 설치한다.

```
pip install requests
```

기본적인 requests 기능을 먼저 살펴보면, requests는 HTTP GET, POST, PUT, DELETE 등을 사용할 수 있으며, 편리한 데이타 인코딩 기능을 제공하고 있다. 즉, 데이타를 Dictionary로 만들어 GET, POST 등에서 사용하면 필요한 Request 인코딩을 자동으로 처리해 준다.

``` python
import requests
 
# GET
resp = requests.get('http://httpbin.org/get')
print(resp.text)
 
# POST
dic = {"id": 1, "name": "Kim", "age": 10}
resp = requests.post('http://httpbin.org/post', data=dic)
print(resp.text)
 
resp = requests.put('http://httpbin.org/put')
resp = requests.delete('http://httpbin.org/delete')    
```

requests.get(url) 함수를 사용하면 해당 웹페이지 호출 결과를 가진 Response 객체를 리턴한다. Response 객체는 HTML Response와 관련된 여러 attribute들을 가지고 있는데, 예를 들어, Response의 status_code 속성을 체크하여 HTTP Status 결과를 체크할 수 있고, Response 에서 리턴된 데이타를 문자열로 리턴하는 text 속성이 있으며, Response 데이타를 바이트(bytes)로 리턴하는 content 속성 등이 있다. 또한, 만약 Response에서 에러가 있을 경우 프로그램을 중단하도록 할 때는 Response 객체의 raise_for_status() 메서드를 호출할 수 있다.
아래 예제는 다음 홈페이지에 접속해서 HTML 문서를 가져와 화면에 출력하는 예이다.

``` python
import requests
 
resp = requests.get( 'http://daum.net' )
# resp.raise_for_status()
 
if (resp.status_code == requests.codes.ok):
    html = resp.text
    print(html)
```



### requests 에서의 한글 깨짐 문제

여기서 간혹 겪게되는 한글 깨짐 문제에 대해 잠깐 집고 넘어가자. requests 에서 웹 호출을 진행한 후 결과는 Response 객체에 담기게 되는데, Response의 text 속성은 str 클래스 타입으로서 보통 requests 모듈에서 자동으로 데이타를 인코딩해 준다. 즉, requests는 HTTP 헤더를 통해 결과 데이타의 인코딩 방식을 추측하여 Response 객체의 encoding 속성에 그 값을 지정하고, text 속성을 엑세스할 때 이 encoding 속성을 사용한다. 만약 인코딩 방식을 변경해야 한다면, text 속성을 읽기 전에 Response의 encoding 속성을 변경하면 된다.

이제 실제 예를 들어 보면, 네이버 홈페이지는 한글 출력에 문제가 없지만, 네이버 증권사이트 웹페이지는 (영문 OS에서 테스트한 결과) 한글이 깨져 보이게 된다. 원인을 찾아보기 위해 Response 객체가 어떤 인코딩인지 체크해 보았다. 네이버 홈페이지는 UTF-8을 사용하고, 네이버 증권사이트는 ISO-8859-1을 사용하고 있다.

``` bash
>>> resp = requests.get('http://naver.com') # 네이버 홈
>>> resp.encoding
'UTF-8'
>>> resp = requests.get('http://finance.naver.com') # 증권
>>> resp.encoding
'ISO-8859-1'
```

인코딩이 유니코드 인코딩(예: UTF-8 등)이거나 한글 인코딩(예: EUC-KR)이면 일반적으로 한글이 깨지지 않지만, ISO-8859-1와 같이 영문 인코딩이면 한글이 깨지게 된다. 이를 해결하는 방법은 미리 Response 객체의 encoding 을 한글인코딩(예: EUC-KR)이나 None (인코딩 추즉을 하지 않도록) 으로 지정한 후, text 속성을 읽으면 된다. 예를 들어, 아래 예제는 네이버 증권사이트의 ISO-8859-1 인코딩 문제를 처리한 코드이다.

``` python
import requests
 
resp = requests.get('http://finance.naver.com/')
resp.raise_for_status()
 
resp.encoding=None   # None 으로 설정
#resp.encoding='euc-kr'  # 한글 인코딩
 
html = resp.text
print(html)
```



## 3. BeautifulSoup - 웹페이지 파싱

웹페이지 HTML 문서를 파싱(Parsing)하기 위해서는 BeautifulSoup 라는 모듈을 사용할 수 있다. 먼저 BeautifulSoup 를 아래와 같이 설치한다.

```
pip install beautifulsoup4
```

BeautifulSoup를 사용하기 위해서는 먼저 BeautifulSoup 모듈을 import하여야 하는데 모듈명은 bs4 이다. bs4 모듈이 import 된 후, bs4.BeautifulSoup(HTML문서) 생성자를 호출하여 BeautifulSoup 객체를 생성한다.

``` python
import bs4
 
html = "<html><body>...생략...</body></html>"
bs = bs4.BeautifulSoup(html, 'html.parser')
```

BeautifulSoup 객체에서 특정 HTML 태그(들)을 찾기 위해 select() 메서드를 사용하는데, 이 메서드의 파라미터로 어떤 태크(들)을 찾을 지를 CSS 스타일의 Selector로 지정하면 된다. 예를 들어, select('.news li') 는 news 라는 CSS 클래스 안이 모든 li 태그들을 리턴하게 된다.

리턴된 결과는 태그(s4.element.Tag)들의 리스트(list) 인데, 각 태그 요소(bs4.element.Tag)로부터 태그내 문자열을 리턴하기 위해서는 getText()를, 특정 태그 attribute를 얻기 위해서는 get('attribute명') 메서드 등을 사용할 수 있다.

아래 예제는 네이버 증권사이트에서 주요 Top 뉴스 제목을 발췌하는 코드이다.

``` python
# -*- coding: utf-8 -*-
 
import requests, bs4
 
resp = requests.get('http://finance.naver.com/')
resp.raise_for_status()
 
resp.encoding='euc-kr'
html = resp.text
 
bs = bs4.BeautifulSoup(html, 'html.parser')
tags = bs.select('div.news_area h2 a') # Top 뉴스
title = tags[0].getText()
print(title)
```

