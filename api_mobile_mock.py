from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from db_config import get_db_connection

try:
    from db_config import get_db_connection
except ImportError:
    # If db_config is not available, use mock
    def get_db_connection():
        return None

app = Flask(__name__)
CORS(app)

# Store data in memory
tuition_requests = []
courses = []
enrollments = []

# ==================== LOGIN ====================
@app.route('/api/login', methods=['POST'])
def mobile_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    print(f"Login attempt: {email}")
    
    if email and password:
        if 'teacher' in email.lower():
            return jsonify({
                "success": True, 
                "user": {
                    "id": 1,
                    "name": "Demo Teacher",
                    "email": email,
                    "role": "teacher"
                }
            })
        else:
            return jsonify({
                "success": True, 
                "user": {
                    "id": 2,
                    "name": "Test User",
                    "email": email,
                    "role": "student"
                }
            })
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

# ==================== REGISTRATION ====================
# Store offline requests in memory
offline_requests = []

@app.route('/api/offline_request', methods=['POST'])
def offline_request():
    data = request.get_json()
    print(f"📝 New Offline Request from {data.get('student_name')}")
    
    new_request = {
        'id': len(offline_requests) + 1,
        'student_name': data.get('student_name'),
        'student_email': data.get('student_email'),
        'student_phone': data.get('student_phone'),
        'subject': data.get('subject'),
        'class_grade': data.get('class_grade'),
        'address': data.get('address'),
        'city': data.get('city'),
        'preferred_timing': data.get('preferred_timing'),
        'budget': data.get('budget', 'Negotiable'),
        'additional_info': data.get('additional_info', ''),
        'preferred_tutor_gender': data.get('preferred_tutor_gender', 'any'),
        'status': 'pending',
        'created_at': str(datetime.now())
    }
    offline_requests.append(new_request)
    
    print(f"✅ Offline request saved. Total: {len(offline_requests)}")
    
    return jsonify({
        'success': True,
        'message': 'Offline request submitted successfully',
        'request_id': new_request['id']
    })

@app.route('/api/teacher_courses', methods=['GET'])
def get_teacher_courses():
    email = request.args.get('email', '')
    print(f"📚 Fetching courses for teacher: {email}")
    
    # Mock data for teacher courses
    mock_courses = [
        {
            'id': 1,
            'course_name': 'Data Science Fundamentals',
            'fee': 2000,
            'duration_weeks': 12,
            'max_students': 30,
            'enrolled_count': 8,
            'status': 'active'
        },
        {
            'id': 2,
            'course_name': 'Python Programming',
            'fee': 1500,
            'duration_weeks': 8,
            'max_students': 25,
            'enrolled_count': 12,
            'status': 'active'
        },
        {
            'id': 3,
            'course_name': 'Web Development',
            'fee': 2500,
            'duration_weeks': 16,
            'max_students': 20,
            'enrolled_count': 5,
            'status': 'draft'
        }
    ]
    
    return jsonify(mock_courses)

@app.route('/api/teacher_profile', methods=['GET'])
def get_teacher_profile():
    email = request.args.get('email', '')
    print(f"📋 Fetching profile for teacher: {email}")
    
    # Mock data
    mock_profile = {
        'phone': '9876543210',
        'city': 'Mumbai',
        'qualification': 'M.Sc. Mathematics',
        'experience': 5,
        'subjects': 'Mathematics, Physics',
        'address': '123, Main Street, Mumbai',
        'whatsapp': '9876543210',
        'monthly_fee': 3000,
        'hourly_fee': 500,
        'mode': 'Both',
        'profile_photo': ''
    }
    
    return jsonify(mock_profile)

@app.route('/api/update_teacher_profile', methods=['POST'])
def update_teacher_profile():
    data = request.get_json()
    print(f"📝 Updating profile for teacher: {data.get('email')}")
    
    return jsonify({
        'success': True,
        'message': 'Profile updated successfully'
    })

@app.route('/api/student_profile', methods=['GET'])
def get_student_profile():
    email = request.args.get('email', '')
    print(f"📋 Fetching profile for student: {email}")
    
    # Mock data
    mock_profile = {
        'phone': '9876543210',
        'city': 'Mumbai',
        'state': 'Maharashtra',
        'pincode': '400001',
        'qualification': 'B.Sc Computer Science',
        'specialization': 'Data Science',
        'address': '123, Main Street, Mumbai',
        'father_name': 'Rajesh Kumar',
        'father_phone': '9876543211',
        'mother_name': 'Sunita Kumar',
        'mother_phone': '9876543212'
    }
    
    return jsonify(mock_profile)

