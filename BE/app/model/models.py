from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), index=True)
    email = Column(String(255), index=True)
    password = Column(String(255), index=True)

    cases = relationship("Case", back_populates="case_owner")

class Case(Base):
    __tablename__ = 'cases'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_name = Column(String(255), index=True)
    case_info = Column(String(255), index=True)
    case_type = Column(String(255), index=True)
    case_owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now, index=True)

    case_owner = relationship("User", back_populates="cases")
    logs = relationship("Logs", back_populates="case")
    files = relationship("File", back_populates="cases")

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pc_name = Column(String(255), index=True)
    file_path = Column(String(255))
    case_id = Column(Integer, ForeignKey('cases.id'))

    cases = relationship("Case", back_populates="files")

class Logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    alias = Column(String(255), index=True)
    event_id = Column(Integer)
    timestamp = Column(DateTime, default=func.now)
    channel = Column(String(255))
    event_data = Column(JSON)
    computer = Column(String(255))

    case = relationship("Case", back_populates="logs")
