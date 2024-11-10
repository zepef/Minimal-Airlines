import sqlite3
import os
from datetime import datetime

class TransactionJournal:
    def __init__(self, db_file="airline_journal.db"):
        self.conn = None
        try:
            # Get the absolute path of the script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Navigate to the instances directory (one level up from script location)
            instances_dir = os.path.join(script_dir, 'instances')
            # Create instances directory if it doesn't exist
            os.makedirs(instances_dir, exist_ok=True)
            # Create the full path for the database file
            db_path = os.path.join(instances_dir, db_file)
            
            print(f"Connecting to journal database at: {db_path}")
            self.conn = sqlite3.connect(db_path)
            self.create_table()
        except Exception as e:
            print(f"Error initializing journal: {e}")

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                             (id INTEGER PRIMARY KEY,
                              timestamp TEXT NOT NULL,
                              user_id TEXT,
                              service_type TEXT NOT NULL,
                              action_type TEXT NOT NULL,
                              details TEXT,
                              status TEXT NOT NULL)''')
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

    def log_transaction(self, user_id, service_type, action_type, details, status="completed"):
        """
        Log a transaction to the journal
        
        Parameters:
        - user_id: ID of the user performing the action
        - service_type: Type of service (flight, baggage, seat, meal)
        - action_type: Type of action (create, change, cancel, etc.)
        - details: Additional details about the transaction
        - status: Status of the transaction (completed, failed, pending)
        """
        try:
            cursor = self.conn.cursor()
            timestamp = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO transactions (timestamp, user_id, service_type, action_type, details, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, user_id, service_type, action_type, details, status))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error logging transaction: {e}")
            return None

    def get_user_transactions(self, user_id):
        """Get all transactions for a specific user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving transactions: {e}")
            return []

    def get_service_transactions(self, service_type):
        """Get all transactions for a specific service type"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE service_type = ? ORDER BY timestamp DESC", (service_type,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving transactions: {e}")
            return []

    def get_recent_transactions(self, limit=50):
        """Get the most recent transactions"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT ?", (limit,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving transactions: {e}")
            return []

    def __del__(self):
        """Ensure the database connection is closed when the object is destroyed"""
        if self.conn:
            self.conn.close()

# Create a global instance of the journal
journal = TransactionJournal()
