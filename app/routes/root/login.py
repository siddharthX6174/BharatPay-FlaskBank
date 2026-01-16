from app import app, bcrypt, limiter
from flask import render_template, request, redirect, url_for, flash, session
from app.models.user import User



@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Limit login attempts
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Retrieve the user email from the db
        user = User.query.filter_by(email=email).first()

        # check for password
        if user and bcrypt.check_password_hash(user.password, password):
            # Check if user is approved
            if user.status != 'approved':
                flash('Your account is pending admin approval. Please wait for verification.', 'warning')
                return redirect(url_for('login'))
            
            session['user_id'] = user.id
            session['user_role'] = user.role
            session.permanent = True  # Use permanent session
            flash('Login successful', 'success')
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        
    return render_template('root/login.html')


@app.route('/logout')
def logout():
    # Clear the session data of the user
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home_page'))