# RSI 상대강도지수 구하기

출처: https://technfin.tistory.com/entry/RSI-%EC%83%81%EB%8C%80%EA%B0%95%EB%8F%84%EC%A7%80%EC%88%98-%EA%B5%AC%ED%95%98%EA%B8%B0-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%97%85%EB%B9%84%ED%8A%B8-%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8-%EC%9E%90%EB%8F%99%EB%A7%A4%EB%A7%A4

다른 여러 자료 있으니 참조 바람.



주식과는 마찬가지로 코인 시장에서도 차트를 이용한 매매 기법을 사용하실 수 있습니다. 그 중에서도 RSI(상대강도지수)는 상당히 많이 사용되는 보조지표중에 하나 입니다.

 

앞으로 업비트 API를 이용해 캔들 데이터를 조회하여 보조 지표를 구하는 방법들에 대해서 살펴볼 예정인데요. 이번 시간에는 RSI(Relative Strength Index)를 구하는 방법에 대해서 살펴 보고 실제로 업비트의 값과 비교해 보도록 하겠습니다.

 

대부분의 지표는 캔들 데이터를 기반으로 계산하기 때문에 먼저 캔들 데이터를 조회하는 방법을 알아야 하는데요. 이 부분은 아래에 링크해 드린 지난 포스트를 참고하시면 좋을 것 같습니다.

