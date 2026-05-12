from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<strong>Hello, this is landing page!</strong>'

@app.route('/login')
def login():
    return '<strong>This is loging page</strong> <button>Click</button>'

@app.route('/logout')
def logout():
    return '<strong>Log out</strong> <button>Click</button>'

if '__main__' == __name__:
    app.run()