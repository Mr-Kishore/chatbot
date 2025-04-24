# --- IMPORTANT WARNING ---
# This is a highly simplified conceptual example for illustration ONLY.
# It LACKS:
# - Real authentication (uses mock login)
# - Real database integration (uses a Python dictionary)
# - Real AI/NLP (uses basic keyword matching)
# - Proper error handling & input validation
# - Security best practices (HTTPS, rate limiting, CSRF protection etc.)
# - Scalability features
# 
# --- --- --- --- --- --- --

from flask import Flask, request, jsonify, session
from flask_cors import CORS # Import CORS
import os

# Initialize Flask app
app = Flask(__name__)

# --- VERY IMPORTANT FOR FRONTEND INTERACTION ---
# Enable CORS (Cross-Origin Resource Sharing) to allow requests
# from your HTML file (served from a different origin - file:// or localhost:xxxx)
# For production, restrict the origins allowed.
CORS(app, supports_credentials=True, origins=["null", "http://127.0.0.1", "http://localhost"]) # Allow file:// (null) and common local dev origins

# Secret key is needed for session management
# Use a strong, random, persistent key in a real application.
# Keep this secret! Don't commit it directly into version control.
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-replace-in-prod') # Example: Get from env var or use default

# Configure session cookie settings for better security (optional but recommended)
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set to True if using HTTPS
    SESSION_COOKIE_HTTPONLY=True, # Prevent client-side JS access
    SESSION_COOKIE_SAMESITE='Lax', # Mitigate CSRF - 'Strict' can be too restrictive sometimes
)


# --- Mock Data Store ---
# In a real application, this would be a secure database (SQL, NoSQL).
MOCK_EMPLOYEE_DATA = {
    "23UIT015": {
        "name": "Kishore",
        "department": "Intern",
        "leave_balance": {"vacation": 12, "sick": 8},
        "performance_review_date": "2025-01-15",
        "contact": "kishore@example.com",
    },
    "E456": {
        "name": "vijay",
        "department": "Internn",
        "leave_balance": {"vacation": 10, "sick": 5},
        "performance_review_date": "2024-12-20",
        "contact": "vj@example.com",
    },
     "E789": {
        "name": "Charlie Chaplin",
        "department": "Entertainment",
        "leave_balance": {"vacation": 20, "sick": 10},
        "performance_review_date": "2025-03-01",
        "contact": "charlie@example.com",
    }
}

# --- Mock User Database for Login ---
# In reality, use an Identity Provider (LDAP, Azure AD, Okta etc.)
MOCK_USERS = {
    "kishore@example.com": {"password": "password123", "employee_id": "23UIT015"},
    "vj@example.com": {"password": "password456", "employee_id": "23USC045"},
    "charlie@example.com": {"password": "password789", "employee_id": "E789"},
}

# --- Mock Admin User ---
MOCK_ADMIN_USERS = {
    "admin@example.com": {"password": "adminpassword"}
}

# --- Helper Functions ---

def get_employee_data(employee_id, field_query):
    """
    Simulates retrieving specific data for ONE employee.
    THIS IS THE CRITICAL PRIVACY FUNCTION.
    It ONLY accesses data for the provided employee_id.
    """
    # Basic input validation
    if not isinstance(field_query, str):
        return "Invalid query format."

    if employee_id not in MOCK_EMPLOYEE_DATA:
        # Avoid revealing if the ID exists or not in error messages if possible
        return "Could not retrieve data. Please check your access or contact support."

    employee_info = MOCK_EMPLOYEE_DATA[employee_id]
    query_lower = field_query.lower()

    # Very basic "NLP" - just matching keywords to fields
    # Add more keywords/logic as needed
    if "leave" in query_lower:
        if "vacation" in query_lower:
            return f"Your vacation leave balance is: {employee_info['leave_balance'].get('vacation', 'N/A')} days."
        elif "sick" in query_lower:
            return f"Your sick leave balance is: {employee_info['leave_balance'].get('sick', 'N/A')} days."
        else:
             return f"Your total leave balances are: Vacation {employee_info['leave_balance'].get('vacation', 'N/A')}, Sick {employee_info['leave_balance'].get('sick', 'N/A')}."
    elif "review" in query_lower or "performance" in query_lower:
        return f"Your last performance review date was: {employee_info.get('performance_review_date', 'N/A')}"
    elif "department" in query_lower:
         return f"You are in the {employee_info.get('department', 'N/A')} department."
    elif "name" in query_lower:
         # Usually users know their own name, but included for example
         return f"Your name is recorded as {employee_info.get('name', 'N/A')}."
    elif "contact" in query_lower or "email" in query_lower:
         return f"Your contact email is {employee_info.get('contact', 'N/A')}."
    elif "help" in query_lower:
        return "You can ask me about your 'leave balance' (vacation or sick), 'performance review' date, 'department', or 'contact' information."
    else:
        # Fallback response
        return "Sorry, I can only answer questions about leave, reviews, department, or contact info. Try asking 'help'."

