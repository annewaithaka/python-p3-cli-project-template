### My Finance Tracker

### Overview
My Finance Tracker is a personal finance management application that allows users to track their expenses, set budgets for different categories, and manage their financial transactions easily through a command-line interface (CLI).

### Features
-User Registration: Users can create an account with their name, email, and password.
-User Login: Existing users can log in to their accounts.

-Transaction Management: Users can:
Add transactions with date, amount, and category.
List all their transactions.
Delete specific transactions.

-Budget Management: Users can:
Set budgets for different categories.
Delete budgets.
Track their spending against their budgets with warnings for overspending.

### Requirements
Python 
SQLAlchemy
SQLite

### Installation
Clone the repository
Install dependencies

### Usage
Run the application: python3 cli.py
Follow the on-screen instructions to register, log in, and manage your transactions and budgets.

### Commands
-Register: Create a new user account.
-Login: Log in to your existing account.
-Add Transaction: Record a new transaction.
-List Transactions: Display all recorded transactions.
-Set Budget: Define a budget limit for a specific category.
-Track Budget: View budget limits, spending, and warnings for overspending.
-Delete Transaction: Remove a specific transaction by its ID.
-Delete Budget: Remove a specific budget by category.
-Delete User: Permanently delete your user account.
-Exit: Exit the application.

### Database Structure
* Users Table
id: Primary key
name: User's name
email: User's email (unique)
password: User's password (stored as plain text)

* Transactions Table
id: Primary key
user_id: Foreign key referencing Users
date: Date of the transaction
amount: Amount spent
category: Category of the transaction

* Budgets Table
id: Primary key
user_id: Foreign key referencing Users
category: Budget category
limit: Budget limit for the category

### Contributing
Contributions are welcome! If you would like to contribute to the project, please fork the repository and submit a pull request.

