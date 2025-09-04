from abc import ABC, abstractmethod
import datetime
from random import randint


class Person:
    """person with with basi details"""
    def __init__(self, name, address, phone):
        """Inieialize a person"""
        self.__name = name
        self.__address = address
        self.__phone = phone

    def get_details(self):
        """return tuple of basic details of person"""
        return (self.__name, self.__address, self.__phone)

class Account(ABC):
    """Abstract class so that different acoounts can be managed"""
    def __init__(self, account_number, balance, owner):
        """Initialize an Account"""
        self.account_number = account_number
        self._balance = balance
        self.owner = owner
        self.transactions = []
        self.status = "pending"

    def get_balance(self):
        """Return balance in float type"""
        return self._balance

    def add_transaction(self, txn):
        "record each transactions"
        self.transactions.append(txn)

    def __str__(self):
        """return representation of account"""
        return self.show_account_details()

    @abstractmethod
    def deposit(self, amount):
        """Deposit money"""
        pass

    @abstractmethod
    def withdraw(self, amount):
        """Withdraw money"""
        pass

    @abstractmethod
    def show_account_details(self):
        """Return account details as a string."""
        pass



class SavingsAccount(Account):
    """Savings account with interest feature."""
    def __init__(self, account_number, balance, owner):
        super().__init__(account_number, balance, owner)
        self.interest_rate = 3

    def deposit(self, amount):
        """Deposit money into savings account."""
        if amount > 0:
            self._balance += amount
            txn = Transaction("deposit", amount)
            self.add_transaction(txn)
            print(f"{amount}: deposit success")
        else:
            print("Amount should be positive")

    def withdraw(self, amount):
        """Withdraw money if sufficient balance is available."""
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            txn = Transaction("withdraw", amount)
            self.add_transaction(txn)
            print(f"{amount}: withdraw success")
        else:
            print("Insufficient Funds")

    def apply_interest(self):
        """Apply interest on current balance and record it as a transaction."""
        interest = self._balance * (self.interest_rate / 100)
        self._balance += interest
        txn = Transaction("interest", interest)
        self.add_transaction(txn)

    def show_account_details(self):
        """Return formatted details of savings account."""
        return (f"SavingsAccount | No:{self.account_number} "
                f"| Balance:{self._balance} | Status:{self.status} "
                f"| Interest Rate:{self.interest_rate}%")



class BusinessAccount(Account):
    """Business account with overdraft facility."""
    def __init__(self, account_number, balance, owner):
        super().__init__(account_number, balance, owner)
        self.overdraft_limit = 1000

    def deposit(self, amount):
        """Deposit money into business account."""
        if amount > 0:
            self._balance += amount
            txn = Transaction("deposit", amount)
            self.add_transaction(txn)
            print(f"{amount}: deposit success")
        else:
            print("Amount should be positive")

    def withdraw(self, amount):
        """Withdraw money with overdraft facility."""
        if amount > 0 and amount <= self._balance + self.overdraft_limit:
            self._balance -= amount
            txn = Transaction("withdraw", amount)
            self.add_transaction(txn)
            print(f"{amount}: withdraw success")
        else:
            print("Overdraft limit exceeded")

    def show_account_details(self):
        """Return formatted details of business account."""
        return (f"BusinessAccount | No:{self.account_number} "
                f"| Balance:{self._balance} | Status:{self.status} "
                f"| Overdraft:{self.overdraft_limit}")



class Customer(Person):
    """Represents a customer who can hold multiple accounts."""
    def __init__(self, name, address, phone):
        super().__init__(name, address, phone)
        self._accounts = []

    def add_account(self, account):
        """Add an account to the customer."""
        self._accounts.append(account)
        print("Account added successfully")

    def remove_account(self, account):
        """Remove an account from the customer."""
        if account in self._accounts:
            self._accounts.remove(account)
            print("Account removed successfully")
        else:
            print("Account not found!")

    def get_accounts(self):
        """Return list of accounts held by customer."""

        return self._accounts

    def accounts_summary(self):
        for acc in self._accounts:
            print(acc)



class Admin(Person):
    """Admin details"""
    def __init__(self, name, address, phone, emp_id):
        super().__init__(name, address, phone)
        self.employee_id = emp_id

    def approve_accounts(self, account):
        """aprove and change status of Account"""
        account.status = "active"

    def view_all_customers(self, bank):
        """To view all customer"""
        bank.view_all_customers()



class Transaction:
    """Records all Transactions"""
    def __init__(self, txn_type, amount):

        self.txn_type = txn_type
        self.amount = amount
        self.date = datetime.datetime.now()

    def __str__(self):
        """Returns transcations"""
        return f"{self.date} - {self.txn_type}: {self.amount}"



