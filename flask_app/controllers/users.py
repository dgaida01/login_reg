import re
from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/welcome')
    return render_template('login_reg.html')

@app.route('/user/register', methods=['post'])
def register_user():
    #create a new user in the database then redirect as appropirate to welcome page
    data = {
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email':request.form['email'],
        'password': request.form['password'],
        'password_confirm' : request.form['password_confirm']
    }

    if User.validate_new_user(data):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        new_user_data = {
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email':request.form['email'],
        'password': pw_hash
        }
        user_id = User.createUser(new_user_data)
        session['user_id'] =user_id
        session['first_name'] = request.form['first_name']
        session['last_name'] =  request.form['last_name']
        session['email'] = request.form['email']        
    return redirect('/')

@app.route('/user/login',methods=['post'])
def login():
    data = {
        'email':request.form['email'],
        'password':request.form['password']
    }
    the_user= User.get_user_by_email(data)
    if the_user is None:
        flash("Email not found","login_error")
        return redirect('/')
    elif not bcrypt.check_password_hash(the_user.password,request.form['password']):
        flash("Password is incorrect","login_error")
        return redirect('/')
    else:
        session['user_id'] =the_user.id
        session['first_name'] = the_user.first_name
        session['last_name'] =  the_user.last_name
        session['email'] = the_user.email
        return redirect('/welcome')

@app.route('/welcome')
def welcome():
    if  'user_id' not in session:
        return redirect('/')
    else:
        return render_template('welcome.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged Out - Sign in to access website","Logout")
    return redirect('/')