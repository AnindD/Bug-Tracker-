from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import re  # Regular Expression 
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user 
import json 

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        login_username = request.form.get("username")
        login_password = request.form.get("password")
        user = User.query.filter_by(username=login_username).first() 
        if user: 
            if check_password_hash(user.password, login_password): 
                flash("Logged in Successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("auth.bug_tracker"))
            else: 
                flash("Incorrect Password, Try, Again", category="error")
        else: 
            flash("Username does not exist", category="error")
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required 
def logout(): 
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        terms_conditions = request.form.getlist("terms_conditions_check")
        passwordRegex = ("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)” + “(?=.*[-+_!@#$%^&*., ?]).+$")
        passwordCompile = re.compile(passwordRegex)
        if len(username) <= 5: 
            flash("Username must be greater than 5 characters", category="error")
        elif len(password) <= 5: 
            flash("Password must be greater than 5 characters.", category="error")
        elif (re.search(passwordCompile, password) == False):
            flash("It is reccomendded your password has one uppercase, one lowercase and a special character", category="Warning")
        elif terms_conditions == []: 
            flash("You must follow the terms and conditions", category="error")
        else: 
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit() 
            flash("Account has been succesfully created!", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", user=current_user)

@auth.route("/bugticket", methods=['GET', 'POST'])
def bug_ticket():
    if request.method == 'POST':
        bug_title = request.form.get("bug_title")
        bug_info = request.form.get("bug_response")
        print(bug_info)
        print(bug_title) 
        new_bug = Note(data=bug_info, user_id=current_user.id)
        db.session.add(new_bug)
        db.session.commit() 
    return render_template("ticket.html", user=current_user)

@auth.route("/bugtracker",)
@login_required
def bug_tracker(): 
    return render_template("bug_tracker.html", user=current_user)

"""@auth.route("/delete-note", methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteID = note['noteId']
    note = Note.query.get(noteID)
    if note: 
        if note.user_id == current_user.id: 
            db.session.delete(note)
            db.session.commit()
    return jsonify()"""
 
