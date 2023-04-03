from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from bs4 import BeautifulSoup
import requests
import pyupbit
import requests
from ast import literal_eval
import requests
import json

THEME_NFT = {
    "THETA": "쎄타토큰",
    "FLOW": "플로우",
    "MANA": "디센트럴랜드",
    "ENJ": "엔진코인",
    "AQT": "알파쿼크",
    "AXS": "엑시인피니티",
    "SAND": "샌드박스",
    "GMT": "스테픈",
    "WAXP": "왁스",
    "BORA": "보라",
    "XTZ": "테조스",
    "QKC": "쿼크체인",
    "PLA": "플레이댑",
    "CHZ": "칠리즈",
    "MOC": "모스코인",
    "WEMIX": "위믹스"
}

THEME_P2E = {
    "DAWN": "던프로토콜",
    "ENJ": "엔진코인",
    "AXS": "엑시인피니티",
    "SAND": "샌드박스",
    "WAXP": "왁스",
    "BORA": "보라",
    "PLA": "플레이댑",
    "WEMIX": "위믹스",
    "HUNT": "헌트",
    "MANA": "디센트럴랜드"
}

THEME_LAYER2 = {
    "NEAR": "니어프로토콜",
    "OMG": "오미세고",
    "SXP": "솔라",
    "MATIC": "폴리곤",
    "AVAX": "아발란체"
}

THEME_WEB3 = {
    "THETA": "쎄타토큰",
    "FLOW": "플로우",
    "NEAR": "니어프로토콜",
    "ALGO": "알고랜드",
    "BAT": "베이직어텐션토큰",
    "ONT": "온톨로지",
    "ATOM": "코스모스",
    "DOT": "폴카닷",
    "CVC": "시빅",
    "STORJ": "스토리지",
    "NU": "누사이퍼",
    "STX": "스택스",
    "STEEM": "스팀",
    "AVAX": "아발란체",
    "SC": "시아코인",
    "ANKR": "앵커",
    "HBAR": "헤데라",
    "SNT": "스테이터스네트워크토큰",
    "ICX": "아이콘",
    "KAVA": "카바",
    "MATIC": "폴리곤",
    "GLM": "골렘",
    "BTT": "비트토렌트",
    "XTZ": "테조스",
    "HIVE": "하이브",
    "IQ": "에브리피디아",
}

THEME_CHINA = {
    "NEO": "네오",
    "ONT": "온톨로지",
    "EOS": "이오스",
    "VET": "비체인",
    "XEC": "이캐시",
    "ONG": "온톨로지가스",
    "SC": "시아코인",
    "QTUM": "퀀텀",
    "BSV": "비트코인에스브이",
    "TT": "썬더토큰",
    "ELF": "엘프",
    "GAS": "가스",
    "BCH": "비트코인캐시",
    "BTT": "비트토렌트",
    "QKC": "쿼크체인",
    "JST": "저스트",
    "TRX": "트론"
}

# DID 코인이란 Decentralized Identitifier의 약자로 한국어로 하자면 신원인증 코인
THEME_DID = {
    "ONT": "온톨로지",
    "CVC": "시빅",
    "ICX": "아이콘",
    "FCT2": "피르마체인",
    "META": "메타디움",
    "HUM": "휴먼스케이프",
    "MED": "메디블록"
}

THEME_PAYMENT = {
    "POWR": "파워렛저",
    "XLM": "스텔라루멘",
    "HBAR": "헤데라",
    "STMX": "스톰엑스",
    "CRO": "크로노스",
    "STRK": "스트라이크",
    "XRP": "리플",
    "PUNDIX": "펀디엑스",
    "MLK": "밀크"
}

THEME_FAN = {
    "CHZ": "칠리즈"
}

THEME_PLATFORM = {
    "NEAR": "니어프로토콜",
    "ETH": "이더리움",
    "ALGO": "알고랜드",
    "EOS": "이오스",
    "DOT": "폴카닷",
    "ATOM": "코스모스",
    "SOL": "솔라나",
    "ADA": "에이다",
    "AVAX": "아발란체",
    "LSK": "리스크",
    "TRX": "트론",
    "NEO": "네오",
    "ARK": "아크",
    "XTZ": "테조스",
    "ICX": "아이콘",
    "ELF": "엘프",
    "MATIC": "폴리곤",
}

