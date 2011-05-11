import logging

from flask import Module, render_template, request, redirect, url_for, session, flash
from portal.forms import LoginForm
from portal.models import PortalUser

door = Module(__name__)

@door.route('/')
def index():
    return render_template('index.html')

@door.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if PortalUser.check_login(request.form['email'], request.form['password']):
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('users.list_users'))
        error = "Invalid email or password"
    form = LoginForm()
    return render_template('login.html', form=form, error=error)

@door.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@door.route('/bootstrap/')
def bootstrap():
    if PortalUser.no_users():
        session['logged_in'] = True
        flash('Logged in without a real user -- be sure and create one soon.')
        return redirect('/users/all/')
    else:
        flash('Bootstrap login not available after first user created.')
        return redirect(url_for('index'))

def check_login():
    if 'logged_in' in session and session['logged_in']:
        logging.info("User is logged in")
    else:
        logging.warn("Hey they're not logged in!")
        return redirect('/login')
