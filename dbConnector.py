import nGram as ng
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import Table, Column, Integer, String, MetaData

# setup for the ngrams table in sqlite3, runs only if ngrams.db not setup yet


def get_session(filename="ngrams.db"):
    engine = create_engine("sqlite:///%s" % filename)
    metadata = MetaData()

    # runs only if the db file does not exist
    ngrams = Table('ngrams', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('prev_words', String),
                   Column('next_word', String),
                   Column('count', Integer),
                   Column('size', Integer)
                   )
    metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)

    mapper(ng.nGram, ngrams)

    return Session