@app.route('/api/update_student_profile', methods=['POST'])
def update_student_profile():
    data = request.get_json()
    print(f"📝 Updating profile for student: {data.get('email')}")
    
    return jsonify({
        'success': True,
        'message': 'Profile updated successfully'
    })

@app.route('/api/schedule_live_class', methods=['POST'])
def schedule_live_class():
    data = request.get_json()
    print(f"🎥 Scheduling live class: {data.get('title')} for course {data.get('course_id')}")
    
    return jsonify({
        'success': True,
        'message': 'Live class scheduled successfully',
        'class_id': 1
    })
@app.route('/api/teacher_live_classes', methods=['GET'])
def get_teacher_live_classes():
    email = request.args.get('email', '')
    print(f"🎥 Fetching live classes for teacher: {email}")
    
    # Mock data for live classes
    mock_classes = [
        {
            'id': 1,
            'course_id': 1,
            'course_name': 'Data Science Fundamentals',
            'title': 'Introduction to Python',
            'description': 'Learn Python basics for data science',
            'class_date': '2026-06-15',
            'start_time': '10:00 AM',
            'end_time': '11:30 AM',
            'meeting_link': 'https://meet.google.com/abc-defg-hij'
        },
        {
            'id': 2,
            'course_id': 1,
            'course_name': 'Data Science Fundamentals',
            'title': 'Data Visualization',
            'description': 'Learn matplotlib and seaborn',
            'class_date': '2026-06-18',
            'start_time': '02:00 PM',
            'end_time': '03:30 PM',
            'meeting_link': 'https://meet.google.com/klm-nopq-rst'
        },
        {
            'id': 3,
            'course_id': 2,
            'course_name': 'Python Programming',
            'title': 'Functions and Modules',
            'description': 'Understanding functions in Python',
            'class_date': '2026-06-20',
            'start_time': '11:00 AM',
            'end_time': '12:30 PM',
            'meeting_link': 'https://meet.google.com/uvw-xyz-abc'
        }
    ]
    
    return jsonify(mock_classes)

@app.route('/api/delete_live_class', methods=['POST'])
def delete_live_class():
    data = request.get_json()
    print(f"🗑️ Deleting live class {data.get('class_id')}")
    
    return jsonify({
        'success': True,
        'message': 'Live class deleted successfully'
    })

@app.route('/api/teacher_payment_requests', methods=['GET'])
def get_teacher_payment_requests():
    email = request.args.get('email', '')
    print(f"💰 Fetching payment requests for teacher: {email}")
    
    # Mock data
    mock_requests = [
        {
            'id': 1,
            'course_id': 1,
            'course_name': 'Data Science Fundamentals',
            'student_id': 1,
            'student_name': 'Rahul Sharma',
            'amount': 2000,
            'requested_date': '12 Jun 2026'
        },
        {
            'id': 2,
            'course_id': 2,
            'course_name': 'Python Programming',
            'student_id': 2,
            'student_name': 'Priya Patel',
            'amount': 1500,
            'requested_date': '11 Jun 2026'
        }
    ]
    
    return jsonify(mock_requests)

@app.route('/api/teacher_payment_history', methods=['GET'])
def get_teacher_payment_history():
    email = request.args.get('email', '')
    print(f"💰 Fetching payment history for teacher: {email}")
    
    # Mock data
    mock_history = [
        {
            'id': 1,
            'course_name': 'Web Development',
            'student_name': 'Amit Kumar',
            'amount': 2500,
            'paid_date': '10 Jun 2026'
        },
        {
            'id': 2,
            'course_name': 'Data Science',
            'student_name': 'Neha Singh',
            'amount': 2000,
            'paid_date': '05 Jun 2026'
        }
    ]
    
    return jsonify(mock_history)

@app.route('/api/mark_payment_received', methods=['POST'])
def mark_payment_received():
    data = request.get_json()
    print(f"✅ Marking payment {data.get('payment_id')} as received")
    
    return jsonify({
        'success': True,
        'message': 'Payment marked as received'
    })

