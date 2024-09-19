from flask import Flask, render_template, Response, jsonify, request, redirect, url_for
import cv2
import requests
import threading 
import time
import numpy as np
from Gender_Model import detect_gender_and_age  # Import the updated detect_gender function
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',  
    'password': 'tana9861751892@',  
    'database': 'raja'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
    

@app.route('/')
def c():
    return render_template('xyz.html')

@app.route('/soss')
def soss():
    return render_template('sos.html')

@app.route('/xy')
def xy():
    return render_template('fast.html')


@app.route('/abc', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['user_id']
        password = request.form['password']
        type = request.form['type']

        connection = get_db_connection()
        if connection:
            if(type=='Authority'):
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM login WHERE userid = %s AND password = %s AND type = %s"
                cursor.execute(query, (userid, password,type))
                user = cursor.fetchone()
                cursor.close()
                connection.close()

                if user:
                    return redirect(url_for('index'))
                else:
                    return "Invalid username or password or type."
            else:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM login WHERE userid = %s AND password = %s AND type = %s"
                cursor.execute(query, (userid, password,type))
                user = cursor.fetchone()
                cursor.close()
                connection.close()

                if user:
                    return redirect(url_for('home'))
                else:
                    return "Invalid username or password or type."
    return render_template('fast.html')

@app.route('/home')
def home():
     return render_template('second.html')


# Global variables to hold counts
count_men = 0
count_women = 0
women_ages = []

frame_data = None
processing_frame = False
output_frame = None

# Function to capture camera feed and update frame_data
def capture_frame(camera):
    global frame_data, processing_frame

    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Lock the frame data while updating it
        if not processing_frame:
            frame_data = frame

        time.sleep(0.02)  # Add slight delay to limit the frame rate (50 fps)

# Function to process frames for gender and age detection
def process_frame():
    global frame_data, processing_frame, output_frame, count_men, count_women, women_ages

    while True:
        if frame_data is not None and not processing_frame:
            processing_frame = True

            # Detect gender and age, then annotate the frame
            label, annotated_frame, men_count, women_count, detected_women_ages = detect_gender_and_age(frame_data)
            
            # Update global counts and output frame
            count_men = men_count
            count_women = women_count
            women_ages = detected_women_ages
            output_frame = annotated_frame

            processing_frame = False

        time.sleep(0.05)  # Slight delay to control processing rate

# Main function to generate frame for streaming
def generate_frame():
    global output_frame

    # Access the local camera feed
    camera = cv2.VideoCapture(0)  # Use the default local camera (index 0)

    # Start a separate thread for capturing frames
    capture_thread = threading.Thread(target=capture_frame, args=(camera,))
    capture_thread.start()

    # Start a separate thread for processing frames
    processing_thread = threading.Thread(target=process_frame)
    processing_thread.start()

    while True:
        # Check if an output frame is available
        if output_frame is not None:
            frame = cv2.resize(output_frame, (640, 640))
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame as a multipart HTTP response (MJPEG format)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release the camera when done
    camera.release()


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gender_count')
def gender_count():
    # Calculate the ratio of women to men
    ratio = count_women / count_men if count_men > 0 else "N/A"
    if women_ages:
        min_age_women = min(women_ages)
        max_age_women = max(women_ages)
    else:
        min_age_women = "N/A"
        max_age_women = "N/A"
    return jsonify({'Men': count_men, 'Women': count_women, 'Ratio': ratio, 'Min_Women': min_age_women, 'Max_Women': max_age_women})

@app.route('/call', methods=['get'])
def call():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM login')
    login = cursor.fetchall()
    conn.close()
    return render_template('viewdatabase.html', login=login)


@app.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        station_name = request.form['station-name']
        booth_number = request.form['booth-number']
        location = request.form['location']
        import re 
        tel_number = request.form['telephone']
        def is_valid_phone_number(tel_number):
            # Remove any non-digit characters
            cleaned_number = re.sub(r'\D', '', tel_number)

            return len(cleaned_number)==10
        password = request.form['new-password']

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO login (STATION_NAME, BOOTH_NUMBER, LOCATION, TELEPHONE_NUMBER, PASSWORD) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (station_name, booth_number, location, tel_number, password))
                connection.commit()  # Commit the transaction
                cursor.close()
                return render_template('second.html')
            except Error as e:
                return f"Error inserting data: {e}"
            finally:
                connection.close()
        else:
            return "Database connection failed!"



if __name__ == '__main__':
    app.run(debug=True)
