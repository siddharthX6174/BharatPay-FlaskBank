from app import app, db
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from app.models.user import User, ProfileChangeLog
from app.models.user.transaction import Transaction
from app.decorators import admin_required
from datetime import datetime, timedelta
from sqlalchemy import func


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    user_id = session.get('user_id')
    admin = db.session.get(User, user_id)
    
    # Get statistics
    total_users = User.query.filter_by(role='user').count()
    pending_users = User.query.filter_by(status='pending', role='user').count()
    approved_users = User.query.filter_by(status='approved', role='user').count()
    rejected_users = User.query.filter_by(status='rejected', role='user').count()
    
    # Get total balance across all users
    total_balance = db.session.query(func.sum(User.balance)).filter_by(role='user').scalar() or 0
    
    # Get recent transactions
    recent_transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(10).all()
    
    # Get transaction statistics (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    total_transactions = Transaction.query.filter(Transaction.timestamp >= thirty_days_ago).count()
    transaction_volume = db.session.query(func.sum(Transaction.amount)).filter(Transaction.timestamp >= thirty_days_ago).scalar() or 0
    
    # Get pending users list
    pending_users_list = User.query.filter_by(status='pending', role='user').order_by(User.created_at.desc()).all()
    
    # Get pending profile changes count
    pending_profile_changes = ProfileChangeLog.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html', 
                         admin=admin,
                         total_users=total_users,
                         pending_users=pending_users,
                         approved_users=approved_users,
                         rejected_users=rejected_users,
                         total_balance=total_balance,
                         recent_transactions=recent_transactions,
                         total_transactions=total_transactions,
                         transaction_volume=transaction_volume,
                         pending_users_list=pending_users_list,
                         pending_profile_changes=pending_profile_changes)

@app.route('/admin/users')
@admin_required
def admin_users():
    user_id = session.get('user_id')
    admin = db.session.get(User, user_id)
    
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('search', '')
    
    # Build query
    query = User.query.filter_by(role='user')
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if search_query:
        query = query.filter(
            (User.full_name.ilike(f'%{search_query}%')) | 
            (User.email.ilike(f'%{search_query}%')) |
            (User.card_number.ilike(f'%{search_query}%')) |
            (User.account_number.ilike(f'%{search_query}%'))
        )
    
    users = query.order_by(User.created_at.desc()).all()
    
    return render_template('admin/users.html', admin=admin, users=users, status_filter=status_filter, search_query=search_query)

@app.route('/admin/user/<int:user_id>/approve', methods=['POST'])
@admin_required
def approve_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    admin_id = session.get('user_id')
    user.status = 'approved'
    user.approved_at = datetime.now()
    user.approved_by = admin_id
    
    db.session.commit()
    
    flash(f'User {user.full_name} has been approved', 'success')
    return jsonify({'success': True, 'message': 'User approved successfully'})

@app.route('/admin/user/<int:user_id>/reject', methods=['POST'])
@admin_required
def reject_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    user.status = 'rejected'
    db.session.commit()
    
    flash(f'User {user.full_name} has been rejected', 'warning')
    return jsonify({'success': True, 'message': 'User rejected successfully'})

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    # Prevent deleting admin users
    if user.role == 'admin':
        return jsonify({'success': False, 'message': 'Cannot delete admin users'}), 403
    
    try:
        # Relationships with cascades in models/user.py handle the deletion of:
        # - Beneficiaries
        # - TransactionLimits
        # - Notifications
        # - ProfileChangeLogs (sent by user)
        # - Transactions (sent by user)
        
        # We still need to handle the 'reviewed_by' reference in change logs
        ProfileChangeLog.query.filter_by(reviewed_by=user_id).update({'reviewed_by': None})
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        flash(f'User {user.full_name} has been deleted', 'info')
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'User deletion failed: {str(e)}')
        return jsonify({'success': False, 'message': 'Deletion failed'}), 500

