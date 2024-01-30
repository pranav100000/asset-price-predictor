from pandas import DataFrame 
from GoogleNews import GoogleNews
from datetime import date, datetime, timedelta
from web_crawler_to_openai_summary.crawler import web_crawler
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import namedtuple

class NewsScraperAndSentimentAnalyzer:
    
    INTERVAL_SIZE = 50
    NUM_PAGES = 5
    
    def __init__(self):
        self.google_news = GoogleNews()
        self.crawler = web_crawler.WebCrawler()
        return
    
    def fetch_all_news(self, ticker_symbol, start_n_days_ago, end_n_days_ago):
        
        DateAndSentimentScore = namedtuple('DateAndSentimentScore', ['date', 'sentiment_score'])
        dates_and_sentiment_scores = []
        for start_interval in range(start_n_days_ago, end_n_days_ago, -self.INTERVAL_SIZE):
            if start_interval - self.INTERVAL_SIZE < 0:
                break
            summaries = self.crawler.crawl_query(ticker_symbol, num_pages=self.NUM_PAGES, start_n_days_ago=start_interval, end_n_days_ago=start_interval-self.INTERVAL_SIZE)
            sentiment_score = self.analyze_sentiment([summary[1] for summary in summaries])
            date_and_score = DateAndSentimentScore(start_interval, sentiment_score)
            dates_and_sentiment_scores.append(date_and_score)
        
        return dates_and_sentiment_scores
        # start_date_object = datetime.strptime(start_date, '%Y-%m-%d').date()
        # end_date_object = datetime.strptime(end_date, '%Y-%m-%d').date()
        # self.google_news.set_time_range(start=start_date_object, end=end_date_object)

        # # Fetch the news articles for the given ticker symbol
        # self.google_news.search(ticker_symbol)
        # self.google_news.get_page(1)
        # news = self.google_news.results()
        # # Convert the news articles into a DataFrame
        # news_df = DataFrame(news)
        # return news_df
        
    def analyze_sentiment(self, summaries):
        # Initializing variables
        positive = 0
        negative = 0
        neutral = 0
        neutral_list = []
        negative_list = []
        positive_list = []

        # Iterating over the news summaries
        for summary in summaries:
            analyzer = SentimentIntensityAnalyzer().polarity_scores(summary)
            neg = analyzer['neg']
            #neu = analyzer['neu']
            pos = analyzer['pos']

            if neg > pos:
                negative_list.append(summary)
                negative += 1
            elif pos > neg:
                positive_list.append(summary)
                positive += 1
            elif pos == neg:
                neutral_list.append(summary)
                neutral += 1

        positive_percentage = (positive / len(summaries)) * 100
        negative_percentage = (negative / len(summaries)) * 100
        neutral_percentage = (neutral / len(summaries)) * 100

        print("Positive Sentiment:", '%.2f' % positive_percentage, end='\n')
        print("Neutral Sentiment:", '%.2f' % neutral_percentage, end='\n')
        print("Negative Sentiment:", '%.2f' % negative_percentage, end='\n')
        
        score = 100 - (negative_percentage + neutral_percentage*0.5)
        
        return score
    
if __name__ == "__main__":
    # Prompt the user to enter the ticker symbol
    ticker_symbol = input("Enter the ticker symbol: ")

    # # Prompt the user to enter the start date
    # start_date = input("Enter the start date (YYYY-MM-DD): ")

    # # Prompt the user to enter the number of days
    # num_days = int(input("Enter the number of days: "))

    sa = NewsScraperAndSentimentAnalyzer()
    # news_df = sa.fetch_news(ticker_symbol, start_date, num_days)
    # sentiment = sa.analyze_sentiment(news_df)
    # sa.display_sentiment(sentiment)
    print(sa.fetch_all_news(ticker_symbol, 365, 0))
