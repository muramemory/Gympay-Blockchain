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

from readme_page import readme

load_dotenv()

# Setting for fullpage

st.set_page_config(page_icon=("Images/gympay_test_logo_2.png"))

### Sidebar 

### Create Top Bar ###

st.markdown(
    "##### Made in [![image_add](https://media-thumbs.golden.com/Ce1V_LeVgumkUOeYYkixMAoRQNU=/200x200/smart/golden-storage-production.s3.amazonaws.com%2Ftopic_images%2Fe509a9c1bb3541c38c30b22a2173d456.png)](https://streamlit.io/) by [Gympay Team](https://github.com/muramemory/Gympay-Blockchain)"
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

    user_wallet = st.selectbox("Select Account", options=accounts)
    user_balance = contract.functions.balanceOf(user_wallet).call()
    user_balance = w3.fromWei(int(user_balance), "ether")
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

        # Grab the list of transactions (This will be a list of addresses)
        transactions_num = contract.functions.getNumTransactions(buyer).call()

        # Check if this is the 4th transaction in the list
        # A discount of 25% is applied on every 4th transaction
        if transactions_num % 4 == 0 & transactions_num != 0:
            price = price * 0.75
        price = w3.toWei(price, "ether")
        contract.functions.approve(buyer, price).transact({'from': account, 'gas': 1000000})
        contract.functions.makeTransaction(buyer, seller, price).transact({'from': buyer, 'gas': 1000000})

def contact_page():
    image = Image.open('Images/Gympay.png')
    st.image(image)
    st.title(f"{selected} the GymPay team")
    st.markdown("""If you have any questions regarding the GymPay project or any $FIT coin queries please submit it using the form below.""")
    st.markdown("""We will aim to get back to you within 48 hours.""")
    st.markdown("""Thank you for your support!""")
    st.markdown("""GymPay Team""")
    st.markdown("""  """)
    with st.form(key='GymPay Form:'):
        text_input = st.text_input(label='Enter your question / query below:')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            st.write(f"Form is now submitted!")


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

    # st.image('https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0x63d492cA657813bfC86c18c8ceA485CF632EF002')



# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu", # required
        options=["Home", "Research", "Wallet", "Transaction","Contact"], #required
        icons=["house","book","wallet","cash","envelope"],
        menu_icon="cast",
        default_index=0,
    )



# Based on the value of selected, each pages respective function is called
if selected == "Home":
    home_page()
elif selected == "Research":
    st.title(f"Welcome to the GymPay {selected} information page")
    readme()
elif selected == "Wallet":
    st.title(f"Welcome to the Wallet Page where you can select your wallet and check your summary")
    wallet_page()
elif selected == "Transaction":
    st.title(f"Welcome to the transcation page")
    transaction_page()
elif selected == "Contact":
    contact_page()
elif selected == "Make a Purchase":
    transaction_page()