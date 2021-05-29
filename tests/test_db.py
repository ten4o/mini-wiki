from source import db
import unittest


class TestDb(unittest.TestCase):
    def test_insert(self):
        title = 't' * db.MAX_TITLE_SIZE
        body = 'body'
        tag_list = ['tag1', 'tag2']
        topic_id = TestDb.db.insert_topic(title, body, tag_list)
        self.assertIsNotNone(topic_id, 'There must be an insert id')

        topic = TestDb.db.get_topic_by_id(topic_id)
        self.assertEqual(topic.title, title, 'Title must be the same')
        self.assertEqual(topic.body, body, 'Body must be the same')
        self.assertListEqual(tag_list, [tag.name for tag in topic.tags])

    def test_insert_long_title(self):
        self.assertRaises(ValueError,
                          TestDb.db.insert_topic, 'title' * 100, 'body', ['tag1', 'tag2'])

    def test_insert_long_tag(self):
        self.assertRaises(ValueError,
                          TestDb.db.insert_topic, 'title long tag', 'body', ['g' * (db.MAX_TAG_SIZE + 1), 'tag2'])

    def test_insert_dup_tags(self):
        title = 'title 2'
        body = 'body 2'
        tag_list = ['tag1', 'tag3']
        topic_id = TestDb.db.insert_topic(title, body, tag_list)
        self.assertIsNotNone(topic_id, 'There must be an insert id')

        topic = TestDb.db.get_topic_by_id(topic_id)
        self.assertEqual(topic.title, title, 'Title must be the same')
        self.assertEqual(topic.body, body, 'Body must be the same')
        self.assertListEqual(tag_list, [tag.name for tag in topic.tags])

    def test_get_by_invalid_id(self):
        topic = TestDb.db.get_topic_by_id(1e9)
        self.assertIsNone(topic)

    def test_get_by_name(self):
        title = 'title 3'
        body = 'body 2'
        tag_list = ['tag1', 'tag3']
        topic_id = TestDb.db.insert_topic(title, body, tag_list)
        self.assertIsNotNone(topic_id, 'There must be an insert id')
        topic = TestDb.db.get_topic_by_title(title)
        self.assertIsNotNone(topic)
        self.assertEqual(topic.body, body, 'Body must be the same')
        self.assertListEqual(tag_list, [tag.name for tag in topic.tags])


    @classmethod
    def setUpClass(cls):
        print('==================== setUpClass')
        cls.db = db.DB()

    @classmethod
    def tearDownClass(cls):
        print('==================== tearDownClass')
        cls.db.drop_all()
