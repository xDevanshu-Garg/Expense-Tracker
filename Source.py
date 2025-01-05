import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# File path for storing expenses
EXPENSES_FILE = "expenses.txt"

# Ensure the file exists
def initialize_file():
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'w') as file:
            pass
    else:
        # Remove empty lines from the file
        with open(EXPENSES_FILE, 'r') as file:
            lines = file.readlines()
        with open(EXPENSES_FILE, 'w') as file:
            for line in lines:
                if line.strip():  # Write non-empty lines back to the file
                    file.write(line)

# Add an expense to the file
def add_expense():
    while True:
        category = input(Fore.LIGHTGREEN_EX + "Enter category (e.g., Food, Travel): ").strip()
        amount = input(Fore.LIGHTGREEN_EX + "Enter amount: ").strip()
        date = input(Fore.LIGHTGREEN_EX + "Enter date (DD-MM-YYYY): ").strip()

        try:
            amount = float(amount)
            datetime.strptime(date, "%d-%m-%Y")  # Validate date format
            break
        except ValueError:
            print(Fore.RED + "Invalid amount or date format. Please try again.")

    with open(EXPENSES_FILE, 'a') as file:
        file.write(f"{category},{amount},{date}\n")
    print(Fore.GREEN + "Expense added successfully!")

# View expenses grouped by category
def view_expenses():
    if not os.path.getsize(EXPENSES_FILE):
        print(Fore.RED + "No expenses recorded yet.")
        return

    expenses_by_category = {}
    with open(EXPENSES_FILE, 'r') as file:
        for line in file:
            category, amount, date = line.strip().split(",")
            if category not in expenses_by_category:
                expenses_by_category[category] = []
            expenses_by_category[category].append((amount, date))

    for category, expenses in expenses_by_category.items():
        print(Fore.CYAN + f"{category}:")
        if not expenses:
            print(Fore.MAGENTA + "  No expenses recorded.")
        for i, (amount, date) in enumerate(expenses):
            print(Fore.LIGHTBLUE_EX + f"  {i+1}. Amount: {amount} - Date: {date}")

# Show a monthly summary of expenses
def monthly_summary():
    while True:
        month_year = input(Fore.MAGENTA + "Enter month and year (MM-YYYY): ").strip()
        try:
            datetime.strptime(month_year, "%m-%Y")  # Validate format
            break
        except ValueError:
            print(Fore.RED + "Invalid month and year format. Please try again.")

    total_expenses = 0
    expenses_by_category = {}

    with open(EXPENSES_FILE, 'r') as file:
        for line in file:
            category, amount, date = line.strip().split(",")
            expense_date = datetime.strptime(date, "%d-%m-%Y")
            if expense_date.strftime("%m-%Y") == month_year:
                total_expenses += float(amount)
                if category not in expenses_by_category:
                    expenses_by_category[category] = 0
                expenses_by_category[category] += float(amount)

    print(Fore.CYAN + f"Monthly Summary ({month_year}):")
    print(Fore.GREEN + f"Total Expenses: {total_expenses}")
    print(Fore.CYAN + "By Category:")
    for category, total in expenses_by_category.items():
        print(Fore.LIGHTBLUE_EX + f"  {category}: {total}")

# Delete an expense
def delete_expense():
    if not os.path.getsize(EXPENSES_FILE):
        print(Fore.RED + "No expenses recorded yet.")
        return

    print(Fore.CYAN + "Expenses:")
    with open(EXPENSES_FILE, 'r') as file:
        for i, line in enumerate(file):
            category, amount, date = line.strip().split(",")
            print(Fore.LIGHTBLUE_EX + f"{i+1}. Category: {category} - Amount: {amount} - Date: {date}")

    while True:
        try:
            choice = int(input(Fore.MAGENTA + "Enter the number of the expense to delete: "))
            if choice < 1:
                print(Fore.RED + "Invalid choice. Please try again.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Invalid choice. Please try again.")

    with open(EXPENSES_FILE, 'r') as file:
        lines = file.readlines()

    if choice > len(lines):
        print(Fore.RED + "Invalid choice. Please try again.")
        return

    with open(EXPENSES_FILE, 'w') as file:
        for i, line in enumerate(lines):
            if i != choice - 1:
                file.write(line)

    print(Fore.GREEN + "Expense deleted successfully!")

# Main menu loop
def main_menu():
    initialize_file()
    while True:
        print(Fore.CYAN + "\nWelcome to Personal Expense Tracker!\n")
        print(Fore.MAGENTA + "1. Add Expense")
        print(Fore.MAGENTA + "2. View Expenses")
        print(Fore.MAGENTA + "3. Monthly Summary")
        print(Fore.MAGENTA + "4. Delete Expense")
        print(Fore.MAGENTA + "5. Exit")
        print()
        choice = input(Fore.MAGENTA + "Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            print(Fore.GREEN + "Goodbye! Spend Wisely")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

main_menu()
