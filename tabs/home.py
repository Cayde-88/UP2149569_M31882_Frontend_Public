import streamlit as st
import alpaca_trade_api as tradeapi
from tabs.secret.secret import host, database, user, password
import sqlalchemy as db
from sqlalchemy.exc import SQLAlchemyError
import time, requests
from PIL import Image
import base64

engine = db.create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

# background image
def set_bg(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "jpg"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover;
             background-repeat: no-repeat;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def app():
    set_bg("tabs/images/background.jpg")
    st.title('Home / Perform Trades')
    image = Image.open("tabs/images/home.png")
    col1, col2, col3, col4 = st.columns(4)
    with col2:
        st.image(image, width=400)
    st.markdown("""
    Welcome to my Alpaca Trading Bot! This is a project I have been working on to learn more about algorithmic trading.
    """)

    if 'api_key_order' not in st.session_state:
        st.session_state['api_key_order'] = ''
    
    if 'secret_order' not in st.session_state:
        st.session_state['secret_order'] = ''
    
    if 'email_order' not in st.session_state:
        st.session_state['email_order'] = ''

    # form for user to submit their API and Secret Key
    placeholder = st.empty()
    if st.session_state['api_key_order'] == '' and st.session_state['secret_order'] == '':
        with placeholder.container():
            st.markdown("""
            > Insert your :orange[Paper Trading] Alpaca API and Secret Key to connect to your Alpaca account. 
            > If you do not have an Alpaca account, you can create one [here](https://app.alpaca.markets/signup).
            """)
            with st.form("Input API and Secret Key"):
                api_key = st.text_input('API Key', help='Login in to your Alpaca account to get your API & secret key (Paper Trading)')
                secret_key = st.text_input('Secret Key', type='password') 
                email = st.text_input('Email (Optional)', help='Enter your email address to receive updates on your trades')               
                submit_button = st.form_submit_button(label='Connect')

                st.session_state['api_key_order'] = api_key
                st.session_state['secret_order'] = secret_key
                st.session_state['email_order'] = email
                
                if submit_button:
                    with st.spinner('Connecting to Alpaca...'):
                        time.sleep(1.5)   

    try:
        api = tradeapi.REST(st.session_state['api_key_order'], st.session_state['secret_order'], base_url='https://paper-api.alpaca.markets', api_version='v2')
        account = api.get_account()
        if account.status == 'ACTIVE':
            st.success('Connected to Alpaca!')
            placeholder.empty()

            # get user to choose days to trade or cancel
            with st.form("Select days to trade or cancel"):
                option = st.selectbox("Select days to trade or cancel", options=['1', '3', '5', '10', '30', '60', '90', 'Indefinite', 'Cancel'])
                submit_button = st.form_submit_button(label='Submit')

                if submit_button:
                    with st.spinner('Submitting...'):
                        time.sleep(2.5) # give time for connection to be established
                        #submit query to database
                        today = time.strftime('%Y-%m-%d')                       
                        try:
                            engine.execute("""
                                    INSERT INTO users (api_key, secret_key, days_to_trade, email, date_submitted)
                                    VALUES (%s, %s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE 
                                    days_to_trade = VALUES(days_to_trade),
                                    email = VALUES(email),
                                    date_submitted = VALUES(date_submitted)
                                """, (st.session_state['api_key_order'], st.session_state['secret_order'], option, st.session_state['email_order'], today))
                            st.success('You\'re all set! Feel free to explore the other tabs, or exit this page.')
                            del st.session_state['api_key_order']
                            del st.session_state['secret_order']
                            del st.session_state['email_order']

                        except SQLAlchemyError:
                            st.error('Note: Server operating hours are 10:00 - 22:00 GMT+8 daily. If there is an error, please click the "Submit" button again. Else if the problem persists, please use the contact form to log the error.')             

        elif account.status == 'INACTIVE':
            st.error('Inactive Alpaca account.')          

    except ValueError:
        del st.session_state['api_key_order']
        del st.session_state['secret_order']
        del st.session_state['email_order']
        pass

    except requests.HTTPError:
        st.error('Invalid Alpaca API or Secret Key. Please double check your API and Secret Key.')
        del st.session_state['api_key_order']
        del st.session_state['secret_order']
        del st.session_state['email_order']
    
    except tradeapi.rest.APIError:
        st.error('By any chance are you using your Live Trading API and Secret Key? Please use your Paper Trading API and Secret Key.')
        del st.session_state['api_key_order']
        del st.session_state['secret_order']
        del st.session_state['email_order']
