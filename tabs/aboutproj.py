import streamlit as st
from PIL import Image
import requests
import bs4 as bs
from bs4 import BeautifulSoup
import datetime
import yfinance as yf
import plotly.express as px
from tabs.home import set_bg

def app():
    set_bg("tabs/images/background.jpg")
    # header and image
    st.title('About the Project')    
    image = Image.open("tabs/images/aboutproj.png")
    col1, col2, col3, col4 = st.columns(4)
    with col2:
        st.image(image, width=400)
    
    # description
    st.markdown("""
    This project uses an algorithmic approach to trading designed to simplify the process of investing in the stock market.
    Through the use of a trading bot, the user can automate the process of buying and selling stocks based on a set of rules.
    \n Here's how it works:
    1. The user registers for an account with Alpaca, a commission-free trading API.
    2. The user submits their API, secret keys and # days to trade which are stored in a secure database.
    3. Every working day at 9:30 EST, the bot will run and check for buy and sell signals.
    4. Trades are then placed based on the signals.
    5. The # of days remaining is then updated in the database.
    6. Accounts with 0 days remaining will be deleted from the database.""")

    flow_img = Image.open('./tabs/images/flowchart.png')
    st.image(flow_img, use_column_width=True)
    
    st.markdown("""\n :red[**Disclaimer**]:
    This project is for *educational purposes only*. Always do your own research before investing in the stock market.
    \n For this project, please be informed of the following:
    1. Only the S&P 500 stocks are available for trading. (View more below) or [here](https://www.slickcharts.com/sp500).
    2. Only paper trading is available.
    3. Testing methodology is below.
    """)
    
    # get stock data
    st.subheader('S&P 500 Ticker Listing')

    # get current list of S&P 500 companies
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    ticker_long_name_map = {}  
    for row in table.findAll('tr')[1:]:
        cells = row.findAll('td')
        ticker = cells[0].text.strip()
        long_name = cells[1].text.strip()
        ticker_long_name_map[ticker] = long_name 

    ticker_long_name_map = dict(sorted(ticker_long_name_map.items(), key=lambda item: item[0]))

    # select box for ticker symbol
    tickerSymbol = st.selectbox('Stock ticker', options=list(ticker_long_name_map.keys()))
    st.markdown("#")

    # get business summary
    # get logo
    string_name = ticker_long_name_map[tickerSymbol]
    url = f'https://en.wikipedia.org/wiki/{string_name.replace(" ", "_")}'  # Replace spaces with underscores
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    logo_element = soup.find('td', class_='infobox-image logo')

    if logo_element:
        string_logo = '<img src=%s style="filter: invert(1);">' % logo_element.find('img')['src']

        col_1, col_2, col_3 = st.columns(3)
        with col_2:
            st.markdown(string_logo, unsafe_allow_html=True)
            st.markdown("#")
    
    try:
        string_summary = yf.Ticker(tickerSymbol).info['longBusinessSummary']
        st.info(string_summary)
    
    except KeyError:
        st.info('No business summary available')
    
    except requests.exceptions.HTTPError:
        st.info('Server is temporarily unavailable. Please try again later.')

    # get historical prices for this ticker
    start_date = datetime.date.today() - datetime.timedelta(days=365*5)
    end_date = datetime.date.today()
    st.subheader('**Historic Performance**')

    button_1, button_2, button_3, button_4, button_5, button_6 = st.columns(6)

    with button_1:
        if st.button('5 Years'):
            start_date = end_date - datetime.timedelta(days=5*365)
    
    with button_2:
        if st.button('1 Year'):
            start_date = end_date - datetime.timedelta(days=365)
    
    with button_3:
        if st.button('6 Months'):
            start_date = end_date - datetime.timedelta(days=6*30)
    
    with button_4:
        if st.button('1 Month'):
            start_date = end_date - datetime.timedelta(days=30)
    
    with button_5:
        if st.button('1 Week'):
            start_date = end_date - datetime.timedelta(days=7)
    
    with button_6:
        if st.button('1 Day'):
            start_date = end_date - datetime.timedelta(days=1)

    
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

    # Plot raw data
    fig = px.line(tickerDf, x=tickerDf.index, y='Close', title=f'Closing Price of {string_name + " (" + tickerSymbol + ")"}')
    fig.update_layout({'plot_bgcolor': 'rgb(255, 255, 255)',}, hoverlabel=dict(bgcolor="blue", font_size=14))
    fig.update_xaxes(minor=dict(ticks="inside"), showgrid=True, gridwidth=1, gridcolor='LightPink')
    st.plotly_chart(fig)
    
    # Algorithm explanation
    st.header('**Algorithm**')
    st.markdown("""
    The algorithm was put through extensive testing to ensure that it is robust enough to handle different market conditions.
    Some of the algorithms tested include:
    \n :orange[**Classic technical analysis indicators:**]
    1. Crossover with Simple Moving Average (SMA), Exponential Moving Average (EMA), Relative Strength Index (RSI).
    2. Momentum with Rate-of-Change (ROC), Relative Strength Index (RSI) and Stochastic Oscillator.
    3. Mean Reversion with Relative Strength Index (RSI) and Bollinger Bands.
    
    """)
    
    # Testing methodology
    st.subheader('Testing Methodology')
    st.markdown("""
    As there are countless combinations of algorithms that can be used, a systematic approach was used to test the algorithms.
    \n **Step 1:** Number of Tickers: 20 chosen at random from the S&P 500.
    \n **Step 2:** Timeframe: 1 week, 1 month, 3 months, 6 months, 1 year, 5 years.
    \n **Step 3:** Algorithm: Test 3 variants for each strategy.
    """)
    
    # Results
    chart_1 = Image.open('./tabs/images/about_chart_1.png')
    st.image(chart_1, use_column_width=True)
    st.markdown("""*Example of returns chart (base 1 USD) for AAPL using crossover strategy w/ RSI*""")
    
    chart_2 = Image.open('./tabs/images/about_chart_2.png')
    st.image(chart_2, use_column_width=True)
    st.markdown("""*Example of buy and sell signals for AAPL using crossover strategy w/ RSI*""")

    # Chosen algorithm - Mean Reversion using Bollinger Bands
    st.subheader('Chosen Algorithm')
    st.markdown("""
    After countless weeks of testing, the algorithm that was chosen was the :green[**Mean Reversion using Bollinger Bands**].
    \n This algorithm was chosen because it had the highest returns across all timeframes.
    """)

    # Results of chosen algorithm
    chart_3 = Image.open('./tabs/images/about_chart_3.png')
    st.image(chart_3, use_column_width=True)
    st.markdown("""*Example of returns chart of AMD with Bollinger Bands*""")

    chart_4 = Image.open('./tabs/images/about_chart_4.png')
    st.image(chart_4, use_column_width=True)
    st.markdown("""*Example of returns for AMD with Bollinger Bands*""")

    chart_5 = Image.open('./tabs/images/about_chart_5.png')
    st.image(chart_5, use_column_width=True)
    st.markdown("""*Example of buy and sell signals for AMD with Bollinger Bands*""")