@app.route('/admin/transactions')
@admin_required
def admin_transactions():
    user_id = session.get('user_id')
    admin = db.session.get(User, user_id)
    
    # Get filter parameters
    transaction_type = request.args.get('type', 'all')
    date_filter = request.args.get('date', 'all')
    
    # Build query
    query = Transaction.query
    
    if transaction_type != 'all':
        query = query.filter_by(type=transaction_type)
    
    if date_filter == 'today':
        today = datetime.now().date()
        query = query.filter(func.date(Transaction.timestamp) == today)
    elif date_filter == 'week':
        week_ago = datetime.now() - timedelta(days=7)
        query = query.filter(Transaction.timestamp >= week_ago)
    elif date_filter == 'month':
        month_ago = datetime.now() - timedelta(days=30)
        query = query.filter(Transaction.timestamp >= month_ago)
    
    transactions = query.order_by(Transaction.timestamp.desc()).limit(100).all()
    
    return render_template('admin/transactions.html', 
                         admin=admin, 
                         transactions=transactions,
                         transaction_type=transaction_type,
                         date_filter=date_filter)

@app.route('/admin/settings')
@admin_required
def admin_settings():
    user_id = session.get('user_id')
    admin = db.session.get(User, user_id)
    
    return render_template('admin/settings.html', admin=admin)

@app.route('/admin/profile-changes')
@admin_required
def admin_profile_changes():
    user_id = session.get('user_id')
    admin = db.session.get(User, user_id)
    
    # Get filter parameter
    status_filter = request.args.get('status', 'pending')
    
    # Build query
    query = ProfileChangeLog.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    # Get all profile changes with user info
    changes = query.order_by(ProfileChangeLog.requested_at.desc()).limit(100).all()
    
    # Get counts for stats
    pending_count = ProfileChangeLog.query.filter_by(status='pending').count()
    approved_count = ProfileChangeLog.query.filter_by(status='approved').count()
    rejected_count = ProfileChangeLog.query.filter_by(status='rejected').count()
    
    return render_template('admin/profile_changes.html',
                         admin=admin,
                         changes=changes,
                         status_filter=status_filter,
                         pending_count=pending_count,
                         approved_count=approved_count,
                         rejected_count=rejected_count)

@app.route('/admin/profile-change/<int:change_id>/approve', methods=['POST'])
@admin_required
def approve_profile_change(change_id):
    user_id = session.get('user_id')
    change = db.session.get(ProfileChangeLog, change_id)
    
    if not change:
        return jsonify({'success': False, 'message': 'Change request not found'}), 404
    
    # Apply the change to the user
    user = db.session.get(User, change.user_id)
    if user:
        setattr(user, change.field_name, change.new_value)
        user.updated_at = datetime.now()
    
    # Update change log
    change.status = 'approved'
    change.reviewed_at = datetime.now()
    change.reviewed_by = user_id
    
    # Check if there are other pending changes for this user
    remaining_pending = ProfileChangeLog.query.filter_by(
        user_id=change.user_id,
        status='pending'
    ).count()
    
    if remaining_pending == 1:  # This is the last one
        user.profile_update_pending = False
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Profile change approved successfully'})

@app.route('/admin/profile-change/<int:change_id>/reject', methods=['POST'])
@admin_required
def reject_profile_change(change_id):
    user_id = session.get('user_id')
    change = db.session.get(ProfileChangeLog, change_id)
    
    if not change:
        return jsonify({'success': False, 'message': 'Change request not found'}), 404
    
    # Get admin notes from request
    data = request.get_json() or {}
    admin_notes = data.get('notes', '')
    
    # Update change log
    change.status = 'rejected'
    change.reviewed_at = datetime.now()
    change.reviewed_by = user_id
    change.admin_notes = admin_notes
    
    # Check if there are other pending changes for this user
    user = db.session.get(User, change.user_id)
    remaining_pending = ProfileChangeLog.query.filter_by(
        user_id=change.user_id,
        status='pending'
    ).count()
    
    if remaining_pending == 1:  # This is the last one
        user.profile_update_pending = False
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Profile change rejected'})

