import csv

# Path to student data CSV file
student_data_path = r"C:\Users\Admin\Desktop\Student_data.csv"

# Function to check if user is registered (based on email)
def is_user_registered(email):
    with open(student_data_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[3] == email:  # Assuming email is the 4th column in Student_data.csv
                return True
    return False

# Function to retrieve student data based on email
def get_user_by_email(email):
    with open(student_data_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[3] == email:  # Email match
                return row  # Return entire row for user details
    return None

# Function to register a new user
def register_user(user_data):
    with open(student_data_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(user_data)

# Function to validate login (just checks if email exists in CSV)
def validate_login(email):
    return is_user_registered(email)
