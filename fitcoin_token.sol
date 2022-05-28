pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";


/*
Coin Description
*/
contract Fitcoin_Token is ERC20, ERC20Detailed, ERC20Mintable{

    /*
        Initialise coin as Fitcoin (FIT) with an initial supply of 0 (by not declaring it)
        and 0 decimals so we can just look at whole numbers
    */

    constructor () ERC20Detailed("Fitcoin", "Fit", 0) public{
        
    }

    /*
        Purchase Function

        @TODO: Call inherited mint function
    */
    function deposit (address account, uint256 amount) public{

	mint(account, amount);

    }

        /*
        Purchase Function

        @TODO: Call inherited burn function
    */
    function withdraw (address account, uint256 amount) public{

	_burn(account, amount);

    }

}



