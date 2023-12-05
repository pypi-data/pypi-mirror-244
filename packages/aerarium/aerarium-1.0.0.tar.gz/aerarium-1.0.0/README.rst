aerarium
============

A simple command line tool for tracking my finances.


Features
--------

- Check account balance

  Use the ``--balance`` or ``-b`` flag to print the current account balance.

- Withdraw amount

  Use the ``--withdraw <amount>`` or ``-w <amount>`` option to withdraw money, along with a description and category prompt.
  Prints new account balance.

- Deposit amount
  
  Use the ``--deposit <amount>`` or ``-d <amount>`` option to deposit money, along with a description and category prompt.
  Prints new account balance.  

- List transactions
  
  Use the ``--transactions`` or ``-t`` flag to print a list of all transactions.

- Predict spending
    
  Use the ``--predict <number_of_days>`` or ``-p <number_of_days>`` flag to print a prediction of spending for next n days.

- Help information

  Use ``--help`` to print usage help.

Usage
-----

Some examples:

.. code-block::

   $ aerarium --balance
   Current balance: $1000
   
   $ aerarium --withdraw 100
   Enter withdrawal description: Groceries  
   Enter withdrawal category: Food
   Balance: 900
   
   $ aerarium --deposit 500
   Enter deposit description: Salary
   Enter deposit category: Income
   Balance: 1400
   
The configuration file contains the account name and starting balance.

**Note**: This project is under active development.
