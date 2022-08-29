# python 트위터 크롤링

출처: [[python\] 트위터 크롤링 (tistory.com)](https://intotw.tistory.com/249)



트위터 크롤링을 위해서는 일반 웹사이트 처럼 크롤링을 해도 되지만,

트위터 API를 이용하면 좀 더 편하게 크롤링이 가능합니다.

 

우선적으로, 트위터 개발자 사이트에서 api를 발급 받으시고, 파이썬 tweepy 라이브러리를 이용해서 쉽게 트위터 크롤링이 가능합니다.

 

### 트위터 데이터 사용하기

트위터 API를 사용하려면 **애플리케이션**을 등록해야 합니다. 기본적으로 애플리케이션은 트위터상의 공개 정보에만 액세스할 수 있습니다. 쪽지를 주고받는 역할을 하는 등의 특정한 엔드 포인트는 추가로 권한을 부여받아야 정보에 액세스할 수 있습니다. 

 

### 트위터 개발자 사이트에서 API 등록 생성하기

개발자는 먼저 트위터 개발자로 등록하여 제작할 어플리케이션에 인증도구로 사용할 consumer_key 등을 받아야 함.

[developer.twitter.com/en/portal/petition/use-case](https://developer.twitter.com/en/portal/petition/use-case)



![[python] 트위터 크롤링 - undefined - 트위터 개발자 사이트에서 API 등록 생성하기](.\images\twitter_Developer_portal_img.png)





이메일과 휴대폰 정보가 입력되어 있어야 합니다.

1). **개발목적 입력 (Which best describes you?)**
=> Hobbyist > Exploring the API > Get stated

2). **기본정보 입력**
What would you like us to call you?
=> 닉네임을 입력합니다.

What country do you live in?
=>거주중인 국가 선택

What’s your current coding skill level?
=> 코딩실력을 입력합니다.

3). **트위터 데이터 또는 API 사용 계획 제출**
=> 사용계획을 쓰라는 란이 있는데, 아래 예시입니다. 구글 번역기를 사용하여 적당히 입력하시면 됩니다.

I am studying python. I want to use the Twitter API to search for Twitter and check the results. To do this, we will learn how to use the API. We will use the data we collect for personal use.

4). **The specifics**
=> 적당히 Yes, No 선택후 Next (모두 No로 하셔도 됩니다.)
5). **작성내용 검토**
6). **약관동의**
7). **이메일 확인**
=> confirm your email 버튼 클릭합니다.
8). 기다림....(약간의 시간이 필요한것 같습니다.)
9). 이메일 승인https://developer.twitter.com



###  tweepy 라이브러리 설치

tweepy 사용하여 크위터 크롤링을 하기위해서 라이브러리를 설치한다.

 

```
> pip install tweepy
```

 

### 크롤링 코딩하기

특정 검색어를 사용하여 트위터에서 검색한후, 검색 결과를 csv 파일로 저장하는 코드이다.

```python
import tweepy
import pandas as pd

# 트위터 Application에서 발급 받은 key 정보들 문자열로 입력
consumer_key = "~~~~"
consumer_secret = "~~~~"
access_token = "~~~~"
access_token_secret = "~~~~"

# 1. 트위터 키 입력
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# 2. 액세스 요청
auth.set_access_token(access_token, access_token_secret)

# 3. twitter API 생성
api = tweepy.API(auth)

#--------------------------
# twitter_search
#--------------------------
def twitter_search(outfilename, keyword):
	result = []  # 크롤링 텍스트를 저장 할 리스트 변수
	
	for i in range(1, 4):  # 1~3 페이지 크롤링
		tweets = api.search_tweets(keyword)  # keyword 검색 실시.
		result = []
		for tweet in tweets:
			result.append([tweet.created_at, tweet.id_str, tweet.text, tweet.favorite_count, tweet.retweet_count])
		result = sorted(result, key=lambda x : -x[-2]) # 정렬: 좋아요 수 기준
	df = pd.DataFrame(result, columns = ['time', 'id', 'text', 'likey', 'retweet'])
	
    # 결과 확인
    print(len(result))  # 트윗 개수 출력
	print(df)  # 결과 확인
	
    # df to csv
    df.to_csv(outfilename, encoding='utf-8-sig')
   

#--------------------------
# Main
#--------------------------
if __name__ == "__main__":
    outfilename='tweet_search.csv'
    keyword = '소녀시대'  # 키워드 입력
    twitter_search(outfilename, keyword)
```



### 실행결과

연번, 시간, id, text, likey, retweet 순서로 결과과 출력되고, tweet_search.csv 파일에 결과물이 저장된다.



![[python] 트위터 크롤링 - undefined - 실행결과](D:\GitHub\python\Crawling\images\twitter_crawling_sample_image_01.png)