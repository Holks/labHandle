from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.auth import bp
import click
from app.auth.forms import RegistrationForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html', title='Login')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()

    return render_template('auth/register.html', title='',
        form=form)
