__author__ = 'David'

from flask import Flask, render_template, url_for, flash, request, redirect, \
    jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


#Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'},
               {'name':'Blue Burgers', 'id':'2'},
               {'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [
    {'name':'Cheese Pizza', 'description':'made with fresh cheese',
     'price':'$5.99','course' :'Entree', 'id':'1'},
    {'name':'Chocolate Cake','description':'made with Dutch Chocolate',
     'price':'$3.99', 'course':'Dessert','id':'2'},
    {'name':'Caesar Salad', 'description':'with fresh organic vegetables',
     'price':'$5.99', 'course':'Entree','id':'3'},
    {'name':'Iced Tea', 'description':'with lemon','price':'$.99',
     'course':'Beverage','id':'4'},
    {'name':'Spinach Dip', 'description':'creamy dip with fresh spinach',
     'price':'$1.99', 'course':'Appetizer','id':'5'}
]
item =  {
    'name':'Cheese Pizza',
    'description':'made with fresh cheese',
    'price':'$5.99',
    'course' :'Entree'
}

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# 1. Home Page Routing
@app.route('/')
@app.route('/restaurants')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    flash("test message")
    return render_template('restaurants.html', restaurants=restaurants)

# 2. Add new restaurant routing
@app.route('/restaurants/newrestaurant/', methods=['GET', 'POST'] )
def addRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Created")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('newrestaurant.html')

# 3. Edit Restaurant routing
@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    # editItem = (each for each in restaurants if each["id"] == restaurant_id).next()
    return render_template('editrestaurant.html', restaurant=restaurant)

# 4. Delete Restaurant Routing
@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return render_template('deleterestaurant.html', restaurant=restaurant)

# 5. Restaurant Menu Listing Routing
@app.route('/restaurants/<int:restaurant_id>/')
def menuList(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    if items == []:
        flash("No menu items to display")
    return render_template('menu.html', restaurant=restaurant, items=items)

# 6. Add new menu item routing
@app.route('/restaurants/<int:restaurant_id>/newitem')
def addMenuItem(restaurant_id):
    return render_template('newmenuitem.html', restaurant=restaurant)

# 7. Edit Menu item routing
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return render_template('editmenuitem.html', restaurant=restaurant, item=item)

# 8. Delete Menu Item routing
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return render_template('deletemenuitem.html', restaurant=restaurant, item=item)


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


