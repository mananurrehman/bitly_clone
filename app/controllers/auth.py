from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.models import User 
from app import db
from flask_login import login_user, logout_user, login_required
import logging
from flask_login import current_user

auth = Blueprint('auth', __name__)

# login route

@auth.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("All fields are required!", 'error')
            return redirect(url_for('auth.login'))

# user authentication    
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)

            # role based redirection
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            elif user.role == 'org_owner':
                return redirect(url_for('main.org_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        
        flash("Invalid email or password", 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('login.html')

# Sign up route

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('All fields are required', 'error')
            return(redirect(url_for('auth.signup')))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return(redirect(url_for('auth.signup')))
        
        new_user = User(email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            logging.error(f"Failed to initialize database: {e}")
    
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    return render_template('signup.html')


# Logout Rotue

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successfully', 'success')
    return redirect(url_for('auth.login'))