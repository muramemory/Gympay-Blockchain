import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

load_dotenv()

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


image = Image.open('Images/Gympay.png')
st.image(image)

st.text('Gympay is a service that enables you to pay for your gym membership with')
st.text('cryptocurrency. Blockchain technology enables cheaper and faster transactions') 
st.text('which gives gym owners opportunities to offer great services at great prices.')
st.text('Purchase Fitcoin below and use your digital wallet to scan into partnered gym')
st.text('facilities for instant access and opportunties to earn rewards.')

################################################################################
# Select wallet
################################################################################

accounts = w3.eth.accounts
account = accounts[0]
user_wallet = st.selectbox("Select Account", options=accounts)
user_balance = contract.functions.balanceOf(user_wallet).call()
st.markdown(user_balance)

################################################################################
# Withdraw and Deposit
################################################################################

amount = st.text_input("Amount to purchase")
if st.button("Purchase"):
    contract.functions.deposit(user_wallet, int(amount)).transact({'from': account, 'gas': 1000000})

amount = st.text_input("Amount to sell")
if st.button("Sell"):
    contract.functions.withdraw(user_wallet, int(amount)).transact({'from': account, 'gas': 1000000})
