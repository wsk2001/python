# -*- coding:utf-8 -*-

import tweepy
import argparse, sys
import traceback

consumer_key = 'sM0MHZJijTDnJDiTReA5Ad6NG'
consumer_secret = '8PXUzeT5rdvnowZGqUY9CoEWAZnuIU0tu9GsRZp3AuuBTamXRv'
access_token = '1444812495890255874-jOnPGby3iAJlNwujiS0rbvUkojXo7B'
access_token_secret = '2THLgX8asWY7A4uanPRMZSuWKTPsdKtCMMebudKiGhECy'
bearer_token = \
    'AAAAAAAAAAAAAAAAAAAAAPeXhwEAAAAAXBNfjk207D72rGas55dPJlvgM7E%3DAbc2bfFVROJanQzJKY8KYFqviTCVS9pdSM53AdtDqTw1j5tnEY'


def getClient():
    client = tweepy.Client(bearer_token=bearer_token)

    return client


def getUserTimeLine(userID):
    auth = tweepy.OAuthHandler(consumer_key='sM0MHZJijTDnJDiTReA5Ad6NG',
                               consumer_secret='8PXUzeT5rdvnowZGqUY9CoEWAZnuIU0tu9GsRZp3AuuBTamXRv')
    auth.set_access_token('1444812495890255874-jOnPGby3iAJlNwujiS0rbvUkojXo7B',
                          '2THLgX8asWY7A4uanPRMZSuWKTPsdKtCMMebudKiGhECy')
    api = tweepy.API(auth)

    user = api.verify_credentials()

    print("The user has " + str(user.followers_count) + " followers.")
    print("The user has " + str(user.friends_count) + " friends.")

    # fetching the statuses
    statuses = api.user_timeline(userID, count=3)

    # printing the statuses
    for status in statuses:
        print(status.text, end="\n\n")

    # tweets = api.user_timeline(screen_name=userID,
    #                            # 200 is the maximum allowed count
    #                            count=200,
    #                            include_rts=False,
    #                            # Necessary to keep full_text
    #                            # otherwise only the first 140 words are extracted
    #                            tweet_mode='extended'
    #                            )
    return statuses



def searchTweets(client, query, max_results):
    tweets = client.search_recent_tweets(query=query, max_results=max_results)
    tweet_data = tweets.data
    results = []
    if not tweet_data is None and len(tweet_data) > 0:
        for tweet in tweet_data:
            obj = {}
            obj['id'] = tweet.id
            obj['text'] = tweet.text
            results.append(obj)
    return results


def getTweet(client, id):
    tweet = client.get_tweet(id, expansions=['author_id'], user_fields=['username'])
    return tweet


def returnSearchTweetList(query, max_results):
    client = getClient()
    tweets = searchTweets(client, query, max_results)
    objs = []
    if len(tweets) > 0:
        for tweet in tweets:
            twt = getTweet(client, tweet['id'])
            obj = {}
            obj['text'] = tweet['text']
            obj['username'] = twt.includes['users'][0].username
            obj['id'] = tweet['id']
            obj['url'] = 'https://twitter.com/{}/status/{}'.format(twt.includes['users'][0].username, tweet['id'])
            objs.append(obj)
    return objs


def retweet(id):
    client = getClient()
    client.retweet(id)


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--user', required=False, help='user')

    args = parser.parse_args()
    user = args.user

    client = getClient()
    client.get_tweet(client.get_user('*'))

if __name__ == "__main__":
    main(sys.argv)

# account = "@1CFMkTJEkTuHbkU"
# statuses = twitter_api.GetUserTimeline(screen_name=account, count=200, include_rts=True, exclude_replies=False)
# #print(statuses)
#
# for status in statuses:
#     print(status.text)
#     print(status.text.encode('utf-8'))
# 여기서 가져온 텍스트는 유니코드이기 때문에, 혹시 텍스트가 깨질 경우 인코딩해서 보면 된다.

# 그리고 분석을 위해 이렇게 따로 텍스트 파일(json형식)으로 저장해볼 수 있겠다.
# output_file_name = "twitter_get_timeline_result.txt"

# with open(output_file_name, "w", encoding="utf-8") as output_file:
#    for status in statuses:
#        print(status, file=output_file)
