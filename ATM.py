atm={4012001037141112:[1234,1000],4012001037167778:[2345,2000],4012001038443335:[3456,5000]}

card=int(input("Enter your ATM card number "))
auth=1
pin=int(input("Enter the pin "))
if atm[card][0]==pin:
    while(auth):       
        print("What do you want to perform ")
        print("Press 1 to check balance ")
        print("Press 2 to Deposit ")
        print("Press 3 to Withdraw ")
        print("Press 4 to change pin ")
        print("Press 5 to exit ")
        Press = int(input("Enter your choice "))
        if Press==5:
            auth=0
        elif Press==1:
            print(atm[card][1])
        elif Press==2:
            Deposit=int(input("Enter the amount you want to deposit "))
            atm[card][1]=atm[card][1]+Deposit
            print("the New Balance is ",atm[card][1])
        elif Press==3:
            Withdraw=int(input("Enter the amount you want to withdraw "))
            atm[card][1]=atm[card][1]-Withdraw
            print("the New Balance is ",atm[card][1])
        elif Press==4:
            Newpin=int(input("Enter the New pin "))
            atm[card][0]=Newpin
            print("the New Pin is ",Newpin)