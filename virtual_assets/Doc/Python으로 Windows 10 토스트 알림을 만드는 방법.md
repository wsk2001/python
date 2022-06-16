# Python으로 Windows 10 토스트 알림을 만드는 방법

출처: https://towardsdatascience.com/how-to-make-windows-10-toast-notifications-with-python-fb3c27ae45b9



### 파이썬!! 저게 뭐에요?

파이썬은 아름다운 프로그래밍 언어입니다. 아마도 당신이 필요로 할 모든 것이 있습니다. 웹 앱, 데스크톱 앱에서 네트워킹 앱 및 데이터 기반 응용 프로그램을 구축하는 데 도움이 될 수 있는 사용하기 쉬운 패키지 관리자가 있습니다.

년에 Python을 배워야 하는 이유를 찾고 있다면 이 스택 오버플로 블로그 게시물을 읽어보세요.

### **win10toast**

머신 러닝 엔지니어로서 저는 오픈 소스 커뮤니티의 뛰어난 사람들이 만든 패키지를 많이 사용합니다. 멋진 커뮤니티에 작은 패키지를 돌려드리게 되어 기쁩니다.

내 작업에서 나는 몇 시간이 걸리는 신경망을 실행하는 데 익숙하기 때문에 영화가 끝날 때까지 기다리면서 영화를 보곤 했습니다. 내 영화를 중단하고 진행 상황을 확인하는 대신 스크립트 실행이 완료되면 알림을 쉽게 받을 수 있는 방법을 원했습니다. 그래서 토스트 알림을 주기 위해 패키지를 만들었습니다 — win10toast 😃



### 시작하는 방법?

패키지는 Pypi로 게시되었으며 pip로 쉽게 설치할 수 있습니다.

``` python
pip install win10toast
```

설치가 완료되면 간단한 알림을 시도할 수 있습니다.

``` python
from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast("Sample Notification","Python is awesome!!!")
```

고급 사용 지침은 [설명서](https://github.com/jithurjacob/Windows-10-Toast-Notifications/blob/master/README.md)를 참조하십시오.

패키지가 마음에 들었거나 확장의 소스 코드에 관심이 있다면 내 [GitHub](https://github.com/jithurjacob/Windows-10-Toast-Notifications) 리포지토리로 이동하십시오.

