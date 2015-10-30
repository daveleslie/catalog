from database_setup import Base, Restaurant, MenuItem
from flask import Flask, render_template, url_for, flash, request, redirect, \
    jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

__author__ = 'David'


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
    return render_template('restaurants.html', restaurants=restaurants)


# 2. Add new restaurant routing
@app.route('/restaurants/newrestaurant/', methods=['GET', 'POST'])
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
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash("Restaurant Updated")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('editrestaurant.html', restaurant=restaurant)


# 4. Delete Restaurant Routing
@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant Deleted")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('deleterestaurant.html', restaurant=restaurant)


# 5. Restaurant Menu Listing Routing
@app.route('/restaurants/<int:restaurant_id>/')
def menuList(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)\
        .all()
    if not items:
        flash("No menu items to display")
    return render_template('menu.html', restaurant=restaurant, items=items)


# 6. Add new menu item routing
@app.route('/restaurants/<int:restaurant_id>/newitem/',
           methods=['GET', 'POST'])
def addMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            course=request.form['course'],
            restaurant_id=restaurant.id
        )
        session.add(newItem)
        session.commit()
        flash("New Menu Item Added")
        return redirect(url_for('menuList', restaurant_id=restaurant.id))
    else:
        return render_template('newmenuitem.html', restaurant=restaurant)


# 7. Edit Menu item routing
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.price = request.form['price']
        item.course = request.form['course']
        item.description = request.form['description']
        session.add(item)
        session.commit()
        flash("Menu Item Updated")
        return redirect(url_for('menuList', restaurant_id=restaurant.id))
    else:
        return render_template('editmenuitem.html', restaurant=restaurant,
                               item=item)


# 8. Delete Menu Item routing
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Menu Item Deleted")
        return redirect(url_for('menuList', restaurant_id=restaurant.id))
    else:
        return render_template('deletemenuitem.html', restaurant=restaurant,
                               item=item)

# **************API ENDPOINTS************** #


# API GET request for restaurant list
@app.route('/restaurants/JSON/')
def restaurantListJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(REstaurants=[i.serialize for i in restaurants])


# API GET request for menu items list
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)\
        .all()
    return jsonify(MenuItems=[i.serialize for i in items])


# API GET request for item details
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(itemDetails=[menuItem.serialize])


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
