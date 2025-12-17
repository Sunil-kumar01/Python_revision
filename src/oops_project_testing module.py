from Module_bank_accounts import * #importing everything from bank_accounts module which we defined in another file called bank_accounts.py

Dave = BankAccount(100,"Dave")
John = BankAccount(150,"John")

#now go back to bank_account file and add methods to the class 

#I defined the Getbalance method now le just call that
Dave.getBalance()
John.getBalance()

#now just add deposit method in back_account file
Dave.deposit(500) # this will now update with 500 and give us 600 as dave had 100+500

#Now lets start withdrawing money and this will be bit tricky as withdrawing need to check the balance as well first

Dave.withdraw(10000) # this should give an error as dave does not have this much balance
John.withdraw(50) # this should work as john has 150 balance

#Now let us test the transfer method we just added in the bank_account file
Dave.transfer(200, John) # this should work as dave has 600 balance after deposit
John.transfer(500, Dave) # this should give error as john has only 100