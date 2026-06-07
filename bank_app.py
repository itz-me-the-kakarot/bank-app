import datetime
import json
import os
import streamlit as st

if "accounts" not in st.session_state:
    st.session_state.accounts = {}

def save_accounts():
    data = {}
    for acc_no, account in st.session_state.accounts.items():
        data[acc_no] = {
            "name": account.name,
            "balance": account.balance,
            "history": account.history
        }
    with open("accounts.json", "w") as f:
        json.dump(data, f)


class Account:
    def __init__(self, name, acc_no, balance,):
        self.name = name
        self.acc_no = acc_no
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        self.balance += amount       
        transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")       
        self.history.append(f"Deposited {amount} berries on {transaction_time}")


    def withdraw(self, amount):
        if amount > self.balance:
            return False
        else:
            self.balance -= amount
            transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history.append(f"Withdrew {amount} berries on {transaction_time}")
            return True           
            
    def check_balance(self):
        print(f"Dear {self.name}, your balance is: {self.balance} berries")

    def check_transaction_history(self):
        print(f"Transaction history for {self.name}:")
        for transaction in self.history:
            print(transaction)

def transfer(sender, receiver, amount):
    if amount > sender.balance:
        return False
    else:
        sender.withdraw(amount)
        receiver.deposit(amount)
        return True
    

def create_account():
    name = st.text_input("Enter your name:")
    acc_no = st.text_input("Enter your account number:")
    balance = st.number_input("Enter initial balance:", min_value=0)
    if st.button("Create"):
        if acc_no in st.session_state.accounts:
            st.error("Account number already exists. Please choose a different one.")
        else:
            st.session_state.accounts[acc_no] = Account(name, acc_no, balance)
            st.success(f"Account created successfully for {name} with account number {acc_no}.")
    save_accounts()
def deposit():
    acc_no = st.text_input("Enter your account number :")
    amount = st.number_input("Enter amount to deposit:", min_value=0)
    if st.button("Deposit"):
        if acc_no in st.session_state.accounts:
            st.session_state.accounts[acc_no].deposit(amount)
            st.success(f"Deposited {amount} berries to account {acc_no}.")
            save_accounts
        else:
            st.error("Account number not found. Please check and try again.")

def withdraw():
    acc_no = st.text_input("Enter your account number:   ")
    amount = st.number_input("Enter amount to withdraw:", min_value=0)
    if st.button("Withdraw"):
        if acc_no in st.session_state.accounts:
            if st.session_state.accounts[acc_no].withdraw(amount):
                st.success(f"Withdrew {amount} berries from account {acc_no}.")
                save_accounts()
            else:
                st.error("Insufficient balance. Please check your balance and try again.")
        else:
            st.error("Account number not found. Please check and try again.")   

def transfer_ui():
    
    sender_acc_no = st.text_input("Enter sender's account number:")
    receiver_acc_no = st.text_input("Enter receiver's account number:")
    amount = st.number_input("Enter amount to transfer:", min_value=0)
    if st.button("Transfer"):
        if sender_acc_no in st.session_state.accounts and receiver_acc_no in st.session_state.accounts:
            sender = st.session_state.accounts[sender_acc_no]
            receiver = st.session_state.accounts[receiver_acc_no]
            if transfer(sender, receiver, amount):
                st.success(f"Transferred {amount} berries from account {sender_acc_no} to account {receiver_acc_no}.")
                save_accounts()
            else:
                st.error("Insufficient balance. Please check the sender's balance and try again.")
        else:
            st.error("One or both account numbers not found. Please check and try again.")
    

def check_balance():
    acc_no = st.text_input("Enter your account number:    ")
    if st.button("Check Balance"):
        if acc_no in st.session_state.accounts:
            st.session_state.accounts[acc_no].check_balance()
            st.success(f"Your balance is: {st.session_state.accounts[acc_no].balance} berries.")
        else:
            st.error("Account number not found. Please check and try again.")



def load_accounts():
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as f:
            data = json.load(f)
            for acc_no, account_data in data.items():
                st.session_state.accounts[acc_no] = Account(
                    account_data["name"],
                    acc_no,
                    account_data["balance"]
                )
                st.session_state.accounts[acc_no].history = account_data["history"]
st.title("Welcome to the Bank App")
st.write("Please create an account to get started.")
tab1, tab2, tab3, tab4, tab5= st.tabs(["Create Account", "Deposit", "Withdraw", "Transfer", "Check Balance"])

load_accounts()

with tab1:
    create_account()


with tab2:
     deposit()

with tab3:
     withdraw()

with tab4:
    transfer_ui()

with tab5:
    check_balance()