@app.route('/api/my_offline_requests', methods=['GET'])
def get_my_offline_requests():
    email = request.args.get('email', '')
    print(f"📋 Fetching offline requests for student: {email}")
    
    user_requests = [r for r in offline_requests if r.get('student_email') == email]
    return jsonify(user_requests)

@app.route('/api/register', methods=['POST'])
def mobile_register():
    data = request.get_json()
    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "user_id": 123
    })

@app.route('/api/student_register', methods=['POST'])
def student_register():
    data = request.get_json()
    print(f"🎓 New Student Registration: {data.get('email')}")
    return jsonify({
        "success": True,
        "message": "Student registered successfully",
        "user_id": 123
    })

@app.route('/api/teacher_register', methods=['POST'])
def teacher_register():
    data = request.get_json()
    print(f"👨‍🏫 New Teacher Registration: {data.get('email')}")
    return jsonify({
        "success": True,
        "message": "Teacher registered successfully",
        "teacher_id": 456
    })

@app.route('/api/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    print(f"📝 New Feedback from {data.get('user_name')} (Rating: {data.get('rating')})")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Insert into feedback table
    cur.execute("""
        INSERT INTO feedback (user_name, user_email, user_type, rating, title, description, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, 'pending', NOW())
    """, (
        data.get('user_name'), data.get('user_email'), data.get('user_role'),
        data.get('rating'), data.get('title'), data.get('description')
    ))
    
    conn.commit()
    feedback_id = cur.lastrowid
    cur.close()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Feedback submitted successfully!',
        'feedback_id': feedback_id
    })

# ==================== TEACHERS ====================
@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    return jsonify([
        {
            "id": 1,
            "name": "Rajesh Sharma",
            "subject": "Mathematics",
            "experience": 8,
            "city": "Mumbai",
            "monthly_fee": 2500,
            "hourly_fee": 350,
            "rating": 4.8,
            "email": "rajesh@teacher.com",
            "phone": "+91 98765 43210"
        },
        {
            "id": 2,
            "name": "Priya Patel",
            "subject": "Physics",
            "experience": 5,
            "city": "Delhi",
            "monthly_fee": 2000,
            "hourly_fee": 300,
            "rating": 4.7,
            "email": "priya@teacher.com",
            "phone": "+91 98765 43211"
        },
        {
            "id": 3,
            "name": "Amit Kumar",
            "subject": "Chemistry",
            "experience": 10,
            "city": "Bangalore",
            "monthly_fee": 3000,
            "hourly_fee": 400,
            "rating": 4.9,
            "email": "amit@teacher.com",
            "phone": "+91 98765 43212"
        }
    ])

# ==================== TUITION REQUESTS ====================
@app.route('/api/post_request', methods=['POST'])
def post_tuition_request():
    data = request.get_json()
    print(f"📝 New request from {data.get('student_email')}")
    
    new_request = {
        'id': len(tuition_requests) + 1,
        'student_name': data.get('student_name', 'Student'),
        'student_email': data.get('student_email', ''),
        'subject': data.get('subject', 'Not specified'),
        'class_level': data.get('class_level', 'Not specified'),
        'location': data.get('location', 'Not specified'),
        'budget': data.get('budget', 'Negotiable'),
        'timing': data.get('timing', 'Flexible'),
        'status': 'pending',
        'created_at': str(datetime.now())
    }
    tuition_requests.append(new_request)
    
    print(f"✅ Request saved. Total requests: {len(tuition_requests)}")
    
    return jsonify({
        'success': True,
        'message': 'Tuition request posted successfully',
        'request_id': new_request['id']
    })

@app.route('/api/my_requests', methods=['GET'])
def get_my_requests():
    email = request.args.get('email', '')
    user_requests = [r for r in tuition_requests if r.get('student_email') == email]
    return jsonify(user_requests)

@app.route('/api/all_requests', methods=['GET'])
def get_all_requests():
    print(f"📋 Returning {len(tuition_requests)} total requests")
    pending = [r for r in tuition_requests if r.get('status') == 'pending']
    return jsonify(pending)

