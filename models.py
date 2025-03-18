from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
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

module_role_association = Table('module_role_association', Base.metadata,
    Column('module_id', Integer, ForeignKey('modules.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

module_pilot_association = Table('module_pilot_association', Base.metadata,
    Column('module_id', Integer, ForeignKey('modules.id')),
    Column('pilot_id', Integer, ForeignKey('pilots.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    roles = relationship('Role', secondary=user_role_association, back_populates='users')
    pilots = relationship('Pilot', secondary=user_pilot_association, back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    users = relationship('User', secondary=user_role_association, back_populates='roles')
    pilots = relationship('Pilot', secondary=role_pilot_association, back_populates='roles')
    modules = relationship('Module', secondary=module_role_association, back_populates='roles')

class Pilot(Base):
    __tablename__ = 'pilots'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    state = Column(Boolean, unique=False, default=False, nullable=False)
    roles = relationship('Role', secondary=role_pilot_association, back_populates='pilots')
    users = relationship('User', secondary=user_pilot_association, back_populates='pilots')
    modules = relationship('Module', secondary=module_pilot_association, back_populates='pilots')

class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, unique=True, nullable=False)
    in_config = Column(Boolean, unique=False, default=False, nullable=False)
    roles = relationship('Role', secondary=module_role_association, back_populates='modules')
    pilots = relationship('Pilot', secondary=module_pilot_association, back_populates='modules')