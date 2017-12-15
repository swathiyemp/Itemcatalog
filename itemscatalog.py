from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import desc

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, cascade="save-update" )

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, cascade="all, single_parent=True")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, cascade="save-update")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Description(Base):
    __tablename__ = 'description'

    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    items_id = Column(Integer, ForeignKey('items.id'))
    items = relationship(Items, cascade="all, single_parent=True")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, cascade="save-update")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'content': self.content,

        }
engine = create_engine("postgresql://catalog:topsecret@localhost/catalogdb")

Base.metadata.create_all(engine)
