
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # 프로젝트 이름에 맞게 수정
django.setup()

from portfolio.models import SecuritiesMarket

data = [
  {
    "code": "005930",
    "name": "삼성전자",
    "price": 54300
  },
  {
    "code": "000660",
    "name": "SK하이닉스",
    "price": 186000
  },
  {
    "code": "207940",
    "name": "삼성바이오로직스",
    "price": 1085000
  },
  {
    "code": "373220",
    "name": "LG에너지솔루션",
    "price": 320500
  },
  {
    "code": "005380",
    "name": "현대차",
    "price": 189400
  },
  {
    "code": "012450",
    "name": "한화에어로스페이스",
    "price": 818000
  },
  {
    "code": "005935",
    "name": "삼성전자우",
    "price": 45300
  },
  {
    "code": "105560",
    "name": "KB금융",
    "price": 93200
  },
  {
    "code": "329180",
    "name": "HD현대중공업",
    "price": 408500
  },
  {
    "code": "068270",
    "name": "셀트리온",
    "price": 162400
  },
  {
    "code": "000270",
    "name": "기아",
    "price": 89400
  },
  {
    "code": "035420",
    "name": "NAVER",
    "price": 197400
  },
  {
    "code": "055550",
    "name": "신한지주",
    "price": 51200
  },
  {
    "code": "042660",
    "name": "한화오션",
    "price": 78900
  },
  {
    "code": "012330",
    "name": "현대모비스",
    "price": 256500
  },
  {
    "code": "138040",
    "name": "메리츠금융지주",
    "price": 122600
  },
  {
    "code": "028260",
    "name": "삼성물산",
    "price": 122200
  },
  {
    "code": "005490",
    "name": "POSCO홀딩스",
    "price": 255500
  },
  {
    "code": "009540",
    "name": "HD한국조선해양",
    "price": 277500
  },
  {
    "code": "196170",
    "name": "알테오젠",
    "price": 356500
  },
  {
    "code": "259960",
    "name": "크래프톤",
    "price": 385000
  },
  {
    "code": "086790",
    "name": "하나금융지주",
    "price": 64100
  },
  {
    "code": "000810",
    "name": "삼성화재",
    "price": 377000
  },
  {
    "code": "034020",
    "name": "두산에너빌리티",
    "price": 27700
  },
  {
    "code": "032830",
    "name": "삼성생명",
    "price": 85300
  },
  {
    "code": "035720",
    "name": "카카오",
    "price": 38050
  },
  {
    "code": "015760",
    "name": "한국전력",
    "price": 25600
  },
  {
    "code": "010130",
    "name": "고려아연",
    "price": 783000
  },
  {
    "code": "011200",
    "name": "HMM",
    "price": 18250
  },
  {
    "code": "051910",
    "name": "LG화학",
    "price": 210000
  },
  {
    "code": "033780",
    "name": "KT&G",
    "price": 116000
  },
  {
    "code": "096770",
    "name": "SK이노베이션",
    "price": 93400
  },
  {
    "code": "030200",
    "name": "KT",
    "price": 53500
  },
  {
    "code": "316140",
    "name": "우리금융지주",
    "price": 17720
  },
  {
    "code": "010140",
    "name": "삼성중공업",
    "price": 14610
  },
  {
    "code": "064350",
    "name": "현대로템",
    "price": 111500
  },
  {
    "code": "024110",
    "name": "기업은행",
    "price": 15220
  },
  {
    "code": "402340",
    "name": "SK스퀘어",
    "price": 91300
  },
  {
    "code": "006400",
    "name": "삼성SDI",
    "price": 173600
  },
  {
    "code": "267260",
    "name": "HD현대일렉트릭",
    "price": 323000
  },
  {
    "code": "066570",
    "name": "LG전자",
    "price": 70600
  },
  {
    "code": "017670",
    "name": "SK텔레콤",
    "price": 53700
  },
  {
    "code": "352820",
    "name": "하이브",
    "price": 264500
  },
  {
    "code": "323410",
    "name": "카카오뱅크",
    "price": 22100
  },
  {
    "code": "003550",
    "name": "LG",
    "price": 66700
  },
  {
    "code": "247540",
    "name": "에코프로비엠",
    "price": 104500
  },
  {
    "code": "018260",
    "name": "삼성에스디에스",
    "price": 128800
  },
  {
    "code": "003670",
    "name": "포스코퓨처엠",
    "price": 124900
  },
  {
    "code": "034730",
    "name": "SK",
    "price": 131700
  },
  {
    "code": "000100",
    "name": "유한양행",
    "price": 113500
  },
  {
    "code": "009150",
    "name": "삼성전기",
    "price": 117600
  },
  {
    "code": "047050",
    "name": "포스코인터내셔널",
    "price": 48800
  },
  {
    "code": "326030",
    "name": "SK바이오팜",
    "price": 107400
  },
  {
    "code": "047810",
    "name": "한국항공우주",
    "price": 85300
  },
  {
    "code": "459580",
    "name": "KODEX CD금리액티브(합성)",
    "price": 1069075
  },
  {
    "code": "086280",
    "name": "현대글로비스",
    "price": 107500
  },
  {
    "code": "272210",
    "name": "한화시스템",
    "price": 41700
  },
  {
    "code": "360750",
    "name": "TIGER 미국S&P500",
    "price": 19665
  },
  {
    "code": "003490",
    "name": "대한항공",
    "price": 21000
  },
  {
    "code": "028300",
    "name": "HLB",
    "price": 57400
  },
  {
    "code": "003230",
    "name": "삼양식품",
    "price": 988000
  },
  {
    "code": "042700",
    "name": "한미반도체",
    "price": 76300
  },
  {
    "code": "090430",
    "name": "아모레퍼시픽",
    "price": 125600
  },
  {
    "code": "079550",
    "name": "LIG넥스원",
    "price": 330000
  },
  {
    "code": "010620",
    "name": "HD현대미포",
    "price": 172100
  },
  {
    "code": "443060",
    "name": "HD현대마린솔루션",
    "price": 153000
  },
  {
    "code": "006800",
    "name": "미래에셋증권",
    "price": 11970
  },
  {
    "code": "086520",
    "name": "에코프로",
    "price": 50200
  },
  {
    "code": "005830",
    "name": "DB손해보험",
    "price": 92900
  },
  {
    "code": "010120",
    "name": "LS ELECTRIC",
    "price": 210500
  },
  {
    "code": "021240",
    "name": "코웨이",
    "price": 86100
  },
  {
    "code": "267250",
    "name": "HD현대",
    "price": 77900
  },
  {
    "code": "069500",
    "name": "KODEX 200",
    "price": 33965
  },
  {
    "code": "488770",
    "name": "KODEX 머니마켓액티브",
    "price": 102720
  },
  {
    "code": "010950",
    "name": "S-Oil",
    "price": 52100
  },
  {
    "code": "088980",
    "name": "맥쿼리인프라",
    "price": 11590
  },
  {
    "code": "000150",
    "name": "두산",
    "price": 333500
  },
  {
    "code": "005387",
    "name": "현대차2우B",
    "price": 152100
  },
  {
    "code": "180640",
    "name": "한진칼",
    "price": 80800
  },
  {
    "code": "032640",
    "name": "LG유플러스",
    "price": 12190
  }
]

for item in data:
    SecuritiesMarket.objects.update_or_create(
        code=item['code'],
        defaults={
            'name': item['name'],
            'price': item['price']
        }
    )