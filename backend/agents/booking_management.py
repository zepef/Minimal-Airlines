import sqlite3
import os
from sqlite3 import Error
from datetime import datetime

class BookingManagementAgent:
    def __init__(self, db_file="airline_bookings.db"):
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
            
            print(f"Connecting to bookings database at: {db_path}")
            self.conn = sqlite3.connect(db_path)
            self.create_table()
        except Error as e:
            print(f"Error initializing booking management: {e}")

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS bookings
                             (id INTEGER PRIMARY KEY,
                              customer_id TEXT NOT NULL,
                              flight_number TEXT NOT NULL,
                              from_airport TEXT NOT NULL,
                              to_airport TEXT NOT NULL,
                              departure_date TEXT NOT NULL,
                              booking_date TEXT NOT NULL,
                              status TEXT NOT NULL)''')
            self.conn.commit()
        except Error as e:
            print(f"Error creating table: {e}")

    def create_booking(self, customer_id, flight_number, from_airport, to_airport, departure_date, status="Confirmed"):
        try:
            cursor = self.conn.cursor()
            booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO bookings(customer_id, flight_number, from_airport, to_airport, departure_date, booking_date, status) VALUES(?,?,?,?,?,?,?)",
                           (customer_id, flight_number, from_airport, to_airport, departure_date, booking_date, status))
            self.conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error creating booking: {e}")
            return None

    def read_booking(self, booking_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM bookings WHERE id=?", (booking_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error reading booking: {e}")
            return None

    def update_booking(self, booking_id, flight_number=None, from_airport=None, to_airport=None, departure_date=None, status=None):
        try:
            cursor = self.conn.cursor()
            current_booking = self.read_booking(booking_id)
            if current_booking is None:
                return 0
            
            new_flight_number = flight_number if flight_number is not None else current_booking[2]
            new_from_airport = from_airport if from_airport is not None else current_booking[3]
            new_to_airport = to_airport if to_airport is not None else current_booking[4]
            new_departure_date = departure_date if departure_date is not None else current_booking[5]
            new_status = status if status is not None else current_booking[7]
            
            cursor.execute("UPDATE bookings SET flight_number=?, from_airport=?, to_airport=?, departure_date=?, status=? WHERE id=?",
                           (new_flight_number, new_from_airport, new_to_airport, new_departure_date, new_status, booking_id))
            self.conn.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error updating booking: {e}")
            return 0

    def delete_booking(self, booking_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
            self.conn.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error deleting booking: {e}")
            return 0

    def list_bookings(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM bookings")
            return cursor.fetchall()
        except Error as e:
            print(f"Error listing bookings: {e}")
            return []

    def __del__(self):
        """Ensure the database connection is closed when the object is destroyed"""
        if self.conn:
            self.conn.close()

# Create a global instance of the booking management agent
booking_management_agent = BookingManagementAgent()
