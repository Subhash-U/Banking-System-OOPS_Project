#test
if __name__ == "__main__":
    bank = Bank("OOPS")
    cust1 = Customer("Ravi", "Delhi", "9999999999")

    savings = SavingsAccount(101, 0, cust1)
    business = BusinessAccount(102, 0, cust1)

    bank.create_customer_account(cust1, savings)
    bank.create_customer_account(cust1, business)

    admin = Admin("Manager", "HQ", "8888888888", "EMP001")
    admin.approve_accounts(savings)
    admin.approve_accounts(business)

    savings.deposit(5000)
    business.deposit(10000)
    savings.withdraw(2000)
    business.withdraw(12000)   # within overdraft
    business.withdraw(50000)   # exceeds overdraft
    savings.apply_interest()

    print("\n--- Account Summaries ---")
    cust1.accounts_summary()

    print("\n--- Transaction History (Savings 101) ---")
    bank.view_transaction_history(101)

    print("\n--- Transaction History (Business 102) ---")
    bank.view_transaction_history(102)

    print("\n--- All Customers in Bank ---")
    bank.view_all_customers()
