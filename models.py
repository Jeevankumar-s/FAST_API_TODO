from sqlalchemy import Column, Integer, String, Boolean;
from database import Base;

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True);
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
     

class User(Base):
    __tablename__ = "user"
    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, nullable=False)
    password = Column(String, nullable=False)

