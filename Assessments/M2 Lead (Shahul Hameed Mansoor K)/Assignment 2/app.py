from re import T
from flask import Flask,render_template,redirect,url_for

app=Flask(__name__)


@app.route("/")
def homePage():
    return render_template('home.html')

@app.route("/about")
def aboutPage():
    return "about Page !!!"

@app.route("/signin")
def signinPAGE():
    return render_template('signin.html')


@app.route("/signup")
def signupPAGE():
    return render_template('signup.html')


@app.route("/admin")
def admin():
    return "Admin Page"

@app.route("/hello/<name>")
def hello_users(name):
    return "Hello!! %s" %name


@app.route("/user/<name>")
def hello_user(name):
    if name=='admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('hello_users',name=name))



if __name__=='__main__':
    app.run(host='0.0.0.0',port=3000,debug=True)