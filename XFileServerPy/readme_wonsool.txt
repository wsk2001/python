Manager test 방법:
	py XfcPolicyManager.py

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
