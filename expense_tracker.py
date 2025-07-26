#Importing necessary libraries
import sqlite3
import os
#fuction to clear the console screen
def clear_screen():
    #Clear the console screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')
#Function to pause the program and wait for user input
def pause():
    input("\nPress Enter to continue...")
#Function to create a connection to the SQLite database
def create_connection():
    #Create a database connection to the SQLite database.
    conn = None
    try:
        conn = sqlite3.connect('my_expense_tracker.db')
        print("Connection established to the database.")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn
#Users Table Functions
#Function to create the users table in the database
def create_user_table(conn):
    try:
        #Connecting to the database
        cursor = conn.cursor()
        #Creating Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE       
            )
        ''')
    except sqlite3.Error as e:
        print(f"Error creating the users table: {e}")

#Function to add a new user to the database
def add_user(conn, username, name, email):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, name, email)
            VALUES (?, ?, ?)
        ''', (username, name, email))
        conn.commit()
        print(f"User {username} added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding user {username}: {e}")

#Function to check if a user exists by user id
def user_exists(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 FROM users WHERE id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"User id:{user_id} does not exist {e}")
        return False
#Function to get all the users from the database
def get_all_users(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users
        ''')
        users = cursor.fetchall()
        return users
    except sqlite3.Error as e:
        print(f"Error retrieving users: {e}")
        return []
#Function to delete a user by user id
def delete_user(conn, user_id):  
    try:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM users WHERE id = ?
        ''', (user_id,))
        conn.commit()
        print(f"User with ID {user_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting user with ID {user_id}: {e}")
#Function to update a user by user id
def update_user(conn, user_id, username, name, email):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET username = ?, name = ?, email = ?
            WHERE id = ?
        ''', (username, name, email, user_id))
        conn.commit()
        print(f"User with ID {user_id} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating user with ID {user_id}: {e}")                
#Expenses Table Functions
#Function to create the expenses table in the database
def create_expenses_table(conn):
    try:
        #Connecting to the database
        cursor = conn.cursor()
        #Creating Expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)       
            )
        ''')
    except sqlite3.Error as e:
        print(f"Error creating the expenses table: {e}")       
#Function to insert a new expense into the database
def add_expense(conn, user_id, category, amount, description, date):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (user_id, category, amount, description, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, category, amount, description, date))
        conn.commit()
        print(f"Expense added successfully for user ID {user_id}.")
    except sqlite3.Error as e:
        print(f"Error adding expense for user ID {user_id}: {e}")
#Function to delete an expense by its ID
def delete_expense(conn, expense_id):   
    try:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM expenses WHERE id = ?
        ''', (expense_id,))
        conn.commit()
        print(f"Expense with ID {expense_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting expense with ID {expense_id}: {e}")
#Function to update an expense by its ID
def update_expense(conn, expense_id, user_id, category, amount, description, date):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE expenses
            SET user_id = ?, category = ?, amount = ?, description = ?, date = ?
            WHERE id = ?
        ''', (user_id, category, amount, description, date, expense_id))
        conn.commit()
        print(f"Expense with ID {expense_id} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating expense with ID {expense_id}: {e}") 
#Function to check if an expense exists by its ID
def expense_exists(conn, expense_id):   
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 FROM expenses WHERE id = ?
        ''', (expense_id,))
        result = cursor.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"Expense ID {expense_id} does not exist: {e}")
        return False               
#Function to get expenses by user ID with Join Operation showing the user's name
def get_expenses_by_user(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT expenses.id,
                   expenses.user_id,    
                   users.name AS name,
                   expenses.category,
                   expenses.amount,
                   expenses.date
            From expenses
            JOIN users ON expenses.user_id = users.id
            WHERE expenses.user_id = ?
            ORDER BY expenses.date DESC          
            ''', (user_id,))
        expenses = cursor.fetchall()
        return expenses
    except sqlite3.Error as e:
        print(f"Error retrieving expenses for user {user_id}: {e}")
        return [] 
