class AtmCard:
    def __init__(self, cardnumber , pin, balance):
        self.cardnumber = cardnumber
        self.pin = pin
        self.balance = balance
    def ShowBalance(self):
        print(self.balance)
    def Withdraw(self,amount):
        if amount<=self.balance:
            self.balance-=amount
            print(f"Amount withdrawn is {amount}, the new balance is {self.balance}")
        else:
            print("Not Enough balance in Account")
    def Deposit(self,amount):
        self.balance+=amount
        print(f"Amount Deposited is {amount}, the new balance is {self.balance}")
    def Changepin(self,Newpin):
        self.pin = Newpin
        print(f"The New pin is set to{Newpin}")


Card1 = AtmCard(1001001,1947,1000)
Card2 = AtmCard(1001002,1936,1000)
Card3 = AtmCard(1001003,1911,1000)
Atmdict={Card1.cardnumber:Card1,Card2.cardnumber:Card2,Card3.cardnumber:Card3}
Card = int(input("Enter your Card Number "))
if Card in Atmdict:
    Pin=int(input("Enter the pin "))
    active=Atmdict[Card]
    if active.pin==Pin:
        while(True):
            print("What do you want to perform \nPress 1 to check balance \
            \nPress 2 to Deposit \nPress 3 to Withdraw \nPress 4 to change pin \nPress 5 to exit ")
            Press = int(input("Enter your choice "))
            match Press:
                case 1:
                    active.ShowBalance()
                case 2:
                    dep=int(input("Enter the Amount you want to Deposit "))
                    active.Deposit(amount=dep)
                case 3:
                    wit=int(input("Enter the Amount you want to Withdraw "))
                    active.Withdraw(amount=wit)
                case 4:
                    Np=int(input("Enter the New pin "))
                    active.Changepin(Np)
                case 5:
                    break
    else: print("incorrect pin")
else:
    print("invalid card")



