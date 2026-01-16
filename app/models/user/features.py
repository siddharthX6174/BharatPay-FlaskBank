from app import db
from datetime import datetime


class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    beneficiary_name = db.Column(db.String(200), nullable=False)
    beneficiary_card_number = db.Column(db.String(16), nullable=False)
    nickname = db.Column(db.String(100), nullable=True)  # Optional friendly name
    is_favorite = db.Column(db.Boolean, default=False)
    added_at = db.Column(db.DateTime, default=datetime.now)
    last_used = db.Column(db.DateTime, nullable=True)
    total_transactions = db.Column(db.Integer, default=0)
    
    # Relationship
    user = db.relationship('User', back_populates='beneficiaries')


class TransactionLimit(db.Model):
    __tablename__ = 'transaction_limits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    daily_limit = db.Column(db.Numeric(12, 2), default=100000.00)  # Daily transaction limit
    per_transaction_limit = db.Column(db.Numeric(12, 2), default=50000.00)  # Per transaction limit
    withdrawal_daily_limit = db.Column(db.Numeric(12, 2), default=50000.00)  # Daily ATM withdrawal limit
    is_active = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationship
    user = db.relationship('User', back_populates='transaction_limit', uselist=False)


class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'transaction', 'security', 'profile', 'admin'
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationship
    user = db.relationship('User', back_populates='notifications')
