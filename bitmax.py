#-*- coding:utf-8 -*-

# 유명 트레이더 포지션 가져 오는 스크립트.
# BeautifulSoup 으로는 되지 않는다, selenium 을 사용하여 분석 할 필요 있음.
# javascript 에 의한 출력 분석 에는  selenium 을 사용하여야 한다. 아니면 Playwright for Python

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

