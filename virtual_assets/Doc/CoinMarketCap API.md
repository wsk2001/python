# CoinMarketCap API

출처: https://coinmarketcap.com/api/documentation/v1/

내 api key : 3971d7a6-7215-4450-89a4-e81bdbb253c9



# Introduction

CoinMarketCap API는 애플리케이션 개발자, 데이터 과학자 및 엔터프라이즈 비즈니스 플랫폼의 미션 크리티컬한 요구 사항을 충족하도록 특별히 설계된 고성능 RESTful JSON 엔드포인트 제품군입니다.

이 API 참조에는 개발자가 타사 응용 프로그램 및 플랫폼을 통합하는 데 필요한 모든 기술 문서가 포함되어 있습니다. 일반적인 질문에 대한 추가 답변은 [CoinMarketCap API FAQ](https://coinmarketcap.com/api/faq)에서 찾을 수 있습니다.



# Quick Start Guide

CoinMarketCap API로 실행을 시작하고자 하는 개발자를 위해 API로 첫 번째 호출을 하기 위한 몇 가지 빠른 단계가 있습니다.

- 무료 개발자 포털 계정에 가입하세요. [pro.coinmarketcap.com](https://pro.coinmarketcap.com/) 에서 가입할 수 있습니다. - 이것은 최신 시장 데이터가 있는 라이브 프로덕션 환경입니다. 요구 사항을 충족하는 경우 무료 기본 계획을 선택하거나 유료 계층으로 업그레이드하십시오.

- API 키를 복사합니다. 등록하면 개발자 포털 계정 대시보드가 나타납니다. 왼쪽 상단 패널의 API 키 상자에서 API를 복사합니다.
- 키를 사용하여 테스트 전화를 겁니다. 아래에 제공된 코드 예제를 사용하여 선택한 프로그래밍 언어로 테스트 호출을 할 수 있습니다. 이 예제는 시가 총액으로 모든 활성 암호화폐를 가져오고 USD로 시장 가치를 반환합니다.
- 샘플 코드의 API 키를 자신의 것으로 교체하고 API 도메인 pro-api.coinmarketcap.com을 사용하거나 sandbox-api.coinmarketcap.com 테스트를 위해 테스트 API 키 b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c를 사용하십시오. Sandbox.coinmarketcap.com 환경. **샌드박스 API에는 모의 데이터가 있으므로 애플리케이션에서 사용하면 안 됩니다.**
- 애플리케이션을 구현합니다. API 키가 작동하는 것을 확인했으므로 이 API 참조의 나머지 부분을 읽고 API에 익숙해지고 애플리케이션 빌드를 시작하십시오!

>참고: Javascript를 사용하여 클라이언트 측에서 HTTP 요청을 수행하는 것은 현재 CORS 구성을 통해 금지되어 있습니다. 이는 API 키가 도용되지 않도록 애플리케이션 사용자에게 표시되어서는 안 되는 API 키를 보호하기 위한 것입니다. 자체 백엔드 서비스를 통해 호출을 라우팅하여 API 키를 보호합니다.



> **View Quick Start Code Examples**



`cURL command line`

``` bash
curl -H "X-CMC_PRO_API_KEY: 8fd0b0e4-a44e-4311-8468-ecaf68a810db" -H "Accept: application/json" -d "start=1&limit=5000&convert=USD" -G https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest
```



`Node.js`

``` javascript

/* Example in Node.js ES6 using request-promise */

const rp = require('request-promise');
const requestOptions = {
  method: 'GET',
  uri: 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
  qs: {
    'start': '1',
    'limit': '5000',
    'convert': 'USD'
  },
  headers: {
    'X-CMC_PRO_API_KEY': '8fd0b0e4-a44e-4311-8468-ecaf68a810db'
  },
  json: true,
  gzip: true
};

rp(requestOptions).then(response => {
  console.log('API call response:', response);
}).catch((err) => {
  console.log('API call error:', err.message);
});
```



`python`

``` python
 
#This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '8fd0b0e4-a44e-4311-8468-ecaf68a810db',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
```



# Authentication

### API 키 획득

CoinMarketCap API에 대한 모든 HTTP 요청은 API 키로 유효성을 검사해야 합니다. 아직 API 키가 없는 경우 [API 개발자 포털](https://coinmarketcap.com/api/)을 방문하여 등록하십시오.

다음 두 가지 방법 중 하나로 REST API 호출에서 API 키를 제공할 수 있습니다.

- 선호하는 방법: X-CMC_PRO_API_KEY라는 사용자 정의 헤더를 통해
- 편리한 방법: CMC_PRO_API_KEY라는 쿼리 문자열 매개변수를 통해

보안 경고: 공개 액세스로부터 API 키를 보호하는 것이 중요합니다. 사용자 지정 헤더 옵션은 프로덕션 환경에서 API 키를 전달하기 위한 쿼리 문자열 옵션보다 강력하게 권장됩니다.

### API 키 사용 크레딧

대부분의 API 계획에는 할 수 있는 데이터 호출 수에 대한 일일 및 월간 제한 또는 '하드 캡'이 포함됩니다. 이 사용량은 다음 예외를 제외하고 귀하의 키로 이루어진 성공적인(HTTP 상태 200) 데이터 호출에 대해 1:1로 증가하는 API '호출 크레딧'으로 추적됩니다.

- 계정 관리 엔드포인트, 사용 통계 엔드포인트 및 오류 응답은 이 제한에 포함되지 않습니다.
- 페이지가 매겨진 끝점: 목록 기반 끝점은 100개 데이터 요소 기본값을 넘어 반환된(반올림) 모든 100개 데이터 요소에 대해 추가 호출 크레딧을 추적합니다. 경량 /map 엔드포인트는 이 제한에 포함되지 않으며 항상 1 크레딧으로 계산됩니다. 자세한 내용은 개별 엔드포인트 설명서를 참조하십시오.
- 번들 API 호출: 많은 엔드포인트가 리소스 및 통화 변환 번들을 지원합니다. 번들 리소스는 반환된 리소스 100개당 호출 크레딧 1개로 추적됩니다(반올림). 변환 매개변수를 사용하는 선택적 통화 변환 번들도 첫 번째 이후에 요청된 모든 변환에 대해 추가 API 호출 크레딧을 증가시킵니다.

개발자 포털에 로그인하여 각 호출에 사용된 크레딧 수를 포함하여 API 키 사용 및 제한에 대한 실시간 통계를 볼 수 있습니다. 각 API 호출에 대한 JSON 응답에서 호출 크레딧 사용량을 찾을 수도 있습니다. 자세한 내용은 상태 개체를 참조하십시오. 또한 /key/info 엔드포인트를 사용하여 사용량을 빠르게 검토하고 API에서 직접 일간/월간 크레딧을 재설정할 수 있습니다.

참고: '일' 및 '월' 크레딧 사용 기간은 API 구독을 기준으로 정의됩니다. 예를 들어 월간 구독이 5일 오전 5시 30분에 시작된 경우 이 청구 기준은 매월 크레딧이 새로 고쳐지는 시점이기도 합니다. 무료 기본 등급은 매일 UTC 자정에 재설정되고 매월 UTC 자정에 재설정됩니다.

### 엔드포인트 개요

CoinMarketCap API는 8개의 최상위 범주로 나뉩니다.

| Endpoint Category                                            | Description                                                  |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| [/cryptocurrency/*](https://coinmarketcap.com/api/documentation/v1/#tag/cryptocurrency) | 주문된 암호 화폐 목록 또는 가격 및 볼륨 데이터와 같은 암호 화폐에 대한 데이터를 반환하는 끝점. |
| [/exchange/*](https://coinmarketcap.com/api/documentation/v1/#tag/exchange) | 주문 교환 목록 및 시장 쌍 데이터와 같은 암호 화폐 교환 관련 데이터를 반환하는 엔드포인트. |
| [/global-metrics/*](https://coinmarketcap.com/api/documentation/v1/#tag/global-metrics) | 글로벌 시가 총액 및 BTC 지배력과 같은 집계 시장 데이터를 반환하는 엔드포인트. |
| [/tools/*](https://coinmarketcap.com/api/documentation/v1/#tag/tools) | 암호화폐 및 법정화폐 가격 변환과 같은 유용한 유틸리티.       |
| [/blockchain/*](https://coinmarketcap.com/api/documentation/v1/#tag/blockchain) | 블록체인에 대한 블록 탐색기 관련 데이터를 반환하는 엔드포인트. |
| [/fiat/*](https://coinmarketcap.com/api/documentation/v1/#tag/fiat) | CMC ID에 대한 매핑을 포함하여 법정 화폐에 대한 데이터를 반환하는 엔드포인트. |
| [/partners/*](https://coinmarketcap.com/api/documentation/v1/#tag/partners) | 타사 암호화 데이터에 편리하게 액세스할 수 있는 끝점입니다.   |
| [/key/*](https://coinmarketcap.com/api/documentation/v1/#tag/key) | 사용량을 검토하고 관리하기 위한 API 키 관리 엔드포인트.      |

끝점 경로는 제공된 데이터 유형과 일치하는 패턴을 따릅니다.

