from app import app, db
from flask import render_template, session, redirect, flash, url_for
from app.models.user import User
from app.decorators import approved_required

@app.route('/exchange_rate')
@approved_required
def exchange_rate():
     # Retrieve user_id from session
     user_id = session.get('user_id')
     user = db.session.get(User, user_id)
     return render_template('user/exchange.html', user=user)