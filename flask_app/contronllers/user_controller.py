from flask_app import app
from flask import render_template,request,redirect,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register/user", methods=["POST"])
def register():
    if not User.validate_user(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name" :request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect("/dashboard")

@app.route("/dashboard")
def welcome_user():
    data = {
        "id":session['user_id']
    }
    #session["user"] = User.one_user(date)  show JSON error?
    user = User.one_user(data)
    #return render_template('dashboard.html',user=session['user'])
    return render_template('dashboard.html',user=user)

@app.route("/login", methods=["POST"])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email2"] }
    user_in_db = User.get_by_email(data)
    print(user_in_db)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password2']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    print(session['user_id'])
    # never render on a post!!!
    return redirect("/dashboard")





    # password2 = request.form['password2']
    # users = User.get_all()
    # for user in users :
    #     if request.form["email2"] == user.email:
    #         if bcrypt.check_password_hash(password2, user.password) == True:
    #             return redirect('/dashboard')
    #         return redirect('/')
    #     return redirect('/')


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id")
    return redirect("/")