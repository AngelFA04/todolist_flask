from flask import Flask, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap

# A news flask app is created
# it takes the actual file
app = Flask(__name__)
bootstrap =  Bootstrap(app)

app.config['SECRET_KEY'] = 'TOP_SECRET'


todos =  ['T1', 'T2', 'T3']

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
    # Set a cookie in the browser
    response.set_cookie('user_ip', user_ip)

    # Return a Flask response
    return response


@app.route('/hello')
def hello():
    # Get user_ip from browser cookies
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip':user_ip, 
        'todos':todos,
    }
    return render_template('hello.html', **context)
    

if __name__ == '__main__':
    app.run(debug=True)
    