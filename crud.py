from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from models import Base
from models import Book
import yaml

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


book = Book(
    title='Deep Learning',
    author='Ian Goodfellow',
    pages=775,
    published=datetime(2016, 11, 18)
)

Session.close_all_sessions()
recreate_database()
s = Session()
s.add(book)
s.commit()

for data in yaml.load_all(open('books.yaml')):
    book = Book(**data)
    s.add(book)

s.commit()

print(s.query(Book).all())