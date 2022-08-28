
-- symbol, 10% 이상 up count + total count
/***/
select a.symbol, count(*) cnt, 
       (select count(*) 
	    from DAY_CANDLE 
		where symbol = a.symbol
		) as days
from DAY_CANDLE a
where 10.0 <= a.hearn
group by a.symbol;
/***/