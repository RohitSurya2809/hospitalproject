from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configurations
DB_CONFIG = {
    'doctor': {
        'host': os.getenv('DOCTOR_DB_HOST', 'localhost'),
        'user': os.getenv('DOCTOR_DB_USER', 'root'),
        'password': os.getenv('DOCTOR_DB_PASSWORD', ''),
        'database': os.getenv('DOCTOR_DB_NAME', 'doctor_db')
    },
    'nurse': {
        'host': os.getenv('NURSE_DB_HOST', 'localhost'),
        'user': os.getenv('NURSE_DB_USER', 'root'),
        'password': os.getenv('NURSE_DB_PASSWORD', ''),
        'database': os.getenv('NURSE_DB_NAME', 'nurse_db')
    },
    'pharmacy': {
        'host': os.getenv('PHARMACY_DB_HOST', 'localhost'),
        'user': os.getenv('PHARMACY_DB_USER', 'root'),
        'password': os.getenv('PHARMACY_DB_PASSWORD', ''),
        'database': os.getenv('PHARMACY_DB_NAME', 'pharmacy_db')
    },
    'patient': {
        'host': os.getenv('PATIENT_DB_HOST', 'localhost'),
        'user': os.getenv('PATIENT_DB_USER', 'root'),
        'password': os.getenv('PATIENT_DB_PASSWORD', ''),
        'database': os.getenv('PATIENT_DB_NAME', 'patient_db')
    }
}

# Helper functions
def get_db_connection(role):
    """Create a database connection based on role"""
    if role not in DB_CONFIG:
        raise ValueError(f"Invalid role: {role}")
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG[role])
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to {role} database: {err}")
        raise

def validate_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    
    return True, ""

def sanitize_input(input_str):
    """Sanitize input to prevent SQL injection"""
    if input_str is None:
        return None
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[\'";]', '', input_str)
    return sanitized

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"success": False, "message": "Invalid request format. JSON required"}), 400
    
    data = request.json or {}
    
    # Extract and sanitize data
    name = sanitize_input(data.get('name'))
    email = sanitize_input(data.get('email'))
    password = data.get('password')
    role = sanitize_input(data.get('role'))
    
    # Validate inputs
    if not password or not isinstance(password, str):
        return jsonify({"success": False, "message": "Password is required and must be a string"}), 400
        
    if not all([name, email, role]):
        return jsonify({"success": False, "message": "All fields are required"}), 400
    
    if not validate_email(email):
        return jsonify({"success": False, "message": "Invalid email format"}), 400
    
    is_valid_password, password_message = validate_password(password)
    if not is_valid_password:
        return jsonify({"success": False, "message": password_message}), 400
    
    if role not in DB_CONFIG:
        return jsonify({"success": False, "message": "Invalid role"}), 400
    
    conn = None
    cursor = None
    try:
        # Connect to the appropriate database
        conn = get_db_connection(role)
        cursor = conn.cursor(dictionary=True)
        
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already registered"}), 409
        
        # Hash the password
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        except (TypeError, AttributeError) as e:
            return jsonify({"success": False, "message": "Invalid password format"}), 400
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (name, email, hashed_password, role)
        )
        conn.commit()
        
        return jsonify({
            "success": True,
            "message": f"Registration successful as {role}"
        }), 201
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"success": False, "message": "Database error occurred"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"success": False, "message": "Invalid request format. JSON required"}), 400
        
    data = request.json or {}
    
    # Extract and sanitize data
    email = sanitize_input(data.get('email'))
    password = data.get('password')
    role = sanitize_input(data.get('role'))
    
    # Validate inputs
    if not password or not isinstance(password, str):
        return jsonify({"success": False, "message": "Password is required and must be a string"}), 400
        
    if not all([email, role]):
        return jsonify({"success": False, "message": "All fields are required"}), 400
    
    if role not in DB_CONFIG:
        return jsonify({"success": False, "message": "Invalid role"}), 400
    
    conn = None
    cursor = None
    try:
        # Connect to the appropriate database
        conn = get_db_connection(role)
        cursor = conn.cursor(dictionary=True)
        
        # Find user by email
        cursor.execute("SELECT * FROM users WHERE email = %s AND role = %s", (email, role))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"success": False, "message": "Invalid email or password"}), 401
        
        # Verify password
        try:
            if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                return jsonify({"success": False, "message": "Invalid email or password"}), 401
        except (TypeError, AttributeError) as e:
            return jsonify({"success": False, "message": "Invalid password format"}), 400
        
        # Create session or token (simplified for this example)
        return jsonify({
            "success": True,
            "message": f"Login successful as {role}",
            "user": {
                "id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "role": user['role']
            }
        }), 200
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"success": False, "message": "Database error occurred"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)