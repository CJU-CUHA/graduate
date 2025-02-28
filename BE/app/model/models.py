from sqlalchemy import Column, Integer, String, DateTime,func,LargeBinary,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    username = Column("username",String(255), index=True)
    email    = Column("email",String(255), index=True)
    password = Column("password",String(255), index=True)

class Case(Base):
    __tablename__ = 'cases'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    case_name = Column("case_name",String(255), index=True)
    case_info = Column("case_info",String(255), index=True)
    case_type = Column("case_type",String(255), index=True)
    case_owner = Column("case_owner",String(255), index=True)
    created_at = Column(DateTime,func,index=True)
    # files = relationship("File",back_populates="case")

class File(Base):
    __tablename__='files'
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    pc_name=Column("pc_name",String(255),index=True)
    file_path=Column("file_path",String(255))
    # case = relationship("Case",back_populates="files")
    # case_id = Column(Integer, ForeignKey('cases.id'))
