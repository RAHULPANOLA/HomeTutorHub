from flask import Flask, render_template, request, redirect, session, flash, Response, jsonify, url_for
from functools import wraps
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import razorpay
import hmac
import hashlib
import random
from flask_mail import Mail, Message
import random
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import json
import time
# -------------------------
# INITIALIZATION
# -------------------------
app = Flask(__name__)
app.secret_key = "secretkey"

# Get credentials from environment or use hardcoded for now
RAZORPAY_KEY_ID = "rzp_live_SnaTwHsV1pEsVj"
RAZORPAY_KEY_SECRET = "HYBkY1ZnQ8RRwy9H49PRYTOo"

# Initialize Razorpay client
try:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    print(f"Razorpay initialized successfully")
except Exception as e:
    print(f"Razorpay initialization failed: {e}")
    razorpay_client = None

print(f"Razorpay initialized with Key ID: {RAZORPAY_KEY_ID}")
# -------------------------
# DATABASE CONFIGURATION
# -------------------------
db_config = {
    'host': 'localhost',
    'user': 'hometuto_rahool',       
    'password': 'Rocko@1992',        
    'database': 'hometuto_teacher_portal', 
    'port': 3306 
}


# -------------------------
# DATABASE CONNECTION FUNCTION
# -------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

app.config['UPLOAD_FOLDER'] = 'static/payment_proofs'
app.config['RESUME_FOLDER'] = 'static/uploads/resumes'
app.config['PHOTO_FOLDER'] = 'static/uploads/profile_photos'

def dashboard_redirect():
    """Redirect to appropriate dashboard based on user type"""
    if 'student_id' in session:
        return redirect(url_for('search'))
    elif 'teacher_id' in session:
        return redirect(url_for('teacher_dashboard'))
    else:
        return redirect(url_for('home'))


# -------------------------
# MAIL CONFIGURATION
# -------------------------


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'hometutorhubindia@gmail.com'
app.config['MAIL_PASSWORD'] = 'rhyh vezz nquz pmqj'  # Your 16-digit App Password
app.config['MAIL_DEFAULT_SENDER'] = 'hometutorhubindia@gmail.com'

mail = Mail(app)



# -------------------------
# COMMON HELPERS
# -------------------------
@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Fetch CMS settings
    cur.execute("SELECT setting_key, setting_value FROM site_settings")
    settings_rows = cur.fetchall()
    settings = {row['setting_key']: row['setting_value'] for row in settings_rows}
    
    # Fetch active testimonials
    cur.execute("""
        SELECT * FROM testimonials 
        WHERE is_active = 1 
        ORDER BY display_order, created_at DESC 
        LIMIT 6
    """)
    testimonials = cur.fetchall()
    
    # Fetch social links
    social_links = {
        'facebook': settings.get('social_facebook', ''),
        'twitter': settings.get('social_twitter', ''),
        'instagram': settings.get('social_instagram', ''),
        'linkedin': settings.get('social_linkedin', '')
    }
    
    cur.close()
    conn.close()
    
    return render_template('index.html', 
                         settings=settings,
                         testimonials=testimonials,
                         social_links=social_links)
    
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect('/')  # This goes to your root home page directly


# -------------------------
# ADMIN SECTION
# -------------------------
# Admin login decorator
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login to access admin panel.', 'warning')
            return redirect(url_for('admin/login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper function to send email notifications
def send_email_notification(email, name, title, content):
    """Helper function to send email notifications"""
    try:
        # You can implement email sending here using Flask-Mail or any other service
        print(f"Email would be sent to {email}: {title}")
        # For now, just log it
        return True
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")
        return False

# Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM admin WHERE email = %s", (email,))
        admin = cur.fetchone()
        cur.close()
        conn.close()
        
        if admin and check_password_hash(admin['password'], password):
            session['admin_id'] = admin['id']
            session['admin_name'] = admin['full_name']
            session['admin_email'] = admin['email']
            flash('Welcome to Admin Panel!', 'success')
            return redirect(url_for('admin_dashboard'))  # FIXED: Use underscore
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('admin_login.html')
    
# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin_login'))

# Admin Dashboard
@app.route('/admin/dashboard')
@admin_login_required
def admin_dashboard():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    try:
        # Get total teachers
        cur.execute("SELECT COUNT(*) as total FROM teachers")
        result = cur.fetchone()
        total_teachers = result['total'] if result else 0
        
        # Get total students
        cur.execute("SELECT COUNT(*) as total FROM students")
        result = cur.fetchone()
        total_students = result['total'] if result else 0
        
        # Get active teachers
        cur.execute("SELECT COUNT(*) as total FROM teachers WHERE status = 'active' AND is_verified = 1")
        result = cur.fetchone()
        active_teachers = result['total'] if result else 0
        
        # In admin_dashboard route, add:
        cur.execute("""
            SELECT subject, COUNT(*) as request_count, 
                   SUM((SELECT COUNT(*) FROM unlocked_leads WHERE request_id = tr.id)) as total_views
            FROM tuition_requests tr
            WHERE status = 'Open'
            GROUP BY subject
            ORDER BY request_count DESC
            LIMIT 5
        """)
        popular_request_subjects = cur.fetchall()
        
        # New registrations (last 30 days)
        cur.execute("""
            SELECT COUNT(*) as count FROM students 
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """)
        result = cur.fetchone()
        new_students = result['count'] if result else 0
        
        cur.execute("""
            SELECT COUNT(*) as count FROM teachers 
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """)
        result = cur.fetchone()
        new_teachers = result['count'] if result else 0
        
        cur.execute("SELECT COUNT(*) as count FROM feedback WHERE status = 'pending'")
        pending_feedback = cur.fetchone()
        pending_feedback_count = pending_feedback['count'] if pending_feedback else 0
        
        # Get recent feedback (last 5)
        cur.execute("""
        SELECT id, user_name, rating, title, status, created_at
        FROM feedback 
        ORDER BY created_at DESC 
        LIMIT 5
        """)
        recent_feedback = cur.fetchall()
        # Most popular subjects from search analytics (if table exists)
        try:
            cur.execute("""
                SELECT search_term, search_count 
                FROM search_analytics 
                ORDER BY search_count DESC 
                LIMIT 10
            """)
            popular_subjects = cur.fetchall()
        except:
            popular_subjects = []
        
        # Online vs Offline tutors - FIXED: backticks around 'both'
        cur.execute("""
            SELECT 
                SUM(CASE WHEN mode = 'Online' THEN 1 ELSE 0 END) as online,
                SUM(CASE WHEN mode = 'Offline' THEN 1 ELSE 0 END) as offline,
                SUM(CASE WHEN mode = 'Both' THEN 1 ELSE 0 END) as `both`
            FROM teachers 
            WHERE status = 'active'
        """)
        tutor_modes = cur.fetchone()
        
        # If no data, set defaults
        if not tutor_modes:
            tutor_modes = {'online': 0, 'offline': 0, 'both': 0}
            

        
        # Recent activities (if table exists)
        try:
            cur.execute("""
                SELECT * FROM admin_logs 
                ORDER BY created_at DESC 
                LIMIT 10
            """)
            recent_activities = cur.fetchall()
        except:
            recent_activities = []
        
        cur.close()
        conn.close()
        
        return render_template("admin_dashboard.html", 
                             total_teachers=total_teachers,
                             total_students=total_students,
                             active_teachers=active_teachers,
                             new_students=new_students,
                             new_teachers=new_teachers,
                             popular_subjects=popular_subjects,
                             tutor_modes=tutor_modes,
                             recent_activities=recent_activities,
                             pending_feedback_count=pending_feedback_count,
                             recent_feedback=recent_feedback)
    
    except Exception as e:
        print(f"Error in admin_dashboard: {e}")
        flash('Error loading dashboard', 'danger')
        return redirect(url_for('admin_login'))
        
        
# Admin - View Student Details
@app.route('/admin/view_student/<int:student_id>')
@admin_login_required
def admin_view_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Exclude password and security_answer
    cur.execute("""
        SELECT id, full_name, email, phone, father_name, father_phone, 
               mother_name, mother_phone, city, state, pincode, address, 
               qualification, specialization, security_question, points, 
               created_at
        FROM students 
        WHERE id = %s
    """, (student_id,))
    student = cur.fetchone()
    
    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for('admin_students'))
    
    cur.close()
    conn.close()
    
    return render_template('admin_view_student.html', student=student)

# Admin - View Teacher Details
@app.route('/admin/view_teacher/<int:teacher_id>')
@admin_login_required
def admin_view_teacher(teacher_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Exclude password and security_answer
    cur.execute("""
        SELECT id, full_name, email, phone, whatsapp, alt_phone, gender, dob,
               city, state, pincode, address, locality, aadhaar,
               qualification, specialization, university, passing_year,
               subjects, classes, boards, experience, exp_type, mode,
               timing, pref_area, monthly_fee, hourly_fee, languages,
               special_skills, photo, resume, my_points, status, is_verified,
               created_at
        FROM teachers 
        WHERE id = %s
    """, (teacher_id,))
    teacher = cur.fetchone()
    
    if not teacher:
        flash("Teacher not found!", "danger")
        return redirect(url_for('admin_teachers'))
    
    # Get subjects from teacher_subjects table
    cur.execute("SELECT subject_name FROM teacher_subjects WHERE teacher_id = %s", (teacher_id,))
    subjects = cur.fetchall()
    teacher['subjects_list'] = [s['subject_name'] for s in subjects]
    
    cur.close()
    conn.close()
    
    return render_template('admin_view_teacher.html', teacher=teacher)

# Admin Teachers Management
@app.route('/admin/teachers')
@admin_login_required
def admin_teachers():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = """
        SELECT t.*, 
               GROUP_CONCAT(DISTINCT ts.subject_name) as all_subjects
        FROM teachers t
        LEFT JOIN teacher_subjects ts ON t.id = ts.teacher_id
        WHERE 1=1
    """
    params = []
    
    if search:
        query += " AND (t.full_name LIKE %s OR t.email LIKE %s OR t.city LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    
    if status:
        query += " AND t.status = %s"
        params.append(status)
    
    query += " GROUP BY t.id ORDER BY t.created_at DESC"
    
    cur.execute(query, params)
    teachers = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('admin_teachers.html', teachers=teachers, search=search, status=status)

# Toggle Teacher Status
@app.route('/admin/toggle_teacher/<int:teacher_id>')
@admin_login_required
def admin_toggle_teacher(teacher_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("SELECT status FROM teachers WHERE id = %s", (teacher_id,))
    teacher = cur.fetchone()
    
    if teacher:
        new_status = 'blocked' if teacher['status'] == 'active' else 'active'
        cur.execute("UPDATE teachers SET status = %s WHERE id = %s", (new_status, teacher_id))
        conn.commit()
        flash(f'Teacher has been {new_status}.', 'success')
    
    cur.close()
    conn.close()
    
    return redirect(url_for('admin_teachers'))

# Delete Teacher
@app.route('/admin/delete_teacher/<int:teacher_id>', methods=['POST'])
@admin_login_required
def admin_delete_teacher(teacher_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    flash('Teacher deleted successfully!', 'success')
    return redirect(url_for('admin_teachers'))

# Admin Students Management
@app.route('/admin/students')
@admin_login_required
def admin_students():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    search = request.args.get('search', '')
    
    query = "SELECT * FROM students WHERE 1=1"
    params = []
    
    if search:
        query += " AND (full_name LIKE %s OR email LIKE %s OR city LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    
    query += " ORDER BY created_at DESC"
    
    cur.execute(query, params)
    students = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('admin_students.html', students=students, search=search)

# Delete Student
@app.route('/admin/delete_student/<int:student_id>', methods=['POST'])
@admin_login_required
def admin_delete_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('admin_students'))

# Download Teachers Excel

@app.route('/admin/download_teachers')
@admin_login_required
def admin_download_teachers():
    import csv
    from io import StringIO
    
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("""
        SELECT t.id, t.full_name, t.email, t.phone, t.city, t.qualification, 
               t.experience, t.mode, t.status, t.created_at,
               GROUP_CONCAT(ts.subject_name) as subjects
        FROM teachers t
        LEFT JOIN teacher_subjects ts ON t.id = ts.teacher_id
        GROUP BY t.id
        ORDER BY t.created_at DESC
    """)
    teachers = cur.fetchall()
    cur.close()
    conn.close()
    
    if not teachers:
        flash('No teacher data to export', 'warning')
        return redirect(url_for('admin_teachers'))
    
    # Create CSV output
    output = StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'City', 'Qualification', 
                     'Experience (Years)', 'Mode', 'Status', 'Registration Date', 'Subjects'])
    
    # Write data
    for t in teachers:
        writer.writerow([
            t['id'], t['full_name'], t['email'], t['phone'] or '', 
            t['city'] or '', t['qualification'] or '', t['experience'] or 0,
            t['mode'] or '', t['status'], t['created_at'], t['subjects'] or ''
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=teachers.csv'}
    )
    
@app.route('/admin/download_students')
@admin_login_required
def admin_download_students():
    import csv
    from io import StringIO
    
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("""
        SELECT id, full_name, email, phone, city, qualification, 
               specialization, points, created_at
        FROM students
        ORDER BY created_at DESC
    """)
    students = cur.fetchall()
    cur.close()
    conn.close()
    
    if not students:
        flash('No student data to export', 'warning')
        return redirect(url_for('admin_students'))
    
    # Create CSV output
    output = StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'City', 'Qualification', 
                     'Subject Needed', 'Points', 'Registration Date'])
    
    # Write data
    for s in students:
        writer.writerow([
            s['id'], s['full_name'], s['email'], s['phone'] or '', 
            s['city'] or '', s['qualification'] or '', s['specialization'] or '',
            s['points'] or 0, s['created_at']
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=students.csv'}
    )

# Announcements
def get_active_announcements(target_audience='all', limit=5):
    """Fetch active announcements for display on dashboards"""
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    query = """
        SELECT * FROM announcements 
        WHERE target_audience IN ('all', %s)
        ORDER BY created_at DESC 
        LIMIT %s
    """
    cur.execute(query, (target_audience, limit))
    announcements = cur.fetchall()
    
    cur.close()
    conn.close()
    return announcements
    
@app.route('/admin/announcements')
@admin_login_required
def admin_announcements():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    category = request.args.get('category', '')
    target = request.args.get('target', '')
    
    query = """
        SELECT a.*, ad.full_name as admin_name 
        FROM announcements a
        LEFT JOIN admin ad ON a.created_by = ad.id
        WHERE 1=1
    """
    params = []
    
    if category:
        query += " AND a.category = %s"
        params.append(category)
    
    if target:
        query += " AND a.target_audience = %s"
        params.append(target)
    
    query += " ORDER BY a.created_at DESC"
    
    cur.execute(query, params)
    announcements = cur.fetchall()
    
    # Get statistics
    cur.execute("SELECT COUNT(*) as total FROM announcements")
    total = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as total FROM announcements WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)")
    recent = cur.fetchone()['total']
    
    cur.execute("""
        SELECT category, COUNT(*) as count 
        FROM announcements 
        GROUP BY category
    """)
    category_stats = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('admin_announcements.html', 
                         announcements=announcements,
                         total=total,
                         recent=recent,
                         category_stats=category_stats,
                         selected_category=category,
                         selected_target=target)

