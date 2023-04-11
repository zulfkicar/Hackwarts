from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
conn = sqlite3.connect('complaints.db')
c = conn.cursor()

# Login route
@app.route('/', methods=['GET','POST'])
@app.route('/main', methods=['GET','POST'])
def main_page():
    if request.method == 'POST':
        if request.form['action'] == 'register':
            reg_no=request.form['registration']
            # Check if reg no exists in users table
            c.execute("SELECT * FROM users WHERE reg_no=?", (reg_no,))
            user = c.fetchone()
            if user:
                return redirect(url_for('register_complaint', reg_no=reg_no))
            else:
                return render_template('main_page.html', error='Invalid registration number')
        elif request.form['action'] == 'track':
            tracking=request.form['tracking']
            reg_no=request.form['registration']
            return redirect(url_for('user_complaint_status', reg_no=reg_no, tracking=tracking))
    return render_template("main_page.html")
            
    
# User complaint registration route
@app.route('/register', methods=['GET','POST'])
def register_complaint():
    if request.method == 'POST':
        reg_no = request.args.get('reg_no')
        
        # Check if reg no exists in users table
        c.execute("SELECT * FROM users WHERE reg_no=?", (reg_no,))
        # Add complaint to complaints table
        nature_of_complaint = request.form['nature_of_complaint']
        departments_concerned = request.form['departments_concerned']
        room_no = request.form['room_no']
        hostel_no = request.form['hostel_no']
        details = request.form['details']
        
        c.execute("INSERT INTO complaints (user_id, nature_of_complaint, departments_concerned, room_no, hostel_no, details) VALUES (?, ?, ?, ?, ?, ?)", (user[0], nature_of_complaint, departments_concerned, room_no, hostel_no, details))
        complaint_id = c.lastrowid
        
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
conn = sqlite3.connect('complaints.db')
c = conn.cursor()

# Login route
@app.route('/', methods=['GET','POST'])
@app.route('/main', methods=['GET','POST'])
def main_page():
    if request.method == 'POST':
        if request.form['action'] == 'register':
            reg_no=request.form['registration']
            # Check if reg no exists in users table
            c.execute("SELECT * FROM users WHERE reg_no=?", (reg_no,))
            user = c.fetchone()
            if user:
                return redirect(url_for('register_complaint', reg_no=reg_no))
            else:
                return render_template('main_page.html', error='Invalid registration number')
        elif request.form['action'] == 'track':
            tracking=request.form['tracking']
            reg_no=request.form['registration']
            return redirect(url_for('user_complaint_status', reg_no=reg_no, tracking=tracking))
    return render_template("main_page.html")
            
    
# User complaint registration route
@app.route('/register', methods=['GET','POST'])
def register_complaint():
    if request.method == 'POST':
        reg_no = request.args.get('reg_no')
        
        # Check if reg no exists in users table
        c.execute("SELECT * FROM users WHERE reg_no=?", (reg_no,))
        user = c.fetchone()
        
        # Add complaint to complaints table
        nature_of_complaint = request.form['nature_of_complaint']
        departments_concerned = request.form['departments_concerned']
        room_no = request.form['room_no']
        hostel_no = request.form['hostel_no']
        details = request.form['details']
        
        c.execute("INSERT INTO complaints (reg_no, nature_of_complaint, departments_concerned, room_no, hostel_no, details) VALUES (?, ?, ?, ?, ?, ?)", (reg_no, nature_of_complaint, departments_concerned, room_no, hostel_no, details))
        complaint_id = c.lastrowid
        
        conn.commit()
        
        return redirect(url_for('complaint_status', reg_no=reg_no, complaint_id=complaint_id))
    
    return render_template('register_complaint.html')

# User complaint status route
@app.route('/tracking', methods=['GET','POST'])
def complaint_status():
    reg_no = request.args.get('reg_no')
    complaint_id = request.args.get('tracking')
    
    # Check if complaint with given reg no and complaint id exists
    c.execute("SELECT * FROM complaints WHERE reg_no=? AND complaint_id=?", (reg_no, complaint_id))
    complaint = c.fetchone()
    
    if not complaint:
        return render_template('complaint_status.html', error='Invalid complaint details')
    
    return render_template('complaint_status.html', complaint=complaint)




# # Admin dashboard route
# @app.route('/admin')
# def admin_dashboard():
#     # Verify user is logged in as admin
#     if 'email' not in session or session['role'] != 'admin':
#         return redirect(url_for('login'))

#     # Get all complaints from database
#     conn = sqlite3.connect('complaints.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM complaints")
#     complaints = cursor.fetchall()
#     conn.close()

#     return render_template('admin_dashboard.html', complaints=complaints)

# # department dashboard route
# @app.route('/department', methods=['GET', 'POST'])
# def department_dashboard(dept_name):
#     if request.method == 'POST':
#         # get the complaint id and action from the form
#         complaint_id = request.form['complaint_id']
#         action = request.form['action']

#         # update the status of the complaint in the database
#         c.execute("UPDATE complaints SET status=? WHERE id=?", (action, complaint_id))
#         conn.commit()

#     # get all the complaints assigned to this department
#     c.execute("SELECT * FROM complaints WHERE dept_assigned=?", (dept_name,))
#     complaints = c.fetchall()

#     return render_template('department.html', dept_name=dept_name, complaints=complaints)

if __name__ == '__main__':
    app.run(debug=True)
