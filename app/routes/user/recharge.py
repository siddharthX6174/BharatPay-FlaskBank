from app import app, db
from flask import render_template, session, redirect, request, flash, url_for
from decimal import Decimal
from datetime import datetime
from app.models.user import User, Transaction
from app.utils.validators import validate_amount
from app.decorators import approved_required


@app.route('/recharge', methods=['GET', 'POST'])
@approved_required
def recharge():
     # Retrieve user_id from session
     user_id = session.get('user_id')
     user = db.session.get(User, user_id)

     if request.method == 'POST':
          try:
               # Transition to Decimal immediately
               amount = Decimal(request.form.get('amount', '0'))
          except Exception:
               flash('Invalid amount', 'danger')
               return redirect(url_for('recharge'))
          
          # Validate amount
          valid, error = validate_amount(float(amount))
          if not valid:
               flash(error, 'danger')
               return redirect(url_for('recharge'))

          # calculate the discount amount (10% of the recharge) using Decimals
          discount = amount * Decimal('0.1')
          total_allowance = amount - discount

          # check if the user has sufficient balance
          if total_allowance > user.balance:
               flash('Insufficient balance', 'danger')
               return redirect(url_for('recharge'))
          
          try:
               # update the user's balance
               user.balance -= total_allowance

               # Create transaction record
               transaction = Transaction(
                    user_id=user.id,
                    recipient_id=user.id,
                    recipient_name=user.full_name,
                    recipient_card_number=user.account_number,
                    amount=total_allowance, 
                    type='recharge',
                    description=f'Mobile Recharge (Amount: {amount}, Discount: {discount})',
                    timestamp=datetime.now()
               )

               db.session.add(transaction)
               db.session.commit()

               return render_template('user/recharge_success.html', amount=float(total_allowance), discount=float(discount))
          except Exception as e:
               db.session.rollback()
               app.logger.error(f'Recharge failed: {str(e)}')
               flash('Recharge failed. Please try again.', 'danger')
               return redirect(url_for('recharge'))
      
     return render_template('user/recharge.html', user=user)