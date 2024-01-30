import yfinance as yf
from prophet import Prophet
import matplotlib.pyplot as plt

class YahooFinanceClient:
    def __init__(self):
        return
    

    def fetch_data(self, ticker_symbol):
        try:
            # Get data on this ticker
            ticker_data = yf.Ticker(ticker_symbol)
            
            # Get historical prices for this ticker
            ticker_df = ticker_data.history(period='day', start='2023-01-01', end='2024-01-01')
            
            # If the DataFrame is empty, it means the ticker symbol was invalid or data is unavailable
            if ticker_df.empty:
                print("No data found for the given ticker symbol.")
                return
            
            # Display the data
            close_data = ticker_df[['Close']]
            close_data.reset_index(level=0, inplace=True)
            close_data = close_data.rename({'Date': 'ds', 'Close': 'y'}, axis='columns')
            close_data['ds'] = close_data['ds'].dt.tz_localize(None)
            return close_data
            
        except Exception as e:
            # Handle any other exceptions
            print(f"An error occurred: {e}")


class ProphetClient:
    
    def __init__(self):
        self.prophet = Prophet(daily_seasonality=True)
        return
        
        
    def fit_model(self, data):
        self.prophet.fit(data)
        future = self.prophet.make_future_dataframe(periods=365)
        forecast = self.prophet.predict(future)
        self.prophet.plot(forecast)
        #self.prophet.plot_components(forecast)
        
        print("Predicted Data")
        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        return forecast


def main():
    # Prompt the user to enter the ticker symbol
    ticker_symbol = input("Enter the ticker symbol: ")
    
    yfc = YahooFinanceClient()
    # Fetch and display the data
    data = yfc.fetch_data(ticker_symbol)
    print(data)
    
    pc = ProphetClient()
    
    forecast = pc.fit_model(data)
    
    # pc.prophet.plot(forecast)
    # plot = pc.prophet.plot_components(forecast)
    # plot.show()
    
    plt.show()
    
    
if __name__ == "__main__":
    main()
