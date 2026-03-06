from app import db
from sqlalchemy import Numeric
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Sender/initiator
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Recipient user
    recipient_name = db.Column(db.String(200))
    recipient_card_number = db.Column(db.String(16))
    amount = db.Column(Numeric(12, 2), nullable=False)
    type = db.Column(db.String(25), nullable=False)  # 'transfer', 'deposit', 'recharge'
    status = db.Column(db.String(20), default='completed')  # 'completed', 'pending', 'failed'
    description = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], back_populates='sent_transactions')
    recipient = db.relationship('User', foreign_keys=[recipient_id])


class ProfileChangeLog(db.Model):
    __tablename__ = 'profile_change_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)  # Which field was changed
    old_value = db.Column(db.String(500), nullable=True)
    new_value = db.Column(db.String(500), nullable=True)
    change_type = db.Column(db.String(50), nullable=False)  # 'update', 'create', 'delete'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    requested_at = db.Column(db.DateTime, default=datetime.now)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    admin_notes = db.Column(db.String(500), nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], back_populates='profile_changes')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])