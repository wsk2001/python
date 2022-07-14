# Python으로 파일 다운로드

출처: https://stackabuse.com/download-files-with-python/

다른 온라인 리소스에서 파일을 다운로드하는 것은 웹에서 수행하는 가장 중요하고 일반적인 프로그래밍 작업 중 하나입니다. 파일 다운로드의 중요성은 수많은 성공적인 응용 프로그램을 통해 사용자가 파일을 다운로드 할 수 있다는 사실에서 강조 될 수 있습니다. 다음은 파일 다운로드가 필요한 몇 가지 웹 애플리케이션 기능입니다.

- File sharing
- Data mining
- Retrieving website code (CSS, JS, etc)
- Social media

이것은 떠오르는 응용 프로그램 중 일부에 불과하지만 더 많은 것을 생각할 수 있다고 확신합니다. 이 기사에서는 Python으로 파일을 다운로드 할 수있는 가장 널리 사용되는 몇 가지 방법을 살펴 보겠습니다.



## urllib.request 모듈 사용

urllib.request 모듈은 HTTP를 통해 파일을 열거 나 다운로드하는 데 사용됩니다. 특히이 모듈의 urlretrieve 메소드는 실제로 파일을 검색하는 데 사용할 것입니다.

이 메서드를 사용하려면 urlretrieve 메서드에 두 개의 인수를 전달해야합니다. 첫 번째 인수는 검색 할 리소스의 URL이고 두 번째 인수는 다운로드 한 파일을 저장할 로컬 파일 경로입니다.

다음 예를 살펴 보겠습니다.

``` python
import urllib.request

print('Beginning file download with urllib2...')

url = 'http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg'
urllib.request.urlretrieve(url, '/Users/scott/Downloads/cat.jpg')
```

위의 코드에서 먼저 urllib.request 모듈을 가져옵니다. 다음으로 다운로드 할 파일의 경로를 포함하는 변수 url을 만듭니다. 마지막으로 urlretrieve 메소드를 호출하고 파일 대상에 대한 두 번째 매개 변수로 '/Users/scott/Downloads/cat.jpg'라는 첫 번째 인수로 url 변수를 전달합니다. 두 번째 매개 변수로 파일 이름을 전달할 수 있으며 올바른 권한이 있다고 가정하면 파일이 가질 위치와 이름입니다.

위 스크립트를 실행하고 '다운로드'디렉토리로 이동합니다. 다운로드 한 'cat.jpg'파일이 표시됩니다.

**Note**:  이 urllib.request.urlretrieve는 Python 3에서 '레거시 인터페이스'로 간주되며 향후 언젠가는 사용되지 않을 수 있습니다. 이 때문에 아래 방법 중 하나를 선호하여 사용하지 않는 것이 좋습니다. Python 2에서 인기가 있기 때문에 여기에 포함했습니다.



## Urllib2 모듈 사용

Python에서 파일을 다운로드하는 또 다른 방법은 urllib2 모듈을 사용하는 것입니다. urllib2 모듈의 urlopen 메소드는 파일 데이터를 포함하는 객체를 반환합니다. 내용을 읽으려면

Python 3에서 urllib2는 urllib.request 및 urllib.error로 urllib에 병합되었습니다. 따라서이 스크립트는 Python 2에서만 작동합니다.

``` python
import urllib2

filedata = urllib2.urlopen('http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg')
datatowrite = filedata.read()
 
with open('/Users/scott/Downloads/cat2.jpg', 'wb') as f:
    f.write(datatowrite)
```

open 메서드는 로컬 파일 경로와 데이터가 기록되는 모드라는 두 개의 매개 변수를받습니다. 여기서 'wb'는 open 메소드가 주어진 파일에 바이너리 데이터를 쓸 수있는 권한이 있어야 함을 나타냅니다.

위의 스크립트를 실행하고 'Downloads'디렉토리로 이동하십시오. 다운로드 한 pdf 문서가 'cat2.jpg'로 표시되어야합니다.



## requests Module 사용

requests 모듈을 사용하여 파일을 다운로드 할 수도 있습니다. requests 모듈의 get 메소드는 바이너리 형식으로 파일 내용을 다운로드하는 데 사용됩니다. 그런 다음 이전 메소드 인 urllib2.urlopen에서했던 것처럼 open 메소드를 사용하여 시스템에서 파일을 열 수 있습니다.

다음 스크립트를 살펴보십시오.

``` python
import requests

print('Beginning file download with requests')

url = 'http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg'
r = requests.get(url)

with open('/Users/scott/Downloads/cat3.jpg', 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)
```

위의 스크립트에서 open 메소드는 로컬 파일에 바이너리 데이터를 쓰기 위해 다시 한 번 사용됩니다. 위의 스크립트를 실행하고 'Downloads'디렉토리로 이동하면 새로 다운로드 한 'cat3.jpg'라는 이름의 JPG 파일이 표시됩니다.

requests 모듈을 사용하면 상태 코드, 헤더 등을 포함하여 요청에 대한 관련 메타 데이터를 쉽게 검색 할 수도 있습니다. 위의 스크립트에서이 메타 데이터에 액세스하는 방법을 볼 수 있습니다.

HTTP GET 요청에 필요한 추가 매개 변수도 마찬가지입니다. 예를 들어 고객 헤더를 추가해야하는 경우 헤더로 dict를 만들고 get 요청에 전달하기 만하면됩니다.

``` python
headers = {'user-agent': 'test-app/0.0.1'}
r = requests.get(url, headers=headers)
```

이 라이브러리에는 더 많은 옵션과 기능이 있으므로 사용 방법에 대한 자세한 정보는 훌륭한 사용자 안내서를 확인하십시오.



## wget Module 사용

Python에서 파일을 다운로드하는 가장 간단한 방법 중 하나는 wget 모듈을 사용하는 것이므로 대상 파일을 열 필요가 없습니다. wget 모듈의 다운로드 방법은 한 줄로 파일을 다운로드합니다. 이 메서드는 다운로드 할 파일의 URL 경로와 파일을 저장할 로컬 경로의 두 가지 매개 변수를 허용합니다.

``` python
import wget

print('Beginning file download with wget module')

url = 'http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg'
wget.download(url, '/Users/scott/Downloads/cat4.jpg')
```

위의 스크립트를 실행하고 '다운로드'디렉토리로 이동합니다. 여기에 새로 다운로드 한 'cat4.jpg'파일이 표시됩니다.



## Conclusion

이 기사에서는 Python에서 파일을 다운로드하는 데 가장 일반적으로 사용되는 네 가지 방법을 제시했습니다. 개인적으로 저는 단순성과 성능의 조합으로 인해 파일 다운로드를 위해 요청 모듈을 사용하는 것을 선호합니다. 그러나 프로젝트에 타사 라이브러리를 사용하지 못하게하는 제약 조건이있을 수 있습니다.이 경우 urllib2 모듈 (Python 2 용) 또는 urllib.request 모듈 (Python 3 용)을 사용합니다.

어떤 라이브러리를 선호하며 그 이유는 무엇입니까? 댓글로 알려주세요!

