__author__ = 'David'

from flask import Flask

app = Flask(__name__)

# 1. Home Page Routing
@app.route('/')
@app.route('/restaurants')
def restaurantList():
    return "This is the list of all restaurants"

# 2. Add new restaurant routing
@app.route('/restaurants/newrestaurant')
def addRestaurant():
    return "Add new restaurant page"

# 3. Edit Restaurant routing
@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return "Edit existing restaurant"

# 4. Delete Restaurant Routing
@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return "Delete Existing Restaurant"

# 5. Restaurant Menu Listing Routing
@app.route('/restaurants/<int:restaurant_id>')
def menuList(restaurant_id):
    return "List menu items"

# 6. Add new menu item routing
@app.route('/restaurants/<int:restaurant_id>/newitem')
def addMenuItem(restaurant_id):
    return "add new menu item"

# 7. Edit Menu item routing
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "edit menu item"

# 8. Delete Menu Item routing
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "delete menu item"



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


