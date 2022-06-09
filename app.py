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
import pickle
import streamlit_authenticator as stauth # pip install streamlit-authenticator
from readme_page import readme

load_dotenv()

# Setting for fullpage

st.set_page_config(page_icon=("Images/gympay_test_logo_2.png"))

# --- USER AUTHENTICATION ---
names = ["Tester", "Craig Braganza", "Kevin Chen", "Dorothy Doutre", "Anthony Mura"]
usernames = ["test", "cbraganza", "kchen", "ddoutre", "amura"]

# Load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "fitcoin_dashboard", "abcdef")

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:


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
        
        
    # ################################################################################
    # # Withdraw and Deposit
    # ################################################################################

    def transaction_page():
        buyer = st.selectbox("Select Account", options=accounts)

        user_balance = contract.functions.balanceOf(buyer).call()
        user_balance = w3.fromWei(int(user_balance), "ether")
        st.markdown(f"Wallet Balance: FIT {user_balance}")
        
        seller = st.text_input("Vendor's address")

        # Check if seller is a valid address
        # For now this wont host the execution of the program, solidity will prevent any bad executions
        if not(seller in accounts):
                st.markdown("The seller is not a valid address")
        
        price = st.number_input("Amount to transfer", min_value=0, value=0, step=1, help="Please enter an amount to transfer")
        
        # Grab the list of transactions
        transactions_filter = contract.events.Transaction.createFilter(fromBlock=0)
        transactions = transactions_filter.get_all_entries()
        # Set discount flag
        discount_flag = False
        if transactions:
            # Check if this is the 4th transaction in the list
            # A discount of 25% is applied on every 4th transaction
            if len(transactions) % 4 == 0:
                discount_flag = True
                st.markdown("Your next purchase will have a 25% discount")
            else:
                st.markdown(f"You have {4 - (len(transactions) % 4)} transactions until your next discount")
        else:
            st.markdown(f"You have {4 - (len(transactions) % 4)} transactions until your next discount")
        if st.button("Make Transaction"):
            # Cast price to float here so we arent casting blank text
            price = float(price)

            if discount_flag:
                price = price * 0.75
            
            price = w3.toWei(price, "ether")
            contract.functions.approve(buyer, price).transact({'from': buyer, 'gas': 1000000})
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
        st.markdown("""### Connect your wallet and buy Fitcoin below """)
        accounts = w3.eth.accounts
        account = accounts[0]
        user_wallet = st.selectbox("Select Account", options=accounts)
        selected = user_wallet
        user_balance = contract.functions.balanceOf(user_wallet).call()
        user_balance = w3.fromWei(int(user_balance), "ether")
        st.markdown(f"Wallet Balance: FIT {user_balance}")

        if user_wallet == selected:
            st.image('https://api.qrserver.com/v1/create-qr-code/?size=150x150&data='+(user_wallet))

        # The UI and functionality will change depending on which account is using the program
        if account == user_wallet:
            root_wallet_page()
        else:
            user_wallet_page(user_wallet)

        # Display transaction history
        transactions_df = pd.DataFrame(columns=["From","To", "Time", "Price"])

        transactions_filter = contract.events.Transaction.createFilter(fromBlock=0)
        transactions = transactions_filter.get_all_entries()
        for transaction in transactions:
            transaction_dictionary = dict(transaction)

            # Get buyer and seller
            buyer = transaction_dictionary["args"]["buyer"]
            seller = transaction_dictionary["args"]["seller"]

            # Grab time and translate from UTC format
            time = transaction_dictionary["args"]["date"]
            time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

            # Get price of transaction
            price = transaction_dictionary["args"]["amount"]
            price = w3.fromWei(price, "ether")

            # Append if the information is relevant to the chosen wallet
            if (buyer == user_wallet or seller == user_wallet):
                transactions_df = transactions_df.append({"From": buyer, "To": seller, "Time": time, "Price": price}, ignore_index=True)
        
        transactions_df = transactions_df.set_index("Time")
        
        st.dataframe(transactions_df)

    # This page displays if the selected account on the wallet page is the root wallet
    def root_wallet_page():
        purchase_amount = st.number_input("Amount to mint", min_value=0, value=0, step=1, help="Please enter an amount to mint")
        if st.button("Mint"):
            purchase_amount = w3.toWei(int(purchase_amount), "ether")
            contract.functions.mint(account, int(purchase_amount)).transact({'from': account, 'gas': 1000000})
        sell_amount = st.number_input("Amount to burn", min_value=0, value=0, step=1, help="Please enter an amount to sell")
        if st.button("burn"):
            sell_amount = w3.toWei(int(sell_amount), "ether")
            contract.functions.burn(account, int(sell_amount)).transact({'from': account, 'gas': 1000000})

    # This page displays if the selected account on the wallet page is not the root wallet
    def user_wallet_page(user_wallet):
        purchase_amount = st.number_input("Amount to purchase", min_value=0, value=0, step=1, help="Please enter an amount to purchase")
        if st.button("Purchase"):
            purchase_amount = w3.toWei(int(purchase_amount), "ether")

            root_balance = contract.functions.balanceOf(account).call()
            
            # If the root account doesn't have enough money to purchase from it will mint the difference
            print(root_balance)
            print(purchase_amount)
            if root_balance < purchase_amount:
                difference = purchase_amount - root_balance
                
                contract.functions.mint(account, int(difference)).transact({'from': account, 'gas': 1000000})

            contract.functions.approve(account, purchase_amount).transact({'from': account, 'gas': 1000000})
            contract.functions.purchase(account, user_wallet, int(purchase_amount)).transact({'from': account, 'gas': 1000000})
        
        sell_amount = st.number_input("Amount to sell", min_value=0, value=0, step=1, help="Please enter an amount to sell")
        if st.button("Sell"):
            sell_amount = w3.toWei(int(sell_amount), "ether")

            contract.functions.approve(user_wallet, sell_amount).transact({'from': user_wallet, 'gas': 1000000})
            contract.functions.sell(account, user_wallet, int(sell_amount)).transact({'from': user_wallet, 'gas': 1000000})

        



    # Sidebar menu
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
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
        st.markdown("""Transfer your funds to another wallet address here.
        \n\nWhen making transactions, a 25% discount is automatically applied when you make your 4th transaction""")
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