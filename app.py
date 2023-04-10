from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
conn = sqlite3.connect('complaints.db')
c = conn.cursor()

# Login route
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    
    # Check if user with given email and password exists
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    
    if not user:
        return render_template('login.html', error='Invalid email or password')
    
    if role == 'admin':
        # Check if user is an admin
        c.execute("SELECT * FROM admins WHERE user_id=?", (user[0],))
        admin = c.fetchone()
        
        if not admin:
            return render_template('login.html', error='Invalid role selected')
        
        return redirect(url_for('admin', user_id=user[0]))
    
    elif role == 'department':
        # Check if user is a department account
        c.execute("SELECT * FROM departments WHERE user_id=?", (user[0],))
        department = c.fetchone()
        
        if not department:
            return render_template('login.html', error='Invalid role selected')
        
        return redirect(url_for('department', user_id=user[0]))
    
    else:
        return render_template('login.html', error='Invalid role selected')
    
# User complaint registration route
@app.route('/user/complaint-registration', methods=['GET', 'POST'])
def user_complaint_registration():
    if request.method == 'POST':
        reg_no = request.form['reg_no']
        
        # Check if reg no exists in users table
        c.execute("SELECT * FROM users WHERE reg_no=?", (reg_no,))
        user = c.fetchone()
        
        if not user:
            return render_template('user_complaint_registration.html', error='Invalid registration number')
        
        # Add complaint to complaints table
        nature_of_complaint = request.form['nature_of_complaint']
        departments_concerned = request.form['departments_concerned']
        room_no = request.form['room_no']
        hostel_no = request.form['hostel_no']
        details = request.form['details']
        
        c.execute("INSERT INTO complaints (user_id, nature_of_complaint, departments_concerned, room_no, hostel_no, details) VALUES (?, ?, ?, ?, ?, ?)", (user[0], nature_of_complaint, departments_concerned, room_no, hostel_no, details))
        complaint_id = c.lastrowid
        
        conn.commit()
        
        return redirect(url_for('user_complaint_status', reg_no=reg_no, complaint_id=complaint_id))
    
    return render_template('user_complaint_registration.html')

# User complaint status route
@app.route('/user/complaint-status')
def user_complaint_status():
    reg_no = request.args.get('reg_no')
    complaint_id = request.args.get('complaint_id')
    
    # Check if complaint with given reg no and complaint id exists
    c.execute("SELECT * FROM complaints WHERE user_id=? AND id=?", (reg_no, complaint_id))
    complaint = c.fetchone()
    
    if not complaint:
        return render_template('user_complaint_status.html', error='Invalid complaint details')
    
    return render_template('user_complaint_status.html', complaint=complaint)

# Admin dashboard route
@app.route('/admin/dashboard')
def admin_dashboard():
    # Verify user is logged in as admin
    if 'email' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    # Get all complaints from database
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', complaints=complaints)

# department dashboard route
@app.route('/department/dashboard', methods=['GET', 'POST'])
def department_dashboard(dept_name):
    if request.method == 'POST':
        # get the complaint id and action from the form
        complaint_id = request.form['complaint_id']
        action = request.form['action']

        # update the status of the complaint in the database
        c.execute("UPDATE complaints SET status=? WHERE id=?", (action, complaint_id))
        conn.commit()

    # get all the complaints assigned to this department
    c.execute("SELECT * FROM complaints WHERE dept_assigned=?", (dept_name,))
    complaints = c.fetchall()

    return render_template('department.html', dept_name=dept_name, complaints=complaints)

if __name__ == '__main__':
    app.run(debug=True)