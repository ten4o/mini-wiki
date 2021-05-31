from source import db
from source.db import DuplicateTitleException
import unittest


class TestDb(unittest.TestCase):
    def assertTopic(self, topic, title, body, tag_list):
        self.assertIsNotNone(topic)
        self.assertEqual(topic.title, title, 'Topic title must be the same')
        self.assertEqual(topic.body, body, 'Topic body must be the same')
        if tag_list:
            self.assertListEqual(sorted(tag_list), sorted([tag.name for tag in topic.tags]))

    def test_insert(self):
        title = 't' * db.MAX_TITLE_SIZE
        body = 'body'
        tag_list = ['tag1', 'tag2']
        topic_id = TestDb.db.insert_topic(title, body, tag_list)
        self.assertIsNotNone(topic_id, 'There must be an insert id')

        topic = TestDb.db.get_topic_by_id(topic_id)
        self.assertTopic(topic, title, body, tag_list)

    def test_insert_long_title(self):
        self.assertRaises(ValueError,
                          TestDb.db.insert_topic, 'title' * 100, 'body', ['tag1', 'tag2'])

    def test_insert_long_tag(self):
        self.assertRaises(ValueError,
                          TestDb.db.insert_topic, 'title long tag', 'body', ['g' * (db.MAX_TAG_SIZE + 1), 'tag2'])

    def test_insert_dup_title(self):
        title = 'title test_insert_dup_title'
        body = 'body 2'
        tag_list = ['tag1', 'tag3']

        TestDb.db.insert_topic(title, body, tag_list)
        try:
            TestDb.db.insert_topic(title, body, tag_list)
            self.assertFalse(True)
        except DuplicateTitleException:
            pass


    def test_insert_dup_tags(self):
        title = 'title 2'
        body = 'body 2'
        tag_list = ['tag1', 'tag3']
        topic_id = TestDb.db.insert_topic(title, body, tag_list)
        self.assertIsNotNone(topic_id, 'There must be an insert id')

        topic = TestDb.db.get_topic_by_id(topic_id)
        self.assertTopic(topic, title, body, tag_list)

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
        self.assertTopic(topic, title, body, tag_list)

    def test_get_topic_list(self):
        # insert 3 topics
        titles = ['test_get_topic_list1 title', 'test_get_topic_list2 title', 'test_get_topic_list3']
        body = ['body1 test_get_topic_list1', 'body test_get_topic_list2', 'body test_get_topic_list3']
        tag_list = ['tag1', 'tag2', 'tag3', 'tag4']
        for idx, obj in enumerate(zip(titles, body)):
            ins_title, ins_body = obj
            TestDb.db.insert_topic(ins_title, ins_body, tag_list[:idx + 2])

        # get all topics from DB
        topic_list = TestDb.db.get_topic_list(None, None)

        # there must be at least 3 topics
        self.assertIsNotNone(topic_list)
        self.assertGreater(len(topic_list), 2);

        # check if our topics are in the result
        for check_title, check_body in zip(titles, body):
            topic = next((t for t in topic_list if t.title == check_title), None)
            self.assertTopic(topic, check_title, check_body, None)

        # search for topic by a substring in the title
        topic_list = TestDb.db.get_topic_list(title = 'list2', body = None)
        self.assertIsNotNone(topic_list)

        # there must be only one topic in the result
        self.assertEqual(len(topic_list), 1)
        self.assertTopic(topic_list[0], titles[1], body[1], tag_list[:3])

        # search for topic by a substring in the title and in the body
        topic_list = TestDb.db.get_topic_list(title = 'title', body = 'body1')
        self.assertIsNotNone(topic_list)

        # there must be only one topic in the result
        self.assertEqual(len(topic_list), 1)
        self.assertTopic(topic_list[0], titles[0], body[0], tag_list[:2])


        # search of non-existing topic
        topic_list = TestDb.db.get_topic_list(title = 'None-existing', body = None)

        # the result must be an empty list
        self.assertEqual(len(topic_list), 0)

        # check that escaping works
        topic_list = TestDb.db.get_topic_list(title = '%_', body = None)
        self.assertEqual(len(topic_list), 0)
        topic_list = TestDb.db.get_topic_list(title = '%', body = None)
        self.assertEqual(len(topic_list), 0)
        topic_list = TestDb.db.get_topic_list(title = '__', body = None)
        self.assertEqual(len(topic_list), 0)


    @classmethod
    def setUpClass(cls):
        cls.db = db.DB(is_test=True)

    @classmethod
    def tearDownClass(cls):
        cls.db.drop_all()
