# Beautiful Soup(뷰티플 수프) 사용법과 예제

출처: https://twpower.github.io/84-how-to-use-beautiful-soup



## 환경 및 선수조건

- HTML, CSS, Javascript
- Python
- pip



## Beautiful Soup 설치

``` sh
$ pip install beautifulsoup4
```



## Beautiful Soup 사용법

### 기본 세팅

기본적으로 패키지 import를 통해서 가져오며 `html파일`을 가져오거나 `urllib` 혹은 `requests` 모듈을 통해서 직접 웹에서 소스를 가져올 수도 있습니다.

#### package import

``` py
from bs4 import BeautifulSoup
```



#### `html` 파일 열기

```py
with open("example.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
```



#### `urllib`를 통해서 웹에 있는 소스 가져오기

- `web_url`에 원하는 `URL`을 추가

```py
import urllib.request
import urllib.parse

# web_url에 원하는 웹의 URL을 넣어주시면 됩니다.
with urllib.request.urlopen(web_url) as response:
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
```



#### `requests`를 통해서 웹에 있는 소스 가져오기

- `web_url`에 원하는 `URL`을 추가

```sh
import requests

# web_url에 원하는 웹의 URL을 넣어주시면 됩니다.
>>> r = requests.get(web_url)
>>> r.status_code
200
>>> r.headers['content-type']
'text/html; charset=UTF-8'
>>> r.encoding
'UTF-8'
>>> r.text
<!DOCTYPE html>
<html class="client-nojs" lang="en" dir="ltr">
```



### HTML 예제

- 아래 html 코드를 통해서 예제를 설명

**example.html**

```html
<!DOCTYPE html>
<html>
	<head>
		<title>Page title</title>
	</head>
	<body>
    	<div>
            <p>a</p>
            <p>b</p>
            <p>c</p>
        </div>
        <div class="ex_class">
            <p>d</p>
            <p>e</p>
            <p>f</p>
        </div>
        <div id="ex_id">
            <p>g</p>
            <p>h</p>
            <p>i</p>
        </div>
		<h1>This is a heading</h1>
		<p>This is a paragraph.</p>
		<p>This is another paragraph.</p>
	</body>
</html>
```



### find() 및 find_all()함수

- 함수 인자로는 찾고자 하는 태그의 이름, 속성 기타 등등이 들어간다.
- `find_all(name, attrs, recursive, string, limit, **kwargs)`
- `find(name, attrs, recursive, string, **kwargs)`

#### find_all

- find_all(): 해당 조건에 맞는 모든 태그들을 가져온다.

```sh
with open("example.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    all_divs = soup.find_all("div")
    print(all_divs)
# 출력 결과
[<div>
<p>a</p>
<p>b</p>
<p>c</p>
</div>, <div class="ex_class">
<p>d</p>
<p>e</p>
<p>f</p>
</div>, <div id="ex_id">
<p>g</p>
<p>h</p>
<p>i</p>
</div>]
```

#### find

- find(): 해당 조건에 맞는 하나의 태그를 가져온다. 중복이면 가장 첫 번째 태그를 가져온다.

```sh
with open("example.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    first_div = soup.find("div")
    print(first_div)
# 출력 결과
<div>
<p>a</p>
<p>b</p>
<p>c</p>
</div>
```



### 태그를 이용해서 가져오기

- 예제: 모든 `<p>` 태그들을 가져오기

```sh
with open("example.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    all_ps = soup.find_all("p")
    print(all_ps)
# 출력 결과
[<p>a</p>, <p>b</p>, <p>c</p>, <p>d</p>, <p>e</p>, <p>f</p>, <p>g</p>, <p>h</p>, <p>i</p>, <p>This is a paragraph.</p>, <p>This is another paragraph.</p>]
```

- 예제: 첫번째 `<div>`태그를 가져오기

```sh
with open("example.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    first_div = soup.find("div")
    print(first_div)
# 출력 결과
<div>
<p>a</p>
<p>b</p>
<p>c</p>
</div>
```



### 태그와 속성을 이용해서 가져오기

태그와 속성을 이용할 때 함수의 인자로 원하는 태그를 첫번째 인자로 그 다음에 `속성:값`의 형태로 `dictionary` 형태로 만들어서 넣어주면 된다.

- `find_all('태그명', {'속성명': '값' ...})`
- `find('태그명', {'속성명': '값' ...})`
- 예제: `<div>` 태그에서 `id`속성의 값이 `ex_id`인거 불러오기

```sh
with open("example.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    ex_id_divs = soup.find('div', {'id': 'ex_id'})
    print(ex_id_divs)
# 출력 결과
<div id="ex_id">
<p>g</p>
<p>h</p>
<p>i</p>
</div>
```



### HTML 구조를 이용해 부분부분 가져오기

- 예제: `id`속성의 값이 `ex_id`인 `<div>` 태그에서 `<p>`태그들만 가져오기

```sh
with open("example.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    # id=ex_id인 div 태그를 가져와서
    ex_id_divs = soup.find("div", {"id":"ex_id"})
    # 그 태그들 안에서 p 태그를 가져온다.
    all_ps_in_ex_id_divs = ex_id_divs.find_all("p")
    print(all_ps_in_ex_id_divs)
# 출력 결과
[<p>g</p>, <p>h</p>, <p>i</p>]
```



### -끝-

