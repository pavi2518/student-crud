from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, db
from flask_cors import CORS
import os, json

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all domains and routes

# Initialize Firebase
if os.path.exists('serviceAccountKey.json'):
    cred = credentials.Certificate('serviceAccountKey.json')
else:
    sa_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
    if not sa_json:
        raise RuntimeError("Firebase credentials not found. Provide serviceAccountKey.json or FIREBASE_SERVICE_ACCOUNT env var.")
    cred = credentials.Certificate(json.loads(sa_json))

firebase_db_url = os.environ.get('FIREBASE_DB_URL', 'https://student-crud-36bc3-default-rtdb.firebaseio.com/')
firebase_admin.initialize_app(cred, {'databaseURL': firebase_db_url})

students_ref = db.reference('students')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    new_ref = students_ref.push(data)
    return jsonify({"id": new_ref.key}), 201

@app.route('/students', methods=['GET'])
def list_students():
    snapshot = students_ref.get() or {}
    return jsonify(snapshot)

@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    student = students_ref.child(student_id).get()
    if not student:
        return jsonify({"error": "Not found"}), 404
    return jsonify(student)

@app.route('/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    students_ref.child(student_id).update(data)
    return jsonify({"id": student_id})

@app.route('/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    students_ref.child(student_id).delete()
    return jsonify({"id": student_id})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
