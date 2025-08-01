import sqlite3

class LibraryDatabase:
    def __init__(self, db_path="library_database.db"):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to the database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            print("Connected to the database successfully.")
            self.conn.row_factory = sqlite3.Row
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return False
        
    def disconnect(self):
        """Disconnect from the database"""
        if self.conn:
            self.conn.close()
            print("Disconnected from the database.")
    
    def execute_query(self, query, params=()):
        """Execute a query and return the result"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        
    def execute_update(self, query, params=()):
        """Execute an update query (INSERT, UPDATE, DELETE)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error executing update: {e}")
            self.conn.rollback()
            return None
        
class LibraryManagementSystem:
    def __init__(self, db_path="library_management.db"):
        self.db = LibraryDatabase(db_path)
        if not self.db.connect():
            raise Exception("Failed to connect to the database.")
    
    def display_menu(self):
        """Display the main menu"""
        print("\nLibrary Management System")
        print("1. Loan Management")
        print("2. Book Management")
        print("3. Member Management")
        print("4. Staff Management")
        print("0. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.loan_management_menu()
        elif choice == "2":
            self.book_management_menu()
        elif choice == "3":
            self.member_management_menu()
        elif choice == "4":
            self.staff_management_menu()
        elif choice == "0":
            print("Exiting...")
        else:
            print("Invalid choice.")

    def loan_management_menu(self):
        """Display the loan management menu"""
        print("\nLoan Management")
        print("1. Borrow Book")
        print("2. Renew Book")
        print("3. Return Book")
        print("4. View Overdue Loans")
        print("5. View Active Loans")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.borrow_book()
        elif choice == "2":
            self.renew_book()
        elif choice == "3":
            self.return_book()
        elif choice == "4":
            self.view_overdue_loans()
        elif choice == "5":
            self.view_active_loans()
        elif choice == "0":
            self.display_menu()
        else:
            print("Invalid choice.")

    def book_management_menu(self):
        """Display the book management menu"""
        print("\nBook Management")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Remove Book")
        print("4. View All Books")
        print("5. Search Books")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.add_book()
        elif choice == "2":
            self.update_book()
        elif choice == "3":
            self.remove_book()
        elif choice == "4":
            self.view_all_books()
        elif choice == "5":
            self.search_books()
        elif choice == "0":
            self.display_menu()
        else:
            print("Invalid choice.")

    def member_management_menu(self):
        """Display the member management menu"""
        print("\nMember Management")
        print("1. Register Member")
        print("2. Update Member")
        print("3. Remove Member")
        print("4. View All Members")
        print("5. Search Members")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.register_member()
        elif choice == "2":
            self.update_member()
        elif choice == "3":
            self.remove_member()
        elif choice == "4":
            self.view_all_members()
        elif choice == "5":
            self.search_members()
        elif choice == "0":
            self.display_menu()
        else:
            print("Invalid choice.")

    def staff_management_menu(self):
        """Display the staff management menu"""
        staff_id = input("Enter your Staff ID to access Staff Management: ")
        query = "SELECT role FROM Staff WHERE staff_id = ?"
        result = self.db.execute_query(query, (staff_id,))
        if not result or result[0]["role"] not in ["Manager", "Head Librarian"]:
            print("Access denied. You do not have permission to manage staff.")
            return

        print("\nStaff Management")
        print("1. Add Staff Member")
        print("2. Update Staff Member")
        print("3. Remove Staff Member")
        print("4. View All Staff Members")
        print("5. Search Staff Members")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.add_staff()
        elif choice == "2":
            self.update_staff()
        elif choice == "3":
            self.remove_staff()
        elif choice == "4":
            self.view_all_staff()
        elif choice == "5":
            self.search_staff()
        elif choice == "0":
            self.display_menu()
        else:
            print("Invalid choice.")