""" Module with all the routes of the auth app """

from app.forms import LoginForm
from flask import render_template, redirect, url_for, session, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from app.firestore_service import get_user, user_put
from app.models import UserData, UserModel

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    """ Render the login form template """
    context = {
        'login_form':login_form,
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            # Password validation
            password_db = user_doc.to_dict()['password']
            if check_password_hash(password_db, password):
                # Login
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)
                flash('Bienvenido de nuevo', category='alert-primary')
                
                redirect(url_for('hello'))
            else:
                flash('La información no coincide', category='alert-warning')
        else:
            flash('El usuario no existe. Registrese si lo desea', category='alert-warning')
            
            return redirect(url_for('auth.signup'))

        return redirect(url_for('index'))

    return render_template('login.html', **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto', category='alert-info')

    return redirect(url_for('auth.login'))

@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context={
        'signup_form':signup_form,
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:    
            # If the current username doesn't exist
            password_hash = generate_password_hash(password)
            
            # Create a new instance of user data
            user_data = UserData(username, password_hash)

            # Load in the firestore
            user_put(user_data)

            # Create UserModel instance for login
            user = UserModel(user_data)
            login_user(user)

            flash('Bienvenido!', category='alert-success')
            return redirect(url_for('hello'))
        else:
            flash('El usuario ya existe, inicia sesión', category='alert-warning')
            #return redirect(url_for('hello'))

    return render_template('signup.html', **context)

