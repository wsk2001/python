Manager test ���:
	py XfcPolicyManager.py

TCP Server/Client test ���:
	py XfcApiServer.py  (API ��å�� �й��ϴ� Server Test ��, ��å�� XfcPolicyManager ���� DB �� ����)
	�ٸ� â ���� py XfcApiClientTest.py ((API ��å ��� �׽�Ʈ�� Client)
	    test �� IP �Է� -> 192.168.60.191 ���

	XfcApiServer.py �� ctrl + Pause �� ����

���� ��� ��ġ
  pip install flet
  pip install pandas
  ...
  ���۽� �ٸ� package �� ���ٰ� �ϸ� �� ó�� pip �� �̿��Ͽ� ��ġ.

[�������� �����]

pip install flet --upgrade
pip install pyinstaller --upgrade

flet pack XFilePolicyManager.py --icon xfc.ico
- ����
  dist\XFilePolicyManager

# flet pack �� �̿��� console app �� �ۼ� �ϸ� back-ground ���� ���� �ϴ� App �� ���� �ȴ�.
# ������ ���� ������ ũ�⸦ ���̱� ���� venv ���� �̿��� ���� ȯ���� ���� ��
# �� �ʿ��� Package �� ��ġ�Ͽ� ��� �ϴ� ����� ��� �Ͽ��� ��.

[flat �� ���� ȯ�� �����]

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

