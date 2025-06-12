import csv
from datetime import datetime

def load_transactions(filename='financial_transactions.csv'):
    """Load transactions from a CSV file into a list of dictionaries."""
    transactions = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            datetime.strptime(row['date'], '%Y-%m-%d')
            amount = float(row['amount'])
            if row['type'].lower() == 'debit':
                row['amount'] = str(amount * -1)
            print(row)
    return transactions


def add_transaction(transactions):
    """Add a new transaction from user input."""
    try:
        # Prompt for date
        date_str = input("Enter transaction date (YYYY-MM-DD): ")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Prompt for customer_id
        customer_id = input("Enter customer ID: ").strip()

        # Prompt for amount
        amount_str = input("Enter transaction amount: ")
        amount = float(amount_str)
        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        # Prompt for transaction type
        trans_type = input("Enter transaction type (credit/debit): ").lower()
        if trans_type not in {"credit", "debit"}:
            print("Invalid transaction type. Must be 'credit' or 'debit'.")
            return

        # Prompt for description
        description = input("Enter transaction description: ").strip()

        # Generate new transaction_id
        transaction_id = len(transactions) + 1  # Simple auto-increment

        # Create transaction dictionary
        transaction = {
            "transaction_id": transaction_id,
            "date": str(date),
            "customer_id": customer_id,
            "amount": amount,
            "type": trans_type,
            "description": description
        }

        # Append to transactions
        transactions.append(transaction)
        print("Transaction added successfully!")

    except ValueError as ve:
        print(f"Invalid input: {ve}")


def view_transactions(transactions):
    """Display transactions in a table format."""
    if not transactions:
        print("No transactions to display.")
        return

    # Define headers
    headers = ["ID", "Date", "Customer ID", "Amount", "Type", "Description"]
    
    # Print header
    print("-" * 80)
    print(f"{headers[0]:<5} {headers[1]:<12} {headers[2]:<15} {headers[3]:>10} {headers[4]:<10} {headers[5]}")
    print("-" * 80)

    # Print each transaction
    for txn in transactions:
        print(f"{txn['transaction_id']:<5} {txn['date']:<12} {txn['customer_id']:<15} "
              f"{float(txn['amount']):>10.2f} {txn['type']:<10} {txn['description']}")

    print("-" * 80)

