import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

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
    with open(Path('fitcoin_abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()


################################################################################
# Select wallet
################################################################################

accounts = w3.eth.accounts
account = accounts[0]
user_wallet = st.selectbox("Select Account", options=accounts)

################################################################################
# Withdraw and Deposit
################################################################################

if st.button("Purchase Fitcoin"):
    with st.sidebar:
        amount = st.text_input("Amount to purchase")
        if st.button("Purchase"):
            contract.functions.deposit(user_wallet, amount).transact({'from': account, 'gas': 1000000})

if st.button("Sell Fitcoin"):
    with st.sidebar:
        amount = st.text_input("Amount to sell")
        if st.button("Sell"):
            contract.functions.wihdraw(user_wallet, amount).transact({'from': account, 'gas': 1000000})
