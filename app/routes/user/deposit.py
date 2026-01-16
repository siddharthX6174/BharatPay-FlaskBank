from app import app, db
from flask import render_template, session, request, redirect, url_for, flash
from decimal import Decimal
from datetime import datetime
from app.models.user import User, Transaction
from app.utils.validators import validate_amount, clean_card_number
from app.decorators import approved_required

@app.route('/deposit', methods=['GET', 'POST'])
@approved_required
def deposit():
     # Retrieve user_id from session
     user_id = session.get('user_id')
     user = db.session.get(User, user_id)

     if request.method == 'POST':
          try:
               # Transition to Decimal immediately
               amount = Decimal(request.form.get('amount', '0'))
          except Exception:
               flash('Invalid amount', 'danger')
               return redirect(url_for('deposit'))
          
          # Validate amount
          valid, error = validate_amount(float(amount))
          if not valid:
               flash(error, 'danger')
               return redirect(url_for('deposit'))
          
          try:
               # update the user's balance
               user.balance += amount

               # create a deposit transaction record
               transaction = Transaction(
                    user_id=user.id,
                    recipient_id=user.id,
                    recipient_name=user.full_name,
                    recipient_card_number=user.account_number,
                    amount=amount,
                    type='deposit',
                    description='Manual Deposit',
                    timestamp=datetime.now()
               )

               db.session.add(transaction)
               db.session.commit()
               
               flash(f'Successfully deposited Rs {amount:,.2f} to your account.', 'success')
               return redirect(url_for('dashboard'))
          except Exception as e:
               db.session.rollback()
               app.logger.error(f'Deposit failed: {str(e)}')
               flash('Deposit failed. Please try again.', 'danger')
               return redirect(url_for('deposit'))
     
     return render_template('user/deposit.html', user=user)
