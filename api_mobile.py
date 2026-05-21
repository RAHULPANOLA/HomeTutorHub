from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime as DateTime

app = Flask(__name__)
CORS(app)  # Important: Allows Flutter app to connect

# Database connection (use your existing config)
db = mysql.connector.connect(
    host="localhost",
    user="root",           # Just "root", not "root@localhost"
    password="",           # Empty password for XAMPP default
    database="hometuto_teacher_portal"
)

@app.route('/api/login', methods=['POST'])
def mobile_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    
    if user:
        return jsonify({"success": True, "user": user})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM teachers WHERE is_verified = 1")
    teachers = cursor.fetchall()
    return jsonify(teachers)

# You will add more APIs (register, post request, accept request, etc.) later
@app.route('/api/teacher_register', methods=['POST'])
def teacher_register():
    data = request.get_json()
    print(f"Teacher registration: {data.get('email')}")
    
    # TODO: Save to your MySQL database
    return jsonify({
        "success": True,
        "message": "Teacher registered successfully",
        "teacher_id": 123
    })

# Store requests in memory
tuition_requests = []

@app.route('/api/post_request', methods=['POST'])
def post_tuition_request():
    data = request.get_json()
    
    new_request = {
        'id': len(tuition_requests) + 1,
        'student_name': data.get('student_name'),
        'student_email': data.get('student_email'),
        'subject': data.get('subject'),
        'class_level': data.get('class_level'),
        'location': data.get('location'),
        'budget': data.get('budget'),
        'timing': data.get('timing'),
        'status': 'pending',
        'created_at': str(DateTime.now())
    }
    tuition_requests.append(new_request)
    
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
    return jsonify([r for r in tuition_requests if r.get('status') == 'pending'])

@app.route('/api/accept_request', methods=['POST'])
def accept_request():
    data = request.get_json()
    request_id = data.get('request_id')
    teacher_email = data.get('teacher_email')
    
    for req in tuition_requests:
        if req['id'] == request_id:
            req['status'] = 'accepted'
            req['accepted_by'] = teacher_email
            return jsonify({
                'success': True,
                'message': 'Request accepted! Student contact: student@example.com, Phone: 9876543210'
            })
    
    return jsonify({'success': False, 'message': 'Request not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)