#-*- coding:utf-8 -*-

# ���� Ʈ���̴� ������ ���� ���� ��ũ��Ʈ.
# BeautifulSoup ���δ� ���� �ʴ´�, selenium �� ����Ͽ� �м� �� �ʿ� ����.
# javascript �� ���� ��� �м� ����  selenium �� ����Ͽ��� �Ѵ�. �ƴϸ� Playwright for Python

import sys
import io
import requests
from bs4 import BeautifulSoup

r = requests.get('https://btctools.io/stats/leaderboard');

soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
str0 = soup.prettify()
print(str0)

#idx = str0.find('<td class="one">')
#str1 = str0[idx:idx+300]
#strs = str1.splitlines()

#str_out = ''
#for s in strs:
#	if s.strip().startswith('<'):
#		continue
#	else:
#		str_out = str_out + ' ' + s.strip()
#
#print(str_out.strip())

