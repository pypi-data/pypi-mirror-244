import uuid
from aerarium.utils import append_to_json, update_config, get_transactions
from tabulate import tabulate
from colorama import Fore, Style
from datetime import datetime


class Accounts:
    def __init__(self, account_name, account_balance):
        self.account_name = account_name
        self.account_balance = account_balance

    def deposit(self, amount, desc, category):
        self.account_balance += amount

        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "amount": amount,
            "desc": desc,
            "category": category,
            "type": "deposit",
        }

        append_to_json(transaction)
        update_config(self.account_balance)

        return self.account_balance

    def withdraw(self, amount, desc, category):
        self.account_balance -= amount

        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "amount": amount,
            "desc": desc,
            "category": category,
            "type": "withdraw",
        }

        append_to_json(transaction)
        update_config(self.account_balance)

        return self.account_balance

    def check_balance(self):
        return self.account_balance

    @staticmethod
    def get_transactions():
        transactions = get_transactions()

        # Format transactions for the table
        table_data = []
        for idx, transaction in enumerate(transactions, start=1):
            if transaction["type"] == "withdraw":
                transaction["amount"] = -transaction["amount"]
            amount = float(transaction["amount"])

            desc = transaction["desc"][:15]
            desc = f"{desc}..." if len(transaction["desc"]) > 15 else desc

            category = transaction["category"]
            formatted_amount = f"{amount:,.2f}"

            # Color the amount based on its sign
            if amount < 0:
                formatted_amount = f"{Fore.RED}{formatted_amount}{Style.RESET_ALL}"
            else:
                formatted_amount = f"{Fore.GREEN}{formatted_amount}{Style.RESET_ALL}"

            table_data.append([idx, formatted_amount, category, desc])

        table_headers = ["N", "Amount", "Category", "Description"]
        table = tabulate(table_data, headers=table_headers, tablefmt="pretty")

        print(table)


if __name__ == "__main__":
    a = Accounts("viraj", 3000)
    print(a.check_balance())
    print(a.withdraw(2000, "salary", "income"))
    print(a.deposit(5000, "salary", "income"))
    print(get_transactions())
    a.get_transactions()
