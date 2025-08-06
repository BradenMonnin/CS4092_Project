# Library Management System

This is a command-line Library Management System built with Python and SQLite. It allows you to manage books, members, staff, and book loans for a library.

## Features

- **Book Management:** Add, update, remove, view, and search books.
- **Member Management:** Register, update, remove, view, and search library members.
- **Staff Management:** Add, update, remove, view, and search staff (restricted to managers/head librarians).
- **Loan Management:** Borrow, renew, return books, and view active/overdue loans.

## Database

The database schema and sample data are defined in [`database_creation.sql`](database_creation.sql). The main database file is `library_management.db`.

## Usage

1. **Setup the Database:**
   - Run the SQL script to create the database and tables:
     ```sh
     sqlite3 library_management.db < database_creation.sql
     ```

2. **Run the Application:**
   - Start the system with:
     ```sh
     python library_management.py
     ```

3. **Follow the Menu:**
   - Use the interactive menu to manage books, members, staff, and loans.

## File Structure

- [`library_management.py`](library_management.py): Main application code.
- [`database_creation.sql`](database_creation.sql): SQL script to create and populate the database.
- `library_management.db`: SQLite database file (generated after running the SQL script).

## Requirements

- Python 3.x
- SQLite3

## Notes

- Staff management is restricted to users with the "Manager" or "Head Librarian" role.
- Members can borrow up to 5 books at a time.
- All actions are performed via the command-line interface.