from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import MeanAbsoluteError
import numpy as np
import cv2
import cvlib as cv

# Load the pre-trained gender detection model
model = load_model('Gender&Age.h5', custom_objects={'mae': MeanAbsoluteError()})

# Classes for prediction
classes = ['man', 'woman']

# Gender dictionary for prediction
gender_dict = {0: 'Male', 1: 'Female'}

def detect_gender_and_age(frame):
    # Apply face detection
    faces, confidences = cv.detect_face(frame)

    if len(faces) == 0:
        return "No face detected", frame, 0, 0

    men_count = 0
    women_count = 0
    women_ages = []

    for idx, f in enumerate(faces):
        (startX, startY) = f[0], f[1]
        (endX, endY) = f[2], f[3]

        # Draw rectangle over the face
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

        # Crop the detected face region
        face_crop = np.copy(frame[startY:endY, startX:endX])

        if face_crop.shape[0] < 10 or face_crop.shape[1] < 10:
            continue

        # Preprocess for gender detection model
        face_crop_resized = cv2.resize(face_crop, (128, 128))
        face_crop_gray = cv2.cvtColor(face_crop_resized, cv2.COLOR_BGR2GRAY)
        face_crop_gray = face_crop_gray.reshape(1, 128, 128, 1) / 255.0

        # Apply gender detection
        pred = model.predict(face_crop_gray)

        # Predict gender and age
        pred_gender = gender_dict[round(pred[0][0][0])]
        conf_gender = pred[0][0][0]
        pred_age = round(pred[1][0][0])


        # Count men and women
        if pred_gender == 'Male':
            men_count += 1
        else:
            women_count += 1
            women_ages.append(pred_age)

        # Display gender and age on the frame
        label = f"{pred_gender}, Age: {pred_age}"
        Y = startY - 10 if startY - 10 > 10 else startY + 10

        # Write label and confidence above the face rectangle
        cv2.putText(frame, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return f"Men: {men_count}, Women: {women_count}", frame, men_count, women_count, women_ages
