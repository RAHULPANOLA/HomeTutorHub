from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store requests in memory
tuition_requests = []

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

@app.route('/api/student_register', methods=['POST'])
def student_register():
    data = request.get_json()
    print(f"🎓 New Student Registration: {data.get('email')}")
    
    # TODO: Insert into students table
    # INSERT INTO students (full_name, email, password, phone, father_name, father_phone, 
    # mother_name, mother_phone, city, state, pincode, qualification, specialization, address)
    # VALUES (...)
    
    return jsonify({
        "success": True,
        "message": "Student registered successfully",
        "user_id": 123
    })

@app.route('/api/teacher_register', methods=['POST'])
def teacher_register():
    data = request.get_json()
    print(f"👨‍🏫 New Teacher Registration: {data.get('email')}")
    
    # Save Base64 images to files or store in database
    profile_photo = data.get('profile_photo', '')
    qualification_doc = data.get('qualification_doc', '')
    aadhaar_doc = data.get('aadhaar_doc', '')
    resume_doc = data.get('resume_doc', '')
    
    # TODO: Save to teachers table with document paths
    # Store Base64 strings in LONGTEXT columns or save as files
    
    return jsonify({
        "success": True,
        "message": "Teacher registered successfully",
        "teacher_id": 456
    })

@app.route('/api/post_request', methods=['POST'])
def post_tuition_request():
    data = request.get_json()
    print(f"📝 New request from {data.get('student_email')}")
    print(f"📝 Data received: {data}")
    
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

# ⭐ THIS IS THE MISSING ENDPOINT ⭐
@app.route('/api/all_requests', methods=['GET'])
def get_all_requests():
    print(f"📋 Returning {len(tuition_requests)} total requests")
    pending = [r for r in tuition_requests if r.get('status') == 'pending']
    print(f"📋 Pending requests: {len(pending)}")
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

@app.route('/api/my_requests', methods=['GET'])
def get_my_requests():
    email = request.args.get('email', '')
    user_requests = [r for r in tuition_requests if r.get('student_email') == email]
    return jsonify(user_requests)

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
        },
        {
            "id": 4,
            "name": "Neha Singh",
            "subject": "English",
            "experience": 6,
            "city": "Pune",
            "monthly_fee": 1800,
            "hourly_fee": 250,
            "rating": 4.6,
            "email": "neha@teacher.com",
            "phone": "+91 98765 43213"
        },
        {
            "id": 5,
            "name": "Suresh Rao",
            "subject": "Computer Science",
            "experience": 7,
            "city": "Hyderabad",
            "monthly_fee": 2800,
            "hourly_fee": 380,
            "rating": 4.8,
            "email": "suresh@teacher.com",
            "phone": "+91 98765 43214"
        }
    ])

@app.route('/api/unlock_contact', methods=['POST'])
def unlock_contact():
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    student_email = data.get('student_email')
    
    print(f"🔓 Unlock contact: Student {student_email} requesting teacher {teacher_id}")
    
    # TODO: Process ₹49 payment here
    
    return jsonify({
        "success": True,
        "message": "Contact unlocked successfully",
        "phone": "+91 98765 43210",
        "email": "teacher@example.com"
    })
@app.route('/api/accepted_students', methods=['GET'])
def get_accepted_students():
    email = request.args.get('email', '')
    print(f"📋 Fetching accepted students for teacher: {email}")
    
    # Mock data for accepted students
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
            "demo_status": "pending",  # pending or completed
            "accepted_date": "2024-01-15"
        },
        {
            "id": 2,
            "student_name": "Priya Patel",
            "student_email": "priya@student.com",
            "student_phone": "+91 98765 12346",
            "subject": "Physics",
            "class_level": "12th",
            "location": "Delhi",
            "budget": "2500/month",
            "request_id": 102,
            "demo_status": "completed",
            "accepted_date": "2024-01-10"
        },
        {
            "id": 3,
            "student_name": "Amit Kumar",
            "student_email": "amit@student.com",
            "student_phone": "+91 98765 12347",
            "subject": "Chemistry",
            "class_level": "11th",
            "location": "Bangalore",
            "budget": "2200/month",
            "request_id": 103,
            "demo_status": "pending",
            "accepted_date": "2024-01-18"
        }
    ]
    
    return jsonify(accepted_students)

@app.route('/api/mark_enrolled', methods=['POST'])
def mark_enrolled():
    data = request.get_json()
    request_id = data.get('request_id')
    teacher_email = data.get('teacher_email')
    
    print(f"✅ Marking student as enrolled for request {request_id}")
    
    return jsonify({
        "success": True,
        "message": "Student marked as enrolled"
    })

if __name__ == '__main__':
    print("🚀 HomeTutorHub API Server")
    print("📍 http://127.0.0.1:5000")
    print("\n📋 Available Endpoints:")
    print("   POST /api/login")
    print("   POST /api/register")
    print("   POST /api/post_request")
    print("   GET  /api/all_requests")  # ⭐ This should now work
    print("   POST /api/accept_request")
    print("   GET  /api/my_requests")
    print("\n✅ Ready for connections!\n")
    app.run(debug=True, host='127.0.0.1', port=5000)