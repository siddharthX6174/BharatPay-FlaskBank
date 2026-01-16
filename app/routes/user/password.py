from app import app, db, bcrypt
from flask import render_template, request, redirect, url_for, session, flash
from app.models.user import User, Notification
from app.decorators import approved_required
from app.utils.validators import validate_password_strength
from datetime import datetime

@app.route('/change-password', methods=['GET', 'POST'])
@approved_required
def change_password():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate current password
        if not bcrypt.check_password_hash(user.password, current_password):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('change_password'))
        
        # Validate new password strength
        valid, error = validate_password_strength(new_password)
        if not valid:
            flash(error, 'warning')
            return redirect(url_for('change_password'))
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return redirect(url_for('change_password'))
        
        if current_password == new_password:
            flash('New password must be different from current password', 'warning')
            return redirect(url_for('change_password'))
        
        # Update password
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        user.updated_at = datetime.now()
        
        # Create notification
        notification = Notification(
            user_id=user_id,
            title='Password Changed',
            message='Your password has been changed successfully',
            type='security'
        )
        db.session.add(notification)
        
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('user/change_password.html', user=user)
