### TA-lib 설치하기 간단 사용기, python, talib, ta-lib

출처: https://swlock.blogspot.com/2022/01/ta-lib-python-talib-ta-lib.html



## TA-Lib

TA-Lib은 금융 시장 데이터의 기술적 분석을 수행하는데 필요한 멀티플랫폼 라이브러리 입니다.

## 1. 공식 홈페이지

http://ta-lib.org/

https://mrjbq7.github.io/ta-lib/ Python wrapper



## 2. 설치 방법

python의 경우 pip로 설치가 되지 않습니다.



### 2.2 다른사람이 컴파일된 파일 사용

https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

자신의 python 버전과 같은 파일을 다운로드 해줍니다. 64bit는 amd64, 32bit는 win32

이것은 python을 실행시키면 어떤 python인지 나옵니다.

제가 사용하는 python은 64bit 3.8 입니다.

그래서 다음 파일을 다운로드 받았습니다. 

```
Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:37:02) [MSC v.1924 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> ^C
```

**TA_Lib‑0.4.24‑cp38‑cp38‑win_amd64.whl**

그리고 **pip install <다운로드한 whl 파일>** 을 적어줍니다.

```
pip install C:\Users\USER\Downloads\TA_Lib-0.4.24-cp38-cp38-win_amd64.whl
Processing c:\users\user\downloads\ta_lib-0.4.24-cp38-cp38-win_amd64.whl
Requirement already satisfied: numpy in c:\users\user\appdata\local\programs\python\python38\lib\site-packages (from TA-Lib==0.4.24) (1.19.5)
Installing collected packages: TA-Lib
Successfully installed TA-Lib-0.4.24
```

``` sh
pip install TA_Lib-0.4.24-cp38-cp38-win_amd64.whl
```





### 2.1 직접 컴파일하는 방법

#### 2.1.1 컴파일러 설치

Windows라면 Visual Studio 를 설치해야합니다. 

링크가 새버전이 나오면 변경되는 경우가 많습니다. 무료 버전을 설치합니다.

https://visualstudio.microsoft.com/ko/downloads/ 여기에서 VC 설치합니다.

리눅스라면 g++ 컴파일러를 설치하면 됩니다.

#### 2.1.2 소스 받기

소스는 https://ta-lib.org/hdr_dw.html 여기에서 받습니다.

**Windows**

Download ta-lib-0.4.0-msvc.zip and unzip to C:\ta-lib



**Linux**

Download ta-lib-0.4.0-src.tar.gz and:

$ untar and cd

$ ./configure --prefix=/usr

$ make

$ sudo make install

If you build TA-Lib using make -jX it will fail but that's OK! Simply rerun make -jX followed by [sudo] make install.



#### 2.1.3 설치

``` sh
pip install ta-lib
```







만약 2.1.2가 제대로 설치 안된 경우 오류 문구가 이렇습니다.

... 생략 ...

 _ta_lib.c

 talib/_ta_lib.c(680): fatal error C1083: Cannot open include file: 'ta_libc.h': No such file or directory

 error: command 'C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\BIN\\x86_amd64\\cl.exe' failed with exit status 2

 \----------------------------------------

 ERROR: Failed building wheel for ta-lib





## 3. 간단 테스트

이동 평균을 구하는 간단한 테스트 입니다.

```python
import numpy
import talib

close = numpy.random.random(100)
output = talib.SMA(close)
print(output)
```

random이라 수치는 변하지만 앞쪽에 데이터가 nan 으로 나오는것으로 보아 정상적으로 출력되었습니다.



### 이동평균선 구하기

talib을 설치했다면 여느 라이브러리와 마찬가지로 import를 해주어야 한다. 그 후 이동평균선을 제작하는 방법은 talib.MA(데이터프레임['칼럼명'], 기간)을 입력하면 된다. 아래의 예시를 참고해보자.
※ 물론 dataframe이라는 데이터 안에 'close'와 'high'라는 칼럼이 있어야 사용할 수 있다.
※ dataframe 안에 있는 칼럼명을 확인하고 싶다면 print()문을 사용해서 확인해보면 된다.

- 종가 기준 10일 이동평균선 : talib.MA(dataframe['close'], 10)
- 종가 기준 20일 이동평균선 : talib.MA(dataframe['close'], 20)
- 고가 기준 10일 이동평균선 : talib.MA(dataframe['high'], 10)