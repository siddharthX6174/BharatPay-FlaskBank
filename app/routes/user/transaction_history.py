from app import app, db
from flask import render_template, session, redirect, flash, url_for
from app.models.user import User, Transaction
from app.decorators import approved_required


@app.route('/transaction_history')
@approved_required
def transaction_history():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)

    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.timestamp.desc()).all()

    return render_template('user/transaction_history.html', user=user, transactions=transactions)
   
  