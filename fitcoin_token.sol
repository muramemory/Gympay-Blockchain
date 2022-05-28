pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";


/*
Coin Description
*/
contract Fitcoin_Token is ERC20, ERC20Detailed, ERC20Mintable{

    mapping(address => Transaction[]) public transactionHistory; // Record of transactions made by accounts
    mapping(address => bool) public discountReward; // Record of reward status of accounts

    /*
        Initialise coin as Fitcoin (FIT) with an initial supply of 0 (by not declaring it)
        and 0 decimals so we can just look at whole numbers
    */

    constructor () ERC20Detailed("Fitcoin", "Fit", 0) public{
        
    }

    //Purchase Function calls mint on account

    function deposit (address account, uint256 amount) public{

	mint(account, amount);

    }

    // Purchase Function calls burn on account
    function withdraw (address account, uint256 amount) public{

	_burn(account, amount);

    }

    /*
        makeTransaction simulates making a transaction with a vendor
        The buyer and seller addresses are provided by the caller, as well as whether to apply a discount reward
        Each call will create a new transaction object
        The function will also award a discount if it is the 4th purchase since the previous discount
    */
    function makeTransaction(address buyer, address seller, bool applyReward) public{
        // Check if discount is requested. Program will check if a discount is eligible
        if (applyReward){
            require(discountReward[buyer], "This account is not eligible for a discount yet");
            discountReward[buyer] = false;
        }
        // Create new transaction object
        Transaction purchase = new Transaction(buyer, seller);
        transactionHistory[buyer].push(purchase);
        
        // Check if eligible for reward and apply
        if(transactionHistory[buyer].length % 4 == 0){
            discountReward[buyer] = true;
        }
    }

}

/*
    Transaction object to store any info we need.
    For now we have buy/sell addresses but more can be added
*/
contract Transaction{
    address buyAddress;
    address sellAddress;

    constructor(address buyer, address seller) public{
        buyAddress = buyer;
        sellAddress = seller;
    }
}