THEME_BITCOIN = {
    "XEC": "이캐시",
    "BTG": "비트코인골드",
    "STX": "스택스",
    "BTC": "비트코인",
    "BSV": "비트코인에스브이",
    "BCH": "비트코인캐시"
}

THEME_STORAGE = {
    "STORJ": "스토리지",
    "BTT": "비트토렌트",
    "SC": "시아코인",
    "FIL": "파일코인",
    "GLM": "골렘"
}

THEME_DEX = {
    "KNC": "카이버네트워크",
    "ZRX": "제로엑스",
}

THEME_MIM = {
    "DOGE": "도지코인",
}

THEME_DEFI = {
    "AVAX": "아발란체",
    "XTZ": "테조스",
    "BAT": "베이직어텐션토큰",
    "ANKR": "앵커",
    "SRM": "세럼",
    "JST": "저스트",
    "ETH": "이더리움",
    "ATOM": "코스모스",
    "VET": "비체인",
    "OMG": "오미세고",
    "AAVE": "에이브",
    "KAVA": "카바",
    "ANC": "앵커 프로토콜",
}

THEME_DAO = {
    "AAVE": "에이브",
}

THEME_BNB = {
    "EPX": "일립시스",
    "CHESS": "트랜체스",
    "XVS": "비너스",
    "BSW": "비스왑",
    "FOR": "포튜브",
    "ALPACA": "알파카 파이낸스",
    "CAKE": "팬케이크스왑",
    "MDX": "엠덱스",
    "BNB": "바이낸스코인",
    "CREAM": "크림파이낸스"
}

THEME_KLAY = {
    "DKA": "디카르고",
    "BORA": "보라",
    "SSX": "썸씽",
    "HUM": "휴먼스케이프",
    "PLA": "플레이댑",
    "WEMIX": "위믹스"
}

THEME_TERA = {
    "LUNA": "테라",
    "MIR": "미러 프로토콜",
    "ANC": "앵커 프로토콜",
    "USTC": "테라USD 클래식",
    "LUNC": "테라 클래식"
}

THEME_SOL = {
    "SOL": "솔라나",
    "SRM": "세럼",
}

THEME_MATIC = {
    "AAVE": "에이브",
    "CRV": "커브",
    "MATIC": "폴리곤",
}

THEME_DOT = {
    "DOT": "폴카닷",
    "ANKR": "앵커",
}

THEME_FTM = {
    "YFI": "와이언파이낸스",
    "FTM": "팬텀",
    "CRV": "커브",
    "SPELL": "스펠토큰",
    "BIFI": "비피 파이낸스"
}

THEME_AVAX = {
    "AAVE": "에이브",
    "AVAX": "아발란체",
}

#####
THEME_METABUS = {
    "MOC": "모스코인",
    "MANA": "디센트럴랜드",
    "PLA": "플레이댑",
    "SAND": "샌드박스",
    "AXS": "엑시인피니티",
    "BORA": "보라",
    "ENJ": "엔진코인",
}

THEME_IPFS = {
    "STORJ": "스토리지",
    "SC": "시아코인",
    "CRE": "캐리프로토콜",
}

#########################################
THEME_KAKAO = {
    "DKA": "디카르고",
    "BORA": "보라",
    "HUM": "휴먼스케이프",
}

THEME_MAJOR = {
    "BTC": "비트코인",
    "ETH": "이더리움",
    "ADA": "에이다",
    "XRP": "리플",
    "SOL": "솔라나",
    "DOT": "폴카닷",
    "DOGE": "도지코인",
}

THEME_SECURITY = {
    "UPP": "센티넬프로토콜",
}

THEME_MEDICAL = {
    "MED": "메디블록",
}

THEME_BINANCE = {
    "1INCH": "1인치네트워크",
    "AAVE": "에이브",
    "ANKR": "앵커",
    "LINK": "체인링크",
}

THEME_KIMCHI = {
    "HUM": "휴먼스케이프",
    "DKA": "디카르고",
    "PXL": "픽셀",
    "UPP": "센티넬프로토콜",
    "BORA": "보라",
    "AHT": "아하토큰",
    "MOC": "모스코인",
    "MBL": "무비블록",
    "MED": "메디블록",
    "META": "메타디움",
    "MLK": "밀크",
    "PLA": "플레이댑",
    "MVL": "엠블",
    "STPT": "에스티피",
    "SSX": "썸씽",
    "UPP": "센티넬프로토콜",
    "CRE": "캐리프로토콜",
    "FCT2": "피르마체인",
    "CBK": "코박토큰",
    "OBSR": "옵저버",
    "TON": "톤",
    "AERGO": "아르고",
    "SAND": "샌드박스",
    "AQT": "알파쿼크",
    "ICX": "아이콘",
}
#########################################

