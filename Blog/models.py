from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="blogs")

    # def __repr__(self):
    #     return "<User(name='%s', fullname='%s', nickname='%s')>" % (
    #         self.name, self.fullname, self.nickname)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    blogs = relationship("Post", back_populates="creator")
