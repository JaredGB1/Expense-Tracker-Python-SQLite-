# Overview

This project is a command-line Expense Tracker application written in Python with a SQLite Relational Database. Users can add, update, delete, and check their expenses by creating users and expenses to track their spending across different dates.

The purpose of creating this program was to demonstrate proficiency in working with SQLite relational databases using Python and to learn more about applying this to real-world cases.

To use the program, you can run the Python file in a terminal. From the menu, you can:
-Add New Users
-Update Users
-Delete Users
-View All Users
-Add Expenses
-Update Expenses
-Delete Expenses
-View All Expenses
-View Expenses by User, Sorted by Date

{Provide a link to your YouTube demonstration. It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of how created the Relational Database.}

[Software Demo Video](https://www.youtube.com/watch?v=F7UNjhzV9FY)

# Relational Database

The program uses SQLite, a lightweight relational database engine stored in a local .db file. The Python Program will create a database including the users and expenses tables the first time it is executed.

Database Tables:

- users

  - id (Primary Key)

  - username (Unique)

  - name

  - email (Unique)

- expenses

  - id (Primary Key)

  - user_id (Foreign Key → users.id)

  - category

  - amount

  - description

  - date

The expenses table uses a foreign key constraint to ensure each expense is linked to a valid user.

# Development Environment

To develop the software, I used Visual Studio Code, The Python Programing language and the libraries os for console screen clearing, and sqlite3 for database connectivity.

# Useful Websites

- [Medium Blog](https://medium.com/@nutanbhogendrasharma/sqlite-relational-database-management-with-python-7d9ca4fc2ae7)
- [SQLite](https://www.sqlite.org/docs.html)

# Future Work

- Add input validation to prevent future or invalid dates
- Create a GUI or a web interface for the program
- Add a category table to keep track of specific categories
- Add an option to export expenses to a file
- Add an option to provide spending summaries by date
