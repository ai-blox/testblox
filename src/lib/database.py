import sqlite3
import logging
import os


class DataBase:
    def __init__(self, name):

        self.connected = None
        self.logger = logging.getLogger(name)

        self.db_file = "db.sqlite"

    def set_db_file(self, db_filename):

        config_path = "db.sqlite" if not db_filename else db_filename
        if not os.path.exists(config_path):
            self.logger.error("Config file not found: %s" % config_path)
            return None

        self.db_file = config_path

    def table_exists(self, table_name):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Execute a query to check if the table exists
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            result = cursor.fetchone()

            conn.close()

            # If a result is returned, the table exists
            return result is not None
        except sqlite3.Error as e:
            self.logger.error(f"Checking if table exists: {e}")
            return False


    def check_db(self, db_file=None):

        if (db_file is not None) and (db_file != self.db_file):
            self.db_file = db_file

        return self.table_exists('versions')

    def get_test_benches(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Execute the SQL query to fetch all values in the "name" column
            cursor.execute("SELECT name FROM test_benches")

            # Fetch all the results and store them in a list
            names = [row[0] for row in cursor.fetchall()]

            conn.close()
            return names
        except sqlite3.Error as e:
            self.logger.error(f"Error fetching names from the table: {e}")
            return []

    def get_test_bench_drivers(self, test_bench_name):
        try:
            conn = sqlite3.connect(self.db_file)
            # make sure the column names are included
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Execute the SQL query to fetch all values in the "name" column
            cursor.execute(f"SELECT test_bench_drivers.* \
                             FROM test_bench_drivers \
                             INNER JOIN test_benches ON test_benches.id=test_bench_drivers.id \
                             WHERE test_benches.name='{test_bench_name}';")

            # Fetch all the results and store them in a list
            drivers = cursor.fetchall()

            conn.close()
            return [dict(driver) for driver in drivers]
        except sqlite3.Error as e:
            self.logger.error(f"Error fetching names from the table: {e}")
            return []
    def get_test_bench_driver_configs(self, test_bench_name, driver_name):
        try:
            conn = sqlite3.connect(self.db_file)
            # make sure the column names are included
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Execute the SQL query to fetch all values in the "name" column
            cursor.execute(f"SELECT test_bench_drivers_configs.* \
                             FROM test_bench_drivers_configs \
                             INNER JOIN test_benches ON test_benches.id=test_bench_drivers_configs.test_bench.id \
                             INNER JOIN test_bench_drivers on test_bench_drivers.id=test_bench_drivers_configs.test_bench_driver_id \
                             WHERE test_benches.name='{test_bench_name}' \
                             AND test_bench_drivers.name='{driver_name}';")

            # Fetch all the results and store them in a list
            drivers = cursor.fetchall()

            conn.close()
            return [dict(driver) for driver in drivers]
        except sqlite3.Error as e:
            self.logger.error(f"Error fetching names from the table: {e}")
            return []