@app.route('/api/accept_request', methods=['POST'])
def accept_request():
    data = request.get_json()
    request_id = data.get('request_id')
    teacher_email = data.get('teacher_email')
    
    for req in tuition_requests:
        if req['id'] == request_id:
            req['status'] = 'accepted'
            req['accepted_by'] = teacher_email
            print(f"✅ Request {request_id} accepted by {teacher_email}")
            return jsonify({
                'success': True,
                'message': 'Student contact: student@example.com, Phone: 9876543210'
            })
    
    return jsonify({'success': False, 'message': 'Request not found'}), 404

@app.route('/api/accepted_students', methods=['GET'])
def get_accepted_students():
    email = request.args.get('email', '')
    print(f"📋 Fetching accepted students for teacher: {email}")
    
    accepted_students = [
        {
            "id": 1,
            "student_name": "Rahul Sharma",
            "student_email": "rahul@student.com",
            "student_phone": "+91 98765 12345",
            "subject": "Mathematics",
            "class_level": "10th",
            "location": "Mumbai",
            "budget": "2000/month",
            "request_id": 101,
            "demo_status": "pending",
            "accepted_date": "2024-01-15"
        }
    ]
    return jsonify(accepted_students)

@app.route('/api/mark_enrolled', methods=['POST'])
def mark_enrolled():
    data = request.get_json()
    print(f"✅ Marking student as enrolled for request {data.get('request_id')}")
    return jsonify({"success": True, "message": "Student marked as enrolled"})

# ==================== COURSES ====================
@app.route('/api/post_course', methods=['POST'])
def post_course():
    data = request.get_json()
    print(f"📚 New Course: {data.get('title')} by {data.get('teacher_name')}")
    
    new_course = {
        'id': len(courses) + 1,
        'title': data.get('title'),
        'subject': data.get('subject'),
        'description': data.get('description'),
        'start_date_time': data.get('start_date_time'),
        'monthly_fee': data.get('monthly_fee'),
        'hourly_fee': data.get('hourly_fee'),
        'teacher_name': data.get('teacher_name'),
        'teacher_email': data.get('teacher_email'),
        'status': 'upcoming',
        'enrolled_students': 0,
    }
    courses.append(new_course)
    
    return jsonify({'success': True, 'message': 'Course posted successfully', 'course_id': new_course['id']})

@app.route('/api/all_courses', methods=['GET'])
def get_all_courses_endpoint():
    upcoming = [c for c in courses if c.get('status') == 'upcoming']
    print(f"📚 Returning {len(upcoming)} courses")
    return jsonify(upcoming)

@app.route('/api/enroll_course', methods=['POST'])
def enroll_course():
    data = request.get_json()
    course_id = data.get('course_id')
    student_email = data.get('student_email')
    student_name = data.get('student_name')
    
    print(f"📝 Student {student_name} enrolling in course {course_id}")
    
    for course in courses:
        if course['id'] == course_id:
            course['enrolled_students'] = course.get('enrolled_students', 0) + 1
            break
    
    enrollments.append({
        'course_id': course_id,
        'student_email': student_email,
        'student_name': student_name,
        'enrolled_at': str(datetime.now())
    })
    
    return jsonify({'success': True, 'message': 'Successfully enrolled in course'})

@app.route('/api/unlock_contact', methods=['POST'])
def unlock_contact():
    data = request.get_json()
    print(f"🔓 Unlock contact for teacher {data.get('teacher_id')}")
    return jsonify({
        "success": True,
        "message": "Contact unlocked successfully",
        "phone": "+91 98765 43210",
        "email": "teacher@example.com"
    })

@app.route('/api/create_point_order', methods=['POST'])
def create_point_order():
    data = request.get_json()
    points = data.get('points')
    amount = data.get('amount')
    student_email = data.get('student_email')
    
    print(f"💰 Point order: {points} points for ₹{amount}")
    
    # For now, return mock order
    return jsonify({
        'success': True,
        'order_id': 'order_' + str(hash(str(data))),
        'key_id': 'rzp_test_123456789',
        'amount': amount * 100
    })

# Store student points in memory (temporary)
student_points = {}

@app.route('/api/add_points', methods=['POST'])
def add_points():
    data = request.get_json()
    student_email = data.get('student_email')
    points = data.get('points')
    
    print(f"💰 Adding {points} points to {student_email}")
    
    # Initialize if not exists
    if student_email not in student_points:
        student_points[student_email] = 0
    
    student_points[student_email] += points
    
    return jsonify({
        'success': True,
        'message': f'{points} points added! Total points: {student_points[student_email]}',
        'points': student_points[student_email]
    })

