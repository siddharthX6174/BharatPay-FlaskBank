from app import app, db
from flask import render_template, request, flash, session
from app.models.user import User, Transaction, TransactionLimit
from datetime import datetime, date
from decimal import Decimal
from app.decorators import approved_required

@app.route('/withdraw', methods=['GET', 'POST'])
@approved_required
def withdraw():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    
    # Helper to get limits and current status
    def get_withdrawal_context():
        limit = TransactionLimit.query.filter_by(user_id=user_id).first()
        if not limit:
            limit = TransactionLimit(
                user_id=user_id,
                daily_limit=Decimal('100000'),
                per_transaction_limit=Decimal('50000'),
                withdrawal_daily_limit=Decimal('50000')
            )
            db.session.add(limit)
            db.session.commit()
            db.session.refresh(limit)
        
        today = date.today()
        today_withdrawals = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.type == 'withdrawal',
            db.func.date(Transaction.timestamp) == today
        ).all()
        
        today_total = sum(Decimal(str(t.amount)) for t in today_withdrawals)
        remaining_limit = Decimal(str(limit.withdrawal_daily_limit or 50000)) - today_total
        return limit, remaining_limit, today_total

    if request.method == 'GET':
        limit, remaining_limit, _ = get_withdrawal_context()
        return render_template('user/withdraw.html', 
                             user=user, 
                             remaining_limit=float(remaining_limit),
                             daily_limit=float(limit.withdrawal_daily_limit or 50000))
    
    # POST request
    try:
        amount = Decimal(request.form.get('amount', '0'))
        atm_location = request.form.get('atm_location', 'ATM')
        
        limit, remaining_limit, today_total = get_withdrawal_context()

        if amount <= 0:
            flash('Please enter a valid amount', 'danger')
            return render_template('user/withdraw.html', user=user, remaining_limit=float(remaining_limit), daily_limit=float(limit.withdrawal_daily_limit or 50000))
        
        # Check balance
        if amount > user.balance:
            flash('Insufficient balance', 'danger')
            return render_template('user/withdraw.html', user=user, remaining_limit=float(remaining_limit), daily_limit=float(limit.withdrawal_daily_limit or 50000))
        
        # Check transaction limit
        if amount > Decimal(str(limit.per_transaction_limit or 50000)):
            flash(f'Amount exceeds per transaction limit of Rs {limit.per_transaction_limit}', 'danger')
            return render_template('user/withdraw.html', user=user, remaining_limit=float(remaining_limit), daily_limit=float(limit.withdrawal_daily_limit or 50000))
        
        # Check daily withdrawal limit
        if (today_total + amount) > Decimal(str(limit.withdrawal_daily_limit or 50000)):
            flash(f'Daily withdrawal limit exceeded. Remaining limit: Rs {float(remaining_limit):.2f}', 'danger')
            return render_template('user/withdraw.html', user=user, remaining_limit=float(remaining_limit), daily_limit=float(limit.withdrawal_daily_limit or 50000))
        
        # Process withdrawal
        user.balance -= amount
        
        # Create transaction record
        transaction = Transaction(
            user_id=user_id,
            recipient_name=user.full_name,
            recipient_card_number=user.account_number,
            type='withdrawal',
            amount=amount,
            description=f'Cash withdrawal at {atm_location}',
            timestamp=datetime.now()
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        # Refresh context for the success view
        limit, remaining_limit, _ = get_withdrawal_context()
        
        flash(f'Successfully withdrawn Rs {amount:,.2f}. New balance: Rs {float(user.balance):.2f}', 'success')
        return render_template('user/withdraw.html', 
                             user=user,
                             remaining_limit=float(remaining_limit),
                             daily_limit=float(limit.withdrawal_daily_limit or 50000))
        
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')
        limit, remaining_limit, _ = get_withdrawal_context()
        return render_template('user/withdraw.html', user=user, remaining_limit=float(remaining_limit), daily_limit=float(limit.withdrawal_daily_limit or 50000))