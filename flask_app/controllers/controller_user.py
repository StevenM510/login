from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def login():
    if'uuid' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def success():
    if'uuid' not in session:
        return redirect('/')
    user = User.get_one_by_id(session['uuid'])
    return render_template('dashboard.html', user = user[0])



@app.route('/user/dashboard', methods=['POST'])
def register_user():
    is_valid = User.validate_user(request.form)
    if is_valid:
        list_of_users = User.get_one_by_email(request.form['email'])
        if len(list_of_users) > 0:
            flash("email already exists")
            return redirect('/')

        pw_hash = bcrypt.generate_password_hash(request.form['pw_hash'])
        info = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "pw_hash": pw_hash,
            }
        new_user_id = User.save(info)
        session['uuid'] = new_user_id
        return redirect('/dashboard')
    return redirect('/')
    

@app.route('/login', methods =['POST'])
def login_user():
    list_of_users = User.get_one_by_email(request.form['email'])
    if len(list_of_users) == 0:
        flash('Invalid credentials')
        return redirect('/')
    else:
        user = list_of_users[0]
        print(user)
        if bcrypt.check_password_hash(user['pw_hash'], request.form['pw_hash']):
            session['uuid'] = user['id']
            
        else:
            flash("Invalid Email/Password")
        return redirect('/')





@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')