pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";


/*
Coin Description
*/
contract Fitcoin_Token is ERC20, ERC20Detailed, ERC20Mintable{
    using SafeMath for uint;

    mapping(address => Transaction[]) public transactionHistory; // Record of transactions made by accounts
    mapping(address => Discount) public discounts; // Record of reward status of accounts
    uint discountID;

    /*
        Initialise coin as Fitcoin (FIT) with an initial supply of 0 (by not declaring it)
        and 0 decimals so we can just look at whole numbers
    */

    constructor () ERC20Detailed("Fitcoin", "Fit", 0) public{
        discountID = 0;
    }


    function getTransactionHistory(address account) public view returns(Transaction[] memory){
        return transactionHistory[account];
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
    */
    function makeTransaction(address buyer, address seller, uint price) public{

        Transaction purchase = new Transaction(buyer, seller, price);
        transactionHistory[buyer].push(purchase);
        
        transferFrom(buyer, seller, price);

    }

}

/*
    Transaction object to store any info we need.
    For now we have buy/sell addresses but more can be added
*/
contract Transaction{
    address buyAddress;
    address sellAddress;
    uint date;
    uint amount;

    constructor(address buyer, address seller, uint price) public{
        buyAddress = buyer;
        sellAddress = seller;
        date = now;
        amount = price;
    }
}

// Currently unused, only required if discounts need to be saved
contract Discount{
    //We can't really do % discounts as solidity does not do floats
    uint amount;
    uint ID;
}