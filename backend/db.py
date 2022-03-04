import os
import sqlite3
from datetime import datetime


def backup_progress(status, remaining, total):
    print("Copied " + str(total - remaining) + " of " + str(total) + " pages...")


class Database:
    def __init__(self):
        # Connect to local database
        #self.db = sqlite3.connect(os.environ["SQLITE_DB_FILE_NAME"])
        self.db = sqlite3.connect("database.db")
        self.cur = self.db.cursor()

        # Set up tables if they do not exist
        self.setup_tables()

    def setup_tables(self):
        # Data tables
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS participants
            (
                id integer primary key,
                created text
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS chalDatapoints
            (
                id integer primary key,
                created text,
                numAttempts integer,
                numChecks integer,
                timeToComplete integer
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS startupDatapoints
            (
                id integer primary key,
                created text,
                experience float,
                familiarity float,
                skill float
            )
        """)
        # Relational tables
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS datalogChalDatapoints
            (
                pID integer,
                dpID integer
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS datalogStartupDatapoints
            (
                pID integer,
                dpID integer
            )
        """)


    def insertChalDatapoint(self, pID, chalDP):
        self.db.execute(f"""
            INSERT INTO chalDatapoints (created, numAttempts, numChecks, timeToComplete) 
            VALUES ({chalDP["created"]}, {chalDP["numAttempts"]}, {chalDP["numChecks"]}, {chalDP["timeToComplete"]});
            INSERT INTO datalogChalDatapoints (pID, dpID) VALUES ({pID}, {self.db.lastrowid})
        """)

    def shutdown(self):
        # Backup and shut down database
        self.backup()
        self.db.close()

    def backup(self):
        bck = sqlite3.connect('bck_' + str(datetime.timestamp(datetime.now())) + ".backupdb")
        with bck:
            self.db.backup(bck, progress=backup_progress)
        bck.close()
