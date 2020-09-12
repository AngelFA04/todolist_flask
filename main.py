from flask import Flask, request
# A news flask app is created
# it takes the actual file
app = Flask(__name__)

@app.route('/')
def hello():
    user_ip = request.remote_addr
    return f'Hello, your ip is {user}'

if __name__ == '__main__':
    app.run(debug=True)
    