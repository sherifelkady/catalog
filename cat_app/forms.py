from flask_wtf import FlaskForm
from wtforms import (
                    StringField,
                    PasswordField,
                    SubmitField,
                    TextAreaField,
                    SelectField
                    )
from wtforms.validators import DataRequired, EqualTo, ValidationError
from cat_app.modules import User, Category, Items
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask import flash
from cat_app import app, db


# User Registrtion Form
class Register(FlaskForm):
    username = StringField("UserName", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    re_password = PasswordField(
                               "Confirm Password",
                               validators=[DataRequired(), EqualTo('password')]
                               )
    submit = SubmitField("Create an account")

    # Validate if Email Unique or not
    def validate_email(self, email):
        get_email = User.query.filter_by(email=email.data).first()
        if get_email:
            raise ValidationError("this email is taken")

    # Validate if Username Unique or not
    def validate_username(self, username):
        get_username = User.query.filter_by(username=username.data).first()
        if get_username:
            raise ValidationError("this email is taken")


# Login Form
class Login_form(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# New Category Form
class add_cat(FlaskForm):
    cat_name = StringField("Category Name", validators=[DataRequired()])
    submit = SubmitField("Add category")


# Add New Item

def cat_query():
    return Category.query


class NewItem(FlaskForm):
    title = StringField("Item Name", validators=[DataRequired()])
    content = TextAreaField("Item Description", validators=[DataRequired()])
    category = QuerySelectField(
                                query_factory=cat_query,
                                allow_blank=True,
                                get_label='name',
                                validators=[DataRequired()]
                                )

    submit = SubmitField("Add item")

    # Validate if Category field empty
    def validate_category():
        if form.category.data =="":
            raise ValidationError("Sorry , you havn't chosen a category name")



# Update  Item
class UpdateItem(FlaskForm):
    title = StringField("Item Name", validators=[DataRequired()])
    content = TextAreaField("Item Description", validators=[DataRequired()])
    category = QuerySelectField(
                                query_factory=cat_query,
                                allow_blank=False,
                                get_label='name'
                                )
    submit = SubmitField("Update item")
