# Every model represents a table in database
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from .database import Base


class Posts(Base):

    __tablename__ = "posts"

    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User") # Helps us to provide information about user who created a post


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Votes(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True)