# Send Announcement
@app.route('/admin/send_announcement', methods=['POST'])
@admin_login_required
def send_announcement():
    title = request.form.get('title')
    content = request.form.get('content')
    category = request.form.get('category')
    target = request.form.get('target')
    send_email = request.form.get('send_email') == 'on'
    
    if not title or not content:
        flash('Please fill in all required fields.', 'danger')
        return redirect(url_for('admin_announcements'))
    
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    try:
        cur.execute("""
            INSERT INTO announcements (title, content, category, target_audience, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, content, category, target, session['admin_id']))
        
        conn.commit()
        flash('Announcement sent successfully!', 'success')
        
    except Exception as e:
        conn.rollback()
        print(f"Error sending announcement: {e}")
        flash('Error sending announcement. Please try again.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_announcements'))

# Delete Announcement
@app.route('/admin/delete_announcement/<int:id>', methods=['POST'])
@admin_login_required
def delete_announcement(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM announcements WHERE id = %s", (id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    flash('Announcement deleted successfully!', 'success')
    return redirect(url_for('admin_announcements'))

# CMS Settings
# -------------------------
# CMS - Content Management System
# -------------------------

@app.route('/admin/cms')
@admin_login_required
def admin_cms():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Get all site settings
    cur.execute("SELECT setting_key, setting_value, setting_type FROM site_settings")
    settings_rows = cur.fetchall()
    settings = {row['setting_key']: row for row in settings_rows}
    
    # Get testimonials
    cur.execute("SELECT * FROM testimonials ORDER BY display_order, created_at DESC")
    testimonials = cur.fetchall()
    
    # Get FAQs
    cur.execute("SELECT * FROM faqs ORDER BY display_order, created_at DESC")
    faqs = cur.fetchall()
    
    # Get featured tutors
    cur.execute("""
        SELECT ft.*, t.full_name, t.qualification, t.city, t.photo, t.experience
        FROM featured_tutors ft
        JOIN teachers t ON ft.teacher_id = t.id
        WHERE t.status = 'active'
        ORDER BY ft.display_order
    """)
    featured_tutors = cur.fetchall()
    
    # Get all active teachers for featured tutors dropdown
    cur.execute("SELECT id, full_name, qualification, city FROM teachers WHERE status = 'active' ORDER BY full_name")
    all_teachers = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('admin_cms.html', 
                         settings=settings,
                         testimonials=testimonials,
                         faqs=faqs,
                         featured_tutors=featured_tutors,
                         all_teachers=all_teachers)

@app.route('/admin/cms/update_settings', methods=['POST'])
@admin_login_required
def update_cms_settings():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Update general settings
        home_hero_title = request.form.get('home_hero_title', '')
        home_hero_subtitle = request.form.get('home_hero_subtitle', '')
        home_hero_button_text = request.form.get('home_hero_button_text', '')
        about_content = request.form.get('about_content', '')
        contact_email = request.form.get('contact_email', '')
        contact_phone = request.form.get('contact_phone', '')
        contact_address = request.form.get('contact_address', '')
        footer_copyright = request.form.get('footer_copyright', '')
        meta_description = request.form.get('meta_description', '')
        meta_keywords = request.form.get('meta_keywords', '')
        
        # Save settings
        settings_data = {
            'home_hero_title': home_hero_title,
            'home_hero_subtitle': home_hero_subtitle,
            'home_hero_button_text': home_hero_button_text,
            'about_content': about_content,
            'contact_email': contact_email,
            'contact_phone': contact_phone,
            'contact_address': contact_address,
            'footer_copyright': footer_copyright,
            'meta_description': meta_description,
            'meta_keywords': meta_keywords
        }
        
        for key, value in settings_data.items():
            cur.execute("""
                INSERT INTO site_settings (setting_key, setting_value, setting_type) 
                VALUES (%s, %s, 'text')
                ON DUPLICATE KEY UPDATE setting_value = %s
            """, (key, value, value))
        
        conn.commit()
        flash('Website settings updated successfully!', 'success')
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating CMS settings: {e}")
        flash('Error updating settings. Please try again.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_cms'))

@app.route('/admin/cms/add_testimonial', methods=['POST'])
@admin_login_required
def add_testimonial():
    student_name = request.form.get('student_name')
    content = request.form.get('content')
    rating = request.form.get('rating', 5)
    display_order = request.form.get('display_order', 0)
    
    # Handle image upload
    photo_file = request.files.get('student_photo')
    photo_name = ''
    if photo_file and photo_file.filename != '':
        photo_name = secure_filename(photo_file.filename)
        photo_path = os.path.join('static/uploads/testimonials', photo_name)
        os.makedirs(os.path.dirname(photo_path), exist_ok=True)
        photo_file.save(photo_path)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO testimonials (student_name, student_image, content, rating, display_order, is_active)
            VALUES (%s, %s, %s, %s, %s, 1)
        """, (student_name, photo_name, content, rating, display_order))
        conn.commit()
        flash('Testimonial added successfully!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"Error adding testimonial: {e}")
        flash('Error adding testimonial.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_cms'))

