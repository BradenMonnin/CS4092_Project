import sqlite3
from datetime import datetime, timedelta

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

    def borrow_book(self):
        """Process book borrowing"""
        try:
            member_id = int(input("Enter Member ID: "))
            book_id = int(input("Enter Book ID: "))
            
            # Check if member exists
            member_check = self.execute_query("SELECT * FROM MEMBER WHERE member_id = ?", (member_id,))
            if not member_check:
                print("Member not found!")
                return
            
            # Check if book exists and is available
            book_check = self.execute_query(
                "SELECT * FROM BOOK WHERE book_id = ? AND available_copies > 0", 
                (book_id,)
            )
            if not book_check:
                print("Book not found or no copies available!")
                return
            
            # Check member's current loan count
            loan_count = self.execute_query(
                "SELECT COUNT(*) as count FROM LOAN WHERE member_id = ? AND status = 'Active'",
                (member_id,)
            )[0]['count']
            
            if loan_count >= 5:
                print("Member has reached the maximum loan limit (5 books)!")
                return
            
            # Create loan record
            loan_date = datetime.now().strftime('%Y-%m-%d')
            due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            
            insert_loan = """
            INSERT INTO LOAN (member_id, book_id, loan_date, due_date, status)
            VALUES (?, ?, ?, ?, 'Active')
            """
            
            # Update available copies
            update_book = """
            UPDATE BOOK SET available_copies = available_copies - 1 
            WHERE book_id = ?
            """
            
            # Execute queries
            if (self.execute_update(insert_loan, (member_id, book_id, loan_date, due_date)) > 0 and
                self.execute_update(update_book, (book_id,)) > 0):
                
                member_name = f"{member_check[0]['first_name']} {member_check[0]['last_name']}"
                book_title = book_check[0]['title']
                
                print(f"Book borrowed successfully!")
                print(f"Member: {member_name}")
                print(f"Book: {book_title}")
                print(f"Due Date: {due_date.strftime('%b %#d, %Y')}")
            else:
                print("Failed to process book borrowing!")
                
        except ValueError:
            print("Please enter valid numeric IDs!")
        except Exception as e:
            print(f"Error: {e}")

    def renew_book(self):
        """Process book renewal"""
        try:
            member_id = int(input("Enter Member ID: "))
            book_id = int(input("Enter Book ID: "))
            
            # Check if loan exists
            loan_check = self.execute_query(
                "SELECT * FROM LOAN WHERE member_id = ? AND book_id = ? AND status = 'Active'",
                (member_id, book_id)
            )
            if not loan_check:
                print("No active loan found for this book and member!")
                return
            
            # Renew the loan
            new_due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            update_loan = """
            UPDATE LOAN SET due_date = ? WHERE member_id = ? AND book_id = ? AND status = 'Active'
            """
            
            if self.execute_update(update_loan, (new_due_date, member_id, book_id)) > 0:
                print(f"Book renewed successfully! New Due Date: {new_due_date.strftime('%b %#d, %Y')}")
            else:
                print("Failed to renew the book!")
                
        except ValueError:
            print("Please enter valid numeric IDs!")
        except Exception as e:
            print(f"Error: {e}")

    def return_book(self):
        """Process book return"""
        try:
            member_id = int(input("Enter Member ID: "))
            book_id = int(input("Enter Book ID: "))
            
            # Check if loan exists
            loan_check = self.execute_query(
                "SELECT * FROM LOAN WHERE member_id = ? AND book_id = ? AND status = 'Active'",
                (member_id, book_id)
            )
            if not loan_check:
                print("No active loan found for this book and member!")
                return
            
            # Update the loan status to 'Returned'
            update_loan = """
            UPDATE LOAN SET status = 'Returned' WHERE member_id = ? AND book_id = ? AND status = 'Active'
            """
            
            # Update available copies
            update_book = """
            UPDATE BOOK SET available_copies = available_copies + 1 
            WHERE book_id = ?
            """
            
            if (self.execute_update(update_loan, (member_id, book_id)) > 0 and
                self.execute_update(update_book, (book_id,)) > 0):
                
                print("Book returned successfully!")
            else:
                print("Failed to return the book!")
                
        except ValueError:
            print("Please enter valid numeric IDs!")
        except Exception as e:
            print(f"Error: {e}")

    def view_overdue_loans(self):
        """View all overdue loans"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            query = """
            SELECT LOAN.loan_id, MEMBER.first_name, MEMBER.last_name, BOOK.title, LOAN.due_date 
            FROM LOAN 
            JOIN MEMBER ON LOAN.member_id = MEMBER.member_id 
            JOIN BOOK ON LOAN.book_id = BOOK.book_id 
            WHERE LOAN.status = 'Active' AND LOAN.due_date < ?
            """
            overdue_loans = self.db.execute_query(query, (today,))
            
            if overdue_loans:
                print("\nOverdue Loans:")
                for loan in overdue_loans:
                    print(f"Loan ID: {loan['loan_id']}, Member: {loan['first_name']} {loan['last_name']}, "
                          f"Book: {loan['title']}, Due Date: {loan['due_date']}")
            else:
                print("No overdue loans found.")
                
        except Exception as e:
            print(f"Error: {e}")

    def view_active_loans(self):
        """View all active loans"""
        try:
            query = """
            SELECT LOAN.loan_id, MEMBER.first_name, MEMBER.last_name, BOOK.title, LOAN.due_date 
            FROM LOAN 
            JOIN MEMBER ON LOAN.member_id = MEMBER.member_id 
            JOIN BOOK ON LOAN.book_id = BOOK.book_id 
            WHERE LOAN.status = 'Active'
            """
            active_loans = self.db.execute_query(query)
            
            if active_loans:
                print("\nActive Loans:")
                for loan in active_loans:
                    print(f"Loan ID: {loan['loan_id']}, Member: {loan['first_name']} {loan['last_name']}, "
                          f"Book: {loan['title']}, Due Date: {loan['due_date']}")
            else:
                print("No active loans found.")
                
        except Exception as e:
            print(f"Error: {e}")

    def add_book(self):
        """Add a new book to the library"""
        try:
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            isbn = input("Enter ISBN: ").strip()
            publication_year = int(input("Enter publication year: "))
            genre = input("Enter genre: ").strip()
            total_copies = int(input("Enter total copies: "))

            if total_copies <= 0:
                print("Total copies must be greater than 0.")
                return

            available_copies = total_copies

            query = """
            INSERT INTO Book (title, author, isbn, publication_year, genre, total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            result = self.db.execute_update(query, (title, author, isbn, publication_year, genre, total_copies, available_copies))
            if result:
                print("Book added successfully!")
            else:
                print("Failed to add book. ISBN may already exist.")
        except ValueError:
            print("Please enter valid numeric values for publication year and total copies.")
        except Exception as e:
            print(f"Error: {e}")

    def update_book(self):
        """Update an existing book in the library"""
        try:
            book_id = int(input("Enter Book ID to update: "))
            title = input("Enter new book title (leave blank to keep current): ").strip()
            author = input("Enter new author name (leave blank to keep current): ").strip()
            isbn = input("Enter new ISBN (leave blank to keep current): ").strip()
            publication_year = input("Enter new publication year (leave blank to keep current): ").strip()
            genre = input("Enter new genre (leave blank to keep current): ").strip()
            total_copies = input("Enter new total copies (leave blank to keep current): ").strip()

            query = "UPDATE Book SET "
            params = []

            if title:
                query += "title = ?, "
                params.append(title)
            if author:
                query += "author = ?, "
                params.append(author)
            if isbn:
                query += "isbn = ?, "
                params.append(isbn)
            if publication_year:
                query += "publication_year = ?, "
                params.append(int(publication_year))
            if genre:
                query += "genre = ?, "
                params.append(genre)
            if total_copies:
                query += "total_copies = ?, available_copies = ? "
                params.append(int(total_copies))
                params.append(int(total_copies))  # Reset available copies to total copies
            else:
                query = query.rstrip(", ")  # Remove trailing comma

            query += " WHERE book_id = ?"
            params.append(book_id)

            result = self.db.execute_update(query, tuple(params))
            if result:
                print("Book updated successfully!")
            else:
                print("Failed to update book. Check if the book exists.")
        except ValueError:
            print("Please enter valid numeric values for publication year and total copies.")
        except Exception as e:
            print(f"Error: {e}")

    def remove_book(self):
        """Remove a book from the library"""
        try:
            book_id = int(input("Enter Book ID to remove: "))
            query = "DELETE FROM Book WHERE book_id = ?"
            result = self.db.execute_update(query, (book_id,))
            if result:
                print("Book removed successfully!")
            else:
                print("Failed to remove book. Check if the book exists.")
        except ValueError:
            print("Please enter a valid numeric Book ID.")
        except Exception as e:
            print(f"Error: {e}")