def get_all_employee_details_for_admin(employee_id):
    """
    Admin function: Retrieves ALL details for a specific employee.
    Still restricted to one employee at a time based on ID provided by admin.
    """
    if employee_id not in MOCK_EMPLOYEE_DATA:
        return {"error": f"Employee data not found for ID: {employee_id}."}
    # Return a copy to prevent accidental modification of the mock data
    return MOCK_EMPLOYEE_DATA[employee_id].copy()

# --- API Endpoints ---

@app.route('/login', methods=['POST'])
def login():
    """Mock Login Endpoint - NOT SECURE"""
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user_info = MOCK_USERS.get(username)
    admin_info = MOCK_ADMIN_USERS.get(username)

    if user_info and user_info['password'] == password:
        # Clear any previous session data
        session.clear()
        # Store employee_id in session - this links the session to the user
        session['employee_id'] = user_info['employee_id']
        session['role'] = 'employee'
        app.logger.info(f"Employee login successful: {username}")
        return jsonify({"message": "Login successful", "role": "employee"}), 200
    elif admin_info and admin_info['password'] == password:
        session.clear()
        session['role'] = 'admin'
        # Admins don't have an employee_id tied to their session directly
        app.logger.info(f"Admin login successful: {username}")
        return jsonify({"message": "Admin login successful", "role": "admin"}), 200
    else:
        app.logger.warning(f"Failed login attempt for username: {username}")
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    """Logs the user out by clearing the session"""
    # Log the logout attempt
    role = session.get('role', 'unknown')
    user_id = session.get('employee_id', 'N/A') if role == 'employee' else 'admin'
    app.logger.info(f"Logout attempt for role: {role}, user: {user_id}")

    session.clear() # Clear the session data
    return jsonify({"message": "Logout successful"}), 200

@app.route('/ask', methods=['POST'])
def ask_chatbot():
    """Endpoint for employees to ask questions."""
    # Check if user is logged in as an employee via session
    if session.get('role') != 'employee' or 'employee_id' not in session:
        app.logger.warning(f"Unauthorized chatbot access attempt. Session data: {session}")
        return jsonify({"error": "Authentication required. Please log in."}), 401

    employee_id = session['employee_id'] # Get ID from secure session

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    query = data.get('query')

    if not query or not isinstance(query, str) or len(query.strip()) == 0:
        return jsonify({"error": "Query parameter is missing or empty"}), 400

    # --- CRITICAL STEP ---
    # Pass the *authenticated employee's ID* to the data retrieval function.
    # This ensures data segregation.
    app.logger.info(f"Chat query from employee {employee_id}: '{query}'")
    response_text = get_employee_data(employee_id, query.strip())
    # --- --- --- --- ---

    return jsonify({"response": response_text})

@app.route('/admin/view_employee', methods=['GET'])
def admin_view_employee():
    """Endpoint for admins to view specific employee details."""
    # Check if user is logged in as an admin via session
    if session.get('role') != 'admin':
        app.logger.warning(f"Unauthorized admin access attempt (view_employee). Session data: {session}")
        return jsonify({"error": "Admin privileges required. Please log in as admin."}), 403

    # Admin needs to specify which employee ID to view via query parameter
    employee_id_to_view = request.args.get('employee_id')

    if not employee_id_to_view:
        return jsonify({"error": "employee_id query parameter is required for admin view"}), 400

    # Retrieve all details for the specified employee
    # In a real system, you'd also log this admin action for auditing.
    app.logger.info(f"Admin request to view details for employee: {employee_id_to_view}")
    employee_details = get_all_employee_details_for_admin(employee_id_to_view)

    # Check if the helper function returned an error
    if 'error' in employee_details:
         app.logger.warning(f"Admin view failed for employee {employee_id_to_view}: {employee_details['error']}")
         return jsonify(employee_details), 404 # Not Found

    return jsonify(employee_details)

@app.route('/admin/list_employees', methods=['GET'])
def admin_list_employees():
    """Endpoint for admins to get a list of employee IDs and names."""
    if session.get('role') != 'admin':
        app.logger.warning(f"Unauthorized admin access attempt (list_employees). Session data: {session}")
        return jsonify({"error": "Admin privileges required."}), 403

    # In a real app, query the database for IDs and names.
    # Avoid loading ALL data into memory if the list is large.
    app.logger.info("Admin request to list employees.")
    employee_list = [
        {"id": eid, "name": data.get("name", "N/A")}
        for eid, data in MOCK_EMPLOYEE_DATA.items()
    ]
    return jsonify({"employees": employee_list})


# --- Basic Root Route (Optional) ---
@app.route('/')
def index():
    # Simple check to see if the server is running
    return "Chatbot backend is running."

# --- Run the App (for local development) ---
if __name__ == '__main__':
    # Important: Use a proper WSGI server (like Gunicorn or Waitress) in production.
    # Run with debug=False in production.
    # Ensure HTTPS is configured in production.
    # Enable basic logging
    import logging
    logging.basicConfig(level=logging.INFO)

    # Run on port 5001 to avoid conflict with common port 5000
    # Host '0.0.0.0' makes it accessible on your local network (use '127.0.0.1' for localhost only)
    app.run(host='0.0.0.0', port=5001, debug=True) # debug=True enables auto-reload and more detailed errors
