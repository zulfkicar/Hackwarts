import sqlite3

# Connect to the main complaints database
conn = sqlite3.connect('complaints.db')
c = conn.cursor()

# Create the users table
c.execute('''
    CREATE TABLE users (
        reg_no INTEGER PRIMARY KEY,
        name TEXT
    )
''')

# Create the complaints table
c.execute('''
    CREATE TABLE complaints (
        complaint_id INTEGER PRIMARY KEY,
        reg_no INTEGER,
        nature_of_complaint TEXT,
        departments_concerned TEXT,
        room_no INTEGER,
        hostel_no INTEGER,
        details TEXT,
        status TEXT,
        FOREIGN KEY(reg_no) REFERENCES users(reg_no)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

# Connect to the admin database
conn = sqlite3.connect('admin.db')
c = conn.cursor()

# Create the admin table
c.execute('''
    CREATE TABLE admin (
        email TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
