from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from extensions import mysql
from datetime import datetime
from utils.auth_utils import login_required
import traceback

review_bp = Blueprint('review', __name__)

@review_bp.route('/reviews')
def reviews():
    cursor = None
    try:
        # Step 1: Test database connection
        cursor = mysql.connection.cursor()
        
        # Step 2: Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = 10  # Number of reviews per page
        
        # Step 3: Count total public reviews for pagination
        cursor.execute('''
            SELECT COUNT(*) as total
            FROM reviews r
            WHERE r.is_public = 1
        ''')
        total_reviews = cursor.fetchone()['total']
        total_pages = (total_reviews + per_page - 1) // per_page  # Ceiling division
        
        # Step 4: Fetch public reviews for the current page
        offset = (page - 1) * per_page
        cursor.execute('''
            SELECT r.*, u.username, t.destination 
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            JOIN trips t ON r.trip_id = t.id
            WHERE r.is_public = 1
            ORDER BY r.created_at DESC
            LIMIT %s OFFSET %s
        ''', (per_page, offset))
        reviews = cursor.fetchall()
        
        # Step 5: Fetch user's trips if logged in
        user_trips = []
        user_reviews = []
        if session.get('user_id'):
            try:
                # Fetch user trips
                cursor.execute('''
                    SELECT id, destination 
                    FROM trips 
                    WHERE user_id = %s
                ''', (session['user_id'],))
                user_trips = cursor.fetchall()

                # Fetch user's reviews (public and private)
                cursor.execute('''
                    SELECT r.*, u.username, t.destination 
                    FROM reviews r
                    JOIN users u ON r.user_id = u.id
                    JOIN trips t ON r.trip_id = t.id
                    WHERE r.user_id = %s
                    ORDER BY r.created_at DESC
                ''', (session['user_id'],))
                user_reviews = cursor.fetchall()
            except Exception as trip_query_error:
                raise Exception(f"Failed to fetch user trips or reviews: {str(trip_query_error)}")
        
        # Step 6: Create a simple pagination object
        pagination = {
            'page': page,
            'pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'total': total_reviews
        }
        
        # Step 7: Render the template with pagination and user reviews
        return render_template('reviews.html', reviews=reviews, user_trips=user_trips, user_reviews=user_reviews, pagination=pagination)
    
    except Exception as e:
        # Log the full traceback to the console
        error_traceback = traceback.format_exc()
        print("Error in /reviews route:")
        print(error_traceback)
        
        # Render an error page with the detailed error message
        error_message = f"Error loading reviews: {str(e)}\n\nDetails:\n{error_traceback}"
        return render_template('error.html', error_message=error_message), 500
    
    finally:
        if cursor:
            cursor.close()

