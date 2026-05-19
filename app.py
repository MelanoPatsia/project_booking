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

@app.route('/register')
def register():
    return '<strong>Register</strong> <button>Click</button>'

@app.route('/profile')
def profile():
    return '<strong>profile</strong> <button>Click</button>'


@app.route('/calculator/<int:num1>/<int:num2>/<int:num3>/<string:sign>')
def calculator(num1, num2, num3, sign):
    try:
        if sign == '+':
            return f'<strong>{num1+num2+num3}</strong>'
        elif sign == '-':
            return f'<strong>{num1-num2-num3}</strong>'
        elif sign == ':':
            return f'<strong>{num1/num2/num3}</strong>'
        elif sign == 'x':
            return f'<strong>{num1*num2*num3}</strong>'
        else:
            return '<strong>Enter a mathematical operation sign!</strong>'
    except ZeroDivisionError:
        return '<strong>You cannot divide by zero</strong>'
if '__main__' == __name__:
    app.run()