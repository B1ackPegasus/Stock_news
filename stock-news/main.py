from twilio.rest import Client
import os
import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_IPKEY = os.environ.get("STOCK_IPKEY")
NEWS_IPKEY=os.environ.get("NEWS_IPKEY")

dict_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_IPKEY

}


response = requests.get(STOCK_ENDPOINT,params=dict_stock)

response.raise_for_status()

data = response.json()["Time Series (Daily)"]
data_list = [value for(key, value) in data.items()] # get value value is dict

yesterday_stock = data_list[0]
before_yesterday_stock = data_list[1]

yesterday_end_price = yesterday_stock["4. close"]
before_yesterday_end_price = before_yesterday_stock["4. close"]


difference= abs(float(yesterday_end_price)-float(before_yesterday_end_price))
diff_yesterday=(difference/float(yesterday_end_price))*100


if diff_yesterday< 20:
    news_dict = {
        "qInTitle": COMPANY_NAME,
        "sortBy": "popularity",
        "apiKey": NEWS_IPKEY
    }
    response_news = requests.get(NEWS_ENDPOINT, params=news_dict)
    response_news.raise_for_status()
    articles = response_news.json()["articles"]

    three_articles = articles[:3]




list_articles = [f"Heading:{article['title']}\nBrief: {article['description']}" for article in three_articles]

account_sid = 'ACaae7848001e489e52ad89b351d60b738'
auth_token = 'a60888ecba20cbc21eaa322114d8efe6'
client = Client (account_sid,auth_token)


for article in list_articles:
    message = client.messages.create(
        body=article,
        from_= os.environ.get('SysNumber_enVar'),
        to = os.environ.get('MyNumber_envVar')
    )





