#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, ListItem, User

# Load data from JSON
import json

engine = create_engine('sqlite:///categoryitem.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


def generateData():
    session = DBSession()
    session.execute('''DELETE FROM category''')
    session.execute('''DELETE FROM list_item''')
    session.execute('''DELETE FROM user''')
    session.commit()
    session.close()

    # Create a dummy user
    User1 = User(name="Robo Barista",
                 email="tinnyTime@udacity.com",
                 picture='https://pbs.twimg.com/profile_images/2671170543/'
                 '18debd694829ed78203a5a36dd364160_400x400.png')
    session.add(User1)
    session.commit()

    # Read JSON
    with open('json_data/category.json') as d:
        categories = json.load(d)
        for category in categories:
            session.add(Category(name=category['name'],
                                 user=User1))
            session.commit()

    with open('json_data/list_item.json') as d:
        items = json.load(d)
        for item in items:
            category = session.query(Category).filter_by(
                       name=item['category']).one()
            session.add(ListItem(name=item['name'],
                                 description=item['description'],
                                 category=category,
                                 user=User1))
            session.commit()

    print("Category added: %s" % session.query(Category).count())
    print("ListItem added: %s" % session.query(ListItem).count())


if __name__ == '__main__':
    generateData()
