# Django 강좌

출처: https://076923.github.io/posts/Python-Django-1/



## 제 1강 - 소개 및 설치

 **상위 목록:** [Python](https://076923.github.io/categories/#Python) **하위 목록:** [Django](https://076923.github.io/posts/#Django) **작성 날짜:** 2020-06-21 **읽는 데** 13 분 소요

###  Django란

`장고(Django)`는 Python 기반의 오픈 소스 웹 애플리케이션 프레임워크(Web Application Framework)입니다.

장고를 활용해 **UI**, **UX**와 관련된 `프론트엔트(Front-end)` 개발과 **Server**, **DB** 등과 관련된 `백엔드(Back-end)` 개발을 진행할 수 있습니다.

장고의 기본 구성은 `모델(Model)`, `템플릿(Template)`, `뷰(View)`로 **MTV 패턴**을 따릅니다.

`모델`은 데이터에 관한 정보**(저장, 접근, 검증, 작동 등)**를 처리하고 `논리 및 규칙`을 직접 관리합니다.

`템플릿`은 **데이터가 어떻게 표시**되는 지를 정의합니다. 템플릿은 사용자에게 실제로 보여지는 웹 페이지나 문서를 작성합니다.

`뷰`는 **어떤 데이터**를 표시할지 정의하며, `HTTP 응답 상태 코드(response)`를 반환합니다. 또한, **웹 페이지**, **리디렉션**, **문서** 등의 형태가 가능합니다.

즉, 데이터베이스에서 관리할 데이터를 정의(Model)하며, 사용자가 보는 화면(Template)과 애플리케이션의 처리 논리(View)를 정의합니다.

장고는 **Instagram, Disqus, Mozilla, Pinterest, Bitbucket** 등에서도 사용하고 있습니다.



### Django 설치

```
pip install django==3.0.7
```

`Django` 프레임워크는 `pip`를 통하여 설치할 수 있습니다.

본 강좌는 **Django 3.0.7**을 기반으로 작성돼 있습니다.

Django가 정상적으로 설치 되었다면, 아래의 구문으로 Django 설치 버전을 확인할 수 있습니다.



```
python -m django --version
```

- **결과**

  3.0.7  

Django 3.0 이상의 버전은 **Python 3.6**, **Python 3.7**, **Python 3.8**만 공식적으로 지원합니다.

만약, `Python 3.5` 등의 낮은 버전을 사용한다면 Django 2.2나 Django 2.1 등의 낮은 버전을 사용합니다.





### Django Rest Framework 설치

```
pip install djangorestframework==3.11.0
```

`Django`에는 **REST(Representational State Transfer)** API를 위한 프레임워크가 존재합니다.

이를 `DRF(Django REST Framework)`라고 합니다.

`DRF`는 `pip`를 통하여 설치할 수 있습니다.





### Rest API란?

`REST`란 **자원(Resource)**을 정의하고 자원에 대한 **주소(URL)**를 지정하는 방법을 의미합니다.

다음 여섯 가지 조건을 `REST`라고 하며 해당 조건을 지켜 설계된 API를 **Restful API**라고 합니다.

- **Uniform Interface (일관적인 인터페이스)** : HTTP 표준만 따른다면 어떤 언어, 어떤 플랫폼에서도 사용이 가능한 인터페이스 스타일
- **Client-Server (클라이언트-서버)** : 서버는 API를 제공하고, 클라이언트는 사용자 인증에 관련된 일들을 직접 관리
- **Stateless (무상태)** : 요청 간 클라이언트의 컨텍스트(context)가 서버에 저장되지 않음
- **Cacheable (캐시 처리 가능)** : 클라이언트는 응답을 캐싱할 수 있어야 함
- **Layerd System (계층화)** : 클라이언트는 대상 서버에 직접 연결되었는지, 중간 서버를 통해 연결되었는지를 알 수 없음, 중간 서버는 로드 밸런싱 기능이나 공유 캐시 기능을 제공함으로써 시스템 규모 확장성을 향상시킬 수 있음
- **Self-descriptiveness (자체 표현 구조)** : Rest API 메시지만 보고도 쉽게 이해할 수 있는 자체 표현 구조로 설계해야 함



- `자원(Resource)` : URI
- `행위(Verb)` : HTTP Method (POST, GET, PUT, DELTE)
- `표현(Representations)` : JSON, XML, TEXT, RSS 등 여러 형태로 응답
- `서버(Server)` : 자원을 가지고 있는 쪽
- `클라이언트(Client)` : 자원을 요청하는 쪽





### Django CORS 설치

```
pip install django-cors-headers==3.4.0
```

`CORS(Cross-Origin Resource Sharing)`란 교차 출처 리소스 공유라는 의미로 **실행 중인 웹 애플리케이션**이 다른 출처의 선택한 자원에 접근할 수 있는 권한을 부여하도록 브라우저에 알려주는 체제입니다.

즉, 외부에서 서버에 접속할 때 `CORS`가 허용되어있지 않다면 `CORS 오류`가 발생합니다.

이를 방지하기 위해 `Django`용 `CORS` 패키지를 설치합니다.



## 제 2강 - 프로젝트 생성

 **상위 목록:** [Python](https://076923.github.io/categories/#Python) **하위 목록:** [Django](https://076923.github.io/posts/#Django) **작성 날짜:** 2020-06-28 **읽는 데** 13 분 소요

### Django Project
장고(Django)를 원활하게 사용하기 위해선 기본 프로젝트 구성을 사용합니다.

기본 프로젝트를 사용할 폴더로 이동합니다.



```
django-admin startproject daehee .
```

`django-admin startproject [프로젝트 이름]`을 통해 장고 기본 프로젝트 생성이 가능합니다.

만약, `django-admin startproject [프로젝트 이름] .`의 형태로 온점(.)을 추가한다면 현재 디렉토리에서 생성합니다.

정상적으로 프로젝트가 생성된다면 아래의 디렉토리 구조로 폴더와 파일이 생성됩니다.



```
[현재 프로젝트]/
  ⬇ 📁 [장고 프로젝트 이름]
    🖹 __init__.py
    🖹 asgi.py
    🖹 settings.py
    🖹 urls.py
    🖹 wsgi.py
  🖹 manage.py
```

`[장고 프로젝트 이름]` : **django-admin startproject**로 생성한 프로젝트 이름입니다. 프로젝트 실행을 위한 Python 패키지가 저장됩니다.

`__init__.py` : 해당 폴더를 패키지로 인식합니다.

`asgi.py` : 현재 프로젝트를 서비스하기 위한 **ASGI(Asynchronous Server Gateway Interface)** 호환 웹 서버 진입점입니다.

`settings.py` : 현재 Django **프로젝트의 환경 및 구성**을 설정합니다.

`urls.py` : 현재 Django **프로젝트의 URL**을 설정합니다.

`wsgi.py` : 현재 프로젝트를 서비스하기 위한 **WSGI(Web Server Gateway Interface)** 호환 웹 서버의 진입점입니다.

`manage.py` : 현재 Django를 서비스를 실행시키기 위한 **커맨드라인의 유틸리티**입니다.



현재 프로젝트의 파일에서 가장 중요한 요소는 `settings.py`, `urls.py`, `manage.py` 입니다.

위 세 가지 파일 중, `manage.py`를 제외하고 직접 수정해 변경합니다.

- Tip : 일반적으로 `manage.py`은 수정하지 않습니다.





### Django Test RunServer

먼저 간단하게 `manage.py`를 활용해 Django 서버를 구동해보겠습니다.

`manage.py`가 존재하는 디렉토리로 이동합니다.

디렉토리 이동은 `cd [장고 프로젝트 이름]` 등으로 이동할 수 있습니다.



```
python manage.py runserver
```

- **결과**

  Watching for file changes with StatReloader Performing system checks…  System check identified no issues (0 silenced).  You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions. Run ‘python manage.py migrate’ to apply them. June 28, 2020 - 19:11:48 Django version 3.0.7, using settings ‘daehee.settings’ Starting development server at http://127.0.0.1:8000/ Quit the server with CTRL-BREAK. [28/Jun/2020 19:11:54] “GET / HTTP/1.1” 200 16351  

서버를 구동하게 되면 **파일 변경 사항**, **시스템 점검**, **마이그레이션 점검**, **설정 반영** 등을 통해 프로젝트를 실행시킵니다.

테스트 프로젝트는 `http://127.0.0.1:8000/`에서 확인할 수 있습니다.

해당 url로 이동해 서버가 정상적으로 구동되는지 확인합니다.

![img](https://076923.github.io/assets/posts/Python/Django/lecture-2/1.webp)

서버를 종료하려면, `Ctrl + C`키를 눌러 서버를 종료할 수 있습니다.

현재 포트는 `8000`에 연결되어 있습니다. 만약 포트를 변경하거나 외부접속을 허용한다면 다음과 같이 문장을 추가합니다.

- Tip : 기본 포트는 `8000`번에 연결되어 있습니다.



```
python manage.py runserver 8080
python manage.py runserver 0:8080
```

python manage.py runserver 뒤에 `8080`을 추가해 포트를 8080으로 변경할 수 있습니다.

python manage.py runserver 뒤에 `0:8080`을 추가해 외부 접속을 허용하고 포트를 8080으로 변경합니다.

- Tip : 모든 공용 IP 접속 허용은 `0`을 추가합니다. `0`은 `0.0.0.0`의 축약입니다.
- Tip : 외부 접속 허용시 `Settgins.py`에서 `ALLOWED_HOST=['*']`로 변경해야합니다.
- Tip : 마이그레이션 경고는 현재 사용하고 있는 데이터베이스에 반영되지 않아 나타나는 경고입니다.



## 제 3강 - 프로젝트 설정

 **상위 목록:** [Python](https://076923.github.io/categories/#Python) **하위 목록:** [Django](https://076923.github.io/posts/#Django) **작성 날짜:** 2020-07-04 **읽는 데** 49 분 소요

### Django setting.py 설정

장고(Django)의 환경 설정은 `setting.py` 파일에서 관리할 수 있습니다.

환경 설정에서 `데이터베이스`, `디버그 모드`, `허용 가능한 호스트`, `애플리케이션` `다국어 및 지역 시간` 등을 설정할 수 있습니다.

`settings.py` 파일의 설정이 올바르지 않거나, 필요한 구성이 누락되었다면 정상적으로 실행되지 않습니다.

장고의 기본적인 설정 파일의 구성은 다음과 같습니다.



```
"""
Django settings for daehee project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '비밀 키'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'daehee.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'daehee.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
```





### 기본 디렉토리 경로

```
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

기본 디렉토리 경로는 `BASE_DIR`로 나타냅니다.

`BASE_DIR`은 임의적으로 디렉토리 경로를 수정한 경우가 아니라면 수정하지 않습니다.





### 비밀 키

```
SECRET_KEY = '비밀 키'
```

`SECRET_KEY`는 **무작위의 50 글자**로 구성되어 있으며, `암호화 서명(Cryptographic signing)`, `쿠키 데이터 해시`, `유저의 비밀번호 초기화`, `일회성 비밀 URL 생성` 등에 사용됩니다.

`SECRET_KEY`는 노출되어서는 안되며, `SECRET_KEY` 키가 노출되었을 때는 **보안 기능이 상실**되므로, 새로운 `SECRET_KEY`를 사용해야 합니다.

`SECRET_KEY`의 값은 분리해서 사용하며, 크게 `환경 변수에 등록`하거나 `비밀 파일로 저장`해 사용합니다.



#### 비밀 키 분리 방법 (1)

```
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
```

환경 변수를 `.bash_profile`, `.profile` 에 등록해서 사용할 수 있습니다.

`Windows`의 경우에는 명령 프롬프트의 `set`에서 `Mac`이나 `Linux`는 터미널의 `export` 명령어로 등록할 수 있습니다.



#### 비밀 키 분리 방법 (2)

```
from keyfile import secret_key

SECRET_KEY = secret_key
```

간단하게 `*.py` 파일을 생성한 다음, 변수로 등록해 사용하거나, `json` 파일에 `SECRET_KEY` 값을 저장한당므 불러와 사용할 수 있습니다.

이때, `git`과 같은 버전관리 시스템을 사용한다면, `.gitignore`에 해당 파일을 추가해 저장되지 않도록 합니다.





### 디버그 모드

```
DEBUG = True
```

디버그 모드는 프로그램을 개발할 때 사용되는 모드입니다.

`True`로 설정되어 있다면, 특정 행동을 수행할 때마다 `로그(Log)`를 표시합니다.

로그를 표시하게 되므로, 모든 데이터가 노출될 수 있습니다.

개발이 완료되고 `운영` 서버 등에 배포할 때는 필히 디버그 모드를 `False`로 사용해야 합니다.





### 허용 가능한 호스트

```
ALLOWED_HOSTS = []
```

허용 가능한 호스트는 운영 서버 등에 배포하여, 서비스할 때 **호스트로 사용 가능한** `호스트` 또는 `도메인` 목록입니다.

서비스할 웹 사이트의 도메인이 등록되어 있지 않다면, `Bad Request (400)`를 반환합니다.

해당 기능은 `CSRF(Cross-site request forgery)`와 `HTTP 웹 서버 헤더 공격`을 막기 위한 조치입니다.

`DEBUG = True`일 때 동작하며, 기본적으로 `localhost`, `127.0.0.1`는 등록해 사용합니다.

또한, 서비스하는 도메인을 등록해야 정상적으로 동작합니다. 구성은 아래와 같이 사용할 수 있습니다.

```
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '076923.github.io']
```

`ALLOWED_HOSTS`에 로컬 호스트를 등록하지 않는다면, `CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False.`의 오류를 반환하며 `manage.py runserver`가 작동하지 않습니다.

- Tip : 모든 호스트를 허용한다면 `ALLOWED_HOSTS = ['*']`으로 설정합니다.





### 설치된 애플리케이션

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

현재 장고 프로젝트에 설치된 애플리케이션의 목록을 의미합니다.

애플리케이션을 등록하지 않는다면 서비스에서 사용할 수 없습니다.

현재 프로젝트는 `REST Framework`와 `CORS` 패키지를 등록할 예정이므로 아래와 같이 추가합니다.



#### 애플리케이션 등록

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    '앞으로 추가할 애플리케이션',
]
```

`rest_framework`와 `corsheaders`는 1강에서 설치한 `Django Rest Framework`와 `Django CORS`입니다.

해당 애플리케이션을 등록하지 않는다면, 장고 프로젝트에서 위의 기능을 사용할 수 없습니다.

`앞으로 추가할 애플리케이션`은 `startapp` 명령어를 통해 생성된 `Python` 모듈 파일을 의미합니다.

추가되는 애플리케이션은 모두 `INSTALLED_APPS` 목록에 추가해야합니다.

- Tip : `startapp` 명령어는 앞으로 배울 `앱 생성 강좌`에서 확인할 수 있습니다.



#### CORS 허용

```
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = False
 
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
 
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    '허용할 메서드',
)
     
CORS_ORIGIN_WHITELIST = (
    '허용할 URL',
)
```

`CORS`를 설정했다면, 위와 같은 내용을 추가합니다.

`CORS_ORIGIN_ALLOW_ALL`은 모든 사이트들의 HTTP 요청을 가능하게 합니다. 개발 중에는 `DEBUG`처럼 `True`로 사용합니다.

서비스 중인 서버에서는 `False`로 사용하고, `CORS_ORIGIN_WHITELIST`를 설정합니다.

`CORS_ALLOW_CREDENTIALS`은 쿠키가 사이트 간 HTTP 요청에 포함 허용 여부를 설정합니다.

`CORS_ALLOW_HEADERS`는 Access-Control-Allow-Headers를 포함하는 **예비 요청(preflight request)** 응답에 사용되는 헤더를 설정합니다.

허용되지 않는 헤더는 `CORS` 오류를 발생시킵니다. 자주 사용되는 **content-type**이나 **authorization** 등의 포함 여부를 확인합니다.

`CORS_ALLOW_METHODS`는 사용 가능한 **HTTP 메서드**를 설정합니다.

`CORS_ORIGIN_WHITELIST`는 사이트 간 요청을 허용하는 호스트 목록을 의미합니다.





### 미들웨어

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

`미들웨어(middleware)`란 운영 체제와 응용 소프트웨어의 중간에서 **조정**과 **중개**의 역할을 수행하는 소프트웨어입니다.

`데이터`, `애플리케이션 서비스`, `인증`, `API`를 관리합니다.

장고의 미들웨어는 장고에서 발생하는 `요청` 및 `응답` 처리에 연결되는 프레임워크입니다.



#### 미들웨어 등록

```
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

장고에서 `CORS`를 허용하기 위해서는 목록의 **가장 최상단**에 `CORS` 미들웨어를 등록해야 합니다.

추가적으로 등록되는 미들웨어는 `하단`에 등록해도 무방합니다.





### 루트 URL

```
ROOT_URLCONF = 'daehee.urls'
```

루트 URL 설정에 대한 Python 경로를 나타내는 문자열입니다.

루트 URL 경로 설정으로 장고 프로젝트의 `URL` 설정값을 가져와 등록합니다.





### 템플릿

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

장고는 웹 사이트에서 활용할 수 있으므로 `html` 코드 등과 연동하여 사용할 수 있습니다.

`BACKEND`는 사용할 템플릿 백엔드를 설정합니다. 아래와 같이 템플릿을 변경해 사용할 수 있습니다.

- ‘BACKEND’: ‘django.template.backends.django.DjangoTemplates’
- ‘BACKEND’: ‘django.template.backends.jinja2.Jinja2’

`DIRS`은 장고가 템플릿 소스 파일을 찾아야하는 디렉터리 경로입니다.

`APP_DIRS`은 장고가 설치된 애플리케이션에서 템플릿 소스 파일을 찾는 여부입니다.

`OPTIONS`는 템플릿 백엔드에 전달할 추가 매개 변수입니다. 사용 가능한 매개 변수는 템플릿 백엔드에 따라 달라집니다.



#### 템플릿 등록

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

템플릿을 사용하는 경우 `DIRS`에 템플릿이 저장된 경로를 등록합니다.

현재 프로젝트 경로의 `templates` 폴더에서 템플릿을 검색합니다.

만약, 템플릿을 사용하지 않는다면 등록하지 않아도 됩니다.





### WSGI 배포

```
WSGI_APPLICATION = 'daehee.wsgi.application'
```

현재 프로젝트를 서비스하기 위해 **WSGI(Web Server Gateway Interface)**의 경로를 의미합니다.

환경변수가 설정되지 않으면 프로젝트를 생성할 때 제공되는 `wsgi.py`의 설정값을 사용합니다.





### 데이터베이스 설정

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

기본값으로 `SQLite`가 설정되어 있으며, 특정 데이터베이스를 연동할 때 `DATABASE` 설정값을 변경합니다.

`ENGINE`은 데이터베이스의 엔진을 의미하며, `MySQL`이나 `PostgreSQL` 등을 연동할 수 있습니다.



#### MySQL 연동
```
pip install mysqlclient
```

`MySQL`을 연동하기 위해서는 `mysqlclient`을 설치합니다.

```
'ENGINE': 'django.db.backends.mysql'
```

설치가 완료된 후, `ENGINE` 값을 수정해 사용할 수 있습니다.



#### PostgreSQL 연동

```
pip install psycopg2
```

`PostgreSQL`을 연동하기 위해서는 `psycopg2`을 설치합니다.

```
'ENGINE': 'django.db.backends.postgresql'
```

설치가 완료된 후, `ENGINE` 값을 수정해 사용할 수 있습니다.



#### 데이터베이스 설정 수정

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': db_host,
        'PORT': db_port,
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
    }
}
```

데이터베이스를 연동시, `호스트(HOST)`, `포트(PORT)`, `이름(NAME)`, `유저(USER)`, `비밀번호(PASSWORD)`를 설정해야합니다.

`호스트(HOST)`는 데이터베이스의 **주소**입니다. 만약, 로컬에서 사용하고 있다면, `localhost`를 입력합니다.

`포트(PORT)`는 데이터베이스의 **포트 번호입**니다. 데이터베이스에서 사용하고 있는 포트 번호를 작성합니다.

`이름(NAME)`은 연동할 **데이터베이스의 이름**을 의미합니다. 사용할 데이터베이스의 이름을 입력합니다.

`유저(USER)`는 데이터베이스에 접속할 **계정 이름**을 의미합니다.

`비밀번호(PASSWORD)`는 접속할 데이터베이스에 설정된 **비밀번호**를 의미합니다.

데이터베이스 설정은 `SECRET_KEY`와 같이 별도로 관리해야 합니다.

데이터베이스의 값이 노출된다면, **보안 기능이 상실**되므로 큰 위험을 초래하게 됩니다.



#### 클라우드 데이터베이스 연동

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': daehee.076923.ap-northeast-2.rds.amazonaws.com,
        'PORT': 5432,
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
    }
}
```

AWS RDS와 같이 클라우드 환경의 데이터베이스와 장고를 연동할 수 있습니다.

클라우드 데이터베이스의 `엔드포인트`를 **호스트(HOST)**에 입력합니다.

클라우드 데이터베이스의 `포트`를 **포트(PORT)**에 입력합니다.

위의 예시와 같이 연동해 사용할 수 있습니다.





### 비밀번호 유효성 검사

```
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

사용자 **비밀번호의 강도**를 확인하는 데 사용되는 `유효성 검증기 목록`입니다.

`UserAttributeSimilarityValidator`는 사용자의 **아이디**나 **이메일**의 속성이 **비밀번호**와 유사한지 확인합니다.

`MinimumLengthValidator`는 비밀번호의 최소 길이를 확인합니다.

`CommonPasswordValidator`는 비밀번호가 흔한 문자열인지 확인합니다.

`NumericPasswordValidator`는 비밀번호가 숫자로만 구성되어있는지 확인합니다.





### 다국어 및 지역 시간 설정

```
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```

`LANGUAGE_CODE`는 장고 프로젝트에서 사용되는 국가를 설정합니다.

`TIME_ZONE`은 **데이터베이스의 시간대**를 설정하는 문자열입니다.

`USE_I18N`은 장고의 **번역 시스템** 활성화 여부를 설정합니다.

`USE_L10N`은 현지화 된 데이터 형식의 사용 여부를 설정합니다.

`USE_TZ`은 장고가 **시간대를 인식**하는 여부를 설정값입니다.

- Tip : `I18N`은 `국제화(Internationalization)`의 약어입니다.
- Tip : `L10N`은 `지역화(localization)`의 약어입니다.



#### 다국어 및 지역 시간 변경

```
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```

다국어 및 지역시간을 한국 시간대에 맞춘다면, 위와 같이 변경해 사용합니다.





### 정적 파일 설정

```
STATIC_URL = '/static/'
```

`STATIC_URL`은 정적 파일을 참조 할 때 사용할 URL을 의미합니다.

**CSS**, **JavaScript**, **Media**와 같은 정적 파일 경로를 설정합니다.

비어 있지 않은 값으로 설정되면 슬래시(/)로 끝나야합니다.



#### 정적 파일 경로 변경

```
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

로컬 경로의 정적 파일을 사용한다면, 위와 같이 변경해 사용할 수 있습니다.

`STATICFILES_DIRS` 정적 파일이 위치한 경로 목록를 설정합니다.





### 기타 설정

이외에도 접근 가능한 IP인 `ALLOW_IPS`나, 크론 작업 `CRONJOBS` 등을 추가할 수 있습니다.

일반적으로 해당 강좌에 설명된 설정을 활용합니다.

만약, 데이터베이스를 사용하지 않고 `API` 등의 기능등만 활용할 때에는 `DATABASES` 속성을 삭제해 사용할수도 있습니다.

`DATABASES`가 없는 경우, 데이터베이스에 연결하지 않고 사용할 수 있습니다.



## 제 4강 - 애플리케이션 생성

 **상위 목록:** [Python](https://076923.github.io/categories/#Python) **하위 목록:** [Django](https://076923.github.io/posts/#Django) **작성 날짜:** 2020-07-11 **읽는 데** 16 분 소요

### Django Start Application

장고에서 `앱(App)`은 `시스템` 및 `데이터베이스` 등을 통해 서비스를 제공하는 **웹 애플리케이션(Web Application)**입니다.

앱에는 **모델(model)**, **템플릿(template)**, **뷰(view)**를 포함하고 있으며, 여러 앱이 프로젝트를 구성하게 됩니다.

프로젝트를 Python의 `클래스(class)`로 생각한다면, 앱은 `함수(function)`로 볼 수 있습니다.

앱은 재사용성 유/무로 앱의 개수가 결정되며, 재사용성이 없는 경우 하나의 앱으로 사용합니다.

앱은 하나의 **서비스**이며, 앱의 이름은 프로젝트 구성에서 중복되지 않아야 합니다.



```
python manage.py startapp first_app
```

`python manage.py startapp [앱 이름]`을 통해 앱 생성이 가능합니다.

`manage.py` 파일을 통해 앱을 생성하므로, `manage.py` 파일이 존재하는 위치에서 명령어를 실행합니다.

정상적으로 앱이 생성된다면 아래의 디렉토리 구조로 폴더와 파일이 생성됩니다.



```
[현재 프로젝트]/
  > 📁 [장고 프로젝트 이름]
  ⬇ 📁 [장고 앱 이름]
    ⬇ 📁 migrations
      🖹 __init__.py
    🖹 __init__.py
    🖹 admin.py
    🖹 apps.py
    🖹 models.py
    🖹 tests.py
    🖹 view.py
  🖹 manage.py
```



`[장고 앱 이름]` : **python manage.py startapp**로 생성한 장고 앱 이름입니다. 앱 실행을 위한 패키지가 생성됩니다.

`migrations` : 모델(model)에 대한 마이그레이션(migrations) 내역을 저장합니다.

`__init__.py` : 해당 폴더를 패키지로 인식합니다.

`admin.py` : 해당 앱에 대한 관리자 인터페이스를 등록합니다.

`apps.py` : 해당 앱의 경로를 설정합니다.

`models.py` : 데이터베이스의 필드 및 데이터를 관리합니다. **MVT 패턴** 중 `모델(Model)`을 의미합니다.

`tests.py` : 테스트를 위한 실행파일 입니다.

`view.py` : 모델의 정보를 받아 로직을 처리합니다. **MVT 패턴** 중 `뷰(View)`를 의미합니다.



기본적으로 위의 디렉터리 및 파일을 지원합니다.

별도로 `템플릿(template)` 디렉터리, 앱에서 URL을 관리할 수 있도록 `urls.py`을 생성하기도 합니다.

복잡한 로직이나 비지니스 로직을 위한 `serializer.py` 등을 생성할 수 있습니다.

앱은 `models.py`, `view.py`, `serializer.py`, `urls.py`, `template` 등을 위주로 코드를 구현합니다.

일반적으로 `__init__.py`, `apps.py`, `tests.py`는 거의 수정하지 않습니다.

`migrations`의 폴더 내부에 생성될 파일들은 특별한 경우가 아닌 이상 인위적으로 수정하지 않습니다.





### Django Project 등록

```
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'first_app',
]
```

`장고 프로젝트 이름/settings.py`로 이동하여 `INSTALLED_APPS`에 생성한 앱 이름을 추가합니다.

앱이 추가될 때마다 `INSTALLED_APPS`에 앱 이름을 등록해야 합니다.

설치된 앱은 `apps.py`의 경로 설정을 따라갑니다.

- Tip : 만약, 앱의 이름을 변경해야 한다면 **앱 내부의 모든 설정** 및 **INSTALLED_APPS**의 설정을 모두 바꾸어야 합니다.





### Django migrate

```
python manage.py migrate
```

일반적으로 `Model` 클래스의 설계가 완료된 후, 모델에 대응되는 테이블을 데이터베이스에서 생성합니다.

하지만, 모델 클래스를 제외하고도 추가되어야하는 테이블이 존재합니다.

먼저, `python manage.py migrate`을 실행해 기본적인 구조를 적용하도록 합니다.



```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying sessions.0001_initial... OK
```

정상적으로 마이그레이션이 진행되면, 위와 같은 메세지가 띄워집니다.

데이터베이스의 설정이 변경될 때마다 마이그레이션을 진행해야 정상적으로 적용됩니다.



```
python manage.py showmigrations
```

마이그레이션이 정상적으로 적용됬는지 확인합니다.

정상적으로 마이그레이션이 적용됐다면, `[X]`로 마이그레이션이 되었다고 표시됩니다.

만약, 마이그레이션이 적용되지 않았다면, `[ ]`로 마이그레이션이 적용되지 않았다고 표시됩니다.



```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
sessions
 [X] 0001_initial
