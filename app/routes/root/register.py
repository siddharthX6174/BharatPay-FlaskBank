from app import app, bcrypt, db
from flask import render_template, request, flash, redirect, url_for, session
import random
from app.models.user import User
from app.utils.validators import sanitize_string, validate_email, validate_password_strength


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        # Sanitize inputs
        full_name = sanitize_string(request.form.get('full_name', ''))
        email = sanitize_string(request.form.get('email', ''), max_length=100).lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Onboarding fields
        phone = sanitize_string(request.form.get('phone', ''), max_length=20)
        address = sanitize_string(request.form.get('address', ''), max_length=500)
        city = sanitize_string(request.form.get('city', ''), max_length=100)
        state = sanitize_string(request.form.get('state', ''), max_length=100)
        pincode = sanitize_string(request.form.get('pincode', ''), max_length=10)
    
        # Validate email
        if not validate_email(email):
            flash('Please enter a valid email address', 'danger')
            return redirect(url_for('register_page'))
        
        # Validate name
        if len(full_name) < 2:
            flash('Please enter your full name', 'danger')
            return redirect(url_for('register_page'))
        
        # Validate phone
        if not phone or len(phone) < 10:
            flash('Please enter a valid phone number', 'danger')
            return redirect(url_for('register_page'))
        
        # Validate address fields
        if not address or not city or not state or not pincode:
            flash('Please complete all address fields', 'danger')
            return redirect(url_for('register_page'))
        
        # Password validation
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register_page'))
        
        # Strong password validation
        valid, error = validate_password_strength(password)
        if not valid:
            flash(error, 'danger')
            return redirect(url_for('register_page'))
        
        # check if email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('An account with this email already exists', 'danger')
            return redirect(url_for('login'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Generate permanent account number (starts with ACC)
        account_number = 'ACC' + ''.join([str(random.randint(0, 9)) for _ in range(13)])
        
        # Generate a card number
        card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])

        # create a user with onboarding details
        new_user = User(
            full_name=full_name, 
            email=email, 
            password=hashed_password,
            account_number=account_number,
            card_number=card_number,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            status='pending'  # Set to pending for admin approval
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Your account is pending admin approval.', 'success')
        return redirect(url_for('login'))
    

    return render_template('root/register.html')
