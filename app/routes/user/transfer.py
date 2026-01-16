from app import app, db
from flask import render_template, session, request, redirect, url_for, flash
from decimal import Decimal
from datetime import datetime
from app.models.user import User, Transaction
from app.utils.validators import validate_amount
from app.decorators import approved_required


@app.route('/transfer', methods=['GET', 'POST'])
@approved_required
def transfer():
     # Retrieve user_id from session
     user_id = session.get('user_id')
     
     user = db.session.get(User, user_id)
     
     # Pre-fill beneficiary data if coming from beneficiaries page
     beneficiary_data = None
     if request.method == 'GET':
          account_number = request.args.get('account', '').strip().upper()
          if account_number:
               # Find beneficiary in user's saved beneficiaries
               from app.models.user.features import Beneficiary
               beneficiary = Beneficiary.query.filter_by(
                    user_id=user_id,
                    beneficiary_card_number=account_number
               ).first()
               
               if beneficiary:
                    beneficiary_data = {
                         'name': beneficiary.beneficiary_name,
                         'account_number': beneficiary.beneficiary_card_number,
                         'nickname': beneficiary.nickname
                    }

     if request.method == 'POST':
          recipient_name = request.form.get('recipient_name', '').strip()
          recipient_account_number = request.form.get('account_number', '').strip().upper()
          
          try:
               # Transition to Decimal immediately
               amount = Decimal(request.form.get('amount', '0'))
          except Exception:
               flash('Invalid amount', 'danger')
               return redirect(url_for('transfer'))
          
          # Validate amount
          valid, error = validate_amount(float(amount))
          if not valid:
               flash(error, 'danger')
               return redirect(url_for('transfer'))
          
          # Validate account number format (ACC + 13 digits)
          if not recipient_account_number.startswith('ACC') or len(recipient_account_number) != 16:
               flash('Invalid account number format. Account number should start with ACC followed by 13 digits.', 'danger')
               return redirect(url_for('transfer'))
          
          if amount > user.balance:
               flash('Insufficient funds', 'danger')
               return redirect(url_for('transfer'))
          
          recipient = User.query.filter_by(account_number=recipient_account_number).first()
          
          if not recipient:
               flash('Recipient account not found', 'danger')
               return redirect(url_for('transfer'))
          
          if recipient.full_name.lower() != recipient_name.lower():
               flash('Account number and name do not match', 'danger')
               return redirect(url_for('transfer'))
          
          if recipient.id == user.id:
               flash('Cannot transfer to yourself', 'danger')
               return redirect(url_for('transfer'))
          
          # Use atomic transaction
          try:
               # Update balances
               user.balance -= amount
               recipient.balance += amount
               
               # Sender transaction (Debit)
               db.session.add(Transaction(
                    user_id=user_id,
                    recipient_id=recipient.id,
                    recipient_name=recipient.full_name,
                    recipient_card_number=recipient.account_number,
                    amount=amount,
                    type='transfer',
                    description=request.form.get('description', 'Funds Transfer'),
                    timestamp=datetime.now()
               ))
               
               # Recipient transaction (Credit)
               db.session.add(Transaction(
                    user_id=recipient.id,
                    recipient_id=user.id,
                    recipient_name=user.full_name,
                    recipient_card_number=user.account_number,
                    amount=amount,
                    type='transfer',
                    description=f'Funds Received from {user.full_name}',
                    timestamp=datetime.now()
               ))
               
               # Update beneficiary if this recipient is saved as beneficiary
               from app.models.user.features import Beneficiary
               beneficiary_record = Beneficiary.query.filter_by(
                    user_id=user_id,
                    beneficiary_card_number=recipient_account_number
               ).first()
               if beneficiary_record:
                    beneficiary_record.last_used = datetime.now()
                    beneficiary_record.total_transactions += 1
               
               db.session.commit()
               
               flash(f'Successfully transferred Rs {amount:,.2f} to {recipient.full_name}', 'success')
               return redirect(url_for('dashboard'))
               
          except Exception as e:
               db.session.rollback()
               app.logger.error(f'Transfer failed: {str(e)}')
               flash('Transfer failed. Please try again.', 'danger')
               return redirect(url_for('transfer'))

     # Get beneficiaries for Quick Send section
     from app.models.user.features import Beneficiary
     beneficiaries_list = Beneficiary.query.filter_by(user_id=user_id).order_by(
          Beneficiary.is_favorite.desc(),
          Beneficiary.last_used.desc()
     ).limit(4).all()
     
     return render_template('user/transfer.html', user=user, beneficiary=beneficiary_data, beneficiaries=beneficiaries_list)