[2021.07.15 - [프로젝트/비트코인 자동매매\] - 캔들 조회 로직 - 파이썬 업비트 비트코인 자동매매](https://technfin.tistory.com/entry/캔들-조회-로직-파이썬-업비트-비트코인-자동매매)




목차 - 클릭하면 이동합니다.

- RSI 보조지표
  - [RSI 지표의 일반적인 해석](https://technfin.tistory.com/entry/RSI-상대강도지수-구하기-파이썬-업비트-비트코인-자동매매#RSI_지표의_일반적인_해석)
  - [RSI 지표를 활용한 매매법](https://technfin.tistory.com/entry/RSI-상대강도지수-구하기-파이썬-업비트-비트코인-자동매매#RSI_지표를_활용한_매매법)
- 전체코드
  - [공통코드](https://technfin.tistory.com/entry/RSI-상대강도지수-구하기-파이썬-업비트-비트코인-자동매매#공통코드)
  - [RSI 조회 프로그램](https://technfin.tistory.com/entry/RSI-상대강도지수-구하기-파이썬-업비트-비트코인-자동매매#RSI_조회_프로그램)
- 실행 결과

 

### RSI 보조지표

RSI 보조지표는 Relative Strength Index의 줄임말로 우리나라 말로는 상대강도지수라고 부릅니다. 가격의 상승 압력과 하락 압력간의 강도를 상대적으로 표현하는 지표로써 1978년 미국 윌레스 와일더(J. Welles Wilder Jr.)가 개발한 지표 입니다.

 

RSI는 0 부터 100까지의 값을 가지고 있으며 RSI가 클수록 상승 추세가 크다는 뜻이며 작을수록 하락추세가 크다는 의미를 가지고 있습니다.



RSI를 구하는 공식은 인터넷에서 쉽게 찾아 보실 수 있으니 별도로 다루지 않고 RSI를 일반적으로 어떻게 해석하고 매매에 활용하는지에 대해서 간단히 살펴 보겠습니다.

 

#### RSI 지표의 일반적인 해석

① RSI 값이 50 이상이면 매수세가 우세, 50 이하이면 매도세가 우세로 판단

② RSI 값이 70 이상이면 과매수 구간에 돌입

③ RSI 값이 30 이하이면 과매도 구간에 돌입

④ RSI 값이 시그널선을 상향 돌파시 단기 매수세가 늘어나는 추세로 판단

⑤ RSI 값이 시그널선을 하향 돌파시 단기 매도세가 늘어나는 추세로 판단

 

#### RSI 지표를 활용한 매매법

RSI 지표를 활용하여 단기적으로 아래와 같은 매매 방법을 적용할 수 있습니다.

 

① RSI가 30 미만으로 떨어져 과매도 구간에 돌입하고, RSI가 시그널선을 상향 돌파시 상승추세로 판단하여 매수

② RSI가 70을 초과하여 과매수 구간에 돌입하고, RSI가 시그널선을 하향 돌파시 하락추세로 판단하여 매도

 

### 전체코드

#### 공통코드

``` python
import logging
import requests
import time
import smtplib
import jwt
import sys
import uuid
import hashlib
import math
import numpy
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
from urllib.parse import urlencode
 
# Keys
access_key = '업비트에서 발급받은 Access Key'
secret_key = '업비트에서 발급받은 Secret Key'
server_url = 'https://api.upbit.com'
 
# -----------------------------------------------------------------------------
# - Name : set_loglevel
# - Desc : 로그레벨 설정
# - Input
#   1) level : 로그레벨
#     1. D(d) : DEBUG
#     2. E(e) : ERROR
#     3. 그외(기본) : INFO
# - Output
# -----------------------------------------------------------------------------
def set_loglevel(level):
    try:
 
        # ---------------------------------------------------------------------
        # 로그레벨 : DEBUG
        # ---------------------------------------------------------------------
        if level.upper() == "D":
            logging.basicConfig(
                format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]:%(message)s',
                datefmt='%Y/%m/%d %I:%M:%S %p',
                level=logging.DEBUG
            )
        # ---------------------------------------------------------------------
        # 로그레벨 : ERROR
        # ---------------------------------------------------------------------
        elif level.upper() == "E":
            logging.basicConfig(
                format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]:%(message)s',
                datefmt='%Y/%m/%d %I:%M:%S %p',
                level=logging.ERROR
            )
        # ---------------------------------------------------------------------
        # 로그레벨 : INFO
        # ---------------------------------------------------------------------
        else:
            # -----------------------------------------------------------------------------
            # 로깅 설정
            # 로그레벨(DEBUG, INFO, WARNING, ERROR, CRITICAL)
            # -----------------------------------------------------------------------------
            logging.basicConfig(
                format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]:%(message)s',
                datefmt='%Y/%m/%d %I:%M:%S %p',
                level=logging.INFO
            )
 
    # ----------------------------------------
    # Exception Raise
    # ----------------------------------------
    except Exception:
        raise
        
 
# -----------------------------------------------------------------------------
# - Name : send_request
# - Desc : 리퀘스트 처리
# - Input
#   1) reqType : 요청 타입
#   2) reqUrl : 요청 URL
#   3) reqParam : 요청 파라메타
#   4) reqHeader : 요청 헤더
# - Output
#   4) reponse : 응답 데이터
# -----------------------------------------------------------------------------
def send_request(reqType, reqUrl, reqParam, reqHeader):
    try:
 
        # 요청 가능회수 확보를 위해 기다리는 시간(초)
        err_sleep_time = 0.3
 
        # 요청에 대한 응답을 받을 때까지 반복 수행
        while True:
 
            # 요청 처리
            response = requests.request(reqType, reqUrl, params=reqParam, headers=reqHeader)
 
            # 요청 가능회수 추출
            if 'Remaining-Req' in response.headers:
 
                hearder_info = response.headers['Remaining-Req']
                start_idx = hearder_info.find("sec=")
                end_idx = len(hearder_info)
                remain_sec = hearder_info[int(start_idx):int(end_idx)].replace('sec=', '')
            else:
                logging.error("헤더 정보 이상")
                logging.error(response.headers)
                break
 
            # 요청 가능회수가 3개 미만이면 요청 가능회수 확보를 위해 일정시간 대기
            if int(remain_sec) < 3:
                logging.debug("요청 가능회수 한도 도달! 남은횟수:" + str(remain_sec))
                time.sleep(err_sleep_time)
 
            # 정상 응답
            if response.status_code == 200 or response.status_code == 201:
                break
            # 요청 가능회수 초과인 경우
            elif response.status_code == 429:
                logging.error("요청 가능회수 초과!:" + str(response.status_code))
                time.sleep(err_sleep_time)
            # 그 외 오류
            else:
                logging.error("기타 에러:" + str(response.status_code))
                logging.error(response.status_code)
                break
 
            # 요청 가능회수 초과 에러 발생시에는 다시 요청
            logging.info("[restRequest] 요청 재처리중...")
 
        return response
 
    # ----------------------------------------
    # Exception Raise
    # ----------------------------------------
    except Exception:
        raise
        
# -----------------------------------------------------------------------------
# - Name : get_candle
# - Desc : 캔들 조회
# - Input
#   1) target_item : 대상 종목
#   2) tick_kind : 캔들 종류 (1, 3, 5, 10, 15, 30, 60, 240 - 분, D-일, W-주, M-월)
#   3) inq_range : 조회 범위
# - Output
#   1) 캔들 정보 배열
# -----------------------------------------------------------------------------
def get_candle(target_item, tick_kind, inq_range):
    try:
 
        # ----------------------------------------
        # Tick 별 호출 URL 설정
        # ----------------------------------------
        # 분붕
        if tick_kind == "1" or tick_kind == "3" or tick_kind == "5" or tick_kind == "10" or tick_kind == "15" or tick_kind == "30" or tick_kind == "60" or tick_kind == "240":
            target_url = "minutes/" + tick_kind
        # 일봉
        elif tick_kind == "D":
            target_url = "days"
        # 주봉
        elif tick_kind == "W":
            target_url = "weeks"
        # 월봉
        elif tick_kind == "M":
            target_url = "months"
        # 잘못된 입력
        else:
            raise Exception("잘못된 틱 종류:" + str(tick_kind))
 
        logging.debug(target_url)
 
        # ----------------------------------------
        # Tick 조회
        # ----------------------------------------
        querystring = {"market": target_item, "count": inq_range}
        res = send_request("GET", server_url + "/v1/candles/" + target_url, querystring, "")
        candle_data = res.json()
 
        logging.debug(candle_data)
 
        return candle_data
 
    # ----------------------------------------
    # Exception Raise
    # ----------------------------------------
    except Exception:
        raise        
 
# -----------------------------------------------------------------------------
# - Name : get_rsi
# - Desc : RSI 조회
# - Input
#   1) target_item : 대상 종목
#   2) tick_kind : 캔들 종류 (1, 3, 5, 10, 15, 30, 60, 240 - 분, D-일, W-주, M-월)
#   3) inq_range : 조회 범위
# - Output
#   1) RSI 값
# -----------------------------------------------------------------------------
def get_rsi(target_item, tick_kind, inq_range):
    try:
 
        # 캔들 추출
        candle_data = get_candle(target_item, tick_kind, inq_range)
 
        df = pd.DataFrame(candle_data)
        df = df.reindex(index=df.index[::-1]).reset_index()
 
        df['close'] = df["trade_price"]
 
        # RSI 계산
        def rsi(ohlc: pd.DataFrame, period: int = 14):
            ohlc["close"] = ohlc["close"]
            delta = ohlc["close"].diff()
 
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
 
            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
 
            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")
 
        rsi = round(rsi(df, 14).iloc[-1], 4)
 
        return rsi
 
 
    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise
```

① 종목코드 : RSI 조회를 위한 종목 코드

② 캔들종류 : 1, 3, 5, 10, 15, 30, 60, 240 - 분, D-일, W-주, M-월

③ 조회범위 : 캔들 조회 범위(200으로 입력)

 

#### RSI 조회 프로그램

``` python
import os
import sys
import logging
import math
import traceback
 
# 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib import upbit as upbit  # noqa
 
# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
if __name__ == '__main__':
 
    # noinspection PyBroadException
    try:
 
        print("***** USAGE ******")
        print("[1] 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)")
 
        # 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)
        upbit.set_loglevel('I')
 
        # ---------------------------------------------------------------------
        # Logic Start!
        # ---------------------------------------------------------------------
        # 보유 종목 리스트 조회
        rsi_data = upbit.get_rsi('KRW-BTC', '30', '200')
        logging.info(rsi_data)
 
 
    except KeyboardInterrupt:
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(1)
 
    except Exception:
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(1)
```

① RSI 값 조회 예시(BTC, 30분봉 기준 RSI)

rsi_data = upbit.get_rsi('KRW-BTC', '30', '200')

  실행 결과



![img](https://blog.kakaocdn.net/dn/c3yeAp/btrazMFz4IF/v2IRoYn3ktCd5cFMnhFfJk/img.png)

![img](https://blog.kakaocdn.net/dn/T1dNx/btraFFSMqiD/IWiX9UsFkSNKDpqY0lP6k1/img.png)



실행 결과 업비트 30분봉 기준 BTC의 RSI값인 44.3309와 일치하는 결과가 조회됨을 확인할 수 있습니다.

 

앞으로 계속해서 다른 보조 지표들에 대해서 알아볼 예정이며 추후 보조 지표를 이용해서 매매를 하는 프로그램에 대해서 작성해 보도록 하겠습니다.

 

우측 상단 버튼을 눌러 블로그를 구독해 주시면 조금 더 빨리 소식을 받아보실 수 있습니다.

