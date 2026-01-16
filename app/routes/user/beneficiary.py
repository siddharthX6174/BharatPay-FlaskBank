from app import app, db
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app.models.user import User, Beneficiary
from app.decorators import approved_required
from datetime import datetime

@app.route('/beneficiaries')
@approved_required
def beneficiaries():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    
    # Get all beneficiaries
    all_beneficiaries = Beneficiary.query.filter_by(user_id=user_id).order_by(
        Beneficiary.is_favorite.desc(),
        Beneficiary.last_used.desc()
    ).all()
    
    return render_template('user/beneficiaries.html', 
                         user=user, 
                         beneficiaries=all_beneficiaries)

@app.route('/beneficiary/add', methods=['POST'])
@approved_required
def add_beneficiary():
    user_id = session.get('user_id')
    
    try:
        account_number = request.form.get('account_number', '').strip().upper()
        nickname = request.form.get('nickname', '').strip()
        
        # Validate account number format (ACC + 13 digits)
        if not account_number.startswith('ACC') or len(account_number) != 16:
            flash('Invalid account number format', 'danger')
            return redirect(url_for('beneficiaries'))
        
        # Check if beneficiary user exists
        beneficiary_user = User.query.filter_by(account_number=account_number).first()
        if not beneficiary_user:
            flash('Account number not found', 'danger')
            return redirect(url_for('beneficiaries'))
        
        if beneficiary_user.id == user_id:
            flash('Cannot add yourself as beneficiary', 'warning')
            return redirect(url_for('beneficiaries'))
        
        # Check if already exists
        existing = Beneficiary.query.filter_by(
            user_id=user_id,
            beneficiary_card_number=account_number
        ).first()
        
        if existing:
            flash('Beneficiary already exists', 'info')
            return redirect(url_for('beneficiaries'))
        
        # Add beneficiary
        beneficiary = Beneficiary(
            user_id=user_id,
            beneficiary_name=beneficiary_user.full_name,
            beneficiary_card_number=account_number,  # Store account number
            nickname=nickname if nickname else beneficiary_user.full_name
        )
        db.session.add(beneficiary)
        db.session.commit()
        
        flash(f'Beneficiary {beneficiary_user.full_name} added successfully', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding beneficiary: {str(e)}', 'danger')
    
    return redirect(url_for('beneficiaries'))

@app.route('/beneficiary/<int:beneficiary_id>/toggle-favorite', methods=['POST'])
@approved_required
def toggle_favorite(beneficiary_id):
    user_id = session.get('user_id')
    beneficiary = db.session.get(Beneficiary, beneficiary_id)
    
    if not beneficiary or beneficiary.user_id != user_id:
        return jsonify({'success': False, 'message': 'Beneficiary not found'}), 404
    
    beneficiary.is_favorite = not beneficiary.is_favorite
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'is_favorite': beneficiary.is_favorite,
        'message': 'Favorite status updated'
    })

@app.route('/beneficiary/<int:beneficiary_id>/delete', methods=['POST'])
@approved_required
def delete_beneficiary(beneficiary_id):
    user_id = session.get('user_id')
    beneficiary = db.session.get(Beneficiary, beneficiary_id)
    
    if not beneficiary or beneficiary.user_id != user_id:
        return jsonify({'success': False, 'message': 'Beneficiary not found'}), 404
    
    db.session.delete(beneficiary)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Beneficiary deleted successfully'})
