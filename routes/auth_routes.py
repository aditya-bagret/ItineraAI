from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import re
from extensions import mysql, bcrypt
from utils.auth_utils import login_required

auth_bp = Blueprint('auth', __name__)

# User Registration
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validate form data
        if not username or not email or not password or not confirm_password:
            flash('Please fill out all fields', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        # Email validation
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address', 'danger')
            return render_template('register.html')
        
        # Password length validation
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template('register.html')
        
        cursor = None
        try:
            # Check if user already exists
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            if user:
                flash('Email already exists', 'danger')
                return render_template('register.html')
            
            # Hash password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            # Insert user into database
            cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', 
                          (username, email, hashed_password))
            mysql.connection.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error during registration: {str(e)}', 'danger')
            return render_template('register.html')
        finally:
            if cursor:
                cursor.close()
    
    return render_template('register.html')

# User Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']
        
        # Validate form data
        if not email or not password:
            flash('Please fill out all fields', 'danger')
            return render_template('login.html')
        
        cursor = None
        try:
            # Check if user exists
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            if not user:
                flash('Invalid email or password', 'danger')
                return render_template('login.html')
            
            # Check password
            if bcrypt.check_password_hash(user['password'], password):
                # Create session (align with login_required)
                session['logged_in'] = True
                session['user_id'] = user['id']
                session['username'] = user['username']
                # Check if user is admin (assuming 'is_admin' column exists in users table)
                session['is_admin'] = user.get('is_admin', 0) == 1
                
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password', 'danger')
                return render_template('login.html')
        except Exception as e:
            flash(f'Error during login: {str(e)}', 'danger')
            return render_template('login.html')
        finally:
            if cursor:
                cursor.close()
    
    return render_template('login.html')

# User Logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

# User Profile
@auth_bp.route('/profile')
@login_required
def profile():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
        user = cursor.fetchone()
        
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('auth.login'))
        
        return render_template('profile.html', user=user)
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))
    finally:
        if cursor:
            cursor.close()

# Update Profile
@auth_bp.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        
        # Validate form data
        if not username or not email:
            flash('Please fill out all fields', 'danger')
            return redirect(url_for('auth.update_profile'))
        
        # Email validation
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address', 'danger')
            return redirect(url_for('auth.update_profile'))
        
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            # Check if email is already taken by another user
            cursor.execute('SELECT * FROM users WHERE email = %s AND id != %s', (email, session['user_id']))
            existing_user = cursor.fetchone()
            
            if existing_user:
                flash('Email is already taken by another user', 'danger')
                return redirect(url_for('auth.update_profile'))
            
            # Update user in database
            cursor.execute('UPDATE users SET username = %s, email = %s WHERE id = %s', 
                          (username, email, session['user_id']))
            mysql.connection.commit()
            
            # Update session
            session['username'] = username
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('auth.profile'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')
            return redirect(url_for('auth.update_profile'))
        finally:
            if cursor:
                cursor.close()
    
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
        user = cursor.fetchone()
        
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('auth.login'))
        
        return render_template('update_profile.html', user=user)
    except Exception as e:
        flash(f'Error loading update profile page: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))
    finally:
        if cursor:
            cursor.close()