@review_bp.route('/reviews/new', methods=['POST'])
@login_required
def new_review():
    cursor = None
    try:
        # Get form data
        trip_id = request.form.get('trip_id')
        rating = request.form.get('rating')
        title = request.form.get('title')
        content = request.form.get('content')
        is_public = 'is_public' in request.form
        
        # Validate form data
        try:
            trip_id = int(trip_id)
            rating = int(rating)
            if not (1 <= rating <= 5):
                raise ValueError('Rating must be between 1 and 5')
            if not title or not content:
                raise ValueError('Title and content are required')
        except (ValueError, TypeError) as e:
            return jsonify({'success': False, 'message': str(e)}), 400
        
        cursor = mysql.connection.cursor()
        
        # Check if trip exists and belongs to user
        cursor.execute('''
            SELECT * FROM trips 
            WHERE id = %s AND user_id = %s
        ''', (trip_id, session['user_id']))
        trip = cursor.fetchone()
        
        if not trip:
            return jsonify({'success': False, 'message': 'Trip not found'}), 404
        
        # Check if review already exists
        cursor.execute('''
            SELECT * FROM reviews 
            WHERE trip_id = %s AND user_id = %s
        ''', (trip_id, session['user_id']))
        existing_review = cursor.fetchone()
        
        if existing_review:
            return jsonify({'success': False, 'message': 'You have already reviewed this trip'}), 400
        
        # Insert review into database
        cursor.execute('''
            INSERT INTO reviews (trip_id, user_id, rating, title, content, is_public) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (trip_id, session['user_id'], rating, title, content, is_public))
        mysql.connection.commit()
        
        # Fetch the newly created review for display
        cursor.execute('''
            SELECT r.*, u.username, t.destination 
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            JOIN trips t ON r.trip_id = t.id
            WHERE r.id = %s
        ''', (cursor.lastrowid,))
        new_review = cursor.fetchone()
        
        # Format the created_at date for display
        new_review['created_at'] = new_review['created_at'].strftime('%b %d, %Y')
        
        return jsonify({'success': True, 'review': new_review})
    except Exception as e:
        if 'cursor' in locals() and cursor:
            mysql.connection.rollback()
        return jsonify({'success': False, 'message': f'Failed to save review: {str(e)}'}), 500
    finally:
        if cursor:
            cursor.close()

@review_bp.route('/trips/<int:trip_id>/review', methods=['GET', 'POST'])
@login_required
def add_review(trip_id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        # Check if trip exists and belongs to user
        cursor.execute('''
            SELECT * FROM trips 
            WHERE id = %s AND user_id = %s
        ''', (trip_id, session['user_id']))
        trip = cursor.fetchone()
        
        if not trip:
            flash('Trip not found', 'danger')
            return redirect(url_for('trip.trips'))
        
        # Check if review already exists
        cursor.execute('''
            SELECT * FROM reviews 
            WHERE trip_id = %s AND user_id = %s
        ''', (trip_id, session['user_id']))
        existing_review = cursor.fetchone()
        
        if existing_review:
            flash('You have already reviewed this trip', 'info')
            return redirect(url_for('review.edit_review', review_id=existing_review['id']))
        
        if request.method == 'POST':
            # Get form data
            rating = request.form.get('rating')
            title = request.form.get('title')
            content = request.form.get('content')
            is_public = 'is_public' in request.form
            
            # Validate form data
            try:
                rating = int(rating)  # Convert to integer
                if not (1 <= rating <= 5):
                    raise ValueError('Rating must be between 1 and 5')
                if not title or not content:
                    raise ValueError('Title and content are required')
            except (ValueError, TypeError) as e:
                flash(str(e), 'danger')
                return render_template('add_review.html', trip=trip)
            
            # Insert review into database
            cursor.execute('''
                INSERT INTO reviews (trip_id, user_id, rating, title, content, is_public) 
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (trip_id, session['user_id'], rating, title, content, is_public))
            mysql.connection.commit()
            
            flash('Review added successfully!', 'success')
            return redirect(url_for('trip.view_trip', trip_id=trip_id))
        
        return render_template('add_review.html', trip=trip)
    except Exception as e:
        flash(f'Error adding review: {str(e)}', 'danger')
        return redirect(url_for('trip.trips'))
    finally:
        if cursor:
            cursor.close()