@app.route('/admin/cms/edit_testimonial/<int:id>', methods=['POST'])
@admin_login_required
def edit_testimonial(id):
    student_name = request.form.get('student_name')
    content = request.form.get('content')
    rating = request.form.get('rating', 5)
    is_active = request.form.get('is_active') == 'on'
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE testimonials 
            SET student_name = %s, content = %s, rating = %s, is_active = %s
            WHERE id = %s
        """, (student_name, content, rating, is_active, id))
        conn.commit()
        flash('Testimonial updated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"Error updating testimonial: {e}")
        flash('Error updating testimonial.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_cms'))

@app.route('/admin/cms/delete_testimonial/<int:id>', methods=['POST'])
@admin_login_required
def delete_testimonial(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM testimonials WHERE id = %s", (id,))
        conn.commit()
        flash('Testimonial deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"Error deleting testimonial: {e}")
        flash('Error deleting testimonial.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_cms'))

@app.route('/admin/cms/add_faq', methods=['POST'])
@admin_login_required
def add_faq():
    question = request.form.get('question')
    answer = request.form.get('answer')
    category = request.form.get('category', 'general')
    display_order = request.form.get('display_order', 0)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO faqs (question, answer, category, display_order, is_active)
            VALUES (%s, %s, %s, %s, 1)
        """, (question, answer, category, display_order))
        conn.commit()
        flash('FAQ added successfully!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"Error adding FAQ: {e}")
        flash('Error adding FAQ.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_cms'))

@app.route('/admin/cms/edit_faq/<int:id>', methods=['POST'])
@admin_login_required
def edit_faq(id):
    question = request.form.get('question')
    answer = request.form.get('answer')
    category = request.form.get('category', 'general')
    display_order = request.form.get('display_order', 0)
    is_active = request.form.get('is_active') == 'on'
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE faqs 
            SET question = %s, answer = %s, category = %s, display_order = %s, is_active = %s
            WHERE id = %s
        """, (question, answer, category, display_order, is_active, id))
        conn.commit()
        flash('FAQ updated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"Error updating FAQ: {e}")
        flash('Error updating FAQ.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_cms'))

@app.route('/admin/cms/delete_faq/<int:id>', methods=['POST'])
@admin_login_required
def delete_faq(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM faqs WHERE id = %s", (id,))
        conn.commit()
        flash('FAQ deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"Error deleting FAQ: {e}")
        flash('Error deleting FAQ.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_cms'))

@app.route('/admin/cms/add_featured_tutor', methods=['POST'])
@admin_login_required
def add_featured_tutor():
    teacher_id = request.form.get('teacher_id')
    display_order = request.form.get('display_order', 0)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO featured_tutors (teacher_id, display_order)
            VALUES (%s, %s)
        """, (teacher_id, display_order))
        conn.commit()
        flash('Featured tutor added successfully!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"Error adding featured tutor: {e}")
        flash('Error adding featured tutor.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_cms'))

@app.route('/admin/cms/remove_featured_tutor/<int:id>', methods=['POST'])
@admin_login_required
def remove_featured_tutor(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM featured_tutors WHERE id = %s", (id,))
        conn.commit()
        flash('Featured tutor removed successfully!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"Error removing featured tutor: {e}")
        flash('Error removing featured tutor.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_cms'))

@app.route('/admin/cms/update_social_links', methods=['POST'])
@admin_login_required
def update_social_links():
    facebook = request.form.get('facebook', '')
    twitter = request.form.get('twitter', '')
    instagram = request.form.get('instagram', '')
    linkedin = request.form.get('linkedin', '')
    youtube = request.form.get('youtube', '')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        social_data = {
            'social_facebook': facebook,
            'social_twitter': twitter,
            'social_instagram': instagram,
            'social_linkedin': linkedin,
            'social_youtube': youtube
        }
        
        for key, value in social_data.items():
            cur.execute("""
                INSERT INTO site_settings (setting_key, setting_value, setting_type) 
                VALUES (%s, %s, 'text')
                ON DUPLICATE KEY UPDATE setting_value = %s
            """, (key, value, value))
        
        conn.commit()
        flash('Social media links updated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"Error updating social links: {e}")
        flash('Error updating social links.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_cms'))
# Backup
@app.route('/admin/backup')
@admin_login_required
def admin_backup():
    return render_template('admin_backup.html')

@app.route('/admin/export_db')
@admin_login_required
def export_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"backup_{timestamp}.sql"
    
    # MySQL credentials
    db_config = {
        'host': 'localhost',
        'user': 'hometuto_rahool',
        'password': 'Rocko@1992',
        'database': 'hometuto_teacher_portal'
    }
    
    # Create backup using mysqldump
    dump_cmd = f"mysqldump -h {db_config['host']} -u {db_config['user']} -p{db_config['password']} {db_config['database']} > /tmp/{backup_file}"
    os.system(dump_cmd)
    
    return send_file(f"/tmp/{backup_file}", as_attachment=True, download_name=backup_file)    
    
# ==================== FEEDBACK ROUTES ====================

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Submit feedback page"""
    if 'student_id' not in session and 'teacher_id' not in session:
        flash("Please login to submit feedback.", "warning")
        return redirect(url_for('student_login'))
    
    if request.method == 'POST':
        user_id = session.get('student_id') or session.get('teacher_id')
        user_type = 'student' if 'student_id' in session else 'teacher'
        user_name = session.get('student_name') or session.get('teacher_name')
        rating = request.form.get('rating', type=int)
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        
        if not rating or not description:
            flash("Please provide rating and description.", "danger")
            return redirect(url_for('feedback'))
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                INSERT INTO feedback (user_id, user_type, user_name, rating, title, description, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'pending')
            """, (user_id, user_type, user_name, rating, title, description))
            conn.commit()
            flash("Thank you for your feedback! It will be reviewed by our team.", "success")
        except Exception as e:
            print(f"Error submitting feedback: {e}")
            flash("Error submitting feedback. Please try again.", "danger")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        
        # Direct redirect based on user type
        if 'student_id' in session:
            return redirect(url_for('search'))
        else:
            return redirect(url_for('teacher_dashboard'))
    
    return render_template('feedback_form.html')


