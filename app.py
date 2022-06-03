import os
import json
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

def transaction_page():
    buyer = st.selectbox("Select Account", options=accounts)
    seller = st.text_input("Vendor's address")
    price = st.text_input("price")
    if st.button("dewit"):
        # Cast price to float here so we arent casting blank text
        price = float(price)
        transactions_list = contract.functions.getTransactionHistory(buyer).call()
        # Check if this is the 4th transaction in the list
        if len(transactions_list) % 4 == 0:
            price = price * 0.75
        price = price * (10*18)
        contract.functions.makeTransaction(buyer, seller, int(price))

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

def readme():

    image = Image.open('Images/Gympay.png')
    st.image(image)
    st.markdown(
        
        """ 

    ## Research
    Minimizing transaction, operational and admin costs by utilising blockchain technology for fitness centres and professionals with a SaaS application called GymPay.

    ## Getting Started
    Using the chrome browser for best viewing, view the dashboard using the link below:

    https://nbviewer.org/github/Dottie-Doutre/GymPay/blob/main/gympay_analysis.ipynb

    The dashboard is embedded for you to navigate between the tabs outlining our findings.

    The code in which was used to generate the dataframes, charts and conclusions are displayed below.

    ## PDF Files of Research and Presentation

    Here are the PDF files of the market research and presentation we created to compliment the data anaylsis. You can click them below or find them above!
    """)
    
    st.markdown("""
    1.[GymPay_Market_Research](https://github.com/Dottie-Doutre/GymPay/blob/main/GYMPAY_MARKET_RESEARCH_2022.docx.pdf)  
    2.[GymPay_Presentation](https://github.com/Dottie-Doutre/GymPay/blob/main/Gympay_presentation.pdf)

    ## Built With
    Jupyter-lab

    Python

    Panel (Pygal, numpy, seaborn, hvplot, matplotlib, plotly.express)

    ## Research Questions
    What is the market demographic?
    ```
    Age, Use Frequency, Crypto User, Smartphone Use
    ```
    What is the market size and oppurtunity?
    ```
    Australia, Addressable Market (Total and Serviceable)
    ```
    What is the competitive landscape?
    ```
    Existing Providers, Cost/Benefit for fitness centres, Cost/Benefit for Gym members
    ```
    ## Summary of findings
    > Increase in smartphone users and cryptocurrency adoption, with a strong negative linear relationship via correlation analysis.

    > There is a steady increase of gym establishments in Australia, with most of the age group demographic within the 25 up to 44 years dominating the use of gyms. 
    Addressing a large portion of the Australian population as a serviceable market.

    > The combination of increasing gym establishments, cryptocurrency adoption and smartphone users, presents GymPay as a valuable SaaS application that will benefit both gyms and customers as presented in the cost benefit analysis.

    > Cost savings of GymPay as a solution is 124x cheaper than existing solutions.

    ## Breakdown of analysis

    ### What is the Market Demographic?
    Analysed the market demographic to help us understand our target market as to help achieve a product/market fit.

    Data source utilised - finder.com.au
    ```
    Created dataframes (crypto_df, smart_df) by reading in csv files.

    Created dataframe (crypto_smart_phone) by concatinating that combination of the two dataframes mentioned perviously.

    Calculate correlation of crypto_smart_phone dataframe (produced a table and heatmap). Used a define function = correlation_table_function and total_opts_table_function.

    Created a pn.pane using Matplotlib to add to dashboard.
    ```
    Conclusion:

    There is a steady increase in both crypto and smartphone users.

    Through our analysis we concluded a correlation factor of -0.69, leaning towards a more negative linear relationship. This indicates for the time being there is a strong relationship between the two factors trending in a negative slope.

    But there is a potential for growing market for gym users and the utility use of GymPay. """)

    image_1 = Image.open('Images/Research/heatmap_cyrpto_smartphone_users.png')
    st.image(image_1)

    st.markdown("""
    ### What is the Market Size Opportunity?
    This section of the analysis was to determine the size of the market and opportunity. Also to calculate the scale for a potential startup for investors and founders.

    Data source utilised - Kaggle
    ```
    Created dataframes (gym_est_df) by reading in csv files.

    Used a new library function not currently explored (pygal) to create a bar graph.
    ```
    Conclusion:
    There is a great opportunity to utlise and scale the application. As it is steadily increasing every year. The total addressiable market (TAM) of 6.8 gym users averaging about 3 gym sessions a week. 

    Equating to 20,400,000 transactions a week, 2,900,000 transactions a day on a pay as you go basis.

    With this finding the serviceable addressabe market is approximately 72% of TAM fit into the age category of 15-55. """)

    image_2 = Image.open('Plots/gym_est_bar.png')
    st.image(image_2)

    image_3 = Image.open('Plots/gym_data.png')
    st.image(image_3)

    image_4 = Image.open('Images/Research/bokeh_plot_smartphone_crypto_users_title.png')
    st.image(image_4)

    image_5 = Image.open('Plots/gym_horizontalbar_market_potential.png')
    st.image(image_5)

    st.markdown("""
    ### What is the existing alternative?
    This section was to understand the competitive landscape that can allow GymPay to innovate on points of weakness with the current competition.
    Data source utilised - Statista
    ```
    Created dataframes (total_ops_df) by reading in csv files.

    Used hvplots (stacked and line) to outline the difference in total cost comparison between businesses and Hedera (cryptocurrency used as an example) via transactional occurences.
    ```
    Conclusion:

    GymPay cost savings advantage will scale with size.

    Cost savings of Hedera (cryptocurrency example) scale linearly against all current payment methods.

    As an example with 100,000 transactions using the Hedera blockchain network, the gym owner would save $174,000. """)

    image_6 = Image.open('Images/Research/Cost_savings.PNG')
    
    st.markdown("""
    ## Example Analysis Graphs """)

    image_7 = Image.open('Images/Research/traditional_vs_blockchain_price.png')
    st.image(image_7)

    image_8 = Image.open('Images/Research/cost_savings_table.png')

    st.markdown("""
    ## Versioning
    Two main branches used for version control.
    Main and sub.

    The team utilised the "sub" branch to input changes created before pushing into the main branch.

    ## Contributing Sources
    Finder.com.au

    Kaggle (Data Science platform by Google)

    Statista (Market and consumer data aggregator)

    Australian Burea of Statistics

    Fitness Australia (Independent Research Agency)

    Blockchain.com """)

def wallet_page():
    accounts = w3.eth.accounts
    account = accounts[0]
    user_wallet = st.selectbox("Select Account", options=accounts)
    user_balance = contract.functions.balanceOf(user_wallet).call()
    st.markdown(user_balance)

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