import click
from datetime import date
from sqlalchemy.orm import sessionmaker
from db.models import User, Transaction, Budget, engine

# Create a new session factory
Session = sessionmaker(bind=engine)

@click.group()
def cli():
    """Personal Finance Tracker CLI"""
    pass

def get_session():
    """Create a new database session."""
    return Session()

@cli.command()
def main_menu():
    """Display the main menu for user interaction."""
    while True:
        click.echo("\n--- My Finance Tracker ---")
        click.echo("Main Menu:")
        click.echo("1. Register")
        click.echo("2. Login")
        click.echo("3. Delete User")
        click.echo("4. Exit")
        choice = click.prompt("Choose an option", type=int)

        if choice == 1:
            register()
        elif choice == 2:
            login()
        elif choice == 3:
            delete_user()
        elif choice == 4:
            click.echo("Exiting the application...")
            break
        else:
            click.echo("Invalid option. Please try again.")

def register():
    """Register a new user interactively."""
    click.echo("\n--- Register ---")
    name = click.prompt("Enter your name")
    email = click.prompt("Enter your email", type=str)

    session = get_session()
    
    # Check if the email is already in use
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        click.echo("This email is already registered. Please use a different email.")
        session.close()
        return

    password = click.prompt("Enter your password", hide_input=True)

    try:
        user = User(name=name, email=email, password=password)  # Store password as plain text
        session.add(user)
        session.commit()
        click.echo("User created successfully!")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

def login():
    """Login an existing user."""
    click.echo("\n--- Login ---")
    email = click.prompt("Enter your email", type=str)
    password = click.prompt("Enter your password", hide_input=True)

    session = get_session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user and user.password == password:  # Compare plain text password
            click.echo("Login successful!")
            user_menu(user.id)
        else:
            click.echo("Login failed: Invalid email or password.")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

def user_menu(user_id):
    """Display the user menu for logged-in users."""
    while True:
        click.echo("\nUser Menu:")
        click.echo("1. Add Transaction")
        click.echo("2. List Transactions")
        click.echo("3. Set Budget")
        click.echo("4. Track Budget")
        click.echo("5. Delete Transaction")
        click.echo("6. Delete Budget")
        click.echo("7. Logout")
        
        choice = click.prompt("Choose an option", type=int)

        if choice == 1:
            add_transaction(user_id)
        elif choice == 2:
            list_transactions(user_id)
        elif choice == 3:
            set_budget(user_id)
        elif choice == 4:
            track_budget(user_id)
        elif choice == 5:
            delete_transaction(user_id)
        elif choice == 6:
            delete_budget(user_id)
        elif choice == 7:
            click.echo("Logging out...")
            break
        else:
            click.echo("Invalid option. Please try again.")

def add_transaction(user_id):
    """Add a new transaction."""
    click.echo("\n--- Add Transaction ---")
    date_str = click.prompt("Enter the transaction date (YYYY-MM-DD)", type=str)
    amount = click.prompt("Enter the amount", type=float)
    category = click.prompt("Enter the category", type=str)

    session = get_session()
    try:
        transaction = Transaction(user_id=user_id, date=date.fromisoformat(date_str), amount=amount, category=category)
        session.add(transaction)
        session.commit()
        click.echo(f"Transaction added: {date_str}, {amount}, {category}")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

def list_transactions(user_id):
    """List all transactions for the user."""
    click.echo("\n--- List Transactions ---")
    session = get_session()
    transactions = session.query(Transaction).filter_by(user_id=user_id).all()

    if transactions:
        for transaction in transactions:
            click.echo(f"ID: {transaction.id}, Date: {transaction.date}, Amount: {transaction.amount}, Category: {transaction.category}")
    else:
        click.echo("No transactions found.")

    session.close()

def set_budget(user_id):
    """Set a budget for a specific category."""
    click.echo("\n--- Set Budget ---")
    category = click.prompt("Enter the budget category", type=str)
    limit = click.prompt("Enter your budget amount", type=float)

    session = get_session()
    
    try:
        # Check if a budget for this category already exists
        existing_budget = session.query(Budget).filter_by(user_id=user_id, category=category).first()
        if existing_budget:
            existing_budget.limit = limit  # Update the existing budget limit
            click.echo(f"Budget for '{category}' updated to {limit}.")
        else:
            budget = Budget(user_id=user_id, category=category, limit=limit)
            session.add(budget)
            click.echo(f"Budget for '{category}' set to {limit}.")
        
        session.commit()
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

def delete_transaction(user_id):
    """Delete a specific transaction."""
    click.echo("\n--- Delete Transaction ---")
    transaction_id = click.prompt("Enter the ID of the transaction to delete", type=int)

    session = get_session()
    
    try:
        transaction = session.query(Transaction).filter_by(id=transaction_id, user_id=user_id).first()
        if transaction:
            session.delete(transaction)
            session.commit()
            click.echo("Transaction deleted successfully!")
        else:
            click.echo("Transaction not found.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

def delete_budget(user_id):
    """Delete a specific budget."""
    click.echo("\n--- Delete Budget ---")
    category = click.prompt("Enter the category of the budget to delete", type=str)

    session = get_session()
    
    try:
        budget = session.query(Budget).filter_by(user_id=user_id, category=category).first()
        if budget:
            session.delete(budget)
            session.commit()
            click.echo("Budget deleted successfully!")
        else:
            click.echo("Budget not found.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

def track_budget(user_id):
    """Track the budget for each category and warn if the budget is exceeded."""
    click.echo("\n--- Track Budget ---")
    session = get_session()
    
    budgets = session.query(Budget).filter_by(user_id=user_id).all()
    transactions = session.query(Transaction).filter_by(user_id=user_id).all()

    budget_summary = {budget.category: budget.limit for budget in budgets}
    transaction_summary = {category: 0 for category in budget_summary.keys()}

    # Summarize transactions by category
    for transaction in transactions:
        if transaction.category in transaction_summary:
            transaction_summary[transaction.category] += transaction.amount

    # Display the budget tracking results
    for category, limit in budget_summary.items():
        spent = transaction_summary.get(category, 0)
        remaining = limit - spent
        click.echo(f"Category: {category}, Budget Limit: {limit}, Spent: {spent}, Remaining: {remaining}")

        if spent > limit:
            click.echo(click.style(f"Warning: You have exceeded the budget for '{category}' by {spent - limit}!", fg='red'))

    session.close()

def delete_user():
    """Delete a user interactively."""
    click.echo("\n--- Delete User ---")
    email = click.prompt("Enter the email of the user to delete", type=str)

    session = get_session()
    
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            session.delete(user)
            session.commit()
            click.echo("User deleted successfully!")
        else:
            click.echo("User not found.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    main_menu()
