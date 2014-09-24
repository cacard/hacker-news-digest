import os
import logging
import psycopg2
import psycopg2.extras
import urlparse

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (
        create_engine, 
        Table, Column, Integer, String, MetaData, ForeignKey
    )

logger = logging.getLogger(__name__)

schemes = [
"""
create table if not exists image(
    id text not null primary key,
    content_type varchar(20),
    raw_data bytea
);
""", """
create table if not exists hackernews(
    rank int,
    title text,
    url text primary key,
    comhead text,
    score int,
    author text,
    author_link text,
    submit_time text,
    comment_cnt int,
    comment_url text,
    summary text,
    img_id text,
    constraint image_delete
        foreign key(img_id) references image(id)
        on delete cascade
);
""", """
create table if not exists startupnews(
    rank int,
    title text,
    url text primary key,
    comhead text,
    score int,
    author text,
    author_link text,
    submit_time text,
    comment_cnt int,
    comment_url text,
    summary text,
    img_id text,
    constraint image_delete
        foreign key(img_id) references image(id)
        on delete cascade
);
"""
]
# Receive unicode strings
# see http://initd.org/psycopg/docs/faq.html#problems-with-type-conversions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

engine = create_engine(os.environ.get("DATABASE_URL", 
    'postgres://postgres@localhost:5432/postgres')\
            .replace('postgres://', 'postgresql://'), pool_size=10, max_overflow=10)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

Base = declarative_base()

class HackerNewsTable(Base):
    __tablename__ = 'hackernews'

    rank = Column(Integer)
    title = Column(String)
    url = Column(String, primary_key=True)
    comhead = Column(String)
    score = Column(Integer)
    author = Column(String)
    author_link = Column(String)
    submit_time = Column(String)
    comment_cnt = Column(Integer)
    comment_url = Column(String)
    summary = Column(String)
    img_id = Column(String)

    def __repr__(self):
        return u"%s<%s>" % (self.title, self.url)

# class StartupNewsTable(HackerNewsTable):
#     __tablename__ = 'startupnews'

print session.query(HackerNewsTable).first()

def sync_db():
    Base.metadata.create_all(engine)

# urlparse.uses_netloc.append("postgres")
# url = urlparse.urlparse(os.environ.get("DATABASE_URL", 
#         'postgress://postgres:@localhost:5432/postgres'))
# conn = psycopg2.connect(
#     database=url.path[1:],
#     user=url.username,
#     password=url.password,
#     host=url.hostname,
#     port=url.port
# )
# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
# for scheme_sql in schemes:
#     cur.execute(scheme_sql)
# conn.commit()
# 
# class Storage(object):
# 
#     def exist(self, **kwargs):
#         k, v = kwargs.items()[0]
#         cur.execute('select * from %s where %s=%s' % (self.table_name, k, '%s'), (v,))
#         return cur.fetchone()
# 
#     get = exist
# 
#     def put(self, **kwargs):
#         # To ensure their sequence
#         keys = map(lambda i: i[0], kwargs.items())
#         values = map(lambda i: i[1], kwargs.items())
#         try:
#             cur.execute('insert into %s(%s) values(%s)' % (
#                     self.table_name, ', '.join(keys),
#                     ', '.join(('%s',)*len(kwargs))), values)
#             conn.commit()
#         # except psycopg2.IntegrityError as e:
#         except psycopg2.DatabaseError as e:
#             logger.info('Failed to save %s, %s', kwargs[self.pk], e)
#             conn.rollback()
#     def update(self, pk, **kwargs):
#         try:
#             cur.execute('update %s set %s where %s' % (self.table_name,
#                 ', '.join(map(lambda k: k+'=%s', kwargs.keys())),
#                 self.pk+'=%s'), kwargs.values()+[pk])
#             conn.commit()
#         except psycopg2.DatabaseError as e:
#             logger.info('Failed to update %s(%s), %s', self.table_name, pk, e)
#             conn.rollback()
# 
#     def delete(self, **kwargs):
#         k, v = kwargs.items()[0]
#         try:
#             cur.execute('delete from %s where %s=%s' % (self.table_name, k, '%s'), (v,))
#             conn.commit()
#         except psycopg2.DatabaseError as e:
#             logger.info('Failed to delete %s(%s), %s', self.table_name, kwargs[self.pk], e)
#             conn.rollback()
# 
# class ImageStorage(Storage):
#     table_name = 'image'
#     pk = 'id'
# 
#     def put(self, **kwargs):
#         if 'raw_data' in kwargs:
#             kwargs['raw_data'] = psycopg2.Binary(kwargs['raw_data'])
#         return super(ImageStorage, self).put(**kwargs)
#     
# 
# class HnStorage(Storage):
#     table_name = 'hackernews'
#     pk = 'url'
# 
#     def get_all(self):
#         cur.execute('select * from %s order by rank' % self.table_name)
#         return cur.fetchall()
# 
# class SnStorage(HnStorage):
#     table_name = 'startupnews'
#     pk = 'url'

if __name__ == '__main__':
    sync_db()
