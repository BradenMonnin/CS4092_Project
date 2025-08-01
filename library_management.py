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