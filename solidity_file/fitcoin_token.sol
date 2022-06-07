pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";


/*

*/
contract Fitcoin_Token is ERC20, ERC20Detailed, ERC20Mintable{

    uint discountID;

    /*
        Initialise coin as Fitcoin (FIT) with an initial supply of 0 (by not declaring it)
        and 0 decimals so we can just look at whole numbers
    */

    constructor () ERC20Detailed("Fitcoin", "Fit", 18) public{
        discountID = 0;
    }

    // This even will keep track of every transaction made with the coin
    event Transaction (address buyer, address seller, uint date, uint amount);

    //Purchase Function calls mint on account
    function purchase (address root_account, address buyer, uint256 amount) public{

	    transferFrom(buyer, root_account, amount);

    }

    // Purchase Function calls burn on account
    function sell (address account, uint256 amount) public{

	    _burn(account, amount);

    }

    /*
        makeTransaction simulates making a transaction with a vendor
        The buyer and seller addresses are provided by the caller, as well as whether to apply a discount reward
        Each call will create a new transaction object
    */
    function makeTransaction(address buyer, address seller, uint price) public{

        emit Transaction(buyer, seller, now, price);
        
        transferFrom(buyer, seller, price);

    }

}
