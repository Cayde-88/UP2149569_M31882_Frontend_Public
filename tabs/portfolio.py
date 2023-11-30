import streamlit as st
import alpaca_trade_api as tradeapi
import time, requests, datetime
import pandas as pd
from PIL import Image
from tabs.home import set_bg
from alpaca_trade_api.rest import TimeFrame

def app():
    set_bg("tabs/images/background.jpg")
    # header and image
    st.title('My Portfolio')
    image = Image.open("tabs/images/portfolio.png")
    col1, col2, col3, col4 = st.columns(4)
    with col2:
        st.image(image, width=400)
        
    # description
    st.markdown("""
    > Input your Alpaca API and Secret Key to view your account information and portfolio.
    """)

    if 'api_key' not in st.session_state:
        st.session_state['api_key'] = ''

    if 'secret' not in st.session_state:
        st.session_state['secret'] = ''

    # input api and secret key
    placeholder = st.empty()
    if st.session_state['api_key'] == '' and st.session_state['secret'] == '':
        with placeholder.container():
            with st.form("Input API and Secret Key"):
                api_key = st.text_input('API Key', help='Login in to your Alpaca account to get your API & secret key (Paper Trading)')
                secret_key = st.text_input('Secret Key', type='password')

                st.session_state['api_key'] = api_key
                st.session_state['secret'] = secret_key

                submit_button = st.form_submit_button(label='Submit')

                if submit_button:
                    with st.spinner('Connecting to Alpaca...'):
                        time.sleep(1.5)    
                   
    # connect to alpaca
    try:
        api = tradeapi.REST(st.session_state['api_key'], st.session_state['secret'], base_url='https://paper-api.alpaca.markets', api_version='v2')

        account = api.get_account()
        if account.status == 'ACTIVE':
            
            st.success('Connected to Alpaca!')
            placeholder.empty()
            
            option = st.radio('Select an option', 
                              ['Account Info', 'Portfolio'])
            
            if option == 'Account Info':
                
                # build dataframe
                df = pd.DataFrame(account.__dict__)
                keys_of_interest = ['id', 'buying_power', 'cash', 'portfolio_value', 'status']
                df = df.loc[keys_of_interest]
                
                # rename columns
                df = df.rename(index={'id': 'Account ID', 'buying_power': 'Buying Power', 'cash': 'Cash', 'portfolio_value': 'Portfolio Value', 'status': 'Status'}, columns = {'_raw': 'Value'})
                st.dataframe(df, use_container_width=True)
                
            else:
                portfolio = api.get_portfolio_history(period='1A', timeframe='1D')
                portfolio_df = pd.DataFrame(portfolio.equity, index=portfolio.timestamp)
                
                # preprocess datetime column
                dates = [datetime.datetime.fromtimestamp(ts) for ts in portfolio_df.index.astype(int)]
                portfolio_df.index = dates
                
                # rename columns
                portfolio_df.rename(columns={0: 'Portfolio Value'}, inplace=True)
                
                # start portfolio index that has a portfolio value
                portfolio_df = portfolio_df[portfolio_df['Portfolio Value'].notna()]
                
                # Display portfolio value
                st.metric(label='Portfolio Value', value = f"${account.equity}", delta = f"{((float(account.equity) - float(account.last_equity)) / float(account.last_equity)):.2f} %")
                st.line_chart(portfolio_df, use_container_width=True)
                
                # List positions
                st.subheader('Positions')
                position_data = []
                start = (datetime.datetime.today() - datetime.timedelta(days=8)).strftime('%Y-%m-%d')
                end = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                with st.expander("Click to expand"):
                    for position in api.list_positions():
                        symbol = position.symbol
                        history = api.get_bars(symbol, TimeFrame.Day, start, end, adjustment='raw').df
                        position_data.append({
                            "Symbol": symbol,
                            "Quantity": position.qty,
                            "Value": position.market_value,
                            "Average Cost": position.avg_entry_price,
                            "Unrealized Profit/Loss": position.unrealized_pl,
                            "7 Days Average Volume": history['volume'].mean()  # Calculate average volume from historical data
                        })

                    position_df = pd.DataFrame(position_data)
                    st.dataframe(position_df, use_container_width=True)

                # Interactive chart
                st.subheader('Asset Performance')
                try:
                    ticker = st.selectbox('Select an asset', position_df['Symbol'].unique())
                    if ticker:
                        ticker_history = api.get_bars(ticker, TimeFrame.Day, start, end, adjustment='raw').df
                        ticker_close = ticker_history['close']
                        st.line_chart(ticker_close, use_container_width=True)

                except KeyError:
                    st.write("No assets to display.")

        elif account.status == 'INACTIVE':
            st.error('Inactive Alpaca account')

    except ValueError:
        del st.session_state['api_key']
        del st.session_state['secret']
        pass

    except requests.HTTPError:
        st.error('Invalid Alpaca API or Secret Key, did you regenerate your keys?')
        del st.session_state['api_key']
        del st.session_state['secret']

