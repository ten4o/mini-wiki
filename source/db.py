from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey, Table

from os import environ

MAX_TITLE_SIZE = 256
MAX_TAG_SIZE = 32

Base = declarative_base()

topic_tag_table = Table('topic_tag', Base.metadata,
                        Column('topic_id', Integer, ForeignKey('topic.id')),
                        Column('tag_id', Integer, ForeignKey('tag.id'))
                        )


class Topic(Base):
    """DB model of table topic"""

    __tablename__ = 'topic'
    id = Column(Integer, Sequence('topic_id_seq'), primary_key=True)
    title = Column(String(MAX_TITLE_SIZE), unique=True)
    body = Column(String)
    tags = relationship("Tag", secondary=topic_tag_table,  lazy='joined')

    def __init__(self, title, body):
        super().__init__()
        self.title = title
        self.body = body

    def __repr__(self):
        tag_list = '[{}]'.format(','.join([tag.name for tag in self.tags]))
        return f'Topic(id:{self.id} title:{self.title} [{len(self.tags)}] {tag_list})'


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


class DB:
    def __init__(self, is_test: bool = False):
        db_url = environ.get('DATABASE_URL')
        if is_test:
            db_url += '_TEST'

        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        """Drops all DB tables"""
        Base.metadata.drop_all(self.engine)

    def insert_topic(self, title: str, body: str, tag_list: list[str]) -> int:
        """Inserts a topic into the DB

        Args:
            title(str): The title of the topic
            body(str): The contents of the topic in markdown format
            tag_list(list[str]): list of tags associated with this topic

        Returns:
            int: id of the topic returned from the DB
        """
        if len(title) > MAX_TITLE_SIZE:
            raise ValueError('title is too long')

        for tag in tag_list:
            if len(tag) > MAX_TAG_SIZE:
                raise ValueError('tag name is too long')

        with Session(self.engine) as session:
            topic = Topic(title, body)
            db_tags = {tag.name: tag for tag in session.query(
                Tag).filter(Tag.name.in_(tag_list)).all()}
            db_tags.update({tag_name: Tag(tag_name)
                           for tag_name in tag_list if tag_name not in db_tags})
            topic.tags.extend(db_tags.values())
            session.add(topic)
            session.commit()
            return topic.id

    def get_topic_by_id(self, topic_id: int) -> Topic:
        """Search a topic by DB id

        Args:
            topic_id(int): The id of the topic

        Returns:
            Topic: object that contains id, title, body and list of tags or None if not found
        """
        with Session(self.engine) as session:
            topic = session.query(Topic).filter(Topic.id == topic_id).first()
            return topic

    def get_topic_by_title(self, title: str) -> Topic:
        """Search a topic by title

        Args:
            title(str): The title of the topic

        Returns:
            Topic: object that contains id, title, body and list of tags or None if not found
        """
        with Session(self.engine) as session:
            return session.query(Topic).filter(Topic.title == title).first()
