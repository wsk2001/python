/*
select sum(S.open) as open, sum(E.close) as close, round((((close / open) -1) * 100),2) as YTD FROM
(
        (
                select symbol, date, open from day_candle
                where date = '2023-01-01'
        ) S,
        (
                select symbol, date, close from day_candle
                where date = '2023-01-01'
        ) E
)
WHERE S.symbol = E.symbol
*/

-- sub query
/*
SELECT A.symbol from (
	select symbol, count(*) as cnt from day_candle
	where date >= '2022-01-01'
	group by symbol
	HAVING cnt = 460
) A
*/

-- VACUUM;
select A.symbol, B.cnt FROM 
( 
       ( 
			select symbol from day_candle
			where 0 < earn and date = (SELECT date('now','localtime','-1 days') as Yesterday)
        ) A, 
        ( 
			select symbol, count(*) as cnt from day_candle
			where earn < 0 and (SELECT date('now','localtime','-4 days') as CheckDay) <= date
			group by symbol
			having 3 <= cnt
        ) B 
) 
WHERE A.symbol = B.symbol
ORDER BY B.cnt desc

/*
select date, strftime('%w', date) from day_candle
where 1 = 1
and symbol='BTC'
and date > '2022-01-01'
and earn > 4.0
*/

/*
select date, substr(date, 9, 2), strftime('%w', date) from day_candle
where 1 = 1
and symbol='BTC'
and earn > 4.0
*/

select * FROM
(
select symbol, count(*) from day_candle
where date = '2023-02-05' and 0 < earn
) D,
(
select A.symbol from
(
select symbol from day_candle
where date = '2023-02-04' and 0 < earn
) A,
(
select symbol, count(*) as cnt from day_candle
where '2023-02-01' <= date and date <= '2023-02-03' and 0 < earn
group by symbol
having 3 = cnt
) B
where A.symbol = B.symbol
) C
where D.symbol = C.symbol

-- select * from day_candle
-- where symbol = 'STX'

-- rate of change
/**
select symbol, round(avg((high-low)/close*100),2) as roc from day_candle
where symbol != 'NU' 
and date >= '2023-04-01'
group by symbol
order by roc desc
limit 40
/**/

/**
select symbol
from day_candle
where 0 < earn
and date = '2023-04-12'
/**/

-- 
select A.symbol, B.cnt FROM 
( 
       ( 
			select symbol from day_candle
			where 0 < earn and date = (SELECT date('now','localtime','-1 days') as Yesterday)
        ) A, 
        ( 
			select symbol, count(*) as cnt from day_candle
			where earn < 0 and (SELECT date('now','localtime','-4 days') as CheckDay) <= date
			group by symbol
			having 2 <= cnt
        ) B 
) 
WHERE A.symbol = B.symbol
ORDER BY B.cnt desc

/*
select symbol as '심볼', 
		case wd
	    WHEN '0' THEN '일'
	    WHEN '1' THEN '월'
	    WHEN '2' THEN '화'
	    WHEN '3' THEN '수'
	    WHEN '4' THEN '목'
	    WHEN '5' THEN '금'
	    WHEN '6' THEN '토'
	    ELSE '값없음'
	    END
		AS '요일'
		,
		round(sum(earn),2) as '등락률(합계)' from weekday_t
where dt > '2022-08-31'
group by symbol, wd
*/

SELECT  F.theme,  A.symbol, A.open as O, D.high as H, C.low as L, B.close as C, round((((B.close / A.open) -1) * 100),2) as E  FROM
(
	(
		select symbol, open from day_candle
		where date = '2022-01-01'
		group by symbol
	) A,
	(
		select symbol, close from day_candle
		where date = '2022-12-31'
		group by symbol
	) B,
	(
		select symbol, min(close) low from day_candle
		where date like '2022-%'
		group by symbol
	) C,
	(
		select symbol, max(close) high from day_candle
		where date like '2022-%'
		group by symbol
	) D,
	( 
		select symbol, theme from coin_theme
		where market = 'UPBIT_KRW'
	) F
)
WHERE A.symbol = B.symbol
AND A.symbol = C.symbol
AND A.symbol = D.symbol
AND A.symbol = F.symbol
order by F.theme, A.symbol

/**
select round(sum(S.open),2) as open, round(sum(E.close),2) as close, round((((close / open) -1) * 100),2) as YTD FROM 
( 
       ( 
                select symbol, date, open from day_candle 
                where date = '2023-01-01' --and symbol != 'BTC'
        ) S, 
        ( 
                select symbol, date, close from day_candle 
                where date = '2023-02-07' --and symbol != 'BTC'
        ) E 
) 
WHERE S.symbol = E.symbol
/**/

/**
select round(sum(S.open),2) as open, round(sum(E.close),2) as close, round((((close / open) -1) * 100),2) as YTD FROM 
( 
       ( 
                select symbol, date, open from day_candle 
                where date = '2023-01-01'
        ) S, 
        ( 
                select symbol, date, close from day_candle 
                where date = '2023-02-07'
        ) E 
) 
WHERE S.symbol = E.symbol
/**/

/** 고가 최고 종목 *
select B.date, B.symbol, B.hearn from
(
	(
		select date, max(hearn) as mx from day_candle 
		where date >= '2023-01-01'
		group by date
	) A,
	(
		select date, symbol, hearn from day_candle 
	) B
)
WHERE B.date = A.date
and   B.hearn = A.mx
order by B.date
/**/

/** 상승률(종가) 최고 종목 */
select B.date, B.symbol, B.earn from
(
	(
		select date, max(earn) as mx from day_candle 
		where date >= '2023-01-01'
		group by date
	) A,
	(
		select date, symbol, earn from day_candle 
	) B
)
WHERE B.date = A.date
and   B.earn = A.mx
order by B.date
/**/



