#!/usr/bin/python
# -*- mode: python -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy.orm import relationship, backref
from sqlalchemy import asc
from datetime import date, datetime, timedelta
import datetime

import os
from flask import Flask, flash, g, jsonify, redirect, render_template,request, session, url_for, request
#from flask.ext.github import GitHub
app = Flask(__name__)

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


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/puppies/<int:puppy_id>/')
def view_puppies(puppy_id):
	#Add a puppy, get info on a puppy, update puppy info , delete puppy
	#view all the puppies
	stmt = db_session.query(Puppy).filter_by(id = puppy_id)
	return render_template('puppies.html', stmt = stmt)
	
@app.route('/puppies/new/', methods = ['GET', 'POST'])
def add_puppy():
	db_session = scoped_session(sessionmaker(bind=engine))
	if request.method == 'POST':
		newPuppy = Puppy(id = request.form['id'], name = request.form['name'],\
			gender = request.form['gender'])
		db_session.add(newPuppy)
		db_session.commit()
		return redirect(url_for('view_puppies', puppy_id = request.form['id']))
	else:
		return render_template('newpuppy.html')
	#return 'Puppy added.'


@app.route('/shelters/<int:shelter_id>/')
def view_shelter(shelter_id):
	stmt = db_session.query(Shelter).filter_by(id = shelter_id)
	return render_template('shelters.html', stmt = stmt)

@app.route('/shelters/new/', methods = ['GET', 'POST'])
def add_shelter():
	db_session = scoped_session(sessionmaker(bind=engine))
	if request.method == 'POST':
		newShelter = Shelter(id = request.form['id'], name = request.form['name'],\
			city = request.form['city'], maximum_capacity = request.form['maximum_capacity'],\
			current_occupancy = request.form['current_occupancy'])
		db_session.add(newShelter)
		db_session.commit()
		return redirect(url_for('view_shelter', shelter_id = request.form['id']))
	else:
		return render_template('newShelter.html')	
	

@app.route('/adopters/<int:adopter_id>/')
def view_adopters(adopter_id):
	stmt = db_session.query(Adopter).filter_by(id = adopter_id)
	return render_template('adopters.html', stmt = stmt)

@app.route('/adopters/new/', methods = ['GET', 'POST'])	
def add_adopter():
	db_session = scoped_session(sessionmaker(bind=engine))
	if request.method == 'POST':
		newAdopter = Adopter(id = request.form['id'], name = request.form['name'])
		db_session.add(newAdopter)
		db_session.commit()
		return redirect(url_for('view_adopters', adopter_id = request.form['id']))
	else:
		return render_template('newAdopter.html')	






if __name__ == '__main__':
    db_session = scoped_session(sessionmaker(bind=engine))
    checkin(15, 'Palo Alto Humane Society')
    # for item in db_session.query(Puppy.id):
    #     print item
    #1. Query all of the puppies and return the results in ascending alphabetical order
    stmt = db_session.query(Puppy).order_by(Puppy.name.asc())
    for item in stmt:
    	print item.name
    
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
   	stmt = db_session.query(Shelter.id,Shelter.name, Shelter.maximum_capacity)
   	# for item in stmt:
   	# 	print 'Shelter capacity:', item
   	app.debug = True
    app.run(host='0.0.0.0', port=8000)

   	
   	
