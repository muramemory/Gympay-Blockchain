import os
import json
import requests
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import pandas as pd
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime

from readme_page import readme

load_dotenv()

# Setting for fullpage

st.set_page_config(page_icon=("Images/gympay_test_logo_2.png"))

### Sidebar 

### Create Top Bar ###

st.markdown(
    "##### A project by the [Gympay Team](https://github.com/muramemory/Gympay-Blockchain) visit our github :computer:"
)


# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Fitcoin ABI
    with open(Path('abi/fitcoin_abi.json')) as f:
        fitcoin_abi = json.load(f)
        
    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=fitcoin_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()

# Load the accounts since they may be used anywhere in the program
accounts = w3.eth.accounts
account = accounts[0]

# Home page streamlit page
def home_page():
    image = Image.open('Images/Gympay.png')
    st.image(image)
    st.markdown("""  """)
    st.markdown("""
    Gympay  is a service that enables you to pay for your gym membership with cryptocurrency. Blockchain technology enables cheaper and faster 
    transactions which gives gym owners opportunities to offer great services at great prices.
    Purchase Fitcoin below and use your digital wallet to scan into partnered gym
    facilities for instant access and opportunties to earn rewards.
    """)
    # st.markdown("""## Fitcoin """)
    st.markdown('**Fitcoin** is the token used to pay for your gym membership fees.') 
    st.markdown('The more frequently you go to the gym, the more rewards you can earn')
    st.markdown("""### Connect your wallet and buy Fitcoin below """)
    user_wallet = st.selectbox("Select Account", options=accounts)
    user_balance = contract.functions.balanceOf(user_wallet).call()
    user_balance = w3.fromWei(int(user_balance), "ether")
    st.markdown(f"Wallet Total:")
    st.markdown(f"Fitcoin")
    st.markdown(user_balance)
    
# ################################################################################
# # Withdraw and Deposit
# ################################################################################

    purchase_amount = st.number_input("Amount to purchase", min_value=0, value=0, step=1, help="Please enter an amount to purchase")
    if st.button("Purchase"):
        purchase_amount = w3.toWei(int(purchase_amount), "ether")
        contract.functions.deposit(user_wallet, int(purchase_amount)).transact({'from': account, 'gas': 1000000})

    sell_amount = st.number_input("Amount to sell", min_value=0, value=0, step=1, help="Please enter an amount to sell")
    if st.button("Sell"):
        sell_amount = w3.toWei(int(sell_amount), "ether")
        contract.functions.withdraw(user_wallet, int(sell_amount)).transact({'from': account, 'gas': 1000000})

def transaction_page():
    buyer = st.selectbox("Select Account", options=accounts)
    seller = st.text_input("Vendor's address")
    price = st.text_input("Price")
    if st.button("Make Transaction"):
        # Cast price to float here so we arent casting blank text
        price = float(price)
        
        # Grab the list of transactions
        transactions_filter = contract.events.Transaction.createFilter(fromBlock=0)
        transactions = transactions_filter.get_all_entries()
        
        if transactions:
            print(len(transactions) % 4)
            # Check if this is the 4th transaction in the list
            # A discount of 25% is applied on every 4th transaction
            if len(transactions) % 4 == 0:
                print(len(transactions) % 4)
                price = price * 0.75
        
        price = w3.toWei(price, "ether")
        contract.functions.approve(buyer, price).transact({'from': account, 'gas': 1000000})
        contract.functions.makeTransaction(buyer, seller, price).transact({'from': buyer, 'gas': 1000000})

def contact_page():
    image = Image.open('Images/Gympay.png')
    st.image(image)
    st.title(f":e-mail:{selected} the GymPay team!")
    st.markdown("""If you have any questions regarding the GymPay project or any $FIT coin enqueries please submit it using the form below.""")
    st.markdown("""We will aim to get back to you within 48 hours.""")
    st.markdown("""Thank you for your support! :muscle:""")
    contact_form = """
        <form action="https://formsubmit.co/ddoutre90@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false"><br>
            <input type="text" name="name" placeholder="Enter your name" required><br>
            <input type="email" name="email" placeholder="Enter Your email" required><br>
            <textarea name="message" placeholder="Type your message here"></textarea><br>
            <button type="submit">Send</button>
        </form>
        """
    st.markdown(contact_form, unsafe_allow_html=True)

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("Images/style.css")



def wallet_page():
    accounts = w3.eth.accounts
    account = accounts[0]
    user_wallet = st.selectbox("Select Account", options=accounts)
    selected = user_wallet
    user_balance = contract.functions.balanceOf(user_wallet).call()
    user_balance = w3.fromWei(int(user_balance), "ether")
    st.markdown(f"Wallet Total:")
    st.markdown(f"Fitcoin")
    st.markdown(user_balance)

    if user_wallet == selected:
        st.image('https://api.qrserver.com/v1/create-qr-code/?size=150x150&data='+(user_wallet))


    # Display transaction history
    transactions_df = pd.DataFrame(columns=["From","To", "Time", "Price"])

    transactions_filter = contract.events.Transaction.createFilter(fromBlock=0)
    transactions = transactions_filter.get_all_entries()
    for transaction in transactions:
        transaction_dictionary = dict(transaction)
        buyer = transaction_dictionary["args"]["buyer"]
        seller = transaction_dictionary["args"]["seller"]
        time = transaction_dictionary["args"]["date"]
        time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        price = transaction_dictionary["args"]["amount"]
        price = w3.fromWei(price, "ether")
        transactions_df = transactions_df.append({"From": buyer, "To": seller, "Time": time, "Price": price}, ignore_index=True)
    
    transactions_df = transactions_df.set_index("Time")
    
    st.dataframe(transactions_df)



# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu", # required
        options=["Home",  "Wallet", "Transaction","Research","Contact"], #required
        icons=["house","book","wallet","cash","envelope"],
        menu_icon="cast",
        default_index=0,
    )



# Based on the value of selected, each pages respective function is called
if selected == "Home":
    home_page()
elif selected == "Wallet":
    image = Image.open('Images/Gympay.png')
    st.image(image)
    st.title(f"Welcome to the Wallet Page")
    st.markdown("In this page you can select your wallet, check your summary and also your transaction history.")
    wallet_page()
elif selected == "Transaction":
    image = Image.open('Images/Gympay.png')
    st.image(image)
    st.title(f"Welcome to the Transaction page")
    st.markdown(f"Transfer your funds to another wallet address here.")
    transaction_page()
elif selected == "Research":
    image = Image.open('Images/Gympay.png')
    st.image(image)
    st.title(f"Welcome to the GymPay {selected} Information page")
    readme()
elif selected == "Contact":
    contact_page()
elif selected == "Make a Purchase":
    transaction_page()