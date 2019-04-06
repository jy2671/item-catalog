#!/usr/bin/env python

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, ListItem, User

# New imports for Oauth
from flask import session as login_session
import random
import string

# Imports for GConnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///categoryitem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a state token to prevent request forgery
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Connect to Google singin
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 50px; height: 50px;border-radius: 25px;"'
    '"-webkit-border-radius: 25px;-moz-border-radius: 25px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response
        (json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?'
    'token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)

        # jy2671 3/31/19
        # response.headers['Content-Type'] = 'application/json'
        # return response

        flash("You have successfully been logged out.", 'success')
        return redirect(url_for('home'))
    else:
        response = make_response
        (json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to show Catalog information
@app.route('/api/catalog.json')
def showCatalogJSON():
    session = DBSession()
    items = session.query(ListItem).order_by(ListItem.name)
    return jsonify(categories=[i.serialize for i in items])


# JSON for Category
@app.route('/api/category/JSON')
def categoriesJSON():
    session = DBSession()
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# JSON for Category List
@app.route('/api/category/<int:cat_id>/list/JSON')
def categoryListJSON(cat_id):
    session = DBSession()
    category = session.query(Category).filter_by(id=cat_id).one()
    items = session.query(ListItem).filter_by(
        cat_id=cat_id).all()
    return jsonify(Items=[i.serialize for i in items])


# JSON for Category List Item
@app.route('/api/category/<int:cat_id>/list/<int:list_id>/JSON')
def listItemJSON(cat_id, list_id):
    session = DBSession()
    List_Item = session.query(ListItem).filter_by(id=list_id).one()
    return jsonify(List_Item=List_Item.serialize)


# Render homepage
@app.route('/')
@app.route('/home')
@app.route('/catalog')
def home():
    session = DBSession()
    categories = session.query(Category).order_by(Category.name)
    # Pass to template, 5 items most recent items
    latest_items = session.query(ListItem).order_by(ListItem.id)[0:12]

    if 'username' not in login_session:
        return render_template('publicCatalog.html',
                               categories=categories,
                               items=latest_items)
    else:
        return render_template('home.html',
                               categories=categories,
                               items=latest_items)


# Show all categories
@app.route('/catalog/<category>')
def showCategories(category):
    session = DBSession()
    cat_id = (session.query(Category).filter_by(name=category).one()).id
    items = session.query(ListItem).filter_by(cat_id=cat_id).all()
    list = session.query(Category).order_by(Category.name)
    return render_template('category.html', items=items,
                           category=category, allCategories=list)


# Show a category list
@app.route('/catalog/<category>/<item>/')
@app.route('/<category>/<item>/')
def showList(category, item):
    session = DBSession()
    item = session.query(ListItem).filter_by(name=item).one()

    if 'username' not in login_session:
        return render_template('publicList.html',
                               category=item.category, item=item)
    else:
        return render_template('list.html',
                               category=item.category, item=item)


# Create a new list item
@app.route('/catalog/new', methods=['GET', 'POST'])
def newListItem():
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        cat_id = session.query(Category).filter_by(
                 name=request.form['category']).one().id
        newItem = ListItem(name=request.form['name'],
                           description=request.form['description'],
                           user_id=login_session['user_id'],
                           cat_id=cat_id)
        session.add(newItem)
        session.commit()
        flash("Added the new item {}".format(newItem.name))
        return redirect(url_for('home'))
    else:
        categoryNames = [cat.name for cat in session.query(Category).all()]
        return render_template('newListItem.html', categoryList=categoryNames)


# Edit a list item
@app.route('/catalog/<categoryName>/<itemName>/edit',
           methods=['GET', 'POST'])
def editListItem(categoryName, itemName):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    itemToEdit = session.query(ListItem).filter_by(name=itemName).one()
    if login_session['user_id'] != itemToEdit.user_id:
        flash("You don't have authority to edit the item {}"
              .format(itemToEdit.name) + ". Only the item owner can edit it.")
        return redirect('/home')

    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        if request.form['category']:
            new_cat_id = session.query(Category).filter_by(
                         name=request.form['category']).one().id
            itemToEdit.cat_id = new_cat_id
        session.add(itemToEdit)
        session.commit()
        flash("Edited item {}".format(itemToEdit.name))
        return redirect(url_for('home'))
    else:
        itemDescription = session.query(ListItem).filter_by(
                          name=itemName).one().description
        categoryNames = [cat.name for cat in session.query(Category).all()]
        return render_template('editListItem.html', categoryName=categoryName,
                               item=itemName, categoryList=categoryNames,
                               itemDescription=itemDescription)


# Delete a list item
@app.route('/catalog/<categoryName>/<itemName>/delete',
           methods=['GET', 'POST'])
def deleteListItem(categoryName, itemName):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(ListItem).filter_by(name=itemName).one()
    if login_session['user_id'] != itemToDelete.user_id:
        flash("You don't have authority to delete the item {}"
              .format(itemToDelete.name) +
              ". Only the item owner can delete it.")
        return redirect('/home')
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Deleted item {}".format(itemToDelete.name))
        return redirect(url_for('home'))
    else:
        categoryNames = [cat.name for cat in session.query(Category).all()]
        return render_template('deleteListItem.html',
                               categoryName=categoryName,
                               item=itemName,
                               catgegoryList=categoryNames)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
