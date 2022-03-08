import os
import sqlite3
from datetime import datetime


def backup_progress(status, remaining, total):
    print("Copied " + str(total - remaining) + " of " + str(total) + " pages...")


class Database:
    def __init__(self):
        # Connect to local database
        self.db = sqlite3.connect(os.environ["SQLITE_DB_FILE_NAME"])
        self.cur = self.db.cursor()

        # Set up tables if they do not exist
        self.setup_tables()

    def setup_tables(self):
        # Data tables
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS participants
            (
                id text,
                created text
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS chalDatapoints
            (
                pID text,
                created text,
                context text,
                numAttempts integer,
                numChecks integer,
                timeToComplete integer
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS startupDatapoints
            (
                pID text,
                created text,
                experience float,
                familiarity float,
                skill float
            )
        """)

        # Save changes
        self.db.commit()

    def insert_participant(self, participant):
        self.insert(f"""
            INSERT INTO participants (id, created) VALUES ("{participant["id"]}", "{participant["created"]}");
        """)

    def insert_chal(self, p_id, chal_dp):
        self.insert(f"""
            INSERT INTO chalDatapoints (pID, created, context, numAttempts, numChecks, timeToComplete) 
            VALUES ("{p_id}", "{chal_dp["created"]}", "{chal_dp["context"]}", {chal_dp["num_attempts"]}, {chal_dp["num_checks"]}, {chal_dp["time_to_complete"]})
        """)

    def insert_start(self, p_id, start_dp):
        self.insert(f"""
            INSERT INTO startupDatapoints (pID, created, experience, familiarity, skill) 
            VALUES ("{p_id}", "{start_dp["created"]}", {start_dp["experience"]}, {start_dp["familiarity"]}, {start_dp["skill"]});
        """)

    def get_insert_id(self):
        return self.query('SELECT last_insert_rowid()')[0][0]

    # Query database and return selected rows
    def query(self, query_string):
        return self.cur.execute(query_string).fetchall()

    # Run command to insert into database
    def insert(self, insert_string):
        self.cur.execute(insert_string)
        self.db.commit()

    # Backup and shut down database
    def shutdown(self):
        self.backup()
        self.db.close()

    # Backup database
    def backup(self):
        backup_name = 'bck_' + str(datetime.timestamp(datetime.now())) + ".backupdb"
        bck = sqlite3.connect(backup_name)
        with bck:
            self.db.backup(bck, progress=backup_progress)
        bck.close()
        # Move backup file to back up directory
        if not os.path.exists("backups"):
            os.makedirs("backups")
        os.rename(backup_name, "backups/" + backup_name)
