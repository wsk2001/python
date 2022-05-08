"""
hancomwith airdrop application
보안을 위해서 con_key 와 sec_key 는 유출 되지 않도록 작업 후 별도로 보관 하고 지워야 한다.
hancomwith.conf 파일에 key 값이 저장되어 있다.

-- 테스트용 가상 환경 활성화
venv\Scripts\activate 실행
-- 테스트용 가상 환경 비활성화
deactivate

-- 설치 (소스 만 복사 한 경우)
python -m venv venv   : 가상 환경 생성시 사용. 가상 환경 사용하지 않을 경우 생략
venv\Scripts\activate : 가상 환경 생성시 사용. 가상 환경 사용하지 않을 경우 생략

pip install -r requirements.txt

-- 설치 package 목록 작성 (추가 package 설치시)
pip freeze > requirements.txt

"""

import datetime
import getopt
import configparser
import openpyxl as xl
import sys
import time
import pybithumb

con_key = ''
sec_key = ''
airdrop_msg = ''
log_filename = ''


def w_log(log_msg, end_flag=''):
    global log_filename
    log = open(log_filename, 'a')
    cur = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + ': '
    print(cur, log_msg, file=log, flush=True, end=end_flag)
    log.close()


def usage(app_name):
    print('python ', app_name, '-f <excel filename> -s <sheet name>')
    print('ex: ', 'python ', app_name, '-f list.xlsx')
    print('    ', 'python ', app_name, '-f list.xlsx -s Sheet1')
    sys.exit(2)


def read_conf(conf_file):
    global con_key
    global sec_key
    global airdrop_msg
    global log_filename

    config = configparser.ConfigParser()
    config.read(conf_file)
    con_key = config['DEFAULT']['con_key'].strip()
    sec_key = config['DEFAULT']['sec_key'].strip()

    airdrop_msg = config['AIRDROP']['message'].strip()
    log_filename = config['AIRDROP']['logfile'].strip()


def airdrop_bithumb(fname, sheet_name):
    global con_key
    global sec_key
    global airdrop_msg

    workbook = xl.load_workbook(fname)
    sheet = workbook[sheet_name]

    try:
        bithumb = pybithumb.Bithumb(con_key, sec_key)
        if bithumb is None:
            print("connection error")
            sys.exit(0)

        # print('아로와나 보유량', bithumb.get_balance('ARW'))

        withdraw_currency = 'ARW'

        for row_data in sheet.iter_rows(min_row=3):  # min_row는 시작 행을 지정
            col = 0
            cust_no = 0
            cust_name = ''
            cust_tel = ''
            target_address = ''
            withdraw_unit = 0.0

            for cell in row_data:
                if col == 0:
                    cust_no = cell.value
                elif col == 1:
                    cust_name = cell.value
                elif col == 2:
                    cust_tel = cell.value
                elif col == 3:
                    target_address = cell.value
                elif col == 4:
                    withdraw_unit = cell.value

                col = col + 1

            res = bithumb.withdraw_coin(withdraw_unit, target_address, airdrop_msg, withdraw_currency)
            if res is None:
                w_log('[ERROR] Exception, no={}, name={}, tel={}, address={}, unit={}'
                      .format(cust_no, cust_name, cust_tel, target_address, withdraw_unit)
                      , '\n')
                print('[ERROR] Exception, no={}, name={}, tel={}, address={}, unit={}'
                      .format(cust_no, cust_name, cust_tel, target_address, withdraw_unit)
                      )
            else:
                if res['status'] == '0000':
                    w_log('[Success] no={}, name={}, tel={}, address={}, unit={}'
                          .format(cust_no, cust_name, cust_tel, target_address, withdraw_unit)
                          , '\n')
                    print('[Success] no={}, name={}, tel={}, address={}, unit={}'
                          .format(cust_no, cust_name, cust_tel, target_address, withdraw_unit)
                          )
                else:
                    w_log('[ERROR]  no={}, name={}, tel={}, address={}, unit={}, err_code={}, err_msg={}'
                          .format(cust_no, cust_name, cust_tel, target_address, withdraw_unit, res['status'],
                                  res['message'])
                          , '\n')
                    print('[ERROR]  no={}, name={}, tel={}, address={}, unit={}, err_code={}, err_msg={}'
                          .format(cust_no, cust_name, cust_tel, target_address, withdraw_unit, res['status'],
                                  res['message'])
                          )
            # Private API 호출시 1초에 15번 까지만 요청 할 수 있습니다.
            # 사용하고 있는 API 는 Private API 중 Trade API 이므로 초당 호출 회수(15) 를 넘길 경우
            # 10 분간 사용이 금지 됩니다. 따라서 sleep time 을 수정 하지 말기 바랍니다.
            time.sleep(0.1)

    except getopt.GetoptError as e:
        print(e)
        sys.exit(0)

    print('airdrop complete')


def main(argv):
    filename = ''
    sheet_name = ''
    try:
        opts, etc_args = getopt.getopt(argv[1:], "hf:s:", ["help", "filename=", "sheet="])

    except getopt.GetoptError:
        usage(argv[0])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(argv[0])
        elif opt in ("-f", "--filename"):  # airdrop list 가 저장되어 있는 파일 (list.xlsx)
            filename = arg
        elif opt in ("-s", "--sheet"):  # airdrop list 가 저장되어 있는 sheet 명 (Sheet1)
            sheet_name = arg

    if len(sheet_name) and len(filename):
        airdrop_bithumb(filename, sheet_name)
    else:
        usage(argv[0])


if __name__ == "__main__":
    # read_conf('hancomwith.conf')
    # main(sys.argv)

    v = 'ARW'
    res = pybithumb.Bithumb.get_ohlc(v)
    print(type(res))
    o = res.get(v)[0]
    h = res.get(v)[1]
    l = res.get(v)[2]
    c = res.get(v)[3]
    e = (c - o) / o * 100.0
    print('{}: open={}, high={}, low={}, current={}, earning={:0.3f}%'
          .format(v, o, h, l, c, e))