```





## 제 5강 - Model

 **상위 목록:** [Python](https://076923.github.io/categories/#Python) **하위 목록:** [Django](https://076923.github.io/posts/#Django) **작성 날짜:** 2020-07-26 **읽는 데** 22 분 소요

### Django Model

장고에서 모델은 **데이터베이스의 구조(layout)**를 의미합니다.

`models.py` 파일에 하나 이상의 모델 클래스를 정의해 데이터베이스의 테이블을 정의할 수 있습니다

장고는 `ORM(Object-relational mapping)`을 사용해, 객체와 관계의 설정을 손쉽게 진행할 수 있습니다.

`ORM`은 서로 다른 **관계형 데이터베이스 관리 시스템(RDBMSs)**에서 필드를 스스로 매핑해 간단하게 데이터베이스를 구성할 수 있습니다.

즉, 복잡한 SQL문을 사용하지 않으며, 재사용 및 유지보수의 편리성이 증가합니다.

장고의 모델 파일(models.py)은 필드의 **인스턴스 이름 및 자료형 등을 정의합니다.**





### models.py

```
import uuid
from django.db import models

# Create your models here.
class UserModel(models.Model):
    id = models.UUIDField(help_text="Unique key", primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(help_text="User E-mail", blank=False, null=False)
    name = models.CharField(help_text="User Full Name", max_length=255, blank=False, null=False)
    age = models.PositiveIntegerField(help_text="User Age", blank=False, null=False)
    created_date = models.DateTimeField(help_text="Created Date time", auto_now_add=True)
    updated_date = models.DateTimeField(help_text="Updated Date time", auto_now=True)

    class Meta:
        verbose_name = "유저 정보"
        verbose_name_plural = "유저 정보"
        ordering = ["name", "age"]
```

모델(models.py) 파일을 위와 같이 정의합니다.

`UserModel` 클래스를 생성하며, `models.Model`을 상속합니다.

`UserModel` 클래스는 데이터베이스의 테이블의 이름을 의미하며, 테이블에는 `first_app_usermodel`로 정의됩니다.

`id`는 데이터의 고유한 이름을 의미합니다. `색인(index)`값을 사용할수도 있지만 `UUID(universally unique identifier)`로 사용하도록 하겠습니다.

`email`은 유저의 이메일, `name`은 유저의 이름, `age`는 유저의 나이, `create_date`는 생성 날짜, `update_date`는 변경 날짜를 의미합니다.

각각의 필드는 `models.필드 타입`으로 정의할 수 있습니다.

필드 타입의 정의가 완료된 후, 각각의 필드에 옵션을 추가해 기본적인 필드 구성을 완료합니다.

마지막으로, `메타(Meta)`를 설정해 해당 데이터베이스의 테이블의 기본 메타데이터 정보를 설정합니다.





### 필드 타입

#### ID 분야

|  필드 타입   | 설명                                                         |
| :----------: | :----------------------------------------------------------- |
|  AutoField   | 기본 키 필드이며, 자동적으로 증가하는 필드입니다. 주로 ID에 할당합니다. |
| BigAutoField | 1 ~ 9223372036854775807까지 1씩 자동으로 증가하는 필드입니다. |
|  UUIDField   | UUID 전용 필드이며, UUID 데이터 유형만 저장할 수 있습니다.   |



#### 문자열 분야

| 필드 타입  | 설명                                      |
| :--------: | :---------------------------------------- |
| CharField  | 적은 문자열을 저장하는 문자열 필드입니다. |
| TextField  | 많은 문자열을 저장하는 문자열 필드입니다. |
|  URLField  | URL 데이터를 저장하는 필드입니다.         |
| EmailField | E-mail 데이터를 저장하는 필드입니다.      |



#### 데이터 분야

|      필드 타입       | 설명                                           |
| :------------------: | :--------------------------------------------- |
|     BinaryField      | 이진 데이터를 저장하는 필드입니다.             |
|     DecimalField     | Decimal 데이터를 저장하는 필드입니다.          |
|     IntegerField     | Interger 데이터를 저장하는 필드입니다.         |
| PositiveIntegerField | 양수의 Interger 데이터를 저장하는 필드입니다.  |
|      FloatField      | Float 데이터를 저장하는 필드입니다.            |
|     BooleanField     | 참/거짓 데이터를 저장하는 필드입니다.          |
|   NullBooleanField   | Null값이 가능한 참/거짓을 저장하는 필드입니다. |



#### 날짜 및 시간 분야

|   필드 타입   | 설명                                      |
| :-----------: | :---------------------------------------- |
|   DateField   | 날짜 데이터를 저장하는 필드입니다.        |
|   TimeField   | 시간 데이터를 저장하는 필드입니다.        |
| DateTimeField | 날짜와 시간 데이터를 저장하는 필드입니다. |



#### 기타 분야

|   필드 타입   | 설명                                      |
| :-----------: | :---------------------------------------- |
|  ImageField   | 이미지 데이터를 저장하는 필드입니다.      |
|   FileField   | 파일 업로드 데이터를 저장하는 필드입니다. |
| FilePathField | 파일 경로 데이터를 저장하는 필드입니다.   |



#### 관계 분야

|    필드 타입    | 설명                               |
| :-------------: | :--------------------------------- |
|  OneToOneField  | 일대일 관계를 저장하는 필드입니다. |
|   ForeignKey    | 일대다 관계를 저장하는 필드입니다. |
| ManyToManyField | 다대다 관계를 저장하는 필드입니다. |

각각의 필드는 기본적으로 규칙을 검사합니다.

예를 들어, `EmailField`는 `EmailValidator`가 기본적으로 적용되어 입력값에 `@` 등이 포함되어있는지 등을 확인합니다.

필드들은 기본적인 유효성 검사를 진행해 효율적인 모델을 구성할 수 있습니다.

또한, 각각의 필드는 필수 인수를 요구하기도 하는데, `CharField`는 `max_length` 인수를 필수값으로 요구합니다.

`max_length`는 문자열 필드의 최대 길이를 설정합니다.

기본적인 필드의 옵션값은 다음과 같습니다.





### 필드 옵션

|     옵션     | 설명                                                         | 기본값 |
| :----------: | :----------------------------------------------------------- | :----: |
|   default    | 필드의 기본값을 설정합니다.                                  |   -    |
|  help_text   | 도움말 텍스트를 설정합니다.                                  |   -    |
|     null     | Null 값 허용 유/무를 설정합니다.                             | False  |
|    blank     | 비어있는 값 허용 유/무를 설정합니다.                         | False  |
|    unique    | 고유 키 유/무를 설정합니다.                                  | False  |
| primary_key  | 기본 키 유/무를 설정합니다. (null=False, unique=True와 동일) | False  |
|   editable   | 필드 수정 유/무를 설정합니다.                                | False  |
|  max_length  | 필드의 최대 길이를 설정합니다.                               |   -    |
|   auto_now   | 개체가 저장될 때마다 값을 설정합니다.                        | False  |
| auto_now_add | 개체가 처음 저장될 때 값을 설정합니다.                       | False  |
|  on_delete   | 개체가 제거될 때의 동작을 설정합니다.                        |   -    |
|  db_column   | 데이터베이스의 컬럼의 이름을 설정합니다.                     |   -    |





### 메타 옵션

메타(Meta) 클래스는 모델 내부에서 사용할 수 있는 설정을 적용합니다.

정렬 순서나 관리 설정 등을 변경할 수 있습니다.

메타 클래스의 옵션은 다음과 같습니다.



|        옵션         | 설명                                                         | 기본값 |
| :-----------------: | :----------------------------------------------------------- | :----: |
|      abstract       | 추상 클래스 유/무를 설정합니다.                              | False  |
|      db_table       | 모델에 사용할 데이터베이스 테이블의 이름을 설정합니다.       |   -    |
|       managed       | 데이터베이스의 생성, 수정, 삭제 등의 권한을 설정합니다.      |  True  |
|      ordering       | 객체를 가져올 때의 정렬 순서를 설정합니다.                   |   -    |
|    verbose_name     | 사람이 읽기 쉬운 객체의 이름을 설정합니다. (단수형으로 작성) |   -    |
| verbose_name_plural | 사람이 읽기 쉬운 객체의 이름을 설정합니다. (복수형으로 작성) |   -    |



여기서 가장 중요한 옵션을 고르자면, `managed`와 `ordering`으로 간주할 수 있습니다.

`managed` 옵션이 `True`일 경우 장고가 데이터베이스의 테이블을 마이그레이션 명령어를 통해 관리합니다.

만약, `managed` 옵션이 `False`일 경우 장고에서 데이터베이스의 테이블을 관리하지 않게 되어, 마이그레이션을 진행하지 않아도 됩니다.

즉, 미리 설계된 데이터베이스의 설정 및 제한 조건을 따라갑니다.

`ordering` 옵션은 데이터베이스의 객체 목록을 가져올 때 정렬 순서를 의미합니다.

예시의 `["name", "age"]`은 `name`과 `age`를 위주로 각각 오름차순으로 정렬합니다.

만약, `name`은 내림차순, `age`는 오름차순으로 정렬할 경우, `-`을 붙여 `["-name", "age"]`로 사용합니다.



## 제 6강 - View

 **상위 목록:** [Python](https://076923.github.io/categories/#Python) **하위 목록:** [Django](https://076923.github.io/posts/#Django) **작성 날짜:** 2020-08-09 **읽는 데** 33 분 소요

### Django View

장고에서 뷰는 **어떤 데이터**를 표시할지 정의하며, `HTTP 응답 상태 코드(response)`를 반환합니다.

`views.py` 파일에 애플리케이션의 처리 논리를 정의합니다.

사용자가 입력한 URL에 따라, `모델(Model)`에서 필요한 데이터를 가져와 뷰에서 가공해 보여주며, `템플릿(Template)`에 전달하는 역할을 합니다.

장고의 뷰 파일(views.py)은 요청에 따른 **처리 논리**를 정의합니다.

즉, 사용자가 요청하는 `값(request)`을 받아 모델과 템플릿을 중개하는 역할을 합니다.





### views.py

```
from django.core.exceptions import *
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from first_app.models import UserModel
from first_app.serializers import UserSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return UserModel.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"message": "Operate successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        # queryset = UserModel.objects.all()
        # serializer = UserSerializer(queryset, many=True)
        serializer = UserSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, uuid=None):
        try:
            objects = UserModel.objects.get(id=uuid)
            serializer = UserSerializer(objects)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "존재하지 않는 UUID({})".format(uuid)}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, uuid=None):
        objects = UserModel.objects.get(id=uuid)
        serializer = UserSerializer(objects, data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"message": "Operate successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, uuid=None):
        objects = UserModel.objects.get(id=uuid)
        objects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

뷰(views.py) 파일을 위와 같이 정의합니다.

DRF에서는 `ViewSet`이라는 추상 클래스를 제공합니다.

`ViewSet` 클래스는 `get()`이나 `post()` 같은 메서드를 제공하지는 않지만, `create()`나 `list()` 같은 메서드를 지원합니다.

`ViewSet` 클래스는 `URL` 설정을 통해서 간단하게 연결할 수 있습니다.



#### Module

```
from django.core.exceptions import *
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from first_app.models import UserModel
from first_app.serializers import UserSerializer
```

`from django.core.exceptions import *`은 장고에서 사용하는 예외 사항을 가져옵니다. `와일드카드(*)`를 사용해서 모든 예외 사항을 등록합니다.

`from rest_framework import status`은 **HTTP 상태 코드(status)**를 등록합니다. `1xx(조건부 응답)`이나 `2xx(성공)` 등을 반환할 수 있습니다.

`from rest_framework import viewsets`은 views.py에서 사용할 뷰 클래스입니다.

`from rest_framework.response import Response`는 응답에 사용할 **TemplateResponse** 형식의 객체입니다. 이를 통해 클라이언트에게 제공할 콘텐츠 형태로 변환합니다.

`from first_app.models import UserModel`은 `models.py`에서 선언한 UserModel 모델입니다.

`from first_app.serializers import UserSerializer`은 `serializers.py`에서 선언한 UserSerializer 직렬화 클래스입니다.

**serializers.py는 아직 선언하지 않았으며, 다음 강좌에서 자세히 다룹니다.**



#### ModelViewSet

```
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return UserModel.objects.all()
```

`UserViewSet`의 이름으로 뷰셋 클래스를 생성하고, `ModelViewSet`을 상속받아 사용합니다.

`ModelViewSet` 클래스는 `mixin` 클래스를 사용하며, `create()`, `update()`, `list()` 등의 **읽기/쓰기** 기능을 모두 제공합니다.

`ModelViewSet` 클래스를 사용하게 되면, `queryset` 및 `serializer_class`를 사용해야 합니다.

`queryset`은 테이블의 모든 데이터를 가져오게 하며, `serializer_class`는 추후에 선언할 `UserSerializer`를 연결합니다.

`get_queryset` 메서드는 `queryset`을 선언하지 않았을 때 사용합니다.

현재 코드에서는 필수요소는 아니지만, 예제를 위해 사용합니다.

`get_queryset`을 선언했을 때, 동일하게 테이블의 모든 데이터를 가져오게합니다.





### create(POST)

```
def create(self, request, *args, **kwargs):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=False):
        serializer.save()
        return Response({"message": "Operate successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
```

`create()` 메서드는 `POST`와 관련된 메서드로 볼 수 있습니다.

데이터베이스 테이블의 **쓰기** 기능을 의미합니다.

`serializer`에 **요청 데이터(request.data)**를 입력해 데이터를 **직렬화** 시킬 수 있도록 전달합니다.

그 후, `serializer.is_valid(raise_exception=False)`를 통해 직렬화된 데이터의 **유효성을 검사**합니다.

`raise_exception=False`을 통해, 오류를 발생시키지 않습니다.

오류를 발생시키지 않는 이유는 `Response`를 통해 **별도의 포맷**으로 제공하기 위함입니다.

유효성 검사에 통과한다면 `참(True)` 값을 반환하며, 통과하지 못한다면 `거짓(False)` 값을 반환합니다.

유효성 검사에 통과한 경우에는 `serializer.save()`을 통해 데이터를 데이터베이스 테이블에 저장합니다.

이 후, 각각 `Response()`메서드를 통해 **메세지** 및 `HTTP 상태 코드(status)`를 반환합니다.

- Tip : POST 메서드는 새로운 리소스를 **생성(create)**할 때 사용됩니다.
- Tip : `status.HTTP_201_CREATED`는 요청이 성공적으로 처리되었으며, 자원이 생성되었음을 나타내는 성공 상태 응답 코드입니다.
- Tip : `HTTP_400_BAD_REQUEST`는 잘못된 문법이나 제한 조건으로 인하여 서버가 요청을 이해할 수 없음을 의미하는 상태 응답 코드입니다.





### list(GET)

```
def list(self, request):
    # queryset = UserModel.objects.all()
    # serializer = UserSerializer(queryset, many=True)
    serializer = UserSerializer(self.get_queryset(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
```

`list()` 메서드는 `GET`과 관련된 메서드로 볼 수 있습니다.

데이터베이스 테이블의 **읽기** 기능을 의미합니다.

주석 처리된 `queryset`과 `serializer`로도 데이터베이스의 테이블에서 값을 읽을 수도 있습니다.

`queryset`에서 테이블에서 값을 가져와, `UserSerializer`에 값을 제공합니다.

`many=True`일 경우 **여러 개의 데이터를 입력**할 수 있습니다.

이 후, `Response()`메서드를 통해 직렬화된 데이터를 전달합니다.

- Tip : `GET 메서드`는 **읽거나(Read)** **검색(Retrieve)**할 때에 사용되는 메서드입니다.
- Tip : `status.HTTP_200_OK`는 요청이 성공했음을 나타내는 성공 응답 상태 코드입니다.





### retrieve(GET)

```
def retrieve(self, request, uuid=None):
    try:
        objects = UserModel.objects.get(id=uuid)
        serializer = UserSerializer(objects)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"message": "존재하지 않는 UUID({})".format(uuid)}, status=status.HTTP_404_NOT_FOUND)
```

`retrieve()` 메서드는 `GET`과 관련된 메서드로 볼 수 있습니다.

데이터베이스 테이블의 **읽기(검색)** 기능을 의미합니다.

`uuid` 매개변수는 `urls.py`에서 입력된 변수명을 의미합니다. `serializers.py`와 마찬가지로 아직 작성하지 않았습니다.

`try` 구문 안의 코드로도 읽기 기능을 작성할 수 있지만, 올바르지 않은 값을 검색했을 때 예외 처리를 위해 `except`를 추가합니다.

`UserModel.objects.get(id=uuid)`는 `UserModel`의 `객체(objects)`에서 **하나의 열(Row)**을 가져오기 위해 `get()` 메서드를 사용합니다.

가져올 키 값을 `id`로 설정하고, 입력받은 `uuid`를 대입합니다.

그럴 경우, `id` 필드에서 `uuid`와 일치하는 열이 `objects` 변수에 저장됩니다.

성공적으로 값을 불러왔을 때, `serializer.data`와 `200 OK`로 응답합니다.

검색한 `id`의 값이 존재하지 않는 경우 `ObjectDoesNotExist` 오류가 발생하므로, `except` 구문에서 오류 메세지를 반환합니다.

- Tip : `retrieve()` 메서드의 `uuid` 매개변수는 `urls.py`의 설정에 따라 달라질 수 있습니다.
- Tip : `UserModel.objects.get(id=uuid)`의 `id`는 `models.py`의 `UserModel`에서 선언한 **id = models.UUIDField()**의 `id` 필드(변수)를 의미합니다.





### update(PUT)

```
def update(self, request, uuid=None):
    objects = UserModel.objects.get(id=uuid)
    serializer = UserSerializer(objects, data=request.data)
    if serializer.is_valid(raise_exception=False):
        serializer.save()
        return Response({"message": "Operate successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
```

`update()` 메서드는 `PUT`과 관련된 메서드로 볼 수 있습니다.

데이터베이스 테이블에 **수정** 기능을 의미합니다.

검색 기능과 마찬가지로 특정 uuid를 통해 검색된 **열(Rows)**의 값을 수정합니다.

수정할 열의 데이터를 검색 기능처럼 가져오며, 쓰기 기능처럼 요청 받은 값을 전달합니다.

차이점은 새로 생성하는 것이 아니므로, 검색된 **열(objects)**과 요청 받은 **값(request.data)**을 `UserSerializer에` 같이 전달합니다.

이후, 쓰기 기능처럼 **유효성을 검사하고 결과에 맞게 응답합니다.**

- Tip : `update()` 메서드의 `uuid` 매개변수는 `urls.py`의 설정에 따라 달라질 수 있습니다.





### destroy(DELETE)

```
def destroy(self, request, uuid=None):
    objects = UserModel.objects.get(id=uuid)
    objects.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
```

`destroy()` 메서드는 `DELETE`과 관련된 메서드로 볼 수 있습니다.

데이터베이스 테이블의 **삭제** 기능을 의미합니다.

동일하게 삭제할 `id`를 검색하고, `delete()` 메서드로 열을 지웁니다.

삭제 처리가 완료됐다면, 응답 상태를 반환합니다.

- Tip : `destroy()` 메서드의 `uuid` 매개변수는 `urls.py`의 설정에 따라 달라질 수 있습니다.
- Tip : `status.HTTP_204_NO_CONTENT`는 요청이 성공했으나 클라이언트가 현재 페이지에서 벗어나지 않아도 된다는 것을 의미하는 상태 응답 코드입니다.





### 상속하지 않고 사용하기

```
# def list(self, request):
#     # queryset = UserModel.objects.all()
#     # serializer = UserSerializer(queryset, many=True)
#     serializer = UserSerializer(self.get_queryset(), many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
```

현재 클래스에서 선언된 `create()`, `list()` 메서드 등은 `mixins` 클래스에서 상속된 메서드입니다.

그러므로, 선언하지 않아도 기본적으로 선언된 메서드들을 사용할 수 있습니다.

만약, `list()` 메서드를 일괄 주석처리하더라도 `ListModelMixin`가 적용됩니다.

`ListModelMixin` 클래스는 UserViewSet 아래에 선언한 `queryset` 또는 `get_queryset`을 불러와 사용합니다.

그러므로, `queryset` 또는 `get_queryset`을 선언해야합니다.


## 제 7강 - Serializers

 **상위 목록:** [Python](https://076923.github.io/categories/#Python) **하위 목록:** [Django](https://076923.github.io/posts/#Django) **작성 날짜:** 2020-08-17 **읽는 데** 25 분 소요

### Django Serializers

장고에서 직렬화는 `쿼리셋(querysets)`이나 `모델 인스턴스(model instances)`와 같은 복잡한 구조의 데이터를 **JSON, XML** 등의 형태로 변환하는 역할을 합니다.

즉, Python 환경에 **적합한 구조로 재구성할 수 있는 포맷으로 변환**하는 과정을 의미합니다.

직렬화를 비롯해 `역직렬화(deserialization)`도 지원하며, 직렬화와 역직렬화를 지원하므로 데이터 유효성 검사도 함께 진행됩니다.

데이터를 접근하거나, 인스턴스를 저장하기 전에 항상 유효성을 검사해야하며, 데이터의 구조나 값이 **유효하지 않으면 오류**를 반환합니다.

`serializers.py` 파일에 직렬화에 관한 논리를 정의합니다.

`serializers.py`는 기본 앱 구성에 포함되지 않으므로, 별도로 생성해야 합니다.

직렬화 파일은 아래의 디렉토리 구조로 파일을 생성합니다.



```
[현재 프로젝트]/
  > 📁 [장고 프로젝트 이름]
  ⬇ 📁 [장고 앱 이름]
    ⬇ 📁 migrations
      🖹 __init__.py
    🖹 __init__.py
    🖹 admin.py
    🖹 apps.py
    🖹 models.py
    🖹 tests.py
    🖹 view.py
    🖹 serializers.py
  🖹 manage.py
```





### serializers.py

```
from rest_framework import serializers
from first_app.models import UserModel

# Create your serializers here.
class UserSerializer(serializers.ModelSerializer):
    event_age = serializers.SerializerMethodField(help_text="Custom Field")

    def get_event_age(self, instance):
        return True if instance.age < 30 else False
        
    class Meta:
        model = UserModel
        fields = "__all__"

    def validate_email(self, instance):

        if "admin" in instance:
            raise serializers.ValidationError(detail="사용할 수 없는 메일 계정입니다.")

        return instance

    def validate_name(self, instance):

        if len(instance) < 2:
            raise serializers.ValidationError(detail="이름이 올바르지 않습니다.")

        return instance

    def validate_age(self, instance):

        if instance < 19:
            raise serializers.ValidationError(detail="회원 가입이 불가능한 나이입니다.")

        return instance


    def validate_nationality(self, instance):
        return instance
```

직렬화(serializers.py) 파일을 위와 같이 정의합니다.

DRF에서는 `Serializer`는 **모델 인스턴스(model instances)**나 파이썬 **내장 함수(primitives)**를 마샬링합니다.

마샬링 프로세스는 파서(parsers)와 렌더러(renderers)에 의해 처리됩니다.

`ModelSerializer` 클래스는 기본 필드를 자동으로 채울 수 있으며, 유효성 검사 및 `create()` 메서드와 `update()` 구현이 제공됩니다.



#### Module

```
from rest_framework import serializers
from first_app.models import UserModel
```

`from rest_framework import serializers`는 직렬화와 관련된 정의를 가져옵니다.

`from first_app.models import UserModel`는 `models.py`에서 선언한 UserModel 모델입니다.



#### ModelSerializer

```
# Create your serializers here.
class UserSerializer(serializers.ModelSerializer):
    event_age = serializers.SerializerMethodField(help_text="Custom Field")

    def get_event_age(self, instance):
        return True if instance.age < 30 else False
```

`UserSerializer`의 이름으로 직렬화 클래스를 생성하고, `ModelSerializer`을 상속받아 사용합니다.

`ModelSerializer` 클래스는 `Serializer` 클래스를 사용하며, `create()`, `update()` 등의 기능을 제공합니다.

모델에서 정의한 필드에 대한 값을 가져와 사용하며, `SerializerMethodField`를 통해 임의의 필드를 사용할 수 있습니다.

모델에서 정의한 필드가 아니라면 사용할 수 없지만, `SerializerMethodField`를 사용하면 모델의 필드 값 등을 변형해 사용할 수 있습니다.

`SerializerMethodField`를 선언하면 해당 필드를 조회할 때 실행할 함수를 생성해야 합니다.

`def get_<필드명>`의 형태로 함수를 생성할 수 있습니다.

데이터가 조회될 때, `get_<필드명>` 함수가 실행됩니다.

예제의 함수는 데이터베이스의 `age` 필드가 `30` 미만인 경우에는 `True`를 반환하며, `30` 이상인 경우에는 `False`를 반환합니다.



#### Meta

```
class Meta:
    model = UserModel
    fields = "__all__"
```

`Meta` 클래스는 어떤 **모델**을 사용할지 정의하며, 해당 모델에서 어떤 **필드**를 사용할지 정의합니다.

`fields`의 값을 `__all__`로 사용하는 경우, 모델의 모든 필드를 사용합니다.

만약, 특정 필드만 사용한다면 `fields = ("email", "name", "age", )` 등의 형태로 사용하려는 필드만 적용할 수 있습니다.



#### validate

```
def validate_email(self, instance):

    if "admin" in instance:
        raise serializers.ValidationError(detail="사용할 수 없는 메일 계정입니다.")

    return instance

def validate_name(self, instance):

    if len(instance) < 2:
        raise serializers.ValidationError(detail="이름이 올바르지 않습니다.")

    return instance

def validate_age(self, instance):

    if instance < 19:
        raise serializers.ValidationError(detail="회원 가입이 불가능한 나이입니다.")

    return instance
```

`validate_<필드명>`을 통해 특정 필드에 입력된 값에 대해 별도의 유효성 검사를 진행할 수 있습니다.

`raise serializers.ValidationError(detail="오류 내용")`을 통해 유효성 오류를 발생시킬 수 있습니다.

`email` 필드에 **admin**이라는 문자열이 포함되어 있다면, 유효성 오류를 발생시킵니다.

`name` 필드의 글자수가 **두 글자 미만**이라면, 유효성 오류를 발생시킵니다.

`age` 필드가 **20 미만**이라면, 유효성 오류를 발생시킵니다.





### 필드 매핑

### ID 분야

|      모델 필드      |        매핑 필드         |
| :-----------------: | :----------------------: |
|  models.AutoField   | serializers.IntegerField |
| models.BigAutoField | serializers.IntegerField |
|  models.UUIDField   |  serializers.UUIDField   |



#### 문자열 분야

|     모델 필드     |       매핑 필드        |
| :---------------: | :--------------------: |
| models.CharField  | serializers.CharField  |
| models.TextField  | serializers.CharField  |
|  models.URLField  |  serializers.URLField  |
| models.EmailField | serializers.EmailField |



#### 데이터 분야

|          모델 필드          |          매핑 필드           |
| :-------------------------: | :--------------------------: |
|     models.BinaryField      |      serializers.Field       |
|     models.DecimalField     |   serializers.DecimalField   |
|     models.IntegerField     |   serializers.IntegerField   |
| models.PositiveIntegerField |   serializers.IntegerField   |
|      models.FloatField      |    serializers.FloatField    |
|     models.BooleanField     |   serializers.BooleanField   |
|   models.NullBooleanField   | serializers.NullBooleanField |



#### 날짜 및 시간 분야

|      모델 필드       |         매핑 필드         |
| :------------------: | :-----------------------: |
|   models.DateField   |   serializers.DateField   |
|   models.TimeField   |   serializers.TimeField   |
| models.DateTimeField | serializers.DateTimeField |



#### 기타 분야

|      모델 필드       |         매핑 필드         |
| :------------------: | :-----------------------: |
|  models.ImageField   |  serializers.ImageField   |
|   models.FileField   |   serializers.FileField   |
| models.FilePathField | serializers.FilePathField |



#### 관계 분야

|    모델 필드    |    매핑 필드     |
| :-------------: | :--------------: |
|  OneToOneField  | Serializer Class |
|   ForeignKey    | Serializer Class |
| ManyToManyField | Serializer Class |



직렬화 필드는 모델 필드와 매핑됩니다.

예를 들어, `models.TextField`는 `serializers.CharField`로 매핑됩니다.

직렬화 필드에는 `TextField` 필드가 없으므로, 위의 표에서 맞는 매핑을 찾아서 작성해야 합니다.

일반적으로 대부분이 모델 필드와 비슷하거나 동일한 형태의 구조를 갖고 있습니다.

`관계 분야` 필드는 필드 안에 다른 필드들이 존재하므로, `Serializer` 클래스를 생성해서 내부에서 또 유효성 검사를 진행해야합니다.

그러므로, 별도의 클래스를 생성해서 매핑합니다.

직렬화 필드도 모델 필드처럼 옵션값이 존재합니다. 옵션값은 다음과 같습니다.





### 필드 옵션

|      옵션      | 설명                                       | 기본값 |
| :------------: | :----------------------------------------- | :----: |
|    default     | 필드의 기본값을 설정합니다.                |   -    |
|     label      | HTML Form 등에 표시될 문자열을 설정합니다. |        |
|   help_text    | 도움말 텍스트를 설정합니다.                |   -    |
|   read_only    | 읽기 전용 필드로 설정합니다.               | False  |
|   write_only   | 쓰기 전용 필드로 설정합니다.               | False  |
|    required    | 역직렬화 여부를 설정합니다.                |  True  |
|   allow_null   | Null 값을 허용합니다.                      | False  |
|   vaildators   | 유효성 검사를 적용할 함수를 등록합니다.    |   -    |
| error_messages | 에러 메세지를 설정합니다.                  |   -    |





### 메타 옵션

메타(Meta) 클래스는 **직렬화 필드**에서 사용할 수 있는 설정을 적용합니다.



|       옵션       | 설명                                |
| :--------------: | :---------------------------------- |
|      fields      | 직렬화에 포함할 필드를 설정합니다.  |
|     exclude      | 직렬화에 제외할 필드를 설정합니다.  |
| read_only_fields | 읽기 전용 필드를 설정합니다.        |
|   extra_kwargs   | 추가 옵션을 설정합니다.             |
|      depth       | 외래키 표현 제한 단계를 설정합니다. |


## 제 8강 - URL
### Django URL

`URL(Uniform Resource Locators)`은 네트워크 상에서 **자원(Resource)**이 어디에 존재하는지 알려주기 위한 규약입니다.

URL의 기본 구조는 아래의 형태와 의미를 갖습니다.

```
https://076923.github.io:8000/python/django?id=1000
```

- `https` : 프로토콜(Protocol)
- `076923.github.io` : 호스트(Host)
- `8000` : 포트(Port)
- `python/django` : 리소스 경로(Resource Path)
- `query` : 쿼리(Query)



**https://076923.github.io:8000/(프로토콜 + 호스트 + 포트)**는 **호스팅**, **현재 IP 주소**, **설정** 등에 의해서 달라집니다.

2강에서 배운 `python manage.py runserver`를 통해 서버를 실행할 때, **http://127.0.0.1:8000/**를 통해 테스트 프로젝트를 확인할 수 있었습니다.

**프로토콜, 호스트, 포트**는 프로젝트 설정이나 호스팅등에 의해 달라지는 것을 알 수 있습니다.



다음으로 **/python/django?id=1000(리소스 경로 + 쿼리)** 등은 URL 설정에서 정의할 수 있습니다.

장고에서 URL은 **URL 경로와 일치하는 뷰(View)**를 `매핑(Mapping)`하거나 `라우팅(Routing)`하는 역할을 합니다.

즉, 장고에서 URL 설정은 하나의 항목을 연결하는 `퍼머링크(Permalink)`를 생성하거나 `쿼리스트링(Query string)` 등을 정의할 수 있습니다.



`urls.py` 파일에 URL 경로에 관한 논리를 정의합니다.

`urls.py` 파일은 [장고 프로젝트 이름]으로 생성한 폴더 아래에 포함되어 있습니다.



```
[현재 프로젝트]/
  ⬇ 📁 [장고 프로젝트 이름]
    🖹 __init__.py
    🖹 asgi.py
    🖹 settings.py
    🖹 urls.py
    🖹 wsgi.py
  > 📁 [장고 앱 이름]
  🖹 manage.py
```





### urls.py

```
"""daehee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from first_app.views import UserViewSet

urlpatterns = [
    url('users/(?P<uuid>[0-9a-f\-]{32,})$', UserViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    url('users', UserViewSet.as_view({'get':'list', 'post':'create'})),
]
```

URL(urls.py) 파일을 위와 같이 정의합니다.

어떤 **리소스 경로**나 **쿼리**로 접근했을 때, 연결될 뷰를 설정합니다.



#### Module

```
from django.conf.urls import url
from first_app.views import UserViewSet
```

`from django.conf.urls import url`는 URL 연결과 관련된 모듈입니다.

`from first_app.views import UserViewSet`는 `first_app` 앱의 `views.py`에서 선언한 UserViewSet 클래스입니다.



#### urlpatterns

```
urlpatterns = [
    url('users/(?P<uuid>[0-9a-f\-]{32,})$', UserViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    url('users', UserViewSet.as_view({'get':'list', 'post':'create'})),
]
```

`urlpatterns` 목록 안에 현재 프로젝트에서 사용될 URL 경로를 url 함수를 통해 설정합니다.

`url(경로, ViewSet 클래스)`를 이용하여 **경로(Path)**와 **ViewSet 클래스**를 연결합니다.

현재 ViewSet 클래스는 `create(POST)`, `list(GET)`, `retrieve(GET)`, `update(PUT)`, `destroy(DELETE)`로 다섯 가지의 함수가 선언되어 있습니다.

`retrieve`, `update`, `destroy`는 하나의 대상에 대해 작업을 진행하며, `create`, `list`는 특별한 대상을 상대로 작업이 진행되지 않습니다.

모든 대상은 `users`의 경로이며, 하나의 대상은 `users/<uuid>`의 경로로 볼 수 있습니다.

그러므로, 특별한 대상으로 작업을 진행하는 `url`부터 먼저 선언되어야 합니다.

그 이유는 `if-elif`의 구조로 생각하면 이해하기 쉽습니다.



```
if 'users' in path:
    return "모든 대상"
elif 'users/<uuid>' in path:
    return "하나의 대상"
```

만약, 위의 구조로 `urlpatterns`가 정의되어 있다면, 하나의 대상으로 작업하는 경로가 인식되지 않아 `retrieve`, `update`, `destroy`는 접근할 수 없습니다.

그러므로, 항상 세부 구조를 탐색하는 경로일수록 **상단에 배치**해 사용합니다.



`경로(Path)`는 **리소스 경로(Resource Path)**나, **쿼리(Query)**를 설정할 수 있습니다.

모델에서 고유 id는 `UUID`를 설정했으므로, `UUID`를 통해 접근하도록 하겠습니다.

`http://127.0.0.1:8000/users/<UUID>`로 접근하려면 `UUID` 패턴을 인식해야 합니다.

`url` 함수는 정규표현식을 지원하므로, 정규표현식을 활용해 `UUID` 패턴을 검증하도록 하겠습니다.



`'users/(?P<uuid>[0-9a-f\-]{32,})$'`의 구조로 하나의 대상에 접근할 수 있습니다.

`(?P)`는 해당 영역 내부의 문자는 **정규표현식을 적용**한다는 의미입니다.

`<uuid>`는 정규표현식으로 작성된 url 경로를 `uuid`라는 **변수**명으로 `뷰(View)`에 전달한다는 의미가 됩니다.

`[0-9a-f\-]{32,}`는 간단하게 작성된 **UUID 패턴**입니다.

즉, UUID 정규표현식 패턴을 `uuid`라는 변수로 뷰에 제공한다는 의미가 됩니다.

뷰에서는 `uuid` 변수를 활용해 `http://127.0.0.1:8000/users/<UUID>`로 접근한 `<UUID>` 값을 확인할 수 있습니다.



`ViewSet 클래스`는 `as_view()`으로 리소스 작업을 `HTTP 메서드`에 바인딩할 수 있습니다.

사전의 구조로 바인딩 할 수 있으며, **{‘HTTP 메서드’, ‘ViewSet 메서드’}**의 구조를 갖습니다.

특별한 경우가 아니라면 HTTP 메서드는 중복해서 사용하지 않습니다.

- Tip : 더 정확한 UUID 패턴은 `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}`으로 사용할 수 있습니다.





### 라우팅(Routing)

`라우팅(Rouing)`이란 네트워크 상에서 데이터를 전달할 때, 목적지까지의 경로를 체계적으로 결정하는 **경로 선택 과정**을 의미합니다.

현재 장고 프로젝트는 하나의 애플리케이션을 가지고 있으므로, 매우 작은 네트워크로 볼 수 있습니다.

만약, 장고 프로젝트가 매우 커진다면 하나의 `urls.py`에서 관리하기가 어려워질 수 있습니다.

그러므로 **애플리케이션**마다 `urls.py`를 생성해 **프로젝트** `urls.py`에 연결해 관리할 수 있습니다.

앱(first_app)에 `urls.py` 파일을 생성해 아래의 코드처럼 생성합니다.



```
## first_app/urls.py
from django.conf.urls import url
from first_app.views import UserViewSet

urlpatterns = [
    url('(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', UserViewSet.as_view({ 'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    url('', UserViewSet.as_view({ 'get':'list', 'post':'create'})),
]
```

`프로젝트 urls.py`와의 차이점은 `경로(Path)`에 `users`가 존재하지 않습니다.

제거된 `users`를 `프로젝트 urls.py`에 설정합니다.



```
## daehee/urls.py
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('users', include('first_app.urls'))
]
```

`프로젝트 urls.py`는 새로운 두 종류의 모듈이 추가됩니다.

`from django.urls import path`는 라우팅할 경로를 설정할 수 있습니다.

`from django.conf.urls import include`는 다른 `urls.py`를 가져와 읽을 수 있는 역할을 합니다.

기본 URL 설정과 동일하게 `urlpatterns` 안에 작성합니다.

`path(경로, 다른 urls.py 경로)`로 설정할 수 있습니다.

`users` 경로를 접근했을 때, `include('first_app.urls')` 경로의 `first_app/urls.py`로 이동해 접근합니다.

즉, `users`로 이동했을 때 URL 경로를 재 탐색하므로, `first_app/urls.py`에는 `users`를 작성하지 않습니다.


## 제 9강 - Migration
### Django Migration

`마이그레이션(Migration)`이란 데이터베이스의 `스키마(Schema)`를 관리하기 위한 방법입니다.

사전적인 의미로는 현재 사용하고 있는 운영 환경을 다른 운영 환경으로 변환하는 작업을 지칭합니다.

데이터베이스에서는 스키마를 비롯해 테이블, 필드 등의 변경이 발생했을 때 지정된 **데이터베이스에 적용**하는 과정을 의미합니다.

현재 **모델(model.py)**은 정의만 되어있을 뿐, 데이터베이스를 생성하고 적용하지 않았습니다.

마이그레이션을 통해 데이터베이스를 생성하고 **모델의 생성, 변경, 삭제 등에 따라 작업 내역을 관리하고 데이터베이스를 최신화할 수 있습니다.**

4강에서 기본 마이그레이션을 진행했다면, `애플리케이션 마이그레이션`으로 이동해 진행합니다.

- Tip : 스키마(Schema)란 데이터베이스에서 자료의 구조, 자료 간의 관계 등을 기술한 것을 의미합니다.





### 기본 마이그레이션

```
python manage.py migrate
```

- **결과**

  

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying sessions.0001_initial... OK
```

`python manage.py migrate`으로 현재 프로젝트의 마이그레이션을 진행합니다.

마이그레이션 진행시, 장고 프로젝트에서 사용하는 11개의 기본 테이블이 생성됩니다.

**sqlite3** 데이터베이스의 경우 생성되는 테이블은 다음과 같습니다.

`auth_group`, `auth_group_permissions`, `auth_permission`, `auth_user`, `auth_user_groups`, `auth_user_user_permissions`, `django_admin_log`, `django_content_type`, `django_migrations`, `django_session`, `sqlite_sequence`의 기본 테이블이 생성됩니다.





### 마이그레이션 상태 확인

```
python manage.py showmigrations
```

- **결과**

  

```
admin
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
first_app
 (no migrations)
sessions
 [X] 0001_initial
```

`python manage.py showmigrations` 명령어로 현재 마이그레이션 상태를 확인할 수 있습니다.

기본적인 마이그레이션으로 11개의 테이블이 생성되었지만, `모델(model.py)`에서 생성한 테이블을 생성되지 않은 것을 확인할 수 있습니다.

이제, 애플리케이션(앱)에서 생성한 모델에 대해 마이그레이션을 적용해보도록 하겠습니다.





### 애플리케이션 마이그레이션

```
python manage.py makemigrations first_app
```

- **결과**

  

```
Migrations for 'first_app':
  first_app\migrations\0001_initial.py
    - Create model UserModel
```

`python manage.py makemigrations [앱 이름]`으로 모델에서 생성한 사항이나, 변경 사항된 사항을 감지하여 파일로 생성합니다.

단순하게 마이그레이션을 진행할 구조를 생성하는 것이므로, 적용은 되지는 않습니다.

다시 `python manage.py showmigrations` 명령어를 통해 마이그레이션 상태를 확인할 경우, 다음과 같이 표시됩니다.

- Tip : 데이터베이스 종류에 따라 다른 SQL이 생성됩니다.



```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
first_app
 [ ] 0001_initial
sessions
 [X] 0001_initial
```

`first_app`에서 **(no migrations)**으로 표시되던 항목이 `[ ] 0001_initial`로 표시되는 것을 확인할 수 있습니다.

이 변경사항에 대해 마이그레이션을 진행해보도록 하겠습니다.



```
python manage.py migrate first_app
```

- **결과**

  

```
Operations to perform:
  Apply all migrations: first_app
Running migrations:
  Applying first_app.0001_initial... OK
```

결과에서 확인할 수 있듯이, `first_app` 앱에 대한 마이그레이션이 적용되었습니다.

다시 `python manage.py showmigrations` 명령어를 통해 마이그레이션 상태를 확인할 경우, 다음과 같이 표시됩니다.



```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
first_app
 [X] 0001_initial
sessions
 [X] 0001_initial
```

`first_app`의 **0001_initial**이 적용된 것을 확인할 수 있습니다.

`python manage.py migrate first_app` 명령어는 현재 적용되지 않은 마이그레이션을 적용하는 역할을 합니다.

마이그레이션이 정상적으로 적용될 경우, `앱_클래스명`의 형태로 테이블이 생성됩니다.

예제를 기준으로 테이블의 이름을 확인한다면, `first_app_usermodel` 테이블이 생성됩니다.

정상적으로 마이그레이션이 완료되었다면, 프로젝트를 실행할 수 있습니다.





### 마이그레이션시 주의사항

마이그레이션을 진행할 때, `모델(model.py)`에서 하나라도 변경이 발생했다면 마이그레이션을 다시 진행해야 합니다.

모델 수정이 발생할 경우, 다음과 같은 절차로 마이그레이션을 적용할 수 있습니다.



```
python manage.py makemigrations [앱 이름]
python manage.py migrate [앱 이름]
```

특정 앱에 대해 마이그레이션 파일을 생성 후, 모든 변경사항을 적용합니다.

모델 마이그레이션 진행 시, 경고 문구가 발생한다면 필수 필드가 생성되었지만 **기본값이 할당되어 있지 않아서 발생하는 문제입니다.**

**임의의 값을 모두 채워주거나, 취소하여 건너 뛸 수 있습니다.**

단, 임의의 값으로 채울 때 올바르지 않은 값을 채운다면 `치명적인 오류`가 발생할 수 있습니다.

마이그레이션이 정상적으로 적용되었다면, 다음과 같은 파일 구조를 갖습니다.



```
[현재 프로젝트]/
  > 📁 [장고 프로젝트 이름]
  ⬇ 📁 [장고 앱 이름]
    > 📁 __pycache__
    ⬇ 📁 migrations
      > 📁 __pycache__
      🖹 __init__.py
      🖹 0001_initial.py
    🖹 __init__.py
    🖹 admin.py
    🖹 apps.py
    🖹 models.py
    🖹 serializers.py
    🖹 tests.py
    🖹 urls.py
    🖹 view.py
  🖹 db.sqlite3
  🖹 manage.py
```



마이그레이션은 `Git`과 다르므로, **마이그레이션은 한 명만 진행**하는 것이 좋습니다.

만약, 여러 명이 작업하게 된다면 데이터베이스가 꼬이는 주된 원인이 됩니다.

마이그레이션은 데이터베이스 스키마에 변화를 발생시키지 않더라도 수행하는 것을 권장합니다.

마이그레이션은 모델의 변경 내역을 누적하는 역할을 하며, **적용된 마이그레이션 파일은 제거하면 안됩니다.**

만약, **마이그레이션을 취소하거나 돌아가야하는 상황**이라면 다음과 같이 적용할 수 있습니다.



```
python manage.py migrate [앱 이름] 0001_initial
```

위의 명령어를 실행할 경우, `0001_initial`의 상태로 되돌아갑니다.

현재 마이그레이션이 적용된 상태가 `0001_initial` 이전이라면, **정방향(forward)으로 마이그레이션이 진행됩니다.**

만약, 현재 마이그레이션이 적용된 상태가 `0001_initial` 이후라면, 순차적으로 지정된 마이그레이션까지 **역방향(backward)으로 마이그레이션이 진행됩니다.**

`마이그레이션을 초기화` 해야하는 경우에는 다음과 같이 실행할 수 있습니다.



```
python manage.py migrate [앱 이름] zero
```

현재 앱에 적용된 모든 마이그레이션을 삭제합니다.

마이그레이션은 **디펜던시(dependencies) 순서에 의해 진행됩니다.**

만약, `no such column` 오류 발생시 마이그레이션이 진행되지 않았다는 의미가 됩니다.





### 데이터베이스 완전 초기화

데이터베이스를 삭제하고 완전하게 처음의 상태로 돌아가기 위해서는 다음과 같은 파일을 제거하면 처음 상태로 돌아갈 수 있습니다.

```
[현재 프로젝트]/
  ⬇ 📁 [장고 프로젝트 이름]
    > 📁 __pycache__
  ⬇ 📁 [장고 앱 이름]
    > 📁 __pycache__
    ⬇ 📁 migrations
      > 📁 __pycache__
      🖹 0001_initial.py
  🖹 db.sqlite3
```

위 구조에서 `[장고 프로젝트 이름]/__pycache__`, `[장고 앱 이름]/__pycache__`, `[장고 앱 이름]/migrations/__pycache__`, `[장고 앱 이름]/migrations/0001_initial.py`, `db.sqlite3`을 삭제합니다.

**모든 캐시 파일(__pycache__), 마이그레이션 내역(0001_initial.py), 데이터베이스(db.sqlite3)**를 삭제한다면 초기 상태로 돌아갈 수 있습니다.

위와 같은 파일을 제거할 경우, `기본 마이그레이션`부터 다시 진행하셔야 합니다.


## 제 10강 - Test
### Django Test

프로젝트의 설정 및 마이그레이션이 완료되면 프로그램이 정상적으로 구동되는지 **테스트**를 진행해야 합니다.

이 과정은 전체적인 실행에 문제가 없더라도, **프로그램이 의도한대로 작동이 되는지 확인**하는 과정도 포함됩니다.

장고 프로젝트를 테스트하는 방법은 크게 세 가지의 방법이 있습니다.

이 중, 두 가지 이상은 병행하여 테스트하는 것을 권장드립니다.


### Django Runserver

```
python manage.py runserver
```

- **결과**

  Watching for file changes with StatReloader Performing system checks…  System check identified no issues (0 silenced).  You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions. Run ‘python manage.py migrate’ to apply them. September 07, 2020 - 18:50:24 Django version 3.0.7, using settings ‘daehee.settings’ Starting development server at http://127.0.0.1:8000/ Quit the server with CTRL-BREAK. [28/Jun/2020 19:11:54] “GET / HTTP/1.1” 200 16351  

먼저, 테스트를 진행하기 위해 서버를 실행시킵니다.

만약 이 구문에서 오류가 발생한다면, `구문 오류(syntax error)`가 발생했을 가능성이 매우 높습니다.

오류가 발생한 위치에서 발생했을수도 있으나, 전혀 다른 위치에서 발생한 오류일 수도 있습니다.

위 구문에서 정상적으로 동작하더라도, 실제 테스트에서 오류가 발생한다면 `논리 오류(logic error)`이므로 전체적으로 다시 검토해야합니다.





### Django Test

![img](https://076923.github.io/assets/posts/Python/Django/lecture-10/1.webp)

`장고 프로젝트 설정 파일(settings.py)`에서 **DEBUG`를 True로 설정**했다면 원활하게 테스트를 진행할 수 있습니다.

`로컬 서버(http://127.0.0.1:8000/users)`에 접속하면 위와 같은 화면을 확인할 수 있습니다.

각각의 필드에 `이메일`, `이름`, `나이`를 작성한 다음, `[POST]` 버튼을 클릭합니다.



![img](https://076923.github.io/assets/posts/Python/Django/lecture-10/2.webp)

정상적인 값을 입력했다면, `View`에서 작성한 `{"message": "Operate successfully"}` 구문이 반환됩니다.

다음으로, 우측 상단의 `[GET]` 버튼을 클릭합니다.


필드에 `이메일`, `이름`, `나이`만 작성했지만, 나머지 필드가 모두 입력되어 표시되는 것을 확인할 수 있습니다.

이번에도 `이메일`, `이름` 그리고 `나이`의 값을 20미만으로 작성한 다음, `[POST]` 버튼을 클릭합니다.


`age` 필드의 유효성 검사의 `instance < 19` 조건으로 **회원 가입이 불가능한 나이입니다.**의 메세지가 반환됩니다.

오류가 발생하거나, 유효성 검사에 실패했을 경우 데이터베이스에 저장되지 않습니다.

이제 다시, 우측 상단의 `[GET]` 버튼을 클릭합니다.



처음에 작성한 데이터의 `id` 필드에서 **835e1ca3-5383-4e2e-a051-fc2b8ad11f5a(UUID)**를 복사해 `URL`에 입력합니다.

즉, `http://127.0.0.1:8000/users/835e1ca3-5383-4e2e-a051-fc2b8ad11f5a`로 이동합니다.

값을 수정한 다음 우측 하단의 `[PUT]` 버튼으로 값을 수정할 수 있으며, 우측 상단의 `[DELETE]` 버튼으로 입력된 데이터를 삭제할 수 있습니다.





### Requests Test

```
import json
import requests

url = "http://127.0.0.1:8000/users"

response = requests.get(url)

status_code = response.status_code
data = json.loads(response.text)

print(status_code)
print(data)
```

- **결과**

  200 [{‘id’: ‘835e1ca3-5383-4e2e-a051-fc2b8ad11f5a’, ‘event_age’: True, ‘email’: ‘s076923@gmail.com’, ‘name’: ‘윤대희’, ‘age’: 20, ‘created_date’: ‘2020-09-07T18:59:23.066156+09:00’, ‘updated_date’: ‘2020-09-07T18:59:23.066156+09:00’}]  

서버가 구동되고 있는 상태에서 새로운 코드 프로젝트를 실행시킵니다.

앞선 예제에서 데이터를 삭제하지 않았다면, 위의 코드로 데이터를 가져올 수 있습니다.

`requests` 모듈을 활용해 `CRUD` 기능을 모두 활용할 수 있습니다.

`[GET]`은 `requests.get(url)`을 활용해 데이터를 가져옵니다.



```
import json
import requests

url = "http://127.0.0.1:8000/users"
data = {
    "email" : "s076923@gmail.com",
    "name" : "윤대희",
    "age" : 21
}

response = requests.post(url, data=data)

status_code = response.status_code
data = json.loads(response.text)

print(status_code)
print(data)
```

- **결과**

  201 {‘message’: ‘Operate successfully’}  

`[POST]`는 `[GET]` 방식과 코드에서 큰 차이를 보이지는 않지만, 데이터를 입력해야 하므로 `사전(Dictionary)` 형식의 값을 생성합니다.

다음으로, `requests.get` 메서드가 아닌 `requests.post` 메서드에 `data` 인자에 `data` 변수를 입력합니다.

다시 `[GET]` 메서드를 실행해보거나, 장고 테스트를 실행한다면 적용된 것을 확인할 수 있습니다.



```
import json
import requests

url = "http://127.0.0.1:8000/users/835e1ca3-5383-4e2e-a051-fc2b8ad11f5a"
data = {
    "email" : "s076923@gmail.com",
    "name" : "윤대희",
    "age" : 22
}

response = requests.put(url, data=data)

status_code = response.status_code
data = json.loads(response.text)

print(status_code)
print(data)
```

- **결과**

  201 {‘message’: ‘Operate successfully’}  

`[PUT]`은 `[POST]`에서 `url`을 특정 `id`로 변경하고 메서드의 이름만 `post`에서 `put`으로 변경합니다.

`data` 필드는 모두 필수 필드이기 때문에, 모두 입력한 다음 명령을 실행합니다.



```
import json
import requests

url = "http://127.0.0.1:8000/users/835e1ca3-5383-4e2e-a051-fc2b8ad11f5a"

response = requests.delete(url)

status_code = response.status_code

print(status_code)
```

- **결과**

  204  

`[DELETE]`는 `[GET]`과 같이 데이터를 사용하지 않으므로 작성하지 않습니다.

또한, 반환값이 없으므로, `response.text`를 읽지 않습니다.





### Postman Test

`포스트맨(Postman)` 애플리케이션을 이용하여 `API` 테스트를 진행할 수 있습니다.

[다운로드 링크](https://www.postman.com/downloads/)를 통하여 설치를 진행합니다.


정상적으로 설치가 완료된 후, `+` 모양의 탭 추가 버튼을 클릭합니다.

새로운 탭을 추가한다면, 다음과 같은 형태로 탭이 추가됩니다.


위와 같은 `Untitled Request` 탭이 추가됩니다.

이 탭을 통하여 요청할 API의 `Method`, `URL`, `Authorization`, `Headers`, `Body` 등을 설정할 수 있습니다.


메서드는 **리스트 박스**를 이용해 설정할 수 있습니다.

URL은 리스트 박스 옆 **텍스트 박스**에 입력합니다.

`GET` 메서드와 함께, `http://127.0.0.1:8000/users` URL을 입력합니다.

그 다음으로, `[SEND]` 버튼을 클릭합니다.


위 이미지와 같이 하단의 `Body`란에 반환된 데이터가 표시됩니다.

동일하게 `[POST], [PUT], [UPDATE]` 등을 진행할 수 있습니다.


`[POST]` 메서드 이용시, 상단의 `Body` 탭에서 필드의 값들을 채워준 다음, `[Send]` 버튼을 클릭합니다.

`[PUT]`이나 `[DELETE]`도 비슷한 방식으로 진행됩니다.


만약, `Body` 탭을 코드와 비슷한 형태로 작성하려면 `form-data`가 아닌 `raw`에서 작성합니다.

`raw`에서 작성하는 경우, 입력하는 데이터가 **json 형식**임을 알려야 합니다.

그러므로, `Headers` 탭에서 `Content-Type`을 추가합니다.

우측 `VAULE` 란에 `application/json`을 입력합니다.

이후, `raw`에서 작성이 완료됬다면 `[Send]` 버튼을 클릭해 요청할 수 있습니다.



## 제 11강 - Foreign Key (1)

### Django Foreign Key

`외래키(Foreign Key)`란 테이블의 필드 중에서 다른 테이블의 행과 **식별할 수 있는 키**를 의미합니다.

일반적으로 외래키가 포함된 테이블을 **자식 테이블**이라 하며, 외래키 값을 갖고 있는 테이블은 **부모 테이블**이라 합니다.

즉, 외래키란 **테이블과 테이블을 연결**하기 위해 사용되는 키입니다.

만약, 외래키를 사용하지 않고 **게시물**과 **댓글**의 내용을 저장할 기능을 구현한다면, 다음과 같은 테이블로 생성해야 합니다.





### Post 테이블

|  id  | 제목                          | 내용             | 댓글1       | 댓글2       | 댓글3 | …    | 댓글N |
| :--: | :---------------------------- | :--------------- | :---------- | :---------- | :---- | :--- | :---- |
|  1   | 제 1강 - Django 소개 및 설치  | 장고(Django)는 … | 안녕하세요… | 감사합니다. | null  | …    | null  |
|  2   | 제 2강 - Django 프로젝트 생성 | 장고(Django)를 … | 질문이 있…  | null        | null  | …    | null  |
|  …   | …                             | …                | …           | …           | …     | …    | …     |



위와 같은 형태는 하나의 테이블에 너무 많은 `열(column)`이 추가되어, 매우 효율적이지 못한 구조가 됩니다.

또한, 열을 N개까지 추가했더라 하더라도 너무 많은 열과 데이터로 인해 조회하는데에 비교적 오랜 시간이 소요됩니다.

위와 같은 구조를 두 개의 테이블로 나눈다면 다음과 같이 변경할 수 있습니다.



#### Post 테이블

|  id  | 제목                          | 내용             |
| :--: | :---------------------------- | :--------------- |
|  1   | 제 1강 - Django 소개 및 설치  | 장고(Django)는 … |
|  2   | 제 2강 - Django 프로젝트 생성 | 장고(Django)를 … |
|  …   | …                             | …                |



#### Comment 테이블

|  id  | post_id | 내용        |
| :--: | :------ | :---------- |
|  1   | 1       | 안녕하세요… |
|  2   | 1       | 감사합니다. |
|  3   | 2       | 질문이 있…  |
|  …   | …       | …           |

`Comment` 테이블을 별도로 생성한 다음, 해당 내용이 어느 `Post` 테이블의 `id`에서 사용됬는지 표기한다면 간단한 구조로 생성할 수 있습니다.

불필요한 열이 생성되지 않아, 효율적인 테이블을 구성할 수 있습니다.


### Django Code 구성

#### models.py

```
from django.db import models

# Create your models here.
class Post(models.Model):
    id = models.BigAutoField(help_text="Post ID", primary_key=True)
    title = models.CharField(help_text="Post title", max_length=100, blank=False, null=False)
    contents = models.TextField(help_text="post contents", blank=False, null=False)


class Comment(models.Model):
    id = models.BigAutoField(help_text="Comment ID", primary_key=True)
    post_id = models.ForeignKey("Post", related_name="post", on_delete=models.CASCADE, db_column="post_id")
    contents = models.TextField(help_text="Comment contents", blank=False, null=False)
```

게시물의 제목과 내용을 저장할 `Post` 테이블을 생성합니다.

`Post` 테이블의 `식별자(id)`, `제목(title)`, `내용(contents)` 필드에 관한 정의를 작성합니다.



게시물에 작성될 댓글의 내용을 저장할 `Comment` 테이블을 생성합니다.

`Comment` 테이블의 `식별자(id)`, `외래키(post_id)`, `내용(contents)` 필드에 관한 정의를 작성합니다.



외래키를 작성할 때 필수적으로 포함되어야할 매개변수는 **참조할 테이블**, **개체 관계에 사용할 이름**, **개체 삭제시 수행할 동작** 등 입니다.

`참조할 테이블`은 외래키에서 어떤 테이블을 참조할지 의미합니다. 예제에서는 `Post` 테이블입니다.

`개체 관계에 사용할 이름(related_name)`은 추상 모델에서 관계를 정의할 때 사용될 이름을 의미합니다. 예제에서는 `post`입니다.

`개체 삭제시 수행할 동작(on_delete)`은 외래키(ForeignKey)가 바라보는 테이블의 값이 삭제될 때 수행할 방법을 지정합니다.

즉, 게시물이 삭제될 때 댓글은 어떻게 처리할지를 정의합니다.

`데이터베이스 상의 필드 이름(db_column)`은 테이블에 정의될 이름을 의미합니다.

만약, `db_column` 매개변수를 사용하지 않는다면, 데이터베이스 필드에 작성될 필드명은 `post_id_id`가 됩니다.

`post_id_id`는 의도한 필드명이 아니므로, `db_column` 매개변수의 인수에 `post_id`를 사용합니다.



##### on_delete

|     on_delete     |                            의미                             |
| :---------------: | :---------------------------------------------------------: |
|  models.CASCADE   |              외래키를 포함하는 행도 함께 삭제               |
|  models.PROTECT   | 해당 요소가 함께 삭제되지 않도록 오류 발생 (ProtectedError) |
|  models.SET_NULL  |   외래키 값을 NULL 값으로 변경 (null=True일 때 사용 가능)   |
| models.SET(func)  | 외래키 값을 func 행동 수행 (func는 함수나 메서드 등을 의미) |
| models.DO_NOTHING |                    아무 행동을 하지 않음                    |



#### views.py

```
from rest_framework import viewsets

from blog.models import Post
from blog.models import Comment
from blog.serializers import PostSerializer
from blog.serializers import CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
```

뷰는 별도의 알고리즘을 추가하지 않고 기본 형태를 사용합니다.

게시물 작성과 댓글 작성은 별도의 기능이므로, 두 개의 뷰셋을 생성합니다.



#### serializers.py

```
from rest_framework import serializers
from blog.models import Post
from blog.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post_id", "contents")


class PostSerializer(serializers.ModelSerializer):
    post = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "contents", "post")
```

`CommentSerializer`와 `PostSerializer`를 선언합니다.

여기서, `PostSerializer`는 `CommentSerializer`를 불러올 예정이므로, `CommentSerializer`, `PostSerializer` 순으로 선언합니다.



댓글은 참조한 **게시물의 ID**와 **내용**을 확인할 예정이므로, `fields`에 `post_id`와 `contents`를 선언합니다.



게시물은 **게시물의 ID** **제목**, **내용**, **댓글 내용**을 확인할 예정입니다.

여기서, 댓글은 `Comment` 테이블에 작성됩니다. 그러므로, `CommentSerializer`를 통해 직렬화를 해야합니다.

새로운 필드인 `post`를 선언하고 해당 필드는 `CommentSerializer`를 통하도록 합니다.

여러 개의 댓글이 작성될 수 있으므로, `many` 매개변수는 `True`로 사용하고, 게시물에서 댓글을 수정하지 않으므로, `read_only` 매개변수도 `True`로 사용합니다.

여기서, 새로운 필드인 `post` 변수명은 `models.py`에서 작성한 `개체 관계에 사용할 이름(related_name)`으로 작성해야 합니다.

만약, 전혀 다른 변수명으로 사용할 경우 정상적으로 동작하지 않습니다.



#### urls.py
```
from django.conf.urls import url
from blog.views import PostViewSet
from blog.views import CommentViewSet


urlpatterns = [
    url('post', PostViewSet.as_view({'get':'list', 'post':'create'})),
    url('comment', CommentViewSet.as_view({'get':'list', 'post':'create'})),
]
```

`URL`은 `post`와 `comment`를 추가합니다.

간단한 **조회(get, list)**와 **작성(post, create)**만 수행하도록 하겠습니다.





### Django Runserver

#### Post

`post` URL로 이동해, 게시물의 **제목**과 **내용**을 입력합니다.


두 게시물이 작성되면 위와 같이 표시되는 것을 알 수 있습니다.

`post` 필드는 현재 작성된 댓글이 없으므로 `[]`의 형태로 표시됩니다.



#### Comment


`comment` URL로 이동해, 특정 게시물에 댓글의 **내용**을 입력합니다.

여기서, 어떤 게시물에 작성할지 `post_id`를 선택하게 됩니다.

`post_id`는 외래키이므로, `Post` 테이블에 존재하는 값만 입력할 수 있습니다.


세 개의 댓글이 작성되면 위와 같이 표시되는 것을 알 수 있습니다.



#### Post

이제 다시, `post` URL로 이동하면 게시물마다 어떤 댓글이 달렸는지 확인할 수 있습니다.





### 자식 테이블에서 부모 테이블 참조하기

현재 `comment` URL에서는 댓글이 어떤 부모 테이블의 행을 참조했는지 확인하기 어렵습니다.

만약, 댓글에서 게시물의 제목과 내용 등을 확인해야하는 일이 발생한다면, 아래와 같이 코드를 추가해 확인할 수 있습니다.



#### serializers.py

```
from rest_framework import serializers
from blog.models import Post
from blog.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post_id", "contents")

    def to_representation(self, instance):
        self.fields['post_id'] =  PostRepresentationSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)


class PostSerializer(serializers.ModelSerializer):
    post = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "contents", "post")


class PostRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "contents")
```

댓글에서 게시물의 내용을 확인하기 위해서 `to_representation` 메서드를 추가합니다.

`to_representation` 메서드는 `Object instance` 형식을 `사전(Dictionary)` 형태로 변경시킵니다.

현재 필드들(self.fields) 중에서 `post_id`의 필드를 다시 직렬화해 부모의 테이블에서 가져오게 합니다.

이때, `PostRepresentationSerializer` 클래스를 새로 생성해야합니다.

`PostRepresentationSerializer`는 `PostSerializer` 클래스와 형태가 비슷하나, `post` 필드를 사용하지 않습니다.

`PostSerializer` 클래스로 직렬화 한다면, 다시 `CommentSerializer`를 부르게 되고, **재귀(Recursion)**에 빠지게 됩니다.

그러므로, `PostRepresentationSerializer`을 선언해 `post` 필드를 제거한 직렬화 클래스를 사용합니다.


다시, `comment` URL로 이동해 결과를 확인한다면 위와 같은 형태로 표시됩니다.

`post_id` 필드의 값을 `사전(Dictionary)` 형식으로 변경시켜, 해당 값이 부모 테이블의 행으로 출력됩니다.

## 제 12강 - Foreign Key (2)

### Django Foreign Key
앞선 외래키 사용법에서는 두 개의 **URL(post, comment)**를 생성해 각각 요청하여 데이터를 입력하였습니다.

`post` 기능과 `comment` 기능은 별도의 기능이기 때문에 분리하였지만, 게시물에 종속된 **별도의 기능(태그, 키워드, 정보)**을 추가해 다른 테이블로 분리했다면 테이블이 다르더라도 함께 작성되는 것이 더 효율적이고 관리하기 편할 수도 있습니다.

이렇듯 하나의 요청으로 **부모 테이블**과 **자식 테이블**이 함께 작성되어야 하는 경우에는 `뷰(views.py)`의 코드를 수정해 적용할 수 있습니다.





### 요청 데이터

![img](https://076923.github.io/assets/posts/Python/Django/lecture-12/1.webp)

**게시물(post) 데이터**와 댓**글(comment) 데이터**를 함께 받아서 `post` 테이블과 `comment` 테이블에 한 번에 입력해보도록 하겠습니다.

Django Rest framework에서 지원되는 **HTML 입력 폼**으로는 지원되지 않는 형태이므로, `포스트맨(Postman)`이나 `코드`를 통해 데이터를 전달합니다.

```
{
    "title" : "제 3강 - Django 프로젝트 설정",
    "contents" : "장고(Django)의 ...",
    "post" : {
        "contents" : "댓글까지 함께 작성."
    }
}
```

위와 같은 형태로 데이터를 `post` URL에 전달합니다.





### Django Code 구성

#### views.py

```
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from blog.models import Post
from blog.models import Comment
from blog.serializers import PostSerializer
from blog.serializers import CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        post_data = {
            "title": request.data["title"],
            "contents": request.data["contents"],
        }
        post_serializer = PostSerializer(data=post_data)
        if post_serializer.is_valid(raise_exception=True):
            post_result = post_serializer.save()

            comment_data = {
                "post_id": post_result.id,
                "contents": request.data["post"]["contents"],
            }
            comment_serializer = CommentSerializer(data=comment_data)
            if comment_serializer.is_valid(raise_exception=True):
                comment_serializer.save()
                return Response({"message": "Operate successfully"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
```

`create()` 메서드를 추가해 각각의 테이블에 맞는 데이터로 변경시키고, 변경시킨 데이터마다 직렬화합니다.

`request.data`는 앞선 **포스트맨(Postman) 데이터**와 동일한 형태를 갖습니다.

이 데이터를 파싱(parsing)하여 `PostSerializer`와 `CommentSerializer`에 맞게끔 변형합니다.



```
post_data = {
    "title": request.data["title"],
    "contents": request.data["contents"],
}
post_serializer = PostSerializer(data=post_data)
if post_serializer.is_valid(raise_exception=True):
    post_result = post_serializer.save()
```

`Comment` 테이블은 `Post` 테이블의 `id`에 영향을 받기 때문에, 먼저 `Post` 테이블에 값을 저장해야 합니다.

그러므로, `PostSerializer`의 형식과 동일한 형태의 `post_data`를 생성합니다.

`PostSerializer`의 결과를 저장한 `post_serializer`를 생성합니다.

여기서, `self.get_serializer`을 사용해도 무방하지만 직관적으로 이해하기 위해 `PostSerializer`를 사용하도록 하겠습니다.

`*.is_valid()` 메서드로 유효성을 확인합니다. 유효하다면 `post_serializer.save()`를 통해 데이터베이스에 값을 저장합니다.

`post_result`는 저장된 결과를 반환합니다.



```
comment_data = {
    "post_id": post_result.id,
    "contents": request.data["post"]["contents"],
}
comment_serializer = CommentSerializer(data=comment_data)
if comment_serializer.is_valid(raise_exception=True):
    comment_serializer.save()
    return Response({"message": "Operate successfully"}, status=status.HTTP_201_CREATED)
```

앞선 방식과 동일한 방식으로 한 번 더 반복합니다.

단, `comment` 테이블은 외래키인 `post_id` 값을 필요로 합니다.

그러므로, `post` 테이블에 값을 저장하면서 발생한 `id` 값을 가져와 `post_id` 필드의 값으로 사용합니다.

정상적으로 저장된다면, `Response`을 통해 성공 결과를 반환합니다.



```
return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)
```

요청 결과가 실패했을 때에도 `Response`을 통해 실패 결과를 반환합니다.

`post` URL로 이동하여 결과를 조회한다면 정상적으로 두 테이블에 저장된 것을 확인할 수 있습니다.



## 제 13강 - Transaction


### Django Transaction

`트랜잭션(Transaction)`이란 **데이터베이스의 상태를 변환**시키려는 작업의 단위를 의미합니다.

트랜잭션의 목적으로는 **데이터베이스 완전성(integrity) 유지**에 있습니다.

또한, 트랜잭션은 아래와 같은 네 가지의 성질을 갖고 있습니다.

```plaintext
  Atomicity(원자성)
```


  - 트랜잭션 연산은 데이터베이스에 모두 반영되거나 모두 반영되지 않아야 합니다.
  - 트랜잭션 내의 모든 명령은 완벽히 수행되어야 하며, 하나라도 오류가 발생한다면 모두 트랜잭션 전부가 취소되어야 합니다.

```
  Consistency(일관성)
```

  - 트랜잭션이 실행을 성공적으로 완료한다면 일관성 있는 데이터베이스 상태로 변환합니다.
  - 트랜잭션 수행 전과 수행 후의 상태가 같아야 합니다.

```plaintext
  Isolation(독립성)
```

  - 둘 이상의 트랜잭션이 동시에 실행되는 경우, 어느 하나의 트랜잭션 실행 중에 다른 트랜잭션의 연산이 끼어들 수 없습니다.
  - 수행 중인 트랜잭션은 완전히 종료될 때까지 다른 트랜잭션에서 수행 결과를 참조할 수 없습니다.

```plaintext
  Durablility(지속성)
```

  - 성공적으로 완료된 트랜잭션의 결과는 시스템이 고장나더라도 영구적으로 반영되어야 합니다.

즉, 트랜잭션 내의 작업은 모든 작업이 정상적으로 완료되면 데이터베이스에 **반영(commit)**하거나, 일부 작업이 실패한다면 실행 전으로 **되돌려야(rollback)**합니다.

앞선 12강의 외래키 예제로 설명한다면, `post` 테이블과 `comment` 테이블에 한 번에 데이터를 입력했습니다.

여기서, `post` 테이블에는 정상적으로 값이 등록됬지만, `comment` 테이블에 데이터를 저장할 때 오류가 발생했다면 `post` 테이블에만 값이 저장됩니다.

이는 의도한 바가 아니기 때문에 되돌리는 작업이 필요합니다.

여기서 오류가 발생했다고 `post` 테이블의 데이터를 삭제하는 것이 아닌, `롤백(rollback)`을 실행합니다.

이를 위해 사용하는 것이 트랜잭션입니다.



![img](https://076923.github.io/assets/posts/Python/Django/lecture-13/1.webp)

앞선 예제를 변경하지 않고, 위와 같이 `post` 필드 내부의 값이 문제가 있다면 오류를 반환하지만 데이터베이스에서는 `Post` 데이터와 관련된 데이터는 저장됩니다.

`post` URL로 이동해서 결과를 확인해본다면, 아래와 같이 결과가 저장된 것을 확인할 수 있습니다.



![img](https://076923.github.io/assets/posts/Python/Django/lecture-13/2.webp)

오류가 발생했지만, `post` 테이블에는 값이 저장된 것을 확인할 수 있습니다.

앞선 코드를 통해 확인해본다면 왜 이런 현상이 발생했는지 알 수 있습니다.



#### views.py

```
def create(self, request, *args, **kwargs):
    post_data = {
        "title": request.data["title"],
        "contents": request.data["contents"],
    }
    post_serializer = PostSerializer(data=post_data)
    if post_serializer.is_valid(raise_exception=True):
        post_result = post_serializer.save()

        comment_data = {
            "post_id": post_result.id,
            "contents": request.data["post"]["contents"],
        }
        comment_serializer = CommentSerializer(data=comment_data)
        if comment_serializer.is_valid(raise_exception=True):
            comment_serializer.save()
            return Response({"message": "Operate successfully"}, status=status.HTTP_201_CREATED)

    return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)
```

코드 상에서 `request.data`를 파싱하여 `PostSerializer`에 대해서만 먼저 유효성을 검사합니다.

유효하다면, `post_serializer.save()`을 통해 데이터베이스에 값을 저장합니다.

이후, `comment_data`에서 `contents` 필드에 `request.data["post"]["contents"]`를 가져오지만, 요청 데이터는 `contents` 필드 대신, `error`로 전혀 다른 필드가 작성되어 있습니다.

이때, 오류가 발생하여 코드가 중단됩니다.

별도의 예외처리를 통해 오류 구문 없이 결과를 출력할 수는 있지만, 이미 `post` 테이블에 저장된 값은 되돌릴 수 없습니다.

이때, 트랜잭션을 추가해 해결할 수 있습니다.





### Django Transaction 구현

#### views.py

```
from django.db import transaction

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from blog.models import Post
from blog.models import Comment
from blog.serializers import PostSerializer
from blog.serializers import CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @transaction.atomic(using='default')
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                post_data = {
                    "title": request.data["title"],
                    "contents": request.data["contents"],
                }
                post_serializer = PostSerializer(data=post_data)
                if post_serializer.is_valid(raise_exception=True):
                    post_result = post_serializer.save()

                    comment_data = {
                        "post_id": post_result.id,
                        "contents": request.data["post"]["contents"],
                    }
                    comment_serializer = CommentSerializer(data=comment_data)
                    if comment_serializer.is_valid(raise_exception=True):
                        comment_serializer.save()
                        return Response({"message": "Operate successfully"}, status=status.HTTP_201_CREATED)
        except:
            pass

        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
```

먼저, `from django.db import transaction` 모듈을 추가해 트랜잭션 기능을 불러옵니다.

트랜잭션을 적용할 메서드 위에 트랜잭션 `데코레이터(Decorator)`를 추가합니다.

예제와 같이 `def create()`위에 `@transaction.atomic(using='default')` 구문을 추가합니다.

다음으로 `try-except`를 통해 어떤 오류가 발생하더라도 마지막 `Response`으로 전달되도록 구성합니다.

트랜잭션이 적용되야할 구문에는 `with transaction.atomic():`의 구문을 추가해 트랜잭션이 적용될 블록을 구성합니다.

여기서 주의해야할 점은 크게 두 가지가 있습니다.



#### try-except 사용

트랜잭션 코드는 `with` 구문안에서 오류가 발생했을 때, `롤백(rollback)`을 적용합니다.

그러므로, `with` 구문안에 `try-except`를 적용한다면 정상적인 과정으로 인식하여 롤백되지 않습니다.



#### raise_exception 사용

`try-except`와 마찬가지로, `serializer.is_valid`의 **raise_exception** 매개변수의 인수는 `True`로 사용해야합니다.

유효성을 검사할 때 `raise_exception`이 `False`라면 오류를 발생시키지 않아, 정상적인 과정으로 인식하여 롤백되지 않습니다.



간단하게 설명하자면, `with transaction.atomic():` 구문은 예외가 발생했을 때, 롤백하는 과정만 가지고 있습니다.

롤백하는 과정만 가지고 있기 때문에, `try-except`와는 다른 역할입니다.

즉, `request.data["post"]["contents"]`를 불러올 때 `contents` 필드가 없어서 발생하는 오류는 `try-except`를 통해 별도로 잡아주어야 합니다.

그렇기 때문에 가장 상단에 `try-except`를 추가하여, `return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)`으로 이동합니다.


트랜잭션을 적용한 다음, `POST` 요청을 해보도록 하겠습니다.

`try-except`을 통하여 오류가 발생했을 때, 정상적인 오류 메세지가 전달되며, 데이터베이스에도 값이 저장되지 않는 것을 확인할 수 있습니다.

복합적으로 데이터베이스에 값을 저장한다면, 트랜잭션 기능을 적용하거나 별도의 함수를 생성하여 오류를 처리해야 합니다.

만약, 트랜잭션이나 별도의 함수를 구현하지 않는다면 **데이터베이스에 저장된 값을 신뢰할 수 없는 상태**가 됩니다.

