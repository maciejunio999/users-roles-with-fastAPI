from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


user_role_association = Table('user_role_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

user_pilot_association = Table('user_pilot_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('pilot_id', Integer, ForeignKey('pilots.id'))
)

role_pilot_association = Table('role_pilot_association', Base.metadata,
    Column('pilot_id', Integer, ForeignKey('pilots.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    roles = relationship('Role', secondary=user_role_association, back_populates='users')
    pilots = relationship('Pilot', secondary=user_pilot_association, back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    users = relationship('User', secondary=user_role_association, back_populates='roles')
    pilots = relationship('Pilot', secondary=role_pilot_association, back_populates='roles')

class Pilot(Base):
    __tablename__ = 'pilots'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    roles = relationship('Role', secondary=role_pilot_association, back_populates='pilots')
    users = relationship('User', secondary=user_pilot_association, back_populates='pilots')