themes = {"nft": THEME_NFT,
          "p2e": THEME_P2E,
          "layer2": THEME_LAYER2,
          "web3": THEME_WEB3,
          "kimchi": THEME_KIMCHI,
          "china": THEME_CHINA,
          "did": THEME_DID,
          "payment": THEME_PAYMENT,
          "fan": THEME_FAN,
          "platform": THEME_PLATFORM,
          "bitcoin": THEME_BITCOIN,
          "storage": THEME_STORAGE,
          "dex": THEME_DEX,
          "mim": THEME_MIM,
          "defi": THEME_DEFI,
          "dao": THEME_DAO,
          "bnb": THEME_BNB,
          "klay": THEME_KLAY,
          "tera": THEME_TERA,
          "sol": THEME_SOL,
          "matic": THEME_MATIC,
          "meta": THEME_METABUS,
          "dot": THEME_DOT,
          "ftm": THEME_FTM,
          "avax": THEME_AVAX,
          "kakao": THEME_KAKAO,
          "major": THEME_MAJOR,
          "security": THEME_SECURITY,
          "medical": THEME_MEDICAL,
          "binance": THEME_BINANCE,
          }


def get_themes(ticker):
    list_theme = []
    list_theme.clear()

    for key in themes:
        if ticker.upper() in themes[key]:
            list_theme.append(key)

    if len(list_theme) == 0:
        list_theme.append('unclassified')

    return ticker.upper(), list_theme


def get_all_themes():
    list_theme = []
    list_theme.clear()

    for key in themes:
        list_theme.append(key)

    return list_theme


def get_theme_symbols(theme):
    return themes[theme.lower()]


def get_theme_symbols_count(theme):
    return len(themes[theme.lower()])

# 마켓코드조회
def market_code_all():
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails": "false"}
    response = requests.request("GET", url, params=querystring)

    # 코인이름 - 마켓코드 매핑
    r_str = response.text
    r_str = r_str.lstrip('[')  # 첫 문자 제거
    r_str = r_str.rstrip(']')  # 마지막 문자 제거
    r_list = r_str.split("}")  # str를 }기준으로 쪼개어 리스트로 변환

    # korean name to symbol
    kts = {}

    # symbol to korean name
    stk = {}

    kts.clear()
    stk.clear()

    for i in range(len(r_list) - 1):
        r_list[i] += "}"
        if i != 0:
            r_list[i] = r_list[i].lstrip(',')
        r_dict = literal_eval(r_list[i])  # element to dict

        if r_dict["market"][0] == 'U':
            temp_dict = {r_dict["market"][5:]: r_dict["korean_name"]}
        else:
            temp_dict = {r_dict["market"][4:]: r_dict["korean_name"]}
        stk.update(temp_dict)  # 코드 - 코인이름 매핑

        if r_dict["market"][0] == 'U':
            temp_dict = {r_dict["korean_name"]: r_dict["market"][5:]}
        else:
            temp_dict = {r_dict["korean_name"]: r_dict["market"][4:]}

        kts.update(temp_dict)  # 코인이름 - 코드 - 매핑

    return stk, kts


def kor_to_symbol(kts, v):
    if v.upper() in kts:
        return v, kts[v.upper()]
    else:
        return None, None


if __name__ == "__main__":
    # stk, kts = market_code_all()
    #
    # f = open("theme.txt", "r", encoding='utf-8')
    # lines = f.readlines()
    #
    # for l in lines:
    #     line = l.strip()
    #
    #     if line.startswith("["):
    #         print()
    #         print(line)
    #         continue
    #
    #     if len(line) <= 0:
    #         continue
    #
    #     ko_name, symbol = kor_to_symbol(kts, line)
    #     if ko_name is not None:
    #         print('"' + symbol + '":', '"' + ko_name + '",')
    #
    # print()

    symbol, lst = get_themes('btt')
    if len(lst):
        print(symbol, lst)

    theme = 'did'
    print()
    print('theme:', theme)
    # t = get_theme_symbols(theme)