@app.route('/admin/feedback')
@admin_login_required
def admin_feedback():
    """Admin view to manage feedback"""
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Get all feedback
    cur.execute("""
        SELECT f.*,
               CASE 
                   WHEN f.user_type = 'student' THEN s.points
                   ELSE t.my_points
               END as user_points
        FROM feedback f
        LEFT JOIN students s ON f.user_id = s.id AND f.user_type = 'student'
        LEFT JOIN teachers t ON f.user_id = t.id AND f.user_type = 'teacher'
        ORDER BY 
            CASE f.status 
                WHEN 'pending' THEN 1 
                WHEN 'approved' THEN 2 
                ELSE 3 
            END,
            f.created_at DESC
    """)
    feedbacks = cur.fetchall()
    
    # Get featured testimonials
    cur.execute("""
        SELECT t.*, f.rating, f.title
        FROM testimonials t
        LEFT JOIN feedback f ON t.feedback_id = f.id
        ORDER BY t.display_order
    """)
    featured = cur.fetchall()
    
    # Get statistics
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN rating = 5 THEN 1 ELSE 0 END) as five_star,
            SUM(CASE WHEN rating = 4 THEN 1 ELSE 0 END) as four_star,
            SUM(CASE WHEN rating = 3 THEN 1 ELSE 0 END) as three_star,
            SUM(CASE WHEN rating = 2 THEN 1 ELSE 0 END) as two_star,
            SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as one_star,
            AVG(rating) as avg_rating,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_count,
            SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved_count
        FROM feedback
    """)
    stats = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return render_template('admin_feedback.html', 
                         feedbacks=feedbacks, 
                         featured=featured,
                         stats=stats)


@app.route('/admin/update_feedback_status/<int:feedback_id>', methods=['POST'])
@admin_login_required
def update_feedback_status(feedback_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    status = request.form.get('status')
    admin_note = request.form.get('admin_note', '')
    
    try:
        cur.execute("""
            UPDATE feedback 
            SET status = %s, admin_note = %s, updated_at = NOW()
            WHERE id = %s
        """, (status, admin_note, feedback_id))
        conn.commit()
        flash(f'Feedback status updated to {status}.', 'success')
    except Exception as e:
        print(f"Error updating feedback: {e}")
        flash('Error updating feedback status.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_feedback'))


@app.route('/admin/feature_feedback/<int:feedback_id>', methods=['POST'])
@admin_login_required
def feature_feedback(feedback_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    try:
        # Get feedback details
        cur.execute("""
            SELECT user_name, user_type, rating, description, title
            FROM feedback WHERE id = %s
        """, (feedback_id,))
        feedback = cur.fetchone()
        
        if not feedback:
            flash('Feedback not found!', 'danger')
            return redirect(url_for('admin_feedback'))
        
        # Check if already featured
        cur.execute("SELECT id FROM testimonials WHERE feedback_id = %s", (feedback_id,))
        existing = cur.fetchone()
        
        if existing:
            cur.execute("DELETE FROM testimonials WHERE feedback_id = %s", (feedback_id,))
            flash('Removed from featured testimonials.', 'info')
        else:
            # Add to testimonials
            cur.execute("""
                INSERT INTO testimonials (feedback_id, user_name, user_type, content, rating)
                VALUES (%s, %s, %s, %s, %s)
            """, (feedback_id, feedback['user_name'], feedback['user_type'], 
                  feedback['description'], feedback['rating']))
            flash('Added to featured testimonials!', 'success')
        
        # Update feedback is_featured flag
        cur.execute("""
            UPDATE feedback SET is_featured = NOT is_featured WHERE id = %s
        """, (feedback_id,))
        
        conn.commit()
    except Exception as e:
        print(f"Error featuring feedback: {e}")
        flash('Error updating featured status.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_feedback'))


@app.route('/admin/delete_feedback/<int:feedback_id>', methods=['POST'])
@admin_login_required
def delete_feedback(feedback_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Also delete from testimonials if exists
        cur.execute("DELETE FROM testimonials WHERE feedback_id = %s", (feedback_id,))
        cur.execute("DELETE FROM feedback WHERE id = %s", (feedback_id,))
        conn.commit()
        flash('Feedback deleted successfully!', 'success')
    except Exception as e:
        print(f"Error deleting feedback: {e}")
        flash('Error deleting feedback.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_feedback'))


def get_featured_testimonials(limit=6):
    """Get featured testimonials for homepage"""
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("""
        SELECT * FROM testimonials 
        WHERE is_active = 1 
        ORDER BY display_order, created_at DESC 
        LIMIT %s
    """, (limit,))
    testimonials = cur.fetchall()
    
    cur.close()
    conn.close()
    return testimonials
        
@app.route('/admin/change_password', methods=['GET', 'POST'])
@admin_login_required
def admin_change_password():
    if request.method == 'POST':
        admin_id = session['admin_id']
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        
        try:
            cur.execute("SELECT password FROM admin WHERE id = %s", (admin_id,))
            admin = cur.fetchone()
            
            if not admin or not check_password_hash(admin['password'], current_password):
                flash("Current password is incorrect", "danger")
                return redirect(url_for('admin_change_password'))
            
            if new_password != confirm_password:
                flash("New passwords do not match", "warning")
                return redirect(url_for('admin_change_password'))
            
            if len(new_password) < 6:
                flash("Password must be at least 6 characters", "warning")
                return redirect(url_for('admin_change_password'))
            
            hashed_password = generate_password_hash(new_password)
            cur.execute("UPDATE admin SET password = %s WHERE id = %s", (hashed_password, admin_id))
            conn.commit()
            
            flash("Password updated successfully! Please login again.", "success")
            session.clear()
            return redirect(url_for('admin_login'))
            
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred. Please try again.", "danger")
        finally:
            cur.close()
            conn.close()
    
    return render_template("admin_change_password.html")
    
@app.route('/offline_request')
def offline_request_page():
    """Show offline tutor request form with auto-filled student data"""
    print("=== OFFLINE REQUEST PAGE CALLED ===")  # Debug print
    print(f"Session: {session}")
    
    if 'student_id' not in session:
        flash("Please login to request an offline tutor.", "warning")
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("""
        SELECT id, full_name, email, phone, city, address, qualification, specialization 
        FROM students WHERE id = %s
    """, (student_id,))
    student = cur.fetchone()
    
    print(f"Student found: {student}")  # Debug print
    
    cur.close()
    conn.close()
    
    return render_template('offline_request.html', student=student)
    


@app.route('/submit_offline_request', methods=['POST'])
def submit_offline_request():
    """Submit offline tutor request using auto-filled data"""
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    
    # Get data from form (only new inputs, not re-entered data)
    student_address = request.form.get('student_address')
    subject = request.form.get('subject')
    class_grade = request.form.get('class_grade')
    subject_interest = request.form.get('subject_interest')
    preferred_timing = request.form.get('preferred_timing')
    additional_info = request.form.get('additional_info')
    budget = request.form.get('budget')
    preferred_tutor_gender = request.form.get('preferred_tutor_gender', 'any')
    
    # Get student data from database (not from form)
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("""
        SELECT full_name, email, phone, city, address 
        FROM students WHERE id = %s
    """, (student_id,))
    student = cur.fetchone()
    
    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for('student_login'))
    
    try:
        cur.execute("""
            INSERT INTO offline_requests 
            (student_id, student_name, student_email, student_phone, student_address, 
             student_city, subject, class_grade, preferred_timing, additional_info, 
             budget, preferred_tutor_gender, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending')
        """, (student_id, student['full_name'], student['email'], student['phone'], 
              student_address or student['address'], student['city'], 
              subject_interest or subject, class_grade, preferred_timing, 
              additional_info, budget, preferred_tutor_gender))
        conn.commit()
        
        flash("Request submitted successfully! Our admin will contact you soon.", "success")
        
    except Exception as e:
        conn.rollback()
        print(f"Error submitting request: {e}")
        flash("Error submitting request. Please try again.", "danger")
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('search'))


@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")


# Admin - Close/Complete Offline Request
@app.route('/admin/close_offline_request/<int:request_id>', methods=['POST'])
@admin_login_required
def close_offline_request(request_id):
    """Mark offline request as completed"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Get request details for notification
        cur.execute("""
            SELECT student_name, student_email, student_phone, assigned_teacher_id 
            FROM offline_requests WHERE id = %s
        """, (request_id,))
        request_data = cur.fetchone()
        
        if request_data:
            # Update request status
            cur.execute("""
                UPDATE offline_requests 
                SET status = 'completed', updated_at = NOW()
                WHERE id = %s
            """, (request_id,))
            
            # If teacher assigned, update teacher's stats (optional)
            if request_data[3]:
                cur.execute("""
                    UPDATE teachers 
                    SET completed_offline_requests = COALESCE(completed_offline_requests, 0) + 1
                    WHERE id = %s
                """, (request_data[3],))
            
            conn.commit()
            
            # Optional: Send email/SMS notification to student
            # send_completion_notification(request_data[0], request_data[1], request_data[2])
            
            flash(f"Request #{request_id} marked as completed! Student has been notified.", "success")
        else:
            flash("Request not found!", "danger")
            
    except Exception as e:
        conn.rollback()
        print(f"Error closing request: {e}")
        flash("Error closing request.", "danger")
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_offline_requests'))

# Admin - Cancel Offline Request
@app.route('/admin/cancel_offline_request/<int:request_id>', methods=['POST'])
@admin_login_required
def cancel_offline_request(request_id):
    """Cancel offline request"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE offline_requests 
            SET status = 'cancelled', updated_at = NOW()
            WHERE id = %s
        """, (request_id,))
        conn.commit()
        
        flash(f"Request #{request_id} has been cancelled.", "warning")
        
    except Exception as e:
        conn.rollback()
        print(f"Error cancelling request: {e}")
        flash("Error cancelling request.", "danger")
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_offline_requests'))

# Student - View their offline request status
@app.route('/my_offline_requests')
def my_offline_requests():
    """Students can view status of their offline requests"""
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("""
        SELECT o.*, t.full_name as teacher_name, t.phone as teacher_phone
        FROM offline_requests o
        LEFT JOIN teachers t ON o.assigned_teacher_id = t.id
        WHERE o.student_id = %s
        ORDER BY o.created_at DESC
    """, (student_id,))
    requests = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('my_offline_requests.html', requests=requests)

