# Python 거래 전략에서 일일 피벗 계산

### 피벗 포인트란 무엇입니까?

피벗 포인트는 데이 트레이딩 에서 자주 사용되는 가격 수준입니다(하지만 스윙 거래에서도 사용할 수 있음). 그들은 일일 시장 세션 동안 가격에 대한 '자연적인' 지지 및 저항으로 간주되므로 시장이 그들에게 가까워질 때 종종 사소하지 않은 방식으로 행동하기 때문에 데이 트레이더에게 매우 유용할 수 있습니다.

여러 유형의 피벗 포인트가 있지만 클래식 피벗 포인트는 일반적으로 마지막 날의 고가, 저가 및 종가에서 시작하여 정의됩니다. 거래자는 이전 시장일의 이러한 가격에 일부 수학적 계산을 적용하여 현재 시장일의 피벗 수준을 계산하고 사용할 수 있습니다. 이 기사에서는 고전적인 피벗 포인트에 중점을 둘 것입니다.

데이 트레이더는 예를 들어 가격이 피벗 수준에 가까운 곳에서 거래 기회를 찾을 수 있습니다. 예를 들어 풀백이나 브레이크아웃을 기다리고 가장 가까운 피벗 수준을 목표로 사용합니다.

### 계산 방법

클래식 피벗 레벨은 마지막 날의 고가, 저가 및 종가에 적용된 [Tradingview 지식 기반](https://www.tradingview.com/support/solutions/43000521824-pivot-points-standard/)에서 가져온 다음 공식에 따라 계산됩니다.

- PP = (High + Low + Close) / 3

- R1 = 2 * PP — Low

- S1 = 2 * PP — High

- R2 = PP + (High — Low)

- S2 = PP — (High — Low)

- R3 = PP + 2 * (High — Low)

- S3 = PP — 2 * (High — Low)

  

PP는 주요 피벗 수준입니다. S1, S2 및 S3은 지지 수준입니다. R1, R2 및 R3은 저항 수준입니다.

다음은 각각의 지지/저항선 계산 공식 입니다.



###### Traditional

```js
    PP = (HIGHprev + LOWprev + CLOSEprev) / 3
    R1 = PP * 2 - LOWprev
    S1 = PP * 2 - HIGHprev
    R2 = PP + (HIGHprev - LOWprev)
    S2 = PP - (HIGHprev - LOWprev)
    R3 = PP * 2 + (HIGHprev - 2 * LOWprev)
    S3 = PP * 2 - (2 * HIGHprev - LOWprev)
    R4 = PP * 3 + (HIGHprev - 3 * LOWprev)
    S4 = PP * 3 - (3 * HIGHprev - LOWprev)
    R5 = PP * 4 + (HIGHprev - 4 * LOWprev)
    S5 = PP * 4 - (4 * HIGHprev - LOWprev)
```



###### Fibonacci

```js
    PP = (HIGHprev + LOWprev + CLOSEprev) / 3
    R1 = PP + 0.382 * (HIGHprev - LOWprev)
    S1 = PP - 0.382 * (HIGHprev - LOWprev)
    R2 = PP + 0.618 * (HIGHprev - LOWprev)
    S2 = PP - 0.618 * (HIGHprev - LOWprev)
    R3 = PP + (HIGHprev - LOWprev)
    S3 = PP - (HIGHprev - LOWprev)
```



###### Woodie

```js
    PP = (HIGHprev + LOWprev + 2 * CLOSEprev) / 4
    R1 = 2 * PP - LOWprev
    S1 = 2 * PP - HIGHprev
    R2 = PP + (HIGHprev - LOWprev)
    S2 = PP - (HIGHprev - LOWprev)
    R3 =  HIGHprev + 2 * (PP -  LOWprev)
    S3 =  LOWprev - 2 * (HIGHprev - PP)
    R4 = R3 + (HIGHprev - LOWprev)
    S4 = S3 - (HIGHprev - LOWprev)
```



###### Classic

```js
    PP = (HIGHprev + LOWprev + CLOSEprev) / 3
    R1 = 2 * PP - LOWprev
    S1 = 2 * PP - HIGHprev
    R2 = PP + (HIGHprev - LOWprev)
    S2 = PP - (HIGHprev - LOWprev)
    R3 = PP + 2 * (HIGHprev - LOWprev)
    S3 = PP - 2 * (HIGHprev - LOWprev)
    R4 = PP + 3 * (HIGHprev - LOWprev)
    S4 = PP - 3 * (HIGHprev - LOWprev)
```



###### Demark

```js
    IF  OPENprev == CLOSEprev
    X = HIGHprev + LOWprev + 2 * CLOSEprev
    ELSE 
    IF CLOSEprev >  OPENprev
        X = 2 * HIGHprev + LOWprev + CLOSEprev
    ELSE
        X = 2 * LOWprev + HIGHprev + CLOSEprev
    PP = X / 4
    R1 = X / 2 - LOWprev
    S1 = X / 2 - HIGHprev
```



###### Camarilla

```js
    PP = (HIGHprev + LOWprev + CLOSEprev) / 3
    R1 = CLOSEprev + 1.1 * (HIGHprev - LOWprev) / 12
    S1 = CLOSEprev - 1.1 * (HIGHprev - LOWprev) / 12
    R2 = CLOSEprev + 1.1 * (HIGHprev - LOWprev) / 6
    S2 = CLOSEprev - 1.1 * (HIGHprev - LOWprev) / 6
    R3 = CLOSEprev + 1.1 * (HIGHprev - LOWprev) / 4
    S3 = CLOSEprev - 1.1 * (HIGHprev - LOWprev) / 4
    R4 = CLOSEprev + 1.1 * (HIGHprev - LOWprev) / 2
    S4 = CLOSEprev - 1.1 * (HIGHprev - LOWprev) / 2
    R5 = (HIGHprev / LOWprev) * CLOSEprev
    S5 = CLOSEprev - (R5 - CLOSEprev)
```

