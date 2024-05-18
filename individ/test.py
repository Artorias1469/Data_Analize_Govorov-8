import unittest
import sqlite3
from pathlib import Path
import os
import flight_management  # Assuming this is where your main code resides

TEST_DB = "test_flights.db"

class CustomTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln(f"{self.getDescription(test)} ... ok")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.stream.writeln(f"{self.getDescription(test)} ... skipped '{reason}'")


class CustomTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)


class FlightManagementTest(unittest.TestCase):

    def setUp(self):
        """Create a test database before each test."""
        self.database_path = Path(TEST_DB)
        flight_management.create_tables(self.database_path)

    def tearDown(self):
        """Remove the test database after each test."""
        os.remove(self.database_path)

    def test_add_flight(self):
        """Test adding a flight."""
        # Add a flight manually
        destination = "Москва"
        flight_number = "SU123"
        aircraft_type = "Boeing 737"

        conn = sqlite3.connect(str(self.database_path))
        cursor = conn.cursor()
        cursor.execute("INSERT INTO flights (destination, flight_number, aircraft_type) VALUES (?, ?, ?)",
                       (destination, flight_number, aircraft_type))
        conn.commit()
        conn.close()

        # Check that the flight is added
        conn = sqlite3.connect(str(self.database_path))
        cursor = conn.cursor()
        cursor.execute("SELECT destination, flight_number, aircraft_type FROM flights WHERE flight_number = ?",
                       (flight_number,))
        row = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(row)
        self.assertEqual(row, (destination, flight_number, aircraft_type))

    def test_print_flights(self):
        """Test printing all flights."""
        # Add flights manually
        flights_data = [
            ("Москва", "SU123", "Boeing 737"),
            ("Санкт-Петербург", "SU124", "Airbus A320")
        ]

        conn = sqlite3.connect(str(self.database_path))
        cursor = conn.cursor()
        for flight_data in flights_data:
            cursor.execute("INSERT INTO flights (destination, flight_number, aircraft_type) VALUES (?, ?, ?)",
                           flight_data)
        conn.commit()
        conn.close()

        # Redirect stdout to a string
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        flight_management.print_flights(self.database_path)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        for destination, flight_number, aircraft_type in flights_data:
            self.assertIn(destination, output)
            self.assertIn(flight_number, output)
            self.assertIn(aircraft_type, output)

    def test_search_flights_by_aircraft_type(self):
        """Test searching flights by aircraft type."""
        # Add flights manually
        flights_data = [
            ("Москва", "SU123", "Boeing 737"),
            ("Санкт-Петербург", "SU124", "Airbus A320")
        ]

        conn = sqlite3.connect(str(self.database_path))
        cursor = conn.cursor()
        for flight_data in flights_data:
            cursor.execute("INSERT INTO flights (destination, flight_number, aircraft_type) VALUES (?, ?, ?)",
                           flight_data)
        conn.commit()
        conn.close()

        # Redirect stdout to a string
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        flight_management.search_flights_by_aircraft_type(self.database_path, "Boeing 737")
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Москва", output)
        self.assertIn("SU123", output)
        self.assertIn("Boeing 737", output)
        self.assertNotIn("Санкт-Петербург", output)
        self.assertNotIn("SU124", output)
        self.assertNotIn("Airbus A320", output)


if __name__ == "__main__":
    # Use the custom test runner
    unittest.main(testRunner=CustomTestRunner)
