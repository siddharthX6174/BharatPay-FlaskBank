from app import app, db
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app.models.user import User, ProfileChangeLog
from app.decorators import approved_required
from datetime import datetime

@app.route('/profile')
@approved_required
def profile():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    
    # Get pending profile changes
    pending_changes = ProfileChangeLog.query.filter_by(
        user_id=user_id, 
        status='pending'
    ).order_by(ProfileChangeLog.requested_at.desc()).all()
    
    # Get change history
    change_history = ProfileChangeLog.query.filter_by(
        user_id=user_id
    ).order_by(ProfileChangeLog.requested_at.desc()).limit(10).all()
    
    return render_template('user/profile.html', 
                         user=user, 
                         pending_changes=pending_changes,
                         change_history=change_history)

@app.route('/profile/update', methods=['POST'])
@approved_required
def update_profile():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    
    # Fields that require admin approval
    sensitive_fields = ['address', 'city', 'state', 'pincode', 'phone']
    # Fields that can be updated immediately
    non_sensitive_fields = ['full_name']
    
    has_sensitive_changes = False
    changes_made = []
    
    # Process form data
    for field in sensitive_fields + non_sensitive_fields:
        new_value = request.form.get(field, '').strip()
        old_value = getattr(user, field) or ''
        
        # Skip if no change
        if new_value == old_value:
            continue
        
        # Create change log entry
        if field in sensitive_fields:
            # Sensitive fields require approval
            change_log = ProfileChangeLog(
                user_id=user_id,
                field_name=field,
                old_value=old_value,
                new_value=new_value,
                change_type='update',
                status='pending'
            )
            db.session.add(change_log)
            has_sensitive_changes = True
            changes_made.append(field)
        else:
            # Non-sensitive fields update immediately
            setattr(user, field, new_value)
            change_log = ProfileChangeLog(
                user_id=user_id,
                field_name=field,
                old_value=old_value,
                new_value=new_value,
                change_type='update',
                status='approved',
                reviewed_at=datetime.now()
            )
            db.session.add(change_log)
            changes_made.append(field)
    
    if changes_made:
        if has_sensitive_changes:
            user.profile_update_pending = True
            flash(f'Profile update request submitted for: {", ".join(changes_made)}. Waiting for admin approval.', 'info')
        else:
            flash('Profile updated successfully!', 'success')
        
        user.updated_at = datetime.now()
        db.session.commit()
    else:
        flash('No changes detected', 'info')
    
    return redirect(url_for('profile'))

@app.route('/profile/changes/<int:change_id>/cancel', methods=['POST'])
@approved_required
def cancel_profile_change(change_id):
    user_id = session.get('user_id')
    change = db.session.get(ProfileChangeLog, change_id)
    
    if not change or change.user_id != user_id:
        return jsonify({'success': False, 'message': 'Change request not found'}), 404
    
    if change.status != 'pending':
        return jsonify({'success': False, 'message': 'Only pending changes can be cancelled'}), 400
    
    db.session.delete(change)
    
    # Check if there are other pending changes
    remaining_pending = ProfileChangeLog.query.filter_by(
        user_id=user_id, 
        status='pending'
    ).count()
    
    if remaining_pending == 0:
        user = db.session.get(User, user_id)
        user.profile_update_pending = False
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Change request cancelled'})