@app.route('/admin/offline_requests')
@admin_login_required
def admin_offline_requests():
    """Admin view for offline tutor requests"""
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    status = request.args.get('status', '')
    city = request.args.get('city', '')
    
    query = """
        SELECT o.*, t.full_name as teacher_name, t.phone as teacher_phone
        FROM offline_requests o
        LEFT JOIN teachers t ON o.assigned_teacher_id = t.id
        WHERE 1=1
    """
    params = []
    
    if status:
        query += " AND o.status = %s"
        params.append(status)
    
    if city:
        query += " AND o.student_city LIKE %s"
        params.append(f"%{city}%")
    
    # Fixed: Single line ORDER BY clause
    query += " ORDER BY CASE o.status WHEN 'pending' THEN 1 WHEN 'assigned' THEN 2 WHEN 'demo_scheduled' THEN 3 ELSE 4 END, o.created_at DESC"
    
    cur.execute(query, params)
    requests = cur.fetchall()
    
    # Get available teachers for assignment
    cur.execute("""
        SELECT id, full_name, city, qualification, mode
        FROM teachers 
        WHERE status = 'active' AND is_verified = 1
        ORDER BY full_name
    """)
    teachers = cur.fetchall()
    
    # Get statistics
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN status = 'assigned' THEN 1 ELSE 0 END) as assigned,
            SUM(CASE WHEN status = 'demo_scheduled' THEN 1 ELSE 0 END) as demo,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled
        FROM offline_requests
    """)
    stats = cur.fetchone()
    
    # Set default values if stats is None
    if not stats:
        stats = {'total': 0, 'pending': 0, 'assigned': 0, 'demo': 0, 'completed': 0, 'cancelled': 0}
    
    cur.close()
    conn.close()
    
    return render_template('admin_offline_requests.html', 
                         requests=requests, 
                         teachers=teachers,
                         stats=stats,
                         selected_status=status,
                         selected_city=city)
# -------------------------
# TEACHER SECTION
# -------------------------

@app.route('/teacher_change_password', methods=['GET', 'POST'])
def teacher_change_password():
    if 'teacher_id' not in session:
        return redirect('/teacher_login')

    if request.method == 'POST':
        teacher_id = session['teacher_id']
        current_pw = request.form.get('current_password')
        new_pw = request.form.get('new_password')
        confirm_pw = request.form.get('confirm_password')

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        try:
            # 1. Fetch current password hash
            cur.execute("SELECT password FROM teachers WHERE id=%s", (teacher_id,))
            teacher = cur.fetchone()

            # 2. Verify current password
            if not teacher or not check_password_hash(teacher['password'], current_pw):
                flash("Current password is incorrect", "danger")
                return redirect('/teacher_change_password')

            # 3. Check if new passwords match
            if new_pw != confirm_pw:
                flash("New passwords do not match", "warning")
                return redirect('/teacher_change_password')

            # 4. Update the password
            hashed_pw = generate_password_hash(new_pw)
            cur.execute("UPDATE teachers SET password=%s WHERE id=%s", (hashed_pw, teacher_id))
            conn.commit()
            
            flash("Password updated successfully!", "success")
            return redirect('/teacher_dashboard')

        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred. Please try again.")
        finally:
            cur.close()
            conn.close()

    return render_template("teacher_change_password.html")
    


@app.route('/teacher_register', methods=['GET', 'POST'])
def teacher_register():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')

        # 1. Handle File Uploads
        # Note: Added 'aadhaar_file' and 'degree_cert' from your HTML
        resume = request.files.get('resume')
        photo = request.files.get('profile_photo')
        aadhaar_img = request.files.get('aadhaar_file')
        
        res_name = secure_filename(resume.filename) if resume else ""
        pho_name = secure_filename(photo.filename) if photo else ""
        aad_name = secure_filename(aadhaar_img.filename) if aadhaar_img else ""
        
        # Save files
        upload_map = {
            'RESUME_FOLDER': (resume, res_name),
            'PHOTO_FOLDER': (photo, pho_name),
            'AADHAAR_FOLDER': (aadhaar_img, aad_name)
        }
        
        for folder_key, (file_obj, filename) in upload_map.items():
            if file_obj:
                path = app.config.get(folder_key, 'uploads/')
                os.makedirs(path, exist_ok=True)
                file_obj.save(os.path.join(path, filename))

        # 2. Prepare Data for Database
        # We collect lists (checkboxes) and join them into strings
        teacher_data = {
            'full_name': data.get('full_name'),
            'gender': data.get('gender'),
            'dob': data.get('dob'),
            'email': email,
            'password': generate_password_hash(data.get('password')),
            'phone': data.get('phone'),
            'whatsapp': data.get('whatsapp'),
            'alt_phone': data.get('alt_phone'),
            'address': data.get('address'),
            'locality': data.get('locality'),
            'city': data.get('city'),
            'state': data.get('state'),
            'pincode': data.get('pincode'),
            'aadhaar': data.get('aadhaar'),
            'photo': pho_name,
            'resume': res_name,
            'qualification': data.get('qualification'),
            'specialization': data.get('specialization'),
            'university': data.get('university'),
            'passing_year': data.get('passing_year'),
            'subjects': data.get('subjects'), # From hidden input in JS
            'classes': ",".join(request.form.getlist('classes')),
            'boards': ",".join(request.form.getlist('boards')),
            'experience': data.get('experience'),
            'exp_type': ",".join(request.form.getlist('exp_type')),
            'mode': data.get('mode'),
            'timing': data.get('timing'),
            'pref_area': data.get('pref_area'),
            'monthly_fee': data.get('monthly_fee'),
            'hourly_fee': data.get('hourly_fee'),
            'languages': data.get('languages'),
            'special_skills': data.get('special_skills'),
            'security_question': data.get('security_question'),
            'security_answer': generate_password_hash(data.get('security_answer')),
            'plan': data.get('plan', 'free_trial'),
            'status': 'active',
            'is_verified': 1,
            'my_points': 49
        }

        # 3. Database Insertion
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Dynamic SQL creation
            columns = ', '.join(teacher_data.keys())
            placeholders = ', '.join(['%s'] * len(teacher_data))
            query = f"INSERT INTO teachers ({columns}) VALUES ({placeholders})"
            
            cur.execute(query, list(teacher_data.values()))
            conn.commit()
            cur.close()
            conn.close()

            flash("Registration successful! Please login.", "success")
            return redirect(url_for('teacher_login'))

        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred during registration.", "danger")
            return redirect(url_for('teacher_register'))

    return render_template('teacher_register.html')
    


# --- SEND REGISTRATION OTP ---

# 1. THE SENDING FUNCTION
def send_otp_email(email, otp):
    try:
        msg = Message(
            subject='Your Verification Code - HomeTutorHub',
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = f"Your OTP is: {otp}"
        msg.html = f"<h3>Welcome to HomeTutorHub!</h3><p>Your OTP for registration is: <b>{otp}</b></p>"
        mail.send(msg)
        return True
    except Exception as e:
        print(f"MAIL ERROR: {e}")
        return False

# 2. THE INITIAL SEND ROUTE
@app.route('/send_registration_otp', methods=['POST'])
def send_registration_otp():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify(success=False, error="Email is required")

    otp = str(random.randint(100000, 999999))
    session['registration_otp'] = otp
    session['registration_email'] = email # Save for resending
    
    if send_otp_email(email, otp):
        return jsonify(success=True)
    return jsonify(success=False, error="Failed to send email")

# 3. THE VERIFY ROUTE
@app.route('/verify_registration_otp', methods=['POST'])
def verify_registration_otp():
    user_otp = request.json.get('otp')
    if user_otp and user_otp == session.get('registration_otp'):
        return jsonify(success=True)
    return jsonify(success=False, error="Invalid OTP")

# 4. THE RESEND ROUTE
@app.route('/resend_registration_otp', methods=['POST'])
def resend_registration_otp():
    email = session.get('registration_email')
    if not email:
        return jsonify(success=False, error="No email found in session")

    otp = str(random.randint(100000, 999999))
    session['registration_otp'] = otp
    
    if send_otp_email(email, otp):
        return jsonify(success=True)
    return jsonify(success=False, error="Failed to resend email")
    
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        security_question = request.form.get('security_question')
        security_answer = request.form.get('security_answer', '').strip()
        new_password = request.form.get('new_password')
        user_type = request.form.get('user_type')  # Add this to your form

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        try:
            # If user type is specified, check only that table
            if user_type == 'student':
                cur.execute("""
                    SELECT id, security_answer, security_question FROM students 
                    WHERE email = %s AND security_question = %s
                """, (email, security_question))
                user = cur.fetchone()
                table_name = "students"
                
            elif user_type == 'teacher':
                cur.execute("""
                    SELECT id, security_answer, security_question FROM teachers 
                    WHERE email = %s AND security_question = %s
                """, (email, security_question))
                user = cur.fetchone()
                table_name = "teachers"
                
            else:
                # Check both tables and prompt user to choose
                cur.execute("""
                    SELECT 'student' as user_type, security_answer, security_question FROM students 
                    WHERE email = %s AND security_question = %s
                    UNION
                    SELECT 'teacher' as user_type, security_answer, security_question FROM teachers 
                    WHERE email = %s AND security_question = %s
                """, (email, security_question, email, security_question))
                users = cur.fetchall()
                
                if len(users) > 1:
                    # Multiple accounts found - need user to specify which one
                    flash("Multiple accounts found with this email. Please select your account type.", "warning")
                    return render_template("forgot_password.html", 
                                         email=email, 
                                         need_user_type=True,
                                         security_question=security_question)
                elif len(users) == 1:
                    user = users[0]
                    table_name = user['user_type']
                else:
                    user = None
                    table_name = None

            # Verify security answer
            if user and check_password_hash(user['security_answer'], security_answer.lower()):
                hashed_new_password = generate_password_hash(new_password)
                
                cur.execute(f"UPDATE {table_name} SET password = %s WHERE email = %s",
                          (hashed_new_password, email))
                conn.commit()
                
                flash("Password updated successfully! Please login with your new password.", "success")
                cur.close()
                conn.close()
                
                return redirect(f'/{table_name}_login')
            else:
                flash("Invalid email, security question, or answer. Please try again.", "danger")
                
        except Exception as e:
            print(f"Error in forgot_password: {e}")
            conn.rollback()
            flash("An error occurred. Please try again.", "danger")
        finally:
            cur.close()
            conn.close()

    return render_template("forgot_password.html")
    
@app.route('/teacher_login', methods=['GET', 'POST'])
@app.route('/teachers_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        session.clear()
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM teachers WHERE email=%s", (email,))
            teacher = cur.fetchone()
        finally:
            cur.close()
            conn.close()

        # 1. Check if teacher exists and password is correct
        if teacher and check_password_hash(teacher['password'], password):
            
            # 2. Check the account status
            if teacher['status'] == 'pending':
                flash("Your account is currently pending admin review. Please try again later.")
                return redirect(url_for('teacher_login'))
            
            elif teacher['status'] != 'active':
                flash("Your account is not active. Please contact the administrator.")
                return redirect(url_for('teacher_login'))

            # 3. If Active, allow login
            session['teacher_id'] = teacher['id']
            session['teacher_name'] = teacher['full_name']
            session['role'] = 'teacher'
            return redirect(url_for('teacher_dashboard'))
        
        else:
            flash("Invalid email or password.")
            
    return render_template("teacher_login.html")
    
@app.route('/teacher_dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if 'teacher_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect('/teacher_login')

    teacher_id = session['teacher_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # --- 1. POST Logic (Update Profile) ---
    if request.method == 'POST':
        try:
            # Update Profile Photo
            photo_file = request.files.get('profile_photo')
            if photo_file and photo_file.filename != '':
                pho_name = secure_filename(photo_file.filename)
                name_parts = pho_name.rsplit('.', 1)
                pho_name = f"{name_parts[0]}_{int(time.time())}.{name_parts[1]}"
                photo_file.save(os.path.join(app.config['PHOTO_FOLDER'], pho_name))
                cur.execute("UPDATE teachers SET photo=%s WHERE id=%s", (pho_name, teacher_id))
            
            # Update Resume
            resume_file = request.files.get('resume')
            if resume_file and resume_file.filename != '':
                res_name = secure_filename(resume_file.filename)
                name_parts = res_name.rsplit('.', 1)
                res_name = f"{name_parts[0]}_{int(time.time())}.{name_parts[1]}"
                resume_file.save(os.path.join(app.config['RESUME_FOLDER'], res_name))
                cur.execute("UPDATE teachers SET resume=%s WHERE id=%s", (res_name, teacher_id))
            
            # Update Profile Info
            phone = request.form.get('phone', '')
            city = request.form.get('city', '')
            qualification = request.form.get('qualification', '')
            experience = request.form.get('experience', 0)
            address = request.form.get('address', '')
            subjects_input = request.form.get('subjects', '')

            cur.execute("""
                UPDATE teachers 
                SET phone=%s, city=%s, qualification=%s, experience=%s, address=%s
                WHERE id=%s
            """, (phone, city, qualification, experience, address, teacher_id))

            # Update Subjects
            cur.execute("DELETE FROM teacher_subjects WHERE teacher_id=%s", (teacher_id,))
            for sub in subjects_input.split(','):
                sub = sub.strip()
                if sub:
                    cur.execute("INSERT INTO teacher_subjects (teacher_id, subject_name) VALUES (%s, %s)", 
                              (teacher_id, sub))
            

            conn.commit()
            flash("Profile updated successfully!", "success")
            return redirect('/teacher_dashboard')

        except Exception as e:
            conn.rollback()
            print(f"Error during POST update: {e}")
            flash(f"An error occurred during update: {str(e)}", "danger")
            return redirect('/teacher_dashboard')

    # --- 2. GET Logic ---
    # --- 2. GET Logic ---
    try:
        # Fetch the full teacher record
        cur.execute("""
            SELECT id, full_name, email, phone, city, qualification, 
                   experience, address, photo, resume, my_points, 
                   status, is_verified
            FROM teachers WHERE id=%s
        """, (teacher_id,))
        teacher = cur.fetchone()
        
        if not teacher:
            session.clear()
            flash("Teacher account not found. Please register again.", "danger")
            return redirect('/teacher_register')
        
        if teacher['status'] != 'active' or not teacher['is_verified']:
            session.clear()
            flash("Access Denied. Your account is pending admin approval.", "warning")
            return redirect('/teacher_login')

        # Fetch subjects
        cur.execute("SELECT subject_name FROM teacher_subjects WHERE teacher_id=%s", (teacher_id,))
        teacher_subjects = cur.fetchall()

        # Get search/filter parameters
        search_subject = request.args.get('subject', '').strip()
        search_location = request.args.get('location', '').strip()
        search_class = request.args.get('class', '').strip()

        # Build query to fetch TUITION REQUESTS
# In teacher_dashboard GET logic
        query = """
            SELECT 
                tr.*,
                s.full_name as student_name,
                s.email as student_email,
                s.phone as student_phone,
                s.city as student_city,
                CASE WHEN ul.id IS NOT NULL THEN 1 ELSE 0 END as is_unlocked,
                (SELECT COUNT(*) FROM unlocked_leads WHERE student_id = tr.student_id) as unlock_count
            FROM tuition_requests tr
            INNER JOIN students s ON tr.student_id = s.id
            LEFT JOIN unlocked_leads ul ON ul.student_id = s.id AND ul.teacher_id = %s
            WHERE tr.status = 'Open'
        """
        params = [teacher_id]
        
        # Add search filters
        if search_subject:
            query += " AND tr.subject LIKE %s"
            params.append(f"%{search_subject}%")
        
        if search_location:
            query += " AND (tr.location LIKE %s OR s.city LIKE %s)"
            params.append(f"%{search_location}%")
            params.append(f"%{search_location}%")
        
        if search_class:
            query += " AND tr.class_grade LIKE %s"
            params.append(f"%{search_class}%")
        
        query += " ORDER BY tr.created_at DESC"
        
        cur.execute(query, params)
        tuition_requests = cur.fetchall()
        
        # Add time_ago to each request
        for req in tuition_requests:
            req['time_ago'] = time_ago(req['created_at'])
        
        # Get unlocked requests for the tab
        unlocked_requests = [req for req in tuition_requests if req.get('is_unlocked')]
        
        # Fetch announcements for teachers
        announcements = get_active_announcements('teachers', 5)
        
        return render_template("teacher_dashboard.html", 
                              teacher=teacher, 
                              subjects=teacher_subjects, 
                              tuition_requests=tuition_requests,
                              unlocked_requests=unlocked_requests,
                              search_subject=search_subject,
                              search_location=search_location,
                              search_class=search_class,
                              announcements=announcements)
        
    except Exception as e:
        print(f"Dashboard Load Error: {e}")
        import traceback
        traceback.print_exc()
        flash(f"Error loading dashboard: {str(e)}", "danger")
        return redirect('/')
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route('/unlock_student_contact/<int:student_id>', methods=['POST'])
def unlock_student_contact(student_id):
    """Unlock student contact details for a teacher (costs 49 points)"""
    if 'teacher_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in first.'}), 401
    
    teacher_id = session['teacher_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
# Correct indentation (4 spaces inside try block)
    try:
        UNLOCK_COST = 49
        
        # Check if already unlocked
        cur.execute("""
            SELECT * FROM unlocked_leads 
            WHERE teacher_id = %s AND student_id = %s
        """, (teacher_id, student_id))
        
        if cur.fetchone():
            return jsonify({'success': False, 'message': 'Contact already unlocked.'}), 400
        
        # Check teacher's points
        cur.execute("SELECT my_points FROM teachers WHERE id = %s", (teacher_id,))
        teacher = cur.fetchone()
        
        if not teacher:
            return jsonify({'success': False, 'message': 'Teacher not found.'}), 404
        
        if teacher['my_points'] < UNLOCK_COST:
            return jsonify({'success': False, 'message': f'Insufficient points! Need {UNLOCK_COST} points.'}), 400
        
        # Deduct points and record unlock
        cur.execute("""
            UPDATE teachers 
            SET my_points = my_points - %s 
            WHERE id = %s
        """, (UNLOCK_COST, teacher_id))
        
        cur.execute("""
            INSERT INTO unlocked_leads (teacher_id, student_id, unlocked_at)
            VALUES (%s, %s, NOW())
        """, (teacher_id, student_id))
        
        conn.commit()
        
        # Get updated points
        cur.execute("SELECT my_points FROM teachers WHERE id = %s", (teacher_id,))
        updated_teacher = cur.fetchone()
        
        return jsonify({
            'success': True, 
            'message': f'Contact unlocked! {UNLOCK_COST} points deducted.',
            'new_points': updated_teacher['my_points']
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error unlocking contact: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/unlock_teacher/<int:teacher_id>')
def unlock_teacher(teacher_id):
    if 'student_id' not in session:
        flash("Please log in to unlock teacher details.", "danger")
        return redirect('/student_login')
    
    student_id = session['student_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    try:
        UNLOCK_COST = 49
        
        # Check if already unlocked
        cur.execute("""
            SELECT * FROM student_unlocked_teachers 
            WHERE student_id = %s AND teacher_id = %s
        """, (student_id, teacher_id))
        
        if cur.fetchone():
            flash("You have already unlocked this teacher's contact details.", "info")
            return redirect('/search')
        
        # Check student's points
        cur.execute("SELECT points FROM students WHERE id = %s", (student_id,))
        student = cur.fetchone()
        
        if not student:
            flash("Student not found.", "danger")
            return redirect('/search')
        
        if student['points'] >= UNLOCK_COST:
            # Deduct points
            cur.execute("""
                UPDATE students 
                SET points = points - %s 
                WHERE id = %s
            """, (UNLOCK_COST, student_id))
            
            # Record the unlock
            cur.execute("""
                INSERT INTO student_unlocked_teachers (student_id, teacher_id, unlocked_at)
                VALUES (%s, %s, NOW())
            """, (student_id, teacher_id))
            
            conn.commit()
            flash(f"Success! {UNLOCK_COST} points deducted. Contact details are now visible.", "success")
        else:
            flash(f"Insufficient points! You need {UNLOCK_COST} points. Current balance: {student['points']} points.", "danger")
        
        return redirect('/search')
        
    except Exception as e:
        print(f"Error in unlock_teacher: {e}")
        conn.rollback()
        flash("An error occurred while unlocking teacher details.", "danger")
        return redirect('/search')
    finally:
        cur.close()
        conn.close()
        
# Student Tuition Request Page
@app.route('/tuition_request')
def tuition_request_page():
    if 'student_id' not in session:
        return redirect('/student_login')
    
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Fetch student's existing requests
    cur.execute("""
        SELECT * FROM tuition_requests 
        WHERE student_id = %s 
        ORDER BY created_at DESC
    """, (session['student_id'],))
    requests = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('tuition_request.html', requests=requests)

# Submit Tuition Request
@app.route('/submit_tuition_request', methods=['POST'])
def submit_tuition_request():
    if 'student_id' not in session:
        return redirect('/student_login')
    
    student_id = session['student_id']
    subject = request.form.get('subject')
    mode = request.form.get('mode')
    location = request.form.get('location')
    class_grade = request.form.get('class_grade')
    
    # Combine time fields
    from_hour = request.form.get('from_hour')
    from_minute = request.form.get('from_minute')
    from_ampm = request.form.get('from_ampm')
    to_hour = request.form.get('to_hour')
    to_minute = request.form.get('to_minute')
    to_ampm = request.form.get('to_ampm')
    
    preferred_timing = f"{from_hour}:{from_minute} {from_ampm} to {to_hour}:{to_minute} {to_ampm}" if all([from_hour, from_minute, from_ampm, to_hour, to_minute, to_ampm]) else ''
    
    description = request.form.get('description', '')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO tuition_requests (student_id, subject, mode, location, class_grade, preferred_timing, description, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Open')
        """, (student_id, subject, mode, location, class_grade, preferred_timing, description))
        conn.commit()
        flash('Tuition request submitted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        flash('Error submitting request. Please try again.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect('/tuition_request')

# Close Tuition Request (Student)
@app.route('/close_tuition_request/<int:request_id>')
def close_tuition_request(request_id):
    if 'student_id' not in session:
        return redirect('/student_login')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE tuition_requests 
            SET status = 'Closed', updated_at = NOW() 
            WHERE id = %s AND student_id = %s
        """, (request_id, session['student_id']))
        conn.commit()
        flash('Tuition request closed successfully!', 'success')
    except Exception as e:
        print(f"Error: {e}")
        flash('Error closing request.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect('/tuition_request')
    
def time_ago(dt):
    """Convert datetime to time ago string"""
    if not dt:
        return "Just now"
    
    from datetime import datetime
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"

# Delete Tuition Request (Student)
@app.route('/delete_tuition_request/<int:request_id>', methods=['POST'])
def delete_tuition_request(request_id):
    if 'student_id' not in session:
        return redirect('/student_login')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM tuition_requests WHERE id = %s AND student_id = %s", 
                   (request_id, session['student_id']))
        conn.commit()
        flash('Tuition request deleted successfully!', 'success')
    except Exception as e:
        print(f"Error: {e}")
        flash('Error deleting request.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect('/tuition_request')
                         
@app.route('/teacher_edit_profile', methods=['GET', 'POST'])
def teacher_edit_profile():
    if 'teacher_id' not in session:
        return redirect('/teacher_login')
 
    teacher_id = session['teacher_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
 
    if request.method == 'POST':
        full_name   = request.form['full_name']
        phone       = request.form['phone']
        city        = request.form['city']
        address     = request.form['address']
        qualification = request.form['qualification']
        experience  = request.form['experience']
        mode        = request.form['mode']
        subjects    = request.form['subjects']   # comma-separated
 
        # Handle new profile photo (optional)
        photo_file = request.files.get('profile_photo')
        if photo_file and photo_file.filename != '':
            photo_name = secure_filename(photo_file.filename)
            photo_file.save(os.path.join('static/uploads/profile_photos', photo_name))
            cur.execute("UPDATE teachers SET photo=%s WHERE id=%s", (photo_name, teacher_id))
 
        # Update teacher core fields
        cur.execute("""
            UPDATE teachers
            SET full_name=%s, phone=%s, city=%s, address=%s,
                qualification=%s, experience=%s, mode=%s
            WHERE id=%s
        """, (full_name, phone, city, address, qualification, experience, mode, teacher_id))
 
        # Update subjects: delete old, insert new
        cur.execute("DELETE FROM teacher_subjects WHERE teacher_id=%s", (teacher_id,))
        for sub in subjects.split(','):
            sub = sub.strip()
            if sub:
                cur.execute(
                    "INSERT INTO teacher_subjects (teacher_id, subject_name) VALUES (%s, %s)",
                    (teacher_id, sub)
                )
 
        # Keep session name in sync
        session['teacher_name'] = full_name
 
        conn.commit()
        cur.close()
        conn.close()
        flash("Profile updated successfully!")
        return redirect('/teacher_dashboard')
 
    # GET — fetch current data
    cur.execute("SELECT * FROM teachers WHERE id=%s", (teacher_id,))
    teacher = cur.fetchone()
 
    cur.execute("SELECT subject_name FROM teacher_subjects WHERE teacher_id=%s", (teacher_id,))
    subjects_rows = cur.fetchall()
    subjects_str  = ', '.join([r['subject_name'] for r in subjects_rows])
 
    cur.close()
    return render_template("teacher_edit_profile.html", teacher=teacher, subjects_str=subjects_str)
 
 
# ── STUDENT EDIT PROFILE ────────────────────────────────────
@app.route('/student_register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        # Get data from the form
        full_name = request.form.get('name')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        phone = request.form.get('phone')
        father_name = request.form.get('father_name')
        father_phone = request.form.get('father_phone')
        mother_name = request.form.get('mother_name')
        mother_phone = request.form.get('mother_phone')
        city = request.form.get('city')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        address = request.form.get('address')
        qualification = request.form.get('qualification')
        specialization = request.form.get('specialization')
        security_question = request.form.get('security_question')
        security_answer = generate_password_hash(request.form.get('security_answer'))
     
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # Check if email already exists
            cur.execute("SELECT id FROM students WHERE email = %s", (email,))
            if cur.fetchone():
                flash("Email already registered. Please login.", "warning")
                return redirect(url_for('student_register'))

            # Insert into students table
            cur.execute("""
                INSERT INTO students (
                    full_name, email, password, phone, father_name, father_phone,
                    mother_name, mother_phone, city, state, pincode, address,
                    qualification, specialization, security_question, security_answer, points
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 49)
            """, (
                full_name, email, password, phone, father_name, father_phone,
                mother_name, mother_phone, city, state, pincode, address,
                qualification, specialization, security_question, security_answer
            ))
            
            conn.commit()
            flash("Student registration successful! 49 bonus points added.", "success")
            return redirect('/student_login')
        except Exception as e:
            conn.rollback()
            print(f"Student Reg Error: {e}")
            flash("Error during registration. Please try again.", "danger")
        finally:
            cur.close()
            conn.close()

    return render_template("student_register.html")

@app.route('/student_edit_profile', methods=['POST'])
def student_edit_profile():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    try:
        full_name = request.form.get('full_name', '')
        phone = request.form.get('phone', '')
        city = request.form.get('city', '')
        qualification = request.form.get('qualification', '')
        specialization = request.form.get('specialization', '')
        # Remove address field since it doesn't exist
        address = request.form.get('address', '')
        
        # Update query without address column
        cur.execute("""
            UPDATE students 
            SET full_name = %s, phone = %s, city = %s, 
                qualification = %s, specialization = %s
            WHERE id = %s
        """, (full_name, phone, city, qualification, specialization, student_id))
        
        conn.commit()
        flash('Profile updated successfully!', 'success')
        
    except Exception as e:
        print(f"Error updating profile: {e}")
        flash('Error updating profile', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('search'))

    # GET Request: Pre-fill the form with existing data
    cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    conn.close()
    
    return render_template('student_edit_profile.html', student=student)
# -------------------------
# STUDENT SECTION
# -------------------------

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    sid = session['student_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    try:
        # Fetch Student data
        cur.execute("""
            SELECT id, full_name, email, phone, city, qualification, 
                   specialization, points as my_points, created_at
            FROM students WHERE id = %s
        """, (sid,))
        user = cur.fetchone()

        if not user:
            flash("Student not found. Please log in again.", "danger")
            return redirect(url_for('student_login'))

        # Check if student should see tuition prompt
        cur.execute("""
            SELECT COUNT(*) as count FROM tuition_requests 
            WHERE student_id = %s AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        """, (sid,))
        request_count = cur.fetchone()
        
        show_tuition_prompt = (request_count and request_count['count'] == 0)

        # Fetch unlocked teachers
        cur.execute("""
            SELECT t.*, sut.unlocked_at 
            FROM teachers t
            INNER JOIN student_unlocked_teachers sut ON t.id = sut.teacher_id
            WHERE sut.student_id = %s AND t.status = 'active'
            ORDER BY sut.unlocked_at DESC
        """, (sid,))
        unlocked_teachers = cur.fetchall()

        # Execute search based on method
        if request.method == 'POST':
            subject = request.form.get('subject', '').strip()
            city = request.form.get('city', '').strip()
            mode = request.form.get('mode', '').strip()

            query = "SELECT * FROM teachers WHERE status = 'active'"
            params = []
            
            if city:
                query += " AND city LIKE %s"
                params.append(f"%{city}%")
            
            if mode:
                query += " AND mode = %s"
                params.append(mode)
            
            if subject:
                query += " AND subjects LIKE %s"
                params.append(f"%{subject}%")
            
            query += " ORDER BY created_at DESC"
            cur.execute(query, params)
        else:
            cur.execute("SELECT * FROM teachers WHERE status = 'active' ORDER BY created_at DESC")
        
        teachers = cur.fetchall()
        unlocked_ids = [t['id'] for t in unlocked_teachers]
        announcements = get_active_announcements('students', 5)
        
        return render_template("search.html", 
                              user=user, 
                              teachers=teachers, 
                              unlocked_teachers=unlocked_teachers, 
                              unlocked_ids=unlocked_ids,
                              announcements=announcements,
                              show_tuition_prompt=show_tuition_prompt)
        
    except Exception as e:
        print(f"Error in search: {e}")
        flash("An error occurred while searching for tutors.", "danger")
        return redirect(url_for('student_login'))
    finally:
        cur.close()
        conn.close()
        
@app.route('/help')
def help_center():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("""
        SELECT * FROM help_articles 
        WHERE is_active = 1 
        ORDER BY category, step_order
    """)
    articles = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('help_center.html', articles=articles)



@app.route('/student_change_password', methods=['GET', 'POST'])
def student_change_password():
    if 'student_id' not in session:
        return redirect('/student_login')

    if request.method == 'POST':
        student_id = session['student_id']
        current_pw = request.form.get('current_password')
        new_pw = request.form.get('new_password')
        confirm_pw = request.form.get('confirm_password')

        # Use your connection helper (ensure it returns a mysql.connector object)
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        try:
            # 1. Fetch student data
            cur.execute("SELECT password FROM students WHERE id=%s", (student_id,))
            student = cur.fetchone()

            # 2. Verify current password
            if not student or not check_password_hash(student['password'], current_pw):
                flash("Current password is incorrect", "danger")
                return redirect('/student_change_password')

            # 3. Check matching passwords
            if new_pw != confirm_pw:
                flash("New passwords do not match", "warning")
                return redirect('/student_change_password')

            # 4. Update password
            hashed_pw = generate_password_hash(new_pw)
            cur.execute("UPDATE students SET password=%s WHERE id=%s", (hashed_pw, student_id))
            
            # Use conn.commit() instead of mysql.connection.commit()
            conn.commit()
            flash("Password updated successfully!", "success")
            return redirect('/search')

        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred during update.")
        finally:
            cur.close()
            conn.close()

    # GET logic
    return render_template("student_change_password.html")


@app.route('/student_login', methods=['GET', 'POST'])
@app.route('/students_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM students WHERE email=%s", (email,))
        student = cur.fetchone()
        cur.close()
        conn.close()
        if student and check_password_hash(student['password'], password):
            session['student_id'] = student['id']
            session['student_name'] = student['full_name']
            return redirect(url_for('search'))
        flash("Invalid credentials")
    return render_template("student_login.html")
    


# -------------------------
# POINTS & UNLOCK LOGIC
# -------------------------
@app.route('/unlock_contact/<int:request_id>', methods=['GET', 'POST'])
def unlock_contact(request_id):
    if 'teacher_id' not in session:
        flash("Please log in first.", "danger")
        return redirect('/teacher_login')

    teacher_id = session['teacher_id']
    unlock_cost = 49
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    try:
        # Get the student_id from the tuition request (NOT using request_id in unlocked_leads)
        cur.execute("SELECT student_id FROM tuition_requests WHERE id = %s AND status = 'Open'", (request_id,))
        request_data = cur.fetchone()
        
        if not request_data:
            flash("Request not found or already closed!", "danger")
            return redirect('/teacher_dashboard')
        
        student_id = request_data['student_id']
        
        # Check if already unlocked (using student_id, since no request_id column)
        cur.execute("""
            SELECT id FROM unlocked_leads 
            WHERE teacher_id = %s AND student_id = %s
        """, (teacher_id, student_id))
        
        if cur.fetchone():
            flash("You have already unlocked this student's contact!", "info")
            return redirect('/teacher_dashboard')

        # Check teacher's points
        cur.execute("SELECT my_points FROM teachers WHERE id = %s", (teacher_id,))
        teacher = cur.fetchone()

        if not teacher or teacher['my_points'] < unlock_cost:
            flash(f"Insufficient points! Need {unlock_cost} points. Current: {teacher['my_points'] if teacher else 0}", "danger")
            return redirect('/teacher_dashboard')

        # Deduct points
        cur.execute("UPDATE teachers SET my_points = my_points - %s WHERE id = %s", (unlock_cost, teacher_id))
        
        # Record unlock (only teacher_id and student_id, no request_id)
        cur.execute("""
            INSERT INTO unlocked_leads (teacher_id, student_id, unlocked_at)
            VALUES (%s, %s, NOW())
        """, (teacher_id, student_id))

        conn.commit()
        
        flash(f"Contact unlocked successfully! {unlock_cost} points deducted.", "success")

    except Exception as e:
        conn.rollback()
        print(f"Unlock Error: {e}")
        flash("An error occurred while unlocking the contact.", "danger")
    finally:
        cur.close()
        conn.close()

    return redirect('/teacher_dashboard')
    
    
@app.route('/accept_student/<int:request_id>') # Must be request_id
def accept_student(request_id):
    if 'teacher_id' not in session:
        return redirect('/teacher_login')
    
    teacher_id = session['teacher_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    try:
        # Check points (matching your column name 'points' from verify_teacher)
        cur.execute("SELECT points FROM teachers WHERE id = %s", (teacher_id,))
        teacher = cur.fetchone()
        
        if not teacher or (teacher['my_points'] or 0) < 20:
            flash("Insufficient points!", "danger")
            return redirect('/teacher_dashboard')

        # Deduct and Insert
        cur.execute("UPDATE teachers SET my_points = my_points - 20 WHERE id = %s", (teacher_id,))
        cur.execute("INSERT INTO unlocked_leads (teacher_id, request_id) VALUES (%s, %s)", (teacher_id, request_id))
        conn.commit()
        flash("Contact unlocked!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}") 
    finally:
        cur.close()
        conn.close()
    return redirect('/teacher_dashboard')

@app.route('/view_teacher_details/<int:teacher_id>')
def view_teacher_details(teacher_id):
    if 'student_id' not in session:
        flash("Please log in to view teacher details.", "danger")
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    try:
        # Verify this student has unlocked this teacher
        cur.execute("""
            SELECT * FROM student_unlocked_teachers 
            WHERE student_id = %s AND teacher_id = %s
        """, (student_id, teacher_id))
        
        if not cur.fetchone():
            flash("You need to unlock this teacher's contact details first.", "warning")
            return redirect(url_for('search'))
        
        # Fetch teacher details - removed 'bio' and 'photo' columns if they don't exist
        cur.execute("""
            SELECT id, full_name, email, phone, qualification, experience, 
                   subjects, city, mode 
            FROM teachers 
            WHERE id = %s AND status = 'active'
        """, (teacher_id,))
        
        teacher = cur.fetchone()
        
        if not teacher:
            flash("Teacher not found.", "danger")
            return redirect(url_for('search'))
        
        return render_template("teacher_details.html", teacher=teacher)
        
    except Exception as e:
        print(f"Error in view_teacher_details: {e}")
        flash("An error occurred while loading teacher details.", "danger")
        return redirect(url_for('search'))
    finally:
        cur.close()
        conn.close()

        
@app.route('/my_unlocked_teachers')
def my_unlocked_teachers():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    try:
        # Get all unlocked teachers for this student
        cur.execute("""
            SELECT t.*, sut.unlocked_at 
            FROM teachers t
            INNER JOIN student_unlocked_teachers sut ON t.id = sut.teacher_id
            WHERE sut.student_id = %s AND t.status = 'active'
            ORDER BY sut.unlocked_at DESC
        """, (student_id,))
        
        unlocked_teachers = cur.fetchall()
        
        return render_template("my_unlocked_teachers.html", teachers=unlocked_teachers)
        
    except Exception as e:
        print(f"Error in my_unlocked_teachers: {e}")
        flash("An error occurred.", "danger")
        return redirect(url_for('search.html'))
    finally:
        cur.close()
        conn.close()

# -------------------------
# PAYMENTS
# -------------------------
@app.route('/buy_points')
def buy_points():
    if 'student_id' not in session and 'teacher_id' not in session:
        flash("Please log in to buy points.", "danger")
        return redirect(url_for('index'))
    
    if 'student_id' in session:
        user_id = session['student_id']
        table = 'students'
        points_column = 'points'
    else:
        user_id = session['teacher_id']
        table = 'teachers'
        points_column = 'my_points'
    
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute(f"SELECT {points_column} FROM {table} WHERE id = %s", (user_id,))
    user = cur.fetchone()
    wallet = user[points_column] if user else 0
    
    cur.close()
    conn.close()
    
    return render_template("buy_points.html", wallet=wallet, RAZORPAY_KEY_ID=RAZORPAY_KEY_ID)

@app.route('/create_razorpay_order', methods=['POST'])
def create_razorpay_order():
    if 'student_id' not in session and 'teacher_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    if razorpay_client is None:
        return jsonify({'error': 'Payment gateway not configured'}), 500
    
    try:
        data = request.get_json()
        amount = data.get('amount')
        
        # Razorpay minimum amount is Rs.1 (100 paise) but for testing use Rs.10
        if not amount or amount < 10:
            return jsonify({'error': 'Minimum amount is Rs.10 for testing'}), 400
        
        # Convert to paise
        amount_paise = int(float(amount)) * 100
        
        # Create order with more details
        order_data = {
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': f'receipt_{int(time.time())}',
            'payment_capture': 1,
            'partial_payment': False,
            'notes': {
                'user_type': 'student' if 'student_id' in session else 'teacher',
                'user_id': session.get('student_id') or session.get('teacher_id'),
                'purpose': 'point_purchase'
            }
        }
        
        print(f"Creating order for amount: {amount} INR ({amount_paise} paise)")
        order = razorpay_client.order.create(order_data)
        print(f"Order created: {order['id']}")
        
        return jsonify({
            'success': True,
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency']
        })
        
    except razorpay.errors.BadRequestError as e:
        print(f"Bad request error: {e}")
        return jsonify({'error': f'Bad request: {str(e)}'}), 400
    except razorpay.errors.AuthenticationError as e:
        print(f"Authentication error: {e}")
        return jsonify({'error': 'Payment gateway authentication failed. Check API keys.'}), 401
    except Exception as e:
        print(f"Error creating order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/verify_razorpay_payment', methods=['POST'])
def verify_razorpay_payment():
    """Verify Razorpay payment and add points to user"""
    if 'student_id' not in session and 'teacher_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    try:
        data = request.get_json()
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        amount = data.get('amount')
        
        if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
            return jsonify({'error': 'Missing payment details'}), 400
        
        # Verify signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        # Verify payment signature
        razorpay_client.utility.verify_payment_signature(params_dict)
        
        # Determine user type and update points
        conn = get_db_connection()
        cur = conn.cursor()
        
        points_to_add = int(float(amount))
        
        if 'student_id' in session:
            user_id = session['student_id']
            table = 'students'
            points_column = 'points'
            user_type = 'student'
        else:
            user_id = session['teacher_id']
            table = 'teachers'
            points_column = 'my_points'
            user_type = 'teacher'
        
        # Update user points
        cur.execute(f"UPDATE {table} SET {points_column} = {points_column} + %s WHERE id = %s", 
                   (points_to_add, user_id))
        
        # Record payment in your payments table
        cur.execute("""
            INSERT INTO payments (student_id, teacher_id, amount, plan, screenshot, payment_method, status, payment_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """, (
            user_id if user_type == 'student' else None,
            user_id if user_type == 'teacher' else None,
            amount,
            'razorpay',
            razorpay_payment_id,
            'razorpay',
            'approved'
        ))
        
        conn.commit()
        
        # Get updated points
        cur.execute(f"SELECT {points_column} FROM {table} WHERE id = %s", (user_id,))
        updated_points = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Payment successful! {points_to_add} points added.',
            'new_points': updated_points
        })
        
    except razorpay.errors.SignatureVerificationError:
        return jsonify({'error': 'Payment verification failed - invalid signature'}), 400
    except Exception as e:
        print(f"Verification error: {e}")
        return jsonify({'error': str(e)}), 500
        
@app.route('/payment_success', methods=['POST'])
def payment_success():
    r_order_id = request.form.get('razorpay_order_id')
    r_payment_id = request.form.get('razorpay_payment_id')
    r_signature = request.form.get('razorpay_signature')
    amount = int(request.form.get('amount_inr', 0))
    
    body = f"{r_order_id}|{r_payment_id}".encode()
    expected_sig = hmac.new(RAZORPAY_KEY_SECRET.encode(), body, hashlib.sha256).hexdigest()
    
    if hmac.compare_digest(expected_sig, r_signature):
        conn = get_db_connection()
        cur = conn.cursor()
        if 'student_id' in session:
            cur.execute("UPDATE students SET my_points = my_points + %s WHERE id=%s", (amount, session['student_id']))
            cur.execute("INSERT INTO payments (student_id, amount, screenshot, status) VALUES (%s, %s, %s, 'approved')", (session['student_id'], amount, r_payment_id))
        elif 'teacher_id' in session:
            cur.execute("UPDATE teachers SET my_points = my_points + %s WHERE id=%s", (amount, session['teacher_id']))
            cur.execute("INSERT INTO payments (teacher_id, amount, screenshot, status) VALUES (%s, %s, %s, 'approved')", (session['teacher_id'], amount, r_payment_id))
        conn.commit()
        cur.close()
        conn.close()
        flash("Payment Successful!")
    return redirect(url_for('buy_points'))

@app.route('/test_app')
def test_app():
    return "App is running with updated code!"

# -------------------------
# DEPLOYMENT CONFIG
# -------------------------
application = app  

if __name__ == "__main__":
    app.run()
