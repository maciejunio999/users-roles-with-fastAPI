from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


user_role_association = Table('user_role_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    roles = relationship('Role', secondary=user_role_association, back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    users = relationship('User', secondary=user_role_association, back_populates='roles')