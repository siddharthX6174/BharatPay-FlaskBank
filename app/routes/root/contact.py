from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.utils.validators import sanitize_string, validate_email


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = sanitize_string(request.form.get('name', ''))
        email = sanitize_string(request.form.get('email', ''), max_length=100)
        message = sanitize_string(request.form.get('message', ''), max_length=1000)
        
        if not name or not email or not message:
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('contact_page'))
        
        if not validate_email(email):
            flash('Please enter a valid email address', 'danger')
            return redirect(url_for('contact_page'))
        
        # Here you would save to database or send email
        # For now, just show success message
        app.logger.info(f'Contact form submission from {email}')
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact_page'))
    
    return render_template('root/contact.html')