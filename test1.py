from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from test import Base, Restaurant, MenuItem

print Base
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()
myFirstRestaurant = Restaurant(name="Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

x = session.query(Restaurant.name).all()
for item in x:
	print item