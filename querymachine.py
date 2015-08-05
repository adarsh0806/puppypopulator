#!/usr/bin/python
# -*- mode: python -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy.orm import relationship, backref
from sqlalchemy import asc
from datetime import date, datetime, timedelta
import datetime

engine = create_engine('sqlite:///puppyshelter1.db', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)


class Shelter(Base):
    __table__ = Base.metadata.tables['shelter']

class Puppy(Base):
	__table__ = Base.metadata.tables['puppy']

class Profile(Base):
	__table__ = Base.metadata.tables['profile']

class Adopter(Base):
	__table__ = Base.metadata.tables['adopter']

'''
Create a function to check a puppy into a shelter, 
if the shelter is at capacity, 
prompt the user to try a different shelter.
'''

def checkin(num_pup, shel_cap):
	db_session = scoped_session(sessionmaker(bind=engine))
	
	stmt1 = db_session.query(Shelter.maximum_capacity).filter_by(name = shel_cap)
	val1, val2 = 0, 0 
	for item in stmt1:
		val1 = item[0]
	print "maximum_capacity: ", val1
	stmt2 = db_session.query(Shelter.current_occupancy).filter_by(name = shel_cap)
	for item in stmt2:
		val2 = item[0]
	print "current_occupancy: ",val2
	
	available = val1 - val2
	print "available = ",available
	print "Puppies requested to have admitted = ", num_pup
	
	if num_pup > available:
		print "Shelter does not have capacity, please choose another shelter."
	else:
		print "Shelter will take these puppies, thank you!"

if __name__ == '__main__':
    db_session = scoped_session(sessionmaker(bind=engine))
    checkin(15, 'Palo Alto Humane Society')
    # for item in db_session.query(Puppy.id):
    #     print item
    #1. Query all of the puppies and return the results in ascending alphabetical order
    stmt = db_session.query(Puppy).order_by(Puppy.name.asc())
    # for item in stmt:
    # 	print item.name
    
    #2. Query all of the puppies that are less than 6 months old organized by the youngest first
    today = datetime.date.today()
    stmt = db_session.query(Puppy.name,Puppy.dateOfBirth).order_by(Puppy.dateOfBirth.asc())
    # for item in stmt:
    # 	diff = today - item[1]
    # 	if (diff.total_seconds()*0.0000115741) < 180:
    # 		print item[1]		
    
    #3. Query all puppies by ascending weight
    stmt = db_session.query(Puppy.name).order_by(Puppy.weight.asc())
    # for item in stmt:
    # 	print item
    
    #4. Query all puppies grouped by the shelter in which they are staying
    stmt = db_session.query(Puppy).filter_by(shelter_id = Shelter.id)
    for item in stmt:
    	# print item.name
    	pass

   	#query the profiles
   	# stmt = db_session.query(Profile.url, Profile.puppy_id)
   	# for item in stmt:
   	# 	print "Profiles:", item

   	#query the adopters
   	stmt = db_session.query(Adopter.name, Adopter.puppy_id)
   	# for item in stmt:
   	# 	print "Adopter:", item

   	#shelter capacity
   	stmt = db_session.query(Shelter.name, Shelter.maximum_capacity)
   	# for item in stmt:
   	# 	print 'Shelter capacity:', item


   	
   	
