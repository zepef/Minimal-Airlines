import sqlite3
import os
from sqlite3 import Error

class UserManagementAgent:
    def __init__(self, db_file="airline_users.db"):
        self.conn = None
        try:
            # Get the absolute path of the script
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # Navigate to the instances directory
            instances_dir = os.path.join(script_dir, 'instances')
            # Create instances directory if it doesn't exist
            os.makedirs(instances_dir, exist_ok=True)
            # Create the full path for the database file
            db_path = os.path.join(instances_dir, db_file)
            
            print(f"Connecting to users database at: {db_path}")
            self.conn = sqlite3.connect(db_path)
            self.create_table()
        except Error as e:
            print(f"Error initializing user management: {e}")

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                             (id INTEGER PRIMARY KEY,
                              username TEXT NOT NULL UNIQUE,
                              email TEXT NOT NULL,
                              role TEXT NOT NULL)''')
            self.conn.commit()
        except Error as e:
            print(f"Error creating table: {e}")

    def create_user(self, username, email, role):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users(username, email, role) VALUES(?,?,?)", (username, email, role))
            self.conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error creating user: {e}")
            return None

    def read_user(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error reading user: {e}")
            return None

    def update_user(self, user_id, username, email, role):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE users SET username=?, email=?, role=? WHERE id=?", (username, email, role, user_id))
            self.conn.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error updating user: {e}")
            return 0

    def delete_user(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            self.conn.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error deleting user: {e}")
            return 0

    def list_users(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
        except Error as e:
            print(f"Error listing users: {e}")
            return []

    def __del__(self):
        """Ensure the database connection is closed when the object is destroyed"""
        if self.conn:
            self.conn.close()

# Create a global instance of the user management agent
user_management_agent = UserManagementAgent()