class Bank:
    """Bank class """
    def __init__(self, name):
        self.name = name
        self.customers = {}

    def create_customer_account(self, customer, account):
    
        for cust_id, cust in self.customers.items():
            if cust.get_details() == customer.get_details():
                cust.add_account(account)
                print(f"Existing customer found. Account added under ID: {cust_id}")
                return cust_id
        
        
        customer_id = randint(10000, 999999)
        self.customers[customer_id] = customer
        customer.add_account(account)
        print(f"New customer created. Customer ID: {customer_id}")
        return customer_id


       

    def delete_customer_account(self, customer_id):
        """Removes all accounts of customer id"""
        if customer_id in self.customers:
            self.customers.pop(customer_id)
            print(f"Customer {customer_id} deleted")

    def view_transaction_history(self, account_number):
        """Returns all Transactions of particular account"""
        for customer in self.customers.values():
            for acc in customer.get_accounts():
                if acc.account_number == account_number:
                    for t in acc.transactions:
                        print(t)

    def view_all_customers(self):
        """"view all customer accounts"""
        for customer_id, customer in self.customers.items():
            print(f"\nCustomer ID: {customer_id}, Details: {customer.get_details()}")
            for acc in customer.get_accounts():
                print("  ", acc)


#menu driven 


if __name__ == "__main__":
    bank = Bank("SBI")
    admin = Admin("Manager", "HQ", "8888888888", "EMP001")
    Employee_id = 1
    customers = {}

    while True:
        print("\n===== BANK MENU =====")
        print("1. Create Customer & Account")
        print("2. Approve Account (Admin only)")
        print("3. View All Customers(Admin Only)")
        print("4. Deposit")
        print("5. Withdraw")
        print("6. View Account Summary")
        print("7. View Transaction History")
        
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            existing = input("Existing customer? (y/n): ").lower()
            if existing == "y":
                cust_id = int(input("Enter customer ID: "))
                if cust_id in customers:
                    cust = customers[cust_id]
                else:
                    print("Invalid customer ID")
                    continue
            else:
                name = input("Enter customer name: ")
                address = input("Enter address: ")
                phone = input("Enter phone: ")
                cust = Customer(name, address, phone)

            acc_type = input("Enter account type (savings/business): ").lower()
            acc_no = int(input("Enter account number: "))

            if acc_type == "savings":
                acc = SavingsAccount(acc_no, 0, cust)
            else:
                acc = BusinessAccount(acc_no, 0, cust)

            
            cust_id = bank.create_customer_account(cust, acc)
            customers[cust_id] = cust
        elif choice == "2":
            e_id =int(input("enter you emp_id:"))
            if e_id == Employee_id:
                cust_id = int(input("Enter customer ID: "))
                acc_no = int(input("Enter account number: "))
                customer = bank.customers.get(cust_id)
                if customer:
                    for acc in customer.get_accounts():
                        if acc.account_number == acc_no:
                            admin.approve_accounts(acc)
                        print("approved")
                        break
                    else:
                        print("Account not found")
                else:
                    print("Customer not found")
            else:
                print("Incorrect emp_id")
                

        elif choice == "3":
            e_id =int(input("enter you emp_id:"))
            if e_id == Employee_id:
                bank.view_all_customers()
            else:
                print("enter valid empid")
                break

        elif choice == "4":
            cust_id = int(input("Enter customer ID: "))
            acc_no = int(input("Enter account number: "))
            amt = float(input("Enter deposit amount: "))
            customer = bank.customers.get(cust_id)
            if customer:
                for acc in customer.get_accounts():
                    if acc.account_number == acc_no:
                        acc.deposit(amt)
                        break
                else:
                    print("Account not found")
            else:
                print("Customer not found")

        elif choice == "5":
            cust_id = int(input("Enter customer ID: "))
            acc_no = int(input("Enter account number: "))
            amt = float(input("Enter withdraw amount: "))
            customer = bank.customers.get(cust_id)
            if customer:
                for acc in customer.get_accounts():
                    if acc.account_number == acc_no:
                        acc.withdraw(amt)
                        break
                else:
                    print("Account not found")
            else:
                print("Customer not found")

        elif choice == "6":
            cust_id = int(input("Enter customer ID: "))
            customer = bank.customers.get(cust_id)
            if customer:
                customer.accounts_summary()
            else:
                print("Customer not found")

        elif choice == "7":
            acc_no = int(input("Enter account number: "))
            bank.view_transaction_history(acc_no)

        

        elif choice == "8":
            print("Hava a great day ,Please visit us again")
            break

        else:
            print("Invalid choice, try again.")