from pandas import DataFrame 
from GoogleNews import GoogleNews
from datetime import date, datetime, timedelta


class SentimentAnalyzer:
    
    def __init__(self):
        self.google_news = GoogleNews()
        return
    
    
    def fetch_all_news(self, ticker_symbol, start_date, end_date):
        
        
        
        
        start_date_object = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_object = datetime.strptime(end_date, '%Y-%m-%d').date()
        self.google_news.set_time_range(start=start_date_object, end=end_date_object)
        
        
        
        
        # Fetch the news articles for the given ticker symbol
        self.google_news.search(ticker_symbol)
        self.google_news.get_page(1)
        news = self.google_news.results()
        
        # Convert the news articles into a DataFrame
        news_df = DataFrame(news)
        return news_df
    
    def fetch_news(self, ticker_symbol, start_date, num_days):
        # Fetch the news articles for the given ticker symbol
        # ...
        return
    
    def analyze_sentiment(self, news_df):
        # Analyze the sentiment of the news articles
        # ...
        return
    
    
    def display_sentiment(self, sentiment):
        # Display the sentiment
        # ...
        return
    
    
# Prompt the user to enter the ticker symbol
ticker_symbol = input("Enter the ticker symbol: ")

# # Prompt the user to enter the start date
# start_date = input("Enter the start date (YYYY-MM-DD): ")

# # Prompt the user to enter the number of days
# num_days = int(input("Enter the number of days: "))

sa = SentimentAnalyzer()
# news_df = sa.fetch_news(ticker_symbol, start_date, num_days)
# sentiment = sa.analyze_sentiment(news_df)
# sa.display_sentiment(sentiment)

print(sa.fetch_all_news(ticker_symbol, '2024-01-01', '2024-08-01'))
