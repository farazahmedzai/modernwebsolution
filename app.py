import os
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

@app.route('/')
def index():
    """Main homepage route"""
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    try:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        # Basic validation
        if not name or not email or not message:
            flash('All fields are required.', 'error')
            return redirect(url_for('index') + '#contact')
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('index') + '#contact')
        
        # In a real application, you would save this to a database or send an email
        # For now, we'll just log it and show a success message
        app.logger.info(f"Contact form submission: Name={name}, Email={email}, Message={message[:50]}...")
        
        flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        return redirect(url_for('index') + '#contact')
        
    except Exception as e:
        app.logger.error(f"Error processing contact form: {str(e)}")
        flash('An error occurred while sending your message. Please try again.', 'error')
        return redirect(url_for('index') + '#contact')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
