from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Column,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship,sessionmaker,scoped_session
import os


BASE_DIR=os.path.dirname(os.path.realpath(__file__))

connection_str= "sqlite:///" + os.path.join(BASE_DIR,'posts.db')

Base=declarative_base()


engine=create_engine(connection_str,echo=True)


session=scoped_session(
    sessionmaker(bind=engine)
)

Base.query = session.query_property()



class User(Base):
    __tablename__="users"
    id = Column(String(), primary_key=True)
    ids=Column(String())
    username=Column(String(45),nullable=False)
    email=Column(String(80),nullable=False)
    password  = Column(String(80),nullable=False)
    todo=relationship("Todo",backref="author")


    def __repr__(self):
        return f"<User {self.username}>"


class Todo(Base):
    __tablename__="posts"
    ids = Column(Integer(), primary_key=True)
    id=Column(Integer())
    title=Column(String(),nullable=False)
    content=Column(Text(),nullable=False)
    date = Column(Text(),nullable=False)
    time = Column(Text(),nullable=False)
    status = Column(Text(),nullable=False)
    user_id=Column(String(),ForeignKey("users.id"))

    def __repr__(self):
        return f"<User {self.title}>"