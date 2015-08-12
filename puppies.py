from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Table
 
Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximum_capacity = Column(Integer)
    current_occupancy = Column(Integer)

association_table = Table('association', Base.metadata,
    Column('puppy_id', Integer, ForeignKey('puppy.id')),
    Column('adopter_id', Integer, ForeignKey('adopter.id'))
)
 
class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))
    adopter = relationship('Adopter', secondary=association_table)
    profile = relationship("Profile", uselist=False, backref="puppy")
    

class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key = True)
    url = Column(String)
    desc = Column(String)
    special_needs = Column(String)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))


class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable=False)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))

engine = create_engine('sqlite:///puppyshelter2.db')
Base.metadata.create_all(engine)