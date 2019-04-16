from flask import render_template, flash, redirect, url_for, abort
from cat_app import app, db
from cat_app.forms import Register, Login_form, add_cat, NewItem, UpdateItem
from cat_app.modules import User, Category, Items
from flask_login import login_user, logout_user, current_user, login_required
from flask_dance.contrib.google import make_google_blueprint, google
from flask import jsonify
import os
import json

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


secId = json.loads(open('client_secret.json', 'r').read())['web']['client_id']


blueprint = make_google_blueprint(
    client_id=secId,
    client_secret="lCzkC0gbn6v1oQhlhEHK8ScC",
    offline=True,
    scope=["profile", "email"],
    redirect_to='login_google',
)
app.register_blueprint(blueprint, url_prefix="/login")


# Third party login
@app.route("/login/google/")
def login_google():
    if not google.authorized:
        return redirect(url_for('google.login'))
    if google.authorized:
        resp = google.get('/oauth2/v2/userinfo')
        assert resp.ok
        email = resp.json()['email']
        user = User.query.filter_by(email=email).first()
        if user is not None:
            login_user(user)
            flash("Success login in", "success")
            return redirect(url_for('home'))
        else:
            flash("Unsuccessful login this email not exists", "danger")
            return redirect(url_for('register'))


# Home page
@app.route("/")
def home():
    items = Items.query
    return render_template("home.html", title="Last Items", items=items)


# JSON endpoint
@app.route("/catlog/json")
def catlog_json():
    get_items = Items.query.all()
    all_items = [{
                'content': item.content,
                'title': item.title,
                'item_id': item.id,
                'category': item.category.name
                }
                for item in get_items
                ]
    return jsonify(all_items)


# Login page
@app.route("/login", methods=['POST', 'GET'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and form.password.data == user.password:
            flash("Success login in", "success")
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Unsuccessful login in", "danger")

    return render_template("login.html", title="Login", form=form)


# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Registration page
@app.route("/register", methods=['POST', 'GET'])
def register():
    form = Register()
    if form.validate_on_submit():
        user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        flash("Your account is created successfuly", 'success')
    return render_template("register.html", form=form, title="Registration")


# Create new category
@app.route("/new-cat", methods=["GET", "POST"])
@login_required
def new_cat():
    form = add_cat()
    if form.validate_on_submit():
        cat = Category(name=form.cat_name.data)
        db.session.add(cat)
        db.session.commit()
        flash("Category add Successfuly ", "success")
    return render_template(
                          "new_category.html",
                          form=form,
                          title="Add new category"
                          )


#  Add New item
@app.route("/add-item", methods=['GET', 'POST'])
@login_required
def addItem():
    form = NewItem()
    if form.validate_on_submit():
        flash("Successful add item", "success")
        item = Items(
                    title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    cat_id=form.category.data.id
                    )

        db.session.add(item)
        db.session.commit()

        return redirect(url_for("addItem"))
    return render_template("add_item.html", form=form, title="Add Item")


# Category by Id
@app.route('/catlog/<int:id>')
def catlog(id):
    items = Items.query.filter_by(cat_id=id)
    item_first = items.first()
    if item_first is not None:
        cat_name = item_first.category.name
        return render_template("catlog.html", items=items, title=cat_name)
    else:
        return render_template("catlog.html", items=items, title="No content")


# get all Category
def all_cat():
    all_cat = Category.query.all()
    return all_cat


# Single item page
@app.route('/catlog/items/<int:id>')
def single_item(id):
    item = Items.query.filter_by(id=id).first()
    return render_template("single.html", item=item, title=item.title)


# Update Item
@app.route('/items/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_item(id):
    form = UpdateItem()
    item = Items.query.filter_by(id=id).first()
    if item.author is not current_user:
        abort(403)
    if form.validate_on_submit():
        item.title = form.title.data
        item.content = form.content.data
        item.category = form.category.data
        db.session.commit()
        flash("Successful update item", "success")
        return redirect(url_for('single_item', id=item.id))
    else:
        form.title.data = item.title
        form.content.data = item.content
        form.category.data = item.category
    return render_template('update_item.html', title="Update item", form=form)


# Delete item
@app.route('/items/<int:id>/delete', methods=['POST'])
@login_required
def delete_item(id):
    item = Items.query.get_or_404(id)
    if item.author is not current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash("Successful Delete item", 'success')
    return redirect(url_for('home'))


# All category query
@app.context_processor
def context():
    return dict(all_cat=all_cat)


# JSON endpoint
@app.route("/api/category/<int:cat_id>/item/<int:item_id>/json")
def select_item(cat_id, item_id):
    item = Items.query.filter_by(cat_id=cat_id, id=item_id).first()

    """Returns JSON of selected item if item exist """
    if item is not None:
        all_items = [{
                'content': item.content,
                'title': item.title,
                'item_id': item.id,
                'category': item.category.name
                 }]
        return jsonify(all_items)
    else:
        flash("This item not exist", 'danger')
        return redirect(url_for("home"))
