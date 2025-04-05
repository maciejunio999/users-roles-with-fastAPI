from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint


user_role_association = Table('user_role_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

user_pilot_association = Table('user_pilot_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('pilot_id', Integer, ForeignKey('pilots.id'))
)

user_product_association = Table('user_product_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
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

module_endpoint_association = Table('module_endpoint_association', Base.metadata,
    Column('module_id', Integer, ForeignKey('modules.id')),
    Column('endpoint_id', Integer, ForeignKey('endpoints.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    roles = relationship('Role', secondary=user_role_association, back_populates='users', cascade="all, delete")
    pilots = relationship('Pilot', secondary=user_pilot_association, back_populates='users', cascade="all, delete")
    products = relationship('Product', secondary=user_product_association, back_populates='users', cascade="all, delete")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    description = Column(String, unique=True, nullable=False)
    users = relationship('User', secondary=user_role_association, back_populates='roles', cascade="all, delete")
    pilots = relationship('Pilot', secondary=role_pilot_association, back_populates='roles', cascade="all, delete")

class Pilot(Base):
    __tablename__ = 'pilots'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    state = Column(Boolean, unique=False, default=False, nullable=False)
    description = Column(String, unique=True, nullable=False)
    roles = relationship('Role', secondary=role_pilot_association, back_populates='pilots', cascade="all, delete")
    users = relationship('User', secondary=user_pilot_association, back_populates='pilots', cascade="all, delete")
    modules = relationship('Module', secondary=module_pilot_association, back_populates='pilots', cascade="all, delete")

class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, unique=True, nullable=False)
    in_config = Column(Boolean, unique=False, default=False, nullable=False)
    pilots = relationship('Pilot', secondary=module_pilot_association, back_populates='modules', cascade="all, delete")
    endpoints = relationship('Endpoint', secondary=module_endpoint_association, back_populates='modules', cascade="all, delete") 

class Endpoint(Base):
    __tablename__ = 'endpoints'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    description = Column(String, nullable=False)
    modules = relationship('Module', secondary=module_endpoint_association, back_populates='endpoints', cascade="all, delete")
    http_method = Column(String, default='_None', nullable=True)
    __table_args__ = (
        CheckConstraint("http_method IN ('_None', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE')", name='valid_http_method'),
    )

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    state = Column(Boolean, unique=False, default=False, nullable=False)
    users = relationship('User', secondary=user_product_association, back_populates='products', cascade="all, delete")