#function to get all expenses from the database
def get_all_expenses(conn): 
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT expenses.id,
                   expenses.user_id,    
                   users.name AS name,
                   expenses.category,
                   expenses.amount,
                   expenses.date
            FROM expenses
            JOIN users ON expenses.user_id = users.id
            ORDER BY expenses.date DESC          
        ''')
        expenses = cursor.fetchall()
        return expenses
    except sqlite3.Error as e:
        print(f"Error retrieving all expenses: {e}")
        return []           
def main():
    print("Welcome to the Expense Tracker!")
    #Establishing a connection to the database
    conn=create_connection()
    #Creating the tables if they do not exist
    create_user_table(conn)
    create_expenses_table(conn)
    #Enabling foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    while True:
        #Clearing the console screen for better readability
        clear_screen()
        #Displaying the menu options
        print("Please Choose an option from the Menu: ")
        print("1. Add User")
        print("2. Update User")
        print("3. Delete User")
        print("4. View All Users")
        print("5. Add Expense")
        print("6. Update Expense")
        print("7. Delete Expense")
        print("8. Check all Expenses Sorted by Date")
        print("9. View Expenses by User Sorted by Date")
        print("10. Exit")
        choice = input("Enter your choice: ")
        #Add User Option. Askes for username, name, and email
        if(choice == '1'):
            try:
                username = input("Enter username: ")
                name = input("Enter name: ")
                email = input("Enter email: ")
                add_user(conn, username, name, email)
                pause()  # Pause after adding a user
            except sqlite3.Error as e:
                print(f"Error adding user: {e}")
                continue       
        #Update User Option. Asks for user ID, username, name, and email
        elif(choice == '2'):    
            try:
                user_id = int(input("Enter user ID to update: "))
                if not user_exists(conn, user_id):
                    print(f"User ID {user_id} does not exist. Please add the user first.")
                    pause()  # Pause after invalid user ID
                    continue
                username = input("Enter new username: ")
                name = input("Enter new name: ")
                email = input("Enter new email: ")
                update_user(conn, user_id, username, name, email)
                pause()  # Pause after updating a user
            except ValueError as e:
                print(f"Invalid input: {e}. Please make sure to enter numbers in user_id.")
                continue
            except sqlite3.Error as e:
                print(f"Error updating user: {e}")
                continue
        #Delete User Option. Asks for user ID and deletes the user
        elif(choice == '3'):
            try:
                user_id = int(input("Enter user ID to delete: "))
                if not user_exists(conn, user_id):
                    print(f"User ID {user_id} does not exist. Please add the user first.")
                    pause()  # Pause after invalid user ID
                    continue
                delete_user(conn, user_id)
                pause()  # Pause after deleting a user
            except ValueError as e:
                print(f"Invalid input: {e}. Please make sure to enter numbers in user_id.")
                continue
            except sqlite3.Error as e:
                print(f"Error deleting user: {e}")
                continue        
        #Check Existing Users Option. Displays all users in the database
        elif(choice == '4'):
            try:
                users = get_all_users(conn)
                if users:
                    print("Existing Users:")
                    for user in users:
                        print(f"ID: {user[0]}, Username: {user[1]}, Name: {user[2]}, Email: {user[3]}")
                else:
                    print("No users found in the database.")
                    pause() # Pause to show no users found
                pause()  # Pause after checking existing users    
            except sqlite3.Error as e:
                print(f"Error retrieving users: {e}")
                continue
        #Add Expense Option. Asks for user ID, category, amount, description, and date
        elif(choice == '5'):
            #Asking for user ID and checking if it exists
            try:
                user_id = int(input("Enter user ID: "))
                if not user_exists(conn, user_id):
                    print(f"User ID {user_id} does not exist. Please add the user first.")
                    pause()  # Pause after invalid user ID
                    continue
                category = input("Enter expense category: ")
                amount = round(float(input("Enter expense amount: ")), 2) #Rounding to 2 decimal places
                description = input("Enter expense description: ")
                date = input("Enter expense date (YYYY-MM-DD): ")
                add_expense(conn, user_id, category, amount, description, date)
                pause()  # Pause after adding an expense
            except ValueError as e:
                print(f"Invalid input: {e}. Please make sure to enter numbers in user_id and amount.")
                continue
            except sqlite3.Error as e:
                print(f"Error adding expense: {e}")
                continue 
        #Update Expense Option. Asks for expense ID, user ID, category, amount, description, and date
        elif(choice == '6'):
            #Asking for expense ID and checking if it exists
            try:
                expense_id = int(input("Enter expense ID to update: "))
                if not expense_exists(conn, expense_id):
                    print(f"Expense ID {expense_id} does not exist. Please add the expense first.")
                    pause()  # Pause after invalid expense ID
                    continue
                user_id = int(input("Enter user ID: "))
                if not user_exists(conn, user_id):
                    print(f"User ID {user_id} does not exist. Please add the user first.")
                    pause()  # Pause after invalid user ID
                    continue
                category = input("Enter new expense category: ")
                amount = round(float(input("Enter new expense amount: ")), 2) #Rounding to 2 decimal places
                description = input("Enter new expense description: ")
                date = input("Enter new expense date (YYYY-MM-DD): ")
                update_expense(conn, expense_id, user_id, category, amount, description, date)
                pause()  # Pause after updating an expense
            except ValueError as e:
                print(f"Invalid input: {e}. Please make sure to enter numbers in expense_id and amount.")
                continue
            except sqlite3.Error as e:
                print(f"Error updating expense: {e}")
                continue
        #Delete Expense Option. Asks for expense ID and deletes the expense
        elif(choice == '7'):
            #Asking for expense ID and checking if it exists
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                if not expense_exists(conn, expense_id):
                    print(f"Expense ID {expense_id} does not exist. Please add the expense first.")
                    pause()  # Pause after invalid expense ID
                    continue
                delete_expense(conn, expense_id)
                pause()  # Pause after deleting an expense
            except ValueError as e:
                print(f"Invalid input: {e}. Please make sure to enter numbers in expense_id.")
                continue
            except sqlite3.Error as e:
                print(f"Error deleting expense: {e}")
                continue
        #Check All Expenses Option. Displays all expenses in the database
        elif(choice == '8'):
            try:
                expenses = get_all_expenses(conn)
                if expenses:
                    print("All Expenses:")
                    for expense in expenses:
                        print(f"ID: {expense[0]}, User ID: {expense[1]}, Name: {expense[2]}, Category: {expense[3]}, Amount: ${expense[4]}, Date: {expense[5]}")
                else:
                    print("No expenses found in the database.")
                    pause()  # Pause to show no expenses found
                pause()  # Pause after checking all expenses
            except sqlite3.Error as e:
                print(f"Error retrieving expenses: {e}")
                continue                
        #View Expenses by User Option. Asks for user ID and displays all expenses for that user    
        elif(choice == '9'):
            #Asking for user ID and checking if it exists
            try:
                user_id = input("Enter user ID to view expenses: ")
                if not user_exists(conn, user_id):
                    print(f"User ID {user_id} does not exist. Please add the user first.")
                    pause()  # Pause after invalid user ID
                    continue
                expenses = get_expenses_by_user(conn, user_id)
                if expenses:
                    print("Expenses for User ID", user_id)
                    for expense in expenses:
                        print(f"ID: {expense[0]}, User ID: {expense[1]}, Name: {expense[2]}, Category: {expense[3]}, Amount: ${expense[4]}, Date: {expense[5]}")
                else:
                    print(f"No expenses found for User ID {user_id}.")
                    pause()  # Pause if no expenses found
                pause()  # Pause after viewing expenses        
            except ValueError as e:
                print(f"Invalid input: {e}. Please make sure to enter a valid user ID.")
                continue
            except sqlite3.Error as e:
                print(f"Error retrieving expenses: {e}")
                continue    
        #Exit Option. Exits the program        
        elif(choice == '10'):
            print("Exiting the Expense Tracker. Goodbye!")
            conn.close()
            break
        #Invalid Option. If the user enters an invalid option, it prompts them to try again
        else:
            print("Invalid choice. Please try again.")
            pause()  # Pause after invalid choice                
#Running the main function to start the program
if __name__ == "__main__":
    main()            