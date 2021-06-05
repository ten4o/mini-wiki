from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import array_agg

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey, Table

from distutils.util import strtobool
from os import environ


MAX_TITLE_SIZE = 256
MAX_TAG_SIZE = 32

Base = declarative_base()

article_tag_table = Table('article_tag', Base.metadata,
                          Column('article_id', Integer, ForeignKey('article.id')),
                          Column('tag_id', Integer, ForeignKey('tag.id'))
                          )


class Article(Base):
    """DB model of table article"""

    __tablename__ = 'article'
    id = Column(Integer, Sequence('article_id_seq'), primary_key=True)
    title = Column(String(MAX_TITLE_SIZE), unique=True)
    body = Column(String)
    tags = relationship("Tag", secondary=article_tag_table,  lazy='joined')

    def __init__(self, title, body):
        super().__init__()
        self.title = title
        self.body = body

    def __repr__(self):
        tag_list = '[{}]'.format(','.join([tag.name for tag in self.tags]))
        return f'Article(id:{self.id} title:"{self.title}" body:"{self.body[:10]}" [{len(self.tags)}] {tag_list})'

    @classmethod
    def create(cls, aid: int, title: str, body: str, tag_name_list: list[str]):
        a = cls(title=title, body=body)
        a.id = aid
        a.tags = [Tag(name) for name in tag_name_list]
        return a


class Tag(Base):
    """DB model of table tag"""

    __tablename__ = 'tag'
    id = Column(Integer, Sequence('tag_id_seq'), primary_key=True)
    name = Column(String(MAX_TAG_SIZE), unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f'Tag(id:{self.id}  name:{self.name})'


class DuplicateTitleException(Exception):
    pass


class DB:
    def __init__(self, is_test: bool = False):
        db_url = environ.get('DATABASE_URL')
        if is_test:
            db_url += '_TEST'

        db_trace_on = environ.get('DATABASE_TRACE_ON')
        db_echo = db_trace_on is not None and strtobool(db_trace_on)
        self.engine = create_engine(db_url, echo=db_echo)
        Base.metadata.create_all(self.engine)

        # we want intarray extension due to its operator & between arrays
        with Session(self.engine) as session:
            session.execute('CREATE EXTENSION IF NOT EXISTS intarray;')
            session.commit()

    def drop_all(self):
        """Drops all DB tables"""
        Base.metadata.drop_all(self.engine)

    def insert_article(self, title: str, body: str, tag_list: list[str]) -> int:
        """Inserts an article into the DB

        Args:
            title(str): The title of the article
            body(str): The contents of the article in markdown format
            tag_list(list[str]): list of tags associated with this article

        Returns:
            int: id of the article returned from the DB
        """
        if len(title) > MAX_TITLE_SIZE:
            raise ValueError('title is too long')

        for tag in tag_list:
            if len(tag) > MAX_TAG_SIZE:
                raise ValueError('tag name is too long')

        try:
            with Session(self.engine) as session:
                article = Article(title, body)
                db_tags = {tag.name: tag for tag in session.query(
                    Tag).filter(Tag.name.in_(tag_list)).all()}
                db_tags.update({tag_name: Tag(tag_name)
                                for tag_name in tag_list if tag_name not in db_tags})
                article.tags.extend(db_tags.values())
                session.add(article)
                session.commit()
                return article.id
        except IntegrityError:
            raise DuplicateTitleException

    def get_article_by_id(self, article_id: int) -> Article:
        """Search an article by DB id

        Args:
            article_id(int): The id of the article

        Returns:
            Article: object that contains id, title, body and list of tags or None if not found
        """
        with Session(self.engine) as session:
            article = session.query(Article).filter(Article.id == article_id).first()
            return article

    def get_article_by_title(self, title: str) -> Article:
        """Search an article by title

        Args:
            title(str): The title of the article

        Returns:
            Article: object that contains id, title, body and list of tags or None if not found
        """
        with Session(self.engine) as session:
            return session.query(Article).filter(Article.title == title).first()

    def get_article_list(self, title: str, body: str, tag_list: list[str] = None) -> list[Article]:
        """Search articles by substring in the title and/or substring in the body
           and/or if a supplied list of tags is a subset of the article's tags

        Args:
            title(str): a substring to search for in the title (Node: whitespace is not considered)
            body(str): a substring to search for in the body
            tag_list(list[str]): list of tag names to search for

        Returns:
            list[Article]: list of article objects or [] if nothing found
        """
        with Session(self.engine) as session:
            criterion = []
            if title:
                criterion.append(func.lower(Article.title).contains(title.lower(), autoescape=True))
            if body:
                criterion.append(func.lower(Article.body).contains(body.lower(), autoescape=True))
            if tag_list:
                #
                # match at least one tag
                #
                # return session.query(Article).join(Article.tags).filter(Tag.name.in_(tag_list)).all()

                #
                # match all tags
                #

                # make an array containing the ids of the tags in tag_list
                query_tag_id_list = session.query(array_agg(Tag.id)).filter(Tag.name.in_(tag_list))

                # subquery with two columns: article id , all its tag ids in an array
                article_all_tags = select([
                    Article.id.label('article_id'),
                    array_agg(Tag.id).label('tagid_list')
                ]).join(Article.tags).group_by(Article.id).alias('article_all_tags')

                # check that the list of tags that we search for is a subset of the list of tags of the article
                criterion.append(
                    article_all_tags.c.tagid_list.contains(query_tag_id_list.scalar_subquery()))

                return session.query(Article).join(article_all_tags, article_all_tags.c.article_id == Article.id
                                                   ).filter(*criterion).all()
            # implicit else
            return session.query(Article).filter(*criterion).all()

    def get_related(self, article_id: int, max_num: int) -> list[Article]:
        """Gets a list of related articles.

        A related article is one that has at least one common tag with the specified article.
        The result is a list of `Articles` sorted by the number of matches/hits.

        Args:
            article_id(int): the id of the specified article

        Returns:
            list[Article]: list of `Articles` sorted by the number of matches/hits or an empty list
        """

        # The following query is PostgreSQL specific. It uses operatar & from intarray extension.
        #
        query = r'''
            SELECT article.id, article.title, article.body, tag_name_list
            FROM article INNER JOIN (
                SELECT article_id,
                        COALESCE(ARRAY_LENGTH(tag_list & ( SELECT array_agg(tag_id) FROM article_tag WHERE article_id = :article_id), 1), 0) AS jaccard_index,
                        tag_name_list
                FROM (
                        SELECT article_id, array_agg(tag_id ORDER BY tag_id) AS tag_list
                                , array_agg(name ORDER BY name) AS tag_name_list
                        FROM article_tag INNER JOIN tag ON tag.id = tag_id
                        GROUP BY article_id
                        HAVING article_id <> :article_id
                    ) subquery1
                ORDER BY jaccard_index DESC
                LIMIT :max_num
            ) subquery2
            ON (article.id = article_id)
            WHERE jaccard_index <> 0
            ORDER BY jaccard_index DESC;
        '''
        article_list = []
        with Session(self.engine) as session:
            db_result = session.execute(query, {'article_id': article_id, 'max_num': max_num})

            # convert the result set to a list of Article objects
            for row in db_result:
                a = Article.create(aid=row[0], title=row[1], body=row[2], tag_name_list=row[3])
                article_list.append(a)

        return article_list