@app.route('/api/get_student_points', methods=['GET'])
def get_student_points():
    email = request.args.get('email', '')
    print(f"📊 Fetching points for student: {email}")
    
    points = student_points.get(email, 0)
    
    return jsonify({
        'success': True,
        'points': points
    })

@app.route('/api/extend_trial', methods=['POST'])
def extend_trial():
    data = request.get_json()
    print(f"⏰ Extending trial for enrollment {data.get('enrollment_id')}")
    
    return jsonify({
        'success': True,
        'message': 'Trial extended successfully'
    })

@app.route('/api/schedule_demo', methods=['POST'])
def schedule_demo():
    data = request.get_json()
    print(f"📅 Scheduling demo: {data.get('demo_date')}")
    
    return jsonify({
        'success': True,
        'message': 'Demo scheduled successfully'
    })

@app.route('/api/course_enrolled_students', methods=['GET'])
def get_course_enrolled_students():
    course_id = request.args.get('course_id', '')
    print(f"📚 Fetching enrolled students for course {course_id}")
    
    # Mock data
    mock_students = [
        {
            'id': 1,
            'student_name': 'Rahul Sharma',
            'student_email': 'rahul@student.com',
            'payment_status': 'trial'
        },
        {
            'id': 2,
            'student_name': 'Priya Patel',
            'student_email': 'priya@student.com',
            'payment_status': 'paid'
        }
    ]
    
    return jsonify(mock_students)

@app.route('/api/update_course', methods=['POST'])
def update_course():
    data = request.get_json()
    print(f"📝 Updating course {data.get('course_id')}")
    
    return jsonify({
        'success': True,
        'message': 'Course updated successfully'
    })

@app.route('/api/delete_course', methods=['POST'])
def delete_course():
    data = request.get_json()
    print(f"🗑️ Deleting course {data.get('course_id')}")
    
    return jsonify({
        'success': True,
        'message': 'Course deleted successfully'
    })

@app.route('/api/student_change_password', methods=['POST'])
def student_change_password():
    data = request.get_json()
    email = data.get('email')
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    print(f"🔑 Student changing password for: {email}")
    
    # In production, verify current password and update
    return jsonify({
        'success': True,
        'message': 'Password changed successfully'
    })
    
@app.route('/api/my_enrolled_courses', methods=['GET'])
def get_my_enrolled_courses():
    email = request.args.get('email', '')
    print(f"📚 Fetching enrolled courses for student: {email}")
    
    # Return mock enrolled courses with different statuses
    return jsonify([
        {
            "id": 1,
            "title": "Mathematics Masterclass",
            "subject": "Mathematics",
            "description": "Complete mathematics course for 10th grade",
            "start_date_time": "2026-06-01T10:00:00",
            "monthly_fee": 2000,
            "hourly_fee": 250,
            "teacher_name": "Rajesh Sharma",
            "teacher_email": "rajesh@teacher.com",
            "status": "upcoming",
            "enrolled_students": 15
        },
        {
            "id": 2,
            "title": "Physics Fundamentals",
            "subject": "Physics",
            "description": "Learn physics concepts with practical examples",
            "start_date_time": "2026-05-20T14:00:00",
            "monthly_fee": 2500,
            "hourly_fee": 300,
            "teacher_name": "Priya Patel",
            "teacher_email": "priya@teacher.com",
            "status": "upcoming",
            "enrolled_students": 8
        }
    ])

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 HomeTutorHub API Server")
    print("📍 http://127.0.0.1:5000")
    print("=" * 50)
    print("\n📋 Available Endpoints:")
    print("   POST /api/login")
    print("   POST /api/register")
    print("   POST /api/student_register")
    print("   POST /api/teacher_register")
    print("   GET  /api/teachers")
    print("   POST /api/post_request")
    print("   GET  /api/my_requests")
    print("   GET  /api/all_requests")
    print("   POST /api/accept_request")
    print("   GET  /api/accepted_students")
    print("   POST /api/mark_enrolled")
    print("   POST /api/post_course")
    print("   GET  /api/all_courses")
    print("   POST /api/enroll_course")
    print("   POST /api/unlock_contact")
    print("\n✅ Ready for connections!\n")
    app.run(debug=True, host='0.0.0.0', port=5000)