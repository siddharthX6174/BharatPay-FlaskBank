from app import app, db
from flask import render_template, session, flash, redirect, url_for
from app.models.user import User
from app.decorators import approved_required

@app.route('/dashboard')
@approved_required
def dashboard():
     # Retrieve user_id from session
     user_id = session.get('user_id')
     # Retrieve the user from the db using the user_id
     user = db.session.get(User, user_id)
     
     # Fetch recent transactions
     from app.models.user.transaction import Transaction
     transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.timestamp.desc()).all()
     
     # Fetch beneficiaries
     from app.models.user.features import Beneficiary
     beneficiaries = Beneficiary.query.filter_by(user_id=user_id).limit(4).all()
     
     # Fetch insights
     from app.utils.stats import get_user_insights
     insights = get_user_insights(user_id)
     
     return render_template('user/index.html', 
                          user=user, 
                          transactions=transactions, 
                          beneficiaries=beneficiaries,
                          insights=insights)

     