def update_transactions(transactions):
    """Update a transaction’s details."""
    if not transactions:
        print("No transactions to update.")
        return

    # Show transactions with index numbers
    print("\nExisting Transactions:")
    for i, txn in enumerate(transactions):
        print(f"{i+1}. ID: {txn['transaction_id']}, Date: {txn['date']}, "
              f"Customer ID: {txn['customer_id']}, Amount: {txn['amount']}, "
              f"Type: {txn['type']}, Description: {txn['description']}")

    try:
        choice = int(input("\nEnter the number of the transaction you want to update: "))
        if not (1 <= choice <= len(transactions)):
            print("Invalid choice.")
            return

        txn = transactions[choice - 1]

        print("\nWhich field would you like to update?")
        fields = ["date", "customer_id", "amount", "type", "description"]
        for i, field in enumerate(fields):
            print(f"{i+1}. {field}")

        field_choice = int(input("Enter the number of the field: "))
        if not (1 <= field_choice <= len(fields)):
            print("Invalid field choice.")
            return

        field_name = fields[field_choice - 1]
        new_value = input(f"Enter new value for '{field_name}': ")

        # Optional: validate field types
        if field_name == "amount":
            new_value = float(new_value)
        elif field_name == "type":
            if new_value.lower() not in {"credit", "debit"}:
                print("Invalid transaction type.")
                return
            new_value = new_value.lower()
        elif field_name == "date":
            try:
                datetime.strptime(new_value, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                return

        txn[field_name] = new_value
        print("Transaction updated successfully!")

    except ValueError as e:
        print(f"Invalid input: {e}")

def delete_transaction(transactions):
    """Delete a transaction from the list."""
    if not transactions:
        print("No transactions to delete.")
        return

    # Show transactions with index numbers
    print("\nExisting Transactions:")
    for i, txn in enumerate(transactions):
        print(f"{i+1}. ID: {txn['transaction_id']}, Date: {txn['date']}, "
              f"Customer ID: {txn['customer_id']}, Amount: {txn['amount']}, "
              f"Type: {txn['type']}, Description: {txn['description']}")

    try:
        choice = int(input("\nEnter the number of the transaction to delete: "))
        if not (1 <= choice <= len(transactions)):
            print("Invalid selection.")
            return

        txn = transactions[choice - 1]
        confirm = input(f"Are you sure you want to delete transaction ID {txn['transaction_id']}? (yes/no): ").lower()
        if confirm == "yes":
            transactions.pop(choice - 1)
            print("Transaction deleted successfully.")
        else:
            print("Deletion cancelled.")

    except ValueError as e:
        print(f"Invalid input: {e}")

def analyze_finances(transactions):
    """Calculate and display financial summaries."""
    if not transactions:
        print("No transactions to analyze.")
        return

    totals_by_type = {
        "credit": 0.0,
        "debit": 0.0,
        "transfer": 0.0  # in case "transfer" exists in the data
    }

    for txn in transactions:
        txn_type = txn['type'].lower()
        amount = float(txn['amount'])

        if txn_type in totals_by_type:
            totals_by_type[txn_type] += amount
        else:
            print(f"Warning: Unknown transaction type '{txn_type}' encountered.")

    # Net balance: credits - debits
    net_balance = totals_by_type["credit"] - totals_by_type["debit"]

    # Print financial summary
    print("\nFinancial Summary:")
    print(f"Total Credits:  ${totals_by_type['credit']:,.2f}")
    print(f"Total Debits:   ${totals_by_type['debit']:,.2f}")
    print(f"Total Transfers:${totals_by_type['transfer']:,.2f}")
    print(f"Net Balance:    ${net_balance:,.2f}")

    # Print by type
    print("\nBy Type:")
    for t_type, total in totals_by_type.items():
        print(f"  {t_type.capitalize()}: ${total:,.2f}")

    """Calculate and display financial summaries."""
    if not transactions:
        print("No transactions to analyze.")
        return

    total_credits = 0.0
    total_debits = 0.0
    customer_summary = {}

    for txn in transactions:
        amount = float(txn['amount'])
        customer_id = txn['customer_id']
        txn_type = txn['type'].lower()

        if txn_type == "credit":
            total_credits += amount
        elif txn_type == "debit":
            total_debits += amount

        # Per-customer breakdown
        if customer_id not in customer_summary:
            customer_summary[customer_id] = 0.0
        customer_summary[customer_id] += amount if txn_type == "credit" else -amount

    net_balance = total_credits - total_debits

    print("\n=== Financial Summary ===")
    print(f"Total Credits: ${total_credits:,.2f}")
    print(f"Total Debits:  ${total_debits:,.2f}")
    print(f"Net Balance:   ${net_balance:,.2f}")

    print("\n=== Balance by Customer ID ===")
    for cust_id, balance in customer_summary.items():
        print(f"Customer {cust_id}: ${balance:,.2f}")

def save_transactions(transactions, filename='financial_transactions.csv'):
    """Save transactions to a CSV file."""
    if not transactions:
        print("No transactions to save.")
        return

    # Get the field names from the first transaction
    fieldnames = ['transaction_id', 'date', 'customer_id', 'amount', 'type', 'description']

    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row
            for txn in transactions:
                writer.writerow(txn)
        print(f"Transactions saved to '{filename}' successfully.")

    except IOError as e:
        print(f"Error saving transactions: {e}")

def generate_report(transactions, filename='report.txt'):
    """Generate a text report of financial summaries."""
    if not transactions:
        print("No transactions to report.")
        return

    # Calculate totals
    totals_by_type = {
        "credit": 0.0,
        "debit": 0.0,
        "transfer": 0.0
    }

    for txn in transactions:
        txn_type = txn['type'].lower()
        amount = float(txn['amount'])

        if txn_type in totals_by_type:
            totals_by_type[txn_type] += amount

    net_balance = totals_by_type["credit"] - totals_by_type["debit"]

    # Build report content
    report_lines = [
        "Financial Summary Report",
        "========================",
        f"Total Credits:   ${totals_by_type['credit']:,.2f}",
        f"Total Debits:    ${totals_by_type['debit']:,.2f}",
        f"Total Transfers: ${totals_by_type['transfer']:,.2f}",
        f"Net Balance:     ${net_balance:,.2f}",
        "",
        "By Type:",
    ]

    for t_type, total in totals_by_type.items():
        report_lines.append(f"  {t_type.capitalize()}: ${total:,.2f}")

    # Write to file
    try:
        with open(filename, 'w') as file:
            for line in report_lines:
                file.write(line + "\n")
        print(f"Report generated and saved to '{filename}'")
    except IOError as e:
        print(f"Error writing report: {e}")


    transactions = []
    while True:
        print("\nSmart Personal Finance Analyzer")
        print("1. Load Transactions")
        print("2. Add Transaction")
        print("3. View Transactions")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Analyze Finances")
        print("7. Save Transactions")
        print("8. Generate Report")
        print("9. Exit")
        choice = input("Select an option: ")
        # Call functions based on choice
        if choice == '9':
            break

def main():
    transactions = []
    while True:
        print("\nSmart Personal Finance Analyzer")
        print("1. Load Transactions")
        print("2. Add Transaction")
        print("3. View Transactions")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Analyze Finances")
        print("7. Save Transactions")
        print("8. Generate Report")
        print("9. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            transactions = load_transactions()
        elif choice == '2':
            add_transaction(transactions)
        elif choice == '3':
            view_transactions(transactions)
        elif choice == '4':
            update_transaction(transactions)
        elif choice == '5':
            delete_transaction(transactions)
        elif choice == '6':
            analyze_finances(transactions)
        elif choice == '7':
            save_transactions(transactions)
        elif choice == '8':
            generate_report(transactions)
        elif choice == '9':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please select a number between 1 and 9.")


if __name__ == "__main__":
    main() 