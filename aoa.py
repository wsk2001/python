#-*- coding:utf-8 -*-

# ������ ������ ���� ���� ��ũ��Ʈ.

import sys
import io
import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.bitsignal.me/indexw.php');

soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
str0 = soup.prettify()
idx = str0.find('<td class="one">')
str1 = str0[idx:idx+300]
strs = str1.splitlines()

str_out = ''
for s in strs:
	if s.strip().startswith('<'):
		continue
	else:
		str_out = str_out + ' ' + s.strip()

print(str_out.strip())

