
import random
from datetime import datetime as dt

logs = open("bankingLogs.txt", "a+")
cred = open("credentials.txt", "a+")
cry = open("credentials.txt", "r")
opera = open("operaLogs.txt", "a+")
operalog = open("operaLogs.txt", "r")


def fprint(string):
    print(string)
    logs.write(string + "\n")


def generate_txn():
    val = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join(random.sample(val, 7))


def generate_cid():
    numbers = '0123456789ABCDEF'
    cid = str("".join(random.sample(numbers, 4)))
    return cid


class Account:
    def __init__(self, name, balance, password, customer_id):
        self.name = name
        self.balance = int(balance)
        self.password = password
        self.cid = customer_id

    def withdraw(self, withdraw_amount):
        if self.balance > int(withdraw_amount):
            self.balance -= withdraw_amount
            fprint(f"You have withdrawn Rs.{withdraw_amount} from your account")
            fprint(f"Your available balance is Rs. {self.balance}")
            opera.write(f"{self.cid} {generate_txn()} Withdrawal {self.name} {self.balance} {dt.now()}\n")

            return withdraw_amount
        else:
            fprint(f"Your withdrawal amount is more than your account balance.")
            fprint(f"Your available balance is Rs. {self.balance}")
            return 0

    def deposit(self, deposit_amount):
        if deposit_amount > 0:
            self.balance += deposit_amount
            fprint(f"You have deposited Rs.{deposit_amount} successfully.")
            fprint(f"Now your account balance is Rs. {self.balance}")
            opera.write(f"{self.cid} {generate_txn()} Deposit {self.name} {self.balance} {dt.now()}\n")

        else:
            fprint("Your deposit amount should be at least 1 rupee.")

    def change_password(self):
        passwd = input("Enter the old password : ")
        if passwd == self.password:
            new_password = input("Enter the new password : ")
            confirm_password = input("Confirm the new password : ")
            if confirm_password == new_password:
                self.password = new_password
                fprint("You have changed your account password successfully. ")
                cred.write(f"{self.cid} {self.name} {self.password}\n")

            else:
                fprint("Your new password does not match with confirm password.")
        else:
            fprint("Try again!")

    def check_pass(self):
        password = input("Enter your password : ")
        if password == self.password:
            fprint(f" Welcome, {self.name}")

            fprint("Choose from following operations :")
            operation = input("A to Check Balance \nB to withdraw amount \nC to deposit amount " +
                              "\nD to change password \nE to check statements \nF to exit \n----:").upper()
            if operation == "A":
                fprint(f"Your account balance is Rs.  {self.balance}")
            elif operation == "B":
                amount = int(input("Enter the amount you want to withdraw : "))
                self.withdraw(amount)
            elif operation == "C":
                amount = int(input("Enter the amount you want to deposit : "))
                self.deposit(amount)
            elif operation == "D":
                self.change_password()
            elif operation == "E":
                self.view_statements()
            else:
                print("Choose a valid operation.")

        else:
            fprint("Your password does not match.")

    def view_statements(self):
        statements = operalog.read().strip().split('\n')
        for statement in statements:
            if statement[0:4] == self.cid:
                print(statement)


def create_account():
    name = input("Create your username that has to be in one word: ")
    balance = input("Enter the amount you want to deposit : ")
    if int(balance) > 0:
        password = input("Create password for your account : ")
        confirm_password = input("Confirm your password : ")

        if password == confirm_password:
            cus_id = generate_cid()
            customer = Account(name, balance, password, cus_id)
            fprint(
                f"Mr/Mrs. {customer.name}, Your account has been successfully created with customer ID  {customer.cid} "
                f"and initial balance Rs. {customer.balance}")

            opera.write(f"{cus_id} {generate_txn()} Deposit {customer.name} {customer.balance} {dt.now()}\n")

            cred.write(f"{customer.cid} {customer.name} {customer.password}\n")
            choice = "y"
            while choice == "y":
                choice = input("Do you perform any operations on your account ? (Y/N) ").lower()
                if choice == "y":
                    customer.check_pass()
                else:
                    choice = "n"
                    fprint("Thank you for using our services.")

        else:
            fprint("Passwords don't match. Try again.")
    else:
        fprint("Your deposit should be at least 1 rupee.")


def check_account():
    usr_name = input("Enter the name : ")
    usr_cid = input("Enter the customer ID : ")
    usr_pass = input("Enter the password : ")

    usr = usr_cid + " " + usr_name + " " + usr_pass
    usr_logs = []

    op_logs = cry.read().strip().split('\n')

    if usr in op_logs:

        operations = operalog.read().strip().split('\n')
        for operation in operations:
            if operation[0:4] == usr_cid:
                usr_logs.append(operation)

        last_txn = usr_logs[len(usr_logs) - 1]

        last_details = last_txn.split(" ")
        balance = last_details[4]

        customer = Account(name=usr_name, balance=balance, password=usr_pass, customer_id=usr_cid)

        fprint(f"Welcome, Mr/Mrs. {customer.name}. We found your account with balance Rs. {customer.balance}")

        choice = 1
        while choice == 1:
            fprint("Choose from following operations :")
            operation = input("A to Check Balance \nB to deposit amount \nC to withdraw amount " +
                              "\nD to change password \nE to check statements \nF to exit \n----:").upper()
            if operation == "A":
                fprint(f"Your account balance is Rs.  {customer.balance}")

            elif operation == "B":
                amount = int(input("Enter the amount you want to withdraw : "))
                customer.withdraw(amount)

            elif operation == "C":
                amount = int(input("Enter the amount you want to deposit : "))
                customer.deposit(amount)

            elif operation == "D":
                customer.change_password()

            elif operation == "E":
                customer.view_statements()

            elif operation == "F":
                choice = 0
                fprint("Thank you for using our services .")
                break

            else:
                fprint("Choose a valid operation.")

    else:

        fprint("Oops, We couldn't find your account.")


sign = input("Choose A if you are already a customer else choose B to create account : ")
if sign == "A":
    check_account()
elif sign == "B":
    create_account()
else:
    fprint("Choose a valid option.")
logs.write("\n----------------------------------------------------------------------\n")
