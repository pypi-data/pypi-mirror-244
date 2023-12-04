import os

try:
    DB_PATH = os.environ["STAFF_DB_PATH"]
except KeyError:
    DB_PATH = os.path.join(os.path.dirname(__file__), "staff.db")
