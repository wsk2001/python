# Python 연관 분석

참고: [Practical Business Python](https://pbpython.com/)



### Python의 장바구니 분석 소개

#### 소개

python 분석가가 사용할 수 있는 데이터 분석 도구는 많이 있으며 특정 상황에서 어떤 도구를 사용해야 하는지 알기 어려울 수 있습니다. 유용한(그러나 다소 간과되는) 기술은 대규모 데이터 세트에서 항목의 공통 패턴을 찾으려고 시도하는 연관 분석이라고 합니다. 하나의 특정 응용 프로그램은 종종 장바구니 분석이라고 합니다. 시장 바구니 분석의 가장 일반적으로 인용되는 예는 소위 '맥주와 기저귀' 사례입니다. 기본적인 이야기는 한 대형 소매업체가 거래 데이터를 마이닝하여 맥주와 아기 기저귀를 동시에 구매하는 개인의 예상치 못한 구매 패턴을 찾을 수 있다는 것입니다.

불행히도 이 이야기는 데이터 도시의 전설일 가능성이 큽니다. 그러나 이는 거래 데이터를 마이닝하여 얻을 수 있는 통찰력 유형에 대한 설명적이고 재미있는 예입니다.

이러한 유형의 연결은 일반적으로 판매 거래를 조회하는 데 사용됩니다. 기본 분석은 클릭 스트림 추적, 예비 부품 주문 및 온라인 추천 엔진과 같은 다른 상황에 적용될 수 있습니다.

파이썬 데이터 과학 세계에 대한 기본적인 이해가 있다면 가장 먼저 scikit-learn에서 기성 알고리즘을 살펴보는 것이 좋습니다. 그러나 scikit-learn은 이 알고리즘을 지원하지 않습니다. 다행히 Sebastian Raschka의 매우 유용한 MLxtend 라이브러리에는 추가 분석을 위해 빈번한 항목 집합을 추출하는 Apriori 알고리즘 구현이 있습니다.

이 기사의 나머지 부분에서는 이 라이브러리를 사용하여 비교적 큰 온라인 소매 데이터 세트를 분석하고 흥미로운 구매 조합을 찾는 예를 살펴보겠습니다. 이 도움말을 마치면 자신의 데이터 세트에 적용하기 위한 기본 접근 방식에 충분히 익숙해질 것입니다.



#### 연관 분석이 필요한 이유

오늘날의 세계에는 데이터를 분석하는 복잡한 방법이 많이 있습니다(클러스터링, 회귀, 신경망, 랜덤 포레스트, SVM 등). 이러한 접근 방식 중 다수의 문제는 조정이 어렵고 해석이 어려우며 좋은 결과를 얻으려면 상당한 양의 데이터 준비 및 기능 엔지니어링이 필요하다는 것입니다. 즉, 매우 강력할 수 있지만 제대로 구현하려면 많은 지식이 필요합니다.

연관 분석은 수학 개념에 대해 상대적으로 가볍고 비기술적인 사람들에게 설명하기 쉽습니다. 또한 숨겨진 패턴을 찾는 비지도 학습 도구이므로 데이터 준비 및 기능 엔지니어링에 대한 필요성이 제한적입니다. 데이터 탐색의 특정 사례를 시작하는 것이 좋으며 다른 접근 방식을 사용하여 데이터를 더 깊이 파고들 수 있는 방법을 제시할 수 있습니다.

추가 보너스로 MLxtend의 python 구현은 scikit-learn 및 pandas에 노출된 모든 사람에게 매우 친숙해야 합니다. 이러한 모든 이유로 데이터 분석 문제에 익숙해지고 도움이 될 수 있는 유용한 도구라고 생각합니다.

한 가지 빠른 메모 - 기술적으로 장바구니 분석은 연관 분석의 한 응용 프로그램일 뿐입니다. 하지만 이 게시물에서는 연관 분석과 장바구니 분석을 같은 의미로 사용하겠습니다.



#### 연관 분석 101

연관 분석에서 이해해야 하는 몇 가지 용어가 사용됩니다. 데이터 마이닝 소개의 이 장은 이러한 정의 뒤에 숨은 수학 및 알고리즘 구현의 세부정보에 관심이 있는 사람들을 위한 훌륭한 참조 자료입니다.

연결 규칙은 일반적으로 다음과 같이 작성됩니다. {기저귀} - {맥주} 이는 동일한 거래에서 기저귀를 구매한 고객과 맥주도 구매한 고객 간에 강력한 관계가 있음을 의미합니다.

위의 예에서 {Diaper}는 전건이고 {Beer}는 후건입니다. 전건과 후건 모두 여러 항목을 가질 수 있습니다. 즉, {기저귀, 껌} - {맥주, 칩}이 유효한 규칙입니다.

지원은 규칙이 표시되는 상대적 빈도입니다. 많은 경우에 유용한 관계인지 확인하기 위해 높은 지원을 원할 수 있습니다. 그러나 '숨겨진' 관계를 찾으려는 경우 낮은 지원이 유용한 경우가 있을 수 있습니다.

신뢰도는 규칙의 신뢰도를 나타내는 척도입니다. 위의 예에서 신뢰도가 0.5라는 것은 기저귀와 껌을 구매한 경우의 50%에서 맥주와 칩도 함께 구매했음을 의미합니다. 제품 추천의 경우 50% 신뢰도는 완벽하게 수용할 수 있지만 의료 상황에서는 이 수준이 충분히 높지 않을 수 있습니다.

상승도는 두 규칙이 독립적인 경우 예상되는 지원에 대한 관찰된 지원의 비율입니다(위키피디아 참조). 기본 경험 법칙은 리프트 값이 1에 가까우면 규칙이 완전히 독립적임을 의미합니다. 상승도 값 1은 일반적으로 더 '흥미로우며' 유용한 규칙 패턴을 나타낼 수 있습니다.

데이터와 관련된 마지막 메모입니다. 이 분석은 트랜잭션에 대한 모든 데이터가 1행에 포함되어야 하고 항목이 1-hot 인코딩되어야 합니다. MLxtend 문서 예시가 유용합니다.

|      | Apple | Corn | Dill | Eggs | Ice cream | Kidney Beans | Milk | Nutmeg | Onion | Unicorn | Yogurt |
| :--- | :---- | :--- | :--- | :--- | :-------- | :----------- | :--- | :----- | :---- | :------ | :----- |
| 0    | 0     | 0    | 0    | 1    | 0         | 1            | 1    | 1      | 1     | 0       | 1      |
| 1    | 0     | 0    | 1    | 1    | 0         | 1            | 0    | 1      | 1     | 0       | 1      |
| 2    | 1     | 0    | 0    | 1    | 0         | 1            | 1    | 0      | 0     | 0       | 0      |
| 3    | 0     | 1    | 0    | 0    | 0         | 1            | 1    | 0      | 0     | 1       | 1      |
| 4    | 0     | 1    | 0    | 1    | 1         | 1            | 0    | 0      | 1     | 0       | 0      |

이 기사의 특정 데이터는 UCI Machine Learning Repository에서 가져왔으며 2010-2011년 영국 소매업체의 거래 데이터를 나타냅니다. 이는 대부분 도매업체에 대한 판매를 나타내므로 소비자 구매 패턴과 약간 다르지만 여전히 유용한 사례 연구입니다.



#### Let’s Code

MLxtend는 pip를 사용하여 설치할 수 있으므로 아래 코드를 실행하기 전에 설치해야 합니다. 설치가 완료되면 아래 코드는 설치 및 실행 방법을 보여줍니다. 노트북을 사용할 수 있도록 만들었으므로 아래의 예를 자유롭게 따르세요.

pandas 및 MLxtend 코드를 가져와서 데이터를 읽습니다.

``` py
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

df = pd.read_excel('http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx')
df.head()
```



| InvoiceNo | StockCode | Description | Quantity                            | InvoiceDate | UnitPrice           | CustomerID | Country |                |
| :-------- | :-------- | :---------- | :---------------------------------- | :---------- | :------------------ | :--------- | :------ | -------------- |
| 0         | 536365    | 85123A      | WHITE HANGING HEART T-LIGHT HOLDER  | 6           | 2010-12-01 08:26:00 | 2.55       | 17850.0 | United Kingdom |
| 1         | 536365    | 71053       | WHITE METAL LANTERN                 | 6           | 2010-12-01 08:26:00 | 3.39       | 17850.0 | United Kingdom |
| 2         | 536365    | 84406B      | CREAM CUPID HEARTS COAT HANGER      | 8           | 2010-12-01 08:26:00 | 2.75       | 17850.0 | United Kingdom |
| 3         | 536365    | 84029G      | KNITTED UNION FLAG HOT WATER BOTTLE | 6           | 2010-12-01 08:26:00 | 3.39       | 17850.0 | United Kingdom |
| 4         | 536365    | 84029E      | RED WOOLLY HOTTIE WHITE HEART.      | 6           | 2010-12-01 08:26:00 | 3.39       | 17850.0 | United Kingdom |

약간의 청소가 필요합니다. 첫째, 일부 설명에는 제거해야 하는 공백이 있습니다. 인보이스 번호가 없는 행도 삭제하고 신용 거래(인보이스 번호에 C가 포함된 거래)도 제거합니다.

``` py
df['Description'] = df['Description'].str.strip()
df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
df['InvoiceNo'] = df['InvoiceNo'].astype('str')
df = df[~df['InvoiceNo'].str.contains('C')]
```

정리 후 각 제품 1 핫 인코딩된 행당 1 트랜잭션으로 항목을 통합해야 합니다. 데이터 세트를 작게 유지하기 위해 프랑스 매출만 보고 있습니다. 그러나 아래 추가 코드에서 이러한 결과를 독일의 판매와 비교할 것입니다. 추가 국가 비교는 조사하는 것이 흥미로울 것입니다.

``` py
basket = (df[df['Country'] =="France"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))
```

처음 몇 개의 열은 다음과 같습니다(참고: 개념을 설명하기 위해 열에 몇 가지 숫자를 추가했습니다. 이 예의 실제 데이터는 모두 0입니다).

| Description | 10 COLOUR SPACEBOY PEN | 12 COLOURED PARTY BALLOONS | 12 EGG HOUSE PAINTED WOOD | 12 MESSAGE CARDS WITH ENVELOPES | 12 PENCIL SMALL TUBE WOODLAND | 12 PENCILS SMALL TUBE RED RETROSPOT | 12 PENCILS SMALL TUBE SKULL | 12 PENCILS TALL TUBE POSY |
| :---------- | :--------------------- | :------------------------- | :------------------------ | :------------------------------ | :---------------------------- | :---------------------------------- | :-------------------------- | :------------------------ |
| InvoiceNo   |                        |                            |                           |                                 |                               |                                     |                             |                           |
| 536370      | 11.0                   | 0.0                        | 0.0                       | 0.0                             | 0.0                           | 0.0                                 | 0.0                         | 1.0                       |
| 536852      | 0.0                    | 0.0                        | 0.0                       | 0.0                             | 5.0                           | 0.0                                 | 0.0                         | 0.0                       |
| 536974      | 0.0                    | 0.0                        | 0.0                       | 0.0                             | 0.0                           | 0.0                                 | 0.0                         | 0.0                       |
| 537065      | 0.0                    | 0.0                        | 0.0                       | 0.0                             | 0.0                           | 7.0                                 | 0.0                         | 0.0                       |
| 537463      | 0.0                    | 0.0                        | 9.0                       | 0.0                             | 0.0                           | 0.0                                 | 0.0                         | 0.0                       |

데이터에 0이 많이 있지만 양수 값이 1로 변환되고 0보다 작은 값이 0으로 설정되어 있는지 확인해야 합니다. 이 단계는 데이터의 원 핫 인코딩을 완료하고 우표 열을 제거합니다. (해당 청구는 저희가 조사하고자 하는 청구가 아니기 때문에):

``` py
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

basket_sets = basket.applymap(encode_units)
basket_sets.drop('POSTAGE', inplace=True, axis=1)
```

이제 데이터가 제대로 구성되었으므로 최소 7%의 지지도를 갖는 빈번한 항목 세트를 생성할 수 있습니다(이 수치는 유용한 예를 충분히 얻을 수 있도록 선택되었습니다).

``` python
frequent_itemsets = apriori(basket_sets, min_support=0.07, use_colnames=True)
```

마지막 단계는 해당 지원, 확신 및 상승도와 함께 규칙을 생성하는 것입니다.

``` py
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules.head()
```



| antecedants | consequents                        | support                            | confidence | lift     |          |
| :---------- | :--------------------------------- | :--------------------------------- | :--------- | :------- | -------- |
| 0           | (PLASTERS IN TIN WOODLAND ANIMALS) | (PLASTERS IN TIN CIRCUS PARADE)    | 0.170918   | 0.597015 | 3.545907 |
| 1           | (PLASTERS IN TIN CIRCUS PARADE)    | (PLASTERS IN TIN WOODLAND ANIMALS) | 0.168367   | 0.606061 | 3.545907 |
| 2           | (PLASTERS IN TIN CIRCUS PARADE)    | (PLASTERS IN TIN SPACEBOY)         | 0.168367   | 0.530303 | 3.849607 |
| 3           | (PLASTERS IN TIN SPACEBOY)         | (PLASTERS IN TIN CIRCUS PARADE)    | 0.137755   | 0.648148 | 3.849607 |
| 4           | (PLASTERS IN TIN WOODLAND ANIMALS) | (PLASTERS IN TIN SPACEBOY)         | 0.170918   | 0.611940 | 4.4422   |

그게 다야!  apriori를 사용하여 빈번한 항목을 작성한 다음 association_rules로 규칙을 작성하십시오.

이제 까다로운 부분은 이것이 우리에게 무엇을 말해주는지 알아내는 것입니다. 예를 들어, 거래 및 제품 조합의 수를 고려할 때 예상보다 더 자주 발생함을 의미하는 높은 리프트 값을 가진 규칙이 꽤 많이 있음을 알 수 있습니다. 우리는 또한 자신감이 높은 여러 곳을 볼 수 있습니다. 분석의 이 부분은 도메인 지식이 유용할 부분입니다. 제가 가지고 있지 않기 때문에 몇 가지 예시를 찾아보겠습니다.

표준 pandas 코드를 사용하여 데이터 프레임을 필터링할 수 있습니다. 이 경우 큰 상승도(6)와 높은 신뢰도(.8)를 찾습니다.

``` py
rules[ (rules['lift'] >= 6) &
       (rules['confidence'] >= 0.8) ]
```

| antecedants | consequents                                     | support                              | confidence | lift     |          |
| :---------- | :---------------------------------------------- | :----------------------------------- | :--------- | :------- | -------- |
| 8           | (SET/6 RED SPOTTY PAPER CUPS)                   | (SET/6 RED SPOTTY PAPER PLATES)      | 0.137755   | 0.888889 | 6.968889 |
| 9           | (SET/6 RED SPOTTY PAPER PLATES)                 | (SET/6 RED SPOTTY PAPER CUPS)        | 0.127551   | 0.960000 | 6.968889 |
| 10          | (ALARM CLOCK BAKELIKE GREEN)                    | (ALARM CLOCK BAKELIKE RED)           | 0.096939   | 0.815789 | 8.642959 |
| 11          | (ALARM CLOCK BAKELIKE RED)                      | (ALARM CLOCK BAKELIKE GREEN)         | 0.094388   | 0.837838 | 8.642959 |
| 16          | (SET/6 RED SPOTTY PAPER CUPS, SET/6 RED SPOTTY… | (SET/20 RED RETROSPOT PAPER NAPKINS) | 0.122449   | 0.812500 | 6.125000 |
| 17          | (SET/6 RED SPOTTY PAPER CUPS, SET/20 RED RETRO… | (SET/6 RED SPOTTY PAPER PLATES)      | 0.102041   | 0.975000 | 7.644000 |
| 18          | (SET/6 RED SPOTTY PAPER PLATES, SET/20 RED RET… | (SET/6 RED SPOTTY PAPER CUPS)        | 0.102041   | 0.975000 | 7.077778 |
| 22          | (SET/6 RED SPOTTY PAPER PLATES)                 | (SET/20 RED RETROSPOT PAPER NAPKINS) | 0.127551   | 0.800000 | 6.030769 |



규칙을 보면 초록색과 빨간색 알람시계는 함께 구매하고 빨간색 종이컵, 냅킨, 접시는 전체 확률이 제시하는 것보다 더 높은 방식으로 함께 구매하는 것으로 보입니다.

이 시점에서 한 제품의 인기를 사용하여 다른 제품의 판매를 유도할 수 있는 기회가 얼마나 많은지 살펴보고 싶을 수 있습니다. 예를 들어 녹색 알람 시계는 340개 판매하지만 빨간색 알람 시계는 316개만 판매하므로 추천을 통해 더 많은 빨간색 알람 시계 판매를 유도할 수 있습니다.

``` py
basket['ALARM CLOCK BAKELIKE GREEN'].sum()

340.0

basket['ALARM CLOCK BAKELIKE RED'].sum()

316.0
```

또한 흥미로운 점은 구매 국가에 따라 조합이 어떻게 다른지 확인하는 것입니다. 독일에서 어떤 인기 있는 조합이 있는지 확인해 보겠습니다.

``` py
basket2 = (df[df['Country'] =="Germany"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))

basket_sets2 = basket2.applymap(encode_units)
basket_sets2.drop('POSTAGE', inplace=True, axis=1)
frequent_itemsets2 = apriori(basket_sets2, min_support=0.05, use_colnames=True)
rules2 = association_rules(frequent_itemsets2, metric="lift", min_threshold=1)

rules2[ (rules2['lift'] >= 4) &
        (rules2['confidence'] >= 0.5)]
```

| antecedants | consequents                     | support                            | confidence | lift     |          |
| :---------- | :------------------------------ | :--------------------------------- | :--------- | :------- | -------- |
| 7           | (PLASTERS IN TIN SPACEBOY)      | (PLASTERS IN TIN WOODLAND ANIMALS) | 0.107221   | 0.571429 | 4.145125 |
| 9           | (PLASTERS IN TIN CIRCUS PARADE) | (PLASTERS IN TIN WOODLAND ANIMALS) | 0.115974   | 0.584906 | 4.242887 |
| 10          | (RED RETROSPOT CHARLOTTE BAG)   | (WOODLAND CHARLOTTE BAG)           | 0.070022   | 0.843750 | 6.648168 |

David Hasselhoff 외에도 독일인들은 Tin Spaceboy와 Woodland 동물의 Plasters를 좋아하는 것 같습니다.

사실 데이터에 정통한 분석가는 이러한 유형의 분석에 대해 12가지 다른 질문을 할 수 있습니다. 추가 국가 또는 고객 콤보에 대해 이 분석을 복제하지 않았지만 위에 표시된 기본 pandas 코드를 고려할 때 전체 프로세스는 비교적 간단합니다.



#### 결론

연관 분석의 정말 좋은 점은 실행하기 쉽고 비교적 해석하기 쉽다는 것입니다. MLxtend 및 이 연관 분석에 대한 액세스 권한이 없었다면 기본 Excel 분석을 사용하여 이러한 패턴을 찾기가 매우 어려울 것입니다. python 및 MLxtend를 사용하면 분석 프로세스가 비교적 간단하며 Python을 사용하고 있으므로 python 생태계의 모든 추가 시각화 기술 및 데이터 분석 도구에 액세스할 수 있습니다.

마지막으로 MLxtend 라이브러리의 나머지 부분을 확인하는 것이 좋습니다. sci-kit에서 작업을 수행하는 경우 MLxtend에 익숙해지고 데이터 과학 도구 키트의 기존 도구 중 일부를 보완할 수 있는 방법을 배우는 것이 도움이 됩니다.