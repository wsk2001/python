Manager test 방법:
	py XFilePolicyManager.py

TCP Server/Client test 방법:
	py XfcApiServer.py  (API 정책을 분배하는 Server Test 용, 정책은 XfcPolicyManager 에서 DB 에 저장)
	다른 창 에서 py XfcApiClientTest.py ((API 정책 취득 테스트용 Client)
	    test 용 IP 입력 -> 192.168.60.191 등등

	XfcApiServer.py 는 ctrl + Pause 로 종료

종속 모듈 설치
  pip install flet
  pip install pandas
  ...
  실핼시 다른 package 가 없다고 하면 위 처럼 pip 를 이용하여 설치.

[실행파일 만들기]

pip install flet --upgrade
pip install pyinstaller --upgrade

flet pack XFilePolicyManager.py --icon xfc.ico
- 실행
  dist\XFilePolicyManager

# flet pack 을 이용해 console app 을 작성 하면 back-ground 에서 동작 하는 App 이 생성 된다.
# 생성된 실행 파일의 크기를 줄이기 위해 venv 등을 이용해 가상 환경을 만든 후
# 꼭 필요한 Package 만 설치하여 사용 하는 방법을 사용 하여야 함.

[flat 용 가상 환경 만들기]

1. make venv
	python -m venv flet_env

	start_flet_env.bat
		flet_env\Scripts\activate.bat
		
	stop_flet_env.bat
		flet_env\Scripts\deactivate.bat

2. install package
	2.1 start_flet_env.bat
	2.2 pip install flet
	2.3 pip install flet --upgrade
	2.4 pip install pandas
	2.5 pip install pyinstaller
	2.6 pip install pillow

