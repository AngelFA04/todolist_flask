from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
import unittest
from app import create_app
from app.forms import LoginForm
app = create_app()


app.config['SECRET_KEY'] = 'TOP_SECRET'


todos =  ['T1', 'T2', 'T3']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(500)
def not_found(error):
    return render_template('error.html', error=error, error_numer=500)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error, error_number=404)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    # Set a cookie in the session
    session['user_ip'] = user_ip

    # Return a Flask response
    return response


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # Get user_ip from browser session
    user_ip = session.get('user_ip')
    login_form =  LoginForm()
    username = session.get('username')
    context = {
        'user_ip':user_ip, 
        'todos':todos,
        'login_form': login_form,
        'username': username,
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))

    return render_template('hello.html', **context)
    

if __name__ == '__main__':
    app.run(debug=True)
    