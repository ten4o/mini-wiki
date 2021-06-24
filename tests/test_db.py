from source import db
from source.db import DuplicateTitleException
import unittest


class TestDb(unittest.TestCase):
    def assertArticle(self, article, title, body, tag_list):
        self.assertIsNotNone(article)
        self.assertEqual(article.title, title, 'Article title must be the same')
        self.assertEqual(article.body, body, 'Article body must be the same')
        if tag_list:
            self.assertListEqual(sorted(tag_list), sorted([tag.name for tag in article.tags]))

    def test_insert(self):
        title = 't' * db.MAX_TITLE_SIZE
        body = 'body'
        tag_list = ['tag1', 'tag2']
        article_id = TestDb.db.insert_article(title, body, tag_list)
        self.assertIsNotNone(article_id, 'There must be an insert id')

        article = TestDb.db.get_article_by_id(article_id)
        self.assertArticle(article, title, body, tag_list)

    def test_insert_long_title(self):
        self.assertRaises(ValueError,
                          TestDb.db.insert_article, 'title' * 100, 'body', ['tag1', 'tag2'])

    def test_insert_long_tag(self):
        self.assertRaises(ValueError,
                          TestDb.db.insert_article, 'title long tag', 'body', ['g' * (db.MAX_TAG_SIZE + 1), 'tag2'])

    def test_insert_dup_title(self):
        title = 'title test_insert_dup_title'
        body = 'body 2'
        tag_list = ['tag1', 'tag3']

        TestDb.db.insert_article(title, body, tag_list)
        try:
            TestDb.db.insert_article(title, body, tag_list)
            self.assertFalse(True)
        except DuplicateTitleException:
            pass

    def test_insert_dup_tags(self):
        title = 'title 2'
        body = 'body 2'
        tag_list = ['tag1', 'tag3']
        article_id = TestDb.db.insert_article(title, body, tag_list)
        self.assertIsNotNone(article_id, 'There must be an insert id')

        article = TestDb.db.get_article_by_id(article_id)
        self.assertArticle(article, title, body, tag_list)

    def test_get_by_invalid_id(self):
        article = TestDb.db.get_article_by_id(1e9)
        self.assertIsNone(article)

    def test_get_by_name(self):
        title = 'title 3'
        body = 'body 2'
        tag_list = ['tag4', 'tag3']
        article_id = TestDb.db.insert_article(title, body, tag_list)
        self.assertIsNotNone(article_id, 'There must be an insert id')
        article = TestDb.db.get_article_by_title(title)
        self.assertArticle(article, title, body, tag_list)

    def test_get_article_list(self):
        # insert 3 articles
        titles = ['test_get_article_list1 title', 'test_get_article_list2 title', 'test_get_article_list3']
        body = ['body1 test_get_article_list1', 'body test_get_article_list2', 'body test_get_article_list3']
        tag_list = ['tag1', 'tag2', 'tag3', 'tag4']
        for idx, obj in enumerate(zip(titles, body)):
            ins_title, ins_body = obj
            TestDb.db.insert_article(ins_title, ins_body, tag_list[:idx + 2])

        # get all articles from DB
        article_list = TestDb.db.get_article_list(None, None)

        # there must be at least 3 articles
        self.assertIsNotNone(article_list)
        self.assertGreater(len(article_list), 2)

        # check if our articles are in the result
        for check_title, check_body in zip(titles, body):
            article = next((t for t in article_list if t.title == check_title), None)
            self.assertArticle(article, check_title, check_body, None)

        # search for article by a substring in the title
        article_list = TestDb.db.get_article_list(title='list2', body=None)
        self.assertIsNotNone(article_list)

        # there must be only one article in the result
        self.assertEqual(len(article_list), 1)
        self.assertArticle(article_list[0], titles[1], body[1], tag_list[:3])

        # search for article by a substring in the title and in the body
        article_list = TestDb.db.get_article_list(title='title', body='body1')
        self.assertIsNotNone(article_list)

        # there must be only one article in the result
        self.assertEqual(len(article_list), 1)
        self.assertArticle(article_list[0], titles[0], body[0], tag_list[:2])

        # search of non-existing article
        article_list = TestDb.db.get_article_list(title='None-existing', body=None)

        # the result must be an empty list
        self.assertEqual(len(article_list), 0)

        # check that escaping works
        article_list = TestDb.db.get_article_list(title='%_', body=None)
        self.assertEqual(len(article_list), 0)
        article_list = TestDb.db.get_article_list(title='%', body=None)
        self.assertEqual(len(article_list), 0)
        article_list = TestDb.db.get_article_list(title='__', body=None)
        self.assertEqual(len(article_list), 0)

        # search by a list of tags

        article_list = TestDb.db.get_article_list(None, None, ['tag1', 'tag2', 'tag3', 'tag4'])
        self.assertIsNotNone(article_list)
        self.assertEqual(len(article_list), 1)
        self.assertArticle(article_list[0], titles[2], body[2], tag_list[:4])

        article_list = TestDb.db.get_article_list(None, None, ['tag1', 'tag3'])
        self.assertIsNotNone(article_list)
        self.assertEqual(len(article_list), 2)

    def test_get_related(self):
        # insert 5 articles
        titles = []
        body_list = []
        for i in range(5):
            titles.append(f'test_get_related{i} title')
            body_list.append(f'body test_get_related{i}')

        tag_list_list = [
            ['rtag1', 'rtag2'],
            ['rtag2', 'rtag3', 'rtag4'],
            ['rtag1', 'rtag3', 'rtag4'],
            ['rtag10'],
            ['rtag1', 'rtag4']
        ]
        last_id = 0
        for title, body, tag_list in zip(titles, body_list, tag_list_list):
            second_to_last_id = last_id
            last_id = TestDb.db.insert_article(title, body, tag_list)

        # get the list of related article for the last (5th) article
        related_list = TestDb.db.get_related(last_id, 10)

        # our id must not be in the result set
        self.assertFalse(any(a.id == last_id for a in related_list))

        # article with tag 'rtag10' must not be in the result set
        self.assertFalse(any(a.id == second_to_last_id for a in related_list))

        # the 3rd article must be the best match
        self.assertArticle(related_list[0], titles[2], body_list[2], tag_list_list[2])

    @classmethod
    def setUpClass(cls):
        cls.db = db.DB(is_test=True)

    @classmethod
    def tearDownClass(cls):
        cls.db.drop_all()
