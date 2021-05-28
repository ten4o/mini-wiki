from source import db
import unittest

class TestDb(unittest.TestCase):
    def test_test(self):
        db_ref = db.DB()
        db_ref.insert_topic('title', 'body', ['tag1', 'tag2'])


