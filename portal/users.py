# coding:utf-8
# Copyright 2011 Litl, LLC. All Rights Reserved.
import logging

from flask import Module, render_template, request, redirect, url_for, session, flash
from portal.models import PortalUser
from portal.forms import UserForm, NewUserForm, PasswordForm
from login import check_login

portal = Module(__name__, url_prefix='/user')

portal.before_request(check_login)

@portal.route('/all/')
def list_users():
    users = PortalUser.all()
    return render_template('user_list.html', users=users)

@portal.route('/save/', methods=['POST'])
def save_user():
    needs_password = 'needs_password' in request.form
    if needs_password:
        form = NewUserForm(request.form)
    else:
        form = UserForm(request.form)
    if form.validate():
        email = form.email.data
        if form.id.data:
            user = PortalUser.find_by_key(form.id.data)
        else:
            user = PortalUser.find_by_email(email)
        if not user:
            user = PortalUser(email=email)
        form.populate_obj(user)
        if 'password' in request.form:
            user.set_password(form.password.data)
        user.save()
        return redirect(url_for('list_users'))
    else:
        return render_template('user_detail.html', form=form, needs_password=needs_password)

@portal.route('/<email>/')
def edit_user(email):
    user = PortalUser.find_by_email(email)
    form = UserForm(request.args, user)
    return render_template('user_detail.html', form=form)

@portal.route('/create/')
def create_user():
    form = NewUserForm()
    return render_template('user_detail.html', form=form, needs_password=True)

@portal.route('/<email>/change_password/', methods=['GET', 'POST'])
def change_password(email):
    if request.method == 'POST':
        form = PasswordForm(request.form)
        if form.validate():
            user = PortalUser.find_by_email(email)
            user.set_password(form.password.data)
            user.save()
            flash('Password changed')
            return redirect('/user/%s/' % email)
    else:
        form = PasswordForm()
    return render_template('change_password.html', form=form, email=email)
