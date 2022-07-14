# Python-UIAutomation

출처: https://velog.io/@chacha/Autoit-Python-Autoit-%EC%84%A4%EC%B9%98-%EB%B0%8F-%EC%8B%A4%ED%96%89



## 1. Python-UIAutomation-for-Windows 이란?

초기버전 windows의 GUI객체 컨트롤은 [Autoit](https://www.autoitscript.com/site/)으로 모두 조작이 가능하였다, 하지만 Windows버전이 올라감에 따라 새로운 UI요소를 그릴 수 있는 Library가 공개되었고 그 것이 .Net Framework임, 현재 사용중인 대부분의 창은 .Net Framework 3.0이후의 버전을 사용해서 그려지고 있다.

이에 따라 Microsoft에서는 .Net Framework의 GUI객체 컨트롤을 위해서 [UIAutomation API](https://docs.microsoft.com/en-us/windows/win32/winauto/entry-uiauto-win32)를 공개하였고, 이번에 소개할 Python-UIAutomation-for-Windows는 UIAutomation API를 Python에서 사용할 수 있도록 하게 해주는 Library이다

### 그리고..

현재 대부분의 **RPA**(Robotic Process Automation)툴 특히 Windows기반의 툴들은 UIAutomation API를 기반으로 만들어져있다

### 그래서 이번 편에서...

Python에서 UIAutomation API를 사용할 수 있게 해주는 Python-UIAutomation-for-Windows의 사용법을 소개한다

#### 설치방법(Python기준)

1. Win32com 설치 ※ 간혹 있는 오류를 위한 사전작업
   정상적인 경우면 필요 없지만 간혹 Python에서 Com object를 조작하는에 오류가 발생한다.
   Win32com을 설치 할 경우 그런 오류를 해결할 수 있다

- [설치 url](https://sourceforge.net/projects/pywin32/files/?source=navbar) 클릭
  ![img](https://media.vlpt.us/post-images/chacha/b7b32d10-3545-11ea-976b-1f1fc7000e0b/image.png)
- 최신빌드버전 클릭 ※ 2020년1월기준 최신버전은 `Build 221`
  ![img](https://media.vlpt.us/post-images/chacha/fcc6e450-3545-11ea-976b-1f1fc7000e0b/image.png)
- 본인 Python버전에 맞는 파일 다운 ※ 필자는 python3.6버전 이므로 `pywin32-221.win-amd64-py3.6.exe`파일 다운로드
  ![img](https://media.vlpt.us/post-images/chacha/356b2aa0-3546-11ea-976b-1f1fc7000e0b/image.png)
- 관리자 권한으로 파일 실행 후 Next연타
  ![img](https://media.vlpt.us/post-images/chacha/716aa9e0-3546-11ea-976b-1f1fc7000e0b/image.png)
- 만약 설치 결과 화면이 다음과 같으면 설치가 정상적으로 안된것
  ![img](https://media.vlpt.us/post-images/chacha/aea8c3a0-3546-11ea-976b-1f1fc7000e0b/image.png)
- 이때는 CMD를 관리자 권한 으로 실행
  ![img](https://media.vlpt.us/post-images/chacha/eb8d24a0-3546-11ea-976b-1f1fc7000e0b/image.png)
- Python설치 폴더내 `Scripts`폴더로 이동 후 `python pywin32_postinstall.py -install`명령어 수행
  ![img](https://media.vlpt.us/post-images/chacha/5e8d7360-3547-11ea-a59e-81eff5f5125a/image.png)

1. pip로 library 설치하기
   이 명령어도 되도록 이면 관리자 CMD창을 열어서 실행할 것!

```shell
pip install uiautomation
```

1. [inspect.exe](https://docs.microsoft.com/zh-cn/windows/desktop/WinAuto/inspect-objects) 내려받기
   [다운로드](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows/raw/master/inspect/InspectX86.exe)
2. Pycharm에서 Sample스크립트 짜보기 ※ 가장 흔한 `계산기`어플 샘플만들어 보기

- 계산기 실행을 위해서 subprocess import 및 계산기 실행

  ```python
  import subprocess
  subprocess.Popen('calc.exe')
  ```

- 실행결과
  ![img](https://media.vlpt.us/post-images/chacha/4d01cdb0-3549-11ea-b9cf-912c8745031c/image.png)

- inspect.exe 실행 후 객체 확인하기
  프로그램 실행 후 마우스를 가져다 대면 인식 된 객체의 정보가 표시된다
  ![img](https://media.vlpt.us/post-images/chacha/48847100-354b-11ea-bcf4-758f8218b6ea/image.png)
  정보를 해석해 보면 해당 객체는 `계산기` 창 이하에 `"1" 단추`이고 이 단추는 오른쪽 텝에 관련된 속성값을 가진 Element로 볼 수 있다

- 확인 된 정보를 통해서

   

  ```
  계산기
  ```

  의

   

  ```
  숫자1
  ```

  번 버튼 클릭하기

  \* uiautomation을 auto로 import하기

  ```null
  import uiautomation as auto
  ```

  ```null
  * 계산기 창을 조작하기 위해서 계산기 창을 찾고 해당 객체값을 반환
  ```

  ```null
  calculator = auto.WindowControl(searchDepth=1, Name='계산기')
  ```

  위의 값중 searchDepth값이 중요한데...

  ※ searchDepth란?

   

  Github페이지

  에 다음과 같이 Depth에 대해서 설명한다

  아래그림에서..

  ```
  0 depth
  ```

  는 Desktop윈도우의 객체 영역으로 우리가 잘 알고 있는 시작메뉴 Bar같은 영역이고

  ```
  1 depth
  ```

  는 Desktop윈도우 위에 떠있는

   

  ```
  창
  ```

  우리가 실행 시킨 프로그램의

   

  ```
  창
  ```

   

  영역

  ```
  n depth
  ```

   

  inspect.exe를 실행한 후 Tree구조상에 하위 레벨을 확인하여 어디까지 검색할 지 범위를 지정한다

  

  \* 계산기 창이 확인될때까지 총 3초를 1초간격으로 확인하기 못찾을 경우 못찾았다는 메시지와 함께 종료

  ~~~null
  ```
  if not calculator.Exists(3, 1):
  	print('Can not find Calculator window')
  	exit(0)
  ```
  * calculator의 `1번`버튼을 클릭
  앞선 객체 정보에서 보면 `1번`버튼은 다음과 같은 속성을 가지고 있다
  ~~~

  

  이 중 중요한 정보는 객체가 Button속성이라게 중요하고, Name값이

   

  ```
  1
  ```

  이라고 표시된 것이 중요하다

  그래서 이 정보를 가지고 앞서 선언한 calculator객체에 Button속성의 Child검색을 수행한다

  ~~~null
   ```
   calculator.ButtonControl(Name="1").Click()
   ```
   수행결과    
  ~~~

  

  소스 정보 :

   

  https://github.com/jjunghyup/UIAutomationExample/blob/master/calculator_sample.py



## 2. Python-UIAutomation-for-Windows - 스크립트작성

### 스크립트 작성하기에서는

이번편에서는 Python-UIAutomation-for-Windows의 library에서 필요할 만한 기능을 설명한다

### 테스트 시나리오

이번편 부터는 자동화 테스트 시나리오를 작성하고 그 시나리오에 맞춰서 스크립트를 작성해본다.
추후에 디테일하게 개인적으로 생각하는 자동화 테스트 시나리오에 필요한 요소를 따로 설명할 예정이다
이번편에서는 간단하게 `테스트데이터`, `Step`, `기대결과`요렇게만 활용할 예정이다

### 샘플 시나리오 : `GIT GUI`툴을 통해서 Clone받기

간단하게 뚝딱 뚝딱 완성
![img](https://media.vlpt.us/post-images/chacha/85f87c50-35a2-11ea-9f92-e31b994ddfc1/image.png)

### Script작성

1. Script파일 생성
   이제부터는 수행 시 pytest를 활용할 예정이다
   그래서 파일이름을 `gitguit_test.py`로 파일이름에 python test코드는 파일 이름에 `test`를 입력한다
   파일에 테스트 수행 용 function을 만들고, assert Fail구문을 입력
   ![img](https://media.vlpt.us/post-images/chacha/031b7060-35a4-11ea-b153-092fccac3603/image.png)
2. 실행해보기
   python파일을 만들면 기본적으로 python으로 실행되서 assert문이 동작하지 않음, pytest로 수행하기 위해서는. function이름에서 `마우스 우클릭 → GO TO → Test` 클릭
   이후 Function왼쪽의 `Run` Icon클릭
   ![img](https://media.vlpt.us/post-images/chacha/9e7a8640-35a4-11ea-b153-092fccac3603/image.png)
   실행결과
   ![img](https://media.vlpt.us/post-images/chacha/c221b8c0-35a4-11ea-8d2c-ebc880386303/image.png)
3. 스크립트에 시나리오 내용을 주석으로 표시
   ![img](https://media.vlpt.us/post-images/chacha/49bc13c0-35a5-11ea-a60a-3ff424a0d6de/image.png)
4. 스크립트 작성 시작!

- Clone 대상 폴더 존재여부 확인

  python에서 폴더 존재 확인은

   

  ```
  os
  ```

  를 통해서 수행한다

  일일이 GUI로 확인해도되지만 절차가 많아져서 이걸로 수행

  ```null
    # Clone폴더 값 정의
    clone_folder = "C:\\dev\\git\\UIAutomationExample"
    # Clone 대상 폴더가 존재할 경우 폴더를 지운다.
    import os
    if os.path.exists(clone_folder):
        os.system('rmdir /S /Q "{}"'.format(clone_folder))
        
    # Clone 대상 폴더가 없는지 확인한다.
    if os.path.exists(clone_folder):
        assert False, "clone대상폴더가 지워지지 않음"
  ```

- GIT GUI실행시키기

  inpect.exe를 통해서 검색 영역의 속성을 확인하기

  왼쪽의 Tree를 보면 검색영역은 3depth인걸 확인할 수 있고, 이후 오른쪽의 세부 속성을 보면 Button속성의 Name값이

   

  ```
  검색하려면 여기에 입력하십시오.
  ```

  인 걸 확인할 수 있다.

  

  위의 값을 통해 검색 버튼을 클릭하는 스크립트를 다음과 같이 작성할 수 있다.

  ```null
  import uiautomation as auto
  auto.ButtonControl(searchDepth=3, Name='검색하려면 여기에 입력하십시오.').Click()
  ```

  gui입력 후 파일 실행 아이콘을 inspect로 확인하면 왼쪽의 tree에는 나타나지 않는것을 확인 할 수 있다. 이럴때는 depth속성을 좀 많이 주면 element가 찾아지는 경우가 있다.

  ```null
  auto.TextControl(searchDepth=10, Name="Git GUI").Click()
  ```

  

  GIT GUI수행 후 확인까지 스크립트

```null
    import uiautomation as auto
    # 검색영역 클릭하기
    auto.ButtonControl(searchDepth=3, Name='검색하려면 여기에 입력하십시오.').Click()
    # 검색영역에 값 입력하기
    auto.EditControl(searchDepth=3, Name='검색 상자').SendKeys('git gui')
    # Git GUI아이콘 클릭하기
    auto.TextControl(searchDepth=10, Name="Git GUI").Click()
    # Git GUI가 정상적으로 수행되었는지 확인
    auto.WindowControl(searchDepth=1,  Name="Git Gui")
```

- Clone repository 수행하기

  원래 계획은 창안의

   

  ```
  Clone Existing Repository
  ```

  을 크릭하려고 하였으나 해당 객체는 inpect가 되지 않고 바로 상위의 객체만 조작이 됨. 이런 경우 해당 객체를 클릭할 수 없어서 계획을 수정해서 상단의 메뉴를 통해서 clone을 수행한다

  

  메뉴를 통한 clone기능 수행 스크립트

  ```null
  # 상단 메뉴를 통해 Clone을 수행
  auto.MenuItemControl(searchDepth=8,  Name="Repository").Click()
  auto.MenuItemControl(searchDepth=8, Name="Repository")
  # inspect를 통해서 menu의 AutomationId가 48이므로 이를 활용
  auto.MenuItemControl(AutomationId = "48").Click()
   # 아쉽게도 해당 APP은 "Clone Existing Repository"에 대한 정보를 확인할 수 없는 앱이어서
    # 이후 동작으로 확인할 수 밖에 없다.
  ```

  앞선 스크립트에서 정상적으로 글씨가 있는지 확인 하고 싶었으나 inspect결과에서 보면 해당 화면의 값을 확인 할 수 있는 속성이 없고,

  화면안의 모든 객체는 단순히

   

  ```
  ClassName
  ```

  이

   

  ```
  TkChild
  ```

  인 것만 확인 가능하다. 이럴때는

   

  ```
  TkChild
  ```

  인 ClassName의 Index로만 객체를 조작 할 수 있다.

  아쉽게도 inspect.exe에서는 Index번호까지는 제대로 알수 없어서

  Autoit의

   

  au3info.exe

  를 통해서 index번호를 확인한다.

  확인결과 Target Directory의 Index는 11인것을 확인할 수 있다 이렇게 확인 된 정보로 이후 동작을 작성한다.

  

```null
    # Source location 및 Target Directory 값 정의
    source_location = "https://github.com/jjunghyup/UIAutomationExample.git"
    target_directory = "C:\\dev\\git\\UIAutomationExample"
    # Source Location값과 Target Directory값을 입력한다.
    auto.PaneControl(ClassName="TkChild", foundIndex=14).Click()
    auto.PaneControl(ClassName="TkChild", foundIndex=14).SendKeys(source_location)
    auto.PaneControl(ClassName="TkChild", foundIndex=11).Click()
    auto.PaneControl(ClassName="TkChild", foundIndex=11).SendKeys(target_directory)
    # 값이 정상적으로 입력된다.
    # 값을 Clipboard에 복사하고 붙여넣기 식으로 확인이 가능하지만 해당 내용은 이후에 작성 예정

    # Clone 버튼을 클릭한다.
    auto.PaneControl(ClassName="TkChild", foundIndex=18).Click()
    # Clone 대상폴더가 존재하는지 확인한다. 10초 동안 확인한다.
    result = False
    for i in range(0, 10):
        if os.path.exists(clone_folder):
           result = True

    assert result, "clone대상폴더가 존재 하지 않음"
```

스크립트 url : https://github.com/jjunghyup/UIAutomationExample/blob/master/gitgui_test.py



## 3. UIAutomator2(Android) - 설치 및 실행

### UIAutomator2란?

Android의 화면 객체를 조작할 수 있도록 Android쪽에서 API를 공개함 이 Library가 UIAutomator2이다. 이 Library를 조작해서 Android의 대부분의 UI영역을 조작 할 수 있음. 대표적인 Framework가 Appium으로 볼 수 있다.
하지만 이번에 소개하는 UIAutomator2는 Appium과 동작방식이 조금 다르다.

### 장점

Go로 만들어진 서버를 단말기에 설치하여 Script 동작 PC에서 단말기의 서버와 직접 통신을 하고, 수신을 받은 서버가 단말기에 설치된 UIAutomator2 Library를 조작하는 Agent APP과 JsonRPC통신을 하며 GUI영역을 조작한다.
이로 얻을 수 있는 장점은 그전의 Appium Server가 여러대의 단말을 조작하기 위해서는 Appium Server를 다수 띄워야했으나.
UIAutomator2는 그럴 필요가 없다
그리고 속도가 빠르다! appium은 초기단계 init과정에 시간이 많이 소요 되지만, uiautomator2는 init속도가 빨라서 스크립트가 바로 수행된다 → 수행시간 감소

### 다중단말 조작 원리 비교(Appium vs UIAutomator2)

![img](https://media.vlpt.us/post-images/chacha/d4135f80-35df-11ea-88d2-a9fa7581c13e/image.png)
![img](https://media.vlpt.us/post-images/chacha/dfe57f00-35df-11ea-bba3-0f62689ec185/image.png)

### 설치방법(Python기준)

1. ADB설치 및 핸드폰 연결방법
   폰마다 방법이 많이 달라서 Galaxy기준 설치방법만 링크한다
   [링크](https://library1008.tistory.com/26)
   정상적으로 설정을 했다면 `ADB devices`명령어 입력시 다음과 같이 표시되어야한다

![img](https://media.vlpt.us/post-images/chacha/cdd985c0-35e1-11ea-acc7-95560279424f/image.png)

1. ATX-Agent Build버전 내려받기
   Android Phone에 설치되는 Go서버 이름은 `Atx-agent`이다
   이 서버를 폰에 설치 하기 위해서는 Android 프로세스 버전에 맞는 설치 파일 압축파일을 내려받아야한다
   Download URL: https://github.com/openatx/atx-agent/releases
   단 대부분의 android폰은 arm7을 거의 공통적으로 지원하므로 arm7용 버전을 받으면 된다.
   ![img](https://media.vlpt.us/post-images/chacha/ea1144b0-35e3-11ea-bba3-0f62689ec185/image.png)
2. ADB에 연결된 Device에 Atx-agent서버 설치
   압축 해제 후 해당 폴더로 이동. 폴더에서 다음 명령어를 통해 연결된 Device에 Atx-agent서버 설치

```null
adb push atx-agent /data/local/tmp
adb shell chmod 755 /data/local/tmp/atx-agent
adb shell /data/local/tmp/atx-agent server -d
```

수행결과
![img](https://media.vlpt.us/post-images/chacha/57a2a060-36ce-11ea-a83e-7b4ac9f8f1f8/image.png)
위의 그림에서 보면 마지막 명령어 수행결과 `7912포트`로 서버가 수행된걸 확인 할 수 있다
정상 설치 여부 확인 - 7912포트로 서비스가 되는지 확인

```null
adb shell
netstat -anp | grep 7912
```

![img](https://media.vlpt.us/post-images/chacha/5e444710-35e4-11ea-84b3-8706ccec3b0b/image.png)

1. UIAutomator2 Library설치
   관리자 CMD창을 열고 다음 명령어 입력

   > pip install -U uiautomator2

2. ADB에 연결된 Device에 UIAutomator2 설치하기 or 연결하기
   Python명령 수행

```null
import uiautomator2 as u2
d = u2.connect() # connect to device
print(d.info)
```

수행결과 스크립트 수행에 필요한 파일이 정상설치된것을 확인할 수 있다
![img](https://media.vlpt.us/post-images/chacha/9c9c3540-35e4-11ea-9a5e-ef951fdfed88/image.png)
위에서 선언한 `d`객체를 통해서 핸드폰에 명령을 수행다
스크립트 작성방법은 다음 글에서...

설치스크립트 url : https://github.com/jjunghyup/UIAutomator2Sample/blob/master/install_to_device.py



## 4. UIAutomator2(Android) - 스크립트 작성해보기

### 스크립트 작성하기에서는

이번편에서는 Android Device에서 내가 조작하고자 하는 Element를 찾고, 이를 조작하는 방법에 대해서 소개한다.

### 테스트 시나리오

이번편에서도 자동화 테스트 시나리오를 작성하고 그 시나리오에 맞춰서 스크립트를 작성한다.
의식이 선택하는 테스트 대상앱은
두구두구두구!!
`캘린더` 앱으로 선정!

### 샘플 시나리오 : 캔린더앱의 달력 추가하고 확인하기!

뚝딱 뚝딱 완성!
![img](https://media.vlpt.us/post-images/chacha/c210ff00-35e8-11ea-a326-d919509547d4/image.png)

### Script작성

1. Script파일 생성
   calendar_test.py 생성 후 실패코드 넣기
   ![img](https://media.vlpt.us/post-images/chacha/14ee6000-35e9-11ea-92f1-f5e3bde93660/image.png)
2. 시나리오 내용을 주석으로 넣기
   ![img](https://media.vlpt.us/post-images/chacha/6c1e7950-35e9-11ea-8994-7308493f5f51/image.png)
3. weditor
   openatx쪽에서 만든 android inspect툴
   설치 방법

```null
pip3 install --upgrade weditor
```

실행방법 CMD창에서 `weditor` 실행

```null
weditor
```

실행결과 CMD에 서버를 하나 실행한다
![img](https://media.vlpt.us/post-images/chacha/fc1c1660-35ea-11ea-a873-37cc22caffcc/image.png)
실행됨과 동시에 기본 Browser에 창이 열리고, inspect서버 주소가 입력된다([http://localhost:17310](http://localhost:17310/))
![img](https://media.vlpt.us/post-images/chacha/47bce590-35eb-11ea-9a5e-ef951fdfed88/image.png)

- 연결하기
  Connect 왼쪽의 입력란에 DeviceID(adb devices입력시 나오는 값) 또는 단말기의 atx서버 주소(ip:7912)를 입력한다.
  ![img](https://media.vlpt.us/post-images/chacha/92c32270-35eb-11ea-b8a5-3d692e45a03f/image.png)
- Dump Hierarchy
  `Connect`우측의 `Dump Hierarchy` 버튼 클리시 다음과 같이 Screen Shot이 나오고 관련정보가 표시된다.
  그 Screenshot의 화면에서 아이콘을 클릭해 보면 다음과 같이 정보가 표시되고, 이중 Xpath정보를 많이 사용한다.
  ![img](https://media.vlpt.us/post-images/chacha/de6b3c40-35f9-11ea-ba19-fd3c1fe5de58/image.png)

1. Script작성하기

- 연결 된 device중 내가 지정한 단말에 접속한다.

  ```null
    # device_id정의
    device_id = "ce031713d239a82002"
    # 핸드폰을 연결한다.
    import uiautomator2 as u2
    device = u2.connect(device_id)
    # 정상적으로 연결된다.
    assert not device.alive, "디바이스가 정상적으로 연결되지 않았습니다."
  ```

- 홈 화면 연결 후 `Calendar`앱 실행
  앱 실행을 위해서는 package명이 필요함, package명은 프로그램 실행 후 Dump Hierarchy실행 후 element를 클릭 하면 알수 있다
  ![img](https://media.vlpt.us/post-images/chacha/e7396dc0-35fd-11ea-a6f1-8d3a99424b4e/image.png)
  해당 정보를 통해 APP실행 후 정상 실행 여부 확인!

```null
    # 캘린더 앱을 실행한다.
    app_package = "com.samsung.android.calendar"
    device.app_start(app_package)
    # 프로그램이 정상적으로 수행된다.
    pid = device.app_wait(app_package, timeout=20.0)
    if not pid:
        print("com.example.android is not running")
        assert False, f"{app_package}가 정상적으로 수행되지 않았습니다."
```

- 신규 일정 등록하기

  일정 버튼, 화면 입력란 등등의 element값을 inspect툴로 확인 후 스크립트 작성하기!

  일정추가 버튼 정보

  

  일정 제목 입력 란 정보

  

  저장 버튼 정보

  

  스크립트

  ```null
      # 할일이름값을 정의한다.
    import time
    task_name = f"{time.time()}_할일"
    # 새로운 일정을 등록한다.
    # 일정등록 버튼 클릭
    d.xpath('//*[@resource-id="com.samsung.android.calendar:id/floating_action_button"]').click()
    # 일정 제목에 내용 입력
    d.xpath('//*[@resource-id="com.samsung.android.calendar:id/title"]').set_text(task_name)
    # 저장 버튼 클릭
    d.xpath('//*[@resource-id="com.samsung.android.calendar:id/action_done"]').click()
  ```

- 일정 정상 등록 여부 확인하기
  일정이 정상적으로 등록되었는지 확인하기 위해서 오른쪽 위의 더보기 아이콘 xpath정보로 click()을 수행해보았지만 수행되지 않는다!
  ![img](https://media.vlpt.us/post-images/chacha/06fba110-3602-11ea-b333-b13bdd39ea1a/image.png)
  이를 해결하기 위해서 uiautomator에서는 잘 찾아지는 element의 위/아래/왼쪽/오른쪽의 elemet를 지정할 수 있다.
  그래서 잘 찾아지는 `보기 방식`버튼을 찾은 후 그 오른쪽 element를 지칭하는 script는 다음과 같다.
  uiautomator에서는 다양한 방식을 통해서 element를 찾을 수 있게 지원한다

```null
d(text="보기 방식").right(className='android.widget.FrameLayout').click()
```

이 방식을 사용해 이후 스크립트를 작성

```null
    # 일정이 정상적으로 등록되었는지 확인한다.
    # 더보기 버튼 클릭
    d(text="보기 방식").right(className='android.widget.FrameLayout').click()
    # 검색 버튼 클릭
    d.xpath('//android.widget.ListView/android.widget.LinearLayout[1]').click()
    # task_name으로 검색
    d(resourceId="android:id/search_src_text").send_keys(task_name)
    # task_name element존재 여부 확인
    d(resourceId="com.samsung.android.calendar:id/title", text=task_name).exists()    
```

수행 결과
![img](https://media.vlpt.us/post-images/chacha/03b14620-3604-11ea-a3a0-3137f7e00132/image.png)

스크립티 url : https://github.com/jjunghyup/UIAutomator2Sample/blob/master/calendar_test.py



## 5. UIAutomator2(Android) - 동시단말 조작 및 자주 겪는 이슈

### 이번편에서는

UIautomator2를 활용한 동시 단말 조작 방법 및 자주겪는 이슈들에 대해서 소개한다.

### UIAutomator2의 동작원리

PC에서 `UIAutomator2 Library`통해서 자동으로 연결(ADB 및 network연결)방법을 설정해서 단말기에 설치된 `Atx-agent서버(7912)`포트에 단말 조작 명령을 전달한다. 이 내용을 `Atx-agent`는 단말기에 설치된 `UIAutomator2 전용 APP`과 JsonRPC방식을 통해 수행결과를 통신한다.
결국 단말기와 통신을 위해서는 `단말IP:7912`에 접근할 수 있는 환경이 구성되어야 한다.
![img](https://media.vlpt.us/post-images/chacha/3d5e49d0-36c8-11ea-8840-dfccc1fc9b1c/image.png)
구체적인 연결방법을 설명하려면 우선 UIAutomator2가 어떤방식으로 단말과 연결하는지 살펴봐야 한다.
UIAutomator2에서 단말과 조작하기 위해서 `u2.connect()` function을 사용하였다.
해당 function의 소스를 살펴보면

```null
def connect(addr=None):
    """
    ...
    (생략)
    ...
    if wifi_addr:
        return connect_wifi(addr)
    return connect_usb(addr)
```

입력된 주소가 `ip address(x.x.x.x)`형식이면 `connect_wifi`를 수행하고, 아니라면 `usb연결`방법을 수행한다. 이점을 확인한 상태에서 동시단말을 조작하는 방법들을 소개한다.

1. 단말ID를 통한 접근
   `adb devices`를 수행한 후 얻게되는 ID값이 다음과 같다면

```null
> adb devices
List of devices attached
ID1xxxxxxxxxxxxxxx     device
ID2xxxxxxxxxxxxxxx     device
```

다음과 같이 2개의 device를 연결할 수 있다.

```null
device1 = u2.connect('ID1xxxxxxxxxxxxxxx')
device2 = u2.connect('ID1xxxxxxxxxxxxxxx')
```

1. wifi를 통한 접근
   앞선 atx-agent 서버를 수행하였을 때 7912포트에 서버가 구동된다고 설명했었다.
   연결을 원하는 device가 wifi로 연결이 되어있다면, device에 ip가 부여되었다고 볼 수 있다. 부여된 device ip는 대체로 공유기 내부의 ip가 부여된다.
   같은 내부IP에 존재하는 pc에서는 별도의 방화벽이 없다면 Network로 접근 할 수 있다.
   만약 부여된 내부IP가 다음과 같다면

```null
device1 = 192.168.1.100
device2 = 192.168.1.101
```

다음과 같이 2개의 device를 연결할 수 있다.

```null
device1 = u2.connect('192.168.1.100:7912')
device2 = u2.connect('192.168.1.101:7912')
```

1. ADB를 통한 portfowarding
   만약 단말기가 wifi에도 연결되어 있지 않고, 외부에서 PC에 연결된 단말기를 조작하고 싶다면.
   ADB의 `port forwarding`기능을 통해서 PC에 연결된 단말의 7912포트로 접속 할 수 있다.
   단말의 device가 다음과 같다고 가정하고..

```null
> adb devices
List of devices attached
ID1xxxxxxxxxxxxxxx     device
ID2xxxxxxxxxxxxxxx     device
```

외부에서 접속이 가능하도록 `Port fowarding`을 위해서는 ADB를 종료하고 `-a nodaemon server start`모드로 수행해야 한다.

```null
> adb kill-server
> adb -a nodaemon server start
```

그렇게 하면 `adb forward`수행 시 외부에서 pc의 device에 접근 할 수 있다.
이 방법을 통해서 2개 device에 연결은 다음과 같이 할 수 있다.
기존의 cmd창은 서버가 구동되고 있으니.
새로 cmd창을 열고
먼저 port forward를 통해 pc의 `7912`포트와 단말의 `7912`포트를 연결한다.

```null
adb -s ID1xxxxxxxxxxxxxxx forward tcp:7912 tcp:7912
```

두번재 단말은 `7913`으로 연결한다 다음과 같이

```null
adb -s ID1xxxxxxxxxxxxxxx forward tcp:7912 tcp:7913
```

이렇게 정의한 단말 2개를 다음과 같이 연결할 수 있다.

```null
device1 = u2.connect('<PC_IP>:7912')
device2 = u2.connect('<PC_IP>:7913')
```

### 자주 겪는 이슈들

1. 잘되던 자동화가 갑자기 수행되지 않을때 확인할 사항

   - Atx-agent가 구동되고 있는지 확인한다.

     단말기에

      

     ```
     shell
     ```

     을 통해서 접속 후

      

     ```
     netstat -anp | grep 7912
     ```

     를 수행해 본다.

     7912로 listen받고 있다면 atx-agent는 정상구동된걸 확인할 수 있다.

     만약 구동되는 서비스가 없다면 다시 atx-agent를 구동한다.

     ```null
     adb shell /data/local/tmp/atx-agent server -d
     ```

   - 만약 Atx-agent가 구동되는데도 실행이 안된다면..UIAutomator2앱의 강제 시작 버튼 클릭
     단말기에 설치된 자동차모양의 앱을 실행
     ![img](https://media.vlpt.us/post-images/chacha/f0e4b7c0-36d0-11ea-8f84-dd6972fc9032/image.png)
     실행 버튼 클릭
     ![img](https://media.vlpt.us/post-images/chacha/0fd16f70-36d1-11ea-8177-1b36684cce7d/image.png)

2. 추가 예정