@review_bp.route('/reviews/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        # Get review details
        cursor.execute('''
            SELECT r.*, t.destination 
            FROM reviews r
            JOIN trips t ON r.trip_id = t.id
            WHERE r.id = %s AND r.user_id = %s
        ''', (review_id, session['user_id']))
        review = cursor.fetchone()
        
        if not review:
            flash('Review not found', 'danger')
            return redirect(url_for('review.reviews'))
        
        if request.method == 'POST':
            # Get form data
            rating = request.form.get('rating')
            title = request.form.get('title')
            content = request.form.get('content')
            is_public = 'is_public' in request.form
            
            # Validate form data
            try:
                rating = int(rating)  # Convert to integer
                if not (1 <= rating <= 5):
                    raise ValueError('Rating must be between 1 and 5')
                if not title or not content:
                    raise ValueError('Title and content are required')
            except (ValueError, TypeError) as e:
                flash(str(e), 'danger')
                return render_template('edit_review.html', review=review)
            
            # Update review in database
            cursor.execute('''
                UPDATE reviews 
                SET rating = %s, title = %s, content = %s, is_public = %s 
                WHERE id = %s
            ''', (rating, title, content, is_public, review_id))
            mysql.connection.commit()
            
            flash('Review updated successfully!', 'success')
            return redirect(url_for('trip.view_trip', trip_id=review['trip_id']))
        
        return render_template('edit_review.html', review=review)
    except Exception as e:
        flash(f'Error editing review: {str(e)}', 'danger')
        return redirect(url_for('review.reviews'))
    finally:
        if cursor:
            cursor.close()

@review_bp.route('/reviews/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        # Check if review exists and belongs to user
        cursor.execute('''
            SELECT * FROM reviews 
            WHERE id = %s AND user_id = %s
        ''', (review_id, session['user_id']))
        review = cursor.fetchone()
        
        if not review:
            flash('Review not found', 'danger')
            return redirect(url_for('review.reviews'))
        
        # Delete review
        cursor.execute('DELETE FROM reviews WHERE id = %s', (review_id,))
        mysql.connection.commit()
        
        flash('Review deleted successfully!', 'success')
        return redirect(url_for('trip.view_trip', trip_id=review['trip_id']))
    except Exception as e:
        if 'cursor' in locals() and cursor:
            mysql.connection.rollback()
        flash(f'Error deleting review: {str(e)}', 'danger')
        return redirect(url_for('review.reviews'))
    finally:
        if cursor:
            cursor.close()

@review_bp.route('/destinations/top-rated')
def top_rated_destinations():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        # Get top-rated destinations based on reviews
        cursor.execute('''
            SELECT t.destination, AVG(r.rating) as avg_rating, COUNT(r.id) as review_count
            FROM reviews r
            JOIN trips t ON r.trip_id = t.id
            GROUP BY t.destination
            HAVING review_count >= 3
            ORDER BY avg_rating DESC
            LIMIT 10
        ''')
        destinations = cursor.fetchall()
        
        return render_template('top_rated_destinations.html', destinations=destinations)
    except Exception as e:
        flash(f'Error loading top-rated destinations: {str(e)}', 'danger')
        return redirect(url_for('index'))
    finally:
        if cursor:
            cursor.close()

@review_bp.route('/reviews/helpful/<int:review_id>', methods=['POST'])
@login_required
def mark_review_helpful(review_id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        # Check if review exists
        cursor.execute('SELECT * FROM reviews WHERE id = %s', (review_id,))
        review = cursor.fetchone()
        
        if not review:
            return jsonify({'success': False, 'message': 'Review not found'}), 404
        
        # Check if user has already marked this review as helpful
        cursor.execute('''
            SELECT * FROM helpful_reviews 
            WHERE review_id = %s AND user_id = %s
        ''', (review_id, session['user_id']))
        existing = cursor.fetchone()
        
        if existing:
            # Remove helpful mark
            cursor.execute('''
                DELETE FROM helpful_reviews 
                WHERE review_id = %s AND user_id = %s
            ''', (review_id, session['user_id']))
            
            # Update helpful count
            cursor.execute('''
                UPDATE reviews 
                SET helpful_count = helpful_count - 1 
                WHERE id = %s
            ''', (review_id,))
            
            mysql.connection.commit()
            
            return jsonify({'success': True, 'helpful': False, 'count': review['helpful_count'] - 1})
        else:
            # Add helpful mark
            cursor.execute('''
                INSERT INTO helpful_reviews (review_id, user_id) 
                VALUES (%s, %s)
            ''', (review_id, session['user_id']))
            
            # Update helpful count
            cursor.execute('''
                UPDATE reviews 
                SET helpful_count = helpful_count + 1 
                WHERE id = %s
            ''', (review_id,))
            
            mysql.connection.commit()
            
            return jsonify({'success': True, 'helpful': True, 'count': review['helpful_count'] + 1})
    except Exception as e:
        if 'cursor' in locals() and cursor:
            mysql.connection.rollback()
        return jsonify({'success': False, 'message': f'Error marking review as helpful: {str(e)}'}), 500
    finally:
        if cursor:
            cursor.close()