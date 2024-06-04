import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client['attendance_db']
collection = db['attendance']

def add_attendance(name, date, status):
    try:
        record = {
            "name": name,
            "date": date.strftime('%Y-%m-%d'),
            "status": status
        }
        collection.insert_one(record)
        return True
    except Exception as e:
        st.error(f"Error adding attendance: {e}")
        return False

def get_attendance():
    try:
        records = list(collection.find({}, {"_id": 0}))
        return records if records else None
    except Exception as e:
        st.error(f"Error fetching attendance records: {e}")
        return None

def get_attendance_percentage(name):
    try:
        total_records = collection.count_documents({"name": name})
        present_records = collection.count_documents({"name": name, "status": "Present"})
        if total_records == 0:
            return 0
        else:
            return (present_records / total_records) * 100
    except Exception as e:
        st.error(f"Error calculating attendance percentage: {e}")
        return None

def welcome():
    st.title('Welcome to Attendance Management System')
    st.write('Please register your attendance or view records.')

def register():
    st.title('Register Attendance')
    with st.form(key='attendance_form'):
        name = st.text_input('Name')
        date = st.date_input('Date', datetime.now())
        status = st.selectbox('Status', ['Present', 'Absent'])
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if name and date and status:
                success = add_attendance(name, date, status)
                if success:
                    st.success(f'Attendance for {name} on {date.strftime("%Y-%m-%d")} marked as {status}')
            else:
                st.error("Please fill in all the fields.")

def view_records():
    st.title('Attendance Records')
    records = get_attendance()
    if not records:
        st.write('No records found.')
    else:
        for record in records:
            st.write(f"Name: {record['name']}, Date: {record['date']}, Status: {record['status']}")

def view_attendance_percentage():
    st.title('Attendance Percentage')
    records = get_attendance()
    if not records:
        st.write('No records found.')
    else:
        names = list(set(record['name'] for record in records))
        for name in names:
            percentage = get_attendance_percentage(name)
            st.write(f"Name: {name}, Attendance Percentage: {percentage:.2f}%")

# Page navigation
pages = ['Welcome', 'Register', 'View Records', 'View Attendance Percentage']
selection = st.sidebar.radio('Go to', pages)

# Page selection
if selection == 'Welcome':
    welcome()
elif selection == 'Register':
    register()
elif selection == 'View Records':
    view_records()
elif selection == 'View Attendance Percentage':
    view_attendance_percentage()

client.close()