from app import db
from app.models.user import User, Transaction
from sqlalchemy import func

def get_global_stats():
    """
    Returns global statistics for the application to be displayed on root pages.
    """
    # Count of approved user role accounts
    total_users = User.query.filter_by(role='user', status='approved').count()
    
    # Total number of transactions
    total_transactions = Transaction.query.count()
    
    # Sum of all transaction amounts
    transaction_volume = db.session.query(func.sum(Transaction.amount)).scalar() or 0
    
    return {
        'total_users': total_users,
        'total_transactions': total_transactions,
        'transaction_volume': transaction_volume,
        'uptime': 99.9
    }

def get_user_insights(user_id):
    """
    Calculates financial insights for a specific user.
    """
    from datetime import datetime, timedelta
    
    # Category percentages
    types = ['transfer', 'deposit', 'recharge', 'withdrawal']
    category_counts = {}
    total_count = 0
    
    for t_type in types:
        count = Transaction.query.filter_by(user_id=user_id, type=t_type).count()
        category_counts[t_type] = count
        total_count += count
        
    category_percentages = {}
    if total_count > 0:
        for t_type in types:
            category_percentages[t_type] = round((category_counts[t_type] / total_count) * 100)
    else:
        category_percentages = {t: 0 for t in types}
        
    # Weekly activity (last 7 days)
    weekly_activity = []
    today = datetime.now()
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Total transaction amount for that day
        day_volume = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.timestamp >= day_start,
            Transaction.timestamp <= day_end
        ).scalar() or 0
        
        weekly_activity.append({
            'day': day.strftime('%a'),
            'volume': float(day_volume)
        })
        
    # Transaction count change (simplified: last 7 days vs previous 7 days)
    last_7_days = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.timestamp >= today - timedelta(days=7)
    ).count()
    previous_7_days = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.timestamp >= today - timedelta(days=14),
        Transaction.timestamp < today - timedelta(days=7)
    ).count()
    
    if previous_7_days > 0:
        transaction_change = round(((last_7_days - previous_7_days) / previous_7_days) * 100)
    else:
        transaction_change = 0 # Or some default if it's the first week
        
    balance_growth = 8 # Placeholder percentage
    
    # Month list for dropdown (last 6 months)
    available_months = []
    for i in range(5, -1, -1):
        m_date = today - timedelta(days=i*30)
        available_months.append(m_date.strftime('%B'))
        
    return {
        'category_percentages': category_percentages,
        'weekly_activity': weekly_activity,
        'balance_growth': balance_growth,
        'transaction_change': transaction_change,
        'current_month': today.strftime('%B'),
        'available_months': available_months
    }
