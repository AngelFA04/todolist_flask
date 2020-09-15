import unittest
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required, current_user
from app import create_app
from app.forms import LoginForm, TodoForm, DeleteTodoForm, UpdateTodoForm

from app.firestore_service import get_users, get_todos, todo_put, delete_todo, update_todo

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
@login_required
def hello():
    # Get user_ip from browser session
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    context = {
        'user_ip':user_ip, 
        'todos': get_todos(username),
        'username': username,
        'current_user': current_user,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form,
    }

    if todo_form.validate_on_submit():
        todo_put(username, todo_form.description.data)
        #import pdb; pdb.set_trace()
        flash('Tarea agregada con éxito', category='alert-success')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)
    

@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id, todo_id)

    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id

    update_todo(user_id, todo_id, done)

    return redirect(url_for('hello'))