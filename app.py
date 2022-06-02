import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import pandas as pd
from streamlit_option_menu import option_menu

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

# Sidebar Menu


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

    accounts = w3.eth.accounts
    account = accounts[0]
    user_wallet = st.selectbox("Select Account", options=accounts)
    user_balance = contract.functions.balanceOf(user_wallet).call()
    st.markdown(user_balance)
    
# ################################################################################
# # Withdraw and Deposit
# ################################################################################

    amount = st.text_input("Amount to purchase")
    if st.button("Purchase"):
        contract.functions.deposit(user_wallet, int(amount)).transact({'from': account, 'gas': 1000000})

    amount = st.text_input("Amount to sell")
    if st.button("Sell"):
        contract.functions.withdraw(user_wallet, int(amount)).transact({'from': account, 'gas': 1000000})

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu", # required
        options=["Home", "Projects", "Contact"], #required
        icons=["house","book","envelope"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    home_page()
elif selected == "Projects":
    st.title(f"Welcome to the GymPay {selected} information page")
elif selected == "Contact":
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

# Top of Page Image


# image = Image.open('Images/Gympay.png')
# st.image(image)

# st.markdown("""
# Gympay  is a service that enables you to pay for your gym membership with cryptocurrency. Blockchain technology enables cheaper and faster 
# transactions which gives gym owners opportunities to offer great services at great prices.
# Purchase Fitcoin below and use your digital wallet to scan into partnered gym
# facilities for instant access and opportunties to earn rewards.

# """)


################################################################################
# Select wallet
################################################################################

# accounts = w3.eth.accounts
# account = accounts[0]
# user_wallet = st.selectbox("Select Account", options=accounts)
# user_balance = contract.functions.balanceOf(user_wallet).call()
# st.markdown(user_balance)

# ################################################################################
# # Withdraw and Deposit
# ################################################################################

# amount = st.text_input("Amount to purchase")
# if st.button("Purchase"):
#     contract.functions.deposit(user_wallet, int(amount)).transact({'from': account, 'gas': 1000000})

# amount = st.text_input("Amount to sell")
# if st.button("Sell"):
#     contract.functions.withdraw(user_wallet, int(amount)).transact({'from': account, 'gas': 1000000})