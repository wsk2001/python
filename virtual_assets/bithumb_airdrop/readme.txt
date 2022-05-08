[ airdrop app 실행 방법 ]

1. [win] + x key 를 누르고 명령 프롬프트(c) 를 선택 한다.
2. cd  명령을 이용해 airdrop.py 파일이 있는 경로로 이동 한다.
3. venv\Scripts\activate, venv\Scripts\activate.bat 파일을 수정 한다.
   VIRTUAL_ENV 다음에 있는 경로명을 실제 복사된 경로로 수정 한다.
4. venv\Scripts\activate 명령을 실행 한다.
5. hancomwith.conf 파일의 con_key 와 sec_key 의 값을 수정 한다
6. list.xlsx 파일을 열어서 airdrop list를 수정 한다.
   Sheet1 의 column 중 전자지갑 주소, 코인 수량 은 정확히 입력 하여야 한다.
   나머지 column 의 값은 log 를 남기기 위한 값 이므로 임의로 작성 하여도 된다.
   * Sheet1 에 작성 하여야 한다. 아니면 실행시 옵션 으로 바뀐 Sheet 명을 입력 하여야 한다.
   * Sheet 의 Form 을 변경 하지 않는다. 변경시 source code 를 수정 하여야 한다.
7. 실행
   python airdrop.py -f list.xlsx -s Sheet1
   * Sheet 명을 바꾼 경우 실행 옵션의 -s 이후에 지정 하여야 한다.
   * Sheet 명을 바꾼 경우 실행 옵션의 -f 이후에 지정 하여야 한다.
8. 결과 log
   실행 결과는 airdrop.log 에 기록 되며 Success 가 아닌 data 는 오류 코드와 Message 를
   참고하여 조치를 취한 후 다시 작업을 수행 하여야 한다.
   * log 파일은 log 내용을 파일의 뒤에 추가 하는 방법으로 생성 한다. 따라서 재 작업시 필요한 경우
     airdrop.log 를 백업 후 작업 하는 방법을 사용 할 수 있다.

- 끝 -

Rate Limits
사용자 급증 등 과도한 트래픽이 발생할 경우 안정적인 서비스 제공을 위해 API 요청량을 별도의 공지 없이 제한 또는 하향 조정할 수 있습니다.

Public API
1초당 최대 135회 요청 가능합니다.
초과 요청을 보내면 API 사용이 제한됩니다.

Private API
1초당 최대 15회 요청 가능합니다.
초과 요청을 보내면 API 사용이 일시적으로 제한됩니다. (Public - 1분 / Private info - 5분 / Private trade - 10분)

※ 제한 상태 해제는 고객센터>1:1 상담 혹은 전화상담을 통해 관리자 승인이 필요합니다.

※ airdrop 은 Private trade API 이므로 초당 15회 이내로 요청 하여야 합니다. 초과 하면 10분간 사용 제한 됩니다.

출처: https://apidocs.bithumb.com/docs/rate_limits
