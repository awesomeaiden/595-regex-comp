from .. import db
from datetime import datetime

# Test data
part_1 = {
    "id": "some_participant_id",
    "created": datetime.now()
}

part_2 = {
    "id": "another_participant_id",
    "created": datetime.now()
}

start_1 = {
    "created": datetime.now(),
    "experience": 0.3,
    "familiarity": 0.6,
    "skill": 0.2
}

start_2 = {
    "created": datetime.now(),
    "experience": 0.8,
    "familiarity": 0.7,
    "skill": 0.5
}

chal_1 = {
    "created": datetime.now(),
    "num_attempts": 12,
    "num_checks": 28,
    "time_to_complete": 90000
}

chal_2 = {
    "created": datetime.now(),
    "num_attempts": 16,
    "num_checks": 20,
    "time_to_complete": 70000
}

chal_3 = {
    "created": datetime.now(),
    "num_attempts": 4,
    "num_checks": 7,
    "time_to_complete": 80000
}


def setup_database():
    return db.Database()


def insert_data(database):
    # Insert new participant
    database.insert_participant(part_1)
    # Insert new startup datapoint
    database.insert_start(part_1["id"], start_1)
    # Insert challenge datapoints
    database.insert_chal(part_1["id"], chal_1)
    database.insert_chal(part_1["id"], chal_2)
    database.insert_chal(part_1["id"], chal_3)

    # Insert another participant
    database.insert_participant(part_2)
    # Insert new startup datapoint
    database.insert_start(part_2["id"], start_2)
    # Insert challenge datapoints
    database.insert_chal(part_2["id"], chal_1)
    database.insert_chal(part_2["id"], chal_2)
    database.insert_chal(part_2["id"], chal_3)


def test_database():
    database = setup_database()

    # Check that all tables exist
    assert(len(database.query("SELECT name FROM sqlite_master WHERE type='table' AND name='participants';")) > 0)
    assert(len(database.query("SELECT name FROM sqlite_master WHERE type='table' AND name='chalDatapoints';")) > 0)
    assert(len(database.query("SELECT name FROM sqlite_master WHERE type='table' AND name='startupDatapoints';")) > 0)
    assert(len(database.query("SELECT name FROM sqlite_master WHERE type='table' AND name='datalogChalDatapoints';")) > 0)
    assert(len(database.query("SELECT name FROM sqlite_master WHERE type='table' AND name='datalogStartupDatapoints';")) > 0)

    # Test inserts
    insert_data(database)
    assert(len(database.query("SELECT * FROM participants")) == 2)
    assert(len(database.query("SELECT * FROM startupDatapoints")) == 2)
    assert(len(database.query("SELECT * FROM chalDatapoints")) == 6)
    assert(len(database.query("SELECT * FROM datalogStartupDatapoints")) == 2)
    assert(len(database.query("SELECT * FROM datalogChalDatapoints")) == 6)

    # Test backup and close
    database.shutdown()
