from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, jsonify
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from itemscatalog import Base, Category, Items, Description, User
from flask import session as login_session
from flask import make_response
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
     open('/var/www/itemcatalog/itemcatalog/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"

engine = create_engine("postgresql://catalog:topsecret@localhost/catalogdb")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

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
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

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
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print data
    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    return output

# logout Page


@app.route('/logout')
def logout():
    gdisconnect()
    return render_template('logout.html')

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
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
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON API For Category List


@app.route('/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

# JSON API For Items in the Category


@app.route('/categories/<int:category_id>/lists/JSON')
def CategoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    lists = session.query(Items).filter_by(
        category_id=category_id).all()
    return jsonify(CategoryItems=[l.serialize for l in lists])

# JSON API For Items Description


@app.route('/lists/<int:items_id>/descriptions/JSON')
def DescriptionsJSON(items_id):
    items = session.query(Items).filter_by(id=items_id).one()
    description = session.query(Description).filter_by(items_id=items.id).all()
    return jsonify(DescriptionofItems=[d.serialize for d in description])

# Show all categories and latest added items


# Show all categories and latest added items


@app.route('/')
@app.route('/category/')
def categorielist():
    categories = session.query(Category).order_by(asc(Category.name))
    addeditems = session.query(Category).order_by('id desc').limit(10)
    item = session.query(Items).order_by('id desc').limit(10)
    if 'username' not in login_session:
        return render_template('PublicCategories.html', categories=categories,
                               addeditems=addeditems, item=item)
    else:
        return render_template('categories.html', categories=categories,
                               addeditems=addeditems, item=item)

# Create a new Category


@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('categorielist'))
    else:
        return render_template('newCategory.html')

# Edit the Category


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedcategory = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedcategory.user_id != login_session['user_id']:
        flash('You are not authorized to edit.Piease create your own category'
              'to edit')
    return redirect(url_for('categorielist', category_id=category_id))
    if request.method == 'POST':
        if request.form['name']:
            editedcategory.name = request.form['name']
        session.add(editedcategory)
        session.commit()
        flash('Category Successfully Edited %s' % editedcategory.name)
        return redirect(url_for('categorielist', category_id=category_id))
    else:
        return render_template('editCategory.html', category=editedcategory)

# Delete the Category


@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        flash('You are not authorized to delete this category. Please create'
              'your own category in order to delete.')
        return redirect(url_for('categorielist', category_id=category_id))
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        flash('Category Successfully Deleted %s' % categoryToDelete.name)
        return redirect(url_for('categorielist', category_id=category_id))
    else:
        return render_template('deleteCategory.html',
                               category=categoryToDelete)

# Show all items of the category


@app.route('/categories/<int:category_id>/lists')
def itemslist(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    print creator
    lists = session.query(Items).filter_by(category_id=category_id).all()
    if 'username' not in login_session or \
       creator.id != login_session['user_id']:
        print 0
        return render_template('Publiclists.html', lists=lists,
                               category=category, category_id=category_id,
                               creator=creator)
    else:
        print 1
        return render_template('lists.html', lists=lists, category=category,
                               category_id=category_id, creator=creator)

# Add New Item in the category


@app.route('/category/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()

    if login_session['user_id'] != category.user_id:
        flash('You are not authorized to add items to this category. Please'
              'create your own category in order to add items.')
        return redirect(url_for('itemslist', category_id=category_id))
    if request.method == 'POST':
        print request.form
        description_text = request.form['description']
        newItem = Items(name=request.form['name'], category_id=category_id,
                        user_id=category.user_id)
        description = Description(content=description_text, items=newItem,
                                  user_id=category.user_id)
        session.add(newItem)
        session.add(description)
        session.commit()
        return redirect(url_for('itemslist', category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)

# Edit an item in the Category


@app.route('/category/<int:category_id>/lists/<int:lists_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, lists_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Items).filter_by(id=lists_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        flash('You are not authorized to edit items to this category. Please'
              'create your own category in order to edit items.')
        return redirect(url_for('itemslist', category_id=category_id))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        flash('Successfully edited')
        session.commit()
        return redirect(url_for('itemslist', category_id=category_id))
    else:
        return render_template(
            'edititem.html', category_id=category_id, lists_id=lists_id,
            items=editedItem)

# Delete an Item in the Category


@app.route('/category/<int:category_id>/lists/<int:lists_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, lists_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    deletedItem = session.query(Items).filter_by(id=lists_id).one()
    if login_session['user_id'] != category.user_id:
        flash('You are not authorized to delete items in this category. Please'
              'create your own category in order to delete items.')
        return redirect(url_for('itemslist', category_id=category_id))
    if request.method == 'POST':
        session.delete(deletedItem)
        flash('Successfully Deleted')
        session.commit()
        return redirect(url_for('itemslist', category_id=category_id))
    else:
        return render_template(
            'deleteItem.html', category_id=category_id, lists_id=lists_id,
            items=deletedItem)

# Show the Description of the Category


@app.route('/lists/<int:items_id>/descriptions')
def itemdesc(items_id):
    items = session.query(Items).filter_by(id=items_id).one()
    creator = getUserInfo(items.user_id)
    print creator
    description = session.query(Description).filter_by(items_id=items.id).one()
    if 'username' not in login_session or \
       creator.id != login_session['user_id']:
        print 0
        return render_template('publicdescription.html', items=items,
                               description=description, creator=creator)
    else:
        print 1
        return render_template('descriptions.html', items=items,
                               description=description, creator=creator)


# Edit the Description


@app.route('/items/<int:items_id>/descriptions/<int:descriptions_id>/edit',
           methods=['GET', 'POST'])
def editDescription(items_id, descriptions_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedDescription = session.query(
                                      Description).filter_by(
                                      id=descriptions_id).one()
    items = session.query(Items).filter_by(id=items_id).one()
    if login_session['user_id'] != items.user_id:
        flash('You are not authorized to edit items in this category. Please'
              'create your own category in order to edit items.')
        return redirect(url_for('itemdesc', items_id=items.id))
    if request.method == 'POST':
        if request.form['content']:
            editedDescription.content = request.form['content']
        session.add(editedDescription)
        flash('Successfully Edited')
        session.commit()
        return redirect(url_for('itemdesc', items_id=items.id))
    else:
        return render_template(
            'editDescription.html', items=items, description=editedDescription)

# Delete the description


@app.route('/items/<int:items_id>/descriptions/<int:descriptions_id>/delete',
           methods=['GET', 'POST'])
def deleteDescription(items_id, descriptions_id):
    if 'username' not in login_session:
        return redirect('/login')
    items = session.query(Items).filter_by(id=items_id).one()
    deletedDescription = session.query(
                                       Description).filter_by(
                                       id=descriptions_id).one()
    if login_session['user_id'] != items.user_id:
        flash('You are not authorized to delete descriptions in this item.'
              'Please create your own item in order to delete.')
        return redirect(url_for('itemdesc', items_id=items.id))
    if request.method == 'POST':
        session.delete(deletedDescription)
        session.commit()
        return redirect(url_for('itemslist', category_id=items.category_id))
    else:
        return render_template(
            'deleteDescription.html', items=items,
            description=deletedDescription)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
